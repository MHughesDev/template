# apps/api/alembic/env.py
"""
BLUEPRINT: apps/api/alembic/env.py

PURPOSE:
Alembic environment configuration. Supports both SQLite and PostgreSQL
connection strings via DATABASE_URL environment variable. Used by all
migration commands. Configures target_metadata from models for autogenerate.

DEPENDS ON:
- sqlalchemy (installed) — engine and session
- alembic (installed) — MigrationContext, Operations
- apps.api.src.database — Base (for target_metadata)
- apps.api.src.config — settings (for DATABASE_URL)
- All model modules must be imported here for autogenerate to detect them

DEPENDED ON BY:
- alembic upgrade head / downgrade / revision --autogenerate

FUNCTIONS:

  run_migrations_offline() -> None:
    PURPOSE: Run migrations in offline mode (SQL script output without DB connection).
    STEPS:
      1. Get URL from config
      2. Configure context with literal SQL output mode
      3. Run migrations
    USED BY: alembic upgrade head --sql

  run_migrations_online() -> None:
    PURPOSE: Run migrations with active DB connection.
    STEPS:
      1. Create engine from DATABASE_URL
      2. Connect and begin transaction
      3. Configure context with connection
      4. Run migrations
    USED BY: alembic upgrade head (default)

DESIGN DECISIONS:
- Both SQLite and Postgres supported via the same env.py
- target_metadata = Base.metadata (autogenerate reads all registered models)
- All model modules imported at top of file for autogenerate completeness
"""
