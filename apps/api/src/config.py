# apps/api/src/config.py
"""
BLUEPRINT: apps/api/src/config.py

PURPOSE:
Single Pydantic BaseSettings class for all application configuration. Reads from
environment variables only. Validates on startup. The ONLY place os.getenv() is
allowed in this codebase. Per PYTHON_PROCEDURES.md §10 and spec §26.8 item 214.

DEPENDS ON:
- pydantic-settings — BaseSettings, Field
- pydantic — field_validator
- functools — lru_cache for get_settings()

DEPENDED ON BY:
- apps.api.src.main — imports settings for app configuration
- apps.api.src.database — imports settings for DATABASE_URL
- apps.api.src.dependencies — provides get_settings() as Depends()
- apps.api.src.auth.service — imports settings for JWT config
- All tests that need config override

CLASSES:

  Settings(BaseSettings):
    PURPOSE: All application configuration loaded from environment variables.
    FIELDS (grouped by section):

      Database:
      - database_url: str = "sqlite+aiosqlite:///./dev.db" — database connection string
      - database_pool_size: int = 10 — connection pool size (PostgreSQL only)

      Auth/JWT:
      - jwt_secret_key: str — JWT signing secret (no default, required)
      - jwt_algorithm: str = "HS256" — signing algorithm
      - jwt_access_token_expire_minutes: int = 30 — access token expiry
      - jwt_refresh_token_expire_days: int = 30 — refresh token expiry

      API:
      - api_host: str = "0.0.0.0" — server bind host
      - api_port: int = 8000 — server bind port
      - api_debug: bool = False — debug mode (never True in production)
      - api_cors_origins: list[str] = ["http://localhost:3000"] — allowed CORS origins
      - api_prefix: str = "/api/v1" — API route prefix
      - project_name: str = "{{PROJECT_NAME}}" — project display name

      Optional: AI/RAG:
      - ai_enabled: bool = False — kill switch for AI features
      - chroma_host: str = "chroma" — ChromaDB host
      - chroma_port: int = 8001 — ChromaDB port

      Optional: Workers:
      - broker_url: str | None = None — task broker URL

      Observability:
      - log_level: str = "INFO" — log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
      - log_format: str = "text" — log format (text | json)

      Feature flags:
      - multi_tenancy_enabled: bool = False — enable tenant middleware enforcement
      - rate_limiting_enabled: bool = False — enable rate limiting middleware

    VALIDATORS:
      - field_validator("api_cors_origins", mode="before") — parse comma-separated string → list
      - field_validator("jwt_secret_key") — ensure not empty or default value
      - field_validator("database_url") — validate URL format
      - model_validator(mode="after") — cross-field: api_debug must be False if not sqlite

    NOTES: model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", frozen=True)

FUNCTIONS:

  get_settings() -> Settings:
    PURPOSE: Cached settings factory for use with FastAPI Depends().
    STEPS: lru_cache-wrapped Settings() instantiation.
    RETURNS: Settings singleton instance
    NOTES: @lru_cache() ensures settings are loaded once at startup

DESIGN DECISIONS:
- frozen=True: configuration never changes at runtime
- @lru_cache() on get_settings(): single instantiation across application lifetime
- env_file=".env": supports loading from .env in development without code change
- No fallback for jwt_secret_key: absence of a secret key = deployment error, fail fast
"""
