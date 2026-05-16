# skills/init/initialize-repo.md

<!-- CROSS-REFERENCES -->
<!-- - Related procedure: docs/procedures/initialize-repo.md -->
<!-- - Related prompt: prompts/repo_initializer.md -->
<!-- - Invoked after: skills/init/idea-validator.md -->
<!-- - Produces input for: skills/init/queue-seeder.md -->
<!-- - Phase 1 methodology: skills/repo-governance/architecture-design.md -->
<!-- - Rule: .cursor/rules/initialization.md -->

**Purpose:** Transform a completed `idea.md` into a fully documented project blueprint by writing every project-specific architecture, API, data, security, operations, and testing document. This skill produces documentation only — no application code, no migrations, no tests. The queue-seeder skill runs after this one and derives queue items from the docs produced here.

---

## When to Invoke

- `idea.md` is fully filled out (all 17 sections, no HTML comment placeholders)
- `make idea:validate` passes
- All placeholder docs under `docs/` show `status: pending-init`
- No prior initialization has run (`INIT_META initialized: false` in `idea.md`)

Do not invoke if any of the following are true:
- `make idea:validate` fails — fix it first
- `idea.md` §16 contains open questions that block architectural decisions — resolve or explicitly accept them first
- `INIT_META initialized: true` — initialization has already run; use a queue item to update specific docs instead

---

## Prerequisites

- `idea.md` read completely, every section understood
- `make idea:validate` passing
- `docs/` placeholder files all present (`status: pending-init`)
- Understanding of the existing module pattern in `apps/api/src/example/`

---

## What This Skill Does NOT Do

- Does not write application code (`router.py`, `service.py`, `models.py`, etc.)
- Does not create or run database migrations
- Does not write tests
- Does not seed the queue — that is the queue-seeder skill's job
- Does not modify `queue/queue.csv` directly
- Does not run `make` commands other than `make docs:check` at the end

---

## The Six Documentation Phases

Work through these phases in order. Each phase has a named output file. Do not skip phases. Do not write to a later phase's files until the current phase is complete.

---

### Phase 1 — Architectural Reasoning (no file output)

Before writing anything, reason through the full system as a software architect. Think through and resolve:

1. **What is this system fundamentally?** Summarize the problem and solution in two sentences from `idea.md` §2.
2. **What archetype best describes it?** Confirm the §3 selection is coherent with the domain described in §4. Flag any mismatch.
3. **What are the true bounded contexts?** Read `idea.md` §4.2 carefully. For each context: what does it own, what does it NOT own, how does it communicate with other contexts? Look for hidden contexts — workflows in §4.3 that don't fit cleanly into the listed contexts.
4. **What are the real entities?** For each entity in §4.2: what fields does it actually need (not just id/label), what enum fields exist, what are the FK relationships and their cardinality, what cascade rules are appropriate?
5. **What workflows don't map to simple CRUD?** From §4.3, identify every workflow that requires more than a single create/update/delete. These become named service methods.
6. **What auth decisions does the domain actually require?** From §6: what is the permission model, what resources are public vs protected vs admin-only, does multi-tenancy affect auth?
7. **Which profiles are actually needed?** Cross-reference §5 selections against the domain described. If a profile is checked but the domain has no use case for it, note the discrepancy. If a domain workflow clearly requires a profile that isn't checked, note it.
8. **What are the open questions?** From §16: classify each as (a) blocks architecture, (b) blocks implementation but not architecture, or (c) non-blocking. Only (a) requires stopping — surface it and do not proceed until resolved.

Write down your conclusions before proceeding to Phase 2. These conclusions drive every subsequent phase.

---

### Phase 2 — Architecture Documents

Write to each file in this order. Each file must be complete before moving to the next.

#### `docs/architecture/overview.md`
Replace the pending-init placeholder body with:
- **System purpose** (2–3 sentences from §2)
- **Archetype** — name it, explain why it fits this domain
- **Component map** — Mermaid diagram showing the major components and how they connect: API, DB, each bounded context module, and any active profiles (workers, AI/RAG, etc.)
- **Primary data flow** — narrative description of the most important request path end-to-end (e.g. "a user submits an order → orders service validates → creates DB record → enqueues confirmation task → returns 201")
- **Key design decisions** — 3–5 bullet points on the most significant architectural choices and why they were made for this domain specifically

