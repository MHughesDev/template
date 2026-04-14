# apps/api/tests/conftest.py
"""Pytest fixtures for API tests."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from apps.api.src.config import get_settings
from apps.api.src.database import Base, dispose_engine, get_db
from apps.api.src.main import create_app


@pytest_asyncio.fixture
async def test_engine() -> AsyncIterator[AsyncEngine]:
    """In-memory SQLite database shared across a test."""

    await dispose_engine()
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key-for-ci-only"
    os.environ["API_DEBUG"] = "true"
    get_settings.cache_clear()

    engine = create_async_engine(os.environ["DATABASE_URL"], future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()
    await dispose_engine()
    get_settings.cache_clear()


@pytest_asyncio.fixture
async def app(test_engine: AsyncEngine):
    """ASGI app with database session override."""

    session_factory = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    application = create_app(get_settings())

    async def _override_db() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    application.dependency_overrides[get_db] = _override_db
    yield application
    application.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    """HTTP client for API tests."""

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
