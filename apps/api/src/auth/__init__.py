# apps/api/src/auth/__init__.py
"""Auth bounded context: JWT auth routes and ``get_current_user`` dependency."""

from apps.api.src.auth.dependencies import get_current_user
from apps.api.src.auth.router import router

__all__ = ["router", "get_current_user"]
