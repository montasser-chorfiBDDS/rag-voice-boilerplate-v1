"""
Vector Store - Manages vector embeddings and similarity search
"""

from typing import List, Optional
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


class VectorStore:
    """Vector store for document embeddings and retrieval."""

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
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

    async def add_document(self, content: str, metadata: Optional[dict] = None):
        """
        Add a document to the vector store.

        Args:
            content: Document content
            metadata: Optional metadata
        """
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

        chunks = text_splitter.create_documents(
            texts=[content],
            metadatas=[metadata or {}],
        )

        # Add to vector store
        self.vector_store.add_documents(chunks)
        self._save_store()

    async def add_documents(self, documents: List[dict]):
        """
        Add multiple documents to the vector store.

        Args:
            documents: List of dicts with 'content' and 'metadata'
        """
        texts = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]

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

    def get_retriever(self, k: int = 4):
        """
        Get a retriever for the vector store.

        Args:
            k: Number of results to return

        Returns:
            Vector store retriever
        """
        return self.vector_store.as_retriever(search_kwargs={"k": k})

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
