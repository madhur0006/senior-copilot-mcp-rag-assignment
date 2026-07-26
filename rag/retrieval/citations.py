"""
Citation helpers for RAG retrieval hits (Step 5j).

Every hit returns: doc_id, title, section, source path, short excerpt.
"""
from dataclasses import asdict, dataclass

from langchain_core.documents import Document


@dataclass
class Citation:
    doc_id: str
    title: str
    section: str
    source_path: str
    excerpt: str
    chunk_id: str = ""
    doc_type: str = ""
    site: str = ""
    score: float | None = None

    # Back-compat alias used in earlier code/docs
    @property
    def pdf_path(self) -> str:
        return self.source_path

    def to_dict(self) -> dict:
        data = asdict(self)
        data["pdf_path"] = self.source_path
        return data


def document_to_citation(
    doc: Document,
    score: float | None = None,
    excerpt_chars: int = 280,
) -> Citation:
    """Build a citation from a LangChain Document."""
    text = (doc.page_content or "").strip()
    excerpt = text[:excerpt_chars]
    if len(text) > excerpt_chars:
        excerpt += "..."
    meta = doc.metadata or {}
    source_path = str(
        meta.get("pdf_path") or meta.get("source_path") or meta.get("source") or ""
    )
    return Citation(
        doc_id=str(meta.get("doc_id") or ""),
        title=str(meta.get("title") or meta.get("doc_id") or ""),
        section=str(meta.get("section") or ""),
        source_path=source_path,
        excerpt=excerpt,
        chunk_id=str(meta.get("chunk_id") or ""),
        doc_type=str(meta.get("doc_type") or ""),
        site=str(meta.get("site") or ""),
        score=score,
    )


def citations_from_hits(
    hits: list,
    excerpt_chars: int = 280,
) -> list[Citation]:
    """
    Convert retrieve hits to citations.

    Accepts either Document list or (Document, score) pairs.
    """
    citations: list[Citation] = []
    for item in hits:
        if isinstance(item, tuple) and len(item) == 2:
            doc, score = item
            citations.append(
                document_to_citation(doc, score=float(score), excerpt_chars=excerpt_chars)
            )
        else:
            citations.append(document_to_citation(item, excerpt_chars=excerpt_chars))
    return citations
