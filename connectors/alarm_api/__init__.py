"""Alarm Management API connector (used by the MCP server)."""

from connectors.alarm_api.client import AlarmApiClient
from connectors.alarm_api.config import AlarmApiConfig
from connectors.alarm_api.errors import (
    AlarmApiAuthError,
    AlarmApiError,
    AlarmApiNotFoundError,
    AlarmApiTimeoutError,
    AlarmApiValidationError,
)

__all__ = [
    "AlarmApiClient",
    "AlarmApiConfig",
    "AlarmApiAuthError",
    "AlarmApiError",
    "AlarmApiNotFoundError",
    "AlarmApiTimeoutError",
    "AlarmApiValidationError",
]
