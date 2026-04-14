# apps/api/src/context.py
"""Request-scoped context aggregate for dependency injection."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RequestContext:
    """Aggregates request-scoped state into a single injectable dependency."""

    correlation_id: str
    user_id: UUID | None = None
    tenant_id: UUID | None = None
    is_authenticated: bool = False
