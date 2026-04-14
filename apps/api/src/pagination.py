# apps/api/src/pagination.py
"""SQLAlchemy query pagination; contract types in ``packages.contracts``."""

from __future__ import annotations

import base64
from collections.abc import Callable
from typing import Any, TypeVar

from packages.contracts.pagination import (
    PageInfo,
    PaginatedResponse,
    PaginationParams,
    calculate_offset,
)
from packages.contracts.pagination import (
    decode_cursor as decode_cursor_payload,
)
from packages.contracts.pagination import (
    encode_cursor as encode_cursor_payload,
)
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.schema import Column

from apps.api.src.exceptions import ValidationError

T = TypeVar("T")


def encode_cursor(value: Any) -> str:
    """Base64url-encode the string representation of the value."""

    raw = str(value).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def decode_cursor(cursor: str) -> str:
    """Base64url-decode to string. Raise ``ValidationError`` on invalid input."""

    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        return base64.urlsafe_b64decode(padded.encode()).decode()
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValidationError("Invalid cursor token") from exc


def paginate_query(
    query: Select[Any],
    params: PaginationParams,
    cursor_column: Column[Any],
) -> Select[Any]:
    """Apply cursor-based or offset-based pagination to a SQLAlchemy ``Select``.

    Uses ``limit + 1`` to detect ``has_next`` without a separate COUNT query.
    """

    limit = params.page_size + 1
    if params.cursor:
        decoded = decode_cursor(params.cursor)
        return query.where(cursor_column > decoded).limit(limit)
    if params.offset is not None:
        return query.offset(params.offset).limit(limit)
    off = calculate_offset(params)
    return query.offset(off).limit(limit)


async def paginated_response(
    query: Select[Any],
    params: PaginationParams,
    session: AsyncSession,
    cursor_column: Column[Any],
    *,
    get_row_cursor_value: Callable[[Any], Any] | None = None,
) -> PaginatedResponse[Any]:
    """Execute the paginated query and build ``PaginatedResponse``."""

    stmt = paginate_query(query, params, cursor_column)
    result = await session.execute(stmt)
    rows = list(result.scalars().all())
    has_next = len(rows) > params.page_size
    items = rows[: params.page_size]
    next_cursor: str | None = None
    if has_next and items:
        last = items[-1]
        if get_row_cursor_value is not None:
            raw = get_row_cursor_value(last)
        else:
            key = getattr(cursor_column, "key", None) or str(cursor_column.name)
            raw = getattr(last, key, None)
        if raw is not None:
            next_cursor = encode_cursor(raw)
    page_info = PageInfo(
        has_next=has_next,
        has_previous=params.offset is not None
        and params.offset > 0
        or params.page > 1
        or bool(params.cursor),
        next_cursor=next_cursor,
    )
    return PaginatedResponse(items=items, page_info=page_info)


__all__ = [
    "PageInfo",
    "PaginatedResponse",
    "PaginationParams",
    "calculate_offset",
    "decode_cursor",
    "decode_cursor_payload",
    "encode_cursor",
    "encode_cursor_payload",
    "paginate_query",
    "paginated_response",
]
