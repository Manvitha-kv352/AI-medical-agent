# 🏥 AI Medical Research Agent

An Agentic AI-powered medical research assistant that combines PubMed search, Retrieval-Augmented Generation (RAG), ChromaDB vector search, LangGraph workflows, and Ollama LLMs to provide evidence-based medical research insights.

---

# 🚀 Overview

The AI Medical Research Agent helps users:

* Search medical literature from PubMed
* Retrieve research papers and metadata
* Store medical knowledge in ChromaDB
* Perform semantic similarity search
* Generate AI-powered medical summaries
* Verify generated responses through a validation layer
* Provide evidence-based answers using retrieved research

The system combines RAG, Agentic AI workflows, and Large Language Models to improve the quality of healthcare research exploration.

---

# 🧠 Architecture

User Query
↓
Router Agent
↓
PubMed Search Tool
↓
RAG Retrieval (ChromaDB)
↓
LangGraph Workflow
↓
Ollama (Llama 3)
↓
Response Verification
↓
Final Answer

---

# ✨ Features

## Medical Research Search

* Search PubMed using natural language queries
* Retrieve recent medical research papers
* Extract paper metadata

## Agentic Workflow

* Query routing system
* Multiple processing nodes
* Automated decision making

## Retrieval-Augmented Generation (RAG)

* Semantic document retrieval
* Context-aware answer generation
* Reduced hallucinations

## Vector Database

* ChromaDB integration
* Embedding-based search
* Medical document storage

## AI Answer Generation

* Powered by Ollama
* Uses Llama 3 locally
* Evidence-based response generation

## Verification Layer

* Response validation
* Safety checking
* Medical answer verification

---

# 🛠️ Tech Stack

## Backend

* Node.js
* Express.js
* LangGraph

## AI & LLM

* Ollama
* Llama 3

## Retrieval

* ChromaDB
* Embedding Models

## Data Source

* PubMed API
* NCBI E-Utilities

## Frontend

* React
* Vite

## Containerization

* Docker
* Docker Compose

---

# 📂 Project Structure

medical-research-agent/

├── backend/

│ ├── server.js

│ ├── agent.js

│ ├── graph/

│ │ ├── medicalGraph.js

│ │ └── verifier.js

│ ├── tools/

│ │ └── pubmedtool.js

│ └── rag/

│ ├── chroma.js

│ ├── embed.js

│ └── ingest.js

│

├── frontend/

│ ├── src/

│ ├── public/

│ └── vite.config.js

│

├── rag_service/

│ └── app.py

│

├── docker-compose.yml

└── README.md

---

# ⚙️ Workflow

## Step 1: Query Routing

The Router Agent analyzes the user's query and determines whether to:

* Use RAG retrieval
* Use direct LLM generation
* Trigger PubMed search

## Step 2: Research Retrieval

The PubMed Tool:

* Searches PubMed
* Retrieves paper metadata
* Returns research references

## Step 3: Semantic Search

ChromaDB:

* Stores embeddings
* Finds relevant medical documents
* Supplies context to the LLM

## Step 4: AI Generation

Llama 3:

* Receives retrieved context
* Generates structured medical responses
* Produces evidence-based outputs

## Step 5: Verification

Verifier Node:

* Checks generated answers
* Detects inconsistencies
* Improves reliability

---

# 🚀 Installation

## Clone Repository

```bash
git clone <repository-url>
cd medical-research-agent
```

## Install Backend Dependencies

```bash
cd backend
npm install
```

## Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Start Ollama

```bash
ollama run llama3
```

## Run Backend

```bash
npm run dev
```

## Run Frontend

```bash
npm run dev
```

---

# 🔎 Example Queries

* What are recent diabetes treatment studies?
* Research papers on machine learning in healthcare
* Latest cancer diagnosis methods
* Cardiovascular disease prediction research
* Neuroscience studies on autism

---

# 🎯 Learning Outcomes

This project demonstrates:

* Agentic AI Design
* LangGraph Workflows
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search
* LLM Integration
* Medical Research Automation
* AI Verification Systems

---

# 🔮 Future Enhancements

* Multi-Agent Collaboration
* Advanced Medical Citation Generation
* PDF Research Paper Retrieval
* Research Trend Analysis
* Medical Knowledge Graph Integration
* Clinical Decision Support Features
* Real-Time Research Monitoring

---

# 👩‍💻 Author

Manvitha kv

Artificial Intelligence & Data Science

Built as an Agentic AI Medical Research Assistant using LangGraph, ChromaDB, PubMed, Ollama, Llama 3, React, Express, and Retrieval-Augmented Generation (RAG).
