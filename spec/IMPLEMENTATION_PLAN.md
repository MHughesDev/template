# Implementation plan — spec checklist
This file is the **implementation checklist** for the template repository described in [`spec/spec.md`](./spec.md). The spec folder is the **source of truth** for policy and structure; this plan enumerates **folders and files** to create so the repository matches the spec (including §26–§28 and the §29 tree).

## How to use
- Check each box when the path exists on disk **and** meets the spec (stubs must include required headings per §26).
- **Optional** items are marked; include them when the relevant profile or feature is enabled.
- The root [`spec.md`](../spec.md) file is a short pointer to the canonical spec.

## Phases

### Phase 1 — Specification and root control plane
**Milestone 1.1 — Spec and policy surface**
- [x] Confirm `spec/spec.md` is the canonical copy; root `spec.md` points to it.
- [x] Add `AGENTS.md` per §4 (all required sections).
- [x] Add `README.md`, `CONTRIBUTING.md`, `LICENSE`, optional `CODE_OF_CONDUCT.md`.
- [x] Add `idea.md`, `CHANGELOG.md` per §27–§28.

### Phase 2 — Machine control layer
**Milestone 2.1 — Cursor rules and commands**
- [x] Create `.cursor/rules/` (global, apps-api, security, queue, initialization, skills, prompts; recommended testing + documentation).
- [x] Create `.cursor/commands/` (initialize, scaffold-module, audit; optional validate, queue-next).

### Phase 3 — Prompts, skills, and procedures
**Milestone 3.1 — Agent libraries**
- [x] Populate `prompts/` including `repo_initializer.md` and role templates per §7.3 and §28.
- [x] Populate `skills/` including `skills/init/` machinery and §6 coverage categories.
- [x] Populate `docs/procedures/` per §8.2 plus initialization procedures in §28.

### Phase 4 — Documentation tree
**Milestone 4.1 — Conceptual and operational docs**
- [x] Create `docs/` subtrees: getting-started, architecture, development, api, operations, security, adr, agents, prompts index, runbooks, release, repo-governance, quality, queue, optional-clients.

### Phase 5 — Queue and GitHub
**Milestone 5.1 — Orchestration and CI/CD**
- [x] Create `queue/` CSV files and queue SOPs; optional `queue.lock` and `audit.log`.
- [x] Add `.github/workflows/` (ci, cd, security), templates, CODEOWNERS, dependabot.

### Phase 6 — Backend, packages, deploy
**Milestone 6.1 — Runnable API + infra**
- [x] Implement `apps/api/` FastAPI monolith with health + auth + tenancy stubs and tests.
- [x] Add `packages/contracts`, `packages/tasks`, optional `packages/ai`.
- [x] Add `deploy/docker`, `deploy/k8s` overlays; optional `apps/web` and `apps/mobile` placeholders.

### Phase 7 — Automation scripts and Makefile
**Milestone 7.1 — Canonical commands**
- [x] Add `scripts/` backing every Make target per §10.2 and §28.6 (including init, idea validation, inventory).
- [x] Wire `Makefile` or Taskfile with minimum catalog + initialization targets (§28.8).
- [x] Add `pyproject.toml`, `.env.example`, `docker-compose.yml`.

### Phase 8 — Validation and governance
**Milestone 8.1 — Definition of done**
- [x] Meet §24 checklist: CI stages, `queue:validate`, `audit:self`, security scans, release docs.
- [x] Run `make inventory:check` (or equivalent) against this checklist.

---

