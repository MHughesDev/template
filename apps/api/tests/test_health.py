# apps/api/tests/test_health.py
"""Tests for health endpoints."""

from __future__ import annotations

from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from apps.api.src.database import get_db


@pytest.mark.asyncio
async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_ready_reports_database_ok(client: AsyncClient) -> None:
    response = await client.get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["checks"]["database"] == "ok"


@pytest.mark.asyncio
async def test_ready_returns_503_when_database_unreachable(
    app, client: AsyncClient
) -> None:
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(side_effect=RuntimeError("simulated db failure"))

    async def _mock_db() -> AsyncIterator[AsyncMock]:
        yield mock_session

    app.dependency_overrides[get_db] = _mock_db
    try:
        response = await client.get("/ready")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert "database" in body["checks"]


@pytest.mark.asyncio
async def test_live_returns_alive(client: AsyncClient) -> None:
    response = await client.get("/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


@pytest.mark.asyncio
async def test_health_does_not_require_auth(client: AsyncClient) -> None:
    response = await client.get("/health", headers={})
    assert response.status_code == 200
