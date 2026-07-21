"""
RAG Voice Boilerplate - Main Application
A production-ready RAG application with voice processing capabilities.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.routes import router
from app.core.rag_engine import RAGEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    # Startup
    app.state.rag_engine = RAGEngine()
    yield
    # Shutdown - nothing to cleanup for simplified version


app = FastAPI(
    title="RAG Voice Boilerplate",
    description="A production-ready RAG application with voice processing",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "RAG Voice Boilerplate API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
