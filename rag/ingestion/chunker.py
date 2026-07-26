"""
LangChain-friendly chunking with better section / table handling.

Strategy:
1. Merge all pages of the same PDF into one document
2. Split on numbered section headings (1. Purpose, 5. Likely causes, …)
3. Keep each section as one chunk when possible (so tables stay together)
4. Only if a section is still very long, use RecursiveCharacterTextSplitter
"""
import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Soft max for a normal section chunk
DEFAULT_CHUNK_SIZE = 1800
DEFAULT_CHUNK_OVERLAP = 200
# Hard max — only split a section if bigger than this
SECTION_HARD_MAX = 3500

# Match: "1. Purpose" or "8.1 High vibration" (not list items with leading spaces)
SECTION_HEADING = re.compile(
    r"^(?P<title>(?:\d+\.\d+\s+[A-Z][^\n]{0,70}|\d+\.\s+[A-Z][^\n]{0,70}))$",
    re.MULTILINE,
)


def get_text_splitter(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> RecursiveCharacterTextSplitter:
    """Fallback splitter for very long sections only."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def merge_pages_by_doc(documents: list[Document]) -> list[Document]:
    """Combine multi-page PDF pages into one Document per doc_id."""
    grouped: dict[str, list[Document]] = {}
    order: list[str] = []

    for doc in documents:
        doc_id = doc.metadata.get("doc_id") or doc.metadata.get("source") or "UNKNOWN"
        if doc_id not in grouped:
            grouped[doc_id] = []
            order.append(doc_id)
        grouped[doc_id].append(doc)

    merged = []
    for doc_id in order:
        pages = grouped[doc_id]
        # Sort by page number when available
        pages = sorted(pages, key=lambda d: d.metadata.get("page", 0) or 0)
        text = "\n".join((p.page_content or "").strip() for p in pages if p.page_content)
        meta = dict(pages[0].metadata)
        meta.pop("page", None)
        merged.append(Document(page_content=text.strip(), metadata=meta))

    return merged


def split_text_by_sections(text: str) -> list[tuple[str, str]]:
    """
    Split full document text into (section_title, section_body) pairs.
    """
    if not text or not text.strip():
        return []

    matches = list(SECTION_HEADING.finditer(text))
    if not matches:
        return [("Full document", text.strip())]

    sections: list[tuple[str, str]] = []

    preface = text[: matches[0].start()].strip()
    if preface:
        sections.append(("Introduction", preface))

    for i, match in enumerate(matches):
        title = match.group("title").strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((title, body))

    return sections


def chunk_documents(
    documents: list[Document],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Document]:
    """
    Chunk documents with section-aware splitting.

    Tables/sections stay together unless a section exceeds SECTION_HARD_MAX.
    """
    merged = merge_pages_by_doc(documents)
    splitter = get_text_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    result: list[Document] = []

    for doc in merged:
        sections = split_text_by_sections(doc.page_content)

        for section_title, section_text in sections:
            meta = dict(doc.metadata)
            meta["section"] = section_title

            # Keep whole section if it fits (or is a table-like section under hard max)
            if len(section_text) <= SECTION_HARD_MAX:
                result.append(Document(page_content=section_text, metadata=meta))
                continue

            # Very long section only — fall back to LangChain splitter
            for piece in splitter.split_text(section_text):
                piece_meta = dict(meta)
                result.append(Document(page_content=piece, metadata=piece_meta))

    # Stable chunk ids per doc
    counters: dict[str, int] = {}
    for chunk in result:
        doc_id = chunk.metadata.get("doc_id", "DOC")
        n = counters.get(doc_id, 0)
        chunk.metadata["chunk_id"] = f"{doc_id}::chunk-{n:03d}"
        counters[doc_id] = n + 1

    return result


if __name__ == "__main__":
    from rag.ingestion.loader import load_documents

    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"PAGE DOCUMENTS: {len(docs)}")
    print(f"MERGED DOCS:    {len(merge_pages_by_doc(docs))}")
    print(f"TOTAL CHUNKS:   {len(chunks)}\n")

    for i, chunk in enumerate(chunks, 1):
        print("=" * 80)
        print(f"[{i}/{len(chunks)}] {chunk.metadata.get('chunk_id')}")
        print(f"doc_id={chunk.metadata.get('doc_id')}")
        print(f"section={chunk.metadata.get('section')}")
        print(f"title={chunk.metadata.get('title')}")
        print(f"doc_type={chunk.metadata.get('doc_type')}")
        print(f"site={chunk.metadata.get('site')}")
        print(f"assets={chunk.metadata.get('assets')}")
        print(f"chars={len(chunk.page_content)}")
        print("-" * 40)
        print(chunk.page_content)
        print()
