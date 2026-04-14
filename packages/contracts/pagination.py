# packages/contracts/pagination.py
"""
BLUEPRINT: packages/contracts/pagination.py

PURPOSE:
Shared pagination models and cursor utilities for the contract layer.
Provides PaginationParams, cursor encoding/decoding, and the PagedResponse
type used across all list endpoints. Per spec §26.12 item 398.

DEPENDS ON:
- pydantic — BaseModel, Field
- base64 — cursor encoding
- json — cursor payload serialization

DEPENDED ON BY:
- packages.contracts.models — imports PagedResponse from here
- apps.api.src.*/router.py — use PaginationParams via Depends
- packages.contracts.__init__ — exports PaginationParams

CLASSES:

  PaginationParams(BaseModel):
    PURPOSE: Query parameters for paginated list endpoints. Used with Depends().
    FIELDS:
      - page: int = Field(1, ge=1, description="Page number (1-indexed)")
      - page_size: int = Field(20, ge=1, le=100, description="Items per page (max 100)")
      - cursor: str | None = Field(None, description="Cursor for cursor-based pagination")
    NOTES: Used as Depends() in route handlers; validated at boundary

FUNCTIONS:

  encode_cursor(payload: dict) -> str:
    PURPOSE: Encode a pagination cursor payload as a URL-safe base64 string.
    STEPS:
      1. json.dumps(payload, sort_keys=True, default=str)
      2. base64.urlsafe_b64encode(json_bytes)
      3. Return decoded string (URL-safe)
    RETURNS: str — cursor token

  decode_cursor(cursor: str) -> dict | None:
    PURPOSE: Decode a cursor token back to a payload dict.
    STEPS:
      1. base64.urlsafe_b64decode(cursor + "==")  (padding)
      2. json.loads(decoded_bytes)
    RETURNS: dict or None if invalid/malformed
    RAISES: Does not raise — returns None for invalid cursors (caller handles gracefully)

  calculate_offset(params: PaginationParams) -> int:
    PURPOSE: Convert page/page_size to SQL OFFSET value.
    RETURNS: (params.page - 1) * params.page_size

DESIGN DECISIONS:
- URL-safe base64: cursors are URL-safe without additional encoding
- Default None on invalid cursor: graceful degradation to first page (not error)
- Both offset and cursor-based: endpoints choose which mode to use
- max page_size=100: prevents excessive data loads on any endpoint
"""
