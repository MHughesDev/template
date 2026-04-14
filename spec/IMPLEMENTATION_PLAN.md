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
| [ ] | `.cursor/` |  |
| [ ] | `.github/` |  |
| [ ] | `apps/` |  |
| [ ] | `deploy/` |  |
| [ ] | `docs/` |  |
| [ ] | `packages/` |  |
| [ ] | `prompts/` |  |
| [ ] | `queue/` |  |
| [ ] | `scripts/` |  |
| [ ] | `skills/` |  |
| [ ] | `spec/` | source of truth for spec |
| [ ] | `.cursor/commands/` |  |
| [ ] | `.cursor/rules/` |  |
| [ ] | `.github/ISSUE_TEMPLATE/` |  |
| [ ] | `.github/workflows/` |  |
| [ ] | `apps/api/` |  |
| [ ] | `apps/mobile/` | optional profile or subtree |
| [ ] | `apps/web/` | optional profile or subtree |
| [ ] | `deploy/docker/` |  |
| [ ] | `deploy/k8s/` |  |
| [ ] | `docs/adr/` |  |
| [ ] | `docs/agents/` |  |
| [ ] | `docs/api/` |  |
| [ ] | `docs/architecture/` |  |
| [ ] | `docs/development/` |  |
| [ ] | `docs/getting-started/` |  |
| [ ] | `docs/operations/` |  |
| [ ] | `docs/optional-clients/` | optional profile or subtree |
| [ ] | `docs/procedures/` |  |
| [ ] | `docs/prompts/` |  |
| [ ] | `docs/quality/` |  |
| [ ] | `docs/queue/` |  |
| [ ] | `docs/release/` |  |
| [ ] | `docs/repo-governance/` |  |
| [ ] | `docs/runbooks/` |  |
| [ ] | `docs/security/` |  |
| [ ] | `packages/ai/` | optional profile or subtree |
| [ ] | `packages/contracts/` |  |
| [ ] | `packages/tasks/` |  |
| [ ] | `skills/agent-ops/` |  |
| [ ] | `skills/ai-rag/` | optional profile or subtree |
| [ ] | `skills/backend/` |  |
| [ ] | `skills/devops/` |  |
| [ ] | `skills/frontend/` | optional profile or subtree |
| [ ] | `skills/init/` |  |
| [ ] | `skills/repo-governance/` |  |
| [ ] | `skills/security/` |  |
| [ ] | `skills/testing/` |  |
| [ ] | `apps/api/alembic/` |  |
| [ ] | `apps/api/src/` |  |
| [ ] | `apps/api/tests/` |  |
| [ ] | `deploy/k8s/base/` |  |
| [ ] | `deploy/k8s/overlays/` |  |
| [ ] | `apps/api/alembic/versions/` |  |
| [ ] | `apps/api/src/auth/` |  |
| [ ] | `apps/api/src/health/` |  |
| [ ] | `apps/api/src/tenancy/` |  |
| [ ] | `deploy/k8s/overlays/dev/` |  |
| [ ] | `deploy/k8s/overlays/prod/` |  |
| [ ] | `deploy/k8s/overlays/staging/` |  |

