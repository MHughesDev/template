# Idea Definition — Project Intake Form

<!-- INIT_META
initialized: false
init_version: "2.0"
init_completed_at: null
init_branch: null
init_pr_url: null
init_manifest_hash: null
-->

> **Purpose:** This is the singular input document for initializing this repository into a working project. Fill out every applicable section. The initialization agent (`prompts/repo_initializer.md`) reads this file and uses it to configure, scaffold, and wire up the entire repository machine.
>
> **How to use:** Copy this template, fill in your answers, then invoke the repo initializer prompt in Cursor. The agent will read this file, map your idea to the correct project archetype, enable the right profiles, populate the queue, and scaffold domain modules.
>
> **Rules:** Do not delete sections — mark inapplicable ones as `N/A`. The more detail you provide, the fewer assumptions the agent makes. Ambiguity here becomes ambiguity in the codebase.

---

## 1. Project identity

| Field | Your answer |
|-------|-------------|
| **Project name** | `template-demo` |
| **Display name** | `Template Demo` |
| **One-line pitch** | `Demonstrates the agent-operated template repository and initialization engine.` |
| **Repository slug** | `MHughesDev/template` |

---

## 2. Problem and solution

### 2.1 Problem statement
<!-- 2–5 sentences. What pain exists today? Who feels it? What happens if it stays unsolved? -->

### 2.2 Proposed solution
<!-- 2–5 sentences. How does this project solve the problem? What is the core mechanism? -->

### 2.3 Success criteria
<!-- Measurable outcomes that prove the solution works. Be specific. -->

- [ ] `<!-- e.g. "API processes 100 invoices/min at p99 < 200ms" -->`
- [ ] `<!-- e.g. "Multi-tenant isolation verified by integration tests" -->`
- [ ] `<!-- e.g. "User can register, login, and perform core action end-to-end" -->`

---

## 3. Project archetype

Pick **one** primary archetype. The initializer uses this to select default modules, middleware, deployment shape, and queue categories.

| Archetype | Select | Description |
|-----------|--------|-------------|
| **API service** | `[x]` | Backend REST/GraphQL API. No user-facing UI. Consumed by other services or clients. |
| **Full-stack web app** | `[ ]` | Backend API + web frontend (React). Users interact via browser. |
| **Full-stack with mobile** | `[ ]` | Backend API + web + mobile (Expo/React Native). |
| **Platform / internal tool** | `[ ]` | Internal APIs, admin dashboards, data pipelines. No external consumer UI. |
| **Data pipeline / ETL** | `[ ]` | Ingestion, transformation, storage. May have API for status/triggers. |
| **AI / ML service** | `[ ]` | Model serving, RAG pipeline, embedding service. ChromaDB profile enabled. |
| **Marketplace / multi-sided** | `[ ]` | Multiple user types (buyer/seller, provider/consumer). Complex auth and tenancy. |
| **SaaS product** | `[ ]` | Multi-tenant B2B/B2C application with billing, onboarding, tenant isolation. |

**If none fit exactly:** describe your archetype below.

N/A — a listed archetype was selected.

---

## 4. Domain model

### 4.1 Core entities

List the primary domain objects. These become database models, API resources, and bounded contexts.

| Entity | Description | Key fields | Relationships |
|--------|-------------|------------|---------------|
| DemoRecord | Sample entity for template validation | id, label, timestamps | Standalone for CI |

### 4.2 Bounded contexts

Group entities into bounded contexts. Each context becomes a module in `apps/api/src/<context>/` with its own router, models, service, schemas, and tests.

| Context name | Entities | Description |
|-------------|----------|-------------|
| demo | DemoRecord | Demonstrates bounded-context scaffolding for the template repository. |

### 4.3 Key workflows

Describe the critical user/system workflows. These become the basis for smoke tests and queue items.

1. Client calls health and authenticated CRUD endpoints on the demo module; tests assert status codes and persistence.
2. N/A for template smoke scope.
3. N/A.

---

## 5. Profile selection

Enable or disable optional system profiles. The initializer uses these to scaffold files, configure Compose services, and set up deployment.

