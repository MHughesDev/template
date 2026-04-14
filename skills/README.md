# skills/README.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §13 (Mandatory Skill Search), prompts/skill_searcher.md -->
<!-- - Procedure: docs/procedures/update-or-create-skill.md -->

> PURPOSE: Skills library index. Lists all skills by category with one-line descriptions. This is the primary entry point for the mandatory skill search (AGENTS.md §13). Every agent reads this file before beginning any task. Per spec §26.4 item 39.

## How to Use This Index

> CONTENT: Instructions for agents on how to use this index:
> 1. Run `make skills:list` to see this index (equivalent to reading this file)
> 2. Identify the PRIMARY domain of your task (backend, security, testing, etc.)
> 3. Identify any SECONDARY domains (e.g., backend task may also involve testing and security)
> 4. Read the "When to invoke" section of every relevant skill
> 5. Read the FULL content of every HIGH-relevance skill before planning or coding
> 6. Note machinery files (.py alongside .md) as available automation tools
>
> Reference `prompts/skill_searcher.md` for a structured search subroutine.

## Skill Format

> CONTENT: Brief description of the §6.2 required sections every skill must have:
> - Purpose, When to invoke, Prerequisites, Relevant files/areas
> - Step-by-step method, Command examples, Validation checklist
> - Common failure modes, Handoff expectations
> - Related procedures, Related prompts, Related rules

## Skills by Category

### Initialization (`skills/init/`)
> CONTENT: Table of all init skills. Columns: Skill file, One-line description, Machinery. Rows:
> - idea-validator.md — Validate idea.md completeness before initialization | idea-validator.py
> - archetype-mapper.md — Map archetype+profiles to concrete scaffolding plan | archetype-mapper.py
> - module-template-generator.md — Generate all files for a domain module | (uses module-scaffolder.py from backend)
> - queue-seeder.md — Populate queue.csv from idea.md §12 | queue-seeder.py
> - profile-resolver.md — Resolve profile enablement with dependency checking | profile-resolver.py
> - env-generator.md — Generate .env.example tailored to enabled profiles | env-generator.py

### Agent Operations (`skills/agent-ops/`)
> CONTENT: Table of agent-ops skills:
> - queue-triage.md [FULL] — Read, interpret, and prioritize queue items | queue-triage.py
> - task-planning.md [FULL] — Decompose tasks with acceptance criteria and risks
> - implementation-handoff.md [FULL] — Write complete handoff documents | handoff-template-generator.py
> - blocked-task-recovery.md — Handle blocked items without silently skipping
> - prompt-to-procedure-promotion.md — Promote successful prompts to library
> - rule-refinement-after-mistakes.md — Encode repeated mistakes as rules
> - post-pr-audit.md — Audit completed PRs against acceptance criteria
> - repo-self-audit.md [FULL] — Run comprehensive repo spec-compliance audit | repo-self-audit.py
> - queue-intelligence.md [FULL] — Advanced queue orchestration (DAG, complexity, batches) | queue-intelligence.py

### Repo Governance (`skills/repo-governance/`)
> CONTENT: Table of repo-governance skills:
> - writing-agents-md.md [FULL] — Author or update AGENTS.md per §4
> - authoring-cursor-rules.md [FULL] — Create or update .cursor/rules/ files | rule-linter.py
> - adding-reusable-commands.md — Add Make targets or Cursor commands
> - maintaining-procedural-docs.md — Keep docs/procedures/ current
> - writing-adrs.md — Author Architecture Decision Records | adr-index-generator.py
> - changelogs-release-notes.md — Maintain CHANGELOG.md per Keep a Changelog
> - repository-hygiene.md — Periodic cleanup: stale branches, orphaned docs
> - docs-generator.md [FULL] — Extend and run the documentation generation pipeline | docs-generator.py
> - docs-freshness-checker.py (machinery only)

