"""PDF loader unit tests."""
from pathlib import Path

import pytest
from langchain_core.documents import Document

from rag.ingestion.config import RagConfig
from rag.ingestion.loader import TEST_INJECT_DOC_ID, load_documents, load_metadata_rows


def test_load_metadata_rows():
    config = RagConfig()
    rows = load_metadata_rows(config.metadata_file)
    assert len(rows) >= 15
    assert any(r["doc_id"] == "OP-BFP-001" for r in rows)


def test_load_documents_returns_langchain_documents():
    docs = load_documents()
    assert len(docs) > 0
    assert isinstance(docs[0], Document)
    assert docs[0].page_content
    assert docs[0].metadata.get("doc_id")
    assert docs[0].metadata.get("site") == "EastRefinery"


def test_load_documents_skips_test_inject():
    docs = load_documents()
    ids = {d.metadata.get("doc_id") for d in docs}
    assert "OP-BFP-001" in ids
    assert TEST_INJECT_DOC_ID not in ids


def test_load_documents_can_include_test_inject():
    docs = load_documents(include_test_inject=True)
    ids = {d.metadata.get("doc_id") for d in docs}
    assert TEST_INJECT_DOC_ID in ids


def test_missing_metadata_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("METADATA_PATH", str(tmp_path / "missing.json"))
    config = RagConfig()
    with pytest.raises(FileNotFoundError):
        load_documents(config=config)
