# apps/api/src/auth/dependencies.py
"""FastAPI dependencies for authentication."""

from __future__ import annotations

from uuid import UUID

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.auth import models
from apps.api.src.auth.service import AuthService
from apps.api.src.config import Settings, get_settings
from apps.api.src.dependencies import get_db
from apps.api.src.exceptions import AppError, AuthenticationError, AuthorizationError

http_bearer = HTTPBearer(auto_error=False)


def get_auth_service(
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    """Construct AuthService with injected session and settings."""

    return AuthService(session=session, settings=settings)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_db),
) -> models.User:
    """Return the authenticated user from a Bearer access token."""

    if credentials is None:
        raise AuthenticationError("Not authenticated")

    claims = service.verify_access_token(credentials.credentials)
    user_id_raw = claims.get("sub")
    if user_id_raw is None:
        raise AuthenticationError("Invalid token claims")

    try:
        user_id = UUID(str(user_id_raw))
    except ValueError as exc:
        raise AuthenticationError("Invalid token subject") from exc

    user = await session.get(models.User, user_id)
    if user is None or not user.is_active:
        raise AuthenticationError("User not found or inactive")

    request.state.user_id = user.id
    return user


async def require_tenant(
    request: Request,
    current_user: models.User = Depends(get_current_user),
) -> tuple[models.User, UUID]:
    """Require a tenant context on the request (JWT claim or explicit header)."""

    tenant_id: UUID | None = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise AuthorizationError("Tenant context required")
    return current_user, tenant_id


def app_error_to_http(exc: AppError) -> HTTPException:
    """Translate domain errors to FastAPI HTTPException."""

    return HTTPException(
        status_code=exc.status_code, detail={"code": exc.code, "message": exc.message}
    )
