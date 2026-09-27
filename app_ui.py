import streamlit as st
import requests
import uuid
import json

# Configuration
API_BASE = "http://localhost:8000/api/v1"

# Page config
st.set_page_config(
    page_title="Advanced RAG Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Styling ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
.sidebar-title { font-size: 20px; font-weight: 700; color: #a78bfa; margin-bottom: 8px; }
.metric-card {
    background: rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 18px;
    margin: 8px 0;
    border: 1px solid rgba(167,139,250,0.3);
}
.metric-card h4 { margin: 0; color: #a78bfa; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; }
.metric-card p  { margin: 4px 0 0; color: #f1f5f9; font-size: 22px; font-weight: 700; }
.tag {
    display: inline-block;
    background: rgba(167,139,250,0.2);
    color: #c4b5fd;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 12px;
    margin: 2px;
    border: 1px solid rgba(167,139,250,0.4);
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "docs_uploaded" not in st.session_state:
    st.session_state.docs_uploaded = 0
if "retrieval_category" not in st.session_state:
    st.session_state.retrieval_category = "agency"

import time

def stream_text(text: str):
    """Generator for streaming text word-by-word in Streamlit."""
    words = text.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.003)

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 RAG AI Assistant</div>', unsafe_allow_html=True)
    st.markdown("*Built by **Montassar Chorfi***")
    st.divider()

    # Session Info
    st.markdown("**📊 Session Stats**")
    col1, col2 = st.columns(2)
    col1.metric("Queries", st.session_state.total_queries)
    col2.metric("Docs", st.session_state.docs_uploaded)
    st.caption(f"Session ID: `{st.session_state.session_id}`")
    st.divider()

    # Active Features
    st.markdown("**⚙️ Active Features**")
    st.markdown('<span class="tag">🔍 Hybrid Search (FAISS + BM25)</span>', unsafe_allow_html=True)
    st.markdown('<span class="tag">📚 Source Citations</span>', unsafe_allow_html=True)
    st.markdown('<span class="tag">⚡ Streamed Responses</span>', unsafe_allow_html=True)
    st.markdown('<span class="tag">🧠 Conversational Memory</span>', unsafe_allow_html=True)
    st.divider()

    # Document upload
    st.markdown("**📚 Upload Document**")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], label_visibility="collapsed")
    if uploaded_file and st.button("📤 Upload & Index", use_container_width=True):
        with st.spinner("Parsing & Indexing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")}
                resp = requests.post(f"{API_BASE}/documents/upload", files=files)
                if resp.status_code == 200:
                    res_data = resp.json()
                    chars = res_data.get("characters_extracted", 0)
                    st.success(f"✅ Indexed: `{uploaded_file.name}` ({chars} characters)")
                    st.session_state.docs_uploaded += 1
                else:
                    st.error(f"Upload Error ({resp.status_code}): {resp.text}")
            except Exception as e:
                st.error(f"Upload failed: {e}")
    st.divider()

    # Retrieval source
    st.markdown("**🎯 Retrieval Source**")
    source = st.radio(
        "Source:",
        ["Agency docs (recommended)", "All documents"],
        index=0,
    )
    st.session_state.retrieval_category = "agency" if "Agency" in source else "all"

    # Reset session
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.rerun()

    # API health check
    try:
        h = requests.get("http://localhost:8000/health", timeout=2)
        if h.status_code == 200:
            st.success("🟢 API Online")
        else:
            st.error("🔴 API Error")
    except:
        st.error("🔴 API Offline")

# ─── Main Chat Area ─────────────────────────────────────────────────────────
st.markdown("## 💬 Conversational RAG Chat")
st.markdown("Ask anything about your uploaded documents. The AI **remembers your conversation** and cites exact sources.")
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📚 المصادر والمقتبسات (Source Citations)", expanded=False):
                for idx, src in enumerate(message["sources"], 1):
                    st.markdown(f"**مقتبس {idx}** — `{src.get('filename', 'Unknown')}`")
                    st.caption(f"> {src.get('snippet', '')}")

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_queries += 1

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("*⏳ Searching context & generating response...*")
        try:
            resp = requests.post(
                f"{API_BASE}/query",
                params={"question": prompt, "session_id": st.session_state.session_id,
                        "category": st.session_state.retrieval_category},
                timeout=180
            )
            resp.raise_for_status()
            data = resp.json()
            answer = data.get("answer", data.get("error", "No response"))
            sources = data.get("sources", [])

            placeholder.empty()
            st.write_stream(stream_text(answer))

            if sources:
                with st.expander("📚 المصادر والمقتبسات (Source Citations)", expanded=False):
                    for idx, src in enumerate(sources, 1):
                        st.markdown(f"**مقتبس {idx}** — `{src.get('filename', 'Unknown')}`")
                        st.caption(f"> {src.get('snippet', '')}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
        except requests.exceptions.ConnectionError:
            placeholder.error("❌ Cannot connect to API. Is the server running on port 8000?")
        except Exception as e:
            placeholder.error(f"❌ Error: {e}")


