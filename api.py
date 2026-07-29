from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.workflow import app as agent_app
from logger import logger
from metrics import metrics_store

app = FastAPI(title="Medical Research Agent API")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-medical-agent-production-54e9.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    question: str


def _error_response(status_code: int, message: str, error_type: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": error_type,
                "message": message,
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return _error_response(exc.status_code, str(exc.detail), "http_exception")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled API exception")
    return _error_response(
        500,
        "Internal server error",
        "internal_server_error",
    )


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {"status": "Medical MCP Agent Running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return metrics_store.snapshot()


# ---------------- RESEARCH ----------------
@app.post("/research")
def research(payload: ResearchRequest):
    question = (payload.question or "").strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    if len(question) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Question is too long",
        )

    start_time = __import__("time").perf_counter()
    try:
        result = agent_app.invoke({
            "question": question,
            "docs": [],
            "context": "",
            "answer": ""
        })
        response_time = __import__("time").perf_counter() - start_time
        metrics_store.record_request(response_time, success=True)
    except Exception as exc:
        response_time = __import__("time").perf_counter() - start_time
        metrics_store.record_request(response_time, success=False)
        logger.exception("Workflow execution failed")
        return _error_response(
            500,
            "Workflow execution failed",
            "workflow_error",
        )

    if not isinstance(result, dict):
        result = {}

    pmids = result.get("pmids", []) or []

    answer = result.get("answer", {}) or {}

    if not isinstance(answer, dict):
        answer = {
            "topic": question,
            "papers": [],
        }

    return {
        "query": question,
        "answer": answer,
        "context": result.get("context", ""),
        "pmids": pmids,
        "citations": [{"pmid": p} for p in pmids],
    }


@app.get("/research")
def research_get(q: str):
    return research(
        ResearchRequest(question=q)
    )
@app.get("/version")
def version():
    return {
        "version": "cors-test-v1"
    }
