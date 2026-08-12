"""
LangChain document loading.

Uses PyMuPDFLoader for each PDF and joins fields from metadata.json.
"""
import json
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

from rag.ingestion.config import RagConfig

TEST_INJECT_DOC_ID = "TEST-INJECT-999"


def load_metadata_rows(metadata_path: Path) -> list:
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata not found: {metadata_path}")
    with open(metadata_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("metadata.json must be a list")
    return data


def _join(values) -> str:
    if not values:
        return ""
    if isinstance(values, str):
        return values
    return " | ".join(str(v) for v in values)


def load_documents(
    config: RagConfig = None,
    include_test_inject: bool = False,
) -> list[Document]:
    """
    Load PDFs with LangChain PyMuPDFLoader.

    Returns a list of LangChain Document objects (usually one per page).
    Parent metadata from metadata.json is attached to every page.
    """
    if config is None:
        config = RagConfig()

    rows = load_metadata_rows(config.metadata_file)
    documents: list[Document] = []

    for row in rows:
        doc_id = row.get("doc_id")
        if not doc_id:
            raise ValueError(f"Missing doc_id in metadata: {row}")

        if doc_id == TEST_INJECT_DOC_ID and not include_test_inject:
            continue

        relative = row.get("pdf_path") or row.get("path")
        if not relative:
            raise ValueError(f"No pdf path for {doc_id}")

        pdf_file = (config.pdf_dir / relative).resolve()
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF missing for {doc_id}: {pdf_file}")

        loader = PyMuPDFLoader(str(pdf_file))
        pages = loader.load()

        base_meta = {
            "doc_id": doc_id,
            "title": row.get("title") or doc_id,
            "doc_type": row.get("doc_type") or "",
            "site": row.get("site") or "",
            "revision": row.get("revision") or "",
            "pdf_path": relative,
            "source": str(pdf_file),
            # Chroma-friendly flat strings
            "assets": _join(row.get("assets")),
            "units": _join(row.get("units")),
            "alarm_tags": _join(row.get("alarm_tags")),
        }

        for page in pages:
            meta = dict(page.metadata or {})
            meta.update(base_meta)
            documents.append(
                Document(page_content=page.page_content or "", metadata=meta)
            )

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"TOTAL PAGE DOCUMENTS: {len(docs)}\n")

    for i, doc in enumerate(docs, 1):
        print("=" * 80)
        print(f"[{i}/{len(docs)}] doc_id={doc.metadata.get('doc_id')}")
        print(f"title={doc.metadata.get('title')}")
        print(f"doc_type={doc.metadata.get('doc_type')}")
        print(f"site={doc.metadata.get('site')}")
        print(f"page={doc.metadata.get('page')}")
        print(f"pdf_path={doc.metadata.get('pdf_path')}")
        print(f"assets={doc.metadata.get('assets')}")
        print(f"alarm_tags={doc.metadata.get('alarm_tags')}")
        print(f"chars={len(doc.page_content)}")
        print("-" * 40)
        print(doc.page_content)
        print()
