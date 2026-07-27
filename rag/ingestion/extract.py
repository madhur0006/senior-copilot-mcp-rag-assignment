"""Compatibility helper — prefer rag.ingestion.loader.load_documents for ingestion."""


def extract_text_from_pdf(pdf_file: str) -> str:
    from langchain_community.document_loaders import PyMuPDFLoader

    pages = PyMuPDFLoader(pdf_file).load()
    return "\n".join(p.page_content or "" for p in pages).strip()
