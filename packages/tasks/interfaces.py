# packages/tasks/interfaces.py
"""
BLUEPRINT: packages/tasks/interfaces.py

PURPOSE:
Abstract Protocol interfaces for background task execution. Defines the contract
that all task implementations must satisfy. Workers are an optional profile —
the interfaces exist regardless; implementations are only loaded when the worker
profile is enabled. Per spec §26.9 item 240 and §12.3.

DEPENDS ON:
- typing — Protocol, runtime_checkable, Any
- dataclasses — TaskDefinition, TaskResult

DEPENDED ON BY:
- packages.tasks.__init__ — exports these interfaces
- (future worker implementations) — implement these protocols
- apps.api.src.*/service.py — call TaskInterface.submit() for background work

CLASSES:

  TaskDefinition:
    PURPOSE: Describes a background task to be submitted.
    FIELDS:
      - task_name: str — registered task handler name
      - args: tuple — positional arguments for the handler
      - kwargs: dict — keyword arguments for the handler
      - idempotency_key: str | None = None — for deduplication
      - priority: int = 0 — higher = higher priority (broker-specific)
    NOTES: dataclass with frozen=True (tasks are immutable after creation)

  TaskResult:
    PURPOSE: Result of a submitted or completed task.
    FIELDS:
      - task_id: str — unique task identifier assigned by the broker
      - status: Literal["pending", "running", "success", "failure", "cancelled"]
      - result: Any | None = None — task output (if completed successfully)
      - error: str | None = None — error message (if failed)
      - created_at: datetime
      - completed_at: datetime | None = None

  TaskInterface(Protocol):
    PURPOSE: Protocol for submitting tasks to a background queue.
    METHODS:
      - async submit(task: TaskDefinition) -> TaskResult — submit a task, return initial result
      - async get_status(task_id: str) -> TaskResult — check task status
      - async cancel(task_id: str) -> bool — cancel a pending task (returns True if cancelled)
    NOTES: @runtime_checkable; implementations must satisfy this protocol

  TaskHandler(Protocol):
    PURPOSE: Protocol for implementing a task handler (the function that executes the task).
    METHODS:
      - async handle(task: TaskDefinition) -> Any — execute the task, return result
    NOTES: Each task type implements this; registered with the worker by task_name

  InMemoryTaskInterface:
    PURPOSE: Simple in-process task execution for development/testing (no broker).
    IMPLEMENTS: TaskInterface
    METHODS:
      - async submit(task) — execute synchronously in a thread pool, return result
    NOTES: Not for production use; used when BROKER_URL is not set

DESIGN DECISIONS:
- Protocol (not ABC): structural typing; duck typing works without explicit inheritance
- InMemoryTaskInterface: allows code using TaskInterface to work without a broker in dev
- Idempotency key: enables safe retries; broker implementations deduplicate
- task_name (string): decoupled from Python import paths; broker-agnostic
"""
