# docs/development/local-setup.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/development/README.md, README.md -->

**Purpose:** Detailed local development setup. All Make/Task targets documented with expected behavior (§10.1).

## Overview

Detailed local development setup. All Make/Task targets documented with expected behavior (§10.1). See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

## Environment

1. **Python:** 3.12+ (`python --version`).
2. **Virtual env:** One-shot bootstrap: `./setup.sh` (creates `.venv`, installs from `requirements.lock` when present then `pip install -e . --no-deps`, else `pip install -e ".[dev]"`, copies `.env` from `.env.example`, runs `make migrate`, lint, fmt, typecheck, test).
3. **Environment file:** Copy `cp .env.example .env` and set `JWT_SECRET_KEY` to a strong value before any shared or production use. All settings are read through `apps/api/src/config.py` only.

## Running the API

- **Development server:** `make dev` (reloads on change; binds per `API_HOST` / `API_PORT` in `.env`).
- **Health checks:** `make health-check` (or `make health:check`) — exercises `/health`, `/ready`, `/live`.

## Canonical Make targets

Run `make help` for the full list. Common targets:

| Target | Role |
|--------|------|
| `make lint` | Ruff lint |
| `make fmt` | Apply Ruff formatting |
| `make fmt-check` / `make fmt:check` | Ruff format verify (CI mode) |
| `make fmt-fix` / `make fmt:fix` | Alias for `make fmt` |
| `make typecheck` | mypy strict |
| `make test` | Pytest with coverage |
| `make test-unit` / `make test:unit` | Unit tests only |
| `make migrate` | Alembic upgrade to head |
| `make ci-migrate-dry-run` | Same SQLite migration checks as CI (`migrate-dry-run` job) — run before pushing migrations |
| `make migrate:create MESSAGE="..."` / `make migrate:create` | New revision (MESSAGE required) |
| `make docker-up` / `make docker:up` | `docker compose up -d` |
| `make docker-down` / `make docker:down` | `docker compose down` |
| `make skills-list` / `make skills:list` | List skills by category |
| `make queue-peek` / `make queue:peek` | Read queue header + first row |
| `make queue-validate` / `make queue:validate` | Validate `queue/queue.csv` |
| `make audit-self` / `make audit:self` | Repo self-audit |
| `make docs-check` / `make docs:check` | Documentation link check |
| `make docs-generate` / `make docs:generate` | Regenerate generated docs |
| `make idea-validate` / `make idea:validate` | Validate `idea.md` placeholders |
| `make security-scan` / `make security:scan` | Bandit + pip-audit |
| `make secret-scan` / `make secret:scan` | Heuristic secret-pattern scan |
| `make env-sync` / `make env:sync` | Compare `.env.example` with `Settings` fields |
| `make test-scaffold MODULE=…` / `make test:scaffold` | Print pytest stubs for a router |
| `make coverage-ratchet` / `make coverage:ratchet` | Compare `coverage.xml` to policy floor |
| `make rule-lint` / `make rule:lint` | Lint `.cursor/rules` front matter |
| `make adr-index` / `make adr:index` | Regenerate `docs/adr/README.md` |
| `make codebase-summary` | Regenerate `CODEBASE_SUMMARY.md` |

Colon forms (e.g. `make queue:peek`) are aliases to the hyphenated targets in the root `Makefile`.

## IDE

Use your editor’s Python integration pointed at `.venv`. The repo uses Ruff and mypy; matching the versions in `pyproject.toml` avoids CI drift.

## Related

- [environment-vars.md](environment-vars.md) — settings reference
- [testing-guide.md](testing-guide.md) — pytest and coverage
- [git-workflow.md](git-workflow.md) — branches and PRs
