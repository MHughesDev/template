# CHANGELOG.md

All notable changes to this project are documented in this file.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) version **1.1.0**. This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- K8s `deploy/k8s/base/secret.yaml` template for `api-secrets`; structured logging (`logging_config.py`); `RequestContext` dependency; auth repositories; OpenAPI metadata; `make fmt-check`, `skill-docs-gen`, `codebase-summary`; CI jobs for migration SQL dry-run and implementation-plan inventory; `docs/procedures/add-make-target.md`; `requirements.lock` placeholder; expanded `repo_self_audit` prompt checks; wired queue graph/analyze to `queue-intelligence.py`.
- Makefile aliases for colon-style targets documented in `spec/spec.md` (e.g. `make skills:list`, `make queue:peek`, `make audit:self`) delegating to existing hyphenated targets.
- **Content depth pass** (`spec/CONTENT_DEPTH_PASS.md`): expanded domain exceptions (`TenantIsolationError`, `StateTransitionError`, structured `AppError.detail` / `to_dict()`), SQLAlchemy pagination helpers, `PageInfo` / `PaginatedResponse` in contracts, central `dependencies.py` re-exports, tenant enforcement middleware for tests, real tenancy tests, queue intelligence CLI (`graph`, `analyze`, `ready`, `blocked`), docs generator pipeline (`skills/repo-governance/docs-generator.py` + `scripts/docs-generate.sh`), expanded `scripts/repo_self_audit.py`, multi-stage API Dockerfile (Python 3.12), seed rows in `queue/queue.csv`, bootstrap scripts (`setup.sh` / `setup.bat` / `run.sh` / `run.bat`), CI matrix (SQLite + Postgres), and AGENTS §15 + global canonical-commands rule.

### Changed

- `make fmt` now applies formatting; CI uses `make fmt-check`. `docs:check` runs generated-docs drift detection. Dockerfile copies full `/usr/local/lib/python3.12` from the builder. `/ready` returns HTTP 503 when the database check fails. Prompt templates use a `# prompts/<file>.md` title line before YAML front matter.
- Consolidated open Dependabot updates: GitHub Actions (checkout, stale, docker/build-push-action, setup-buildx-action), API Docker base image to Python 3.14-slim, and Python dependency floors in `pyproject.toml` (asyncpg, bandit, email-validator, pydantic-settings, pytest-cov).
- Documentation and skills: removed blueprint-style `> PURPOSE:` / `> CONTENT:` blockquotes in favor of normal Markdown; filled stub skills from `spec/spec.md` summaries; expanded `docs/development/` guides (local setup, env vars, git workflow, testing, modules).
- Added maintenance scripts: `scripts/convert-blueprint-markdown.py`, `scripts/enrich-docs-from-spec.py`, `scripts/enrich-skills-from-spec.py` for future bulk doc alignment.

### Fixed

### Removed

### Security

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