| Profile | Enable? | Notes |
|---------|---------|-------|
| **Web frontend** (React) | `[x] no` | Template default: API-only. |
| **Mobile app** (Expo) | `[x] no` | Template default: API-only. |
| **Background workers** | `[x] no` | Enable when Celery/Redis is required. |
| **AI / RAG (ChromaDB)** | `[x] no` | Optional Chroma profile. |
| **Multi-tenancy** | `[x] no` | Use TenantMixin when product needs isolation. |
| **WebSocket / real-time** | `[x] no` | Optional realtime module. |
| **Scheduled jobs / cron** | `[x] no` | Optional APScheduler profile. |
| **File uploads / storage** | `[x] no` | Optional S3/local storage package. |
| **Email / notifications** | `[x] no` | Optional notifications package. |
| **Search (full-text)** | `[x] no` | Optional Meilisearch or FTS. |
| **Billing / payments** | `[x] no` | Optional Stripe integration. |
| **Analytics / events** | `[x] no` | Optional analytics env flags. |

---

## 6. Authentication and authorization

| Field | Your answer |
|-------|-------------|
| **Auth model** | JWT access tokens with email/password registration (template default). |
| **User types / roles** | Registered user; admin role deferred. |
| **Permission model** | Authenticated vs anonymous for MVP; RBAC later. |
| **SSO / IdP integration** | Deferred — add when product requires SSO. |
| **API key support** | Deferred for MVP. |
| **Multi-tenant auth** | N/A until multi-tenancy profile is enabled. |

---

## 7. Data layer

| Field | Your answer |
|-------|-------------|
| **Primary database** | SQLite for local development and CI. Optional containerized relational database for production parity is documented under deployment (use the `db` Compose profile). |
| **Expected data volume** | Small — template and demo data only until product launch. |
| **Read/write ratio** | Read-heavy for API demos; exact ratio TBD per product. |
| **Caching needs** | In-process first; Redis when workers profile is enabled. |
| **External data sources** | None for template bootstrap. |
| **Data retention policy** | Default SQLite file lifecycle; formal policy when product ships. |

---

## 8. Integrations and external services

List every external system this project will communicate with.

| Service | Direction | Protocol | Purpose | Required for MVP? |
|---------|-----------|----------|---------|-------------------|
| `<!-- e.g. Stripe -->` | `<!-- outbound -->` | `<!-- REST API -->` | `<!-- payment processing -->` | `<!-- yes/no -->` |
| `<!-- e.g. SendGrid -->` | `<!-- outbound -->` | `<!-- REST API -->` | `<!-- transactional email -->` | `<!-- no — defer -->` |
| `<!-- e.g. Webhook receiver -->` | `<!-- inbound -->` | `<!-- HTTP webhook -->` | `<!-- payment status updates -->` | `<!-- yes -->` |
| `<!-- add rows as needed -->` | | | | |

---

## 9. API design

| Field | Your answer |
|-------|-------------|
| **API style** | REST JSON over HTTP (FastAPI). |
| **Versioning strategy** | URL prefix `/api/v1/` (configurable via `API_PREFIX`). |
| **Pagination style** | Cursor-based for list endpoints where needed; offset for small demos. |
| **Rate limiting** | Deferred — enable `RATE_LIMITING_ENABLED` when exposing public internet. |
| **OpenAPI / docs** | Auto-generated OpenAPI and Swagger when `API_DEBUG=true`. |

### 9.1 Key endpoints (sketch)

List the most important API endpoints to scaffold during initialization.

| Method | Path | Description | Auth required? |
|--------|------|-------------|----------------|
| GET | `/api/v1/demo/` | List demo records | yes |
| POST | `/api/v1/demo/` | Create demo record | yes |
| GET | `/api/v1/demo/{id}` | Fetch demo record | yes |

---

## 10. Non-functional requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Availability** | `<!-- e.g. 99.9% -->` | |
| **Latency (p95)** | `<!-- e.g. < 200ms for API responses -->` | |
| **Throughput** | `<!-- e.g. 1000 req/s peak -->` | |
| **Scalability** | `<!-- horizontal, vertical, or specific plan -->` | |
| **Compliance** | `<!-- GDPR, SOC2, HIPAA, PCI-DSS, none, or defer -->` | |
| **Data residency** | `<!-- regions, or no constraint -->` | |
| **Backup RPO** | `<!-- e.g. 1 hour, 24 hours, or defer -->` | |
| **Backup RTO** | `<!-- e.g. 4 hours, 1 hour, or defer -->` | |

---

## 11. Deployment and infrastructure

