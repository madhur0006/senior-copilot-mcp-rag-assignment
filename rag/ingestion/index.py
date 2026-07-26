"""
LangChain + Chroma vector index.

Build / open the local Chroma store under VECTOR_STORE_URL.
"""
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag.ingestion.config import RagConfig
from rag.ingestion.embeddings import get_embeddings

COLLECTION_NAME = "alarm_rag"


def get_vectorstore(config: RagConfig = None, embeddings=None) -> Chroma:
    """Open (or create) the persistent Chroma collection."""
    if config is None:
        config = RagConfig()
    if embeddings is None:
        embeddings = get_embeddings(config)

    config.index_dir.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(config.index_dir),
    )


def build_index(
    chunks: list[Document],
    config: RagConfig = None,
    reset: bool = True,
) -> Chroma:
    """
    Upsert chunks into Chroma.

    If reset=True, delete the old collection folder first so rebuild is clean.
    """
    if config is None:
        config = RagConfig()

    embeddings = get_embeddings(config)

    if reset:
        _clear_index_dir(config.index_dir)

    config.index_dir.mkdir(parents=True, exist_ok=True)

    if not chunks:
        return get_vectorstore(config=config, embeddings=embeddings)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(config.index_dir),
    )


def _clear_index_dir(index_dir: Path) -> None:
    """Remove old index files if present."""
    if not index_dir.exists():
        return
    for path in index_dir.rglob("*"):
        if path.is_file():
            path.unlink()
    for path in sorted(index_dir.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass
