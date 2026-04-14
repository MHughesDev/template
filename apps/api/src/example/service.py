# apps/api/src/example/service.py
"""Application service for the example teaching module."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from packages.contracts.pagination import PageInfo, PaginatedResponse, PaginationParams

from apps.api.src.example.models import Example
from apps.api.src.example.repository import ExampleRepository
from apps.api.src.example.schemas import ExampleCreate, ExampleResponse, ExampleUpdate
from apps.api.src.exceptions import NotFoundError


class ExampleService:
    """Coordinates example CRUD."""

    def __init__(self, repo: ExampleRepository) -> None:
        self._repo = repo

    async def get(self, example_id: uuid.UUID) -> Example:
        row = await self._repo.get_by_id(example_id)
        if row is None:
            raise NotFoundError("Example", str(example_id))
        return row

    async def list(
        self, params: PaginationParams
    ) -> PaginatedResponse[ExampleResponse]:
        rows, _total = await self._repo.list_all(params)
        has_next = len(rows) > params.page_size
        page_rows = rows[: params.page_size]
        items = [ExampleResponse.model_validate(r) for r in page_rows]
        page_info = PageInfo(
            has_next=has_next,
            has_previous=params.page > 1 or (params.offset or 0) > 0,
            next_cursor=None,
            previous_cursor=None,
            total_count=None,
        )
        return PaginatedResponse(items=items, page_info=page_info)

    async def create(self, data: ExampleCreate) -> Example:
        now = datetime.now(UTC)
        row = Example(
            title=data.title,
            description=data.description,
            status="draft",
            tenant_id=None,
            created_at=now,
            updated_at=now,
        )
        return await self._repo.create(row)

    async def update(self, example_id: uuid.UUID, data: ExampleUpdate) -> Example:
        row = await self._repo.get_by_id(example_id)
        if row is None:
            raise NotFoundError("Example", str(example_id))
        if data.title is not None:
            row.title = data.title
        if data.description is not None:
            row.description = data.description
        if data.status is not None:
            row.status = data.status
        row.updated_at = datetime.now(UTC)
        return await self._repo.update(row)

    async def delete(self, example_id: uuid.UUID) -> None:
        ok = await self._repo.delete(example_id)
        if not ok:
            raise NotFoundError("Example", str(example_id))
