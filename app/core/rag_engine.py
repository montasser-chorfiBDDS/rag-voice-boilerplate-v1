"""
RAG Engine - Core retrieval augmented generation logic
"""

from app.config import settings


class RAGEngine:
    """RAG Engine for retrieval augmented generation."""

    def __init__(self):
        from transformers import pipeline
        self.llm = pipeline(
            "text-generation",
            model=settings.HUGGINGFACE_MODEL,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
        )

    async def query(self, question: str) -> dict:
        """
        Query the RAG engine with a question.
        """
        try:
            prompt = f"Question: {question}\nAnswer:"
            result = self.llm(prompt)[0]["generated_text"]
            answer = result[len(prompt):].strip().split("\n")[0].strip()
            return {"answer": answer}
        except Exception as e:
            return {"error": str(e)}

    async def add_document(self, content: str, metadata: dict = None) -> bool:
        return True