# Full Template Repository Specification

**Version:** 1.0  
**Stack:** Python 3.12+, FastAPI, optional React/Expo front-ends  
**Philosophy:** Cursor-first, GitHub-centric, backend-centric modular monolith with a clean path to microservices  

This document is the authoritative specification for a **downloadable, batteries-included template repository**. Implementers should treat it as a checklist: every section maps to folders, files, or processes to create or adopt.

---

## 1. Goals and Non-Goals

### 1.1 Goals

- Provide a **production-minded starting point** for API-first products (SaaS, internal tools, AI-augmented backends).
- Be **Cursor-first**: skills, rules, and repeatable commands are first-class artifacts, not afterthoughts.
- Be **GitHub-centric**: issues, PRs, Actions, and repository hygiene are assumed from day one.
- Support **CI and CD** with clear separation: validate on every change, deploy on approved paths.
- Prefer **Docker** for local parity and **Kubernetes** for deployment, with **optional managed cloud** (any provider that runs K8s or containers).
- Include a **simple, file-based queue system** for agent work (`queue.csv` / `queuearchive.csv`) with explicit workflows and an agent prompt.
- Ship a **structured `docs/` tree** so onboarding and operations do not depend on tribal knowledge.
- Offer **optional** web and mobile clients; the **core product is the backend** (FastAPI).
- Use a **modular monolith** layout that can **split into microservices** without rewriting domain logic.
- Include a **full authentication layer** that is **optional multi-tenant**, supports **organizational SSO**, **JWTs**, and **email/password**, with clear extension points.
- Use **SQLite** when the app is single-node / dev / small-scale; use **PostgreSQL** when multi-instance, HA, or heavy concurrency is expected.
- When AI/RAG features are in scope, use **ChromaDB** (vector store) with Docker/K8s-friendly deployment.

### 1.2 Non-Goals

- Prescribing a single cloud vendor (AWS/GCP/Azure) beyond “containers + K8s + optional managed DBs.”
- Shipping a full design system for optional front-ends (only stubs and integration points).
- Replacing a dedicated issue tracker with the CSV queue (the queue is for **agent work coordination**, not product backlog management).

---

## 2. Repository Topology (High Level)

```
repo-root/
├── .cursor/                    # Cursor: rules, optional commands metadata
├── .github/                    # GitHub: CI/CD, templates, CODEOWNERS, dependabot
├── apps/
│   ├── api/                    # FastAPI modular monolith (primary)
│   ├── web/                    # Optional: React (or similar) SPA
│   └── mobile/                 # Optional: Expo/React Native
├── packages/                   # Shared Python libs (domain, contracts, clients)
├── deploy/
│   ├── docker/                 # Dockerfiles, compose for local + CI
│   └── k8s/                    # Helm or Kustomize base + overlays (dev/stage/prod)
├── docs/                       # Full documentation tree (see §8)
├── queue/
│   ├── queue.csv               # Open queue items (single writer discipline)
│   ├── queuearchive.csv        # Completed / cancelled items (append-only archive)
│   ├── QUEUE_INSTRUCTIONS.md # Human + agent instructions for the queue
│   └── QUEUE_AGENT_PROMPT.md # Copy-paste prompt for queue-processing agents
├── skills/                     # Cursor skills (large catalog, see §3)
├── scripts/                    # Dev ergonomics: fmt, lint, migrate, queue helpers
├── .env.example
├── docker-compose.yml          # Root compose: api, db, chroma (optional), reverse proxy (optional)
├── Makefile or taskfile        # One entrypoint for common commands
├── pyproject.toml              # Workspace / tooling at root if monorepo
└── README.md                   # Quickstart + links to docs/
```

**Naming:** This spec uses `queue/` at the repo root so paths are obvious and grep-friendly. If you prefer `.queue/` or `agent-queue/`, keep the **file names** `queue.csv` and `queuearchive.csv` as specified.

---

## 3. Cursor-First: Skills, Rules, and Commands

### 3.1 `.cursor/rules` (Repository Rules)

Create rule files (Markdown or `.mdc` per Cursor conventions) that encode:

