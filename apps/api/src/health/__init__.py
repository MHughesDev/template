# apps/api/src/health/__init__.py
"""
BLUEPRINT: apps/api/src/health/__init__.py

PURPOSE:
Package marker for the health module. Exports the router for registration in main.py.
Per spec §26.8 item 217.
"""
from apps.api.src.health.router import router

__all__ = ["router"]