## Folder checklist
| Created | Path | Notes |
|:-------:|------|-------|
| [x] | `/` (repo root) | Top-level control plane and configuration. Contains `AGENTS.md`, `spec/spec.md` (canonical spec), optional root `spec.md` pointer, `idea.md`, `README.md`, `Makefile`, `pyproject.toml`, `docker-compose.yml`, `.env.example`, `CHANGELOG.md`, and legal files. Everything an agent or human needs to orient and begin work. |
| [x] | `.cursor/` | Machine-control layer for Cursor IDE. Houses persistent rules and reusable commands that shape agent behavior during development sessions. |
| [x] | `.cursor/rules/` | Always-on and path-scoped constraints. Global rules apply everywhere; path-scoped rules activate only in matching directories. Agents load these automatically. Includes initialization, skills, and prompts rules. |
| [x] | `.cursor/commands/` | Reusable Cursor command definitions. Shortcuts that invoke canonical scripts or document exact command sequences. Includes initialization, scaffolding, and audit commands. |
| [x] | `prompts/` | Reusable, versioned prompt templates for recurring agent roles. Each template has metadata (purpose, inputs, outputs, linked procedures/skills) and a prompt body with placeholders. Includes the master `repo_initializer` prompt. |
| [x] | `skills/` | Executable playbooks organized by category. Each skill has a `.md` playbook and may include supporting code (machinery) for automation, validation, and generation. |
| [x] | `skills/init/` | Initialization skills and machinery. Used during repo initialization from `idea.md`: validation, archetype mapping, module scaffolding, queue seeding, profile resolution, env generation. |
| [x] | `skills/agent-ops/` | Skills for agent-specific operations: queue triage, task planning, handoffs, blocked recovery, prompt promotion, rule refinement, auditing. Includes Python machinery for queue analysis, handoff generation, and self-audit. |
| [x] | `skills/repo-governance/` | Skills for maintaining the repository machine: writing `AGENTS.md`, authoring rules, maintaining procedures, writing ADRs, changelogs, hygiene. Includes machinery for rule linting, docs freshness checking, and ADR index generation. |
| [x] | `skills/backend/` | Skills for backend/platform development: FastAPI patterns, service layers, health endpoints, API versioning, background jobs, configuration, logging, metrics, tracing, rate limiting, migrations. Includes machinery for module scaffolding, error code registry, env var sync, and OpenAPI diffing. |
| [x] | `skills/security/` | Skills for security and compliance: secret handling, token lifecycle, RBAC/tenant isolation, dependency review, code/image scanning, SBOM, incident evidence. Includes machinery for secret scanning, dependency auditing, and tenant isolation checking. |
| [x] | `skills/testing/` | Skills for testing and quality: pytest conventions, async testing, contract testing, snapshots, smoke tests, regression, load testing, flaky triage, validation loops. Includes machinery for test scaffolding, coverage ratcheting, and flaky detection. |
| [x] | `skills/devops/` | Skills for DevOps and operations: Docker builds, Compose profiles, K8s probes, rollout/rollback, GitHub Actions, release promotion, artifact publishing, env config, backup/restore. Includes machinery for Dockerfile linting, K8s manifest validation, and Compose profile testing. |
| [x] | `skills/ai-rag/` | Skills for AI/RAG operations (optional profile): ChromaDB ingestion, embedding refresh, retrieval evaluation, prompt versioning, kill switch, provider abstraction, safety review. |
| [x] | `skills/frontend/` | Skills for optional frontend/mobile profiles: generated clients, React API integration, Expo auth storage, frontend env handling. |
| [x] | `docs/` | Documentation hub. All conceptual and operational documentation organized by subsystem. Every major subsystem has both a conceptual explanation (why) and an operational explanation (how). |
| [x] | `docs/getting-started/` | Onboarding documentation: prerequisites, quickstart from clone to running dev server with passing tests. |
| [x] | `docs/architecture/` | Architecture documentation: modular monolith design, data layer strategy, auth/multi-tenancy, AI/RAG architecture, system context, domain model, API design. |
| [x] | `docs/development/` | Development documentation: local setup with all Make targets, coding standards, testing guide, env var reference, module patterns, dependency management. |
| [x] | `docs/api/` | API documentation: endpoint catalog, error code taxonomy. |
| [x] | `docs/operations/` | Operations documentation: Docker, Kubernetes, observability, backups, rollback, configuration, health checks. |
| [x] | `docs/security/` | Security documentation: threat model, secrets management, incident response, token lifecycle. |
| [x] | `docs/procedures/` | Standard Operating Procedures. Canonical workflows written for agents first, usable by humans. Includes initialization, scaffolding, profile enablement, and idea validation procedures alongside all original SOPs. |
| [x] | `docs/adr/` | Architecture Decision Records. Index of all architectural decisions with template for new ones. |
| [x] | `docs/agents/` | Agent supervision documentation for human maintainers: initialization guide, supervision, review AI diffs, audit PRs, ratchet quality, evolve from incidents. |
| [x] | `docs/prompts/` | Prompt library documentation: conventions, metadata format, authoring guide, index of all templates. |
| [x] | `docs/runbooks/` | Operational runbooks for specific failure scenarios: API down, DB failure, JWT key rotation, ChromaDB unavailable. |
| [x] | `docs/release/` | Release documentation: versioning strategy, promotion path (dev → staging → prod), changelog guide. |
| [x] | `docs/repo-governance/` | Repository governance documentation: improvement loops, audits, procedure drift detection, documentation freshness. |
| [x] | `docs/quality/` | Quality documentation: testing strategy, coverage policy and floors, flaky test policy. |
| [x] | `docs/queue/` | Queue system documentation: conceptual overview of the CSV-based agent work orchestration system, queue category registry. |
| [x] | `docs/optional-clients/` | Documentation for optional application profiles (web, mobile): when to enable, setup, operational burden. |
| [x] | `queue/` | Agent work orchestration lane. CSV-based queue with strict lifecycle, single-lane processing, audit logging, and validation tooling. |
| [x] | `.github/` | GitHub repository management: CI/CD workflows, issue templates, PR template, code ownership, dependency management, labels. |
| [x] | `.github/workflows/` | GitHub Actions workflow definitions: CI (lint, typecheck, test, build, scan), CD (deploy through environments), security scanning. |
| [x] | `.github/ISSUE_TEMPLATE/` | GitHub issue templates: structured forms for bug reports, feature requests, and queue items. |
| [x] | `apps/` | Application code. Contains the primary API and optional frontend/mobile profiles. Each app may have its own scoped `AGENTS.md`. |
| [x] | `apps/api/` | FastAPI modular monolith — the primary application. Health endpoints, auth stubs, tenant hooks, Alembic migrations, Docker build, tests. |
| [x] | `apps/api/alembic/` | Database migration configuration and version scripts (Alembic). |
| [x] | `apps/api/alembic/versions/` | Individual migration version files. Starts with `.gitkeep`; populated as schema evolves. |
| [x] | `apps/api/src/` | API application source code organized by bounded context (health, auth, tenancy). |
| [x] | `apps/api/src/health/` | Health module: health, readiness, and liveness endpoints for operational monitoring and K8s probes. |
| [x] | `apps/api/src/auth/` | Authentication module: register, login, refresh, logout endpoints with JWT token management. Policy-complete stubs with extension points. |
| [x] | `apps/api/src/tenancy/` | Multi-tenancy module: tenant context middleware, tenant models, query scoping mixin. |
| [x] | `apps/api/tests/` | API test suite: health endpoint tests, auth endpoint tests, shared fixtures and configuration. |
| [x] | `apps/web/` | Optional web frontend placeholder. Contains README and scoped AGENTS.md when profile is enabled. |
| [x] | `apps/mobile/` | Optional mobile app placeholder. Contains README and scoped AGENTS.md when profile is enabled. |
| [x] | `packages/` | Shared packages used across bounded contexts and applications. Contracts, task interfaces, AI interfaces. |
| [x] | `packages/contracts/` | Shared Pydantic models and OpenAPI schemas. The contract layer for the modular monolith — backward compatibility is mandatory. |
| [x] | `packages/tasks/` | Background task interfaces. Abstract base classes for task submission and handling. Workers are an optional profile. |
| [x] | `packages/ai/` | AI/RAG interfaces (optional profile). Provider-agnostic abstractions for embedding, retrieval, and generation with ChromaDB implementation. |
| [x] | `deploy/` | Deployment configuration for Docker and Kubernetes. |
| [x] | `deploy/docker/` | Docker-specific deployment documentation and configurations. |
| [x] | `deploy/k8s/` | Kubernetes manifests organized with Kustomize: base resources and environment-specific overlays. |
| [x] | `deploy/k8s/base/` | Base Kubernetes manifests: Deployment, Service, ConfigMap, Kustomization. Shared across all environments. |
| [x] | `deploy/k8s/overlays/` | Environment-specific Kustomize overlays that patch base manifests for dev, staging, and production. |
| [x] | `deploy/k8s/overlays/dev/` | Dev environment overlay: single replica, debug settings, relaxed resource limits. |
| [x] | `deploy/k8s/overlays/staging/` | Staging environment overlay: production-like configuration at lower scale. |
| [x] | `deploy/k8s/overlays/prod/` | Production environment overlay: full scale, strict settings, pod disruption budgets. |
| [x] | `scripts/` | Shell script implementations backing Makefile targets. The execution layer for all canonical commands including initialization and scaffolding. |
| [x] | `.devcontainer/` | Dev container configuration for reproducible development environments (VS Code / Codespaces). |
| [x] | `docs/troubleshooting/` | Common development issues and their solutions (index + curated fixes). |
| [x] | `docs/architecture/diagrams/` | Architecture diagram source files (optional Mermaid/PlantUML). |
| [x] | `monitoring/` | Observability configuration files (recommended local stack overlay). |
| [x] | `monitoring/prometheus/` | Prometheus configuration and alert rules. |
| [x] | `monitoring/grafana/` | Grafana configuration and dashboard provisioning. |
| [x] | `monitoring/grafana/dashboards/` | Exportable Grafana dashboard JSON files. |
| [x] | `.github/actions/` | Reusable composite GitHub Actions (optional). |
| [x] | `.github/actions/setup-python/` | Composite action: Python setup with caching. |
| [x] | `.github/actions/docker-build/` | Composite action: Docker build with layer caching. |

