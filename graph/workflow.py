import re
from typing import TypedDict, List
from llm.model import llm
from tools.reranker import rerank
from evaluation.ragas_backend import run_evaluation_in_background
from prompts.prompt_loader import get_prompt_versions, render_prompt

# MCP TOOLS
from tools.mcp_tools import (
    pubmed_search,
    fetch_abstracts,
    store_docs,
    hybrid_search,
)


# =========================
# STATE
# =========================
class AgentState(TypedDict):
    question: str
    docs: List
    context: str
    pmids: List[str]
    retrieved_docs: List[dict]
    answer: str


# =========================
# 1. RETRIEVE (MCP)
# =========================
def retrieve(state):
    query = state["question"]
    ids = pubmed_search(query)
    docs = fetch_abstracts(ids)
    return {"docs": docs}


# =========================
# 2. STORE (MCP VECTOR DB)
# =========================
def embed(state):
    docs = state.get("docs", [])
    if not docs:
        return {}
    store_docs(docs)
    return {}


# =========================
# 3. CONTEXT (MCP VECTOR SEARCH)
# =========================
def context_node(state):
    query = state["question"]
    docs = hybrid_search(query=query, docs=state.get("docs", []), top_k=8)
    before_rerank = docs
    print("[Debug] Documents retrieved before reranking:", len(before_rerank))
    print("[Debug] PMIDs before reranking:", [doc.get("pmid") for doc in before_rerank if doc.get("pmid")])

    docs = rerank(query=query, docs=docs, top_k=5)
    print("[Debug] Documents after reranking:", len(docs))
    print("[Debug] PMIDs after reranking:", [doc.get("pmid") for doc in docs if doc.get("pmid")])
    print("[Debug] Reranked papers:")
    for doc in docs:
        title = doc.get("title") or (doc.get("text", "").splitlines()[0] if doc.get("text") else "Untitled")
        print(f"  - PMID: {doc.get('pmid')} | Title: {title}")

    context = "\n\n".join(
        f"PMID: {doc.get('pmid', 'unknown')}\nTitle: {doc.get('title') or 'Untitled'}\nAbstract: {doc.get('abstract') or doc.get('text', '')}\nMetadata: PMID={doc.get('pmid', '')}; URL={doc.get('pubmed_url', '')}"
        for doc in docs
    )

    print("[Debug] Final context sent to Groq LLM:\n", context)

    pmids = [doc.get("pmid") for doc in docs if doc.get("pmid")]
    return {"context": context, "pmids": pmids, "retrieved_docs": docs}


# =========================
# 4. GENERATE
# =========================
def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text


def _validate_citations(answer, state):
    docs = state.get("retrieved_docs", []) or []
    retrieved_pmids = {str(doc.get("pmid", "")) for doc in docs if doc.get("pmid")}

    if not isinstance(answer, dict):
        return answer, []

    papers = answer.get("papers", []) or []
    validation_results = []

    for index, paper in enumerate(papers, start=1):
        pmid = str(paper.get("pmid", "") or "").strip()
        url = str(paper.get("pubmed_url", "") or "").strip()
        title = str(paper.get("title", "") or "").strip()
        summary = str(paper.get("summary", "") or "").strip()

        missing_fields = []
        if not title:
            missing_fields.append("title")
        if not pmid:
            missing_fields.append("pmid")
        if not url:
            missing_fields.append("pubmed_url")

        is_retrieved = pmid in retrieved_pmids if pmid else False
        if not is_retrieved:
            missing_fields.append("source_alignment")

        if missing_fields:
            paper["citation_status"] = "missing"
            paper["citation_missing_fields"] = missing_fields
            paper["pmid"] = pmid or "Not available"
            paper["pubmed_url"] = url or "Not available"
            paper["summary"] = summary or "Not available in abstract"
        else:
            paper["citation_status"] = "ok"
            paper["citation_missing_fields"] = []

        validation_results.append({
            "paper_index": index,
            "pmid": pmid or "Not available",
            "title": title or "Not available",
            "status": paper.get("citation_status"),
            "missing_fields": paper.get("citation_missing_fields", []),
        })

    answer["papers"] = papers
    print("[Citation Validation] Validation results:")
    for item in validation_results:
        print(item)

    return answer, validation_results