- **Stack:** Python + FastAPI, `uv` or `pip-tools`, typing (`mypy` or `pyright`), formatting (`ruff format`), linting (`ruff`).
- **API design:** OpenAPI-first, versioned routes (`/api/v1/...`), Pydantic v2 models, explicit error payloads.
- **Security:** no secrets in repo; JWT handling; cookie vs header; CORS policy by environment.
- **Testing:** `pytest`, coverage thresholds in CI, contract tests for public HTTP APIs.
- **Database:** SQLAlchemy 2.x async optional; Alembic migrations; SQLite vs Postgres selection rules.
- **Multi-tenancy:** tenant resolution order (JWT claim → header → subdomain), and denial-by-default data access.
- **Queue discipline:** one agent at a time; read top row; move to archive when done; never delete history without archiving.

### 3.2 `skills/` Folder (Large Catalog)

The `skills/` directory holds **reusable skill documents** (Markdown). Each skill is a short, actionable guide Cursor (or humans) can apply. Minimum categories and example skill titles:

| Category | Example skill files |
|----------|---------------------|
| **FastAPI & Python** | `fastapi-router-layout.md`, `pydantic-v2-patterns.md`, `dependency-injection-auth.md`, `background-tasks-and-workers.md` |
| **Data & persistence** | `sqlalchemy-async-patterns.md`, `alembic-migrations.md`, `sqlite-to-postgres-migration.md`, `redis-caching.md` |
| **Auth & security** | `jwt-access-refresh.md`, `oauth2-oidc-sso-org.md`, `multi-tenant-data-scoping.md`, `rbac-and-policies.md` |
| **AI / RAG** | `chromadb-ingestion.md`, `embedding-pipelines.md`, `rag-evaluation-checklist.md` |
| **DevOps** | `docker-multi-stage-builds.md`, `kubernetes-health-probes.md`, `github-actions-cache.md`, `secrets-management-k8s.md` |
| **Testing & quality** | `pytest-asyncio.md`, `httpx-testing.md`, `load-testing-k6.md` |
| **Frontend (optional)** | `react-query-api.md`, `expo-secure-storage.md` |
| **Queue & agents** | `queue-csv-workflow.md`, `agent-handoff-checklist.md` |

**Requirement:** The template repo should ship **at least 25** skill stubs (title + outline + “when to use”), with **5** fully written end-to-end (e.g. FastAPI layout, Alembic, JWT, Docker, queue workflow).

### 3.3 Commands (Documented + Scripted)

Expose consistent commands via `Makefile` or `task` + `scripts/`:

| Command | Purpose |
|---------|---------|
| `dev` | Run API locally with hot reload |
| `lint` | Ruff + optional typecheck |
| `test` | Pytest with coverage |
| `migrate` | Run Alembic upgrades |
| `docker:up` / `docker:down` | Compose stack |
| `queue:peek` | Print header + first open row (read-only helper) |
| `queue:validate` | Validate CSV schema and invariants |

Document these in `docs/development/local-setup.md` and mirror short descriptions in `README.md`.

---

## 4. GitHub-Centric: `.github/` Layout

### 4.1 Required Contents

```
.github/
├── workflows/
│   ├── ci.yml              # Lint, typecheck, tests, build images on PRs
│   ├── cd.yml              # Deploy on tags or main branch (environment-gated)
│   └── security.yml        # Dependency review, CodeQL optional
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
├── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS              # Optional but recommended
├── dependabot.yml          # Python, GitHub Actions, Docker base images
└── labels.yml              # Optional: standardized labels (sync via workflow or manual)
```

### 4.2 CI Pipeline (Conceptual Stages)

1. **Checkout** → cache dependencies.  
2. **Static analysis** → `ruff`, `ruff format --check`, optional `mypy`/`pyright`.  
3. **Tests** → `pytest` with coverage report artifact.  
4. **Build** → Docker image build (API) and scan (Trivy or GitHub’s built-in).  
5. **Optional matrix** → Python version, SQLite vs Postgres test job.

### 4.3 CD Pipeline (Conceptual)

