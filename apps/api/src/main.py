# apps/api/src/main.py
"""FastAPI application factory and ASGI entrypoint."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request

from apps.api.src.auth.router import router as auth_router
from apps.api.src.config import Settings, get_settings
from apps.api.src.database import dispose_engine
from apps.api.src.example.router import router as example_router
from apps.api.src.exceptions import AppError
from apps.api.src.health.router import router as health_router
from apps.api.src.logging_config import configure_logging
from apps.api.src.middleware import (
    CorrelationIdMiddleware,
    RequestLoggingMiddleware,
    app_error_handler,
    configure_cors,
)
from apps.api.src.tenancy.middleware import (
    TenantContextMiddleware,
    TenantEnforcementMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup/shutdown hooks."""

    settings = get_settings()
    configure_logging(settings)
    yield
    await dispose_engine()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a configured FastAPI application."""

    resolved = settings or get_settings()
    app = FastAPI(
        title=resolved.project_name,
        version="0.1.0",
        description="Agent-operated API — see spec/spec.md for full specification.",
        lifespan=lifespan,
        docs_url="/docs" if resolved.api_debug else None,
        redoc_url="/redoc" if resolved.api_debug else None,
        openapi_url="/openapi.json",
    )

    # Starlette runs last-registered middleware first. Put CORS outermost.
    app.add_middleware(TenantEnforcementMiddleware)
    app.add_middleware(TenantContextMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)
    configure_cors(app, resolved.api_cors_origins)

    async def _app_error_bridge(request: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, AppError):
            return await app_error_handler(request, exc)
        raise exc

    app.add_exception_handler(AppError, _app_error_bridge)

    app.include_router(health_router)
    app.include_router(auth_router, prefix=resolved.api_prefix)
    app.include_router(example_router, prefix=resolved.api_prefix)

    return app


app = create_app()
