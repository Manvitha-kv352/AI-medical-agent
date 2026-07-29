const axios = require("axios");
const { searchVectors } = require("./rag/chroma");

// ---------------------- OLLAMA CALL ----------------------
async function callOllama(prompt) {
  try {
    const res = await axios.post("http://localhost:11434/api/generate", {
      model: "llama3",
      prompt,
      stream: false
    });

    return res.data.response;
  } catch (err) {
    console.error("Ollama Error:", err.message);
    return "Error: LLM failed to respond";
  }
}

// ---------------------- RAG RETRIEVAL ----------------------
async function retrieveMedicalContext(query) {
  try {
    const docs = await searchVectors(query);

    if (!docs || docs.length === 0) {
      return "No relevant medical context found in database.";
    }

    return docs.join("\n");
  } catch (err) {
    console.error("RAG Error:", err.message);
    return "RAG retrieval failed.";
  }
}

// ---------------------- AGENT CORE ----------------------
async function runMedicalAgent(query) {
  try {
    // 1. Retrieve context from RAG
    const context = await retrieveMedicalContext(query);

    // 2. Build medical prompt
    const prompt = `
You are an expert medical AI assistant.

Use ONLY the context below if relevant:
-------------------------------------
${context}
-------------------------------------

User Question:
${query}

Instructions:
  - Respond in clean markdown with short sections.
  - Start with a brief direct answer.
  - Use headings like "## Overview", "## Symptoms", "## Causes", "## Treatment", "## When to seek help" only when relevant.
  - Use bullet points for lists and keep paragraphs short.
  - If context is insufficient, say "based on general medical knowledge".
  - Do not hallucinate facts.
  - Do not return a single compressed paragraph.
`;

    // 3. Call Ollama
    const answer = await callOllama(prompt);

    // 4. Return structured response
    return {
      answer,
      contextUsed: context,
      model: "ollama + chromadb (RAG)"
    };

  } catch (err) {
    console.error("Agent Error:", err.message);

    return {
      answer: "Agent failed to process request",
      error: err.message
    };
  }
}

module.exports = {
  runMedicalAgent
};