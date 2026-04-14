# apps/api/src/middleware.py
"""CORS, correlation IDs, request logging, and AppError translation."""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any, cast

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from apps.api.src.exceptions import AppError

logger = logging.getLogger("api")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Ensure every request/response has ``X-Request-ID``."""

    header_name = "X-Request-ID"

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        incoming = request.headers.get(self.header_name)
        correlation_id = incoming or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = cast(Response, await call_next(request))
        response.headers[self.header_name] = correlation_id
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Structured request/response logging without bodies."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        start = time.perf_counter()
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        logger.info(
            "request_started",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
            },
        )
        response = cast(Response, await call_next(request))
        duration_ms = int((time.perf_counter() - start) * 1000)
        log_method = logger.info
        if response.status_code >= 500:
            log_method = logger.error
        elif response.status_code >= 400:
            log_method = logger.warning
        log_method(
            "request_finished",
            extra={
                "correlation_id": correlation_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response


def configure_cors(app: FastAPI, allowed_origins: list[str]) -> None:
    """Attach CORS middleware with safe defaults."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Serialize ``AppError`` subclasses to JSON."""

    correlation_id = getattr(request.state, "correlation_id", "unknown")
    if exc.status_code >= 500:
        logger.error(
            "app_error",
            extra={"correlation_id": correlation_id, "code": exc.code},
            exc_info=True,
        )
    body = {"error": {"code": exc.code, "message": exc.message}}
    return JSONResponse(status_code=exc.status_code, content=body)
