# apps/api/src/dependencies.py
"""
BLUEPRINT: apps/api/src/dependencies.py

PURPOSE:
Shared FastAPI dependencies used across multiple modules. Provides get_db
(database session), get_settings (application configuration), and request
context utilities (correlation ID access). Per spec §26.12 item 370.

DEPENDS ON:
- sqlalchemy.ext.asyncio — AsyncSession
- apps.api.src.database — get_db generator
- apps.api.src.config — get_settings

DEPENDED ON BY:
- apps.api.src.auth.router — imports get_db, get_settings
- apps.api.src.health.router — imports get_db
- apps.api.src.*/router.py — all routers import shared deps from here

FUNCTIONS:

  get_db() -> AsyncGenerator[AsyncSession, None]:
    PURPOSE: Re-export database session dependency.
    NOTES: Defined in database.py; re-exported here for single import point.

  get_settings() -> Settings:
    PURPOSE: Re-export settings dependency.
    NOTES: Defined in config.py; re-exported here for single import point.

  get_correlation_id(request: Request) -> str:
    PURPOSE: Extract correlation ID from request state.
    STEPS:
      1. Return request.state.correlation_id (set by CorrelationIdMiddleware)
      2. Fallback: return "unknown" if not set (should not happen after middleware)
    RETURNS: str — correlation ID for the current request

DESIGN DECISIONS:
- Single import point: routes import all deps from here, not scattered imports
- get_db and get_settings are re-exported for convenience but defined in their modules
- correlation_id from request.state (not header) to prevent injection attacks
"""
