# Implementation plan — spec checklist
This file is the **implementation checklist** for the template repository described in [`spec/spec.md`](./spec.md). The spec folder is the **source of truth** for policy and structure; this plan enumerates **folders and files** to create so the repository matches the spec (including §26–§28 and the §29 tree).

## How to use
- Check each box when the path exists on disk **and** meets the spec (stubs must include required headings per §26).
- **Optional** items are marked; include them when the relevant profile or feature is enabled.
- The root [`spec.md`](../spec.md) file is a short pointer to the canonical spec.

## Phases

### Phase 1 — Specification and root control plane
**Milestone 1.1 — Spec and policy surface**
- [ ] Confirm `spec/spec.md` is the canonical copy; root `spec.md` points to it.
- [ ] Add `AGENTS.md` per §4 (all required sections).
- [ ] Add `README.md`, `CONTRIBUTING.md`, `LICENSE`, optional `CODE_OF_CONDUCT.md`.
- [ ] Add `idea.md`, `CHANGELOG.md` per §27–§28.

### Phase 2 — Machine control layer
**Milestone 2.1 — Cursor rules and commands**
- [ ] Create `.cursor/rules/` (global, apps-api, security, queue, initialization, skills, prompts; recommended testing + documentation).
- [ ] Create `.cursor/commands/` (initialize, scaffold-module, audit; optional validate, queue-next).

### Phase 3 — Prompts, skills, and procedures
**Milestone 3.1 — Agent libraries**
- [ ] Populate `prompts/` including `repo_initializer.md` and role templates per §7.3 and §28.
- [ ] Populate `skills/` including `skills/init/` machinery and §6 coverage categories.
- [ ] Populate `docs/procedures/` per §8.2 plus initialization procedures in §28.

### Phase 4 — Documentation tree
**Milestone 4.1 — Conceptual and operational docs**
- [ ] Create `docs/` subtrees: getting-started, architecture, development, api, operations, security, adr, agents, prompts index, runbooks, release, repo-governance, quality, queue, optional-clients.

### Phase 5 — Queue and GitHub
**Milestone 5.1 — Orchestration and CI/CD**
- [ ] Create `queue/` CSV files and queue SOPs; optional `queue.lock` and `audit.log`.
- [ ] Add `.github/workflows/` (ci, cd, security), templates, CODEOWNERS, dependabot.

### Phase 6 — Backend, packages, deploy
**Milestone 6.1 — Runnable API + infra**
- [ ] Implement `apps/api/` FastAPI monolith with health + auth + tenancy stubs and tests.
- [ ] Add `packages/contracts`, `packages/tasks`, optional `packages/ai`.
- [ ] Add `deploy/docker`, `deploy/k8s` overlays; optional `apps/web` and `apps/mobile` placeholders.

### Phase 7 — Automation scripts and Makefile
**Milestone 7.1 — Canonical commands**
- [ ] Add `scripts/` backing every Make target per §10.2 and §28.6 (including init, idea validation, inventory).
- [ ] Wire `Makefile` or Taskfile with minimum catalog + initialization targets (§28.8).
- [ ] Add `pyproject.toml`, `.env.example`, `docker-compose.yml`.

### Phase 8 — Validation and governance
**Milestone 8.1 — Definition of done**
- [ ] Meet §24 checklist: CI stages, `queue:validate`, `audit:self`, security scans, release docs.
- [ ] Run `make inventory:check` (or equivalent) against this checklist.

---

