# packages/contracts/__init__.py
"""
BLUEPRINT: packages/contracts/__init__.py

PURPOSE:
Package marker. Exports shared Pydantic models, error responses, and pagination
utilities used across bounded contexts. The contract layer for the modular monolith.
Per spec §26.9 item 236.
"""
from packages.contracts.models import ErrorResponse, PagedResponse
from packages.contracts.errors import ErrorCode
from packages.contracts.pagination import PaginationParams

__all__ = ["ErrorResponse", "PagedResponse", "ErrorCode", "PaginationParams"]
