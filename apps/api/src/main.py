# apps/api/src/main.py
"""
BLUEPRINT: apps/api/src/main.py

PURPOSE:
FastAPI application entry point. Creates the app instance, registers all routers,
configures middleware (CORS, tenant context, logging, correlation ID), sets up
lifespan events (startup/shutdown database connections), and registers global
error handlers.

DEPENDS ON:
- fastapi — FastAPI, Lifespan, middleware utilities
- contextlib — asynccontextmanager for lifespan
- apps.api.src.config — settings
- apps.api.src.middleware — CORSMiddleware setup, CorrelationIdMiddleware, logging
- apps.api.src.database — database engine initialization
- apps.api.src.exceptions — AppError subclasses for error handlers
- apps.api.src.health — health router
- apps.api.src.auth — auth router
- apps.api.src.tenancy.middleware — TenantContextMiddleware

DEPENDED ON BY:
- uvicorn (CLI entrypoint): `uvicorn apps.api.src.main:app`
- alembic env.py: imports for target_metadata
- test conftest.py: `from apps.api.src.main import app`

FUNCTIONS:

  lifespan(app: FastAPI) -> AsyncContextManager:
    PURPOSE: Manage application startup and shutdown lifecycle.
    STEPS:
      1. On startup: initialize database connection pool, log startup
      2. On shutdown: dispose database connections, log shutdown
    NOTES: Used as `@asynccontextmanager` yielding at startup/shutdown boundary

  create_app() -> FastAPI:
    PURPOSE: Create and configure the FastAPI application instance.
    STEPS:
      1. Create FastAPI(title=settings.project_name, lifespan=lifespan)
      2. Add CORSMiddleware with origins from settings.api_cors_origins
      3. Add CorrelationIdMiddleware (inject X-Request-ID header)
      4. Add RequestLoggingMiddleware (structured request/response logs)
      5. Add TenantContextMiddleware (extract tenant from JWT)
      6. Register global exception handler for AppError → structured JSON response
      7. Include routers (alphabetical):
         - health_router (prefix="/api/v1") or no prefix for /, /health
         - auth_router (prefix="/api/v1/auth")
         - (future contexts registered here)
      8. Return configured app
    RETURNS: FastAPI instance

CONSTANTS:
  - app: FastAPI = create_app() — module-level app instance used by uvicorn

DESIGN DECISIONS:
- create_app() factory pattern enables test isolation (create fresh app per test)
- Middleware order matters: correlation ID first (needed by logging), then logging, then tenant
- Global error handler translates AppError subclasses → consistent JSON shape
- Lifespan over deprecated startup/shutdown events (FastAPI 0.93+ pattern)
"""
