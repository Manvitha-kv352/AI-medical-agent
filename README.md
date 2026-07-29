# 🏥 AI Medical Research Agent

An AI-powered Medical Research Assistant that retrieves, ranks, and summarizes biomedical literature from PubMed using Retrieval-Augmented Generation (RAG), hybrid search, citation validation, and automated evaluation.

---

## 🚀 Overview

The AI Medical Research Agent helps researchers, clinicians, and students quickly explore medical literature by combining Large Language Models with trusted biomedical sources.

Instead of generating unsupported answers, the system retrieves relevant PubMed papers, reranks them using hybrid retrieval, validates citations, and produces structured research summaries.

---

## ✨ Features

* 🔎 Intelligent PubMed search
* 🧠 Retrieval-Augmented Generation (RAG)
* 📚 Hybrid Retrieval (Dense + BM25)
* 📄 Automatic paper summarization
* ✅ Citation validation
* 📌 PMID and PubMed link generation
* ⚡ LangGraph workflow orchestration
* 🤖 Groq LLM integration
* 🗂️ ChromaDB vector database
* 📊 Automatic evaluation pipeline
* 🐳 Docker support
* 🌐 FastAPI REST API
* 💻 React + Vite frontend

---

## 🏗️ System Architecture

```text
User Query
     │
     ▼
FastAPI API
     │
     ▼
LangGraph Workflow
     │
     ├──────────────► Query Generation
     │
     ▼
PubMed Search
     │
     ▼
Document Retrieval
     │
     ▼
ChromaDB Vector Search
     │
     ▼
Hybrid Reranking (Dense + BM25)
     │
     ▼
Context Assembly
     │
     ▼
Groq LLM
     │
     ▼
Citation Validation
     │
     ▼
Evaluation Pipeline
     │
     ▼
Structured Research Response
```

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* LangGraph
* LangChain
* ChromaDB
* Groq API

### Retrieval

* PubMed API
* Hybrid Retrieval
* BM25
* Dense Vector Search

### Frontend

* React
* Vite

### DevOps

* Docker
* Docker Compose
* GitHub

### Evaluation

* RAGAS (with heuristic fallback)
* Prompt versioning
* Citation validation

---

## 📂 Project Structure

```text
AI-medical-agent/
│
├── backend/
├── frontend/
├── graph/
├── prompts/
├── evaluation/
├── rag_service/
├── tools/
├── tests/
├── medical_db/
├── api.py
├── app.py
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Manvitha-kv352/AI-medical-agent.git
cd AI-medical-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Backend

```bash
uvicorn api:app --reload
```

Backend:

```
http://localhost:8000
```

Health endpoint:

```
GET /health
```

Research endpoint:

```
POST /research
```

---

## 🐳 Run with Docker

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up
```

---

## 📥 Example Request

```json
{
  "question": "Find papers about AI applications in neuroscience and healthcare."
}
```

---

## 📤 Example Response

```json
{
  "query": "...",
  "answer": {
    "topic": "...",
    "papers": [
      {
        "title": "...",
        "summary": "...",
        "pmid": "...",
        "pubmed_url": "..."
      }
    ]
  },
  "pmids": [
    "41006992"
  ]
}
```

---

## 📊 Evaluation Pipeline

The project includes an evaluation framework that measures:

* Retrieval quality
* Citation completeness
* Prompt version
* Answer quality
* Evaluation metadata

If RAGAS dependencies are unavailable, the system automatically falls back to heuristic evaluation to maintain service availability.

---

## 🔐 Citation Validation

Every generated paper is checked for:

* Valid title
* PMID
* PubMed URL
* Alignment with retrieved documents

Incomplete citations are flagged instead of being presented as verified references.

---

## 🧪 Testing

Run the smoke tests:

```bash
pytest -q tests/test_smoke.py
```

---

## 🚀 Future Improvements

* PDF research report generation
* Conversation memory
* Streaming responses
* Authentication
* Monitoring and metrics
* Cloud deployment
* Advanced biomedical reranking

---

## 👩‍💻 Author

**Manvitha K V**

Artificial Intelligence & Data Science Engineer

GitHub: https://github.com/Manvitha-kv352

---

## 📄 License

This project is released under the MIT License.