---
## File checklist
| Created | Path | Notes |
|:-------:|------|-------|
| [x] | `.bandit.yml` |  |
| [x] | `.cursor/commands/audit.md` |  |
| [x] | `.cursor/commands/initialize.md` |  |
| [x] | `.cursor/commands/queue-next.md` | optional |
| [x] | `.cursor/commands/scaffold-module.md` |  |
| [x] | `.cursor/commands/validate.md` | optional |
| [x] | `.cursor/rules/apps-api.md` |  |
| [x] | `.cursor/rules/documentation.md` | recommended |
| [x] | `.cursor/rules/global.md` |  |
| [x] | `.cursor/rules/initialization.md` |  |
| [x] | `.cursor/rules/prompts.md` |  |
| [x] | `.cursor/rules/queue.md` |  |
| [x] | `.cursor/rules/security.md` |  |
| [x] | `.cursor/rules/skills.md` |  |
| [x] | `.cursor/rules/testing.md` | recommended |
| [x] | `.cursorignore` |  |
| [x] | `.devcontainer/devcontainer.json` |  |
| [x] | `.dockerignore` |  |
| [x] | `.editorconfig` |  |
| [x] | `.env.example` |  |
| [x] | `.envrc` | optional |
| [x] | `.gitattributes` |  |
| [x] | `.github/CODEOWNERS` |  |
| [x] | `.github/ISSUE_TEMPLATE/bug_report.md` |  |
| [x] | `.github/ISSUE_TEMPLATE/feature_request.md` |  |
| [x] | `.github/ISSUE_TEMPLATE/queue_item.md` | recommended |
| [x] | `.github/PULL_REQUEST_TEMPLATE.md` |  |
| [x] | `.github/actions/docker-build/action.yml` | optional |
| [x] | `.github/actions/setup-python/action.yml` | optional |
| [x] | `.github/dependabot.yml` |  |
| [x] | `.github/labels.yml` | recommended |
| [x] | `.github/release.yml` |  |
| [x] | `.github/workflows/cd.yml` |  |
| [x] | `.github/workflows/ci.yml` |  |
| [x] | `.github/workflows/label-sync.yml` | optional |
| [x] | `.github/workflows/security.yml` |  |
| [x] | `.github/workflows/stale.yml` | optional |
| [x] | `.gitignore` |  |
| [x] | `.mailmap` | optional |
| [x] | `.pre-commit-config.yaml` |  |
| [x] | `.python-version` |  |
| [x] | `.trivyignore` |  |
| [x] | `AGENTS.md` |  |
| [x] | `CHANGELOG.md` |  |
| [x] | `CODEBASE_SUMMARY.md` | optional |
| [x] | `CODE_OF_CONDUCT.md` | optional |
| [x] | `CONTRIBUTING.md` |  |
| [x] | `LICENSE` |  |
| [x] | `Makefile` |  |
| [x] | `NOTICE` | optional |
| [x] | `README.md` |  |
| [x] | `SECURITY.md` |  |
| [x] | `apps/api/AGENTS.md` |  |
| [x] | `apps/api/Dockerfile` |  |
| [x] | `apps/api/alembic.ini` |  |
| [x] | `apps/api/alembic/env.py` |  |
| [x] | `apps/api/alembic/script.py.mako` |  |
| [x] | `apps/api/alembic/versions/.gitkeep` |  |
| [x] | `apps/api/src/__init__.py` |  |
| [x] | `apps/api/src/auth/__init__.py` |  |
| [x] | `apps/api/src/auth/dependencies.py` |  |
| [x] | `apps/api/src/auth/models.py` |  |
| [x] | `apps/api/src/auth/router.py` |  |
| [x] | `apps/api/src/auth/schemas.py` |  |
| [x] | `apps/api/src/auth/service.py` |  |
| [x] | `apps/api/src/config.py` |  |
| [x] | `apps/api/src/database.py` |  |
| [x] | `apps/api/src/dependencies.py` |  |
| [x] | `apps/api/src/events.py` | optional |
| [x] | `apps/api/src/exceptions.py` |  |
| [x] | `apps/api/src/health/__init__.py` |  |
| [x] | `apps/api/src/health/router.py` |  |
| [x] | `apps/api/src/main.py` |  |
| [x] | `apps/api/src/middleware.py` |  |
| [x] | `apps/api/src/pagination.py` |  |
| [x] | `apps/api/src/tenancy/__init__.py` |  |
| [x] | `apps/api/src/tenancy/middleware.py` |  |
| [x] | `apps/api/src/tenancy/models.py` |  |
| [x] | `apps/api/tests/__init__.py` |  |
| [x] | `apps/api/tests/conftest.py` |  |
| [x] | `apps/api/tests/factories.py` |  |
| [x] | `apps/api/tests/test_auth.py` |  |
| [x] | `apps/api/tests/test_health.py` |  |
| [x] | `apps/api/tests/test_tenancy.py` |  |
| [x] | `apps/mobile/AGENTS.md` | optional |
| [x] | `apps/mobile/README.md` | optional |
| [x] | `apps/web/AGENTS.md` | optional |
| [x] | `apps/web/README.md` | optional |
| [x] | `deploy/docker/README.md` |  |
| [x] | `deploy/k8s/README.md` |  |
| [x] | `deploy/k8s/base/configmap.yaml` |  |
| [x] | `deploy/k8s/base/deployment.yaml` |  |
| [x] | `deploy/k8s/base/hpa.yaml` |  |
| [x] | `deploy/k8s/base/ingress.yaml` |  |
| [x] | `deploy/k8s/base/kustomization.yaml` |  |
| [x] | `deploy/k8s/base/networkpolicy.yaml` |  |
| [x] | `deploy/k8s/base/service.yaml` |  |
| [x] | `deploy/k8s/base/serviceaccount.yaml` |  |
| [x] | `deploy/k8s/overlays/dev/kustomization.yaml` |  |
| [x] | `deploy/k8s/overlays/prod/kustomization.yaml` |  |
| [x] | `deploy/k8s/overlays/staging/kustomization.yaml` |  |
| [x] | `docker-compose.test.yml` | optional |
| [x] | `docker-compose.yml` |  |
| [x] | `docs/README.md` |  |
| [x] | `docs/adr/README.md` |  |
| [x] | `docs/adr/template.md` |  |
| [x] | `docs/agents/README.md` |  |
| [x] | `docs/agents/evolving-from-incidents.md` |  |
| [x] | `docs/agents/initialization-guide.md` |  |
| [x] | `docs/agents/pr-audit-checklist.md` |  |
| [x] | `docs/agents/quality-ratcheting.md` |  |
| [x] | `docs/agents/reviewing-ai-diffs.md` |  |
| [x] | `docs/agents/supervision-guide.md` |  |
| [x] | `docs/api/README.md` |  |
| [x] | `docs/api/endpoints.md` |  |
| [x] | `docs/api/error-codes.md` |  |
| [x] | `docs/api/openapi-baseline.json` | optional |
| [x] | `docs/architecture/README.md` |  |
| [x] | `docs/architecture/ai-rag-chromadb.md` | optional |
| [x] | `docs/architecture/api-design.md` |  |
| [x] | `docs/architecture/auth-multi-tenancy.md` |  |
| [x] | `docs/architecture/data-layer.md` |  |
| [x] | `docs/architecture/diagrams/README.md` | optional |
| [x] | `docs/architecture/domain-model.md` |  |
| [x] | `docs/architecture/error-handling.md` | optional |
| [x] | `docs/architecture/modular-monolith.md` |  |
| [x] | `docs/architecture/system-context.md` |  |
| [x] | `docs/development/README.md` |  |
| [x] | `docs/development/coding-standards.md` |  |
| [x] | `docs/development/dependency-management.md` |  |
| [x] | `docs/development/docs-generation.md` |  |
| [x] | `docs/development/environment-vars.md` |  |
| [x] | `docs/development/git-workflow.md` |  |
| [x] | `docs/development/local-setup.md` |  |
| [x] | `docs/development/module-patterns.md` |  |
| [x] | `docs/development/testing-guide.md` |  |
| [x] | `docs/getting-started/README.md` |  |
| [x] | `docs/getting-started/prerequisites.md` |  |
| [x] | `docs/getting-started/quickstart.md` |  |
| [x] | `docs/glossary.md` |  |
| [x] | `docs/operations/README.md` |  |
| [x] | `docs/operations/backups.md` |  |
| [x] | `docs/operations/configuration.md` |  |
| [x] | `docs/operations/database-operations.md` | optional |
| [x] | `docs/operations/docker.md` |  |
| [x] | `docs/operations/health-checks.md` |  |
| [x] | `docs/operations/kubernetes.md` |  |
| [x] | `docs/operations/observability.md` |  |
| [x] | `docs/operations/rollback.md` |  |
| [x] | `docs/operations/scaling.md` | optional |
| [x] | `docs/optional-clients/mobile.md` | optional |
| [x] | `docs/optional-clients/web.md` | optional |
| [x] | `docs/procedures/README.md` |  |
| [x] | `docs/procedures/add-optional-app-profile.md` |  |
| [x] | `docs/procedures/add-prompt-template.md` |  |
| [x] | `docs/procedures/add-queue-category.md` |  |
| [x] | `docs/procedures/archive-queue-item.md` |  |
| [x] | `docs/procedures/database-migration.md` |  |
| [x] | `docs/procedures/dependency-upgrade.md` |  |
| [x] | `docs/procedures/enable-profile.md` |  |
| [x] | `docs/procedures/extract-service-from-monolith.md` |  |
| [x] | `docs/procedures/handle-blocked-work.md` |  |
| [x] | `docs/procedures/handoff.md` |  |
| [x] | `docs/procedures/implement-change.md` |  |
| [x] | `docs/procedures/incident-rollback.md` |  |
| [x] | `docs/procedures/initialize-repo.md` |  |
| [x] | `docs/procedures/open-pull-request.md` |  |
| [x] | `docs/procedures/plan-change.md` |  |
| [x] | `docs/procedures/release-preparation.md` |  |
| [x] | `docs/procedures/scaffold-domain-module.md` |  |
| [x] | `docs/procedures/start-queue-item.md` |  |
| [x] | `docs/procedures/update-documentation.md` |  |
| [x] | `docs/procedures/update-or-create-rule.md` |  |
| [x] | `docs/procedures/update-or-create-skill.md` |  |
| [x] | `docs/procedures/validate-change.md` |  |
| [x] | `docs/procedures/validate-idea-md.md` |  |
| [x] | `docs/prompts/README.md` |  |
| [x] | `docs/prompts/conventions.md` |  |
| [x] | `docs/prompts/index.md` |  |
| [x] | `docs/quality/README.md` |  |
| [x] | `docs/quality/coverage-policy.md` |  |
| [x] | `docs/quality/flake-policy.md` |  |
| [x] | `docs/quality/testing-strategy.md` |  |
| [x] | `docs/queue/queue-categories.md` |  |
| [x] | `docs/queue/queue-intelligence.md` |  |
| [x] | `docs/queue/queue-system-overview.md` |  |
| [x] | `docs/release/README.md` |  |
| [x] | `docs/release/changelog-guide.md` |  |
| [x] | `docs/release/promotion.md` |  |
| [x] | `docs/release/versioning.md` |  |
| [x] | `docs/repo-governance/README.md` |  |
| [x] | `docs/repo-governance/audits.md` |  |
| [x] | `docs/repo-governance/documentation-freshness.md` |  |
| [x] | `docs/repo-governance/improvement-loops.md` |  |
| [x] | `docs/repo-governance/procedure-drift-detection.md` |  |
| [x] | `docs/runbooks/README.md` |  |
| [x] | `docs/runbooks/api-down.md` |  |
| [x] | `docs/runbooks/chroma-unavailable.md` | optional |
| [x] | `docs/runbooks/db-failure.md` |  |
| [x] | `docs/runbooks/jwt-key-rotation.md` |  |
| [x] | `docs/security/README.md` |  |
| [x] | `docs/security/accepted-risks.md` |  |
| [x] | `docs/security/cors-policy.md` | optional |
| [x] | `docs/security/incident-response.md` |  |
| [x] | `docs/security/secrets-management.md` |  |
| [x] | `docs/security/threat-model-stub.md` |  |
| [x] | `docs/security/token-lifecycle.md` |  |
| [x] | `docs/troubleshooting/README.md` |  |
| [x] | `docs/troubleshooting/common-issues.md` |  |
| [x] | `idea.md` |  |
| [x] | `monitoring/docker-compose.monitoring.yml` |  |
| [x] | `monitoring/grafana/dashboards/api-overview.json` |  |
| [x] | `monitoring/prometheus/alerts.yml` |  |
| [x] | `packages/ai/AGENTS.md` | optional |
| [x] | `packages/ai/__init__.py` | optional |
| [x] | `packages/ai/chromadb_client.py` | optional |
| [x] | `packages/ai/interfaces.py` | optional |
| [x] | `packages/ai/py.typed` | optional |
| [x] | `packages/contracts/AGENTS.md` |  |
| [x] | `packages/contracts/__init__.py` |  |
| [x] | `packages/contracts/errors.py` |  |
| [x] | `packages/contracts/models.py` |  |
| [x] | `packages/contracts/pagination.py` |  |
| [x] | `packages/contracts/py.typed` | optional |
| [x] | `packages/tasks/AGENTS.md` |  |
| [x] | `packages/tasks/__init__.py` |  |
| [x] | `packages/tasks/interfaces.py` |  |
| [x] | `packages/tasks/py.typed` | optional |
| [x] | `prompts/README.md` |  |
| [x] | `prompts/debugger.md` |  |
| [x] | `prompts/dependency_upgrade_agent.md` |  |
| [x] | `prompts/documentation_updater.md` |  |
| [x] | `prompts/domain_modeler.md` |  |
| [x] | `prompts/implementation_agent.md` |  |
| [x] | `prompts/incident_triage_agent.md` |  |
| [x] | `prompts/migration_author.md` |  |
| [x] | `prompts/performance_audit_agent.md` |  |
| [x] | `prompts/profile_configurator.md` |  |
| [x] | `prompts/queue_processor.md` |  |
| [x] | `prompts/refactorer.md` |  |
| [x] | `prompts/release_manager.md` |  |
| [x] | `prompts/repo_bootstrap_agent.md` |  |
| [x] | `prompts/repo_initializer.md` |  |
| [x] | `prompts/reviewer_critic.md` |  |
| [x] | `prompts/rule_authoring_agent.md` |  |
| [x] | `prompts/security_review_agent.md` |  |
| [x] | `prompts/skill_authoring_agent.md` |  |
| [x] | `prompts/skill_searcher.md` |  |
| [x] | `prompts/spec_hardening_agent.md` |  |
| [x] | `prompts/task_planner.md` |  |
| [x] | `prompts/test_writer.md` |  |
| [x] | `pyproject.toml` |  |
| [x] | `pyrightconfig.json` | optional |
| [x] | `queue/QUEUE_AGENT_PROMPT.md` |  |
| [x] | `queue/QUEUE_INSTRUCTIONS.md` |  |
| [x] | `queue/audit.log` | recommended |
| [x] | `queue/queue.csv` |  |
| [x] | `queue/queue.lock` | recommended |
| [x] | `queue/queuearchive.csv` |  |
| [x] | `run.bat` |  |
| [x] | `run.sh` |  |
| [x] | `scripts/README.md` |  |
| [x] | `scripts/audit-self.sh` |  |
| [x] | `scripts/clean.sh` |  |
| [x] | `scripts/db-reset.sh` |  |
| [x] | `scripts/dev.sh` |  |
| [x] | `scripts/docs-check.sh` |  |
| [x] | `scripts/docs-generate.sh` |  |
| [x] | `scripts/docs-index.sh` | recommended |
| [x] | `scripts/fmt.sh` |  |
| [x] | `scripts/generate-env.sh` |  |
| [x] | `scripts/health-check.sh` |  |
| [x] | `scripts/idea-to-queue.sh` |  |
| [x] | `scripts/image-build.sh` |  |
| [x] | `scripts/image-scan.sh` |  |
| [x] | `scripts/init-repo.sh` |  |
| [x] | `scripts/inventory-check.sh` |  |
| [x] | `scripts/k8s-render.sh` |  |
| [x] | `scripts/k8s-validate.sh` |  |
| [x] | `scripts/lint.sh` |  |
| [x] | `scripts/migrate.sh` |  |
| [x] | `scripts/profile-enable.sh` |  |
| [x] | `scripts/prompt-list.sh` |  |
| [x] | `scripts/queue-analyze.sh` |  |
| [x] | `scripts/queue-archive.sh` | recommended |
| [x] | `scripts/queue-graph.sh` |  |
| [x] | `scripts/queue-peek.sh` |  |
| [x] | `scripts/queue-validate.sh` |  |
| [x] | `scripts/release-prepare.sh` |  |
| [x] | `scripts/release-verify.sh` |  |
| [x] | `scripts/rules-check.sh` |  |
| [x] | `scripts/scaffold-module.sh` |  |
| [x] | `scripts/security-scan.sh` |  |
| [x] | `scripts/seed-db.sh` |  |
| [x] | `scripts/skills-list.sh` |  |
| [x] | `scripts/test.sh` |  |
| [x] | `scripts/typecheck.sh` |  |
| [x] | `scripts/validate-idea.sh` |  |
| [x] | `setup.bat` |  |
| [x] | `setup.sh` |  |
| [x] | `skills/README.md` |  |
| [x] | `skills/agent-ops/blocked-task-recovery.md` |  |
| [x] | `skills/agent-ops/handoff-template-generator.py` |  |
| [x] | `skills/agent-ops/implementation-handoff.md` |  |
| [x] | `skills/agent-ops/post-pr-audit.md` |  |
| [x] | `skills/agent-ops/prompt-to-procedure-promotion.md` |  |
| [x] | `skills/agent-ops/queue-intelligence.md` |  |
| [x] | `skills/agent-ops/queue-intelligence.py` |  |
| [x] | `skills/agent-ops/queue-triage.md` |  |
| [x] | `skills/agent-ops/queue-triage.py` |  |
| [x] | `skills/agent-ops/repo-self-audit.md` |  |
| [x] | `skills/agent-ops/repo-self-audit.py` |  |
| [x] | `skills/agent-ops/rule-refinement-after-mistakes.md` |  |
| [x] | `skills/agent-ops/task-planning.md` |  |
| [x] | `skills/ai-rag/ai-kill-switch.md` | optional |
| [x] | `skills/ai-rag/ai-safety-review.md` | optional |
| [x] | `skills/ai-rag/chromadb-ingestion.md` | optional |
| [x] | `skills/ai-rag/embedding-refresh.md` | optional |
| [x] | `skills/ai-rag/model-provider-abstraction.md` | optional |
| [x] | `skills/ai-rag/prompt-versioning.md` | optional |
| [x] | `skills/ai-rag/retrieval-evaluation.md` | optional |
| [x] | `skills/backend/api-versioning.md` |  |
| [x] | `skills/backend/background-jobs.md` |  |
| [x] | `skills/backend/configuration-management.md` |  |
| [x] | `skills/backend/env-var-sync.py` |  |
| [x] | `skills/backend/error-code-registry.py` |  |
| [x] | `skills/backend/error-taxonomy.md` |  |
| [x] | `skills/backend/fastapi-router-module.md` |  |
| [x] | `skills/backend/feature-flags.md` |  |
| [x] | `skills/backend/health-readiness-liveness.md` |  |
| [x] | `skills/backend/idempotent-tasks.md` |  |
| [x] | `skills/backend/metrics-exposition.md` |  |
| [x] | `skills/backend/module-scaffolder.py` |  |
| [x] | `skills/backend/openapi-diff.py` |  |
| [x] | `skills/backend/opentelemetry-tracing.md` |  |
| [x] | `skills/backend/rate-limiting.md` |  |
| [x] | `skills/backend/retries-circuit-breakers.md` |  |
| [x] | `skills/backend/safe-migration-rollout.md` |  |
| [x] | `skills/backend/service-repository-pattern.md` |  |
| [x] | `skills/backend/sqlite-to-postgres.md` |  |
| [x] | `skills/backend/structured-logging.md` |  |
| [x] | `skills/backend/worker-integration.md` |  |
| [x] | `skills/devops/artifact-publishing.md` |  |
| [x] | `skills/devops/backup-restore-drills.md` | recommended |
| [x] | `skills/devops/compose-profile-matrix.py` |  |
| [x] | `skills/devops/compose-profiles.md` |  |
| [x] | `skills/devops/docker-multi-stage-builds.md` |  |
| [x] | `skills/devops/dockerfile-linter.py` |  |
| [x] | `skills/devops/environment-configuration.md` |  |
| [x] | `skills/devops/github-actions-troubleshooting.md` |  |
| [x] | `skills/devops/k8s-manifest-validator.py` |  |
| [x] | `skills/devops/k8s-probes.md` |  |
| [x] | `skills/devops/release-promotion.md` |  |
| [x] | `skills/devops/rollout-rollback.md` |  |
| [x] | `skills/frontend/expo-auth-storage.md` | optional |
| [x] | `skills/frontend/frontend-env-handling.md` | optional |
| [x] | `skills/frontend/generated-client-usage.md` | optional |
| [x] | `skills/frontend/react-api-integration.md` | optional |
| [x] | `skills/init/README.md` |  |
| [x] | `skills/init/archetype-mapper.md` |  |
| [x] | `skills/init/archetype-mapper.py` |  |
| [x] | `skills/init/env-generator.md` |  |
| [x] | `skills/init/env-generator.py` |  |
| [x] | `skills/init/idea-validator.md` |  |
| [x] | `skills/init/idea-validator.py` |  |
| [x] | `skills/init/module-template-generator.md` |  |
| [x] | `skills/init/profile-resolver.md` |  |
| [x] | `skills/init/profile-resolver.py` |  |
| [x] | `skills/init/queue-seeder.md` |  |
| [x] | `skills/init/queue-seeder.py` |  |
| [x] | `skills/repo-governance/adding-reusable-commands.md` |  |
| [x] | `skills/repo-governance/adr-index-generator.py` |  |
| [x] | `skills/repo-governance/authoring-cursor-rules.md` |  |
| [x] | `skills/repo-governance/changelogs-release-notes.md` |  |
| [x] | `skills/repo-governance/docs-freshness-checker.py` |  |
| [x] | `skills/repo-governance/docs-generator.md` |  |
| [x] | `skills/repo-governance/docs-generator.py` |  |
| [x] | `skills/repo-governance/maintaining-procedural-docs.md` |  |
| [x] | `skills/repo-governance/repository-hygiene.md` |  |
| [x] | `skills/repo-governance/rule-linter.py` |  |
| [x] | `skills/repo-governance/writing-adrs.md` |  |
| [x] | `skills/repo-governance/writing-agents-md.md` |  |
| [x] | `skills/security/code-scanning.md` |  |
| [x] | `skills/security/dependency-audit.py` |  |
| [x] | `skills/security/dependency-review.md` |  |
| [x] | `skills/security/image-scanning.md` |  |
| [x] | `skills/security/incident-evidence-capture.md` |  |
| [x] | `skills/security/rbac-tenant-isolation.md` |  |
| [x] | `skills/security/sbom-attestation.md` | recommended |
| [x] | `skills/security/secret-handling.md` |  |
| [x] | `skills/security/secret-scanner.py` |  |
| [x] | `skills/security/secure-defaults-review.md` |  |
| [x] | `skills/security/tenant-isolation-checker.py` |  |
| [x] | `skills/security/token-lifecycle.md` |  |
| [x] | `skills/testing/api-contract-testing.md` |  |
| [x] | `skills/testing/async-testing.md` |  |
| [x] | `skills/testing/coverage-ratchet.py` |  |
| [x] | `skills/testing/flaky-detector.py` |  |
| [x] | `skills/testing/flaky-test-triage.md` |  |
| [x] | `skills/testing/load-test-basics.md` | recommended |
| [x] | `skills/testing/pytest-conventions.md` |  |
| [x] | `skills/testing/regression-harness.md` |  |
| [x] | `skills/testing/smoke-tests.md` |  |
| [x] | `skills/testing/snapshot-testing.md` |  |
| [x] | `skills/testing/test-scaffolder.py` |  |
| [x] | `skills/testing/validation-loop-design.md` |  |
| [x] | `spec/spec.md` |  |
| [x] | `trivy.yaml` |  |

---
## Counts
- **Folders listed:** 70 (per `spec/spec.md` §30)
- **Files listed:** 408 (per `spec/spec.md` §26 + §28 inventory; §32 total **408** enumerated files)
- **§24 reference:** See `spec/spec.md` §24 (implementation checklist — machine operability) for outcome-level acceptance criteria.
