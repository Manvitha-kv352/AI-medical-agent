from fastapi import FastAPI
from graph.workflow import app as agent_app

app = FastAPI()


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"status": "Medical MCP Agent Running 🚀"}


# =========================
# MAIN ENDPOINT
# =========================
@app.get("/research")
def research(q: str):

    result = agent_app.invoke({
        "question": q,
        "docs": [],
        "context": "",
        "answer": ""
    })

    return {
    "query": q,
    "answer": result["answer"],
    "context": result["context"],
    "pmids": result["pmids"]
}