| Field | Your answer |
|-------|-------------|
| **Target environment** | `<!-- local-only, single VPS, Kubernetes, cloud-managed, or defer -->` |
| **Cloud provider** | `<!-- AWS, GCP, Azure, Hetzner, self-hosted, or cloud-agnostic -->` |
| **Container registry** | `<!-- GHCR, ECR, Docker Hub, or defer -->` |
| **Domain / DNS** | `<!-- e.g. api.myproject.com, or defer -->` |
| **TLS / certificates** | `<!-- Let's Encrypt, cloud-managed, or defer -->` |
| **CI/CD beyond GitHub Actions** | `<!-- any additional CD tooling, or default is fine -->` |

---

## 12. Initial queue items

Seed the queue with the first batch of work items. These become the initialization batch in `queue/queue.csv`.

| Priority | Category | Summary |
|----------|----------|---------|
| 1 | core-api | Implement the `demo` bounded context end-to-end: SQLAlchemy model with UUID primary key, repository, service, Pydantic schemas, FastAPI router with list/create/get, and pytest coverage including 401/404 paths. Acceptance: all routes return documented status codes; `make test` passes; no raw SQL in routers. Definition of done: router registered under `api_prefix`, migration or metadata create_all verified in CI. |
| 2 | infrastructure | Add optional PostgreSQL smoke test job documentation and verify `docker compose --profile db up` works with asyncpg `DATABASE_URL`. Acceptance: connection health check passes against the container; pool settings documented in `docs/architecture/data-layer.md`. |
| 3 | testing | Raise coverage floor incrementally: add integration tests for auth edge cases and tenant middleware when multi-tenancy is enabled. Acceptance: coverage ratchet target met; no flaky tests in CI. |

---

## 13. Constraints and non-goals

### 13.1 Hard constraints
<!-- Things that absolutely must be true. List as bullet points. -->

- `<!-- e.g. "Must run on Python 3.12+ — no earlier versions" -->`
- `<!-- e.g. "Must not store PII in logs" -->`
- `<!-- e.g. "All API responses must include correlation ID header" -->`

### 13.2 Non-goals (explicit exclusions)
<!-- Things this project will NOT do, at least not in initial scope. -->

- `<!-- e.g. "No admin UI in first release" -->`
- `<!-- e.g. "No support for legacy API clients" -->`
- `<!-- e.g. "No real-time features until post-MVP" -->`

---

## 14. Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `<!-- e.g. "Complex tenant isolation logic" -->` | `<!-- high/med/low -->` | `<!-- high/med/low -->` | `<!-- e.g. "Use TenantMixin with mandatory test coverage" -->` |
| `<!-- e.g. "Third-party API rate limits" -->` | `<!-- med -->` | `<!-- med -->` | `<!-- e.g. "Implement circuit breaker per skill" -->` |
| `<!-- add rows as needed -->` | | | |

---

## 15. Timeline and phasing (optional)

If you have phases in mind, describe them. The initializer can map these to queue batches.

| Phase | Milestone | Scope |
|-------|-----------|-------|
| 1 — MVP | `<!-- e.g. "Core API with auth and primary domain" -->` | `<!-- entities, endpoints, features -->` |
| 2 — Beta | `<!-- e.g. "Add web frontend, email notifications" -->` | `<!-- profiles to enable, features to add -->` |
| 3 — GA | `<!-- e.g. "Production hardening, monitoring, scale" -->` | `<!-- non-functional requirements, compliance -->` |

---

## 16. Open questions

List anything you are unsure about. The initialization agent will flag these for human resolution before proceeding with those areas.

1. `<!-- e.g. "Should invoices support multiple currencies?" -->`
2. `<!-- e.g. "What is the billing provider — Stripe or custom?" -->`
3. `<!-- add as needed -->`

---

## 17. Additional context

Attach or link any additional context: wireframes, ERDs, existing API docs, competitor references, design docs, Slack threads.

<!-- paste links, descriptions, or inline content here -->

---

## 18. Initialization log

> This section is auto-populated by `make idea:execute`. Do not edit manually.

| Field              | Value |
| ------------------ | ----- |
| Status             | `not initialized` |
| Manifest version   | — |
| Executed at        | — |
| Profiles enabled   | — |
| Contexts scaffolded| — |
| Queue rows seeded  | — |
| Init PR            | — |

---

**End of idea definition.**

> After filling this out, run the repo initializer:
> 1. Open Cursor in this repository
> 2. Reference this file and `prompts/repo_initializer.md`
> 3. The agent will read `idea.md`, validate completeness, and execute the initialization procedure
> 4. Review the initialization PR for correctness before merging
