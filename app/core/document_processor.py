"""
Document Processor - Handles document parsing and preprocessing
"""

from typing import List, Optional
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)

from app.config import settings


class DocumentProcessor:
    """Process and chunk documents for RAG."""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )

    async def process_file(self, file_path: str) -> List[dict]:
        """
        Process a file and return chunks.

        Args:
            file_path: Path to the file

        Returns:
            List of document chunks
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        # Load document based on type
        if suffix == ".pdf":
            loader = PyPDFLoader(file_path)
        elif suffix == ".csv":
            loader = CSVLoader(file_path)
        elif suffix in [".txt", ".md"]:
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        # Load and split
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)

        return [
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]

    async def process_text(self, text: str, metadata: Optional[dict] = None) -> List[dict]:
        """
        Process raw text and return chunks.

        Args:
            text: Raw text content
            metadata: Optional metadata

        Returns:
            List of document chunks
        """
        chunks = self.text_splitter.create_documents(
            texts=[text],
            metadatas=[metadata or {}],
        )

        return [
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]

    async def process_multiple_files(self, file_paths: List[str]) -> List[dict]:
        """
        Process multiple files.

        Args:
            file_paths: List of file paths

        Returns:
            List of all document chunks
        """
        all_chunks = []
        for file_path in file_paths:
            chunks = await self.process_file(file_path)
            all_chunks.extend(chunks)
        return all_chunks
