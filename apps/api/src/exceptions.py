# apps/api/src/exceptions.py
"""Domain error hierarchy for HTTP translation via middleware."""

from __future__ import annotations


class AppError(Exception):
    """Base error with stable ``code``, HTTP ``status_code``, and safe ``message``."""

    code: str = "APP_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.__class__.__doc__ or "An error occurred"
        super().__init__(self.message)


class NotFoundError(AppError):
    """Resource was not found."""

    code = "NOT_FOUND"
    status_code = 404


class AuthenticationError(AppError):
    """Authentication failed or token invalid."""

    code = "AUTH_INVALID_CREDENTIALS"
    status_code = 401


class AuthorizationError(AppError):
    """Authenticated caller is not allowed to perform this action."""

    code = "FORBIDDEN"
    status_code = 403


class ConflictError(AppError):
    """Request conflicts with current state."""

    code = "CONFLICT"
    status_code = 409


class ValidationError(AppError):
    """Domain validation failed (distinct from request schema validation)."""

    code = "VALIDATION_FAILED"
    status_code = 400


class ExternalServiceError(AppError):
    """Upstream dependency failed."""

    code = "EXTERNAL_SERVICE_ERROR"
    status_code = 503


class RateLimitError(AppError):
    """Rate limit exceeded."""

    code = "RATE_LIMIT_EXCEEDED"
    status_code = 429
