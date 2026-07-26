"""
RAG paths and LLM settings from .env (OpenAI).
"""
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class RagConfig(BaseSettings):
    """Config for RAG ingestion — reads from environment / .env"""

    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    document_pdf_path: str = Field(
        default="./rag/documents-pdf",
        alias="DOCUMENT_PDF_PATH",
    )
    metadata_path: str = Field(
        default="./rag/documents-pdf/metadata.json",
        alias="METADATA_PATH",
    )
    vector_store_url: str = Field(
        default="./rag/.index",
        alias="VECTOR_STORE_URL",
    )

    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small",
        alias="OPENAI_EMBEDDING_MODEL",
    )
    openai_chat_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_CHAT_MODEL",
    )

    @property
    def provider(self) -> str:
        return (self.llm_provider or "openai").strip().lower()

    @property
    def embedding_model(self) -> str:
        return self.openai_embedding_model

    @property
    def chat_model(self) -> str:
        return self.openai_chat_model

    @property
    def openai_key(self) -> str:
        return self.openai_api_key or self.llm_api_key

    @property
    def pdf_dir(self) -> Path:
        path = Path(self.document_pdf_path)
        if not path.is_absolute():
            path = ROOT / path
        return path.resolve()

    @property
    def metadata_file(self) -> Path:
        path = Path(self.metadata_path)
        if not path.is_absolute():
            path = ROOT / path
        return path.resolve()

    @property
    def index_dir(self) -> Path:
        path = Path(self.vector_store_url)
        if not path.is_absolute():
            path = ROOT / path
        return path.resolve()
