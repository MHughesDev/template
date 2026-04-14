# Idea Definition — Project Intake Form

> **Purpose:** This is the singular input document for initializing this repository into a working project. Fill out every applicable section. The initialization agent (`prompts/repo_initializer.md`) reads this file and uses it to configure, scaffold, and wire up the entire repository machine.
>
> **How to use:** Copy this template, fill in your answers, then invoke the repo initializer prompt in Cursor. The agent will read this file, map your idea to the correct project archetype, enable the right profiles, populate the queue, and scaffold domain modules.
>
> **Rules:** Do not delete sections — mark inapplicable ones as `N/A`. The more detail you provide, the fewer assumptions the agent makes. Ambiguity here becomes ambiguity in the codebase.

---

## 1. Project identity

| Field | Your answer |
|-------|-------------|
| **Project name** | `<!-- short kebab-case name, e.g. invoice-engine -->` |
| **Display name** | `<!-- human-readable, e.g. Invoice Engine -->` |
| **One-line pitch** | `<!-- what it does in ≤15 words -->` |
| **Repository slug** | `<!-- GitHub org/repo, e.g. acme/invoice-engine -->` |

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
| **API service** | `[ ]` | Backend REST/GraphQL API. No user-facing UI. Consumed by other services or clients. |
| **Full-stack web app** | `[ ]` | Backend API + web frontend (React). Users interact via browser. |
| **Full-stack with mobile** | `[ ]` | Backend API + web + mobile (Expo/React Native). |
| **Platform / internal tool** | `[ ]` | Internal APIs, admin dashboards, data pipelines. No external consumer UI. |
| **Data pipeline / ETL** | `[ ]` | Ingestion, transformation, storage. May have API for status/triggers. |
| **AI / ML service** | `[ ]` | Model serving, RAG pipeline, embedding service. ChromaDB profile enabled. |
| **Marketplace / multi-sided** | `[ ]` | Multiple user types (buyer/seller, provider/consumer). Complex auth and tenancy. |
| **SaaS product** | `[ ]` | Multi-tenant B2B/B2C application with billing, onboarding, tenant isolation. |

**If none fit exactly:** describe your archetype below.

<!-- custom archetype description if needed -->

---

## 4. Domain model

### 4.1 Core entities

List the primary domain objects. These become database models, API resources, and bounded contexts.

| Entity | Description | Key fields | Relationships |
|--------|-------------|------------|---------------|
| `<!-- e.g. Invoice -->` | `<!-- what it represents -->` | `<!-- id, amount, status, due_date -->` | `<!-- belongs_to: Customer, has_many: LineItems -->` |
| `<!-- e.g. Customer -->` | `<!-- ... -->` | `<!-- ... -->` | `<!-- ... -->` |
| `<!-- add rows as needed -->` | | | |

### 4.2 Bounded contexts

Group entities into bounded contexts. Each context becomes a module in `apps/api/src/<context>/` with its own router, models, service, schemas, and tests.

| Context name | Entities | Description |
|-------------|----------|-------------|
| `<!-- e.g. billing -->` | `<!-- Invoice, Payment, LineItem -->` | `<!-- handles invoicing and payment processing -->` |
| `<!-- e.g. customers -->` | `<!-- Customer, Organization -->` | `<!-- customer management and profiles -->` |
| `<!-- add rows as needed -->` | | |

### 4.3 Key workflows

Describe the critical user/system workflows. These become the basis for smoke tests and queue items.

1. `<!-- e.g. "Customer creates invoice → system validates → invoice enters pending state → payment received → invoice marked paid" -->`
2. `<!-- e.g. "Admin onboards new tenant → system provisions isolated data → first user invited" -->`
3. `<!-- add as needed -->`

---

## 5. Profile selection

Enable or disable optional system profiles. The initializer uses these to scaffold files, configure Compose services, and set up deployment.

