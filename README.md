# 🏭 Template — Agent-Operated Software Factory

> **Ship production-grade software with AI agents doing the heavy lifting.**
> A Cursor-first, Claude-ready template that turns a single `idea.md` file into a fully-wired FastAPI backend, optional React/Expo frontends, a live CI pipeline, and a self-auditing docs system.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose_v2-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

</div>

---

## ✨ What you get

| | Feature |
|---|---------|
| 🤖 | **Agent-native from day one** — AGENTS.md contract, skill playbooks, prompt templates, CSV task queue |
| ⚡ | **One command bootstrap** — `./setup.sh` wires deps, env, migrations, and tests automatically |
| 🧩 | **Profile system** — enable/disable React web, Expo mobile, billing, multi-tenancy, workers, and more |
| 🔒 | **Security built-in** — JWT auth, tenant isolation, CORS policy, threat model, secrets management |
| 🧪 | **Full test pyramid** — unit, integration, smoke; 55% coverage floor enforced in CI |
| 📋 | **Self-auditing repo** — `make audit:self` checks 7 invariants; CI blocks on failure |
| 📖 | **Living documentation** — freshness checks, drift detection, improvement loops |
| 🚢 | **Production-ready CI** — lint, typecheck, test matrix (SQLite + Postgres), migrate dry-run |

---

## 🚀 Quickstart

```bash
# 1. Clone
git clone <repo-url> && cd <repo-name>

# 2. Bootstrap (recommended)
./setup.sh          # Linux/macOS
setup.bat           # Windows

# 3. Start developing
make dev            # spin up local API + dev stack
make test           # run full test suite
```

> **Manual path:** `cp .env.example .env`, edit values, then `make dev` + `make test`.

---

## 🗺️ How it works

```
idea.md  ──►  make idea:execute  ──►  fully-wired FastAPI app
   │                                        │
   │  describe your project                 │  scaffolded modules
   │  pick profiles (web, billing…)         │  wired routes + DB models
   │  list bounded contexts                 │  CI/CD pipeline
   └──────────────────────────────────────►─┘  enabled profile code
```

1. **Fill `idea.md`** — name, archetype, profiles, bounded contexts, queue seeds.
2. **Run `make idea:validate`** — catches errors before anything writes to disk.
3. **Run `make idea:execute`** — orchestrator scaffolds, wires, and opens a PR.
4. **Ship features** — agents use `AGENTS.md`, skills, and the queue to work autonomously.

---

## 🧩 Profiles

Enable optional capabilities in `idea.md §5`:

| Profile | What it adds |
|---------|-------------|
| `web` | Next.js App Router frontend in `apps/web/` |
| `mobile` | Expo/React Native app in `apps/mobile/` |
| `workers` | Celery + Redis background task infrastructure |
| `billing` | Stripe integration scaffolding |
| `multi_tenancy` | Tenant isolation layer + JWT `tenant_id` claim |
| `analytics` | Event tracking package in `packages/analytics/` |
| `notifications` | Email/push notification service |
| `admin_ui` | Admin panel scaffolding |
| `storage` | File upload + S3-compatible storage |
| `search` | Full-text search integration |
| `feature_flags` | Feature flag service scaffolding |

---

## 🛠️ Essential commands

```bash
make dev              # start local dev stack
make test             # full test suite with coverage
make test-unit        # unit tests only (fast, no DB)
make test-integration # integration tests only
make lint             # Ruff linter
make fmt              # format check
make typecheck        # mypy strict
make migrate          # run Alembic migrations
make audit:self       # 7-check repo self-audit
make queue:top-item   # one JSON line — full top queue row (agents: read this first)
make queue:peek       # raw CSV: header + first row
make docs:check       # verify doc link integrity
make help             # full target catalog
```

---

## 📁 Project structure

```
.
├── apps/
│   ├── api/          # FastAPI application (always present)
│   ├── web/          # Next.js frontend (web profile)
│   └── mobile/       # Expo app (mobile profile)
├── packages/         # Shared Python packages (per-profile)
├── scripts/          # Orchestration, validation, scaffold scripts
│   └── profiles/     # enable-*.sh / discard-*.sh for each profile
├── skills/           # Agent playbooks by domain
├── prompts/          # Role-specific prompt templates
├── docs/             # Architecture, procedures, governance, security
├── queue/            # CSV task queue + instructions
├── spec/             # Full system specification
├── idea.md           # ← Start here: your project intake form
├── AGENTS.md         # ← Agent contract and workflow policy
└── Makefile          # All automation targets
```

---

## 📚 Key resources

| Resource | Path | Purpose |
|----------|------|---------|
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

---

## 🔧 Technical details

### Stack

| Layer | Technology |
|-------|-----------|
| API framework | FastAPI 0.110+ with Pydantic v2 |
| ORM | SQLAlchemy 2.0 async |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt |
| Task queue | Celery + Redis (workers profile) |
| Test runner | pytest with asyncio, SQLite in-memory |
| Linter | Ruff |
| Type checker | mypy (strict) |
| Containerisation | Docker multi-stage (python:3.12-slim) |
| CI | GitHub Actions — lint, test matrix, migrate dry-run, audit |

### Prerequisites

| Tool | Minimum | Check |
|------|---------|-------|
| Python | 3.12 | `python --version` |
| Docker + Compose | v2+ | `docker compose version` |
| GNU Make | any | `make --version` |
| Git | any | `git --version` |
| Node (web profile) | 20+ | `node --version` |
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
