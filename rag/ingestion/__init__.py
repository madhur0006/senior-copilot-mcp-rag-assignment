"""Document ingestion helpers — LangChain pipeline."""

from rag.ingestion.chunker import chunk_documents
from rag.ingestion.embeddings import embed_documents, get_embeddings
from rag.ingestion.index import build_index, get_vectorstore
from rag.ingestion.loader import load_documents

# Lazy import avoids RuntimeWarning when running: python -m rag.ingestion.pipeline


def __getattr__(name: str):
    if name == "run_ingestion":
        from rag.ingestion.pipeline import run_ingestion

        return run_ingestion
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "load_documents",
    "chunk_documents",
    "get_embeddings",
    "embed_documents",
    "build_index",
    "get_vectorstore",
    "run_ingestion",
]
