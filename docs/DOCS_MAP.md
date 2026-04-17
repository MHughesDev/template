---
doc_id: "0"
title: "Documentation Map"
section: "Root"
summary: "Canonical index of every documentation file in this repository."
updated: "2026-04-20"
---

# 0 — Documentation Map

Authoritative index of all documentation under `docs/`. Every doc appears here with its stable ID, path, and one-sentence purpose. Reference docs by `doc_id` in PRs, queue rows, commits, and handoffs.

## 0.1 How to use

- Reference any doc by `doc_id` — never by filename alone.
- Adding a new doc: pick the next free `N.M` in its section, add frontmatter, add a row here.
- Removing a doc: move its row to the retired table below; do not reuse the number.
- Moving a doc: keep the same `doc_id`; update the Path column only.

## 0.2 Sections

### Section 1 — Getting Started

Purpose: Orient new contributors and agents: tools, clone-to-green paths, and quickstart.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 1.0 | Getting Started overview | `docs/getting-started/README.md` | Getting started index. Links to prerequisites and quickstart. |
| 1.1 | prerequisites | `docs/getting-started/prerequisites.md` | Required tools and versions. Python 3.12+, Docker, Make/Task, Git. |
| 1.2 | quickstart | `docs/getting-started/quickstart.md` | Step-by-step from clone to running dev server with passing tests. |

### Section 2 — Architecture

Purpose: Explains system design: contexts, data layer, auth, APIs, errors, and optional AI/RAG.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 2.0 | Architecture overview | `docs/architecture/README.md` | Architecture documentation index. |
| 2.1 | ai rag chromadb | `docs/architecture/ai-rag-chromadb.md` | AI/RAG architecture with ChromaDB: embedding strategy, retrieval pipeline, kill switch, provider abstraction (§13). |
| 2.2 | api design | `docs/architecture/api-design.md` | API design decisions: style, versioning, pagination, rate limiting, error handling conventions. Populated from `idea.md` §9. |
| 2.3 | auth multi tenancy | `docs/architecture/auth-multi-tenancy.md` | Authentication and multi-tenancy architecture: JWT flow, token lifecycle, tenant isolation, SSO extension points (§14). |
| 2.4 | data layer | `docs/architecture/data-layer.md` | Data layer architecture: SQLite for dev/constrained MVP, PostgreSQL for production, migration strategy. |
| 2.5 | Diagrams overview | `docs/architecture/diagrams/README.md` | Index for Mermaid/PlantUML architecture diagram sources. Optional per spec §26.12 item 399. |
| 2.6 | domain model | `docs/architecture/domain-model.md` | Domain model documentation. Entity definitions, relationships, bounded context map. Populated from `idea.md` §4. |
| 2.7 | error handling | `docs/architecture/error-handling.md` | Cross-cutting error handling strategy. |
| 2.8 | modular monolith | `docs/architecture/modular-monolith.md` | Modular monolith design: bounded contexts, contract boundaries, data ownership, extraction criteria (§12). |
| 2.9 | system context | `docs/architecture/system-context.md` | System context diagram and description. Shows the system boundary, external actors, and integrations. Populated from `idea.md` §8. |

### Section 3 — Development

Purpose: Covers local setup, coding standards, testing, env vars, git flow, and doc generation.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 3.0 | Development overview | `docs/development/README.md` | Index of developer documentation: setup, workflow, testing, and standards. |
| 3.1 | coding standards | `docs/development/coding-standards.md` | Python and API coding standards for this repository (typing, style, security). |
| 3.2 | dependency management | `docs/development/dependency-management.md` | How Python dependencies are declared, upgraded, and reviewed in this repo. |
| 3.3 | docs generation | `docs/development/docs-generation.md` | How the docs pipeline works and how to extend it. |
| 3.4 | environment vars | `docs/development/environment-vars.md` | Environment variable reference. All vars documented with defaults, read by `apps/api/src/config.py` via Pydantic Settings (§10.3). |
| 3.5 | git workflow | `docs/development/git-workflow.md` | Git branching, PR workflow, and review expectations for this repository. |
| 3.6 | Init manifest schema | `docs/development/init-manifest-schema.md` | Defines init-manifest.json fields produced from idea.md for deterministic initialization. |
| 3.7 | local setup | `docs/development/local-setup.md` | Detailed local development setup. All Make/Task targets documented with expected behavior (§10.1). |
| 3.8 | module patterns | `docs/development/module-patterns.md` | How to structure bounded-context modules under `apps/api/src/` (router, service, models, tests). |
| 3.9 | testing guide | `docs/development/testing-guide.md` | Pytest layout, markers, async tests, and coverage expectations for the API. |

