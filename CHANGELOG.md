# CHANGELOG.md

All notable changes to this project are documented in this file.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) version **1.1.0**. This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **Agent onboarding** — README and AGENTS.md explicitly require every agent session to read both; AGENTS.md adds re-read before merge/handoff when policy applies; branch cleanup after merge documented. PR template checkboxes for README/AGENTS.md reads and post-merge branch deletion.

- **`make queue:archive-top`** — archives the first (top) open row in `queue/queue.csv` without passing `QUEUE_ID` (`scripts/queue_archive.py --top`). Documented in queue agent SOP for token-efficient completion workflows.
- **Queue CSV `related_files` column** — between `dependencies` and `notes`; comma-separated repo-relative paths agents must read before completing an item. Validators (`scripts/queue_validate.py`), archive script, queue seeder, idea-parser manifest rows, and docs (`queue/QUEUE_INSTRUCTIONS.md`, `queue/QUEUE_AGENT_PROMPT.md`, `.cursor/rules/queue.md`) updated; conflict detection uses `summary` + `related_files`.
- **MCP integration** — optional `fastapi-mcp` mount at `/mcp`, custom `mcp_health_check` OpenAPI tool under `/mcp-tools/health_check`, procedure [docs/procedures/add-mcp-tool.md](docs/procedures/add-mcp-tool.md), and lockfile pins for the new dependency tree.
- **`example/` teaching module** — full CRUD under `/api/v1/examples` with repository/service layers, Alembic `examples` table, and integration tests; `make scaffold:module` now runs `module-scaffolder.py` with full file set; `idea-to-queue.sh` seeds from idea.md §12; `profile-resolver.py` supports `--profile` and `--apply`; skill machinery Make targets (`secret-scan`, `test-scaffold`, `env-sync`, `coverage-ratchet`, `rule-lint`, `adr-index`); regenerated `requirements.lock`; `CODEBASE_SUMMARY.md` full regeneration; exception unit tests (`test_exceptions.py`).
- K8s `deploy/k8s/base/secret.yaml` template for `api-secrets`; structured logging (`logging_config.py`); `RequestContext` dependency; auth repositories; OpenAPI metadata; `make fmt-check`, `skill-docs-gen`, `codebase-summary`; CI jobs for migration SQL dry-run and implementation-plan inventory; `docs/procedures/add-make-target.md`; `requirements.lock` placeholder; expanded `repo_self_audit` prompt checks; wired queue graph/analyze to `queue-intelligence.py`.
- Makefile aliases for colon-style targets documented in `spec/spec.md` (e.g. `make skills:list`, `make queue:peek`, `make audit:self`) delegating to existing hyphenated targets.
- **Content depth pass** (`spec/CONTENT_DEPTH_PASS.md`): expanded domain exceptions (`TenantIsolationError`, `StateTransitionError`, structured `AppError.detail` / `to_dict()`), SQLAlchemy pagination helpers, `PageInfo` / `PaginatedResponse` in contracts, central `dependencies.py` re-exports, tenant enforcement middleware for tests, real tenancy tests, queue intelligence CLI (`graph`, `analyze`, `ready`, `blocked`), docs generator pipeline (`skills/repo-governance/docs-generator.py` + `scripts/docs-generate.sh`), expanded `scripts/repo_self_audit.py`, multi-stage API Dockerfile (Python 3.12), seed rows in `queue/queue.csv`, bootstrap scripts (`setup.sh` / `setup.bat` / `run.sh` / `run.bat`), CI matrix (SQLite + Postgres), and AGENTS §15 + global canonical-commands rule.

### Changed

- Example module: `ExampleRepository.list_all` uses `paginate_query`; `ExampleService` takes `Settings`; routes use `require_auth`; `idea-to-queue.sh` matches prompt (`queue-seeder` defaults to idea §12); `env-var-sync` scans `os.getenv` / `os.environ` in Python sources.
- `make fmt` now applies formatting; CI uses `make fmt-check`. `docs:check` runs generated-docs drift detection. Dockerfile copies full `/usr/local/lib/python3.12` from the builder. `/ready` returns HTTP 503 when the database check fails. Prompt templates use a `# prompts/<file>.md` title line before YAML front matter.
- Consolidated open Dependabot updates: GitHub Actions (checkout, stale, docker/build-push-action, setup-buildx-action), API Docker base image to Python 3.14-slim, and Python dependency floors in `pyproject.toml` (asyncpg, bandit, email-validator, pydantic-settings, pytest-cov).
- Documentation and skills: removed blueprint-style `> PURPOSE:` / `> CONTENT:` blockquotes in favor of normal Markdown; filled stub skills from `spec/spec.md` summaries; expanded `docs/development/` guides (local setup, env vars, git workflow, testing, modules).
- Added maintenance scripts: `scripts/convert-blueprint-markdown.py`, `scripts/enrich-docs-from-spec.py`, `scripts/enrich-skills-from-spec.py` for future bulk doc alignment.

### Fixed

- **Trivy:** `.trivyignore` had a typo (`CVE-2024-23342N`) so PyPI `ecdsa` was not ignored; corrected. Documented Debian base-image CVEs in `docs/security/accepted-risks.md` and listed them in `.trivyignore` until `python:3.12-slim` ships fixes.
- **Migrations (SQLite):** `c2d3e4f5a6b7` uses `batch_alter_table(..., copy_from=...)` for SQLite FK add; CI `migrate-dry-run` SQL step no longer uses a pipe to `head` (avoids BrokenPipeError). Added `make ci-migrate-dry-run`.
- Docker image build: `.dockerignore` had excluded `*.md`, so `COPY README.md` in `apps/api/Dockerfile` failed; root `README.md` is now un-ignored for hatchling (`readme = "README.md"` in `pyproject.toml`).
- **Examples API:** list/get/update/delete are scoped to the authenticated user via `owner_user_id` (fixes `test_list_examples_empty` on shared Postgres CI DBs). Alembic migration `c2d3e4f5a6b7_add_example_owner_user_id`.
- **CI:** Trivy action `aquasecurity/trivy-action@v0.35.0` with `version: v0.69.3`; CD workflow logs into GHCR before push; dependency-review job uses `continue-on-error` when Dependency graph is disabled.

### Removed

### Security

- Container scanning: API runner stage runs `apt-get upgrade -y` after installing `curl` so Debian base packages match security updates; Security workflow Trivy step uses `trivy.yaml`, `.trivyignore`, `exit-code: 1`, and `aquasecurity/trivy-action@v0.35.0`. Accepted-risk CVEs listed in `.trivyignore` with rationale in `docs/security/accepted-risks.md`.

### Deprecated

## [0.1.0] — 2026-04-14

### Added

- Initial agent-operated template repository structure per **spec v4.0**
- FastAPI modular monolith layout (health, auth, tenancy) with tests and tooling
- CSV queue (`queue/queue.csv`, `queue/queuearchive.csv`) and queue SOPs
- Documentation tree, skills library, and prompt templates
- CI workflows (lint, typecheck, test, security) and Dependabot configuration
- Kubernetes base manifests with dev/staging/prod overlays
- Cross-platform bootstrap scripts (`setup.sh` / `setup.bat`, `run.sh` / `run.bat`)
- Makefile as the canonical command entrypoint

[Unreleased]: https://github.com/MHughesDev/template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MHughesDev/template/releases/tag/v0.1.0
