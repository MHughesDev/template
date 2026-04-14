# apps/api/src/exceptions.py
"""
BLUEPRINT: apps/api/src/exceptions.py

PURPOSE:
Custom exception hierarchy for the API. All domain exceptions inherit from AppError
which carries code (stable string), status_code (HTTP), and message (human-readable).
Services raise AppError subclasses; the global error handler in middleware.py
translates them to HTTP responses. Per spec §26.12 item 343 and PYTHON_PROCEDURES.md §9.

DEPENDS ON:
- (no imports — pure Python exception hierarchy)

DEPENDED ON BY:
- apps.api.src.middleware — global_exception_handler catches AppError
- apps.api.src.auth.service — raises AuthenticationError, ConflictError
- apps.api.src.health.router — raises ExternalServiceError (for DB check)
- apps.api.src.*/service.py — all services raise appropriate subclasses
- skills/backend/error-code-registry.py — scans this file for code definitions

CLASSES:

  AppError(Exception):
    PURPOSE: Base class for all domain exceptions. Carries stable error code, HTTP status, and message.
    FIELDS:
      - code: str — stable string error code (e.g., "AUTH_INVALID_CREDENTIALS")
      - status_code: int — HTTP status code for this error
      - message: str — human-readable message (safe for API clients)
    METHODS:
      - __init__(self, message: str | None = None) — uses class defaults if message not provided
    NOTES: Never raise AppError directly — always raise a specific subclass

  NotFoundError(AppError):
    PURPOSE: Resource not found (404). Client can safely retry with different ID.
    FIELDS:
      - code: str = "NOT_FOUND"
      - status_code: int = 404

  AuthenticationError(AppError):
    PURPOSE: Authentication failed — invalid credentials, expired token, no token (401).
    FIELDS:
      - code: str = "AUTH_INVALID_CREDENTIALS"
      - status_code: int = 401

  AuthorizationError(AppError):
    PURPOSE: Authenticated but not authorized for this resource (403).
    FIELDS:
      - code: str = "FORBIDDEN"
      - status_code: int = 403

  ConflictError(AppError):
    PURPOSE: Resource conflict — duplicate creation, optimistic lock failure (409).
    FIELDS:
      - code: str = "CONFLICT"
      - status_code: int = 409

  ValidationError(AppError):
    PURPOSE: Domain validation failure (400) — distinct from Pydantic schema validation (422).
    FIELDS:
      - code: str = "VALIDATION_FAILED"
      - status_code: int = 400

  ExternalServiceError(AppError):
    PURPOSE: External dependency (DB, broker, third-party API) is unavailable or errored (503).
    FIELDS:
      - code: str = "EXTERNAL_SERVICE_ERROR"
      - status_code: int = 503

  RateLimitError(AppError):
    PURPOSE: Rate limit exceeded (429).
    FIELDS:
      - code: str = "RATE_LIMIT_EXCEEDED"
      - status_code: int = 429

DESIGN DECISIONS:
- code strings are STABLE across API versions (clients depend on them)
- status_code is a class attribute with default; callers may override per-instance
- message is safe for external exposure (never includes internal details or stack traces)
- message can be overridden at raise time: raise NotFoundError("Invoice Q-001 not found")
- No ImportError from this module: no external dependencies
"""
