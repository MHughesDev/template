# apps/api/AGENTS.md

Scoped instructions for **`apps/api/`**. Root **[AGENTS.md](../../AGENTS.md)** is supreme — this file only narrows scope for the FastAPI app.

## Module layout

Each bounded context under **`apps/api/src/<context>/`** should include:

| File | Role |
|------|------|
| `__init__.py` | Export `router` and key public types |
| `router.py` | HTTP endpoints only — no business rules |
| `models.py` | SQLAlchemy models |
| `schemas.py` | Pydantic request/response models |
| `service.py` | Domain logic and orchestration |
| `dependencies.py` | `Depends()` factories (optional per module) |

Contexts today: **`health/`**, **`auth/`**, **`tenancy/`**.

## Routers

Register routers in **`main.py`** under **`api_prefix`** (default `/api/v1`). Health checks stay **without** that prefix.

## Dependencies

| Need | Use |
|------|-----|
| DB session | `Depends(get_db)` from **`dependencies.py`** |
| Settings | `Depends(get_settings)` |
| Current user | `Depends(get_current_user)` from **`auth/dependencies.py`** |

Do not construct services inline in handlers.

## Tests

- Location: **`apps/api/tests/`**
- Client: **`httpx.AsyncClient`** with ASGI transport
- Naming: `test_<unit>_<scenario>_<outcome>`

## Imports

**`router → service → repository`** only. Shared types live in **`packages/contracts/`**.
