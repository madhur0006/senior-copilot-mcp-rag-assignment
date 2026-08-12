"""
Full RAG ingestion: load PDFs + metadata → chunk → embed → Chroma index.

  PYTHONPATH=. python3 -m rag.ingestion.pipeline
"""
from rag.ingestion.chunker import chunk_documents
from rag.ingestion.config import RagConfig
from rag.ingestion.index import build_index
from rag.ingestion.loader import load_documents


def run_ingestion(
    config: RagConfig = None,
    include_test_inject: bool = False,
    reset: bool = True,
):
    """Run the full ingest pipeline and return (chunks, vectorstore)."""
    if config is None:
        config = RagConfig()

    docs = load_documents(config=config, include_test_inject=include_test_inject)
    chunks = chunk_documents(docs)
    store = build_index(chunks, config=config, reset=reset)
    return chunks, store


if __name__ == "__main__":
    config = RagConfig()
    print(f"Provider:  {config.provider}")
    print(f"Embed:     {config.embedding_model}")
    print(f"PDFs:      {config.pdf_dir}")
    print(f"Metadata:  {config.metadata_file}")
    print(f"Index:     {config.index_dir}")
    print("Running full ingestion (load → chunk → embed → Chroma)...\n")

    chunks, store = run_ingestion(config=config, reset=True)
    print(f"DONE — indexed {len(chunks)} chunks into {config.index_dir}")
    print(f"Collection count: {store._collection.count()}")
