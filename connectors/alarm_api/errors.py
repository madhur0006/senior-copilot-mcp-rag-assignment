from __future__ import annotations


class AlarmApiError(Exception):
    """Base error for Alarm API connector failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        trace_id: str | None = None,
        retry_count: int = 0,
        details: object | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.trace_id = trace_id
        self.retry_count = retry_count
        self.details = details

    def to_dict(self) -> dict:
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "status_code": self.status_code,
            "trace_id": self.trace_id,
            "retry_count": self.retry_count,
            "details": self.details,
        }


class AlarmApiAuthError(AlarmApiError):
    """401/403 authentication or authorization failure."""


class AlarmApiNotFoundError(AlarmApiError):
    """404 resource not found."""


class AlarmApiValidationError(AlarmApiError):
    """400/422 validation failure."""


class AlarmApiTimeoutError(AlarmApiError):
    """Request timed out after retries."""