def _build_structured_answer(state):
    question = state.get("question", "")
    docs = state.get("retrieved_docs", []) or []

    papers = []
    for doc in docs[:5]:
        title = doc.get("title") or (doc.get("text", "").splitlines()[0] if doc.get("text") else "Untitled paper")
        abstract = doc.get("abstract") or doc.get("text", "")
        text_for_summary = _clean_text(abstract)

        if text_for_summary:
            summary = text_for_summary[:500]
            if len(text_for_summary) > 500:
                summary = summary + "..."
        else:
            summary = "No abstract text was available in the retrieved context."

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text_for_summary) if s.strip()][:2]
        key_findings = sentences if sentences else ["No additional findings were available in the retrieved context."]

        query_terms = [term for term in re.findall(r"[a-z0-9]+", question.lower()) if len(term) > 2]
        overlap = [term for term in query_terms if term in text_for_summary.lower()]
        if overlap:
            relevance = f"Relevant to the requested topic because the retrieved context contains terms related to: {', '.join(overlap[:3])}."
        else:
            relevance = "Relevant to the requested topic based on the retrieved context, but the abstract did not contain obvious keyword overlap with the query."

        papers.append({
            "title": title,
            "summary": summary,
            "key_findings": key_findings,
            "relevance": relevance,
            "pmid": doc.get("pmid", ""),
            "pubmed_url": doc.get("pubmed_url", "") or (f"https://pubmed.ncbi.nlm.nih.gov/{doc.get('pmid')}/" if doc.get("pmid") else ""),
        })

    if not papers:
        papers = [{
            "title": "No paper retrieved",
            "summary": "No relevant paper context was available from the retrieved abstracts.",
            "key_findings": ["No supporting findings were available in the retrieved context."],
            "relevance": "No supporting evidence was available.",
            "pmid": "",
            "pubmed_url": "",
        }]

    return {"topic": question, "papers": papers}


def generate(state):
    context_text = state.get("context", "")
    question = state.get("question", "")
    prompt_versions = get_prompt_versions()

    prompt = render_prompt(
        "answer_generation",
        version=prompt_versions["answer"],
        question=question,
        context_text=context_text,
    )

    response = llm.invoke(prompt)

    try:
        import json
        if isinstance(response, str):
            parsed = json.loads(response)
        else:
            parsed = response
        if isinstance(parsed, dict):
            validated_answer, _ = _validate_citations(parsed, state)
            state_with_answer = {**state, "answer": validated_answer}
            run_evaluation_in_background(
                query=state.get("question", ""),
                answer=validated_answer,
                retrieved_docs=state.get("retrieved_docs", []),
                prompt_versions=prompt_versions,
            )
            return state_with_answer
    except Exception:
        pass

    structured_answer = _build_structured_answer(state)
    validated_answer, _ = _validate_citations(structured_answer, state)
    state_with_answer = {**state, "answer": validated_answer}
    run_evaluation_in_background(
        query=state.get("question", ""),
        answer=validated_answer,
        retrieved_docs=state.get("retrieved_docs", []),
        prompt_versions=prompt_versions,
    )
    return state_with_answer


# =========================
# SIMPLE EXECUTION ENTRYPOINT
# =========================
def run_agent(question: str):
    state = {"question": question, "docs": [], "context": "", "pmids": [], "answer": ""}
    state.update(retrieve(state))
    state.update(embed(state))
    state.update(context_node(state))
    state.update(generate(state))
    return state


class WorkflowApp:
    def invoke(self, state):
        question = state.get("question", "") if isinstance(state, dict) else str(state)
        return run_agent(question)


# Compatibility export used by api.py
app = WorkflowApp()