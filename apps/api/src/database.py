# apps/api/src/database.py
"""
BLUEPRINT: apps/api/src/database.py

PURPOSE:
Database connection and session management. Creates the async SQLAlchemy engine
from DATABASE_URL, provides the session factory, the request-scoped session
dependency for FastAPI, and the Base declarative class for all models.
Supports both SQLite (aiosqlite) and PostgreSQL (asyncpg).

DEPENDS ON:
- sqlalchemy.ext.asyncio — create_async_engine, AsyncSession, async_sessionmaker
- sqlalchemy.orm — declarative_base
- apps.api.src.config — get_settings() for DATABASE_URL

DEPENDED ON BY:
- apps.api.src.main — engine.dispose() in lifespan
- apps.api.src.dependencies — get_db() uses AsyncSession
- apps.api.src.auth.models — User, RefreshToken inherit Base
- apps.api.src.tenancy.models — Tenant inherits Base
- apps.api.src.*/models.py — all domain models inherit Base
- alembic env.py — target_metadata = Base.metadata

CLASSES:

  Base (DeclarativeBase):
    PURPOSE: Base class for all SQLAlchemy models. Provides metadata for Alembic autogenerate.
    NOTES: All model classes in models.py files must inherit from this Base.

CONSTANTS:
  - engine: AsyncEngine — module-level engine created from DATABASE_URL at import time
  - AsyncSessionLocal: async_sessionmaker — session factory configured with engine

FUNCTIONS:

  get_db() -> AsyncGenerator[AsyncSession, None]:
    PURPOSE: FastAPI dependency that provides a request-scoped async DB session.
    STEPS:
      1. Create AsyncSession from AsyncSessionLocal
      2. yield session (used within the request lifecycle)
      3. Close session after request (finally block)
    RETURNS: AsyncSession (via generator)
    RAISES: Propagates any SQLAlchemy errors from query execution
    NOTES: Used as `Depends(get_db)` in route handlers

DESIGN DECISIONS:
- Async engine: required for non-blocking DB operations in async FastAPI handlers
- SQLite connect_args={"check_same_thread": False}: required for SQLite in async context
- PostgreSQL: no special connect_args needed, asyncpg is async-native
- Session closed in finally: ensures cleanup even on exceptions
- engine at module level: created once, reused across all requests
"""
