class AlarmApiError(Exception):
    """Base exception for Alarm API errors."""
    
    def __init__(self, message, status_code=None, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class AlarmApiAuthError(AlarmApiError):
    """Authentication or authorization error (401/403)."""
    pass


class AlarmApiNotFoundError(AlarmApiError):
    """Resource not found error (404)."""
    pass


class AlarmApiValidationError(AlarmApiError):
    """Request validation error (400/422)."""
    pass


class AlarmApiTimeoutError(AlarmApiError):
    """Request timeout error."""
    pass
