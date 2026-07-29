const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const { runGraph } = require("./graph/medicalGraph");

dotenv.config();

const app = express();

// ---------- MIDDLEWARE ----------
app.use(cors());
app.use(express.json());

// ---------- IN-MEMORY LOG ----------
const researchLogs = [];

// ---------- HEALTH CHECK ----------
app.get("/api/health", (req, res) => {
  res.json({
    success: true,
    status: "Medical AI Agent Running 🚀",
    timestamp: new Date()
  });
});

// ---------- MAIN AGENT ROUTE (LANGGRAPH FLOW) ----------
app.post("/api/research/search", async (req, res) => {
  try {
    console.log("🔥 SEARCH API HIT");

    const { query } = req.body;

    if (!query) {
      return res.status(400).json({
        success: false,
        error: "Query is required"
      });
    }

    // 🧠 RUN LANGGRAPH AGENT
    const result = await runGraph(query);

    // 📌 STORE LOG
    const logEntry = {
      id: Date.now(),
      query,
      timestamp: new Date(),
      result
    };

    researchLogs.push(logEntry);

    // 📤 RESPONSE
    return res.json({
      success: true,
      query,
      result
    });

  } catch (err) {
    console.error("Search error:", err);

    return res.status(500).json({
      success: false,
      error: err.message
    });
  }
});

// ---------- GET ALL LOGS ----------
app.get("/api/research/logs", (req, res) => {
  res.json({
    success: true,
    count: researchLogs.length,
    data: researchLogs
  });
});

// ---------- CLEAR LOGS ----------
app.delete("/api/research/logs", (req, res) => {
  researchLogs.length = 0;

  res.json({
    success: true,
    message: "Logs cleared"
  });
});

// ---------- START SERVER ----------
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🏥 Medical Agent Server running on port ${PORT}`);
  console.log(`🧠 LangGraph Agent Active`);
  console.log(`🤖 Ollama + RAG Connected`);
});