## Folder checklist
| Created | Path | Notes |
|:-------:|------|-------|
| [ ] | `/` (repo root) | Top-level control plane and configuration. Contains `AGENTS.md`, `spec/spec.md` (canonical spec), optional root `spec.md` pointer, `idea.md`, `README.md`, `Makefile`, `pyproject.toml`, `docker-compose.yml`, `.env.example`, `CHANGELOG.md`, and legal files. Everything an agent or human needs to orient and begin work. |
| [ ] | `.cursor/` | Machine-control layer for Cursor IDE. Houses persistent rules and reusable commands that shape agent behavior during development sessions. |
| [ ] | `.cursor/rules/` | Always-on and path-scoped constraints. Global rules apply everywhere; path-scoped rules activate only in matching directories. Agents load these automatically. Includes initialization, skills, and prompts rules. |
| [ ] | `.cursor/commands/` | Reusable Cursor command definitions. Shortcuts that invoke canonical scripts or document exact command sequences. Includes initialization, scaffolding, and audit commands. |
| [ ] | `prompts/` | Reusable, versioned prompt templates for recurring agent roles. Each template has metadata (purpose, inputs, outputs, linked procedures/skills) and a prompt body with placeholders. Includes the master `repo_initializer` prompt. |
| [ ] | `skills/` | Executable playbooks organized by category. Each skill has a `.md` playbook and may include supporting code (machinery) for automation, validation, and generation. |
| [ ] | `skills/init/` | Initialization skills and machinery. Used during repo initialization from `idea.md`: validation, archetype mapping, module scaffolding, queue seeding, profile resolution, env generation. |
| [ ] | `skills/agent-ops/` | Skills for agent-specific operations: queue triage, task planning, handoffs, blocked recovery, prompt promotion, rule refinement, auditing. Includes Python machinery for queue analysis, handoff generation, and self-audit. |
| [ ] | `skills/repo-governance/` | Skills for maintaining the repository machine: writing `AGENTS.md`, authoring rules, maintaining procedures, writing ADRs, changelogs, hygiene. Includes machinery for rule linting, docs freshness checking, and ADR index generation. |
| [ ] | `skills/backend/` | Skills for backend/platform development: FastAPI patterns, service layers, health endpoints, API versioning, background jobs, configuration, logging, metrics, tracing, rate limiting, migrations. Includes machinery for module scaffolding, error code registry, env var sync, and OpenAPI diffing. |
| [ ] | `skills/security/` | Skills for security and compliance: secret handling, token lifecycle, RBAC/tenant isolation, dependency review, code/image scanning, SBOM, incident evidence. Includes machinery for secret scanning, dependency auditing, and tenant isolation checking. |
| [ ] | `skills/testing/` | Skills for testing and quality: pytest conventions, async testing, contract testing, snapshots, smoke tests, regression, load testing, flaky triage, validation loops. Includes machinery for test scaffolding, coverage ratcheting, and flaky detection. |
| [ ] | `skills/devops/` | Skills for DevOps and operations: Docker builds, Compose profiles, K8s probes, rollout/rollback, GitHub Actions, release promotion, artifact publishing, env config, backup/restore. Includes machinery for Dockerfile linting, K8s manifest validation, and Compose profile testing. |
| [ ] | `skills/ai-rag/` | Skills for AI/RAG operations (optional profile): ChromaDB ingestion, embedding refresh, retrieval evaluation, prompt versioning, kill switch, provider abstraction, safety review. |
| [ ] | `skills/frontend/` | Skills for optional frontend/mobile profiles: generated clients, React API integration, Expo auth storage, frontend env handling. |
| [ ] | `docs/` | Documentation hub. All conceptual and operational documentation organized by subsystem. Every major subsystem has both a conceptual explanation (why) and an operational explanation (how). |
| [ ] | `docs/getting-started/` | Onboarding documentation: prerequisites, quickstart from clone to running dev server with passing tests. |
| [ ] | `docs/architecture/` | Architecture documentation: modular monolith design, data layer strategy, auth/multi-tenancy, AI/RAG architecture, system context, domain model, API design. |
| [ ] | `docs/development/` | Development documentation: local setup with all Make targets, coding standards, testing guide, env var reference, module patterns, dependency management. |
| [ ] | `docs/api/` | API documentation: endpoint catalog, error code taxonomy. |
| [ ] | `docs/operations/` | Operations documentation: Docker, Kubernetes, observability, backups, rollback, configuration, health checks. |
| [ ] | `docs/security/` | Security documentation: threat model, secrets management, incident response, token lifecycle. |
| [ ] | `docs/procedures/` | Standard Operating Procedures. Canonical workflows written for agents first, usable by humans. Includes initialization, scaffolding, profile enablement, and idea validation procedures alongside all original SOPs. |
| [ ] | `docs/adr/` | Architecture Decision Records. Index of all architectural decisions with template for new ones. |
| [ ] | `docs/agents/` | Agent supervision documentation for human maintainers: initialization guide, supervision, review AI diffs, audit PRs, ratchet quality, evolve from incidents. |
| [ ] | `docs/prompts/` | Prompt library documentation: conventions, metadata format, authoring guide, index of all templates. |
| [ ] | `docs/runbooks/` | Operational runbooks for specific failure scenarios: API down, DB failure, JWT key rotation, ChromaDB unavailable. |
| [ ] | `docs/release/` | Release documentation: versioning strategy, promotion path (dev → staging → prod), changelog guide. |
| [ ] | `docs/repo-governance/` | Repository governance documentation: improvement loops, audits, procedure drift detection, documentation freshness. |
| [ ] | `docs/quality/` | Quality documentation: testing strategy, coverage policy and floors, flaky test policy. |
| [ ] | `docs/queue/` | Queue system documentation: conceptual overview of the CSV-based agent work orchestration system, queue category registry. |
| [ ] | `docs/optional-clients/` | Documentation for optional application profiles (web, mobile): when to enable, setup, operational burden. |
| [ ] | `queue/` | Agent work orchestration lane. CSV-based queue with strict lifecycle, single-lane processing, audit logging, and validation tooling. |
| [ ] | `.github/` | GitHub repository management: CI/CD workflows, issue templates, PR template, code ownership, dependency management, labels. |
| [ ] | `.github/workflows/` | GitHub Actions workflow definitions: CI (lint, typecheck, test, build, scan), CD (deploy through environments), security scanning. |
| [ ] | `.github/ISSUE_TEMPLATE/` | GitHub issue templates: structured forms for bug reports, feature requests, and queue items. |
| [ ] | `apps/` | Application code. Contains the primary API and optional frontend/mobile profiles. Each app may have its own scoped `AGENTS.md`. |
| [ ] | `apps/api/` | FastAPI modular monolith — the primary application. Health endpoints, auth stubs, tenant hooks, Alembic migrations, Docker build, tests. |
| [ ] | `apps/api/alembic/` | Database migration configuration and version scripts (Alembic). |
| [ ] | `apps/api/alembic/versions/` | Individual migration version files. Starts with `.gitkeep`; populated as schema evolves. |
| [ ] | `apps/api/src/` | API application source code organized by bounded context (health, auth, tenancy). |
| [ ] | `apps/api/src/health/` | Health module: health, readiness, and liveness endpoints for operational monitoring and K8s probes. |
| [ ] | `apps/api/src/auth/` | Authentication module: register, login, refresh, logout endpoints with JWT token management. Policy-complete stubs with extension points. |
| [ ] | `apps/api/src/tenancy/` | Multi-tenancy module: tenant context middleware, tenant models, query scoping mixin. |
| [ ] | `apps/api/tests/` | API test suite: health endpoint tests, auth endpoint tests, shared fixtures and configuration. |
| [ ] | `apps/web/` | Optional web frontend placeholder. Contains README and scoped AGENTS.md when profile is enabled. |
| [ ] | `apps/mobile/` | Optional mobile app placeholder. Contains README and scoped AGENTS.md when profile is enabled. |
| [ ] | `packages/` | Shared packages used across bounded contexts and applications. Contracts, task interfaces, AI interfaces. |
| [ ] | `packages/contracts/` | Shared Pydantic models and OpenAPI schemas. The contract layer for the modular monolith — backward compatibility is mandatory. |
| [ ] | `packages/tasks/` | Background task interfaces. Abstract base classes for task submission and handling. Workers are an optional profile. |
| [ ] | `packages/ai/` | AI/RAG interfaces (optional profile). Provider-agnostic abstractions for embedding, retrieval, and generation with ChromaDB implementation. |
| [ ] | `deploy/` | Deployment configuration for Docker and Kubernetes. |
| [ ] | `deploy/docker/` | Docker-specific deployment documentation and configurations. |
| [ ] | `deploy/k8s/` | Kubernetes manifests organized with Kustomize: base resources and environment-specific overlays. |
| [ ] | `deploy/k8s/base/` | Base Kubernetes manifests: Deployment, Service, ConfigMap, Kustomization. Shared across all environments. |
| [ ] | `deploy/k8s/overlays/` | Environment-specific Kustomize overlays that patch base manifests for dev, staging, and production. |
| [ ] | `deploy/k8s/overlays/dev/` | Dev environment overlay: single replica, debug settings, relaxed resource limits. |
| [ ] | `deploy/k8s/overlays/staging/` | Staging environment overlay: production-like configuration at lower scale. |
| [ ] | `deploy/k8s/overlays/prod/` | Production environment overlay: full scale, strict settings, pod disruption budgets. |
| [ ] | `scripts/` | Shell script implementations backing Makefile targets. The execution layer for all canonical commands including initialization and scaffolding. |
| [ ] | `.devcontainer/` | Dev container configuration for reproducible development environments (VS Code / Codespaces). |
| [ ] | `docs/troubleshooting/` | Common development issues and their solutions (index + curated fixes). |
| [ ] | `docs/architecture/diagrams/` | Architecture diagram source files (optional Mermaid/PlantUML). |
| [ ] | `monitoring/` | Observability configuration files (recommended local stack overlay). |
| [ ] | `monitoring/prometheus/` | Prometheus configuration and alert rules. |
| [ ] | `monitoring/grafana/` | Grafana configuration and dashboard provisioning. |
| [ ] | `monitoring/grafana/dashboards/` | Exportable Grafana dashboard JSON files. |
| [ ] | `.github/actions/` | Reusable composite GitHub Actions (optional). |
| [ ] | `.github/actions/setup-python/` | Composite action: Python setup with caching. |
| [ ] | `.github/actions/docker-build/` | Composite action: Docker build with layer caching. |

