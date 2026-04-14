# packages/contracts/errors.py
"""
BLUEPRINT: packages/contracts/errors.py

PURPOSE:
Shared error response models and error code enumeration. Provides the
ErrorCode enum that defines stable, versioned error codes shared across
the API and client contracts. Per spec §26.12 item 397.

DEPENDS ON:
- enum — Enum for ErrorCode
- pydantic — BaseModel for error shapes

DEPENDED ON BY:
- packages.contracts.models — ErrorDetail uses ErrorCode
- apps.api.src.exceptions — exception classes reference error codes
- docs/api/error-codes.md — generated from this file by error-code-registry.py

CLASSES:

  ErrorCode(str, Enum):
    PURPOSE: Stable, versioned enumeration of all API error codes.
    VALUES:
      # Auth errors
      - AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
      - AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
      - AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
      # Authorization errors
      - FORBIDDEN = "FORBIDDEN"
      # Not found
      - NOT_FOUND = "NOT_FOUND"
      # Validation
      - VALIDATION_FAILED = "VALIDATION_FAILED"
      # Conflict
      - CONFLICT = "CONFLICT"
      # Rate limiting
      - RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
      # External service
      - EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
      # Internal
      - INTERNAL_ERROR = "INTERNAL_ERROR"
    NOTES: Error codes are STABLE across API versions. Never remove or rename.

DESIGN DECISIONS:
- str Enum: serializes to string in JSON responses (not "ErrorCode.AUTH_INVALID_CREDENTIALS")
- Centralized: single source of truth for all error codes
- Lives in packages/contracts/: shared between API and any generated clients
- Never remove existing codes: clients may depend on them
"""
