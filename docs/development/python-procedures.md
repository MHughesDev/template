# PYTHON_PROCEDURES.md

> **Referenced by:** `AGENTS.md` §10, `.cursor/rules/global.md`
>
> **Purpose:** This document defines the authoritative Python implementation procedures for every Python file in this repository. All agents writing Python code MUST follow these procedures. Composer agents read these procedures and implement accordingly. These are not suggestions — they are enforced by CI (mypy --strict, ruff, pytest, bandit).

---

## Table of Contents

1. [Boundary-First Design](#1-boundary-first-design)
2. [Typed Signatures](#2-typed-signatures)
3. [Shape Declaration and Serialization](#3-shape-declaration-and-serialization)
4. [Interface and Dependency Injection](#4-interface-and-dependency-injection)
5. [Validation at the Edge](#5-validation-at-the-edge)
6. [Domain Separation](#6-domain-separation)
7. [Import Direction and Module Structure](#7-import-direction-and-module-structure)
8. [Explicit State](#8-explicit-state)
9. [Error Policy](#9-error-policy)
10. [Configuration](#10-configuration)
11. [Async](#11-async)
12. [Nullability](#12-nullability)
13. [Immutability by Default](#13-immutability-by-default)
14. [Persistence](#14-persistence)
15. [Testing](#15-testing)
16. [Logging and Observability](#16-logging-and-observability)
17. [CI Enforcement](#17-ci-enforcement)
18. [Code Review](#18-code-review)
19. [Condensed 12-Point Rule Set](#19-condensed-12-point-rule-set)
20. [Refactor Triggers](#20-refactor-triggers)

---

## 1. Boundary-First Design

**Every public function must have a fully typed boundary.**

- Declare Pydantic models for request/response before writing logic
- Declare Enum types for all state machines before writing logic
- Declare `TypedDict` for JSON-like structures
- Never use `**kwargs` in public signatures
- Never use `dict[str, Any]` as a response type

## 2. Typed Signatures

**Every public function must be fully typed.**

```python
# ✅ Good
def calculate_total(items: list[LineItem], tax_rate: Decimal) -> Money:
    ...

# ❌ Bad
def calculate_total(items, tax_rate):
    ...
```

- Use `typing` module imports: `list`, `dict`, `Optional`, `Union`, `Callable`
- Return type must be explicit, never implied
- Use `Sequence` for read-only collections, `list` for mutable
- Use `Mapping` for read-only dicts, `dict` for mutable

## 3. Shape Declaration and Serialization

**Boundary shapes use Pydantic v2 models.**

```python
class PaymentRequest(BaseModel):
    amount: Money
    currency: CurrencyCode  # Enum, not str
    method: PaymentMethod   # Enum, not str
```

- Use constrained types: `Annotated[str, Field(max_length=100)]`
- Use custom validators for cross-field validation
- Never use `json.loads()` without a schema

## 4. Interface and Dependency Injection

**Depend on protocols, not concrete types.**

```python
class PaymentGateway(Protocol):
    async def charge(self, amount: Money) -> Transaction: ...

# Depends on protocol, not StripeGateway
async def process_payment(gateway: PaymentGateway, ...) -> ...
```

- Declare protocols in `interfaces.py` or at module top
- Inject via constructor or function parameter
- No global state access in business logic

## 5. Validation at the Edge

**Validate at the outermost boundary.**

- HTTP layer: FastAPI + Pydantic validates requests
- Service layer: Business rules validate domain invariants
- Repository layer: Database constraints validate persistence
- Never validate in the middle of business logic

## 6. Domain Separation

**Keep domain logic pure.**

- Domain models have no dependencies on infrastructure
- Domain services orchestrate, not implement
- Use anti-corruption layers for external integrations
- Never import `requests`, `boto3`, etc. in domain modules

## 7. Import Direction and Module Structure

**Import direction flows inward:**

```
api/routes/ → services/ → domain/ → repositories/
```

- Outer layers import inner layers, never reverse
- Domain never imports infrastructure
- Services never import HTTP
- Use dependency injection to break circular imports

## 8. Explicit State

**Model state as explicit enums with transition maps.**

```python
class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

VALID_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.REFUNDED},
    ...
}
```

- Never use string constants for state
- Transition validation is explicit, not ad-hoc
- State machines are documented and tested

## 9. Error Policy

**Use exceptions for exceptional cases, not control flow.**

- Define custom exception hierarchies per domain
- Use `Result` types for expected failures (validation, not-found)
- Never catch `Exception` bare
- Never use `None` as an error signal

```python
# ✅ Good
class PaymentError(Exception): ...
class InsufficientFundsError(PaymentError): ...

# ❌ Bad
def charge() -> None:  # None means error? success?
    ...
```

## 10. Configuration

**Single source of truth for config.**

- Use `pydantic-settings` for environment variables
- One `Settings` class per app
- Never use `os.getenv()` outside config module
- Validate config at startup, not runtime

```python
# app/core/config.py
class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    JWT_SECRET: str = Field(min_length=32)
    
    model_config = SettingsConfigDict(env_file=".env")
```

## 11. Async

**Async all the way or sync all the way.**

- FastAPI routes: async
- Database: asyncpg or sync SQLAlchemy, never mix
- External HTTP: `httpx.AsyncClient`
- CPU-bound: thread pool or process pool, never block event loop

## 12. Nullability

**Handle `None` explicitly.**

- Use `Optional[T]` or `T | None` (Python 3.10+)
- Never return `None` implicitly
- Use `assert x is not None` or `if x is None: raise` pattern
- Prefer `raise NotFoundError()` over returning `None`

## 13. Immutability by Default

**Prefer immutable data structures.**

- Use frozen Pydantic models where possible
- Use `dataclass(frozen=True)` for value objects
- Never mutate collections while iterating
- Return new instances, modify in place only when necessary

## 14. Persistence

**Repository pattern for data access.**

- One repository per aggregate root
- Repository returns domain models, not ORM objects
- Queries live in repository, not in services
- Unit of work pattern for transactions

```python
class OrderRepository:
    async def get(self, id: OrderId) -> Order: ...
    async def save(self, order: Order) -> None: ...
    async def list_by_customer(self, customer_id: CustomerId) -> list[Order]: ...
```

## 15. Testing

**Test behavior, not implementation.**

- Unit tests: fast, no I/O, use fakes
- Integration tests: real DB, cleanup after
- E2E tests: full stack, critical paths only
- Use `pytest` fixtures for dependency injection

```python
# ✅ Good - test behavior
def test_order_shipment_triggers_notification():
    notifier = FakeNotifier()
    service = OrderService(notifier=notifier)
    service.ship(order)
    assert notifier.was_notified(order.customer_id)

# ❌ Bad - test implementation
def test_order_shipment_calls_db():
    ...
```

## 16. Logging and Observability

**Structured logging, not print statements.**

- Use `structlog` for structured JSON logging
- Include correlation IDs in all logs
- Never log secrets or PII
- Use appropriate levels: DEBUG for dev, INFO for prod, ERROR for alerts

## 17. CI Enforcement

**CI blocks merge on violations.**

| Tool | Purpose | Strictness |
|------|---------|------------|
| ruff | Linting | All checks pass |
| ruff format | Formatting | No diffs allowed |
| mypy | Type checking | `--strict` mode |
| pytest | Tests | 100% pass rate |
| bandit | Security scan | No HIGH/CRITICAL |
| pip-audit | Dependency CVEs | No HIGH/CRITICAL in direct deps |

## 18. Code Review

**Reviewers check procedure compliance.**

- [ ] All public functions typed
- [ ] Pydantic models for boundaries
- [ ] No `os.getenv()` outside config
- [ ] No `dict[str, Any]` as return type
- [ ] Tests cover behavior, not mocks
- [ ] Error handling uses exceptions, not `None`
- [ ] State modeled with Enum + transition map
- [ ] No string constants for state

## 19. Condensed 12-Point Rule Set

For quick reference during coding:

1. **Boundary-first**: Pydantic models before logic
2. **Fully typed**: Every public function
3. **Protocols**: Depend on interfaces, not concrete
4. **Validate edge**: HTTP/service/repository layers
5. **Pure domain**: No infra imports in business logic
6. **Import direction**: Routes → Services → Domain → Repos
7. **Explicit state**: Enum + transition map
8. **Exceptions**: For errors, not control flow
9. **Single config**: One Settings, no `os.getenv()` scattered
10. **Async consistency**: All async or all sync
11. **Handle None**: Explicitly, never implicit
12. **Test behavior**: Not implementation details

## 20. Refactor Triggers

When to refactor:

- **Type coverage drops below 100%** → Add types
- **Function has 3+ boolean parameters** → Use Pydantic model
- **Service imports HTTP client** → Add gateway interface
- **String constants for state** → Convert to Enum
- `**kwargs` in public API → Explicit parameters
- `dict[str, Any]` anywhere → Pydantic model
- `os.getenv()` outside config → Centralize in Settings
- `None` returns for errors → Custom exceptions

---

**Questions?** See `[AGENTS.md](../../AGENTS.md)` §10 or ask in PR review.
