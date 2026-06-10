# 🏥 Medical Research AI Agent

An AI-powered Medical Research Agent that retrieves real research papers from PubMed, stores them in a vector database, performs semantic search, and generates evidence-based summaries using Large Language Models.

## 🚀 Project Overview

This project combines Agentic AI, Retrieval-Augmented Generation (RAG), LangGraph, MCP tools, and local LLMs to help users explore medical research papers efficiently.

The agent can:

* Search PubMed for medical research papers
* Fetch abstracts and metadata
* Store papers in a vector database
* Perform semantic similarity search
* Generate evidence-based summaries
* Provide PMIDs for research verification
* Answer healthcare research queries using retrieved literature

---

## 🛠️ Tech Stack

### AI & Agent Framework

* LangGraph
* MCP (Model Context Protocol)
* Ollama
* Llama 3

### Retrieval & Vector Database

* ChromaDB
* Sentence Transformers
* all-MiniLM-L6-v2 Embeddings

### Research Data Source

* PubMed API (NCBI E-Utilities)

### Backend

* FastAPI
* Python

### Frontend

* Streamlit

---

## 🏗️ System Architecture

User Query
↓
LangGraph Agent
↓
PubMed Search Tool
↓
Abstract Retrieval Tool
↓
ChromaDB Vector Storage
↓
Semantic Search
↓
Llama 3 (Ollama)
↓
Evidence-Based Answer

---

## 🔥 Features

### Research Retrieval

* Search medical literature from PubMed
* Retrieve latest research papers
* Fetch abstracts automatically

### Semantic Search

* Vector embeddings using Sentence Transformers
* Similarity-based paper retrieval
* Context-aware document selection

### AI Summarization

* Research paper summaries
* Key findings extraction
* Evidence-based responses
* Citation support using PMIDs

### Agentic Workflow

* LangGraph orchestration
* MCP tool integration
* Multi-step reasoning pipeline

---

## 📂 Project Structure

medical-research-agent/

├── api.py

├── agent_langgraph.py

├── mcp_tools.py

├── ui.py

├── medical_db/

├── requirements.txt

└── README.md

---

## ⚙️ LangGraph Workflow

### 1. Retrieve Node

Searches PubMed using the user query.

### 2. Embed Node

Stores research papers inside ChromaDB.

### 3. Context Node

Retrieves the most relevant documents using semantic search.

### 4. Generate Node

Uses Llama 3 to generate evidence-based summaries.

---

## ▶️ Running the Project

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Ollama

```bash
ollama run llama3
```

### Start FastAPI Backend

```bash
uvicorn api:app --reload
```

### Start Streamlit Frontend

```bash
streamlit run ui.py
```

---

## Example Queries

* Type 2 diabetes interventions
* Machine learning in healthcare
* Cancer diagnosis using AI
* Neuroscience research papers
* Cardiovascular disease prediction

---

## Learning Outcomes

This project demonstrates:

* Agentic AI Development
* LangGraph Workflows
* MCP Tool Integration
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* LLM Applications in Healthcare
* Research Automation

---

## Future Improvements

* Multi-Agent Architecture
* Research Paper Ranking Agent
* PDF Paper Retrieval
* Medical Citation Verification Agent
* Research Trend Analysis
* Knowledge Graph Integration
* Clinical Decision Support

---

## Author

Manvitha kv

AI & Data Science Engineer

Built as an Agentic AI Healthcare Research Assistant using LangGraph, MCP, FastAPI, ChromaDB, PubMed, Ollama, and Llama 3.
