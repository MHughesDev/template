# apps/api/src/events.py
"""
BLUEPRINT: apps/api/src/events.py

PURPOSE:
Domain events and event bus foundation. Optional per spec §26.12 item 396.
Provides the base DomainEvent type, an in-process event bus for pub/sub
communication between bounded contexts, and event emission utilities.
Enable when bounded contexts need to communicate without direct imports.

DEPENDS ON:
- pydantic — BaseModel, ConfigDict (frozen=True for events)
- datetime — for event timestamps
- uuid — for event IDs
- asyncio — for async event handling
- typing — for generic event types

DEPENDED ON BY:
- apps.api.src.*/service.py — emit domain events
- (future): event handlers in subscriber modules

CLASSES:

  DomainEvent(BaseModel):
    PURPOSE: Base class for all domain events.
    FIELDS:
      - event_id: UUID — unique event identifier
      - event_type: str — type discriminator (e.g., "invoice.created")
      - occurred_at: datetime — when the event occurred (UTC)
      - aggregate_id: str — ID of the entity that caused the event
      - tenant_id: str | None = None — tenant context for multi-tenant deployments
    NOTES: model_config = ConfigDict(frozen=True) — events are immutable

  EventBus:
    PURPOSE: In-process event bus for synchronous or async event dispatch.
    METHODS:
      - subscribe(event_type: str, handler: Callable) -> None
        Register a handler for a specific event type.
      - publish(event: DomainEvent) -> None
        Publish an event to all registered handlers.
      - async_publish(event: DomainEvent) -> None
        Async version of publish for async handlers.
    NOTES: Simple in-process bus; replace with external broker for cross-service events

CONSTANTS:
  - event_bus: EventBus — module-level singleton for the in-process event bus

DESIGN DECISIONS:
- Optional module: only imported when bounded context communication is needed
- In-process bus: sufficient for monolith; swap for external broker when extracting services
- Events are immutable (frozen=True): domain events represent facts, never changed
- No persistence here: events are fire-and-forget in-process (add outbox for reliability)
"""
