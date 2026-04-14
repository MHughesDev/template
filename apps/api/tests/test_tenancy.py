# apps/api/tests/test_tenancy.py
"""Tenancy middleware and model tests."""

from __future__ import annotations

import os
import uuid
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient
from jose import jwt
from starlette.requests import Request

from apps.api.src.config import get_settings
from apps.api.src.database import Base
from apps.api.src.main import create_app
from apps.api.src.tenancy.middleware import TenantContextMiddleware
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.src.tenancy.models import Tenant, TenantMixin


def test_tenant_mixin_adds_tenant_id_column() -> None:
    """``TenantMixin`` adds a ``tenant_id`` column to the model table."""

    class _Model(Base, TenantMixin):
        __tablename__ = "test_tenant_mixin_probe"
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    assert "tenant_id" in _Model.__table__.columns


@pytest.mark.asyncio
async def test_tenant_middleware_sets_request_state() -> None:
    """JWT with ``tenant_id`` sets ``request.state.tenant_id``."""

    tid = str(uuid.uuid4())
    token = jwt.encode(
        {"sub": str(uuid.uuid4()), "tenant_id": tid},
        "test-jwt-secret-key-for-ci-only",
        algorithm="HS256",
    )
    from starlette.responses import Response as StarletteResponse

    middleware = TenantContextMiddleware(app=lambda r: StarletteResponse())

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "raw_path": b"/",
        "headers": [
            (b"authorization", f"Bearer {token}".encode()),
        ],
        "client": ("127.0.0.1", 12345),
        "server": ("test", 80),
        "scheme": "http",
    }
    request = Request(scope)

    with patch.dict(
        os.environ,
        {
            "MULTI_TENANCY_ENABLED": "true",
            "JWT_SECRET_KEY": "test-jwt-secret-key-for-ci-only",
        },
        clear=False,
    ):
        get_settings.cache_clear()
        received: Request | None = None

        async def inner(req: Request):  # noqa: ANN202
            nonlocal received
            received = req
            return StarletteResponse("ok")

        await middleware.dispatch(request, inner)
        get_settings.cache_clear()

    assert received is not None
    assert received.state.tenant_id == uuid.UUID(tid)


@pytest.mark.asyncio
async def test_tenant_middleware_missing_tenant_returns_403() -> None:
    """With multi-tenancy enabled, Bearer token without ``tenant_id`` returns 403."""

    token = jwt.encode(
        {"sub": str(uuid.uuid4())},
        "test-jwt-secret-key-for-ci-only",
        algorithm="HS256",
    )
    prev = os.environ.get("MULTI_TENANCY_ENABLED")
    os.environ["MULTI_TENANCY_ENABLED"] = "true"
    get_settings.cache_clear()
    try:
        app = create_app(get_settings())
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(
                "/health",
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 403
        body = response.json()
        assert body["error"]["code"] == "TENANT_ISOLATION_VIOLATION"
    finally:
        if prev is None:
            os.environ.pop("MULTI_TENANCY_ENABLED", None)
        else:
            os.environ["MULTI_TENANCY_ENABLED"] = prev
        get_settings.cache_clear()


def test_tenant_model_has_required_fields() -> None:
    """``Tenant`` exposes id, name, is_active, created_at."""

    cols = {c.name for c in Tenant.__table__.columns}
    assert {"id", "name", "is_active", "created_at"}.issubset(cols)


@pytest.mark.skip(reason="Scoped query helper not yet implemented on TenantMixin")
def test_tenant_mixin_query_scoping() -> None:
    """Placeholder: when TenantMixin provides scoped queries, assert tenant filter."""
