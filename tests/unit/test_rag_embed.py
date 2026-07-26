"""Unit tests for OpenAI embeddings factory (mocked)."""
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from rag.ingestion.config import RagConfig
from rag.ingestion.embeddings import embed_documents, get_embeddings


def test_embed_documents_uses_langchain_embeddings():
    config = RagConfig(LLM_PROVIDER="openai", OPENAI_API_KEY="sk-fake")
    mock_emb = MagicMock()
    mock_emb.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]

    docs = [
        Document(page_content="hello", metadata={}),
        Document(page_content="world", metadata={}),
    ]
    vectors = embed_documents(docs, config=config, embeddings=mock_emb)
    assert vectors == [[0.1, 0.2], [0.3, 0.4]]
    mock_emb.embed_documents.assert_called_once()


def test_get_embeddings_rejects_missing_openai_key():
    config = RagConfig(LLM_PROVIDER="openai", OPENAI_API_KEY="", LLM_API_KEY="")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        get_embeddings(config)


def test_get_embeddings_rejects_unknown_provider():
    config = RagConfig(LLM_PROVIDER="google", OPENAI_API_KEY="sk-fake")
    with pytest.raises(ValueError, match="OpenAI only"):
        get_embeddings(config)


def test_get_embeddings_openai_constructs_langchain_class():
    with patch("rag.ingestion.embeddings.OpenAIEmbeddings") as mock_cls:
        mock_cls.return_value = MagicMock(name="embeddings")
        config = RagConfig(
            LLM_PROVIDER="openai",
            OPENAI_API_KEY="sk-real",
            OPENAI_EMBEDDING_MODEL="text-embedding-3-small",
        )
        result = get_embeddings(config)
        mock_cls.assert_called_once()
        assert result is mock_cls.return_value
