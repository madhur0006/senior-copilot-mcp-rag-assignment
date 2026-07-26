"""Unit tests for OpenAI chat invoke."""
from unittest.mock import MagicMock

import pytest

from rag.ingestion.config import RagConfig
from rag.llm.chat import get_chat_model, invoke_chat


def test_invoke_chat_returns_content():
    config = RagConfig(LLM_PROVIDER="openai", OPENAI_API_KEY="sk-fake")
    mock_chat = MagicMock()
    mock_chat.invoke.return_value = MagicMock(content="ok answer")

    result = invoke_chat("hello", config=config, chat_model=mock_chat)
    assert result == "ok answer"
    mock_chat.invoke.assert_called_once()


def test_invoke_chat_raises_errors():
    config = RagConfig(LLM_PROVIDER="openai", OPENAI_API_KEY="sk-fake")
    mock_chat = MagicMock()
    mock_chat.invoke.side_effect = ValueError("bad request")

    with pytest.raises(ValueError, match="bad request"):
        invoke_chat("hello", config=config, chat_model=mock_chat)


def test_get_chat_model_rejects_missing_key():
    config = RagConfig(LLM_PROVIDER="openai", OPENAI_API_KEY="", LLM_API_KEY="")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        get_chat_model(config)
