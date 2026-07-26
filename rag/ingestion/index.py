"""
LangChain + Chroma vector index.

Build / open the local Chroma store under VECTOR_STORE_URL.

Uses an explicit chromadb.PersistentClient so LangChain does not fall back
to HttpClient(localhost:8000) — that port is the Alarm API simulator and
causes: "Could not connect to tenant default_tenant".
"""
from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag.ingestion.config import RagConfig
from rag.ingestion.embeddings import get_embeddings

COLLECTION_NAME = "alarm_rag"


def _clear_chroma_system_cache() -> None:
    """Avoid SharedSystemClient conflicts across Streamlit reruns."""
    try:
        from chromadb.api.client import SharedSystemClient

        SharedSystemClient.clear_system_cache()
    except Exception:
        pass


def _persistent_client(index_dir: Path) -> chromadb.PersistentClient:
    index_dir.mkdir(parents=True, exist_ok=True)
    _clear_chroma_system_cache()
    return chromadb.PersistentClient(path=str(index_dir))


def get_vectorstore(config: RagConfig = None, embeddings=None) -> Chroma:
    """Open (or create) the persistent Chroma collection."""
    if config is None:
        config = RagConfig()
    if embeddings is None:
        embeddings = get_embeddings(config)

    client = _persistent_client(config.index_dir)
    return Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
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
        _clear_chroma_system_cache()
        _clear_index_dir(config.index_dir)

    if not chunks:
        return get_vectorstore(config=config, embeddings=embeddings)

    client = _persistent_client(config.index_dir)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        client=client,
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
