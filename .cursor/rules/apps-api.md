---
globs:
  - "apps/api/**"
description: Path-scoped rules for apps/api/. Enforces FastAPI patterns, service/repository boundaries, import conventions, and test co-location.
---

# .cursor/rules/apps-api.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: apps/api/AGENTS.md, PYTHON_PROCEDURES.md §6 (Domain Separation) -->
<!-- - Enforced by: scripts/audit-self.sh, mypy --strict -->

> PURPOSE: Path-scoped rules for the apps/api/ directory. Enforces FastAPI module patterns, service/repository layer boundaries, dependency injection, Pydantic model location, error response shape, and test file naming. Per spec §26.2 item 12.

## Section: Module Structure Rules

> CONTENT: Rules for the canonical module layout under apps/api/src/<context>/. Rules:
> 1. Every bounded context MUST have: `__init__.py`, `router.py`, `models.py`, `schemas.py`, `service.py`
> 2. `__init__.py` exports the router and key public types
> 3. `dependencies.py` is optional but required when the module has non-trivial FastAPI dependencies
> 4. `repository.py` is optional but MUST be separate from `service.py` if persistence logic is complex
> 5. All module directories MUST have a corresponding `tests/test_<module>.py`
> 6. No module may exceed 5 files in its directory without a documented rationale

## Section: Router Registration Pattern

> CONTENT: Rules for how routers are registered. Rules:
> 1. Router is defined in `router.py` as `router = APIRouter(prefix="/<context>", tags=["<Context>"])`
> 2. Router MUST be imported and registered in `apps/api/src/main.py` via `app.include_router(router, prefix="/api/v1")`
> 3. Router prefix and main.py registration prefix MUST NOT duplicate the path segment
> 4. Every router MUST have an `__init__.py` that exports `router` as the module's public interface
> 5. New routers are registered in main.py in alphabetical order by module name

## Section: Dependency Injection Rules

> CONTENT: Rules for FastAPI Depends() usage. Rules:
> 1. Services are NEVER instantiated directly in route handlers — always via `Depends()`
> 2. Database sessions are injected via `Depends(get_db)` from `apps/api/src/dependencies.py`
> 3. Current user is injected via `Depends(get_current_user)` from `apps/api/src/auth/dependencies.py`
> 4. Settings are injected via `Depends(get_settings)` — never `from config import settings` directly in routers
> 5. Factory functions for Depends() live in the module's `dependencies.py` or in the shared `apps/api/src/dependencies.py`

## Section: Pydantic Model Location

> CONTENT: Rules for where Pydantic models live. Rules:
> 1. Request and response schemas for a module live in `<module>/schemas.py` — not in `router.py` or `service.py`
> 2. Schemas shared across multiple modules live in `packages/contracts/models.py`
> 3. SQLAlchemy models live in `<module>/models.py` — never mixed with Pydantic schemas
> 4. Response schemas are prefixed `<Entity>Response`; request schemas are `<Entity>Request` or `Create<Entity>Request`
> 5. Never return SQLAlchemy models directly from endpoints — always convert to Pydantic response schema

## Section: Error Response Shape

> CONTENT: Rules for consistent API error responses. Rules:
> 1. All error responses use the standard shape: `{"error": {"code": "ERROR_CODE", "message": "...", "detail": ...}}`
> 2. Error codes are defined in `apps/api/src/exceptions.py` as string constants (e.g., `AUTH_INVALID_CREDENTIALS`)
> 3. Services raise `AppError` subclasses from `exceptions.py` — never `HTTPException` directly
> 4. The global exception handler in `middleware.py` translates `AppError` to HTTP responses
> 5. HTTP status codes map to error categories: 400=validation, 401=auth, 403=forbidden, 404=not-found, 409=conflict, 422=schema-error, 500=internal

## Section: Test File Naming

> CONTENT: Rules for test file organization. Rules:
> 1. API module tests live in `apps/api/tests/test_<module>.py` (not co-located with source)
> 2. Test function names follow: `test_<endpoint_or_function>_<scenario>_<expected_outcome>`
> 3. Fixtures shared across test files live in `apps/api/tests/conftest.py`
> 4. Test factories live in `apps/api/tests/factories.py`
> 5. Integration tests (requiring real DB) are marked with `@pytest.mark.integration`
> 6. Every public endpoint MUST have at least one happy-path test and one error-path test