### Backend / Platform (`skills/backend/`)
> CONTENT: Table of backend skills:
> - fastapi-router-module.md [FULL] — Add a new FastAPI router/module | module-scaffolder.py
> - service-repository-pattern.md [FULL] — Service and repository layer patterns
> - health-readiness-liveness.md — Implement and verify health/ready/live endpoints
> - api-versioning.md — Version API endpoints with URL prefix strategy
> - background-jobs.md — Define and register background jobs via packages/tasks
> - worker-integration.md — Enable worker profile with broker connection
> - idempotent-tasks.md — Design idempotent task handlers
> - configuration-management.md — Add config via BaseSettings correctly
> - feature-flags.md — Implement env-based feature flags
> - error-taxonomy.md — Define and use stable error codes
> - structured-logging.md — Implement structured JSON logging with correlation IDs
> - opentelemetry-tracing.md — Add OpenTelemetry tracing
> - metrics-exposition.md — Expose Prometheus-compatible metrics
> - rate-limiting.md — Implement rate limiting middleware
> - retries-circuit-breakers.md — Retry logic and circuit breakers
> - safe-migration-rollout.md [FULL] — Roll out migrations safely with expand/contract
> - sqlite-to-postgres.md — Migrate from SQLite to PostgreSQL
> - env-var-sync.py, error-code-registry.py, openapi-diff.py (machinery)

### Security / Compliance (`skills/security/`)
> CONTENT: Table of security skills:
> - secret-handling.md [FULL] — Handle secrets: env-only, rotation, detection | secret-scanner.py
> - token-lifecycle.md — JWT issuance, refresh, revocation, key rotation
> - rbac-tenant-isolation.md — Verify RBAC and tenant isolation | tenant-isolation-checker.py
> - dependency-review.md — Review dependency changes for CVEs | dependency-audit.py
> - code-scanning.md — Run and interpret bandit/semgrep results
> - image-scanning.md — Scan container images with Trivy
> - sbom-attestation.md — Generate SBOMs and attestations
> - secure-defaults-review.md — Audit for secure defaults
> - incident-evidence-capture.md — Capture evidence during security incidents

### Testing / Quality (`skills/testing/`)
> CONTENT: Table of testing skills:
> - pytest-conventions.md [FULL] — Pytest conventions, fixtures, markers, coverage | test-scaffolder.py
> - async-testing.md — Test async FastAPI code with pytest-asyncio
> - api-contract-testing.md — API contract tests with schema validation
> - snapshot-testing.md — Snapshot testing for API responses
> - smoke-tests.md — Write and run smoke tests
> - regression-harness.md — Add regression tests after bug fixes
> - load-test-basics.md — Basic load testing with locust/k6
> - flaky-test-triage.md — Identify, isolate, and fix flaky tests | flaky-detector.py
> - validation-loop-design.md — Design validation loops for agent workflows
> - coverage-ratchet.py (machinery only)

### DevOps / Operations (`skills/devops/`)
> CONTENT: Table of devops skills:
> - docker-multi-stage-builds.md — Build efficient multi-stage Docker images | dockerfile-linter.py
> - compose-profiles.md — Manage Docker Compose profiles | compose-profile-matrix.py
> - k8s-probes.md — Configure Kubernetes liveness/readiness/startup probes | k8s-manifest-validator.py
> - rollout-rollback.md — Kubernetes rollouts and rollbacks
> - github-actions-troubleshooting.md — Debug failing GitHub Actions
> - release-promotion.md — Promote releases through dev→staging→prod
> - artifact-publishing.md — Publish container and Python package artifacts
> - environment-configuration.md — Manage environment-specific config
> - backup-restore-drills.md — Backup and restore drills

### AI / RAG (`skills/ai-rag/`) — Optional Profile
> CONTENT: Table of AI skills (all optional):
> - chromadb-ingestion.md — Ingest documents into ChromaDB
> - embedding-refresh.md — Refresh embeddings for updated documents
> - retrieval-evaluation.md — Evaluate retrieval quality
> - prompt-versioning.md — Version AI prompts
> - ai-kill-switch.md — Implement and test AI kill switch
> - model-provider-abstraction.md — Abstract model/provider dependencies
> - ai-safety-review.md — Review AI outputs for safety

### Frontend / Mobile (`skills/frontend/`) — Optional Profiles
> CONTENT: Table of frontend skills (all optional):
> - generated-client-usage.md — Use auto-generated API clients
> - react-api-integration.md — Integrate React with FastAPI
> - expo-auth-storage.md — Handle auth tokens in Expo
> - frontend-env-handling.md — Manage frontend environment variables

## Adding a New Skill

> CONTENT: Brief reference to docs/procedures/update-or-create-skill.md. Summary:
> 1. Choose the correct category directory
> 2. Create skill .md with all §6.2 sections (see skill format above)
> 3. Create machinery .py if applicable
> 4. Update this README index
> 5. PR with validation (make rules:check, make skills:list)
