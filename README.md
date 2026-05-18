# 🏭 Template — Agent-Operated Full-Stack Software Factory

> **Ship production-grade software with AI agents doing the heavy lifting.**
> A Cursor-first, Claude-ready full-stack template: **FastAPI + React 19** out of the box, wired through a typed OpenAPI client, with `idea.md` → fully-wired app initialization, a self-auditing docs system, a CSV task queue, and skill-driven agent playbooks.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.114+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose_v2-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

</div>

---

## For coding agents (required every session)

1. **MicroFast dev MCP first** — before reading this file or acting on the repo, ensure **`microfast-dev`** is connected (see **[AGENTS.md](AGENTS.md)** section 3 step 1). If it is already running in your client, do not start another. Details: [docs/procedures/microfast-dev-mcp.md](docs/procedures/microfast-dev-mcp.md).
2. Read this **README.md** (you are here) for orientation, structure, and commands.
3. Read **[AGENTS.md](AGENTS.md)** completely — it is the **authoritative** policy for workflow, hierarchy, validation, and handoff. Re-read **`AGENTS.md`** whenever policy is unclear or you are merging or handing off work.
4. Follow the mandatory skill search in **`AGENTS.md`** section 13 (`skills/README.md` or `make skills:list`).
5. Land changes via **pull request**; after **merge**, **delete the feature branch** (remote and local).

---

## ✨ What you get

| | Feature |
|---|---------|
| 🤖 | **Agent-native from day one** — AGENTS.md contract, skill playbooks, prompt templates, CSV task queue |
| 🐍 | **Real FastAPI backend** — SQLModel + Postgres + Alembic + JWT auth + email + Sentry (`apps/api/`) |
| ⚛️ | **Real React 19 frontend** — Vite + TanStack Router/Query + Tailwind v4 + shadcn/ui (`apps/web/`) |
| 🔌 | **Typed end-to-end** — OpenAPI → typed TS client via `openapi-ts` (`make generate-client`) |
| 🐳 | **Production-grade Docker** — `compose.yml` + override + Traefik stack from Tiangolo's template |
| 🔒 | **Security built-in** — JWT auth, password hashing (argon2/bcrypt), CORS policy, secrets management |
| 🧪 | **Full test pyramid** — pytest (backend) + Playwright (frontend) with fixtures and CI hooks |
| 📋 | **Self-auditing repo** — `make audit:self` checks 7 invariants; CI blocks on failure |
| 📖 | **Living documentation** — freshness checks, drift detection, improvement loops |
| 🧩 | **Profile system** — enable/disable optional capabilities (mobile, workers, AI/RAG, etc.) |

---

## 🚀 Quickstart

```bash
# 1. Clone
git clone <repo-url> && cd <repo-name>

# 2. Configure
cp .env.example .env       # edit SECRET_KEY, POSTGRES_*, FIRST_SUPERUSER_*

# 3. Start the full stack with Docker (Postgres + backend + frontend + adminer)
make docker-up             # equivalent: docker compose up -d
make health-check          # GET /api/v1/utils/health-check/

# 4. Or run pieces locally
make web-install           # install frontend deps via bun
make dev-api               # FastAPI on :8000 (needs Postgres running)
make dev-web               # Vite on :5173

# 5. Tests
make test                  # backend pytest with coverage
make test-web              # frontend Playwright e2e
```

> The frontend talks to the backend via a generated TypeScript client. After
> changing backend routes or schemas, run `make generate-client` to refresh
> `apps/web/src/client/`.

---

## 🗺️ How it works

```
idea.md ─►  skills/init/repo_initialize.md  ─►  refreshed spec/docs + initial MVP queue
   (human-authored)                                (no product code yet — that's queued)
```

1. **Fill out `idea.md` end-to-end** — every applicable section, with `N/A` where inapplicable. `idea.md` is the canonical product-intake contract.
2. **Ask an AI agent to run `skills/init/repo_initialize.md`** — the single canonical procedural skill. It refreshes the spec, generates design docs from the spec, and seeds initial MVP queue rows. It does **not** write product code.
3. **Resolve open questions** — the skill creates blocked `category=human-ops` queue rows for anything ambiguous in `idea.md`. Answer them and unblock.
4. **Ship features** — agents pick the top row of `queue/queue.csv` and execute against the `acceptance_criteria` in that row. Each row is sized so an executor can pick it up cold.

There is no `make idea:*` orchestrator — initialization is an AI-judged procedure, not a shell command.

---

## 🧩 What's in the box

The full-stack app is **always present** (no profile required):

