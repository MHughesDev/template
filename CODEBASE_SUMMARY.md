# CODEBASE_SUMMARY.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §Navigation, .cursorignore (not excluded) -->

> PURPOSE: Token-efficient LLM context summary (~100 lines). A dense reference document that gives an agent a complete structural orientation in minimal tokens. Per spec §26.12 item 407. Optional but recommended.

## One-Line Description

> CONTENT: Single sentence: what this repository is and does. Example: "Python 3.12+ FastAPI template repository, agent-operated, with queue-driven work orchestration, 70+ skills, full CI/CD, and optional React/Expo profiles."

## Repository Structure (compressed)

> CONTENT: Compact tree showing only top-level directories and their one-line purpose. Format:
> ```
> repo-root/
> ├── apps/api/          # FastAPI modular monolith (health, auth, tenancy)
> ├── packages/          # Shared contracts, task interfaces, AI interfaces
> ├── deploy/            # Docker + Kubernetes (Kustomize base + overlays)
> ├── docs/              # Full documentation hub (procedures, architecture, operations...)
> ├── queue/             # CSV-based agent work orchestration
> ├── skills/            # 70+ executable skill playbooks + machinery
> ├── prompts/           # 22 reusable agent role templates
> ├── scripts/           # Shell implementations of all Make targets
> ├── .cursor/           # Machine control: rules (constraints) + commands
> ├── .github/           # CI/CD workflows, templates, Dependabot, CODEOWNERS
> └── monitoring/        # Prometheus + Grafana observability stack
> ```

## Key Files (quick reference)

> CONTENT: Table of the most important files an agent needs. Columns: File, Purpose. Rows:
> - AGENTS.md — root agent policy (read first)
> - spec/spec.md — canonical specification v4.0
> - idea.md — project intake form (fill before initialization)
> - queue/QUEUE_INSTRUCTIONS.md — queue SOP
> - queue/queue.csv — open work items (top row = active)
> - skills/README.md — skills index by category
> - prompts/README.md — prompt template index
> - Makefile — all canonical commands
> - PYTHON_PROCEDURES.md — Python coding procedures (18 rules)
> - docs/procedures/README.md — all SOPs index

## Primary Stack

> CONTENT: Bullet list of core technologies: Python 3.12+, FastAPI, SQLAlchemy (async), Alembic, Pydantic v2, pytest + pytest-asyncio, ruff (lint+fmt), mypy (--strict), Docker + Docker Compose, Kubernetes (Kustomize), GitHub Actions.

## Agent Workflow (4 lines)

> CONTENT: Ultra-compressed workflow:
> 1. Read AGENTS.md → task → skills/ (mandatory search) → plan
> 2. Implement in increments → make lint + test after each
> 3. Validate: make audit:self before PR
> 4. Handoff: files changed + commands run + PR link + queue update

## Module Pattern (compressed)

> CONTENT: One-paragraph description of the canonical module layout in apps/api/src/<context>/: __init__.py (exports), router.py (handlers), models.py (SQLAlchemy), schemas.py (Pydantic), service.py (business logic), dependencies.py (FastAPI Depends factories). Import direction: router → service → repository → DB.

## Queue Schema

> CONTENT: One-line CSV column listing: `id, batch, phase, category, summary, dependencies, notes, created_date`. State: "summary must be elaborative (≥100 chars with goal, acceptance criteria, definition of done, out-of-scope)."

## CI Checks

> CONTENT: Ordered list: fmt → lint → typecheck → test (coverage) → build → image scan → docs:check → migration dry-run → k8s validate.