### Section 4 — API

Purpose: Indexes HTTP API surface: route catalog, error codes, and how docs stay in sync.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 4.0 | Api overview | `docs/api/README.md` | API documentation index. |
| 4.1 | endpoints | `docs/api/endpoints.md` | API endpoint catalog. Auto-generated or manually maintained list of all routes with request/response schemas. |
| 4.2 | error codes | `docs/api/error-codes.md` | Error code taxonomy. Stable codes with descriptions, HTTP status mappings, and client handling guidance. |

### Section 5 — Procedures

Purpose: Canonical agent SOPs: queue work, implementation, validation, init, migrations, and PRs.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 5.0 | Procedures overview | `docs/procedures/README.md` | Procedures index. Lists all SOPs with one-line descriptions and links. These are canonical workflows written for agents first, usable by... |
| 5.1 | add make target | `docs/procedures/add-make-target.md` | Standard procedure for adding a new canonical command to the Makefile. |
| 5.10 | extract service from monolith | `docs/procedures/extract-service-from-monolith.md` | SOP for extract-service-from-monolith. |
| 5.11 | handle blocked work | `docs/procedures/handle-blocked-work.md` | SOP: Document blockers, escalate, optionally requeue lower items. |
| 5.12 | handoff | `docs/procedures/handoff.md` | SOP: Complete handoff — files changed, commands run, results, risks, follow-ups. |
| 5.13 | implement change | `docs/procedures/implement-change.md` | SOP: Execute code changes in small validated increments with commits that tell a story. |
| 5.14 | incident rollback | `docs/procedures/incident-rollback.md` | SOP for incident-rollback. |
| 5.15 | Initialize from idea | `docs/procedures/initialize-from-idea.md` | Runs structured repository initialization from idea.md using the initialization engine. |
| 5.16 | initialize repo | `docs/procedures/initialize-repo.md` | SOP for initializing the repo from idea.md. The canonical procedure that the repo_initializer prompt follows. Turns a blank template into... |
| 5.17 | open pull request | `docs/procedures/open-pull-request.md` | SOP: Create PR with title, description template, evidence, labels, queue linkage. |
| 5.18 | plan change | `docs/procedures/plan-change.md` | SOP: Create implementation plan with acceptance criteria, file impact, risks, scope bounds. |
| 5.19 | release preparation | `docs/procedures/release-preparation.md` | SOP for release-preparation. |
| 5.2 | Add an MCP Tool | `docs/procedures/add-mcp-tool.md` | Adds MCP tools by exposing FastAPI routes that surface as OpenAPI-derived MCP tools. |
| 5.20 | scaffold domain module | `docs/procedures/scaffold-domain-module.md` | SOP for scaffold-domain-module. |
| 5.21 | start queue item | `docs/procedures/start-queue-item.md` | SOP: Claim top queue row, create branch, read relevant docs. |
| 5.22 | update documentation | `docs/procedures/update-documentation.md` | SOP: When and how to update docs alongside code changes. |
| 5.23 | update or create rule | `docs/procedures/update-or-create-rule.md` | SOP: Rule lifecycle — creating new .cursor/rules or updating existing ones. |
| 5.24 | update or create skill | `docs/procedures/update-or-create-skill.md` | SOP: Skill lifecycle — creating new skills or updating existing ones to the standard format. |
| 5.25 | validate change | `docs/procedures/validate-change.md` | SOP: Run full validation matrix before opening PR. |
| 5.26 | validate idea md | `docs/procedures/validate-idea-md.md` | SOP for validate-idea-md. |
| 5.3 | add optional app profile | `docs/procedures/add-optional-app-profile.md` | SOP for add-optional-app-profile. |
| 5.4 | add prompt template | `docs/procedures/add-prompt-template.md` | SOP for add-prompt-template. |
| 5.5 | add queue category | `docs/procedures/add-queue-category.md` | SOP for add-queue-category. |
| 5.6 | archive queue item | `docs/procedures/archive-queue-item.md` | SOP: Move completed queue row to archive with required fields, then update GitHub (merge PR + delete branch). |
| 5.7 | database migration | `docs/procedures/database-migration.md` | SOP for database-migration. |
| 5.8 | dependency upgrade | `docs/procedures/dependency-upgrade.md` | SOP for dependency-upgrade. |
| 5.9 | enable profile | `docs/procedures/enable-profile.md` | SOP for enable-profile. |