- **Triggers:** protected branch (`main`), or semver tags (`v*.*.*`), or manual `workflow_dispatch`.  
- **Artifacts:** container images pushed to GHCR (or other registry).  
- **Deploy:** Kubernetes apply (Helm upgrade) or cloud-specific deploy **behind** a thin abstraction so the template stays portable.  
- **Environments:** `development`, `staging`, `production` with GitHub Environment protection rules.

---

## 5. Backend: Modular Monolith (FastAPI) and Microservice Readiness

### 5.1 Modular Monolith Principles

- **Bounded contexts** as Python packages under `packages/` or `apps/api/src/<context>/`.
- **Stable contracts:** OpenAPI for HTTP; internal use of **pydantic models** shared via `packages/contracts`.
- **No shared DB tables across contexts** without explicit foreign keys and documented ownership.
- **Outbox pattern** (optional): domain events table for future async consumers.

### 5.2 Microservice Split Criteria

Document in `docs/architecture/modular-monolith.md`:

- When a context has **independent deploy cadence**, **separate scaling**, or **different SLOs**, extract to a service with the same contract package.
- **Strangler pattern:** new endpoints in a new deployable first, old clients migrate.

### 5.3 Optional Workers

- For long tasks: **Celery + Redis/RabbitMQ** or **Arq** (Redis) — keep interface in `packages/tasks` so the worker can become a separate deployment later.

---

## 6. Data Layer: SQLite vs PostgreSQL, ChromaDB for AI

### 6.1 Default Policy

| Profile | Database | When |
|---------|----------|------|
| **Local / MVP / single node** | SQLite | Fast iteration, minimal ops |
| **Production / HA / concurrent writes** | PostgreSQL | Required for serious multi-tenant SaaS |

**Configuration:** Single `DATABASE_URL` with documented switching; Alembic migrations must support both where feasible (avoid raw SQL that is SQLite-only in shared migrations).

### 6.2 ChromaDB (AI / RAG)

- Run Chroma as **its own container** in Compose and K8s.  
- Persist volumes for embeddings; document backup/restore in `docs/operations/`.  
- Application code isolates **vector operations** behind `packages/ai/` interfaces.

---

## 7. Authentication and Multi-Tenancy (Pre-Built, Optional)

### 7.1 Features

- **Email + password** with secure hashing (argon2/bcrypt), email verification hooks (stub provider).  
- **JWT access + refresh** tokens; rotation and revocation strategy documented.  
- **Optional multi-tenant:** tenant ID on users, organizations, memberships, roles.  
- **Organizational SSO:** OIDC/OAuth2 (Keycloak, Google Workspace, Okta-compatible) — implement as pluggable **IdP profiles** in config.  
- **Audit fields:** created_at, updated_at, soft-delete optional.

### 7.2 API Surface

- `/api/v1/auth/*` — login, refresh, logout, password reset.  
- `/api/v1/orgs/*`, `/api/v1/users/*` — as needed for tenant admin.  
- **Middleware:** tenant resolution from JWT claims first; reject cross-tenant access at repository layer.

### 7.3 Secrets

- JWT signing keys from environment / K8s secrets.  
- SSO client secrets never committed; `.env.example` lists keys only.

---

## 8. Documentation (`docs/`) — Full Structure

```
docs/
├── README.md                      # Index and navigation
├── getting-started/
│   ├── overview.md
│   ├── prerequisites.md
│   └── quickstart.md
├── architecture/
│   ├── modular-monolith.md
│   ├── data-model-overview.md
│   ├── auth-and-tenancy.md
│   └── ai-rag-chromadb.md
├── development/
│   ├── local-setup.md
│   ├── testing.md
│   ├── linting-and-formatting.md
│   └── database-migrations.md
├── api/
│   ├── openapi.md                 # How to export/view OpenAPI
│   └── versioning.md
├── operations/
│   ├── docker.md
│   ├── kubernetes.md
│   ├── observability.md             # Logging, metrics, tracing hooks
│   └── backups.md
├── security/
│   ├── threat-model-stub.md
│   └── secrets-management.md
├── queue/
│   └── queue-system-overview.md     # Links to queue/QUEUE_INSTRUCTIONS.md
└── optional-clients/
    ├── web.md
    └── mobile.md
```

Each file should be a **stub with a table of contents and TODO sections** where implementation will fill detail.

---

## 9. Optional Front-End and Mobile