| Profile | Enable? | Notes |
|---------|---------|-------|
| **Web frontend** (React) | `[ ] yes / [ ] no` | `<!-- any framework preferences, e.g. Next.js, Vite -->` |
| **Mobile app** (Expo) | `[ ] yes / [ ] no` | `<!-- platforms: iOS, Android, both -->` |
| **Background workers** | `[ ] yes / [ ] no` | `<!-- broker preference: Redis, RabbitMQ, or defer -->` |
| **AI / RAG (ChromaDB)** | `[ ] yes / [ ] no` | `<!-- use case: search, recommendations, content gen -->` |
| **Multi-tenancy** | `[ ] yes / [ ] no` | `<!-- isolation model: row-level, schema-level, database-level -->` |
| **WebSocket / real-time** | `[ ] yes / [ ] no` | `<!-- what needs real-time: notifications, chat, live updates -->` |
| **Scheduled jobs / cron** | `[ ] yes / [ ] no` | `<!-- what runs on schedule: reports, cleanup, sync -->` |
| **File uploads / storage** | `[ ] yes / [ ] no` | `<!-- storage target: S3-compatible, local, cloud-native -->` |
| **Email / notifications** | `[ ] yes / [ ] no` | `<!-- provider preference: SMTP, SendGrid, SES, or defer -->` |
| **Search (full-text)** | `[ ] yes / [ ] no` | `<!-- engine: PostgreSQL FTS, Elasticsearch, Meilisearch -->` |
| **Billing / payments** | `[ ] yes / [ ] no` | `<!-- provider: Stripe, custom, or defer -->` |
| **Analytics / events** | `[ ] yes / [ ] no` | `<!-- what to track, where to send -->` |

---

## 6. Authentication and authorization

| Field | Your answer |
|-------|-------------|
| **Auth model** | `<!-- email/password, OAuth2/SSO, API keys, magic links, or combination -->` |
| **User types / roles** | `<!-- e.g. admin, member, viewer; or buyer, seller -->` |
| **Permission model** | `<!-- RBAC, ABAC, simple role check, or custom -->` |
| **SSO / IdP integration** | `<!-- e.g. Google, Okta, Auth0, none, defer -->` |
| **API key support** | `<!-- yes/no — for service-to-service or external developer access -->` |
| **Multi-tenant auth** | `<!-- shared user pool, tenant-scoped users, or N/A -->` |

---

## 7. Data layer

| Field | Your answer |
|-------|-------------|
| **Primary database** | `<!-- SQLite (dev/MVP) or PostgreSQL (production) — or both with migration path -->` |
| **Expected data volume** | `<!-- rows/GB estimate for first year — helps sizing decisions -->` |
| **Read/write ratio** | `<!-- e.g. 80/20 read-heavy, 50/50 balanced, 20/80 write-heavy -->` |
| **Caching needs** | `<!-- Redis, in-process, none, or defer -->` |
| **External data sources** | `<!-- APIs, feeds, imports that the system ingests -->` |
| **Data retention policy** | `<!-- how long to keep data, archival rules, or defer -->` |

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
| **API style** | `<!-- REST, GraphQL, gRPC, or hybrid -->` |
| **Versioning strategy** | `<!-- URL prefix (/v1/), header, or query param -->` |
| **Pagination style** | `<!-- cursor-based, offset-based, or keyset -->` |
| **Rate limiting** | `<!-- per-user, per-tenant, per-endpoint, global, or defer -->` |
| **OpenAPI / docs** | `<!-- auto-generated (default), custom, or both -->` |

### 9.1 Key endpoints (sketch)

List the most important API endpoints to scaffold during initialization.

| Method | Path | Description | Auth required? |
|--------|------|-------------|----------------|
| `<!-- GET -->` | `<!-- /v1/invoices -->` | `<!-- list invoices for current tenant -->` | `<!-- yes -->` |
| `<!-- POST -->` | `<!-- /v1/invoices -->` | `<!-- create new invoice -->` | `<!-- yes -->` |
| `<!-- add rows as needed -->` | | | |

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
| 1 | `<!-- e.g. core-api -->` | `<!-- e.g. "Implement Customer CRUD: models, service, router, schemas, tests. Accept criteria: all endpoints return correct status codes, tenant-scoped, integration tests pass." -->` |
| 2 | `<!-- e.g. core-api -->` | `<!-- e.g. "Implement Invoice domain: models with line items, status state machine, service layer, router, tests." -->` |
| 3 | `<!-- e.g. infrastructure -->` | `<!-- e.g. "Configure production PostgreSQL connection with connection pooling and health checks." -->` |
| `<!-- add rows -->` | | |

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

**End of idea definition.**

> After filling this out, run the repo initializer:
> 1. Open Cursor in this repository
> 2. Reference this file and `prompts/repo_initializer.md`
> 3. The agent will read `idea.md`, validate completeness, and execute the initialization procedure
> 4. Review the initialization PR for correctness before merging