### Section 6 — Operations

Purpose: Run and scale the system: Docker, Kubernetes, health, backups, observability, rollback.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 6.0 | Operations overview | `docs/operations/README.md` | Operations documentation index. |
| 6.1 | backups | `docs/operations/backups.md` | Backup and restore procedures for databases and persistent volumes. |
| 6.2 | configuration | `docs/operations/configuration.md` | Operations configuration reference: how config flows from env vars through Pydantic settings to application code. |
| 6.3 | database operations | `docs/operations/database-operations.md` | Database operations: VACUUM, indexes, pool tuning, slow queries. |
| 6.4 | docker | `docs/operations/docker.md` | Docker operations: building images, running containers, Compose profiles, troubleshooting. |
| 6.5 | health checks | `docs/operations/health-checks.md` | Health check documentation: endpoint contracts, probe configuration, dependency checks, degraded states. |
| 6.6 | kubernetes | `docs/operations/kubernetes.md` | Kubernetes operations: manifest rendering, deployment, scaling, monitoring. |
| 6.7 | observability | `docs/operations/observability.md` | Observability setup: structured logging, metrics, tracing, dashboards (§21). |
| 6.8 | rollback | `docs/operations/rollback.md` | Rollback and forward-fix decision tree. When to rollback vs fix-forward, procedures for each (§2). |
| 6.9 | scaling | `docs/operations/scaling.md` | Scaling playbook: horizontal pod autoscaling, workers, cache. |

### Section 7 — ADR

Purpose: Records architecture decisions: template, status, and the decision index.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 7.0 | Adr overview | `docs/adr/README.md` | ADR index. Lists all decisions with status. |
| 7.1 | template | `docs/adr/template.md` | ADR template for new decisions. |

### Section 8 — Agents

Purpose: Defines human supervision of agents: review, quality gates, and incident-driven policy.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 8.0 | Agents overview | `docs/agents/README.md` | Agent supervision documentation index (§9.3). |
| 8.1 | evolving from incidents | `docs/agents/evolving-from-incidents.md` | How to evolve rules/skills/prompts from incidents: post-incident analysis → artifact updates. |
| 8.2 | initialization guide | `docs/agents/initialization-guide.md` | Guide for the initialization process: what `idea.md` is, how to fill it out, what the initializer does, what to review in the initializat... |
| 8.3 | pr audit checklist | `docs/agents/pr-audit-checklist.md` | Checklist for auditing a PR against acceptance criteria. |
| 8.4 | quality ratcheting | `docs/agents/quality-ratcheting.md` | How to ratchet quality over time: increasing coverage floors, adding rules, tightening procedures. |
| 8.5 | reviewing ai diffs | `docs/agents/reviewing-ai-diffs.md` | How to review AI-generated diffs: security focus, tenant isolation, scope validation, test adequacy. |
| 8.6 | supervision guide | `docs/agents/supervision-guide.md` | How a human maintainer supervises agent work: monitoring, intervention triggers, review cadence. |

### Section 9 — Optional Clients

