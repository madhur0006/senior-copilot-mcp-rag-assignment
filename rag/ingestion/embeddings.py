"""LangChain OpenAI embeddings for document texts."""
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from rag.ingestion.config import RagConfig


def get_embeddings(config: RagConfig = None):
    """Return a LangChain OpenAI Embeddings instance."""
    if config is None:
        config = RagConfig()

    if config.provider != "openai":
        raise ValueError(
            f"Unsupported LLM_PROVIDER={config.provider!r}. This project uses OpenAI only."
        )

    key = config.openai_key
    if not key or key.startswith("sk-replace") or key == "replace-me":
        raise ValueError("OPENAI_API_KEY / LLM_API_KEY not set in .env")

    return OpenAIEmbeddings(model=config.embedding_model, api_key=key)


def embed_documents(
    documents: list[Document],
    config: RagConfig = None,
    embeddings=None,
) -> list[list[float]]:
    """Embed document page_content strings; returns vectors in the same order."""
    if config is None:
        config = RagConfig()
    if embeddings is None:
        embeddings = get_embeddings(config)

    texts = [d.page_content for d in documents]
    if not texts:
        return []
    return embeddings.embed_documents(texts)


if __name__ == "__main__":
    from rag.ingestion.chunker import chunk_documents
    from rag.ingestion.loader import load_documents

    config = RagConfig()
    chunks = chunk_documents(load_documents())
    print(f"Provider: {config.provider}")
    print(f"Model:    {config.embedding_model}")
    print(f"TOTAL CHUNKS TO EMBED: {len(chunks)}\n")

    vectors = embed_documents(chunks, config=config)

    for i, (chunk, vector) in enumerate(zip(chunks, vectors), 1):
        print("=" * 80)
        print(f"[{i}/{len(chunks)}] {chunk.metadata.get('chunk_id')}")
        print(f"doc_id={chunk.metadata.get('doc_id')}")
        print(f"chars={len(chunk.page_content)}")
        print(f"embedding_dim={len(vector)}")
        print(f"first_8_values={vector[:8]}")
        print(f"text_preview={chunk.page_content[:150].replace(chr(10), ' ')}...")
        print()

    print(f"DONE — embedded all {len(vectors)} chunks")
