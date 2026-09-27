"""
RAG Engine - Core retrieval augmented generation logic
Uses a local Ollama LLM (free, no cloud credits required)
"""

from app.config import settings
from app.database.vector_store import VectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from typing import Optional

# Custom prompts for multilingual (Arabic/English) RAG
qa_template = """أنت مساعد ذكي متميز ومتخصص في تحليل المستندات والوثائق الإدارية والقانونية.
استخدم القطع والنصوص التالية المأخوذة من المستندات المرفقة فقط للإجابة عن سؤال المستخدم بشكل وافٍ ودقيق باللغة العربية.
إذا لم تكن الإجابة موجودة بوضوح في المستندات المرفقة، أجب باحترام بأن المعطيات غير متوفرة في المستندات المرفوعة.

المستندات والمعطيات المتاحة:
{context}

السؤال: {question}
الإجابة المفصلة:"""

QA_PROMPT = PromptTemplate(
    template=qa_template, input_variables=["context", "question"]
)

condense_template = """بناءً على المحادثة السابقة والسؤال الجديد، أعد صياغة السؤال الجديد ليكتب بشكل مستقل باللغة العربية.

تاريخ المحادثة:
{chat_history}
السؤال الجديد: {question}
السؤال المستقل:"""

CONDENSE_PROMPT = PromptTemplate(
    template=condense_template, input_variables=["chat_history", "question"]
)


class RAGEngine:
    """RAG Engine using a local Ollama LLM (fully free, no cloud credits)."""

    def __init__(self):
        self.llm = Ollama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.3,
            num_predict=700,
        )
        self.vector_store = VectorStore()
        self.sessions = {}

    def get_session_memory(self, session_id: str):
        """Get or create conversation memory for a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True, output_key="answer"
            )
        return self.sessions[session_id]

    async def query(self, question: str, session_id: str = "default", category: Optional[str] = None) -> dict:
        """
        Query the RAG engine with a question using conversational memory.

        Args:
            question: User question
            session_id: Conversation session identifier
            category: Optional category filter ("agency" or "upload"). None = all documents.
        """
        try:
            memory = self.get_session_memory(session_id)
            retriever = self.vector_store.get_retriever(k=6, category=category)
            chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory,
                combine_docs_chain_kwargs={"prompt": QA_PROMPT},
                condense_question_prompt=CONDENSE_PROMPT,
                return_source_documents=True,
                output_key="answer",
            )
            result = chain.invoke({"question": question})

            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    filename = doc.metadata.get("filename", "مستند غير معروف")
                    content_snippet = doc.page_content.strip()
                    if len(content_snippet) > 250:
                        content_snippet = content_snippet[:250] + "..."
                    sources.append({
                        "filename": filename,
                        "snippet": content_snippet
                    })

            return {
                "answer": result["answer"],
                "sources": sources
            }
        except Exception as e:
            return {"error": str(e)}

    async def add_document(self, content: str, metadata: dict = None, category: str = "upload") -> bool:
        """Add a document to the vector store."""
        await self.vector_store.add_document(content, metadata, category=category)
        return True
