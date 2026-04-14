# apps/api/src/config.py
"""Application settings loaded from environment (single source for env access)."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the API process."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", frozen=True
    )

    database_url: str = Field(
        default="sqlite+aiosqlite:///./dev.db",
        description="SQLAlchemy async database URL",
    )
    database_pool_size: int = Field(default=10, ge=1, le=100)

    jwt_secret_key: str = Field(
        default="change-me-in-production",
        min_length=8,
        description="Secret used to sign JWT access tokens",
    )
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = Field(default=30, ge=1, le=24 * 60)
    jwt_refresh_token_expire_days: int = Field(default=30, ge=1, le=365)

    api_host: str = "0.0.0.0"  # noqa: S104
    api_port: int = Field(default=8000, ge=1, le=65535)
    api_debug: bool = False
    api_cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )
    api_prefix: str = "/api/v1"
    project_name: str = "Template API"

    ai_enabled: bool = False
    chroma_host: str = "chroma"
    chroma_port: int = 8001

    broker_url: str | None = None

    log_level: str = "INFO"
    log_format: str = "text"

    multi_tenancy_enabled: bool = False
    rate_limiting_enabled: bool = False

    @field_validator("api_cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if not value:
            return []
        return [part.strip() for part in str(value).split(",") if part.strip()]

    @field_validator("jwt_secret_key")
    @classmethod
    def _reject_placeholder_secret(cls, value: str) -> str:
        if value in {"change-me", "changeme", "secret"}:
            msg = "JWT secret must be changed from the insecure placeholder value"
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def _debug_policy(self) -> Settings:
        if self.api_debug and not self.database_url.startswith("sqlite"):
            msg = "api_debug is only allowed for local sqlite development"
            raise ValueError(msg)
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings for FastAPI ``Depends``."""

    return Settings()
