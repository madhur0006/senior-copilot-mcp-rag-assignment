"""PDF text extract helper tests."""
from pathlib import Path

from rag.ingestion.extract import extract_text_from_pdf

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PDF = (
    ROOT
    / "rag/documents-pdf/operating-procedures/OP-BFP-001-boiler-feed-pump-operation.pdf"
)


def test_extract_text_from_sample_pdf():
    text = extract_text_from_pdf(str(SAMPLE_PDF))
    assert len(text) > 200
    assert "Boiler Feed" in text or "OP-BFP-001" in text
