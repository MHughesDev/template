# apps/api/src/events.py
"""Lightweight in-process domain event primitives (optional)."""

from __future__ import annotations

import asyncio
import uuid
from collections import defaultdict
from collections.abc import Awaitable, Callable, Coroutine
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DomainEvent(BaseModel):
    """Immutable domain event envelope."""

    model_config = ConfigDict(frozen=True)

    event_id: uuid.UUID
    event_type: str
    occurred_at: datetime
    aggregate_id: str
    tenant_id: str | None = None


Handler = Callable[[DomainEvent], Coroutine[Any, Any, None] | Awaitable[None]]


class EventBus:
    """Simple async in-process pub/sub bus."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Handler) -> None:
        """Register ``handler`` for ``event_type``."""

        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        """Dispatch ``event`` to subscribers."""

        handlers = list(self._handlers.get(event.event_type, []))
        await asyncio.gather(*(self._call(handler, event) for handler in handlers))

    async def _call(self, handler: Handler, event: DomainEvent) -> None:
        result = handler(event)
        if asyncio.iscoroutine(result):
            await result


event_bus = EventBus()


def emit_domain_event(
    event_type: str,
    aggregate_id: str,
    *,
    tenant_id: str | None = None,
) -> DomainEvent:
    """Build a timestamped event (callers may publish via ``event_bus``)."""

    return DomainEvent(
        event_id=uuid.uuid4(),
        event_type=event_type,
        occurred_at=datetime.now(UTC),
        aggregate_id=aggregate_id,
        tenant_id=tenant_id,
    )
