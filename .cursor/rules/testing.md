---
globs:
  - "**/tests/**"
  - "**/test_*"
  - "**/*_test.py"
description: Testing standards. Coverage expectations, naming conventions, fixture patterns, mock boundaries.
---

# .cursor/rules/testing.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: PYTHON_PROCEDURES.md §15 (Testing) -->
<!-- - Skills: skills/testing/pytest-conventions.md, skills/testing/async-testing.md -->
<!-- - Coverage: docs/quality/coverage-policy.md -->

> PURPOSE: Testing standards and conventions. Covers naming, fixtures, scope, markers, mock boundaries, async patterns, and coverage requirements. Recommended per spec §26.2 item 15.

## Section: Test Naming Convention

> CONTENT: Rules for test function and file names. Rules:
> 1. Test function naming: `test_<unit_under_test>_<scenario>_<expected_outcome>`
>    - Good: `test_login_invalid_password_returns_401`
>    - Bad: `test_login`, `test_auth`, `test1`
> 2. Test file naming: `test_<module>.py` for unit tests, `test_<module>_integration.py` for integration tests
> 3. Test class naming (when used): `Test<Component>` (no `_` separator)
> 4. Parametrized test IDs: use descriptive strings in `pytest.mark.parametrize` ids, not numbers

## Section: Fixture Scope Rules

> CONTENT: Rules for pytest fixture scopes. Rules:
> 1. Default fixture scope is `function` — each test gets a fresh fixture
> 2. `session` scope: only for expensive, truly read-only resources (e.g., a compiled regex)
> 3. `module` scope: rarely used; only when test isolation within a module is verified
> 4. Database fixtures: use `function` scope with transaction rollback to ensure test isolation
> 5. NEVER share mutable state between tests via `session` or `module` scope fixtures
> 6. Shared fixtures live in `apps/api/tests/conftest.py`; module-local fixtures in the test file

## Section: Mock Boundary Policy

> CONTENT: Rules for what to mock vs what to test against real implementations. Rules:
> 1. Unit tests: mock all external dependencies (database, HTTP clients, file system, time)
> 2. Integration tests: use real database (SQLite in CI via `database_url` fixture), real sessions
> 3. API tests: mock external HTTP services only; use real application + real DB
> 4. NEVER mock the unit under test — if you need to mock it, you're testing the wrong thing
> 5. Prefer dependency injection and Protocol interfaces over `monkeypatch.setattr` for mocking
> 6. When you must use `monkeypatch`, patch at the import boundary (where the thing is used), not where it's defined

## Section: Async Test Patterns

> CONTENT: Rules for testing async FastAPI code. Rules:
> 1. Use `pytest-asyncio` with `asyncio_mode = "auto"` in `pyproject.toml`
> 2. Async test functions: `async def test_...()` — no `@pytest.mark.asyncio` needed with auto mode
> 3. Test client: `httpx.AsyncClient(app=app, base_url="http://test")` — not `TestClient`
> 4. Database sessions in tests: use `AsyncSession` from the test `db_session` fixture
> 5. Avoid `asyncio.run()` in tests — let pytest-asyncio manage the event loop
> 6. For testing background tasks: use `anyio.from_thread.run_sync` or mock the task submission

## Section: Coverage Requirements

> CONTENT: Rules for test coverage. Rules:
> 1. Coverage floor is defined in `docs/quality/coverage-policy.md` — never decrease it
> 2. Run `make test` to execute tests with coverage; CI fails if coverage drops below the floor
> 3. Coverage ratcheting: use `scripts/coverage-ratchet.py` to auto-update floor when coverage improves
> 4. Excluded from coverage: `alembic/`, `__init__.py`, and `if TYPE_CHECKING:` blocks
> 5. New modules MUST have ≥80% coverage on their first PR (exceptions require documented rationale)

## Section: Test Markers

> CONTENT: Rules for pytest markers. Rules:
> 1. `@pytest.mark.unit` — pure unit tests with no external dependencies (fast, <100ms)
> 2. `@pytest.mark.integration` — tests requiring real DB or other services (slower, require setup)
> 3. `@pytest.mark.smoke` — critical path tests run after deployment
> 4. `@pytest.mark.slow` — tests taking >5 seconds (excluded from default run with `-m "not slow"`)
> 5. Markers MUST be registered in `pyproject.toml` `[tool.pytest.ini_options]` markers list
