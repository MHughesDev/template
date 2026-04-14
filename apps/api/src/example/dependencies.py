# apps/api/src/example/dependencies.py
"""FastAPI dependencies for the example module."""

from __future__ import annotations

from fastapi import Depends, Query
from packages.contracts.pagination import PaginationParams
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.config import Settings, get_settings
from apps.api.src.database import get_db
from apps.api.src.example.repository import ExampleRepository
from apps.api.src.example.service import ExampleService


def get_example_service(
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ExampleService:
    """Construct ``ExampleService`` with repository and settings."""

    return ExampleService(repo=ExampleRepository(session), settings=settings)


def get_pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    cursor: str | None = Query(None),
    offset: int | None = Query(None, ge=0),
) -> PaginationParams:
    """Parse pagination query parameters into ``PaginationParams``."""

    return PaginationParams(
        page=page,
        page_size=page_size,
        cursor=cursor,
        offset=offset,
    )
