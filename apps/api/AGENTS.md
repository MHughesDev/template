# apps/api/AGENTS.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Overrides: AGENTS.md (root) for API-specific concerns (never contradicts root) -->
<!-- - Rules: .cursor/rules/apps-api.md -->

> PURPOSE: Scoped agent instructions for the API application. Narrows scope to API concerns; never contradicts root AGENTS.md. Per spec §26.8 item 206.

## API Scope

> CONTENT: This AGENTS.md file narrows the agent's scope to apps/api/ concerns. It does not grant additional authority beyond the root AGENTS.md — it only narrows. For all repo-wide policy: read AGENTS.md (root) first.

## Module Structure

> CONTENT: The canonical module layout under apps/api/src/<context>/:
> - `__init__.py` — exports router and key types
> - `router.py` — FastAPI router with endpoints (thin — no business logic)
> - `models.py` — SQLAlchemy models inheriting Base
> - `schemas.py` — Pydantic request/response models (frozen=True for inputs)
> - `service.py` — business logic (no DB queries, no HTTP concerns)
> - `dependencies.py` — FastAPI Depends() factories
>
> Current modules: health/, auth/, tenancy/

## Router Registration Pattern

> CONTENT: All routers registered in apps/api/src/main.py via `app.include_router()`. New routers: add import and registration in alphabetical order. Prefix: `/api/v1`. Router prefix must NOT duplicate the main.py prefix.

## Dependency Injection Patterns

> CONTENT: Required dependencies:
> - DB session: `Depends(get_db)` from apps/api/src/dependencies.py
> - Current user: `Depends(get_current_user)` from apps/api/src/auth/dependencies.py
> - Settings: `Depends(get_settings)` from apps/api/src/dependencies.py
> Never instantiate services directly in route handlers.

## Testing Requirements

> CONTENT:
> - Every new endpoint: at minimum one happy-path test and one auth failure test
> - Every new service function: unit tests with mocked dependencies
> - Tests live in apps/api/tests/ (not co-located with source)
> - Use httpx.AsyncClient for API tests (not TestClient)
> - All tests follow: `test_<unit>_<scenario>_<expected>` naming convention

## Import Conventions

> CONTENT: Import direction strictly enforced: router → service → repository. Circular imports are structural errors — fix the structure. Shared types go in packages/contracts/.
