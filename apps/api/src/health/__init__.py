# apps/api/src/health/__init__.py
"""Health/readiness/liveness routes."""

from apps.api.src.health.router import router

__all__ = ["router"]