### 9.1 Web (`apps/web/`)

- Optional **React + Vite** (or Next.js if SSR is required — document tradeoff).  
- API client generated from OpenAPI or hand-written typed client in `packages/ts-client/` (optional).  
- Environment-based API URL; no secrets in client bundle.

### 9.2 Mobile (`apps/mobile/`)

- Optional **Expo** app with secure token storage, deep links for SSO.  
- Same API contract as web; feature parity is not required for MVP.

---

## 10. Docker and Kubernetes

### 10.1 Docker

- **Multi-stage** Dockerfile for `apps/api`: builder → slim runtime.  
- Non-root user, healthcheck, `UVICORN` workers configurable.  
- `docker-compose.yml` at root: `api`, `postgres` (optional profile), `chroma` (optional profile), `redis` (optional if workers).

### 10.2 Kubernetes

- **Kustomize** base + overlays: `overlays/dev`, `staging`, `prod`.  
- Resources: `Deployment`, `Service`, `Ingress`, `HPA` (optional), `ConfigMap`, `Secret` (external-secrets compatible).  
- Probes: `/health/live`, `/health/ready` exposing DB and dependency checks.

### 10.3 Optional Cloud

- Document **portable** paths: any Kubernetes (EKS, GKE, AKS, k3s).  
- Managed Postgres (RDS, Cloud SQL, Azure Database) as **connection string** swap.  
- Object storage (S3/GCS) as optional interface for file uploads.

---

## 11. Queue System (CSV-Based Agent Work)

### 11.1 Files

| File | Role |
|------|------|
| `queue/queue.csv` | **Open** queue items; **ordered** with the **next actionable row at the top** (after header). |
| `queue/queuearchive.csv` | **Historical** items; append-only when an item is completed or cancelled. |

### 11.2 Concurrency and Discipline

- **One queue processor at a time** (human or agent). Enforce via team process; optionally add a `queue.lock` file or GitHub issue assignment for human teams.  
- Processor **reads the entire first data row** (top of queue under the header) as the single active item.  
- On completion: **append** the row to `queuearchive.csv` with completion metadata, then **remove** that row from `queue.csv`.  
- Never reorder silently; if reprioritization is needed, edit explicitly with rationale in Git commit message.

### 11.3 CSV Schema (Minimum Columns)

**Header row (exact names recommended for tooling):**

| Column | Required | Description |
|--------|----------|-------------|
| `id` | Yes | Unique identifier (UUID or monotonic `Q-2026-0001`). |
| `name` | Yes | Short human-readable title. |
| `created_date` | Yes | ISO-8601 date (UTC). |
| `category` | Yes | One of the controlled categories (see §11.4). |
| `summary` | Yes | **Elaborative** summary: goal, acceptance criteria, constraints, and definition of done. |
| `relevant_docs` | Yes | Semicolon-separated list of paths or URLs to documentation the agent must read **before** coding. |
| `relevant_files` | Yes | Semicolon-separated repo-relative paths likely touched or used as reference. |
| `batch` | No | Integer or string group identifier for coordinated multi-item efforts. |
| `phase` | No | Integer phase within a batch or roadmap. |
| `priority` | No | `P0`–`P4` or numeric. |
| `status` | Yes for archive | e.g. `done`, `cancelled`, `superseded`. |
| `completed_date` | No | ISO-8601 when archived. |
| `notes` | No | Freeform handoff notes, links to PRs. |

**Encoding:** UTF-8. **Delimiter:** comma. **Quoting:** RFC-style quoting for fields that contain commas.

### 11.4 Categories (MVP List — Small, Practical)

Use a **small** set so the queue stays scannable:

| `category` value | Description |
|------------------|-------------|
| `feature` | Implement new functionality. |
| `bugfix` | Fix incorrect behavior. |
| `test` | Add or fix automated tests, coverage, CI gates. |
| `docs` | Documentation, ADRs, comments where appropriate. |
| `refactor` | Internal quality improvement without behavior change. |
| `chore` | Tooling, deps, housekeeping. |
| `security` | Security fixes or hardening. |
| `perf` | Performance optimization. |
| `ai` | RAG, embeddings, prompts, model integration. |
| `ops` | Docker, K8s, deploy pipelines, observability. |

