"""
Helper utilities
"""

import hashlib
from typing import Optional


def calculate_hash(content: str) -> str:
    """Calculate SHA256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_metadata(metadata: Optional[dict]) -> str:
    """Format metadata dictionary to string."""
    if not metadata:
        return ""
    return " | ".join(f"{k}: {v}" for k, v in metadata.items())
