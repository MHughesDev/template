# apps/api/src/pagination.py
"""
BLUEPRINT: apps/api/src/pagination.py

PURPOSE:
Pagination utilities and shared list response models. Provides cursor-based
and offset-based pagination support, standard list response schema, and
pagination parameter dependencies for FastAPI routes.
Per spec §26.12 item 371.

DEPENDS ON:
- pydantic — BaseModel, ConfigDict
- fastapi — Query (for pagination params as Depends)
- typing — Generic, TypeVar

DEPENDED ON BY:
- apps.api.src.*/router.py — uses PaginationParams and PagedResponse
- packages.contracts.pagination — may import shared models from here

CLASSES:

  PaginationParams:
    PURPOSE: Query parameters for paginated list endpoints.
    FIELDS:
      - page: int = Query(1, ge=1) — page number (1-indexed, offset-based)
      - page_size: int = Query(20, ge=1, le=100) — items per page
      - cursor: str | None = Query(None) — cursor token (cursor-based alternative)
    NOTES: Injected via Depends(get_pagination) in route handlers

  PagedResponse(BaseModel, Generic[T]):
    PURPOSE: Standard list response envelope wrapping any list of items.
    FIELDS:
      - items: list[T] — the page of items
      - total: int — total count of matching items
      - page: int — current page number (offset-based)
      - page_size: int — items per page
      - next_cursor: str | None = None — cursor for next page (cursor-based)
      - has_next: bool — True if more pages exist

FUNCTIONS:

  get_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
  ) -> PaginationParams:
    PURPOSE: FastAPI dependency for pagination query parameters.
    STEPS: Validate and return PaginationParams instance.
    RETURNS: PaginationParams

  calculate_offset(params: PaginationParams) -> int:
    PURPOSE: Convert page/page_size to SQL OFFSET value.
    RETURNS: int — (page - 1) * page_size

DESIGN DECISIONS:
- Support both offset-based (page/page_size) and cursor-based (cursor) pagination
- PagedResponse is Generic[T] for type-safe usage across modules
- page_size max 100: prevents excessive data loads
- next_cursor is optional: absent for offset-based, present for cursor-based
"""