Update frontmatter: change `status: "pending-init"` to `status: "current"` and set `updated` to today's date.

#### `docs/architecture/bounded-contexts.md`
For each bounded context identified in Phase 1:
- **Context name** and the module path it maps to (`apps/api/src/<name>/`)
- **Owns:** the entities it is the single source of truth for
- **Does not own:** entities from other contexts it may read but never writes
- **Exposes:** the service methods and API endpoints it provides
- **Consumes:** what it needs from other contexts (via packages/contracts/ only, never direct import)
- **Workflows:** the named business operations this context is responsible for

Include a Mermaid context map diagram showing context boundaries and inter-context dependencies.

Update frontmatter status to `"current"`.

#### `docs/architecture/data-model.md`
For every entity across all bounded contexts:
- **Table name** and which bounded context owns it
- **Fields:** name, Python/SQLAlchemy type, nullable, default, any constraints
- **Enums:** all enum fields with every valid value defined
- **Relationships:** FK targets, cardinality (one-to-many, many-to-many), cascade rules, lazy vs eager loading decision
- **Indexes:** which fields are indexed and what query pattern each index serves

Include a Mermaid ER diagram covering all entities.

This document is the source of truth. `models.py` files must match it exactly. Flag any conflict.

Update frontmatter status to `"current"`.

#### `docs/architecture/auth.md`
- **Strategy chosen** (JWT, OAuth, API key, or combination) and why it fits the domain
- **Token lifecycle** — how tokens are issued, their TTL, how they are refreshed, how they are revoked
- **Permission model** — roles defined, scopes if applicable, how permissions are checked in code (via `Depends()`)
- **Endpoint access matrix** — for every route group: public / authenticated / role-required
- **Multi-tenancy intersection** — if multi-tenancy is enabled, how tenant isolation is enforced in the auth layer

Update frontmatter status to `"current"`.

#### `docs/architecture/frontend.md`
If web profile is enabled:
- **Page inventory** — every page/route, its purpose, and what data it needs
- **Component hierarchy** — top-level layout, shared components, page-specific components
- **API integration** — which endpoints each page calls, how auth tokens are managed in the client
- **State management** — approach chosen and why

If web profile is NOT enabled, replace body with:
```
Not applicable — no web frontend profile enabled for this project.
```

Update frontmatter status to `"current"`.

#### `docs/architecture/mobile.md`
If mobile profile is enabled:
- **Screen inventory** — every screen, its purpose, navigation relationships
- **Navigation structure** — tab structure, stack navigators, deep link patterns
- **Auth and token storage** — where tokens are stored on device, refresh flow
- **Offline behavior** — what works offline, what requires connectivity

If mobile profile is NOT enabled:
```
Not applicable — no mobile profile enabled for this project.
```

Update frontmatter status to `"current"`.

#### `docs/architecture/async-workers.md`
If workers profile is enabled:
- **Task inventory** — every Celery task: name, trigger (which service method dispatches it), payload schema, expected duration
- **Retry policy** — max retries, backoff strategy, dead letter behavior per task
- **Idempotency** — how each task ensures safe re-execution
- **Failure handling** — how failures surface (logging, alerting, DLQ)

If workers profile is NOT enabled:
```
Not applicable — no workers profile enabled for this project.
```

Update frontmatter status to `"current"`.

#### `docs/architecture/ai-rag.md`
If AI/RAG profile is enabled:
- **Ingestion pipeline** — what data is ingested, when, and how (batch vs real-time)
- **Embedding strategy** — model used, chunk size, refresh schedule
- **Retrieval approach** — similarity threshold, top-k, hybrid search if applicable
- **Model provider** — which provider, which abstraction layer, how to swap
- **Kill switch** — what `AI_KILL_SWITCH=true` disables and how to activate it

If AI/RAG profile is NOT enabled:
```
Not applicable — no AI/RAG profile enabled for this project.
```

Update frontmatter status to `"current"`.

#### `docs/architecture/multi-tenancy.md`
If multi-tenancy is enabled:
- **Isolation model** — row-level security or schema-per-tenant, and why
- **Tenant context propagation** — how tenant ID is extracted from the request and passed through the stack
- **Shared vs isolated data** — which tables are global, which are tenant-scoped
- **Tenant provisioning** — how a new tenant is created and initialized

If NOT enabled:
```
Not applicable — multi-tenancy not enabled for this project.
```

Update frontmatter status to `"current"`.