Purpose: Documents optional web and mobile profiles: enablement, setup, and operational cost.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 9.1 | mobile | `docs/optional-clients/mobile.md` | mobile profile documentation: when to enable, setup, env vars, operational burden. |
| 9.2 | web | `docs/optional-clients/web.md` | web profile documentation: when to enable, setup, env vars, operational burden. |

### Section 10 — Prompts

Purpose: Describes prompt library conventions, metadata, and the prompt index.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 10.0 | Prompts overview | `docs/prompts/README.md` | Prompt library conventions, metadata format, how to add templates (§7.1, §7.2). |
| 10.1 | conventions | `docs/prompts/conventions.md` | Detailed prompt authoring conventions: placeholder syntax, context injection, output formatting. |
| 10.2 | index | `docs/prompts/index.md` | Auto-generated or manually maintained index of all prompt templates with metadata summaries. |

### Section 11 — Quality

Purpose: Defines testing strategy, coverage floors, and flaky-test policy.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 11.0 | Quality overview | `docs/quality/README.md` | Quality documentation index. |
| 11.1 | coverage policy | `docs/quality/coverage-policy.md` | Coverage floor definition and ratcheting mechanism. |
| 11.2 | flake policy | `docs/quality/flake-policy.md` | Flaky test policy — detection, quarantine, fix SLA, and root cause tracking. |
| 11.3 | testing strategy | `docs/quality/testing-strategy.md` | Testing strategy — pyramid, what to test at each level, when to add tests, and coverage policy. |

### Section 12 — Queue

Purpose: Explains the CSV queue: categories, lifecycle, and intelligence concepts.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 12.1 | queue categories | `docs/queue/queue-categories.md` | Registry of valid queue categories with descriptions, validation rules, and examples. |
| 12.2 | queue intelligence | `docs/queue/queue-intelligence.md` | Conceptual documentation for the queue intelligence layer: DAG, complexity, batching, conflict detection. |
| 12.3 | queue system overview | `docs/queue/queue-system-overview.md` | Queue system conceptual overview: purpose, lifecycle, single-lane semantics, tooling. |

### Section 13 — Release

Purpose: Covers versioning, promotion, and changelog practices for releases.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 13.0 | Release overview | `docs/release/README.md` | Release documentation index. |
| 13.1 | changelog guide | `docs/release/changelog-guide.md` | How to maintain the changelog: format (Keep a Changelog), automation, release notes. |
| 13.2 | promotion | `docs/release/promotion.md` | Release promotion path: dev → staging → prod with gates and verification (§11.3). |
| 13.3 | versioning | `docs/release/versioning.md` | Versioning strategy: semver, when to bump major/minor/patch, pre-release conventions. |

### Section 14 — Repo Governance

Purpose: Covers audits, freshness, improvement loops, and procedure drift detection.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 14.0 | Repo Governance overview | `docs/repo-governance/README.md` | Repo governance documentation index (§20). |
| 14.1 | audits | `docs/repo-governance/audits.md` | Scheduled repository self-audits using `make audit:self` — what is checked, how to interpret results, and how to remediate failures. |
| 14.2 | documentation freshness | `docs/repo-governance/documentation-freshness.md` | Keeping docs current — staleness indicators, `make docs:check`, and the quarterly review process. |
| 14.3 | improvement loops | `docs/repo-governance/improvement-loops.md` | Post-task retrospectives and encoding learnings into durable artifacts — skills, rules, procedures, and queue items. |
| 14.4 | procedure drift detection | `docs/repo-governance/procedure-drift-detection.md` | Detecting and fixing drift between documented procedures and the actual CI/operations reality. |

### Section 15 — Runbooks

Purpose: Holds operational runbooks for outages, DB failures, JWT rotation, and Chroma.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 15.0 | Runbooks overview | `docs/runbooks/README.md` | Runbooks index. |
| 15.1 | api down | `docs/runbooks/api-down.md` | Runbook: API service is down or unresponsive (§21). |
| 15.2 | chroma unavailable | `docs/runbooks/chroma-unavailable.md` | Runbook: ChromaDB unavailable — graceful degradation via kill switch. |
| 15.3 | db failure | `docs/runbooks/db-failure.md` | Runbook: Database failure or connectivity loss. |
| 15.4 | jwt key rotation | `docs/runbooks/jwt-key-rotation.md` | Runbook: JWT signing key rotation procedure. |

