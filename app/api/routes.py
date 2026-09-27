"""
API Routes - FastAPI endpoints
"""

import io
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from pypdf import PdfReader

router = APIRouter()


@router.post("/query")
async def query_rag(request: Request, question: str, session_id: Optional[str] = "default", category: Optional[str] = "agency"):
    """
    Query the RAG engine with a text question.

    Args:
        question: User question
        session_id: Conversation identifier
        category: "agency" (trusted docs), "upload" (user uploads), or "all".
    """
    rag_engine = request.app.state.rag_engine
    cat = None if category == "all" else category
    result = await rag_engine.query(question, session_id=session_id, category=cat)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@router.post("/documents/upload")
async def upload_document(request: Request, file: UploadFile = File(...)):
    """
    Upload and index a PDF or TXT document into the vector store.
    """
    rag_engine = request.app.state.rag_engine
    filename = file.filename or "uploaded_document"

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    text_content = ""
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        try:
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            pages_text = []
            for i, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted and extracted.strip():
                    pages_text.append(extracted.strip())
            text_content = "\n\n".join(pages_text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    elif filename_lower.endswith(".txt") or filename_lower.endswith(".md"):
        try:
            text_content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text_content = file_bytes.decode("latin-1", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or TXT.")

    if not text_content or not text_content.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract readable text from document. If this is a scanned PDF image, OCR is required."
        )

    await rag_engine.add_document(text_content, metadata={"filename": filename})
    return {
        "status": "success",
        "filename": filename,
        "characters_extracted": len(text_content),
        "message": f"Successfully indexed {filename} ({len(text_content)} characters)."
    }

