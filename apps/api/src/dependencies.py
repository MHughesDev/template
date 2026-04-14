# apps/api/src/dependencies.py
"""Central FastAPI dependencies — routers should import from here."""

from __future__ import annotations

import uuid
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from apps.api.src.auth.dependencies import get_current_user, require_auth
from apps.api.src.config import Settings, get_settings
from apps.api.src.context import RequestContext
from apps.api.src.database import get_db

__all__ = [
    "get_app_settings",
    "get_correlation_id",
    "get_current_user",
    "get_db",
    "get_db_session",
    "get_request_context",
    "get_settings",
    "require_auth",
]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Re-export ``get_db`` for explicit naming in routers."""

    async for session in get_db():
        yield session


def get_app_settings() -> Settings:
    """Thin wrapper for ``Depends()`` consistency."""

    return get_settings()


def get_correlation_id(request: Request) -> str:
    """Correlation ID from middleware, or a new UUID string if missing."""

    cid = getattr(request.state, "correlation_id", None)
    if isinstance(cid, str) and cid:
        return cid
    return str(uuid.uuid4())


def get_request_context(request: Request) -> RequestContext:
    """Aggregate request-scoped identifiers for injection."""

    user_id = getattr(request.state, "user_id", None)
    tenant_id = getattr(request.state, "tenant_id", None)
    return RequestContext(
        correlation_id=get_correlation_id(request),
        user_id=user_id,
        tenant_id=tenant_id,
        is_authenticated=user_id is not None,
    )