| Path | What it is |
|------|-----------|
| `apps/api/` | FastAPI + SQLModel + Postgres + Alembic + JWT (Tiangolo full-stack template) |
| `apps/web/` | React 19 + Vite + TanStack Router/Query + Tailwind v4 + shadcn/ui |
| `packages/contracts/` | Cross-service Pydantic models, error catalog, pagination helpers |
| `packages/tasks/` | Background task interfaces (Celery-compatible) |
| `packages/ai/` | Optional ChromaDB client + RAG helpers (extras: `pip install -e .[ai]`) |
| `dev_mcp/` | MicroFast dev MCP server used by Cursor / Claude clients |
| `compose.yml` | Full Docker stack: db + adminer + backend + frontend + prestart |
| `compose.traefik.yml` | Production Traefik overlay |

Optional profiles (enable via `idea.md §5`):

| Profile | What it adds |
|---------|-------------|
| `mobile` | Expo/React Native app in `apps/mobile/` |
| `workers` | Celery + Redis background task infrastructure |
| `billing` | Stripe integration scaffolding |
| `multi_tenancy` | Tenant isolation layer + JWT `tenant_id` claim |
| `analytics` | Event tracking package in `packages/analytics/` |
| `notifications` | Email/push notification service |
| `admin_ui` | Admin panel scaffolding (note: a minimal admin UI is already in `apps/web/`) |
| `storage` | File upload + S3-compatible storage |
| `search` | Full-text search integration |
| `feature_flags` | Feature flag service scaffolding |
| `ai_rag` | ChromaDB vector store + retrieval helpers |

---

## 🛠️ Essential commands

```bash
# Local dev (backend + frontend)
make dev-api          # FastAPI with uvicorn --reload (port 8000)
make dev-web          # Vite dev server (port 5173)
make docker-up        # full stack via docker compose (db + backend + frontend)
make docker-down      # tear it down

# Backend
make test             # pytest with coverage
make lint             # Ruff lint
make fmt              # Ruff format
make typecheck        # mypy
make migrate          # alembic upgrade head
MESSAGE="add foo" make migrate:create   # autogenerate revision
make db-reset         # drop + recreate Postgres dev db, run prestart

# Frontend
make web-install      # bun install
make lint-web         # biome
make test-web         # Playwright
make generate-client  # regenerate apps/web/src/client/ from backend OpenAPI

# Systemization layer (preserved from template)
make audit:self       # 7-check repo self-audit
make queue:top-item   # one JSON line — full top queue row (agents: read this first)
make queue:peek       # raw CSV: header + first row
make queue:pr-merge   # after archive+validate — gh merge + delete branch
make docs:check       # verify doc link integrity
make help             # full target catalog
```

---

## 📁 Project structure

```
.
├── apps/
│   ├── api/                # FastAPI backend (SQLModel + Postgres + Alembic)
│   │   ├── app/            # Python package (app.main, app.api, app.core, ...)
│   │   ├── alembic.ini
│   │   ├── tests/          # pytest suite (api / crud / scripts / utils)
│   │   ├── scripts/        # format / lint / test / prestart
│   │   ├── pyproject.toml  # backend deps (uv-managed)
│   │   └── Dockerfile
│   ├── web/                # React 19 + Vite frontend
│   │   ├── src/            # routes/, components/, client/ (generated), ...
│   │   ├── tests/          # Playwright e2e
│   │   ├── public/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── openapi-ts.config.ts
│   │   └── Dockerfile / Dockerfile.playwright
│   └── mobile/             # Expo app stub (mobile profile)
├── packages/               # Optional Python packages
│   ├── contracts/          # Shared Pydantic models + error catalog
│   ├── tasks/              # Background task interfaces
│   └── ai/                 # ChromaDB / RAG helpers (extras)
├── compose.yml             # Full Docker stack (db + adminer + backend + frontend + prestart)
├── compose.override.yml    # Local dev overrides (volume mounts, hot reload)
├── compose.traefik.yml     # Production Traefik overlay
├── scripts/                # Orchestration, validation, scaffold scripts
│   └── profiles/           # enable-*.sh / discard-*.sh for each profile
├── skills/                 # Agent playbooks by domain
├── prompts/                # Role-specific prompt templates
├── docs/                   # Architecture, procedures, governance, security
├── queue/                  # CSV task queue + instructions
├── spec/                   # Full system specification
├── dev_mcp/                # MicroFast dev MCP server for Cursor / Claude
├── idea.md                 # ← Start here: your project intake form
├── AGENTS.md               # ← Agent contract and workflow policy
├── pyproject.toml          # Repo-wide Python tool config (ruff, mypy, pytest)
├── package.json            # Bun workspace pointing at apps/web
└── Makefile                # All automation targets
```

---

## 📚 Key resources

