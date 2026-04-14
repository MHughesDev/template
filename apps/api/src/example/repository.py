# apps/api/src/example/repository.py
"""Persistence for ``Example`` rows."""

from __future__ import annotations

import uuid
from typing import Any, cast

from packages.contracts.pagination import PaginationParams
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Column

from apps.api.src.example.models import Example
from apps.api.src.pagination import paginate_query


class ExampleRepository:
    """Example table access."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, example_id: uuid.UUID) -> Example | None:
        return await self._session.get(Example, example_id)

    async def list_all(self, params: PaginationParams) -> tuple[list[Example], int]:
        """Rows (limit page_size+1 for has_next) and total count."""

        count_stmt = select(func.count()).select_from(Example)
        total = int((await self._session.execute(count_stmt)).scalar_one())
        base = select(Example).order_by(Example.id)
        id_col = cast(Column[Any], Example.__table__.c.id)
        stmt = paginate_query(base, params, id_col)
        result = await self._session.execute(stmt)
        rows: list[Any] = list(result.scalars().all())
        return rows, total

    async def create(self, example: Example) -> Example:
        self._session.add(example)
        await self._session.commit()
        await self._session.refresh(example)
        return example

    async def update(self, example: Example) -> Example:
        await self._session.commit()
        await self._session.refresh(example)
        return example

    async def delete(self, example_id: uuid.UUID) -> bool:
        row = await self.get_by_id(example_id)
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.commit()
        return True
