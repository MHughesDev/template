# apps/api/tests/test_mcp_mount.py
"""Tests for MCP server mount and custom tool route."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.api.src.config import get_settings
from apps.api.src.main import create_app


@pytest.mark.asyncio
async def test_mcp_health_check_route_returns_ok() -> None:
    app = create_app(get_settings())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/mcp-tools/health_check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "template-api"}


@pytest.mark.asyncio
async def test_mcp_mount_path_registered() -> None:
    app = create_app(get_settings())
    paths = {getattr(r, "path", None) for r in app.routes}
    assert "/mcp" in paths or any(
        p is not None and str(p).startswith("/mcp") for p in paths
    )
