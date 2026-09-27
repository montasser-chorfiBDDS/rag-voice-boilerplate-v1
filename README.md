# RAG Voice Boilerplate — Multilingual Conversational RAG Assistant

A production-ready, **fully local and free** RAG (Retrieval-Augmented Generation) assistant with a Streamlit chat UI, hybrid search (FAISS + BM25), conversational memory, and multilingual Arabic/English answers with source citations.

> Built by **Montassar Chorfi** — Data Scientist & Big Data Specialist

---

## ✨ Features

- 🔍 **Hybrid Search** — FAISS embeddings + BM25 keyword retrieval (ensemble 70/30)
- 🌍 **Multilingual** — optimized for Arabic & English using `paraphrase-multilingual-MiniLM-L12-v2` embeddings
- 🧠 **Conversational Memory** — follow-up questions work naturally
- 🏠 **Fully Local LLM** — no cloud credits, no API cost (Ollama + `qwen2.5:3b`)
- 📚 **Source Citations** — every answer shows the exact document chunks used
- 📤 **On-the-fly uploads** — index PDF/TXT documents directly from the UI
- 🎛️ **Source scoping** — trusted agency docs vs. all uploaded documents
- 🗂️ **Hybrid sync** — `run_app.bat` + optional C→D backup sync script

---

## 🚀 Quickstart (Windows)

1. **Install Ollama** from https://ollama.com/download
2. **Pull a model**:
   ```bash
   ollama pull qwen2.5:3b
   ```
3. **Create a Python venv** and install requirements:
   ```bash
   python -m venv venv_rag
   venv_rag\Scripts\pip install -r requirements.txt
   ```
4. **Create `.env`** (optional — defaults work with local Ollama):
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=qwen2.5:3b
   DEBUG=true
   ```
5. **Launch**:
   ```bash
   run_app.bat
   ```
   → Backend: `http://localhost:8000` · UI: `http://localhost:8501`

---

## 🧱 Architecture

```
Streamlit UI (8501)  ──HTTP──►  FastAPI (8000)  ──►  RAGEngine (LangChain)
                                                       │
                                     ┌─────────────────┴─────────────────┐
                                 Ollama LLM (local)             VectorStore (FAISS+BM25)
                                 qwen2.5:3b                     embeddings: multilingual
```

Key modules:

| Path | Role |
|---|---|
| `app/api/routes.py` | FastAPI endpoints (`/query`, `/documents/upload`) |
| `app/core/rag_engine.py` | RAG orchestration + conversational memory |
| `app/database/vector_store.py` | FAISS store, hybrid retriever, category filter |
| `app/config.py` | Central settings (Ollama, chunking, embeddings) |
| `app_ui.py` | Streamlit chat interface |

---

## 🔌 API Reference

### Query the assistant
```
POST /api/v1/query?question=<text>&session_id=<id>&category=agency|all
```
`category=agency` — only trusted base documents · `category=all` — include user uploads.

### Upload a document
```
POST /api/v1/documents/upload  (multipart, field `file`: .pdf/.txt/.md)
```
PDFs are parsed with `pypdf`; text is chunked (CHUNK_SIZE=500, overlap=100) and embedded.

---

## ⚙️ Configuration (`app/config.py` / `.env`)

| Setting | Default | Purpose |
|---|---|---|
| `OLLAMA_MODEL` | `qwen2.5:3b` | Local LLM model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama endpoint |
| `EMBEDDING_MODEL` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Embeddings via HF Inference |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `500` / `100` | Document chunking |
| `VECTOR_STORE_PATH` | `./data/vector_store` | FAISS index location (gitignored) |

> Note: embeddings use the HuggingFace Inference API. If your HF account has no included credits left, you may switch to a local embedding model instead.

---

## 🧪 Evaluation

```bash
python tests/evaluation/evaluate_rag.py
```

---

## 📁 Repository Layout (public)

```
├── app/                  # Backend (FastAPI + RAG)
│   ├── api/routes.py
│   ├── core/rag_engine.py
│   └── database/vector_store.py
├── app_ui.py             # Streamlit chat UI
├── main.py               # FastAPI entrypoint
├── run_app.bat           # One-click launcher
├── requirements.txt
├── PROJECT_OVERVIEW.md   # Full technical spec
└── palmera_widget.js     # Embeddable widget (refer to docs)
```

Private data (`data/`, `.env`, `venv_rag/`) is excluded via `.gitignore` for a clean public showcase.

---

## 📄 License

MIT — see `LICENSE`.

## 👨‍💻 Author

**Montassar Chorfi**

- GitHub: [montasser-chorfiBDDS](https://github.com/montasser-chorfiBDDS)
- Email: montasserchorfi26@gmail.com