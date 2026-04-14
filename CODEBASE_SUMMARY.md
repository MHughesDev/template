# CODEBASE_SUMMARY.md

Dense orientation for agents (~100 lines). Read **`AGENTS.md`** and **`spec/spec.md`** for full policy.

## One-line description

Python 3.12+ **FastAPI** modular monolith template: async SQLAlchemy + Alembic, JWT auth, CSV **queue**, **skills** with runnable machinery, **Make**-backed scripts, Docker/K8s, GitHub Actions.

## Repository structure

```
repo-root/
├── apps/api/          # FastAPI app (health, auth, tenancy)
├── packages/          # contracts (Pydantic), tasks (protocols), ai (optional ChromaDB)
├── deploy/            # Kustomize base + dev/staging/prod overlays
├── docs/              # Architecture, procedures, operations, API notes
├── queue/             # queue.csv, archive, SOPs
├── skills/            # Playbooks + *.py tooling
├── prompts/           # Role templates (YAML front matter)
├── scripts/           # Shell + Python helpers for Make targets
├── .cursor/           # Rules + commands
├── .github/           # CI, CD, Dependabot, templates
└── monitoring/        # Prometheus/Grafana stubs
```

## Key files

| File | Role |
|------|------|
| `AGENTS.md` | Agent policy (read first) |
| `spec/spec.md` | Canonical specification |
| `idea.md` | Project intake |
| `Makefile` | `make lint`, `make test`, `make queue-validate`, … |
| `queue/QUEUE_INSTRUCTIONS.md` | Queue SOP |
| `queue/queue.csv` | Open work items |
| `skills/README.md` | Skills index |
| `prompts/README.md` | Prompt index |
| `PYTHON_PROCEDURES.md` | Python style |

## Stack

- **Runtime:** Python 3.12, FastAPI, Uvicorn  
- **Data:** SQLAlchemy 2 async, Alembic, SQLite (dev) / PostgreSQL (prod)  
- **Auth:** JWT + refresh tokens (passlib pbkdf2)  
- **Quality:** Ruff, mypy strict, pytest + pytest-asyncio + coverage  
- **Ops:** Docker Compose, Kubernetes (Kustomize), GitHub Actions  

## Agent workflow

1. Read `AGENTS.md` → task → **`make skills-list`** / search `skills/` → plan  
2. Implement in small steps → **`make lint`** + **`make test`**  
3. Before PR: **`make audit-self`**, **`make queue-validate`** if queue touched  
4. Handoff: files, commands, PR link, queue archive if applicable  

## API module pattern

Under `apps/api/src/<context>/`: `router.py` (HTTP), `schemas.py`, `models.py`, `service.py`, `dependencies.py`. Register routers in `main.py` under `api_prefix`.

## Queue CSV

Columns: `id, batch, phase, category, summary, dependencies, notes, created_date`. Summaries should be elaborative. **`scripts/queue_validate.py`** enforces schema.

## CI (`.github/workflows/ci.yml`)

Checkout → setup Python → **`make lint`**, **`make fmt`**, **`make typecheck`**, **`make test`**, **`make queue-validate`**, **`make audit-self`**.
