# docs/architecture/error-handling.md

<!-- Optional per spec §26.12 item 400 -->

**Purpose:** Cross-cutting error handling strategy. Per spec §26.12 item 400.

## Error Hierarchy

AppError hierarchy from apps/api/src/exceptions.py. Base class structure, HTTP status mappings, stable error codes.

## Error Response Shape

Standard JSON error envelope: {"error": {"code": "...", "message": "..."}}. Never expose stack traces externally.

## Error Propagation

Service raises AppError subclass → global exception handler in middleware.py translates → structured JSON response. Layer responsibilities: repositories translate SQLAlchemy errors at the adapter boundary.

## Client Handling Guide

How API clients should handle each error category: 401 (re-auth), 429 (backoff), 503 (retry with backoff), 422 (fix request).