---
## File checklist
| Created | Path | Notes |
|:-------:|------|-------|
| [ ] | `AGENTS.md` |  |
| [ ] | `README.md` |  |
| [ ] | `idea.md` |  |
| [ ] | `CHANGELOG.md` |  |
| [ ] | `.env.example` |  |
| [ ] | `docker-compose.yml` |  |
| [ ] | `Makefile` |  |
| [ ] | `pyproject.toml` |  |
| [ ] | `LICENSE` |  |
| [ ] | `CONTRIBUTING.md` |  |
| [ ] | `CODE_OF_CONDUCT.md` | optional |
| [ ] | `.cursor/rules/global.md` |  |
| [ ] | `.cursor/rules/apps-api.md` |  |
| [ ] | `.cursor/rules/security.md` |  |
| [ ] | `.cursor/rules/queue.md` |  |
| [ ] | `.cursor/rules/testing.md` | optional |
| [ ] | `.cursor/rules/documentation.md` | optional |
| [ ] | `.cursor/rules/initialization.md` |  |
| [ ] | `.cursor/rules/skills.md` |  |
| [ ] | `.cursor/rules/prompts.md` |  |
| [ ] | `.cursor/commands/validate.md` | optional |
| [ ] | `.cursor/commands/queue-next.md` | optional |
| [ ] | `.cursor/commands/initialize.md` |  |
| [ ] | `.cursor/commands/scaffold-module.md` |  |
| [ ] | `.cursor/commands/audit.md` |  |
| [ ] | `prompts/README.md` |  |
| [ ] | `prompts/repo_initializer.md` |  |
| [ ] | `prompts/domain_modeler.md` |  |
| [ ] | `prompts/profile_configurator.md` |  |
| [ ] | `prompts/task_planner.md` |  |
| [ ] | `prompts/implementation_agent.md` |  |
| [ ] | `prompts/reviewer_critic.md` |  |
| [ ] | `prompts/test_writer.md` |  |
| [ ] | `prompts/debugger.md` |  |
| [ ] | `prompts/refactorer.md` |  |
| [ ] | `prompts/documentation_updater.md` |  |
| [ ] | `prompts/migration_author.md` |  |
| [ ] | `prompts/queue_processor.md` |  |
| [ ] | `prompts/release_manager.md` |  |
| [ ] | `prompts/dependency_upgrade_agent.md` |  |
| [ ] | `prompts/security_review_agent.md` |  |
| [ ] | `prompts/incident_triage_agent.md` |  |
| [ ] | `prompts/performance_audit_agent.md` |  |
| [ ] | `prompts/repo_bootstrap_agent.md` |  |
| [ ] | `prompts/spec_hardening_agent.md` |  |
| [ ] | `prompts/skill_authoring_agent.md` |  |
| [ ] | `prompts/rule_authoring_agent.md` |  |
| [ ] | `skills/README.md` |  |
| [ ] | `skills/init/README.md` |  |
| [ ] | `skills/init/idea-validator.md` |  |
| [ ] | `skills/init/idea-validator.py` |  |
| [ ] | `skills/init/archetype-mapper.md` |  |
| [ ] | `skills/init/archetype-mapper.py` |  |
| [ ] | `skills/init/module-template-generator.md` |  |
| [ ] | `skills/init/queue-seeder.md` |  |
| [ ] | `skills/init/queue-seeder.py` |  |
| [ ] | `skills/init/profile-resolver.md` |  |
| [ ] | `skills/init/profile-resolver.py` |  |
| [ ] | `skills/init/env-generator.md` |  |
| [ ] | `skills/init/env-generator.py` |  |
| [ ] | `skills/agent-ops/queue-triage.md` |  |
| [ ] | `skills/agent-ops/queue-triage.py` |  |
| [ ] | `skills/agent-ops/task-planning.md` |  |
| [ ] | `skills/agent-ops/implementation-handoff.md` |  |
| [ ] | `skills/agent-ops/handoff-template-generator.py` |  |
| [ ] | `skills/agent-ops/blocked-task-recovery.md` |  |
| [ ] | `skills/agent-ops/prompt-to-procedure-promotion.md` |  |
| [ ] | `skills/agent-ops/rule-refinement-after-mistakes.md` |  |
| [ ] | `skills/agent-ops/post-pr-audit.md` |  |
| [ ] | `skills/agent-ops/repo-self-audit.md` |  |
| [ ] | `skills/agent-ops/repo-self-audit.py` |  |
| [ ] | `skills/repo-governance/writing-agents-md.md` |  |
| [ ] | `skills/repo-governance/authoring-cursor-rules.md` |  |
| [ ] | `skills/repo-governance/adding-reusable-commands.md` |  |
| [ ] | `skills/repo-governance/maintaining-procedural-docs.md` |  |
| [ ] | `skills/repo-governance/writing-adrs.md` |  |
| [ ] | `skills/repo-governance/changelogs-release-notes.md` |  |
| [ ] | `skills/repo-governance/repository-hygiene.md` |  |
| [ ] | `skills/repo-governance/rule-linter.py` |  |
| [ ] | `skills/repo-governance/docs-freshness-checker.py` |  |
| [ ] | `skills/repo-governance/adr-index-generator.py` |  |
| [ ] | `skills/backend/fastapi-router-module.md` |  |
| [ ] | `skills/backend/service-repository-pattern.md` |  |
| [ ] | `skills/backend/health-readiness-liveness.md` |  |
| [ ] | `skills/backend/api-versioning.md` |  |
| [ ] | `skills/backend/background-jobs.md` |  |
| [ ] | `skills/backend/worker-integration.md` |  |
| [ ] | `skills/backend/idempotent-tasks.md` |  |
| [ ] | `skills/backend/configuration-management.md` |  |
| [ ] | `skills/backend/feature-flags.md` |  |
| [ ] | `skills/backend/error-taxonomy.md` |  |
| [ ] | `skills/backend/structured-logging.md` |  |
| [ ] | `skills/backend/opentelemetry-tracing.md` |  |
| [ ] | `skills/backend/metrics-exposition.md` |  |
| [ ] | `skills/backend/rate-limiting.md` |  |
| [ ] | `skills/backend/retries-circuit-breakers.md` |  |
| [ ] | `skills/backend/safe-migration-rollout.md` |  |
| [ ] | `skills/backend/sqlite-to-postgres.md` |  |
| [ ] | `skills/backend/module-scaffolder.py` |  |
| [ ] | `skills/backend/error-code-registry.py` |  |
| [ ] | `skills/backend/env-var-sync.py` |  |
| [ ] | `skills/backend/openapi-diff.py` | optional |
| [ ] | `skills/security/secret-handling.md` |  |
| [ ] | `skills/security/token-lifecycle.md` |  |
| [ ] | `skills/security/rbac-tenant-isolation.md` |  |
| [ ] | `skills/security/dependency-review.md` |  |
| [ ] | `skills/security/code-scanning.md` |  |
| [ ] | `skills/security/image-scanning.md` |  |
| [ ] | `skills/security/sbom-attestation.md` | optional |
| [ ] | `skills/security/secure-defaults-review.md` |  |
| [ ] | `skills/security/incident-evidence-capture.md` |  |
| [ ] | `skills/security/secret-scanner.py` |  |
| [ ] | `skills/security/dependency-audit.py` |  |
| [ ] | `skills/security/tenant-isolation-checker.py` |  |
| [ ] | `skills/testing/pytest-conventions.md` |  |
| [ ] | `skills/testing/async-testing.md` |  |
| [ ] | `skills/testing/api-contract-testing.md` |  |
| [ ] | `skills/testing/snapshot-testing.md` |  |
| [ ] | `skills/testing/smoke-tests.md` |  |
| [ ] | `skills/testing/regression-harness.md` |  |
| [ ] | `skills/testing/load-test-basics.md` | optional |
| [ ] | `skills/testing/flaky-test-triage.md` |  |
| [ ] | `skills/testing/validation-loop-design.md` |  |
| [ ] | `skills/testing/test-scaffolder.py` |  |
| [ ] | `skills/testing/coverage-ratchet.py` |  |
| [ ] | `skills/testing/flaky-detector.py` | optional |
| [ ] | `skills/devops/docker-multi-stage-builds.md` |  |
| [ ] | `skills/devops/compose-profiles.md` |  |
| [ ] | `skills/devops/k8s-probes.md` |  |
| [ ] | `skills/devops/rollout-rollback.md` |  |
| [ ] | `skills/devops/github-actions-troubleshooting.md` |  |
| [ ] | `skills/devops/release-promotion.md` |  |
| [ ] | `skills/devops/artifact-publishing.md` |  |
| [ ] | `skills/devops/environment-configuration.md` |  |
| [ ] | `skills/devops/backup-restore-drills.md` | optional |
| [ ] | `skills/devops/dockerfile-linter.py` |  |
| [ ] | `skills/devops/k8s-manifest-validator.py` |  |
| [ ] | `skills/devops/compose-profile-matrix.py` | optional |
| [ ] | `skills/ai-rag/chromadb-ingestion.md` | optional |
| [ ] | `skills/ai-rag/embedding-refresh.md` | optional |
| [ ] | `skills/ai-rag/retrieval-evaluation.md` | optional |
| [ ] | `skills/ai-rag/prompt-versioning.md` | optional |
| [ ] | `skills/ai-rag/ai-kill-switch.md` | optional |
| [ ] | `skills/ai-rag/model-provider-abstraction.md` | optional |
| [ ] | `skills/ai-rag/ai-safety-review.md` | optional |
| [ ] | `skills/frontend/generated-client-usage.md` | optional |
| [ ] | `skills/frontend/react-api-integration.md` | optional |
| [ ] | `skills/frontend/expo-auth-storage.md` | optional |
| [ ] | `skills/frontend/frontend-env-handling.md` | optional |
| [ ] | `docs/README.md` |  |
| [ ] | `docs/getting-started/README.md` |  |
| [ ] | `docs/getting-started/prerequisites.md` |  |
| [ ] | `docs/getting-started/quickstart.md` |  |
| [ ] | `docs/architecture/README.md` |  |
| [ ] | `docs/architecture/modular-monolith.md` |  |
| [ ] | `docs/architecture/data-layer.md` |  |
| [ ] | `docs/architecture/auth-multi-tenancy.md` |  |
| [ ] | `docs/architecture/ai-rag-chromadb.md` | optional |
| [ ] | `docs/architecture/system-context.md` |  |
| [ ] | `docs/architecture/domain-model.md` |  |
| [ ] | `docs/architecture/api-design.md` |  |
| [ ] | `docs/development/README.md` |  |
| [ ] | `docs/development/local-setup.md` |  |
| [ ] | `docs/development/coding-standards.md` |  |
| [ ] | `docs/development/testing-guide.md` |  |
| [ ] | `docs/development/environment-vars.md` |  |
| [ ] | `docs/development/module-patterns.md` |  |
| [ ] | `docs/development/dependency-management.md` |  |
| [ ] | `docs/api/README.md` |  |
| [ ] | `docs/api/endpoints.md` |  |
| [ ] | `docs/api/error-codes.md` |  |
| [ ] | `docs/operations/README.md` |  |
| [ ] | `docs/operations/docker.md` |  |
| [ ] | `docs/operations/kubernetes.md` |  |
| [ ] | `docs/operations/observability.md` |  |
| [ ] | `docs/operations/backups.md` |  |
| [ ] | `docs/operations/rollback.md` |  |
| [ ] | `docs/operations/configuration.md` |  |
| [ ] | `docs/operations/health-checks.md` |  |
| [ ] | `docs/security/README.md` |  |
| [ ] | `docs/security/threat-model-stub.md` |  |
| [ ] | `docs/security/secrets-management.md` |  |
| [ ] | `docs/security/incident-response.md` |  |
| [ ] | `docs/security/token-lifecycle.md` |  |
| [ ] | `docs/procedures/README.md` |  |
| [ ] | `docs/procedures/initialize-repo.md` |  |
| [ ] | `docs/procedures/scaffold-domain-module.md` |  |
| [ ] | `docs/procedures/enable-profile.md` |  |
| [ ] | `docs/procedures/validate-idea-md.md` |  |
| [ ] | `docs/procedures/start-queue-item.md` |  |
| [ ] | `docs/procedures/plan-change.md` |  |
| [ ] | `docs/procedures/implement-change.md` |  |
| [ ] | `docs/procedures/validate-change.md` |  |
| [ ] | `docs/procedures/open-pull-request.md` |  |
| [ ] | `docs/procedures/handoff.md` |  |
| [ ] | `docs/procedures/archive-queue-item.md` |  |
| [ ] | `docs/procedures/handle-blocked-work.md` |  |
| [ ] | `docs/procedures/update-documentation.md` |  |
| [ ] | `docs/procedures/update-or-create-skill.md` |  |
| [ ] | `docs/procedures/update-or-create-rule.md` |  |
| [ ] | `docs/procedures/dependency-upgrade.md` |  |
| [ ] | `docs/procedures/database-migration.md` |  |
| [ ] | `docs/procedures/release-preparation.md` |  |
| [ ] | `docs/procedures/incident-rollback.md` |  |
| [ ] | `docs/procedures/extract-service-from-monolith.md` |  |
| [ ] | `docs/procedures/add-optional-app-profile.md` |  |
| [ ] | `docs/procedures/add-queue-category.md` |  |
| [ ] | `docs/procedures/add-prompt-template.md` |  |
| [ ] | `docs/adr/README.md` |  |
| [ ] | `docs/adr/template.md` |  |
| [ ] | `docs/agents/README.md` |  |
| [ ] | `docs/agents/initialization-guide.md` |  |
| [ ] | `docs/agents/supervision-guide.md` |  |
| [ ] | `docs/agents/reviewing-ai-diffs.md` |  |
| [ ] | `docs/agents/pr-audit-checklist.md` |  |
| [ ] | `docs/agents/quality-ratcheting.md` |  |
| [ ] | `docs/agents/evolving-from-incidents.md` |  |
| [ ] | `docs/prompts/README.md` |  |
| [ ] | `docs/prompts/conventions.md` |  |
| [ ] | `docs/prompts/index.md` |  |
| [ ] | `docs/runbooks/README.md` |  |
| [ ] | `docs/runbooks/api-down.md` |  |
| [ ] | `docs/runbooks/db-failure.md` |  |
| [ ] | `docs/runbooks/jwt-key-rotation.md` |  |
| [ ] | `docs/runbooks/chroma-unavailable.md` | optional |
| [ ] | `docs/release/README.md` |  |
| [ ] | `docs/release/versioning.md` |  |
| [ ] | `docs/release/promotion.md` |  |
| [ ] | `docs/release/changelog-guide.md` |  |
| [ ] | `docs/repo-governance/README.md` |  |
| [ ] | `docs/repo-governance/improvement-loops.md` |  |
| [ ] | `docs/repo-governance/audits.md` |  |
| [ ] | `docs/repo-governance/procedure-drift-detection.md` |  |
| [ ] | `docs/repo-governance/documentation-freshness.md` |  |
| [ ] | `docs/quality/README.md` |  |
| [ ] | `docs/quality/testing-strategy.md` |  |
| [ ] | `docs/quality/coverage-policy.md` |  |
| [ ] | `docs/quality/flake-policy.md` |  |
| [ ] | `docs/queue/queue-system-overview.md` |  |
| [ ] | `docs/queue/queue-categories.md` |  |
| [ ] | `docs/optional-clients/web.md` | optional |
| [ ] | `docs/optional-clients/mobile.md` | optional |
| [ ] | `queue/queue.csv` |  |
| [ ] | `queue/queuearchive.csv` |  |
| [ ] | `queue/QUEUE_INSTRUCTIONS.md` |  |
| [ ] | `queue/QUEUE_AGENT_PROMPT.md` |  |
| [ ] | `queue/queue.lock` | optional |
| [ ] | `queue/audit.log` | optional |
| [ ] | `.github/workflows/ci.yml` |  |
| [ ] | `.github/workflows/cd.yml` |  |
| [ ] | `.github/workflows/security.yml` |  |
| [ ] | `.github/ISSUE_TEMPLATE/bug_report.md` |  |
| [ ] | `.github/ISSUE_TEMPLATE/feature_request.md` |  |
| [ ] | `.github/ISSUE_TEMPLATE/queue_item.md` | optional |
| [ ] | `.github/PULL_REQUEST_TEMPLATE.md` |  |
| [ ] | `.github/CODEOWNERS` |  |
| [ ] | `.github/dependabot.yml` |  |
| [ ] | `.github/labels.yml` | optional |
| [ ] | `apps/api/AGENTS.md` |  |
| [ ] | `apps/api/Dockerfile` |  |
| [ ] | `apps/api/alembic.ini` |  |
| [ ] | `apps/api/alembic/env.py` |  |
| [ ] | `apps/api/alembic/script.py.mako` |  |
| [ ] | `apps/api/alembic/versions/.gitkeep` |  |
| [ ] | `apps/api/src/__init__.py` |  |
| [ ] | `apps/api/src/main.py` |  |
| [ ] | `apps/api/src/config.py` |  |
| [ ] | `apps/api/src/database.py` |  |
| [ ] | `apps/api/src/middleware.py` |  |
| [ ] | `apps/api/src/health/__init__.py` |  |
| [ ] | `apps/api/src/health/router.py` |  |
| [ ] | `apps/api/src/auth/__init__.py` |  |
| [ ] | `apps/api/src/auth/router.py` |  |
| [ ] | `apps/api/src/auth/models.py` |  |
| [ ] | `apps/api/src/auth/schemas.py` |  |
| [ ] | `apps/api/src/auth/service.py` |  |
| [ ] | `apps/api/src/auth/dependencies.py` |  |
| [ ] | `apps/api/src/tenancy/__init__.py` |  |
| [ ] | `apps/api/src/tenancy/middleware.py` |  |
| [ ] | `apps/api/src/tenancy/models.py` |  |
| [ ] | `apps/api/tests/__init__.py` |  |
| [ ] | `apps/api/tests/conftest.py` |  |
| [ ] | `apps/api/tests/test_health.py` |  |
| [ ] | `apps/api/tests/test_auth.py` |  |
| [ ] | `apps/web/README.md` | optional |
| [ ] | `apps/web/AGENTS.md` | optional |
| [ ] | `apps/mobile/README.md` | optional |
| [ ] | `apps/mobile/AGENTS.md` | optional |
| [ ] | `packages/contracts/__init__.py` |  |
| [ ] | `packages/contracts/models.py` |  |
| [ ] | `packages/contracts/AGENTS.md` |  |
| [ ] | `packages/tasks/__init__.py` |  |
| [ ] | `packages/tasks/interfaces.py` |  |
| [ ] | `packages/tasks/AGENTS.md` |  |
| [ ] | `packages/ai/__init__.py` | optional |
| [ ] | `packages/ai/interfaces.py` | optional |
| [ ] | `packages/ai/chromadb_client.py` | optional |
| [ ] | `packages/ai/AGENTS.md` | optional |
| [ ] | `deploy/docker/README.md` |  |
| [ ] | `deploy/k8s/README.md` |  |
| [ ] | `deploy/k8s/base/deployment.yaml` |  |
| [ ] | `deploy/k8s/base/service.yaml` |  |
| [ ] | `deploy/k8s/base/configmap.yaml` |  |
| [ ] | `deploy/k8s/base/kustomization.yaml` |  |
| [ ] | `deploy/k8s/overlays/dev/kustomization.yaml` |  |
| [ ] | `deploy/k8s/overlays/staging/kustomization.yaml` |  |
| [ ] | `deploy/k8s/overlays/prod/kustomization.yaml` |  |
| [ ] | `scripts/README.md` |  |
| [ ] | `scripts/dev.sh` |  |
| [ ] | `scripts/lint.sh` |  |
| [ ] | `scripts/fmt.sh` |  |
| [ ] | `scripts/typecheck.sh` |  |
| [ ] | `scripts/test.sh` |  |
| [ ] | `scripts/migrate.sh` |  |
| [ ] | `scripts/docs-check.sh` |  |
| [ ] | `scripts/docs-index.sh` | optional |
| [ ] | `scripts/queue-peek.sh` |  |
| [ ] | `scripts/queue-validate.sh` |  |
| [ ] | `scripts/queue-archive.sh` | optional |
| [ ] | `scripts/prompt-list.sh` |  |
| [ ] | `scripts/skills-list.sh` |  |
| [ ] | `scripts/rules-check.sh` |  |
| [ ] | `scripts/audit-self.sh` |  |
| [ ] | `scripts/security-scan.sh` |  |
| [ ] | `scripts/image-build.sh` |  |
| [ ] | `scripts/image-scan.sh` |  |
| [ ] | `scripts/release-prepare.sh` |  |
| [ ] | `scripts/release-verify.sh` |  |
| [ ] | `scripts/k8s-render.sh` |  |
| [ ] | `scripts/k8s-validate.sh` |  |
| [ ] | `scripts/init-repo.sh` |  |
| [ ] | `scripts/validate-idea.sh` |  |
| [ ] | `scripts/scaffold-module.sh` |  |
| [ ] | `scripts/profile-enable.sh` |  |
| [ ] | `scripts/idea-to-queue.sh` | optional |
| [ ] | `scripts/generate-env.sh` |  |
| [ ] | `scripts/inventory-check.sh` |  |
| [ ] | `spec/spec.md` |  |

---
## Counts
- **Folders listed:** 60
- **Files listed:** 338 (per §29 expanded tree; §28.10 total **338** new paths)
- **§24 reference:** See `spec/spec.md` §24 (implementation checklist — machine operability) for outcome-level acceptance criteria.
