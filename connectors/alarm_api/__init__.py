"""Alarm Management API connector package.

This package is used by the MCP server only.
The copilot orchestration layer must not import and call this client directly
in the final architecture; it should go through MCP tools.
"""

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
