"""RAG retrieval package — search, citations, grounded answers (Steps 5h–5m)."""

from rag.retrieval.citations import Citation, citations_from_hits, document_to_citation
from rag.retrieval.grounded import GroundedAnswer, generate_grounded_answer
from rag.retrieval.retriever import (
    INSUFFICIENT_EVIDENCE,
    RetrievalResult,
    retrieve_detailed,
)

__all__ = [
    "Citation",
    "GroundedAnswer",
    "INSUFFICIENT_EVIDENCE",
    "RetrievalResult",
    "citations_from_hits",
    "document_to_citation",
    "generate_grounded_answer",
    "retrieve_detailed",
]