### Section 16 — Security

Purpose: Covers threat model, secrets, CORS, tokens, incidents, and accepted risks.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 16.0 | Security overview | `docs/security/README.md` | Security documentation index. |
| 16.1 | accepted risks | `docs/security/accepted-risks.md` | Accepted CVEs and review dates; links to dependency audit. |
| 16.2 | cors policy | `docs/security/cors-policy.md` | CORS origins and security rationale. |
| 16.3 | incident response | `docs/security/incident-response.md` | Incident response plan: classification, evidence capture, communication, remediation, post-incident (§2). |
| 16.4 | secrets management | `docs/security/secrets-management.md` | How secrets are managed: sourcing (env vars only), rotation procedures, CI/CD injection, never in code. |
| 16.5 | threat model stub | `docs/security/threat-model-stub.md` | Generic threat model for FastAPI applications built on this template. Identifies assets, threat actors, attack surfaces, and mitigations.... |
| 16.6 | token lifecycle | `docs/security/token-lifecycle.md` | JWT token lifecycle details: issuance parameters, refresh windows, revocation mechanism, key rotation (§14). |

### Section 17 — Troubleshooting

Purpose: Lists common development issues and fixes.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 17.0 | Troubleshooting overview | `docs/troubleshooting/README.md` | Troubleshooting index. |
| 17.1 | common issues | `docs/troubleshooting/common-issues.md` | Common development issues and solutions. |

### Section 18 — Root

Purpose: Hub entry and ubiquitous language: the docs index and domain glossary.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 18.0 | Docs overview | `docs/README.md` | Documentation hub. Index of all doc sections with one-line descriptions and links. |
| 18.1 | glossary | `docs/glossary.md` | Ubiquitous language and domain glossary. Defines terms used consistently across spec, code, and documentation. |

### Section 19 — BRAINSTORM

Purpose: Read-only ideation; one brainstorm file holds the whole idea and typically maps to **many** queue rows.

| ID | Title | Path | Summary |
| --- | --- | --- | --- |
| 19.0 | BRAINSTORM overview | `docs/BRAINSTORM/README.md` | Read-only ideation space; one brainstorm file is the whole idea and may spawn many queue rows. |
| 19.1 | BRAINSTORM agent contract | `docs/BRAINSTORM/AGENTS.md` | Scoped agent rules for docs/BRAINSTORM: read-only vs code; one idea file maps to many queue items. |
| 19.2 | Pipeline brainstorm to queue | `docs/BRAINSTORM/PIPELINE-from-brainstorm-to-queue.md` | Steps from a ready brainstorm to many queue rows, then code, then spec and docs alignment. |
| 19.3 | Brainstorm idea files | `docs/BRAINSTORM/ideas/README.md` | One Markdown file per whole idea; implementation splits into many queue rows via the pipeline. |
| 19.4 | Brainstorm template | `docs/BRAINSTORM/TEMPLATE-brainstorm.md` | Structured template for one whole idea; expect many queue rows and list them in section 10. |

## 0.3 Retired IDs

| ID | Original title | Retired date | Reason |
| --- | --- | --- | --- |

## 0.4 Invariants enforced by `make docs:map-check`

- Every `.md` file under `docs/` except `DOCS_MAP.md` and files under `docs/generated/` has `doc_id` frontmatter.
- No two files share a `doc_id`.
- Every `doc_id` in this map points to an existing file.
- Every doc file has exactly one row in this map.
- Retired IDs do not appear as active entries.

## 0.5 Machine-generated outputs (no stable doc_id)

These files live under `docs/generated/` and are overwritten by `make docs:generate`. They are validated by `make docs:check` and intentionally omit `doc_id` frontmatter.

- `docs/generated/cursor-rules.md`
- `docs/generated/docker-compose.md`
- `docs/generated/k8s-base.md`
- `docs/generated/make-targets.md`
- `docs/generated/migrations.md`
- `docs/generated/settings-fields.md`
