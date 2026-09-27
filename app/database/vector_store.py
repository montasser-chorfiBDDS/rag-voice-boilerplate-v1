"""
Vector Store - Manages vector embeddings and similarity search
"""

from typing import List, Optional
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from huggingface_hub import InferenceClient
from typing import List

from app.config import settings


class HFHubEmbeddings(Embeddings):
    """Embeddings using huggingface_hub InferenceClient (new router endpoint)."""

    def __init__(self, model_name: str, api_key: str):
        self.client = InferenceClient(model=model_name, token=api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.feature_extraction(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
        result = self.client.feature_extraction(text)
        return result.tolist() if hasattr(result[0], '__iter__') is False else result[0].tolist()


class VectorStore:
    """Vector store for document embeddings and retrieval."""

    def __init__(self):
        self.embeddings = HFHubEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            api_key=settings.HUGGINGFACE_API_KEY
        )
        self.vector_store = None
        self._load_or_create_store()

    def _load_or_create_store(self):
        """Load existing vector store or create new one."""
        store_path = Path(settings.VECTOR_STORE_PATH)
        store_path.mkdir(parents=True, exist_ok=True)

        index_path = store_path / "index.faiss"
        if index_path.exists():
            self.vector_store = FAISS.load_local(
                str(store_path),
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            # Create empty vector store with dummy document
            self.vector_store = FAISS.from_texts(
                ["Initial document for vector store initialization"],
                self.embeddings,
            )

    async def add_document(self, content: str, metadata: Optional[dict] = None, category: str = "upload"):
        """
        Add a document to the vector store.

        Args:
            content: Document content
            metadata: Optional metadata
            category: Document category filter key ("agency" or "upload")
        """
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

        meta = dict(metadata or {})
        meta["category"] = category

        chunks = text_splitter.create_documents(
            texts=[content],
            metadatas=[meta],
        )

        # Add to vector store
        self.vector_store.add_documents(chunks)
        self._save_store()

    async def add_documents(self, documents: List[dict], category: str = "upload"):
        """
        Add multiple documents to the vector store.

        Args:
            documents: List of dicts with 'content' and 'metadata'
            category: Document category filter key ("agency" or "upload")
        """
        texts = [doc["content"] for doc in documents]
        metadatas = []
        for doc in documents:
            meta = dict(doc.get("metadata", {}))
            meta["category"] = category
            metadatas.append(meta)

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

        chunks = text_splitter.create_documents(
            texts=texts,
            metadatas=metadatas,
        )

        # Add to vector store
        self.vector_store.add_documents(chunks)
        self._save_store()

    def get_retriever(self, k: int = 4, category: Optional[str] = None):
        """
        Get a retriever for the vector store.

        Args:
            k: Number of results to return
            category: Optional category to filter by ("agency" or "upload"). None = all.

        Returns:
            Vector store retriever
        """
        doc_values = {}
        for doc_id, doc in self.vector_store.docstore._dict.items():
            if category is None or doc.metadata.get("category") == category:
                doc_values[doc_id] = doc

        docs = list(doc_values.values())
        if not docs:
            return self.vector_store.as_retriever(search_kwargs={"k": k})

        bm25_retriever = BM25Retriever.from_documents(docs)
        bm25_retriever.k = k
        if category is not None:
            faiss_kwargs = {"k": k, "filter": {"category": category}}
        else:
            faiss_kwargs = {"k": k}
        faiss_retriever = self.vector_store.as_retriever(search_kwargs=faiss_kwargs)

        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever],
            weights=[0.3, 0.7]
        )
        return ensemble_retriever

    async def similarity_search(self, query: str, k: int = 4) -> List[dict]:
        """
        Perform similarity search.

        Args:
            query: Search query
            k: Number of results

        Returns:
            List of similar documents
        """
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score,
            }
            for doc, score in results
        ]

    def _save_store(self):
        """Save vector store to disk."""
        self.vector_store.save_local(settings.VECTOR_STORE_PATH)

    async def close(self):
        """Cleanup resources."""
        self._save_store()
