const axios = require("axios");

const RAG_URL = "http://127.0.0.1:8000"; // future python service

// 🔍 SEARCH VECTOR DB
async function searchVectors(query) {
  try {
    const res = await axios.post(`${RAG_URL}/search`, {
      query
    });

    return res.data.documents || [];
  } catch (err) {
    console.error("Chroma search error:", err.message);
    return [];
  }
}

// 📥 INGEST DATA
async function addDocuments(docs) {
  try {
    const res = await axios.post(`${RAG_URL}/ingest`, {
      docs
    });

    return res.data;
  } catch (err) {
    console.error("Chroma ingest error:", err.message);
    return null;
  }
}

module.exports = {
  searchVectors,
  addDocuments
};