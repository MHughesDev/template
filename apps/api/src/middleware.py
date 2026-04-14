# apps/api/src/middleware.py
"""
BLUEPRINT: apps/api/src/middleware.py

PURPOSE:
Shared middleware: CORS configuration, request logging with structured output,
correlation ID injection (X-Request-ID header), and the global exception handler
that translates AppError subclasses to structured JSON error responses.

DEPENDS ON:
- fastapi — Request, Response
- starlette.middleware.cors — CORSMiddleware
- starlette.middleware.base — BaseHTTPMiddleware
- uuid — UUID4 for correlation ID generation
- logging — structlog or stdlib for structured logging
- apps.api.src.exceptions — AppError (for global error handler)

DEPENDED ON BY:
- apps.api.src.main — registers all middleware and error handlers

CLASSES:

  CorrelationIdMiddleware(BaseHTTPMiddleware):
    PURPOSE: Injects a unique X-Request-ID header into every request and response.
    FIELDS:
      - header_name: str = "X-Request-ID"
    METHODS:
      - dispatch(request, call_next) -> Response
        1. Read X-Request-ID from request headers if present, else generate UUID4
        2. Store in request.state.correlation_id
        3. Call next middleware
        4. Set X-Request-ID in response headers
    NOTES: Correlation ID flows through all log records for that request

  RequestLoggingMiddleware(BaseHTTPMiddleware):
    PURPOSE: Log structured request/response data for observability.
    METHODS:
      - dispatch(request, call_next) -> Response
        1. Log request: method, path, correlation_id (not query params with secrets)
        2. Record start time
        3. Call next middleware
        4. Log response: status_code, duration_ms, correlation_id
        5. Log at WARNING level for 4xx, ERROR for 5xx, INFO for 2xx/3xx
    NOTES: Never log request bodies (may contain secrets/PII)

FUNCTIONS:

  configure_cors(app: FastAPI, allowed_origins: list[str]) -> None:
    PURPOSE: Add CORSMiddleware to the FastAPI app with security-appropriate defaults.
    STEPS:
      1. app.add_middleware(CORSMiddleware, ...)
      2. allow_origins = allowed_origins (from settings, never "*" in production)
      3. allow_credentials = True (for auth cookie support)
      4. allow_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
      5. allow_headers = ["*"] (or specific list for strict mode)

  global_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    PURPOSE: Translate AppError subclasses to structured JSON error responses.
    STEPS:
      1. Extract status_code from exc.status_code
      2. Build response body: {"error": {"code": exc.code, "message": exc.message}}
      3. Log the error with correlation_id and exc_info=True for 5xx errors
      4. Return JSONResponse(status_code=status_code, content=body)
    NOTES: Registered in main.py with app.add_exception_handler(AppError, handler)

DESIGN DECISIONS:
- Correlation ID: generated UUID4 if not provided; passed through if client sends X-Request-ID
- Never log bodies: request/response bodies may contain credentials or PII
- CORS: origins from settings (never hardcoded); wildcard not allowed in production
- Global error handler: translates domain errors to HTTP responses (keeps routers thin)
"""
