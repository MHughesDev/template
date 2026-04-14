# apps/api/src/dependencies.py
"""Shared FastAPI dependencies."""

from __future__ import annotations

from fastapi import Request

from apps.api.src.config import get_settings
from apps.api.src.database import get_db

__all__ = ["get_db", "get_settings", "get_correlation_id"]


def get_correlation_id(request: Request) -> str:
    """Return the correlation id for the active request."""

    return getattr(request.state, "correlation_id", "unknown")
