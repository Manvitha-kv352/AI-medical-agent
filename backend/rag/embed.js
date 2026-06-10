const axios = require("axios");

// 🔥 Ollama embeddings (optional future upgrade)
async function getEmbedding(text) {
  const res = await axios.post("http://localhost:11434/api/embeddings", {
    model: "llama3",
    prompt: text
  });

  return res.data.embedding;
}

module.exports = {
  getEmbedding
};