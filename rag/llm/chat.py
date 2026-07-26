"""
LangChain chat models — OpenAI.
"""
from langchain_openai import ChatOpenAI

from rag.ingestion.config import RagConfig


def get_chat_model(config: RagConfig = None):
    """Return a LangChain OpenAI chat model."""
    if config is None:
        config = RagConfig()

    if config.provider != "openai":
        raise ValueError(
            f"Unsupported LLM_PROVIDER={config.provider!r}. This project uses OpenAI only."
        )

    key = config.openai_key
    if not key or key.startswith("sk-replace") or key == "replace-me":
        raise ValueError("OPENAI_API_KEY / LLM_API_KEY not set in .env")

    return ChatOpenAI(model=config.chat_model, api_key=key, temperature=0.2)


def invoke_chat(
    prompt: str,
    config: RagConfig = None,
    chat_model=None,
) -> str:
    """Call the OpenAI chat model and return text content."""
    if config is None:
        config = RagConfig()
    if chat_model is None:
        chat_model = get_chat_model(config)

    response = chat_model.invoke(prompt)
    content = getattr(response, "content", response)
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            else:
                parts.append(str(block))
        return "".join(parts)
    return str(content)
