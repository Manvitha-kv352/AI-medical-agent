from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from llm.model import llm

# MCP TOOLS
from tools.mcp_tools import (
    pubmed_search,
    fetch_abstracts,
    store_docs,
    vector_search,
)


# =========================
# STATE
# =========================
class AgentState(TypedDict):
    question: str
    docs: List
    context: str
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

    docs = state["docs"]

    if not docs:
        return {}

    store_docs(docs)

    return {}


# =========================
# 3. CONTEXT (MCP VECTOR SEARCH)
# =========================
def context_node(state):

    query = state["question"]

    results = hybrid_search(
    query=query,
    docs=state["docs"],
    top_k=5
)
    docs = results["documents"][0]

    context = "\n\n".join(docs)

    return {"context": context}


# =========================
# 4. GENERATE
# =========================
def generate(state):

    prompt = f"""
You are an evidence-based medical research assistant.

RULES:
- Use ONLY the provided context.
- Do NOT hallucinate.
- Do NOT invent findings.
- Summarize each paper separately.

Context:
{state.get('context', '')}

User Question:
{state.get('question', '')}
"""

    print("\n===== CONTEXT =====")
    print(state.get("context", "")[:1000])

    print("\n===== QUESTION =====")
    print(state.get("question", ""))

    response = llm.invoke(prompt)

    print("\n===== LLM RESPONSE =====")
    print(response)

    return {
        **state,
        "answer": response
    }
# =========================
# GRAPH
# =========================
graph = StateGraph(AgentState)

graph.add_node("retrieve", retrieve)
graph.add_node("embed", embed)
graph.add_node("context", context_node)
graph.add_node("generate", generate)

graph.set_entry_point("retrieve")

graph.add_edge("retrieve", "embed")
graph.add_edge("embed", "context")
graph.add_edge("context", "generate")
graph.add_edge("generate", END)

app = graph.compile()