"""
Database - SQLite database for metadata storage
"""

import sqlite3
from typing import Optional, List, Dict
from pathlib import Path

from app.config import settings


class Database:
    """SQLite database for storing document metadata."""

    def __init__(self):
        self.db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    content_hash TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT,
                    sources TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    async def add_document(self, filename: str, content_hash: str, metadata: Optional[str] = None):
        """Add document record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO documents (filename, content_hash, metadata) VALUES (?, ?, ?)",
                (filename, content_hash, metadata),
            )
            conn.commit()

    async def add_conversation(self, query: str, response: str, sources: Optional[str] = None):
        """Add conversation record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (query, response, sources) VALUES (?, ?, ?)",
                (query, response, sources),
            )
            conn.commit()

    async def get_documents(self) -> List[Dict]:
        """Get all documents."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    async def get_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM conversations ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
