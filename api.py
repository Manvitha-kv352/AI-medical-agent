from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.workflow import app as agent_app

app = FastAPI(title="Medical Research Agent API")


class ResearchRequest(BaseModel):
    question: str


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"status": "Medical MCP Agent Running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# MAIN ENDPOINT
# =========================
@app.post("/research")
def research(payload: ResearchRequest):
    question = (payload.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = agent_app.invoke({
        "question": question,
        "docs": [],
        "context": "",
        "answer": ""
    })

    pmids = result.get("pmids", []) or []

    answer = result.get("answer", "") or {}
    if isinstance(answer, dict):
        answer = {key: value for key, value in answer.items()}
    else:
        answer = {"topic": question, "papers": []}

    return {
        "query": question,
        "answer": answer,
        "context": result.get("context", ""),
        "pmids": pmids,
        "citations": [{"pmid": pmid} for pmid in pmids],
    }


@app.get("/research")
def research_get(q: str):
    return research(ResearchRequest(question=q))