| Resource | Path | Purpose |
|----------|------|---------|
| **Documentation map** | [docs/DOCS_MAP.md](docs/DOCS_MAP.md) | Stable `doc_id` index for every file under `docs/` |
| **Agent contract** | [AGENTS.md](AGENTS.md) | Read first — policy, workflow, escalation |
| **Full spec** | [spec/spec.md](spec/spec.md) | Authoritative design and requirements |
| **Getting started** | [docs/getting-started/](docs/getting-started/) | Prerequisites and detailed quickstart |
| **Architecture** | [docs/architecture/](docs/architecture/) | System design and bounded contexts |
| **Init procedure** | [docs/procedures/initialize-from-idea.md](docs/procedures/initialize-from-idea.md) | Step-by-step `idea.md` → app |
| **Queue** | [queue/QUEUE_INSTRUCTIONS.md](queue/QUEUE_INSTRUCTIONS.md) | CSV queue lifecycle |
| **Skills** | [skills/README.md](skills/README.md) | Agent playbooks by category |
| **Prompts** | [prompts/README.md](prompts/README.md) | Role-specific prompt templates |
| **Security** | [docs/security/](docs/security/) | Threat model, secrets, CORS, incidents |
| **API docs** | [docs/api/](docs/api/) | Endpoints and error catalog |
| **Founding ADR** | [docs/adr/0001-initial-template-architecture.md](docs/adr/0001-initial-template-architecture.md) | The template's initialization model: idea.md → repo_initialize skill → docs + queue |

---

## 🔧 Technical details

### Stack

| Layer | Technology |
|-------|-----------|
| API framework | FastAPI 0.114+ with Pydantic v2 |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| Database | PostgreSQL 18 (Postgres 16 also fine) |
| Migrations | Alembic |
| Auth | JWT (PyJWT) + pwdlib (argon2 / bcrypt) |
| Email | `emails` + Jinja2 + MJML templates |
| Observability | Sentry SDK (`sentry-sdk[fastapi]`) |
| Backend tests | pytest with fixtures + coverage |
| Backend lint | Ruff |
| Backend type checker | mypy + `ty` |
| Frontend framework | React 19 + Vite 7 |
| Frontend router | TanStack Router (file-based) |
| Frontend state | TanStack Query |
| Frontend styling | Tailwind v4 + shadcn/ui + Radix |
| Frontend forms | react-hook-form + zod |
| Frontend lint/format | Biome |
| Frontend tests | Playwright |
| Typed client | `@hey-api/openapi-ts` (generated from `/api/v1/openapi.json`) |
| Containerisation | Docker multi-stage (python:3.10 + nginx) |
| Orchestration | Docker Compose v2 + optional Traefik |
| Task queue | Celery + Redis (workers profile) |
| CI | GitHub Actions — lint, test matrix, migrate dry-run, audit |

### Prerequisites

| Tool | Minimum | Check |
|------|---------|-------|
| Python | 3.10 | `python --version` |
| Docker + Compose | v2+ | `docker compose version` |
| GNU Make | any | `make --version` |
| Git | any | `git --version` |
| Bun (frontend) | 1.x | `bun --version` |
| uv (backend pkg mgr) | 0.4+ | `uv --version` |
| Expo CLI (mobile profile) | latest | `npx expo --version` |

Full details and troubleshooting: [docs/getting-started/prerequisites.md](docs/getting-started/prerequisites.md).

### CI pipeline

Every PR runs:
1. **`lint`** — Ruff + import order
2. **`fmt`** — Black/Ruff format check
3. **`typecheck`** — mypy strict
4. **`test`** — pytest matrix: SQLite and PostgreSQL
5. **`ci-migrate-dry-run`** — Alembic `--sql` dry run
6. **`audit-self`** — 7-check repo self-audit

All jobs must pass before merge. See `.github/workflows/ci.yml`.

### Repo self-audit (`make audit:self`)

The audit script checks 7 invariants on every PR:

| Check | What it validates |
|-------|------------------|
| `required_files` | All critical files exist (AGENTS.md, Dockerfile, queue CSVs, CI workflows) |
| `queue_validate` | `queue/queue.csv` schema valid; summaries ≥ 100 chars |
| `file_title_comments` | Every `.py`, `.md`, `.sh`, `.yml` has a first-line title comment |
| `skills_headings` | Every skill `.md` has Purpose, When to invoke, Prerequisites headings |
| `prompts_frontmatter` | Every prompt template has a `---` YAML frontmatter block |
| `prompts_title_and_fields` | Prompt frontmatter contains `purpose:` and `when_to_use:` |
| `makefile_help` | Every Makefile target has a `## target: description` help comment |

---

## 📄 License

MIT — see [LICENSE](LICENSE).
