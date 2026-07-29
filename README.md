# Medical Research Agent

A production-oriented medical research assistant that combines FastAPI, LangGraph-style workflow orchestration, PubMed retrieval, and Groq-backed generation to answer biomedical questions with grounded citations.

## Overview

The project accepts a natural-language medical research question, retrieves candidate papers from PubMed, builds a retrieval context, and generates a structured answer with paper summaries and citation metadata. The current backend is implemented with FastAPI and the frontend is a Vite/React application.

## Architecture

```text
User -> Frontend (Vite/React)
        -> FastAPI backend (/health, /research)
        -> Retrieval workflow
           -> PubMed search + abstract fetch
           -> Context assembly + reranking
           -> Prompt rendering + Groq generation
           -> Citation validation + evaluation logging
```

## Features

- PubMed-powered retrieval for biomedical literature
- Structured answer generation with paper-level summaries
- Citation validation and source alignment checks
- Prompt versioning and evaluation hooks
- Docker-based local deployment
- FastAPI health and research endpoints

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Workflow: LangGraph-style Python orchestration
- Retrieval: PubMed E-Utilities, optional Chroma-backed storage
- LLM: Groq via OpenAI-compatible endpoint
- Frontend: React, Vite, Axios
- Containerization: Docker, Docker Compose

## Project Structure

```text
medical-research-agent/
├── api.py
├── Dockerfile
├── docker-compose.yml
├── requirements-minimal.txt
├── requirements.txt
├── graph/
├── llm/
├── prompts/
├── tools/
├── evaluation/
├── frontend/
├── tests/
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- Node.js 20+
- Docker Desktop (optional)

### Python environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-minimal.txt
```

### Frontend dependencies

```bash
cd frontend
npm install
```

## Environment Variables

Create a copy of [.env.example](.env.example) and fill in the required values.

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
VITE_API_URL=http://localhost:8000
```

## Running Locally

### Backend

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

## Running with Docker

```bash
docker compose up --build
```

The backend will be available on http://localhost:8000 and the frontend on http://localhost:5173.

## API Documentation

The FastAPI app exposes:

- GET /health
- GET /
- POST /research
- GET /research

### Example request

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"question":"Find papers about AI in neuroscience"}'
```

### Example response

```json
{
  "query": "Find papers about AI in neuroscience",
  "answer": {
    "topic": "Find papers about AI in neuroscience",
    "papers": []
  },
  "context": "",
  "pmids": [],
  "citations": []
}
```

## Evaluation Pipeline

Evaluation results are written to the evaluation output directory when the workflow completes. The evaluation layer uses fallback heuristics if the RAGAS stack is unavailable.

## Troubleshooting

- Verify that the Groq API key is set in the environment.
- If PubMed retrieval fails, the workflow still returns a structured fallback answer.
- For Docker issues, rebuild containers with:

```bash
docker compose down
docker compose up --build
```

## Deployment Notes

The current project is sized for container-based deployment on Render, Azure App Service, or Railway with environment variables configured at the platform level.

