"""Citation and retrieval unit tests."""
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from rag.ingestion.loader import TEST_INJECT_DOC_ID
from rag.retrieval.citations import citations_from_hits, document_to_citation
from rag.retrieval.retriever import (
    INSUFFICIENT_EVIDENCE,
    _normalize_filters,
    _post_filter_docs,
    retrieve_detailed,
)


def test_document_to_citation_includes_section_and_source():
    doc = Document(
        page_content="Hello world " * 40,
        metadata={
            "doc_id": "OP-BFP-001",
            "title": "BFP OP",
            "section": "5. Alarm response",
            "chunk_id": "OP-BFP-001::chunk-003",
            "pdf_path": "operating-procedures/OP-BFP-001.pdf",
            "doc_type": "operating_procedure",
            "site": "EastRefinery",
        },
    )
    cite = document_to_citation(doc, score=0.42, excerpt_chars=20)
    assert cite.doc_id == "OP-BFP-001"
    assert cite.section == "5. Alarm response"
    assert cite.source_path == "operating-procedures/OP-BFP-001.pdf"
    assert cite.pdf_path == cite.source_path
    assert cite.excerpt.endswith("...")


def test_citations_from_hits_with_scores():
    docs = [
        Document(
            page_content="a",
            metadata={
                "doc_id": "A",
                "title": "A",
                "section": "Intro",
                "chunk_id": "A-1",
                "pdf_path": "a.pdf",
            },
        ),
    ]
    cites = citations_from_hits([(docs[0], 0.1)])
    assert cites[0].section == "Intro"
    assert cites[0].score == 0.1


def test_normalize_filters_asset_alias():
    assert _normalize_filters({"asset": "BFP-101"}) == {"assets": "BFP-101"}


def test_post_filter_excludes_test_inject_by_default():
    pairs = [
        (
            Document(
                page_content="hostile",
                metadata={"doc_id": TEST_INJECT_DOC_ID, "assets": "BFP-101"},
            ),
            0.01,
        ),
        (
            Document(
                page_content="ok",
                metadata={"doc_id": "OP-BFP-001", "assets": "BFP-101"},
            ),
            0.2,
        ),
    ]
    kept = _post_filter_docs(pairs, {"assets": "BFP-101"}, include_test_inject=False)
    assert len(kept) == 1
    assert kept[0][0].metadata["doc_id"] == "OP-BFP-001"


def test_post_filter_can_include_test_inject():
    pairs = [
        (
            Document(page_content="hostile", metadata={"doc_id": TEST_INJECT_DOC_ID}),
            0.01,
        ),
    ]
    kept = _post_filter_docs(pairs, None, include_test_inject=True)
    assert len(kept) == 1


def test_retrieve_detailed_none_confidence():
    mock_store = MagicMock()
    mock_store.similarity_search_with_score.return_value = []

    with patch("rag.retrieval.retriever.get_vectorstore", return_value=mock_store):
        result = retrieve_detailed("anything", k=3)

    assert result.confidence == "none"
    assert result.insufficient_evidence
    assert "Insufficient evidence" in result.reason


def test_retrieve_detailed_low_confidence():
    doc = Document(
        page_content="weak match",
        metadata={
            "doc_id": "X",
            "title": "X",
            "section": "Notes",
            "chunk_id": "X-1",
            "pdf_path": "x.pdf",
        },
    )
    mock_store = MagicMock()
    mock_store.similarity_search_with_score.return_value = [(doc, 2.5)]

    with patch("rag.retrieval.retriever.get_vectorstore", return_value=mock_store):
        result = retrieve_detailed("anything", k=3, max_distance=1.2)

    assert result.confidence == "low"
    assert result.reason == INSUFFICIENT_EVIDENCE


def test_retrieve_detailed_high_confidence():
    doc = Document(
        page_content="good match",
        metadata={
            "doc_id": "OP-BFP-001",
            "title": "BFP",
            "section": "5. Alarm response",
            "chunk_id": "OP-BFP-001::chunk-001",
            "pdf_path": "op.pdf",
        },
    )
    mock_store = MagicMock()
    mock_store.similarity_search_with_score.return_value = [(doc, 0.3)]

    with patch("rag.retrieval.retriever.get_vectorstore", return_value=mock_store):
        result = retrieve_detailed("bfp vibration", k=3, max_distance=1.2)

    assert result.confidence == "high"
    assert result.citations[0].section == "5. Alarm response"
    assert result.scores[0] == 0.3
