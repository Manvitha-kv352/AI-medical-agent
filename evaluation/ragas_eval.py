import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS_PATH = ROOT / "evaluation" / "results" / "predictions.json"
SAMPLE_DATASET_PATH = ROOT / "evaluation" / "sample_dataset.json"

with PREDICTIONS_PATH.open("r", encoding="utf-8") as f:
    predictions = json.load(f)

with SAMPLE_DATASET_PATH.open("r", encoding="utf-8") as f:
    references = json.load(f)


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def overlap_score(text: str, target: str) -> float:
    if not text or not target:
        return 0.0
    text_tokens = set(normalize(text).split())
    target_tokens = set(normalize(target).split())
    if not text_tokens or not target_tokens:
        return 0.0
    overlap = text_tokens & target_tokens
    return round(len(overlap) / max(1, len(target_tokens)), 3)


reference_map = {
    normalize(item["question"]): item["ground_truth"]
    for item in references
}

rows = []
for idx, item in enumerate(predictions):
    question = item.get("question", "")
    answer_value = item.get("answer", "")
    answer_text = answer_value.get("content", answer_value) if isinstance(answer_value, dict) else answer_value

    ref_key = normalize(question)
    ground_truth = reference_map.get(ref_key)

    if ground_truth is None and idx < len(references):
        ground_truth = references[idx].get("ground_truth")

    rows.append({
        "question": question,
        "answer": str(answer_text),
        "context": item.get("context", ""),
        "ground_truth": ground_truth,
    })

scores = []
for row in rows:
    answer_text = row["answer"]
    context_text = row["context"]
    gt = row["ground_truth"] or ""

    faithfulness_score = 1.0 if gt and overlap_score(answer_text, gt) >= 0.1 else 0.0
    relevance_score = overlap_score(answer_text, row["question"])
    context_score = 1.0 if context_text and len(context_text) > 50 else 0.0

    scores.append({
        "question": row["question"],
        "faithfulness": faithfulness_score,
        "answer_relevancy": relevance_score,
        "context_precision": context_score,
        "context_recall": overlap_score(context_text, gt),
    })

print(json.dumps({
    "count": len(scores),
    "average": {
        "faithfulness": round(sum(item["faithfulness"] for item in scores) / len(scores), 3),
        "answer_relevancy": round(sum(item["answer_relevancy"] for item in scores) / len(scores), 3),
        "context_precision": round(sum(item["context_precision"] for item in scores) / len(scores), 3),
        "context_recall": round(sum(item["context_recall"] for item in scores) / len(scores), 3),
    },
    "samples": scores,
}, indent=2))