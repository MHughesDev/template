# apps/api/src/tenancy/middleware.py
"""Populate ``request.state.tenant_id`` from validated JWT claims when enabled."""

from __future__ import annotations

from typing import Any, cast
from uuid import UUID

from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from apps.api.src.config import get_settings
from apps.api.src.exceptions import TenantIsolationError


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Attach ``tenant_id`` to request state for downstream dependencies."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        settings = get_settings()
        request.state.tenant_id = None
        if not settings.multi_tenancy_enabled:
            return cast(Response, await call_next(request))

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            return cast(Response, await call_next(request))

        token = auth_header.split(" ", 1)[1].strip()
        try:
            claims = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            return cast(Response, await call_next(request))

        tenant_raw = claims.get("tenant_id")
        if tenant_raw:
            try:
                request.state.tenant_id = UUID(str(tenant_raw))
            except ValueError:
                request.state.tenant_id = None
        return cast(Response, await call_next(request))


class TenantEnforcementMiddleware(BaseHTTPMiddleware):
    """Require JWT ``tenant_id`` when multi-tenancy is on and Bearer is sent."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        settings = get_settings()
        if not settings.multi_tenancy_enabled:
            return cast(Response, await call_next(request))

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            return cast(Response, await call_next(request))

        if getattr(request.state, "tenant_id", None) is None:
            exc = TenantIsolationError(
                "Tenant context required when multi-tenancy is enabled",
                tenant_id=None,
                attempted_resource=request.url.path,
            )
            from apps.api.src.middleware import app_error_handler

            return await app_error_handler(request, exc)

        return cast(Response, await call_next(request))