---
## File checklist
| Created | Path | Notes |
|:-------:|------|-------|
| [ ] | `.bandit.yml` |  |
| [ ] | `.cursor/commands/audit.md` |  |
| [ ] | `.cursor/commands/initialize.md` |  |
| [ ] | `.cursor/commands/queue-next.md` | optional |
| [ ] | `.cursor/commands/scaffold-module.md` |  |
| [ ] | `.cursor/commands/validate.md` | optional |
| [ ] | `.cursor/rules/apps-api.md` |  |
| [ ] | `.cursor/rules/documentation.md` | recommended |
| [ ] | `.cursor/rules/global.md` |  |
| [ ] | `.cursor/rules/initialization.md` |  |
| [ ] | `.cursor/rules/prompts.md` |  |
| [ ] | `.cursor/rules/queue.md` |  |
| [ ] | `.cursor/rules/security.md` |  |
| [ ] | `.cursor/rules/skills.md` |  |
| [ ] | `.cursor/rules/testing.md` | recommended |
| [ ] | `.cursorignore` |  |
| [ ] | `.devcontainer/devcontainer.json` |  |
| [ ] | `.dockerignore` |  |
| [ ] | `.editorconfig` |  |
| [ ] | `.env.example` |  |
| [ ] | `.envrc` | optional |
| [ ] | `.gitattributes` |  |
| [ ] | `.github/CODEOWNERS` |  |
| [ ] | `.github/ISSUE_TEMPLATE/bug_report.md` |  |
| [ ] | `.github/ISSUE_TEMPLATE/feature_request.md` |  |
| [ ] | `.github/ISSUE_TEMPLATE/queue_item.md` | recommended |
| [ ] | `.github/PULL_REQUEST_TEMPLATE.md` |  |
| [ ] | `.github/actions/docker-build/action.yml` | optional |
| [ ] | `.github/actions/setup-python/action.yml` | optional |
| [ ] | `.github/dependabot.yml` |  |
| [ ] | `.github/labels.yml` | recommended |
| [ ] | `.github/release.yml` |  |
| [ ] | `.github/workflows/cd.yml` |  |
| [ ] | `.github/workflows/ci.yml` |  |
| [ ] | `.github/workflows/label-sync.yml` | optional |
| [ ] | `.github/workflows/security.yml` |  |
| [ ] | `.github/workflows/stale.yml` | optional |
| [ ] | `.gitignore` |  |
| [ ] | `.mailmap` | optional |
| [ ] | `.pre-commit-config.yaml` |  |
| [ ] | `.python-version` |  |
| [ ] | `.trivyignore` |  |
| [ ] | `AGENTS.md` |  |
| [ ] | `CHANGELOG.md` |  |
| [ ] | `CODEBASE_SUMMARY.md` | optional |
| [ ] | `CODE_OF_CONDUCT.md` | optional |
| [ ] | `CONTRIBUTING.md` |  |
| [ ] | `LICENSE` |  |
| [ ] | `Makefile` |  |
| [ ] | `NOTICE` | optional |
| [ ] | `README.md` |  |
| [ ] | `SECURITY.md` |  |
| [ ] | `apps/api/AGENTS.md` |  |
| [ ] | `apps/api/Dockerfile` |  |
| [ ] | `apps/api/alembic.ini` |  |
| [ ] | `apps/api/alembic/env.py` |  |
| [ ] | `apps/api/alembic/script.py.mako` |  |
| [ ] | `apps/api/alembic/versions/.gitkeep` |  |
| [ ] | `apps/api/src/__init__.py` |  |
| [ ] | `apps/api/src/auth/__init__.py` |  |
| [ ] | `apps/api/src/auth/dependencies.py` |  |
| [ ] | `apps/api/src/auth/models.py` |  |
| [ ] | `apps/api/src/auth/router.py` |  |
| [ ] | `apps/api/src/auth/schemas.py` |  |
| [ ] | `apps/api/src/auth/service.py` |  |
| [ ] | `apps/api/src/config.py` |  |
| [ ] | `apps/api/src/database.py` |  |
| [ ] | `apps/api/src/dependencies.py` |  |
| [ ] | `apps/api/src/events.py` | optional |
| [ ] | `apps/api/src/exceptions.py` |  |
| [ ] | `apps/api/src/health/__init__.py` |  |
| [ ] | `apps/api/src/health/router.py` |  |
| [ ] | `apps/api/src/main.py` |  |
| [ ] | `apps/api/src/middleware.py` |  |
| [ ] | `apps/api/src/pagination.py` |  |
| [ ] | `apps/api/src/tenancy/__init__.py` |  |
| [ ] | `apps/api/src/tenancy/middleware.py` |  |
| [ ] | `apps/api/src/tenancy/models.py` |  |
| [ ] | `apps/api/tests/__init__.py` |  |
| [ ] | `apps/api/tests/conftest.py` |  |
| [ ] | `apps/api/tests/factories.py` |  |
| [ ] | `apps/api/tests/test_auth.py` |  |
| [ ] | `apps/api/tests/test_health.py` |  |
| [ ] | `apps/api/tests/test_tenancy.py` |  |
| [ ] | `apps/mobile/AGENTS.md` | optional |
| [ ] | `apps/mobile/README.md` | optional |
| [ ] | `apps/web/AGENTS.md` | optional |
| [ ] | `apps/web/README.md` | optional |
| [ ] | `deploy/docker/README.md` |  |
| [ ] | `deploy/k8s/README.md` |  |
| [ ] | `deploy/k8s/base/configmap.yaml` |  |
| [ ] | `deploy/k8s/base/deployment.yaml` |  |
| [ ] | `deploy/k8s/base/hpa.yaml` |  |
| [ ] | `deploy/k8s/base/ingress.yaml` |  |
| [ ] | `deploy/k8s/base/kustomization.yaml` |  |
| [ ] | `deploy/k8s/base/networkpolicy.yaml` |  |
| [ ] | `deploy/k8s/base/service.yaml` |  |
| [ ] | `deploy/k8s/base/serviceaccount.yaml` |  |
| [ ] | `deploy/k8s/overlays/dev/kustomization.yaml` |  |
| [ ] | `deploy/k8s/overlays/prod/kustomization.yaml` |  |
| [ ] | `deploy/k8s/overlays/staging/kustomization.yaml` |  |
| [ ] | `docker-compose.test.yml` | optional |
| [ ] | `docker-compose.yml` |  |
| [ ] | `docs/README.md` |  |
| [ ] | `docs/adr/README.md` |  |
| [ ] | `docs/adr/template.md` |  |
| [ ] | `docs/agents/README.md` |  |
| [ ] | `docs/agents/evolving-from-incidents.md` |  |
| [ ] | `docs/agents/initialization-guide.md` |  |
| [ ] | `docs/agents/pr-audit-checklist.md` |  |
| [ ] | `docs/agents/quality-ratcheting.md` |  |
| [ ] | `docs/agents/reviewing-ai-diffs.md` |  |
| [ ] | `docs/agents/supervision-guide.md` |  |
| [ ] | `docs/api/README.md` |  |
| [ ] | `docs/api/endpoints.md` |  |
| [ ] | `docs/api/error-codes.md` |  |
| [ ] | `docs/api/openapi-baseline.json` | optional |
| [ ] | `docs/architecture/README.md` |  |
| [ ] | `docs/architecture/ai-rag-chromadb.md` | optional |
| [ ] | `docs/architecture/api-design.md` |  |
| [ ] | `docs/architecture/auth-multi-tenancy.md` |  |
| [ ] | `docs/architecture/data-layer.md` |  |
| [ ] | `docs/architecture/diagrams/README.md` | optional |
| [ ] | `docs/architecture/domain-model.md` |  |
| [ ] | `docs/architecture/error-handling.md` | optional |
| [ ] | `docs/architecture/modular-monolith.md` |  |
| [ ] | `docs/architecture/system-context.md` |  |
| [ ] | `docs/development/README.md` |  |
| [ ] | `docs/development/coding-standards.md` |  |
| [ ] | `docs/development/dependency-management.md` |  |
| [ ] | `docs/development/docs-generation.md` |  |
| [ ] | `docs/development/environment-vars.md` |  |
| [ ] | `docs/development/git-workflow.md` |  |
| [ ] | `docs/development/local-setup.md` |  |
| [ ] | `docs/development/module-patterns.md` |  |
| [ ] | `docs/development/testing-guide.md` |  |
| [ ] | `docs/getting-started/README.md` |  |
| [ ] | `docs/getting-started/prerequisites.md` |  |
| [ ] | `docs/getting-started/quickstart.md` |  |
| [ ] | `docs/glossary.md` |  |
| [ ] | `docs/operations/README.md` |  |
| [ ] | `docs/operations/backups.md` |  |
| [ ] | `docs/operations/configuration.md` |  |
| [ ] | `docs/operations/database-operations.md` | optional |
| [ ] | `docs/operations/docker.md` |  |
| [ ] | `docs/operations/health-checks.md` |  |
| [ ] | `docs/operations/kubernetes.md` |  |
| [ ] | `docs/operations/observability.md` |  |
| [ ] | `docs/operations/rollback.md` |  |
| [ ] | `docs/operations/scaling.md` | optional |
| [ ] | `docs/optional-clients/mobile.md` | optional |
| [ ] | `docs/optional-clients/web.md` | optional |
| [ ] | `docs/procedures/README.md` |  |
| [ ] | `docs/procedures/add-optional-app-profile.md` |  |
| [ ] | `docs/procedures/add-prompt-template.md` |  |
| [ ] | `docs/procedures/add-queue-category.md` |  |
| [ ] | `docs/procedures/archive-queue-item.md` |  |
| [ ] | `docs/procedures/database-migration.md` |  |
| [ ] | `docs/procedures/dependency-upgrade.md` |  |
| [ ] | `docs/procedures/enable-profile.md` |  |
| [ ] | `docs/procedures/extract-service-from-monolith.md` |  |
| [ ] | `docs/procedures/handle-blocked-work.md` |  |
| [ ] | `docs/procedures/handoff.md` |  |
| [ ] | `docs/procedures/implement-change.md` |  |
| [ ] | `docs/procedures/incident-rollback.md` |  |
| [ ] | `docs/procedures/initialize-repo.md` |  |
| [ ] | `docs/procedures/open-pull-request.md` |  |
| [ ] | `docs/procedures/plan-change.md` |  |
| [ ] | `docs/procedures/release-preparation.md` |  |
| [ ] | `docs/procedures/scaffold-domain-module.md` |  |
| [ ] | `docs/procedures/start-queue-item.md` |  |
| [ ] | `docs/procedures/update-documentation.md` |  |
| [ ] | `docs/procedures/update-or-create-rule.md` |  |
| [ ] | `docs/procedures/update-or-create-skill.md` |  |
| [ ] | `docs/procedures/validate-change.md` |  |
| [ ] | `docs/procedures/validate-idea-md.md` |  |
| [ ] | `docs/prompts/README.md` |  |
| [ ] | `docs/prompts/conventions.md` |  |
| [ ] | `docs/prompts/index.md` |  |
| [ ] | `docs/quality/README.md` |  |
| [ ] | `docs/quality/coverage-policy.md` |  |
| [ ] | `docs/quality/flake-policy.md` |  |
| [ ] | `docs/quality/testing-strategy.md` |  |
| [ ] | `docs/queue/queue-categories.md` |  |
| [ ] | `docs/queue/queue-intelligence.md` |  |
| [ ] | `docs/queue/queue-system-overview.md` |  |
| [ ] | `docs/release/README.md` |  |
| [ ] | `docs/release/changelog-guide.md` |  |
| [ ] | `docs/release/promotion.md` |  |
| [ ] | `docs/release/versioning.md` |  |
| [ ] | `docs/repo-governance/README.md` |  |
| [ ] | `docs/repo-governance/audits.md` |  |
| [ ] | `docs/repo-governance/documentation-freshness.md` |  |
| [ ] | `docs/repo-governance/improvement-loops.md` |  |
| [ ] | `docs/repo-governance/procedure-drift-detection.md` |  |
| [ ] | `docs/runbooks/README.md` |  |
| [ ] | `docs/runbooks/api-down.md` |  |
| [ ] | `docs/runbooks/chroma-unavailable.md` | optional |
| [ ] | `docs/runbooks/db-failure.md` |  |
| [ ] | `docs/runbooks/jwt-key-rotation.md` |  |
| [ ] | `docs/security/README.md` |  |
| [ ] | `docs/security/accepted-risks.md` |  |
| [ ] | `docs/security/cors-policy.md` | optional |
| [ ] | `docs/security/incident-response.md` |  |
| [ ] | `docs/security/secrets-management.md` |  |
| [ ] | `docs/security/threat-model-stub.md` |  |
| [ ] | `docs/security/token-lifecycle.md` |  |
| [ ] | `docs/troubleshooting/README.md` |  |
| [ ] | `docs/troubleshooting/common-issues.md` |  |
| [ ] | `idea.md` |  |
| [ ] | `monitoring/docker-compose.monitoring.yml` |  |
| [ ] | `monitoring/grafana/dashboards/api-overview.json` |  |
| [ ] | `monitoring/prometheus/alerts.yml` |  |
| [ ] | `packages/ai/AGENTS.md` | optional |
| [ ] | `packages/ai/__init__.py` | optional |
| [ ] | `packages/ai/chromadb_client.py` | optional |
| [ ] | `packages/ai/interfaces.py` | optional |
| [ ] | `packages/ai/py.typed` | optional |
| [ ] | `packages/contracts/AGENTS.md` |  |
| [ ] | `packages/contracts/__init__.py` |  |
| [ ] | `packages/contracts/errors.py` |  |
| [ ] | `packages/contracts/models.py` |  |
| [ ] | `packages/contracts/pagination.py` |  |
| [ ] | `packages/contracts/py.typed` | optional |
| [ ] | `packages/tasks/AGENTS.md` |  |
| [ ] | `packages/tasks/__init__.py` |  |
| [ ] | `packages/tasks/interfaces.py` |  |
| [ ] | `packages/tasks/py.typed` | optional |
| [ ] | `prompts/README.md` |  |
| [ ] | `prompts/debugger.md` |  |
| [ ] | `prompts/dependency_upgrade_agent.md` |  |
| [ ] | `prompts/documentation_updater.md` |  |
| [ ] | `prompts/domain_modeler.md` |  |
| [ ] | `prompts/implementation_agent.md` |  |
| [ ] | `prompts/incident_triage_agent.md` |  |
| [ ] | `prompts/migration_author.md` |  |
| [ ] | `prompts/performance_audit_agent.md` |  |
| [ ] | `prompts/profile_configurator.md` |  |
| [ ] | `prompts/queue_processor.md` |  |
| [ ] | `prompts/refactorer.md` |  |
| [ ] | `prompts/release_manager.md` |  |
| [ ] | `prompts/repo_bootstrap_agent.md` |  |
| [ ] | `prompts/repo_initializer.md` |  |
| [ ] | `prompts/reviewer_critic.md` |  |
| [ ] | `prompts/rule_authoring_agent.md` |  |
| [ ] | `prompts/security_review_agent.md` |  |
| [ ] | `prompts/skill_authoring_agent.md` |  |
| [ ] | `prompts/skill_searcher.md` |  |
| [ ] | `prompts/spec_hardening_agent.md` |  |
| [ ] | `prompts/task_planner.md` |  |
| [ ] | `prompts/test_writer.md` |  |
| [ ] | `pyproject.toml` |  |
| [ ] | `pyrightconfig.json` | optional |
| [ ] | `queue/QUEUE_AGENT_PROMPT.md` |  |
| [ ] | `queue/QUEUE_INSTRUCTIONS.md` |  |
| [ ] | `queue/audit.log` | recommended |
| [ ] | `queue/queue.csv` |  |
| [ ] | `queue/queue.lock` | recommended |
| [ ] | `queue/queuearchive.csv` |  |
| [ ] | `run.bat` |  |
| [ ] | `run.sh` |  |
| [ ] | `scripts/README.md` |  |
| [ ] | `scripts/audit-self.sh` |  |
| [ ] | `scripts/clean.sh` |  |
| [ ] | `scripts/db-reset.sh` |  |
| [ ] | `scripts/dev.sh` |  |
| [ ] | `scripts/docs-check.sh` |  |
| [ ] | `scripts/docs-generate.sh` |  |
| [ ] | `scripts/docs-index.sh` | recommended |
| [ ] | `scripts/fmt.sh` |  |
| [ ] | `scripts/generate-env.sh` |  |
| [ ] | `scripts/health-check.sh` |  |
| [ ] | `scripts/idea-to-queue.sh` |  |
| [ ] | `scripts/image-build.sh` |  |
| [ ] | `scripts/image-scan.sh` |  |
| [ ] | `scripts/init-repo.sh` |  |
| [ ] | `scripts/inventory-check.sh` |  |
| [ ] | `scripts/k8s-render.sh` |  |
| [ ] | `scripts/k8s-validate.sh` |  |
| [ ] | `scripts/lint.sh` |  |
| [ ] | `scripts/migrate.sh` |  |
| [ ] | `scripts/profile-enable.sh` |  |
| [ ] | `scripts/prompt-list.sh` |  |
| [ ] | `scripts/queue-analyze.sh` |  |
| [ ] | `scripts/queue-archive.sh` | recommended |
| [ ] | `scripts/queue-graph.sh` |  |
| [ ] | `scripts/queue-peek.sh` |  |
| [ ] | `scripts/queue-validate.sh` |  |
| [ ] | `scripts/release-prepare.sh` |  |
| [ ] | `scripts/release-verify.sh` |  |
| [ ] | `scripts/rules-check.sh` |  |
| [ ] | `scripts/scaffold-module.sh` |  |
| [ ] | `scripts/security-scan.sh` |  |
| [ ] | `scripts/seed-db.sh` |  |
| [ ] | `scripts/skills-list.sh` |  |
| [ ] | `scripts/test.sh` |  |
| [ ] | `scripts/typecheck.sh` |  |
| [ ] | `scripts/validate-idea.sh` |  |
| [ ] | `setup.bat` |  |
| [ ] | `setup.sh` |  |
| [ ] | `skills/README.md` |  |
| [ ] | `skills/agent-ops/blocked-task-recovery.md` |  |
| [ ] | `skills/agent-ops/handoff-template-generator.py` |  |
| [ ] | `skills/agent-ops/implementation-handoff.md` |  |
| [ ] | `skills/agent-ops/post-pr-audit.md` |  |
| [ ] | `skills/agent-ops/prompt-to-procedure-promotion.md` |  |
| [ ] | `skills/agent-ops/queue-intelligence.md` |  |
| [ ] | `skills/agent-ops/queue-intelligence.py` |  |
| [ ] | `skills/agent-ops/queue-triage.md` |  |
| [ ] | `skills/agent-ops/queue-triage.py` |  |
| [ ] | `skills/agent-ops/repo-self-audit.md` |  |
| [ ] | `skills/agent-ops/repo-self-audit.py` |  |
| [ ] | `skills/agent-ops/rule-refinement-after-mistakes.md` |  |
| [ ] | `skills/agent-ops/task-planning.md` |  |
| [ ] | `skills/ai-rag/ai-kill-switch.md` | optional |
| [ ] | `skills/ai-rag/ai-safety-review.md` | optional |
| [ ] | `skills/ai-rag/chromadb-ingestion.md` | optional |
| [ ] | `skills/ai-rag/embedding-refresh.md` | optional |
| [ ] | `skills/ai-rag/model-provider-abstraction.md` | optional |
| [ ] | `skills/ai-rag/prompt-versioning.md` | optional |
| [ ] | `skills/ai-rag/retrieval-evaluation.md` | optional |
| [ ] | `skills/backend/api-versioning.md` |  |
| [ ] | `skills/backend/background-jobs.md` |  |
| [ ] | `skills/backend/configuration-management.md` |  |
| [ ] | `skills/backend/env-var-sync.py` |  |
| [ ] | `skills/backend/error-code-registry.py` |  |
| [ ] | `skills/backend/error-taxonomy.md` |  |
| [ ] | `skills/backend/fastapi-router-module.md` |  |
| [ ] | `skills/backend/feature-flags.md` |  |
| [ ] | `skills/backend/health-readiness-liveness.md` |  |
| [ ] | `skills/backend/idempotent-tasks.md` |  |
| [ ] | `skills/backend/metrics-exposition.md` |  |
| [ ] | `skills/backend/module-scaffolder.py` |  |
| [ ] | `skills/backend/openapi-diff.py` |  |
| [ ] | `skills/backend/opentelemetry-tracing.md` |  |
| [ ] | `skills/backend/rate-limiting.md` |  |
| [ ] | `skills/backend/retries-circuit-breakers.md` |  |
| [ ] | `skills/backend/safe-migration-rollout.md` |  |
| [ ] | `skills/backend/service-repository-pattern.md` |  |
| [ ] | `skills/backend/sqlite-to-postgres.md` |  |
| [ ] | `skills/backend/structured-logging.md` |  |
| [ ] | `skills/backend/worker-integration.md` |  |
| [ ] | `skills/devops/artifact-publishing.md` |  |
| [ ] | `skills/devops/backup-restore-drills.md` | recommended |
| [ ] | `skills/devops/compose-profile-matrix.py` |  |
| [ ] | `skills/devops/compose-profiles.md` |  |
| [ ] | `skills/devops/docker-multi-stage-builds.md` |  |
| [ ] | `skills/devops/dockerfile-linter.py` |  |
| [ ] | `skills/devops/environment-configuration.md` |  |
| [ ] | `skills/devops/github-actions-troubleshooting.md` |  |
| [ ] | `skills/devops/k8s-manifest-validator.py` |  |
| [ ] | `skills/devops/k8s-probes.md` |  |
| [ ] | `skills/devops/release-promotion.md` |  |
| [ ] | `skills/devops/rollout-rollback.md` |  |
| [ ] | `skills/frontend/expo-auth-storage.md` | optional |
| [ ] | `skills/frontend/frontend-env-handling.md` | optional |
| [ ] | `skills/frontend/generated-client-usage.md` | optional |
| [ ] | `skills/frontend/react-api-integration.md` | optional |
| [ ] | `skills/init/README.md` |  |
| [ ] | `skills/init/archetype-mapper.md` |  |
| [ ] | `skills/init/archetype-mapper.py` |  |
| [ ] | `skills/init/env-generator.md` |  |
| [ ] | `skills/init/env-generator.py` |  |
| [ ] | `skills/init/idea-validator.md` |  |
| [ ] | `skills/init/idea-validator.py` |  |
| [ ] | `skills/init/module-template-generator.md` |  |
| [ ] | `skills/init/profile-resolver.md` |  |
| [ ] | `skills/init/profile-resolver.py` |  |
| [ ] | `skills/init/queue-seeder.md` |  |
| [ ] | `skills/init/queue-seeder.py` |  |
| [ ] | `skills/repo-governance/adding-reusable-commands.md` |  |
| [ ] | `skills/repo-governance/adr-index-generator.py` |  |
| [ ] | `skills/repo-governance/authoring-cursor-rules.md` |  |
| [ ] | `skills/repo-governance/changelogs-release-notes.md` |  |
| [ ] | `skills/repo-governance/docs-freshness-checker.py` |  |
| [ ] | `skills/repo-governance/docs-generator.md` |  |
| [ ] | `skills/repo-governance/docs-generator.py` |  |
| [ ] | `skills/repo-governance/maintaining-procedural-docs.md` |  |
| [ ] | `skills/repo-governance/repository-hygiene.md` |  |
| [ ] | `skills/repo-governance/rule-linter.py` |  |
| [ ] | `skills/repo-governance/writing-adrs.md` |  |
| [ ] | `skills/repo-governance/writing-agents-md.md` |  |
| [ ] | `skills/security/code-scanning.md` |  |
| [ ] | `skills/security/dependency-audit.py` |  |
| [ ] | `skills/security/dependency-review.md` |  |
| [ ] | `skills/security/image-scanning.md` |  |
| [ ] | `skills/security/incident-evidence-capture.md` |  |
| [ ] | `skills/security/rbac-tenant-isolation.md` |  |
| [ ] | `skills/security/sbom-attestation.md` | recommended |
| [ ] | `skills/security/secret-handling.md` |  |
| [ ] | `skills/security/secret-scanner.py` |  |
| [ ] | `skills/security/secure-defaults-review.md` |  |
| [ ] | `skills/security/tenant-isolation-checker.py` |  |
| [ ] | `skills/security/token-lifecycle.md` |  |
| [ ] | `skills/testing/api-contract-testing.md` |  |
| [ ] | `skills/testing/async-testing.md` |  |
| [ ] | `skills/testing/coverage-ratchet.py` |  |
| [ ] | `skills/testing/flaky-detector.py` |  |
| [ ] | `skills/testing/flaky-test-triage.md` |  |
| [ ] | `skills/testing/load-test-basics.md` | recommended |
| [ ] | `skills/testing/pytest-conventions.md` |  |
| [ ] | `skills/testing/regression-harness.md` |  |
| [ ] | `skills/testing/smoke-tests.md` |  |
| [ ] | `skills/testing/snapshot-testing.md` |  |
| [ ] | `skills/testing/test-scaffolder.py` |  |
| [ ] | `skills/testing/validation-loop-design.md` |  |
| [ ] | `spec/spec.md` |  |
| [ ] | `trivy.yaml` |  |

---
## Counts
- **Folders listed:** 70 (per `spec/spec.md` §30)
- **Files listed:** 408 (per `spec/spec.md` §26 + §28 inventory; §32 total **408** enumerated files)
- **§24 reference:** See `spec/spec.md` §24 (implementation checklist — machine operability) for outcome-level acceptance criteria.
