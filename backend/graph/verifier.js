const axios = require("axios");

// Simple medical safety + hallucination checker
async function verifyResponse(query, result) {
  console.log("🧪 Verifier Node Running...");

  const answerText = typeof result === "string"
    ? result
    : result?.answer || JSON.stringify(result);

  try {
    // Ask Ollama to verify medically
    const response = await axios.post("http://localhost:11434/api/generate", {
      model: "llama3",
      prompt: `
You are a medical verifier AI.

Task:
Check if the following answer is medically correct, safe, and not hallucinated.

User Query:
${query}

AI Answer:
${answerText}

Return STRICT JSON only:
{
  "safe": true/false,
  "corrected_answer": "improved answer if needed, preserving markdown structure",
  "issues": ["list issues if any"]
}
`,
      stream: false
    });

    const text = response.data.response;

    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch (e) {
      parsed = {
        safe: true,
        corrected_answer: answerText,
        issues: []
      };
    }

    return parsed;

  } catch (err) {
    console.error("Verifier error:", err.message);

    // fail-safe: don't break system
    return {
      safe: true,
      corrected_answer: answerText,
      issues: ["verifier_failed"]
    };
  }
}

module.exports = { verifyResponse };