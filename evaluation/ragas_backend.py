import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from prompts.prompt_loader import get_prompt_versions, render_prompt

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "evaluations.jsonl"
LOG_PATH = RESULTS_DIR / "evaluation.log"

try:
    from datasets import Dataset
    from openai import OpenAI
    from ragas import evaluate
    from ragas.llms import llm_factory
    from ragas.metrics import (
        AnswerRelevancy,
        ContextPrecision,
        ContextRecall,
        Faithfulness,
    )
    from sentence_transformers import SentenceTransformer
except Exception as exc:  # pragma: no cover - defensive import path
    Dataset = None
    OpenAI = None
    evaluate = None
    llm_factory = None
    AnswerRelevancy = ContextPrecision = ContextRecall = Faithfulness = None
    SentenceTransformer = None
    RAGAS_IMPORT_ERROR = exc
else:
    RAGAS_IMPORT_ERROR = None


class SimpleEmbeddings:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text])[0].tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(list(texts)).tolist()


def _normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _safe_answer_text(answer: Any) -> str:
    if isinstance(answer, dict):
        return json.dumps(answer, ensure_ascii=False, default=str)
    if answer is None:
        return ""
    return str(answer)


def _build_contexts(retrieved_docs: Optional[List[dict]]) -> List[str]:
    contexts: List[str] = []
    for doc in retrieved_docs or []:
        text = doc.get("abstract") or doc.get("text") or doc.get("title") or ""
        if text:
            contexts.append(text[:2500])
    return contexts


def _build_ground_truths(retrieved_docs: Optional[List[dict]]) -> List[str]:
    truths: List[str] = []
    for doc in retrieved_docs or []:
        title = doc.get("title") or ""
        abstract = doc.get("abstract") or doc.get("text") or ""
        combined = f"{title}\n{abstract}".strip()
        if combined:
            truths.append(combined[:2000])
    return truths


def _heuristic_scores(query: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    q_tokens = set(_normalize_text(query).split())
    a_tokens = set(_normalize_text(answer).split())

    if not q_tokens and not a_tokens:
        return {
            "faithfulness_score": 0.0,
            "context_precision_score": 0.0,
            "context_recall_score": 0.0,
            "answer_relevancy_score": 0.0,
        }

    context_text = "\n".join(contexts)
    context_tokens = set(_normalize_text(context_text).split())

    overlap_answer_context = len(a_tokens & context_tokens) / max(1, len(a_tokens)) if a_tokens else 0.0
    overlap_query_answer = len(q_tokens & a_tokens) / max(1, len(q_tokens)) if q_tokens else 0.0
    overlap_query_context = len(q_tokens & context_tokens) / max(1, len(q_tokens)) if q_tokens else 0.0

    return {
        "faithfulness_score": round(min(1.0, overlap_answer_context), 3),
        "context_precision_score": round(min(1.0, overlap_query_answer), 3),
        "context_recall_score": round(min(1.0, overlap_query_context), 3),
        "answer_relevancy_score": round(min(1.0, overlap_query_answer), 3),
    }


def _evaluate_with_ragas(query: str, answer: str, contexts: List[str], retrieved_docs: Optional[List[dict]]) -> Dict[str, float]:
    if not contexts:
        return {
            "faithfulness_score": 0.0,
            "context_precision_score": 0.0,
            "context_recall_score": 0.0,
            "answer_relevancy_score": 0.0,
        }

    if not all([Dataset, OpenAI, evaluate, llm_factory, SentenceTransformer]):
        raise RuntimeError(f"RAGAS dependencies unavailable: {RAGAS_IMPORT_ERROR}")

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    client = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
    ragas_llm = llm_factory("llama-3.3-70b-versatile", provider="openai", client=client)
    ragas_embeddings = SimpleEmbeddings()

    dataset = Dataset.from_list([{
        "question": query,
        "answer": answer,
        "contexts": contexts,
        "reference": "\n".join(_build_ground_truths(retrieved_docs)),
    }])

    result = evaluate(
        dataset,
        metrics=[
            Faithfulness(llm=ragas_llm),
            ContextPrecision(llm=ragas_llm),
            ContextRecall(llm=ragas_llm),
            AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
        ],
        llm=ragas_llm,
        embeddings=ragas_embeddings,
        raise_exceptions=True,
        show_progress=False,
        batch_size=1,
    )

    if hasattr(result, "scores"):
        try:
            scores = result.scores[0] if isinstance(result.scores, list) else result.scores
            if isinstance(scores, dict):
                return {
                    "faithfulness_score": round(float(scores.get("faithfulness", 0.0) or 0.0), 3),
                    "context_precision_score": round(float(scores.get("context_precision", 0.0) or 0.0), 3),
                    "context_recall_score": round(float(scores.get("context_recall", 0.0) or 0.0), 3),
                    "answer_relevancy_score": round(float(scores.get("answer_relevancy", 0.0) or 0.0), 3),
                }
        except Exception:
            pass

    raise RuntimeError("RAGAS did not return a parseable score payload")


def _write_record(record: Dict[str, Any]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def evaluate_and_store(
    query: str,
    answer: Any,
    retrieved_docs: Optional[List[dict]] = None,
    prompt_versions: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    answer_text = _safe_answer_text(answer)
    contexts = _build_contexts(retrieved_docs)

    print(f"[Evaluation] Starting evaluation for query: {query}")

    try:
        scores = _evaluate_with_ragas(query, answer_text, contexts, retrieved_docs)
        print(f"[Evaluation] RAGAS scores: {scores}")
    except Exception as exc:
        scores = _heuristic_scores(query, answer_text, contexts)
        print(f"[Evaluation] RAGAS evaluation failed, using fallback scores: {exc}")

    versions = prompt_versions or get_prompt_versions()
    evaluation_prompt = render_prompt("evaluation", version=versions.get("evaluation", "v1"), query=query, answer=answer_text)

    record = {
        "query": query,
        "answer": answer_text,
        "faithfulness_score": scores.get("faithfulness_score", 0.0),
        "context_precision_score": scores.get("context_precision_score", 0.0),
        "context_recall_score": scores.get("context_recall_score", 0.0),
        "answer_relevancy_score": scores.get("answer_relevancy_score", 0.0),
        "answer_prompt_version": versions.get("answer", "v1"),
        "citation_prompt_version": versions.get("citation", "v1"),
        "evaluation_prompt_version": versions.get("evaluation", "v1"),
        "evaluation_prompt_text": evaluation_prompt,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    _write_record(record)
    print(f"[Evaluation] Stored evaluation record: {record['timestamp']}")
    return record


def run_evaluation_in_background(
    query: str,
    answer: Any,
    retrieved_docs: Optional[List[dict]] = None,
    prompt_versions: Optional[Dict[str, str]] = None,
) -> None:
    thread = threading.Thread(
        target=evaluate_and_store,
        args=(query, answer, retrieved_docs, prompt_versions),
        daemon=True,
    )
    thread.start()
    print(f"[Evaluation] Background evaluation thread started for query: {query}")
