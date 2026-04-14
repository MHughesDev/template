# apps/api/src/exceptions.py
"""Domain error hierarchy for HTTP translation via middleware."""

from __future__ import annotations

import logging

logger = logging.getLogger("api")


class AppError(Exception):
    """Base error with stable ``code``, HTTP ``status_code``, and safe ``message``."""

    code: str = "APP_ERROR"
    status_code: int = 500
    detail: dict[str, object] | None = None

    def __init__(
        self,
        message: str | None = None,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        self.message = message or self.__class__.__doc__ or "An error occurred"
        self.detail = detail
        super().__init__(self.message)

    def to_dict(self) -> dict[str, object]:
        """Serialize for API responses and logs."""

        out: dict[str, object] = {
            "code": self.code,
            "message": self.message,
            "detail": self.detail,
        }
        return out


class NotFoundError(AppError):
    """Resource was not found."""

    code = "NOT_FOUND"
    status_code = 404

    def __init__(self, entity: str, identifier: str) -> None:
        self.entity = entity
        self.identifier = identifier
        msg = f"{entity} '{identifier}' not found"
        super().__init__(
            msg,
            detail={"entity": entity, "identifier": identifier},
        )


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

    def __init__(
        self,
        service_name: str,
        message: str | None = None,
        original_error: Exception | None = None,
    ) -> None:
        self.service_name = service_name
        self.original_error = original_error
        detail: dict[str, object] = {"service_name": service_name}
        if original_error is not None:
            detail["original_error"] = repr(original_error)
        super().__init__(
            message or f"External service {service_name} failed",
            detail=detail,
        )


class RateLimitError(AppError):
    """Rate limit exceeded."""

    code = "RATE_LIMIT_EXCEEDED"
    status_code = 429

    def __init__(self, retry_after: int = 60) -> None:
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit exceeded; retry after {retry_after} seconds",
            detail={"retry_after": retry_after},
        )


class TenantIsolationError(AppError):
    """Tenant boundary violated — wrong or missing tenant context.

    Should be logged at WARNING when raised (enforced by middleware / handlers).
    """

    code = "TENANT_ISOLATION_VIOLATION"
    status_code = 403

    def __init__(
        self,
        message: str | None = None,
        *,
        tenant_id: str | None = None,
        attempted_resource: str | None = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.attempted_resource = attempted_resource
        detail: dict[str, object] = {}
        if tenant_id is not None:
            detail["tenant_id"] = tenant_id
        if attempted_resource is not None:
            detail["attempted_resource"] = attempted_resource
        super().__init__(
            message or "Tenant isolation violation",
            detail=detail or None,
        )
        logger.warning(
            "tenant_isolation",
            extra={"tenant_id": tenant_id, "attempted_resource": attempted_resource},
        )


class StateTransitionError(AppError):
    """Invalid state machine transition."""

    code = "STATE_TRANSITION_INVALID"
    status_code = 409

    def __init__(
        self,
        current_state: str,
        attempted_state: str,
        allowed_states: set[str],
    ) -> None:
        self.current_state = current_state
        self.attempted_state = attempted_state
        self.allowed_states = allowed_states
        allowed = ", ".join(sorted(allowed_states))
        msg = (
            f"Cannot transition from {current_state!r} to {attempted_state!r}; "
            f"allowed: {allowed}"
        )
        super().__init__(
            msg,
            detail={
                "current_state": current_state,
                "attempted_state": attempted_state,
                "allowed_states": sorted(allowed_states),
            },
        )
