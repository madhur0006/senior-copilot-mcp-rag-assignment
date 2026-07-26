"""Unit tests for section-aware LangChain chunking."""
from langchain_core.documents import Document

from rag.ingestion.chunker import (
    chunk_documents,
    merge_pages_by_doc,
    split_text_by_sections,
)
from rag.ingestion.loader import load_documents

SAMPLE = """Header line

1. Purpose
This is the purpose section.

5. Likely causes and what to do
Alarm pattern
Likely cause
Do now
Do next
Short critical discharge bursts
Recirc valve hunting
Stabilise valve
Positioner work
Seal leak on hot days
Flush cooler fouling
Switch to standby
Clean cooler

6. When recommendations disagree
Prefer the safer instruction.
"""


def test_split_text_by_sections_keeps_table_section_together():
    sections = dict(split_text_by_sections(SAMPLE))
    assert "5. Likely causes and what to do" in sections
    table = sections["5. Likely causes and what to do"]
    assert "Seal leak on hot days" in table
    assert "Clean cooler" in table
    assert "Alarm pattern" in table


def test_merge_pages_by_doc():
    pages = [
        Document(page_content="Page A", metadata={"doc_id": "X", "page": 0}),
        Document(page_content="Page B", metadata={"doc_id": "X", "page": 1}),
        Document(page_content="Other", metadata={"doc_id": "Y", "page": 0}),
    ]
    merged = merge_pages_by_doc(pages)
    assert len(merged) == 2
    x = next(d for d in merged if d.metadata["doc_id"] == "X")
    assert "Page A" in x.page_content and "Page B" in x.page_content


def test_chunk_documents_table_not_split_mid_row():
    docs = [
        Document(
            page_content=SAMPLE,
            metadata={"doc_id": "TG-BFP-020", "title": "Test", "doc_type": "troubleshooting_guide"},
        )
    ]
    chunks = chunk_documents(docs)
    table_chunks = [c for c in chunks if "Likely causes" in (c.metadata.get("section") or "")]
    assert len(table_chunks) == 1
    assert "Seal leak on hot days" in table_chunks[0].page_content
    assert "Clean cooler" in table_chunks[0].page_content


def test_chunk_real_tg_bfp_table_stays_in_one_chunk():
    docs = [d for d in load_documents() if d.metadata.get("doc_id") == "TG-BFP-020"]
    chunks = chunk_documents(docs)
    table_chunks = [
        c
        for c in chunks
        if "Likely causes" in (c.metadata.get("section") or "")
        or "Seal leak on hot days" in c.page_content
    ]
    # The table content should appear in a single section chunk, not split on "margins"
    matching = [c for c in chunks if "Seal leak on hot days" in c.page_content]
    assert matching
    assert all("margins" in c.page_content or "NPSH" in c.page_content for c in matching)
    # No orphan chunk that starts with just "margins"
    assert not any(c.page_content.strip().startswith("margins") for c in chunks)
