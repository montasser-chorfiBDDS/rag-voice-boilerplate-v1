# 🚀 Advanced Multilingual Conversational RAG (Tunisian Legal & Enterprise Assistant)

> **Document Version**: 2.0.0 (Updated & Upgraded)  
> **Last Updated**: August 2026  
> **Author**: Montassar Chorfi  
> **Purpose**: Complete Technical Architecture, Feature Spec & AI Handover Reference Guide.

---

## 📌 1. Executive Summary & Architecture

This project is an **enterprise-grade, production-ready Conversational RAG (Retrieval-Augmented Generation)** web application designed for processing, indexing, and querying complex documents (such as Tunisian public procurement laws and enterprise PDFs).

### 🏗️ Architecture Diagram
```
                                 ┌─────────────────────────┐
                                 │     User Interface      │
                                 │   Streamlit (Port 8501) │
                                 └────────────┬────────────┘
                                              │ HTTP Requests
                                              ▼
                                 ┌─────────────────────────┐
                                 │     FastAPI Backend     │
                                 │   Main API (Port 8000)  │
                                 └────────────┬────────────┘
                                              │
                                 ┌────────────┴────────────┐
                                 │    RAG Engine Core      │
                                 │ (Multilingual Prompts)  │
                                 └────────────┬────────────┘
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
        ┌──────────────────────────┐                      ┌──────────────────────────┐
        │  Hybrid Vector Retriever │                      │  HuggingFace Inference   │
        │   BM25 (30%) + FAISS (70%)│                      │   API (Qwen2.5-72B)      │
        └──────────────────────────┘                      └──────────────────────────┘
```

---

## ✨ 2. Key Features Implemented (V2.0)

| Feature | Description | Technical Implementation |
|---|---|---|
| 🔍 **Hybrid Search** | Combines exact keyword matching & semantic search | `EnsembleRetriever` (BM25 30% + FAISS 70%) |
| ⚡ **Live Streaming** | Real-time word-by-word response streaming | `st.write_stream` with custom generator in Streamlit |
| 📚 **Source Citations** | Clickable expandable evidence for every answer | Returns `source_documents` snippets & filenames |
| 📄 **Document Indexing** | Instant PDF & TXT text extraction and indexing | `pypdf` + `RecursiveCharacterTextSplitter` |
| 🧠 **Conversational Memory** | Multi-turn chat context memory | `ConversationBufferMemory` with `output_key="answer"` |
| 🐳 **Docker Deployment** | 1-command containerized production build | `docker-compose` with lightweight image (<350MB) |

---

## 📁 3. Project Directory Structure

Project Root: `C:\Users\pc\.gemini\antigravity\scratch\rag-voice-boilerplate-v1`

```
rag-voice-boilerplate-v1/
├── app/
│   ├── api/
│   │   └── routes.py              # Endpoints: /query, /documents/upload
│   ├── core/
│   │   └── rag_engine.py          # RAGEngine, HFHubLLM, Arabic Prompts, Citations
│   ├── database/
│   │   └── vector_store.py        # FAISS + BM25 EnsembleRetriever, HFHubEmbeddings
│   └── config.py                  # Pydantic Settings (.env configuration)
├── data/
│   └── vector_store/              # Persistent FAISS index files
├── docker/
│   └── Dockerfile                 # Optimized Docker build specification
├── .dockerignore                  # Context exclusion file (excludes venvs & data)
├── .env                           # Environment variables (HUGGINGFACE_API_KEY)
├── app_ui.py                      # Streamlit UI with Live Streaming & Citations
├── docker-compose.yml             # Dual service orchestrator (backend + frontend)
├── main.py                        # FastAPI entry point
├── run_app.bat                    # 1-click Windows Batch Launcher
├── requirements.txt               # Lightweight dependencies (No PyTorch needed)
└── PROJECT_OVERVIEW.md            # Technical Reference File
```

---

## 🚀 4. How to Run the Application

### Method 1: Using 1-Click Batch File (Local Windows)
Simply double-click:
```powershell
run_app.bat
```

### Method 2: Using Docker (Containerized Production)
```powershell
cd C:\Users\pc\.gemini\antigravity\scratch\rag-voice-boilerplate-v1
docker-compose up -d
```
* **Frontend**: `http://localhost:8501`
* **Backend API**: `http://localhost:8000`

---

## 📡 5. API Endpoints Specification

### 1. Document Upload & Real-Time Indexing
- **Endpoint**: `POST /api/v1/documents/upload`
- **Body**: `multipart/form-data` with `file` (PDF/TXT)
- **Response**:
  ```json
  {
    "status": "success",
    "filename": "decree_1039.pdf",
    "characters_extracted": 45200,
    "message": "Successfully indexed decree_1039.pdf (45200 characters)."
  }
  ```

### 2. Conversational RAG Query with Citations
- **Endpoint**: `POST /api/v1/query?question=...&session_id=...`
- **Response**:
  ```json
  {
    "answer": "وفقاً للأمر عدد 1039...",
    "sources": [
      {
        "filename": "decree_1039.pdf",
        "snippet": "الفصل 6 - تنقسم الصفقات العمومية..."
      }
    ]
  }
  ```

---

## 🤖 6. AI Assistant Handover Prompt

When continuing this project with any AI assistant, send them this snippet:

```text
I am working on an Enterprise Multilingual RAG application (Version 2.0) located at:
`C:\Users\pc\.gemini\antigravity\scratch\rag-voice-boilerplate-v1`

Key Specs:
1. Backend: FastAPI (`main.py`, `app/api/routes.py`) on port 8000.
2. Frontend: Streamlit (`app_ui.py`) on port 8501 with Live Response Streaming & Source Citations.
3. Vector Store: Hybrid FAISS + BM25 (`app/database/vector_store.py`).
4. LLM & Embeddings: `huggingface_hub.InferenceClient` (`Qwen/Qwen2.5-72B-Instruct`).
5. Deployment: `docker-compose.yml` (Dockerized dual container backend + frontend).

Please review `PROJECT_OVERVIEW.md` before making architectural suggestions.
```