#### `docs/architecture/billing.md`
If billing profile is enabled:
- **Payment provider** — which provider and why
- **Webhook handling** — endpoint path, signature verification, idempotency key
- **Subscription model** — plans, pricing, upgrade/downgrade behavior
- **Failure and retry** — what happens on payment failure, retry schedule, dunning

If NOT enabled:
```
Not applicable — no billing profile enabled for this project.
```

Update frontmatter status to `"current"`.

---

### Phase 3 — API Documents

#### `docs/api/endpoints.md`
For every endpoint across all bounded contexts, grouped by context:
- **Method and path** (e.g. `POST /api/v1/orders/`)
- **Auth requirement** (public / authenticated / role: admin)
- **Request schema** — body fields with types and validation rules
- **Response schema** — fields returned with types
- **Error codes** — which error codes this endpoint can return (reference `docs/api/error-codes.md`)
- **Example** — one realistic request and response pair per endpoint

Update frontmatter status to `"current"`.

#### `docs/api/error-codes.md`
Define the complete error taxonomy for this project:
- **Error code** (e.g. `ORDER_NOT_FOUND`)
- **HTTP status** (e.g. 404)
- **Message** — the message returned in the response body
- **When it occurs** — the specific condition that triggers it
- **How to resolve** — guidance for API consumers

Cover all domain errors identified in Phase 1 workflows, plus standard auth errors.

Update frontmatter status to `"current"`.

#### `docs/api/versioning.md`
- **Current version** and base path (e.g. `v1`, `/api/v1/`)
- **Versioning policy** — what constitutes a breaking change requiring a version bump
- **Deprecation policy** — how long deprecated versions are supported
- **Migration guide** — empty for now, will be populated when v2 is introduced

Update frontmatter status to `"current"`.

---

### Phase 4 — Data Documents

#### `docs/data/schema.md`
Narrative description of the physical database schema:
- For each table: its purpose in plain language, the most important fields, why it is structured the way it is
- Key relationships between tables and the join patterns they enable
- Index rationale — for each index, what query it optimizes and why that query is important for this domain

Update frontmatter status to `"current"`.

#### `docs/data/migrations.md`
Project-specific migration SOP:
- **Create a migration:** exact command (`make migrate:create MESSAGE="..."`)
- **Review checklist:** what to verify before applying (reversible?, data-safe?, index strategy?)
- **Apply:** `make migrate` — environments and order
- **Rollback:** exact alembic command and any data considerations
- **CI behavior:** how migration dry-run runs in CI for this project

Update frontmatter status to `"current"`.

#### `docs/data/seeding.md`
- **What `make db-seed` creates** — list of records created per entity
- **Purpose** — what state it establishes (e.g. admin user, demo data, reference data)
- **Safe environments** — local and CI only; never production
- **Reset and re-seed** — `make db-reset && make db-seed`

Update frontmatter status to `"current"`.

---

### Phase 5 — Security, Operations, and Testing Documents

Write these in parallel — they do not depend on each other.

#### `docs/security/overview.md`
- **Attack surface** — what is exposed given the archetype and enabled profiles
- **Controls in place** — auth, input validation, secrets management, CORS policy, rate limiting (if applicable)
- **Out of scope** — what is explicitly not handled and why
- **Where to find detail** — links to `auth.md`, `threat-model.md`, `secrets-management.md`

Update frontmatter status to `"current"`.

#### `docs/security/threat-model.md`
For this project's archetype and data:
- **Top threats** — the 3–5 most likely attack vectors
- **Mitigation** — what is in place for each
- **Accepted risks** — residual risks accepted with rationale
- **Out of scope** — threats not addressed and why

Update frontmatter status to `"current"`.

#### `docs/operations/deployment.md`
- **Environments** — local, staging, production (or whichever apply)
- **Deploy steps** — ordered procedure per environment
- **Post-deploy verification** — what to check after each deploy (`make health:check`, smoke tests)
- **Failed deploy** — how to detect and what to do

Update frontmatter status to `"current"`.

#### `docs/operations/monitoring.md`
- **What is instrumented** — which endpoints, which async tasks, which DB operations
- **Alerts** — what conditions trigger alerts and at what thresholds
- **First-look checklist** — when something breaks, in what order do you check things
- **Dashboards** — what exists and where

Update frontmatter status to `"current"`.

