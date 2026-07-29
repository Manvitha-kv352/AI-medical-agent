const { runMedicalAgent } = require("../agent");
const { verifyResponse } = require("./verifier");
const { searchPubMed } = require("../tools/pubmedtool");

// ---------------- STATE ----------------
function createState(query) {
  return {
    query,
    route: null,
    result: null,
    papers: []
  };
}

// ---------------- ROUTER ----------------
function router(state) {
  const q = state.query.toLowerCase();

  console.log("🧠 Router checking query...");

  if (
    q.includes("paper") ||
    q.includes("research") ||
    q.includes("study")
  ) {
    state.route = "rag";
  } else {
    state.route = "llm";
  }

  return state;
}

// ---------------- RAG NODE ----------------
async function ragNode(state) {
  console.log("📚 RAG Node triggered");

  const result = await runMedicalAgent(state.query, {
    mode: "rag"
  });

  state.result = result;
  return state;
}

// ---------------- LLM NODE ----------------
async function llmNode(state) {
  console.log("🤖 LLM Node triggered");

  const result = await runMedicalAgent(state.query, {
    mode: "llm"
  });

  state.result = result;
  return state;
}

// ---------------- PUBMED NODE ----------------
async function pubmedNode(state) {
  console.log("📚 PubMed Node triggered");

  const papers = await searchPubMed(state.query);

  state.papers = papers;

  return state;
}

// ---------------- VERIFIER NODE ----------------
async function verifierNode(state) {
  console.log("🧪 Verifier Node triggered");

  const verification = await verifyResponse(
    state.query,
    {
      answer: state.result,
      papers: state.papers
    }
  );

  return {
    query: state.query,
    route: state.route,
    result: state.result,
    papers: state.papers,
    verified: verification.corrected_answer,
    safe: verification.safe,
    issues: verification.issues
  };
}

// ---------------- EXECUTOR ----------------
async function runGraph(query) {
  let state = createState(query);

  // 1. Router
  state = router(state);

  // 2. AI Node
  if (state.route === "rag") {
    state = await ragNode(state);
  } else {
    state = await llmNode(state);
  }

  // 3. 📚 PUBMED NODE (REAL MEDICAL DATA)
  state = await pubmedNode(state);

  // 4. 🧪 VERIFIER NODE (SAFETY LAYER)
  const finalOutput = await verifierNode(state);

  return finalOutput;
}

module.exports = { runGraph };