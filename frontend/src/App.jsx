import { useEffect, useRef, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

export default function App() {
  const apiBaseUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendMessage = async (nextQuery) => {
    const trimmedQuery = nextQuery.trim();
    if (!trimmedQuery || loading) return;

    setQuery("");

    const userMessage = { role: "user", text: trimmedQuery };
    setChat(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await axios.post(
        `${apiBaseUrl}/api/research/search`,
        { query: trimmedQuery }
      );

      const botMessage = {
        role: "bot",
        text:
          res.data?.result?.verified?.answer ||
          res.data?.result?.verified?.corrected_answer ||
          res.data?.result?.result?.answer ||
          res.data?.result?.answer ||
          "No response"
      };

      setChat(prev => [...prev, botMessage]);

    } catch (err) {
      setChat(prev => [
        ...prev,
        { role: "bot", text: "❌ Backend not reachable" }
      ]);
    }

    setLoading(false);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await sendMessage(query);
  };

  return (
    <div className="app-shell">
      <main className="chat-shell">
        <header className="page-header">
          <div>
            <p className="page-kicker">Medical Research Agent</p>
            <h1>Medical AI Assistant</h1>
            <p className="page-subtitle">
              Ask a medical question and get a structured response.
            </p>
          </div>

          <div className="status-pill">
            <span className={`status-dot ${loading ? "is-thinking" : "is-live"}`} />
            <span>{loading ? "Thinking" : "Ready"}</span>
          </div>
        </header>

        <section className="chat-card">
          <div className="chat-log">
        {chat.map((msg, i) => (
          <div
            key={i}
            className={`message-row ${msg.role === "user" ? "message-row-user" : "message-row-bot"}`}
          >
            <div className={`message-bubble ${msg.role === "user" ? "message-user" : "message-bot"}`}>
              {msg.role === "bot" ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
              ) : (
                msg.text
              )}
            </div>
          </div>
        ))}

            <div ref={chatEndRef} />
          </div>

          <form className="composer" onSubmit={handleSubmit}>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a medical question..."
              className="composer-input"
              disabled={loading}
            />

            <button className="composer-button" type="submit" disabled={loading}>
              {loading ? "Searching..." : "Search"}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}