#### `docs/operations/runbooks/incident-response.md`
For the 3–4 most likely failure modes given this project's archetype and profiles, write a scenario section for each:
- **Detection** — what signals indicate this failure
- **Immediate actions** — first 5 minutes
- **Investigation steps** — how to diagnose root cause
- **Resolution** — how to fix and verify

Update frontmatter status to `"current"`.

#### `docs/operations/runbooks/rollback.md`
- **Application rollback** — exact steps to revert to the previous deploy
- **Migration rollback** — `alembic downgrade -1` and data considerations
- **Worker drain** — how to drain the task queue safely before a rollback

Update frontmatter status to `"current"`.

#### `docs/testing/strategy.md`
- **Unit tests** — what is unit-tested, which bounded contexts have the most complex logic requiring deep unit coverage
- **Integration tests** — what is integration-tested, the test DB setup
- **Smoke tests** — which endpoints are smoke-tested on every deploy
- **Domain-specific concerns** — any testing challenges specific to this project (async workflows, external APIs, multi-tenant isolation)
- **Coverage floor** — the minimum set in `pyproject.toml`

Update frontmatter status to `"current"`.

#### `docs/testing/coverage.md`
- **Overall floor** — the `fail_under` value in `pyproject.toml`
- **Per-module targets** — if some contexts are more critical and require higher coverage
- **Excluded modules** — what is excluded from coverage measurement and why
- **Ratchet policy** — the floor only moves up, never down; how it is enforced

Update frontmatter status to `"current"`.

---

### Phase 6 — ADR and Development Reference

#### `docs/adr/0001-initial-architecture.md`
Record every significant architectural decision made during initialization:
- **Archetype decision** — chosen archetype, alternatives considered, why this one
- **Profile decisions** — each enabled profile, what domain need drove it
- **Auth strategy** — chosen strategy, alternatives, rationale
- **Database choice** — SQLite vs PostgreSQL decision, rationale, trade-offs accepted
- **Bounded context boundaries** — how the domain was decomposed and any non-obvious boundary decisions
- **Constraints accepted** — anything from `idea.md` §13 that shaped the architecture

Format each decision as:
```
## Decision: [Title]
**Status:** Accepted
**Context:** [why a decision was needed]
**Decision:** [what was decided]
**Rationale:** [why]
**Trade-offs:** [what was given up]
```

Update frontmatter status to `"current"`.

#### `docs/development/commands.md`
List every `make` target that is relevant to this project. For each:
- Target name
- What it does
- When to use it
- Any required variables (e.g. `MESSAGE=`, `MODULE=`)

Group by: dev workflow, testing, database, queue, CI/release, profiles.

Update frontmatter status to `"current"`.

#### `docs/development/ci.md`
- **Pipeline stages in order** with what each checks
- **Matrix** — if multiple DB backends or Python versions are tested
- **Reproduce locally** — the exact local command sequence that mirrors CI
- **Common CI failures** — the 3–4 most frequent failures and how to fix them

Update frontmatter status to `"current"`.

---

## Validation Checklist

Run this before handing off to the queue-seeder skill:

- [ ] All 25 placeholder files have `status: "current"` in frontmatter (not `pending-init`)
- [ ] `docs/architecture/data-model.md` contains every entity from `idea.md` §4.2 with real fields (not just id/label)
- [ ] `docs/api/endpoints.md` has an entry for every workflow identified in `idea.md` §4.3
- [ ] `docs/api/error-codes.md` covers every domain error identified across all workflows
- [ ] Every conditional doc (frontend, mobile, async-workers, ai-rag, multi-tenancy, billing) either has real content or the standard "Not applicable" note
- [ ] `docs/adr/0001-initial-architecture.md` records every significant decision with rationale
- [ ] Run `make docs:check` — must pass
- [ ] No doc still contains the `> **Pending initialization.**` blockquote

---

## Handoff Expectations

When this skill completes:
- All 25 project-specific docs are written and status is `"current"`
- `make docs:check` passes
- A summary of the architectural decisions made is ready to pass to the queue-seeder skill, which will use the docs as the source of truth for generating queue items
- The next skill to invoke is `skills/init/queue-seeder.md`

## Related Procedures

`docs/procedures/initialize-repo.md` — the full SOP this skill is part of

## Related Prompts

`prompts/repo_initializer.md`

## Related Rules

`.cursor/rules/initialization.md`, `.cursor/rules/documentation.md`
