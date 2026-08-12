"""
LangChain retrieval against the Chroma index.

Supports metadata filters (asset/site/doc_type), excludes TEST-INJECT-999 by
default, and labels low-confidence / empty results as insufficient evidence.
"""
from dataclasses import dataclass

from langchain_core.documents import Document

from rag.ingestion.config import RagConfig
from rag.ingestion.index import get_vectorstore
from rag.ingestion.loader import TEST_INJECT_DOC_ID
from rag.retrieval.citations import Citation, citations_from_hits

# Chroma L2 distance: lower is closer. Above this → insufficient evidence.
DEFAULT_MAX_DISTANCE = 1.2

INSUFFICIENT_EVIDENCE = (
    "Insufficient evidence in the indexed procedures and guides for a reliable answer. "
    "Do not invent procedure steps. Refine the query (asset, alarm tag, site, or doc_id) "
    "or confirm the RAG index is built."
)


@dataclass
class RetrievalResult:
    """Structured retrieval outcome for the copilot / GUI."""

    query: str
    documents: list[Document]
    citations: list[Citation]
    scores: list[float]
    confidence: str  # "high" | "low" | "none"
    reason: str = ""

    @property
    def hits(self) -> list[Document]:
        return self.documents

    @property
    def insufficient_evidence(self) -> bool:
        return self.confidence in ("none", "low")


def _normalize_filters(filters: dict | None) -> dict | None:
    """Accept asset as alias for assets (substring match)."""
    if not filters:
        return None
    out = dict(filters)
    if "asset" in out and "assets" not in out:
        out["assets"] = out.pop("asset")
    elif "asset" in out:
        out.pop("asset")
    return out


def _build_chroma_filter(filters: dict | None) -> dict | None:
    """
    Build a Chroma where-filter from equality filters.

    Exact: doc_id, doc_type, site, revision
    Substring (post-filter): assets, units, alarm_tags
    """
    if not filters:
        return None

    exact_keys = {"doc_id", "doc_type", "site", "revision"}
    clauses = []
    for key, value in filters.items():
        if key in exact_keys and value not in (None, ""):
            clauses.append({key: {"$eq": str(value)}})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def _post_filter_docs(
    pairs: list[tuple[Document, float]],
    filters: dict | None,
    include_test_inject: bool,
) -> list[tuple[Document, float]]:
    """Substring filters + always-on TEST-INJECT-999 exclusion for normal search."""
    out = []
    for doc, score in pairs:
        meta = doc.metadata or {}
        doc_id = str(meta.get("doc_id") or "")

        if not include_test_inject and doc_id == TEST_INJECT_DOC_ID:
            continue

        if filters:
            keep = True
            for key in ("assets", "units", "alarm_tags"):
                needle = filters.get(key)
                if not needle:
                    continue
                hay = str(meta.get(key) or "")
                if str(needle).lower() not in hay.lower():
                    keep = False
                    break
            if not keep:
                continue

        out.append((doc, score))
    return out


def retrieve_detailed(
    query: str,
    k: int = 4,
    config: RagConfig = None,
    filters: dict = None,
    max_distance: float = DEFAULT_MAX_DISTANCE,
    fetch_k: int | None = None,
    include_test_inject: bool = False,
) -> RetrievalResult:
    """
    Embed query, top-k search, return text + metadata + scores.

    confidence:
      - none: no hits → insufficient evidence
      - low:  best distance > max_distance → insufficient evidence
      - high: usable evidence
    """
    if config is None:
        config = RagConfig()

    filters = _normalize_filters(filters)
    store = get_vectorstore(config=config)
    overfetch = fetch_k or (max(k * 3, k + 5) if filters else k + 2)
    where = _build_chroma_filter(filters)

    try:
        if where:
            pairs = store.similarity_search_with_score(query, k=overfetch, filter=where)
        else:
            pairs = store.similarity_search_with_score(query, k=overfetch)
    except Exception:
        pairs = store.similarity_search_with_score(query, k=overfetch)

    pairs = [(doc, float(score)) for doc, score in pairs]
    pairs = _post_filter_docs(pairs, filters, include_test_inject=include_test_inject)
    pairs = pairs[:k]

    if not pairs:
        return RetrievalResult(
            query=query,
            documents=[],
            citations=[],
            scores=[],
            confidence="none",
            reason=INSUFFICIENT_EVIDENCE,
        )

    docs = [d for d, _ in pairs]
    scores = [s for _, s in pairs]
    best = min(scores)
    citations = citations_from_hits(pairs)

    if best > max_distance:
        return RetrievalResult(
            query=query,
            documents=docs,
            citations=citations,
            scores=scores,
            confidence="low",
            reason=INSUFFICIENT_EVIDENCE,
        )

    return RetrievalResult(
        query=query,
        documents=docs,
        citations=citations,
        scores=scores,
        confidence="high",
        reason="",
    )
