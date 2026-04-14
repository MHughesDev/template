# packages/contracts/models.py
"""
BLUEPRINT: packages/contracts/models.py

PURPOSE:
Shared Pydantic models used across bounded contexts and by external API clients.
The contract layer for the modular monolith — backward compatibility is mandatory.
Per spec §26.9 item 237.

DEPENDS ON:
- pydantic — BaseModel, ConfigDict
- datetime — for timestamp fields
- uuid — for ID fields

DEPENDED ON BY:
- apps.api.src.*/schemas.py — bounded context schemas may extend these
- packages.contracts.errors — ErrorResponse uses ErrorDetail
- packages.contracts.pagination — PagedResponse uses these base models

CLASSES:

  BaseSchema(BaseModel):
    PURPOSE: Base Pydantic schema with common configuration for all contract models.
    CONFIG: from_attributes=True (ORM interop), populate_by_name=True

  TimestampMixin(BaseModel):
    PURPOSE: Mixin adding created_at and updated_at to any schema.
    FIELDS:
      - created_at: datetime — resource creation timestamp
      - updated_at: datetime | None = None — resource last update timestamp

  IdentifiedMixin(BaseModel):
    PURPOSE: Mixin adding id field (UUID) to any schema.
    FIELDS:
      - id: UUID — resource identifier

  ErrorDetail(BaseSchema):
    PURPOSE: Structured error detail for API error responses.
    FIELDS:
      - code: str — stable error code string
      - message: str — human-readable error description
      - field: str | None = None — field name for validation errors
      - detail: dict | None = None — additional context (never includes secrets)
    CONFIG: frozen=True

  ErrorResponse(BaseSchema):
    PURPOSE: Standard API error response envelope.
    FIELDS:
      - error: ErrorDetail
    CONFIG: frozen=True
    NOTES: All API errors use this shape: {"error": {"code": ..., "message": ...}}

  PagedResponse(BaseSchema, Generic[T]):
    PURPOSE: Standard list response envelope for paginated collections.
    FIELDS:
      - items: list[T] — the page of items
      - total: int — total count of matching items
      - page: int — current page number
      - page_size: int — items per page
      - next_cursor: str | None = None — cursor for next page

DESIGN DECISIONS:
- Backward compatibility: never remove or rename fields; add new fields as optional
- ErrorResponse is a shared contract: all API error responses use this shape
- Generic PagedResponse: type-safe across all list endpoints
- frozen=True on error schemas: errors are immutable facts
- from_attributes=True: allows validation from SQLAlchemy model instances
"""
