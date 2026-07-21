"""
API Routes - FastAPI endpoints
"""

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.post("/query")
async def query_rag(request: Request, question: str):
    """
    Query the RAG engine with a text question.
    """
    rag_engine = request.app.state.rag_engine
    result = await rag_engine.query(question)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result