### 11.5 `queue/QUEUE_INSTRUCTIONS.md` (Contents Outline)

Must include:

1. Purpose of the queue vs GitHub Issues.  
2. How to add a row (copy-paste template, validation rules).  
3. How processing works (single active item, top row).  
4. How to archive and required fields in archive.  
5. Git workflow: branch naming, PR requirement, linking PR URL in `notes`.  
6. Conflict resolution if two writers edit `queue.csv`.

### 11.6 `queue/QUEUE_AGENT_PROMPT.md` (Behavior Contract)

The agent prompt must instruct the executor to:

1. **Open** `queue/QUEUE_INSTRUCTIONS.md` and comply.  
2. **Read** the header row and the **first data row** of `queue/queue.csv` in full.  
3. **Read** every path in `relevant_docs` and **review** every path in `relevant_files`.  
4. **Restate** the task and acceptance criteria from `summary` before starting work.  
5. **Execute** the work on a dedicated branch; open a PR; update `notes` if policy allows.  
6. On success: **move** the row to `queuearchive.csv` with `status`, `completed_date`, and PR link; remove from `queue.csv`.  
7. If blocked: append `notes` with blocker and do not remove the row; or move to archive with `status=cancelled` per policy.

### 11.7 Example Row (Illustrative)

```csv
id,name,created_date,category,summary,relevant_files,relevant_docs,batch,phase,priority
Q-2026-00042,"Add health readiness probe",2026-04-14T00:00:00Z,ops,"Implement /health/ready that checks PostgreSQL connectivity and returns JSON with dependency status; must pass k8s readiness probe; include tests with testcontainers or mocked DB.",docs/operations/kubernetes.md;apps/api/src/health/routes.py,docs/operations/kubernetes.md;docs/development/testing.md,rel-2026-04,2,P2
```

---

## 12. CI/CD Summary (Cross-Reference)

| Concern | CI | CD |
|---------|----|----|
| Lint / test | On every PR | — |
| Build image | On PR + main | On main/tags |
| Deploy | — | Staging auto, prod manual or tagged |
| DB migrations | Dry-run in CI | Run as job with approval |

---

## 13. Observability and Operations

- **Logging:** structured JSON logs, correlation IDs, request ID middleware.  
- **Metrics:** Prometheus metrics endpoint optional (`/metrics` behind auth or network policy).  
- **Tracing:** OpenTelemetry hooks optional.  
- **Runbooks:** `docs/operations/` with failure modes for DB, JWT, and Chroma.

---

## 14. Legal and Meta

- **License:** template should include `LICENSE` (MIT or Apache-2.0 — choose one explicitly in implementation).  
- **Contributing:** `CONTRIBUTING.md` linking to queue usage and PR rules.  
- **Code of Conduct:** optional `CODE_OF_CONDUCT.md`.

---

## 15. Implementation Checklist (For Builders)

Use this as a **definition of done** for generating the template from this spec:

- [ ] `.cursor/rules` present and aligned with stack.  
- [ ] `skills/` contains ≥25 stubs and ≥5 complete skills.  
- [ ] `.github/workflows` CI (and CD scaffold) present.  
- [ ] `apps/api` FastAPI modular monolith with health, auth stubs, tenant hooks.  
- [ ] Alembic migrations; SQLite + Postgres documented.  
- [ ] `docker-compose.yml` and `deploy/k8s` base.  
- [ ] `queue/` with `queue.csv`, `queuearchive.csv`, `QUEUE_INSTRUCTIONS.md`, `QUEUE_AGENT_PROMPT.md`.  
- [ ] `docs/` tree as §8 with stubs.  
- [ ] Optional `apps/web`, `apps/mobile` placeholders with README only.  
- [ ] ChromaDB integration stub under `packages/ai/` when AI is enabled.  
- [ ] Root `README.md` quickstart and links.

---

## 16. Document Control

| Item | Value |
|------|--------|
| **Canonical spec file** | `downloadable.md` (this file) |
| **Owners** | Repository maintainers |
| **Change process** | PR with rationale; bump version in §1 when breaking |

---

*End of specification.*
