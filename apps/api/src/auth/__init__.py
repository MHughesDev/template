# apps/api/src/auth/__init__.py
"""
BLUEPRINT: apps/api/src/auth/__init__.py

PURPOSE:
Package marker for the auth module. Exports the router and key dependency
functions for use in other modules. Per spec §26.8 item 219.
"""
from apps.api.src.auth.router import router
from apps.api.src.auth.dependencies import get_current_user

__all__ = ["router", "get_current_user"]
