from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AlarmApiConfig(BaseSettings):
    """Configuration for Alarm API client - reads from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    base_url: str = Field(
        default="http://localhost:8000",
        alias="ALARM_API_BASE_URL",
    )
    token: str = Field(
        default="demo-token",
        alias="ALARM_API_TOKEN",
    )
    timeout_seconds: float = Field(
        default=30.0,
        alias="REQUEST_TIMEOUT_SECONDS",
    )
    retry_count: int = Field(
        default=3,
        alias="RETRY_COUNT",
    )
    client_id: str = Field(
        default="alarm-investigation-copilot",
        alias="ALARM_API_CLIENT_ID",
    )
    metadata_tag: str = Field(
        default="connector",
        alias="ALARM_API_METADATA_TAG",
    )

    @property
    def normalized_base_url(self) -> str:
        return self.base_url.rstrip("/")
