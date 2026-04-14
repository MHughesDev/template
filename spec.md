# Template Repository Specification — Agent-Operated Machine

**Version:** 3.0  
**Stack:** Python 3.12+, FastAPI, optional React/Expo front-ends  
**Primary operators:** Coding agents (Cursor and compatible tooling). Humans are **reviewers, supervisors, and policy maintainers**, not the default execution path.

This document is the **authoritative specification** for a batteries-included template repository designed as a **Cursor-first, agentic-coding-centric repository machine**: a software factory where subsystems have explicit **purpose, inputs, outputs, invariants, commands, failure modes, tests, related prompts, and handoff rules**.

Implementers treat this spec as a **checklist and process contract**. Ambiguity and tribal knowledge are **failure modes**; recurring work must become **documented, reusable machine procedures** (prompts, skills, rules, commands, checklists, tests).

**Canonical specification:** **`spec.md`** (this file). Use it for copy, version control, releases, and attachments.

---

## Instruction hierarchy and precedence

When instructions conflict, agents **resolve in this order** (higher overrides lower):

1. **Explicit task prompt** for the current run (user message, issue comment, or single-task injection).  
2. **Root `AGENTS.md`** — repo-wide operating contract.  
3. **Scoped agent instruction files** — e.g. `apps/api/AGENTS.md`, `packages/contracts/AGENTS.md` (directory-local constraints).  
4. **`.cursor/rules`** (global and path-scoped rules).  
5. **`docs/procedures/`** — canonical operational workflows for named situations.  
6. **`skills/`** — reusable execution knowledge for specialized tasks.  
7. **`prompts/`** (or equivalent catalog) — reusable invocation templates.  
8. **General documentation** under `docs/` (conceptual reference; does not override policy files above).

**Conflict handling:** If two sources at the same rank disagree, **stop and escalate** per `AGENTS.md` (do not guess). Maintainers fix the conflict by editing the higher-precedence artifact or demoting duplicate guidance.

---

## 1. Positioning: repository as operating system for agents

### 1.1 Core intent

The **center of gravity is coding agents**, not humans typing application code by default. The repository must enable agents to reliably:

- Understand the system (structure, contracts, policies).  
- Plan work with explicit acceptance criteria and scope bounds.  
- Execute changes through **canonical commands** and small validated increments.  
- Validate outcomes (tests, linters, type checks, smoke checks, security scans as applicable).  
- Hand off results with **machine-readable traces** (PR description, notes, queue state, logs of commands run).  
- Update documentation when behavior or operational assumptions change.  
- Update **queue state** according to strict lifecycle rules.  
- Leave **evidence**: what changed, why, how it was verified, residual risks.

**Deterministic commands and validation loops** are preferred over informal prose. **“Figure it out”** is not a strategy; **“run X, expect Y, else Z”** is.

### 1.2 Humans

Humans **define policy** (`AGENTS.md`, rules, procedures), **review** diffs and risk, **approve** deployments and migrations, and **maintain** the machine (skills, prompts, CI/CD). Humans may execute work, but the repo must not *depend* on informal human habit.

### 1.3 Machine subsystems (conceptual)

Each major subsystem MUST be describable as:

| Aspect | Requirement |
|--------|----------------|
| Purpose | One paragraph, outcome-oriented. |
| Inputs | Config, env vars, files, queue rows, API calls. |
| Outputs | Artifacts, side effects, observability signals. |
| Invariants | What must never break (security, data, SLO). |
| Commands | Links to canonical `make` / `task` targets or scripts. |
| Failure modes | What breaks, how it surfaces, first response. |
| Tests | What proves correctness; where they live. |
| Related prompts | Entries in `prompts/` or procedure links. |
| Handoff rules | What the next agent or human must see. |

### 1.4 Philosophy retained (hardened)

- **Cursor-first:** `.cursor/` is a **machine-control layer**, not a junk drawer.  
- **GitHub-centric:** Issues, PRs, Actions, environments, and branch protection are part of the machine.  
- **Backend-first:** FastAPI modular monolith is the source of truth; optional web/mobile are **profiles**.  
- **Modular monolith → microservices:** boundaries and contracts first; split only with documented criteria.  
- **Docker/Kubernetes:** default path for parity and production shapes.  
- **Queue-driven agent work:** CSV queue is an **operating lane** with strict lifecycle.  
- **Strong docs:** conceptual + operational docs for every subsystem; **procedures** are first-class.

### 1.5 Goals (agentic)

- Minimize ambiguity: **prefer explicit procedures and commands** over implied convention.  
- Make **every recurring workflow** a documented, reusable **machine procedure** in `docs/procedures/`.  
- Encode learning from **repeated mistakes** into **rules, skills, prompts, procedures, tests** — not memory.  
- Support **CI** (validate everything meaningful on change) and **CD** (deploy only through defined gates).  
- Maintain **optional** web/mobile; core is API + platform.  
- Ship **authentication** (email/password, JWT, optional multi-tenant org SSO) as **policy-complete stubs** with extension points.  
- Use **SQLite** for single-node / dev / constrained MVP; **PostgreSQL** for production-grade multi-instance and concurrency.  
- Use **ChromaDB** for AI/RAG when enabled, behind `packages/ai/` interfaces.

### 1.6 Non-goals

- Mandating one public cloud; stay **portable** (K8s + containers + standard data stores).  
- Shipping a full product UI kit for optional front-ends.  
- Replacing GitHub Issues with the CSV queue for **product backlog** — the queue is **agent work orchestration**, not a PM system.

---

## 2. First-class artifacts (required inventory)

The following MUST exist in a generated template (stubs allowed where noted):

| Artifact | Role |
|----------|------|
| `idea.md` | Project intake form: singular input for repo initialization. Defines project identity, archetype, domain model, profiles, auth, data, integrations, API design, NFRs, deployment, queue seed, constraints, risks. |
| `AGENTS.md` (root) | Top-level control plane: mission, hierarchy, workflows, validation, queue, escalation. |
| `.cursor/rules/` | Persistent constraints; path-scoped as repo grows. |
| `.cursor/commands/` or equivalent | Optional: command metadata / reusable Cursor commands if supported by tooling. |
| `skills/` | Executable playbooks (see §6). |
| `prompts/` | Reusable prompt templates with metadata (see §7). |
| `docs/procedures/` | Canonical SOPs for agents (see §8). |
| `docs/agents/` | Agent onboarding, supervision, review guidance for humans. |
| `docs/prompts/` | Index and conventions for the prompt library. |
| `docs/adr/` | Architecture Decision Records. |
| `docs/runbooks/` | Operational runbooks (failure modes, dashboards, contacts). |
| `docs/release/` | Release promotion, versioning, tagging. |
| `docs/repo-governance/` | Improvement loops, audits, ratcheting quality. |
| `docs/quality/` | Testing strategy, flake policy, coverage expectations. |
| `docs/security/incident-response.md` | IR steps, evidence, comms placeholders. |
| `docs/operations/rollback.md` | Rollback and forward-fix decision tree. |
| `queue/queue.csv` | Open items; **top data row = sole active item**. |
| `queue/queuearchive.csv` | Completed/cancelled/superseded rows; append-only. |
| `queue/QUEUE_INSTRUCTIONS.md` | Human + agent queue SOP. |
| `queue/QUEUE_AGENT_PROMPT.md` | Executable behavior contract for queue processors. |
| `.github/` | CI/CD, templates, Dependabot, CODEOWNERS. |
| `apps/`, `packages/`, `deploy/` | As in topology §3. |

---

## 3. Repository topology (high level)

```
repo-root/
├── idea.md                     # REQUIRED: project intake form (fill before init)
├── AGENTS.md                   # REQUIRED: repo-wide agent control plane
├── .cursor/
│   ├── rules/                  # Global + scoped rules (mdc/md)
│   └── commands/               # Optional: Cursor command definitions
├── .github/
├── prompts/                    # REQUIRED: prompt catalog (templates + metadata)
├── apps/
│   ├── api/                    # FastAPI modular monolith (primary)
│   ├── web/                    # Optional profile
│   └── mobile/                 # Optional profile
├── packages/
├── deploy/
│   ├── docker/
│   └── k8s/
├── docs/                       # Expanded tree — §9
├── queue/
├── skills/
├── scripts/                    # Implementations backing Make/Task targets
├── .env.example
├── docker-compose.yml
├── Makefile or Taskfile        # REQUIRED: single canonical entrypoint style
├── pyproject.toml
├── spec.md                     # Canonical full specification (this document)
└── README.md                   # Quickstart; links to AGENTS.md and docs/
```

**Optional:** `apps/<app>/AGENTS.md` and `packages/<pkg>/AGENTS.md` when those subtrees grow — **root `AGENTS.md` remains supreme** for repo-wide policy unless a scoped file explicitly narrows scope (never contradicts root).

**Naming:** Default queue directory is `queue/`; preserve file names `queue.csv` and `queuearchive.csv` even if the directory is renamed.

---

## 4. `AGENTS.md` (root) — specification

`AGENTS.md` is **one of the most important files in the repository**. It is the **default policy surface** for agents when no higher precedence than general docs applies.

It MUST contain at least these sections (headings may vary; content must exist):

### 4.1 Required sections

1. **Repository mission and operating philosophy** — agent-primary; humans as reviewers; evidence-first.  
2. **Instruction hierarchy** — short pointer to this spec’s precedence table; link to **`spec.md`** (canonical full spec).  
3. **Required workflow for agents** — read order: `AGENTS.md` → task → queue instructions if queue work → relevant docs/files → plan → implement → validate → handoff.  
4. **Branch and PR policy** — naming (`cursor/…` or `queue/<id>-…` per queue rules), one logical change per PR where possible, required checks green.  
5. **Planning before coding** — restate acceptance criteria; list files to touch; name risks; scope bounds.  
6. **Scope control** — no silent scope creep; out-of-scope findings become new queue rows or issues.  
7. **Validation before handoff** — minimum commands (see §10); when to add tests; documentation update triggers.  
8. **Documentation update requirements** — when behavior, env vars, or ops steps change.  
9. **Queue interaction rules** — pointer to `queue/QUEUE_INSTRUCTIONS.md`; top row semantics; blocked vs done.  
10. **When to create or update skills, rules, prompts, procedures** — if the same class of work or mistake appears twice, encode it.  
11. **Escalation of uncertainty** — stop; document unknowns in PR or queue `notes`; do not guess security or tenancy semantics.  
12. **Anti-patterns and forbidden behaviors** — e.g. committing secrets, bypassing CI, editing queue without lifecycle rules, “fixing unrelated bugs” in the same change without approval.

### 4.2 Navigation and machine interface

`AGENTS.md` MUST guide agents on:

- How to **navigate** the repo (where API code, packages, deploy, docs live).  
- Which **canonical commands** to run (`make` / `task` targets), and that **ad hoc commands are disfavored** when a canonical target exists.  
- How to **validate** changes (lint, typecheck, tests, smoke, optional security).  
- How to **update queue state** (archive, blocked, notes).  
- How to **write handoffs** — commands run with key output, files changed, PR link, residual risks.  
- How to decide whether **docs, tests, skills, rules** need updates alongside code.

---

## 5. `.cursor/` — machine-control layer

### 5.1 Contents

- **`rules/`** — Always-on or path-scoped **constraints**: style, security, tenancy, API versioning, queue invariants.  
- **`commands/`** (optional) — Shortcuts that invoke **canonical** scripts or document exact command lines; must not fork behavior that contradicts `Makefile`/`Taskfile`.

### 5.2 When to add what

| Need | Use |
|------|-----|
| “Never do X” or “Always do Y in subtree Z” | Rule (`.cursor/rules`) |
| Repeatable multi-step execution with validation | Skill (`skills/`) + procedure (`docs/procedures/`) |
| A named workflow with triggers and artifacts | Procedure (`docs/procedures/`) |
| LLM invocation template for a role | Prompt (`prompts/`) |
| Repo-wide policy and precedence | `AGENTS.md` |

**After repeated agent mistakes**, maintainers MUST improve **at least one** of: rules, skills, prompts, procedures, tests — **not** “be more careful.”

---

## 6. `skills/` — expanded operational requirements

### 6.1 Quantitative requirements

- **At least 40 skill stubs**: title, outline, when to invoke, prerequisites, links to related areas.  
- **At least 10 fully written, production-usable skills** with complete sections (below).

### 6.2 Required structure per skill

Every skill (stubs may omit some fields but must list them as TODO) MUST be designed to support:

- **Purpose**  
- **When to invoke**  
- **Prerequisites** (tools, env, prior reads)  
- **Relevant files / areas**  
- **Step-by-step method**  
- **Command examples** (canonical targets preferred)  
- **Validation checklist**  
- **Common failure modes**  
- **Handoff expectations**  
- **Related procedures** (`docs/procedures/`)  
- **Related prompts** (`prompts/`)  
- **Related rules** (`.cursor/rules`)

Skills are **executable**, not essays: short steps, checkboxes, explicit commands.

### 6.3 Coverage categories (minimum)

The stub set MUST include coverage across:

**Agent operations:** queue triage, task planning, implementation handoff, blocked-task recovery, prompt-to-procedure promotion, rule refinement after mistakes, post-PR audit, repo self-audit.

**Repo governance:** writing `AGENTS.md`, authoring `.cursor/rules`, adding reusable commands, maintaining procedural docs, ADRs, changelogs/release notes, repository hygiene.

**Backend/platform:** FastAPI router/module patterns, service/repository boundaries, health/readiness/liveness, API versioning, background jobs, worker integration, idempotent tasks, configuration management, feature flags, error taxonomy, structured logging, OpenTelemetry, metrics, tracing hooks, rate limiting, retries, circuit breakers, safe migration rollout, SQLite→Postgres operations.

**Security/compliance:** secret handling, token lifecycle, RBAC/tenant isolation checks, dependency review, code scanning, image scanning, SBOM/attestation (as applicable), secure defaults review, incident evidence capture.

**Testing/quality:** pytest conventions, async testing, API contract testing, snapshots, smoke tests, regression harness, load-test basics, flaky test triage, validation loop design.

**DevOps/operations:** Docker multi-stage builds, Compose profiles, K8s probes, rollout/rollback, GitHub Actions troubleshooting, release promotion, artifact publishing, environment configuration, backup/restore drills.

**AI/RAG:** ChromaDB ingestion, embedding refresh, retrieval evaluation, prompt versioning, AI kill switch, model/provider abstraction, AI safety review.

**Optional frontend/mobile:** generated client usage, React API integration, Expo auth storage, frontend env handling.

---

## 7. `prompts/` — built-in prompt infrastructure

### 7.1 Purpose

A **prompt library** (required top-level folder: **`prompts/`**) holds **reusable, versioned templates** for recurring agent roles. **`docs/prompts/`** documents conventions, indexing, and how templates link to procedures and commands.

Repeated successful one-off prompts SHOULD be **promoted** into `prompts/` with metadata.

### 7.2 Metadata per template

Each template MUST include YAML front matter or a paired `.meta.yaml` (choose one convention and document it in `docs/prompts/README.md`) with:

- **purpose**  
- **when_to_use**  
- **required_inputs**  
- **expected_outputs**  
- **validation_expectations**  
- **constraints / non-goals**  
- **linked_commands** (Make/Task targets)  
- **linked_procedures**  
- **linked_skills**

### 7.3 Required templates (minimum)

The library MUST include templates for at least these **roles**:

| Template | Role |
|----------|------|
| `repo_initializer` | Master prompt: read idea.md, scaffold entire repo (§27) |
| `domain_modeler` | Analyze domain model, produce context map and scaffolding plan |
| `profile_configurator` | Enable/disable profiles based on idea.md selections |
| `task_planner` | Decompose work, acceptance criteria, risks |
| `implementation_agent` | Code change execution with scope discipline |
| `reviewer_critic` | Adversarial review against spec and security |
| `test_writer` | Tests aligned to acceptance criteria |
| `debugger` | Systematic isolation of failures |
| `refactorer` | Behavior-preserving structural changes |
| `documentation_updater` | Docs aligned to code and ops |
| `migration_author` | DB migrations with rollback notes |
| `queue_processor` | Single top-row queue execution |
| `release_manager` | Versioning, changelog, release verification |
| `dependency_upgrade_agent` | Safe dep bumps with CI evidence |
| `security_review_agent` | Threat-focused review |
| `incident_triage_agent` | Initial classification and evidence |
| `performance_audit_agent` | Latency/resource review |
| `repo_bootstrap_agent` | New clone to green dev |
| `spec_hardening_agent` | Spec/procedure alignment PRs |
| `skill_authoring_agent` | New or updated skills to standard |
| `rule_authoring_agent` | New or updated rules, scoped |

---

## 8. `docs/procedures/` — standard operating procedures

### 8.1 Purpose

**Procedures** are canonical workflows. They are written **for agents first**, usable by humans. Vague steps are not acceptable: use **ordered steps**, **exact commands or command families**, and **expected artifacts**.

### 8.2 Required procedure documents

At least one procedure file per topic (names illustrative; content required):

| Procedure | Covers |
|-----------|--------|
| `initialize-repo.md` | Full repo initialization from idea.md (§27.4) |
| `scaffold-domain-module.md` | Create bounded context module in apps/api/src/ |
| `enable-profile.md` | Enable optional profile with dependency checking |
| `validate-idea-md.md` | Validate idea.md completeness before initialization |
| `start-queue-item.md` | Claim work, branch, read docs row |
| `plan-change.md` | Planning outputs, scope, risk |
| `implement-change.md` | Editing, commits, incremental validation |
| `validate-change.md` | Full validation matrix before PR |
| `open-pull-request.md` | Title, description, evidence, labels |
| `handoff.md` | What the next agent/human needs |
| `archive-queue-item.md` | Move row, required fields |
| `handle-blocked-work.md` | Notes, escalation, optional requeue |
| `update-documentation.md` | When and how to edit docs tree |
| `update-or-create-skill.md` | Skill lifecycle |
| `update-or-create-rule.md` | Rule lifecycle |
| `dependency-upgrade.md` | Upgrade + lockfile + CI |
| `database-migration.md` | Alembic, expand/contract, rollback |
| `release-preparation.md` | Changelog, tag, verification |
| `incident-rollback.md` | Tie to `docs/operations/rollback.md` |
| `extract-service-from-monolith.md` | Strangler, contracts, cutover |
| `add-optional-app-profile.md` | e.g. enable `apps/web` |
| `add-queue-category.md` | Category enum, validators, docs |
| `add-prompt-template.md` | Prompt metadata and links |

### 8.3 Required fields per procedure

Each procedure MUST include:

- **Purpose**  
- **Trigger / when to use**  
- **Prerequisites**  
- **Exact commands or command families** (canonical entrypoints)  
- **Ordered steps**  
- **Expected artifacts / outputs**  
- **Validation checks**  
- **Rollback or failure handling**  
- **Handoff expectations**

Each major procedure MUST **link** to relevant **Make/Task** targets (§10).

---

## 9. Documentation (`docs/`) — full structure

```
docs/
├── README.md
├── getting-started/
├── architecture/
├── development/
├── api/
├── operations/
│   ├── docker.md
│   ├── kubernetes.md
│   ├── observability.md
│   ├── backups.md
│   └── rollback.md              # REQUIRED — deploy rollback path
├── security/
│   ├── threat-model-stub.md
│   ├── secrets-management.md
│   └── incident-response.md     # REQUIRED
├── procedures/                  # REQUIRED — §8
├── adr/                         # REQUIRED — decisions index + template
├── agents/                      # REQUIRED — supervision, reviewing AI diffs, auditor role
├── prompts/                     # REQUIRED — index for prompts/
├── runbooks/                    # REQUIRED — service-specific ops
├── release/                     # REQUIRED — promotion, versioning
├── repo-governance/             # REQUIRED — improvement loops, audits
├── quality/                     # REQUIRED — testing/flake/coverage policy
├── queue/
│   └── queue-system-overview.md
└── optional-clients/
    ├── web.md
    └── mobile.md
```

### 9.1 Conceptual + operational pairing

Every **major subsystem** (API, auth, queue, CI/CD, deploy, AI) MUST have:

- **Conceptual** explanation (architecture / why), and  
- **Operational** explanation (how to run, verify, fail, rollback).

### 9.2 Optional subsystems

Every optional profile (web, mobile, workers, Chroma, multi-region, etc.) MUST document:

- **When to enable**  
- **When not to enable**  
- **Operational burden** (cost, complexity, monitoring, failure modes)

### 9.3 Maintainer supervision

`docs/agents/` MUST address:

- How a **human maintainer supervises** agent work  
- How to **review AI-generated diffs** (security, tenancy, scope)  
- How to **audit a PR** against acceptance criteria  
- How to **ratchet quality** over time (rules, tests, procedures)  
- How to **evolve** rules/skills/prompts from incidents

---

## 10. Command surface — canonical workflow entrypoints

### 10.1 Single entrypoint style

The repo MUST expose **one** primary style: **`Makefile`** or **`Taskfile`** (or equivalent) calling `scripts/`. **Agents MUST prefer these targets over ad hoc shell.**

Document all targets in `README.md` and `docs/development/local-setup.md`.

### 10.2 Required command catalog (minimum)

| Target | Purpose |
|--------|---------|
| `dev` | Local API with hot reload |
| `lint` | Ruff lint |
| `fmt` | Ruff format (apply) |
| `typecheck` | mypy or pyright |
| `test` | Full test suite |
| `test:unit` | Unit tests only |
| `test:integration` | Integration tests |
| `test:smoke` | Smoke suite |
| `migrate` | Apply migrations |
| `migrate:create` | Scaffold revision (document args) |
| `docs:check` | Link check or docs build if applicable |
| `docs:index` | Regenerate doc index if applicable |
| `queue:peek` | Read-only: header + first open row |
| `queue:validate` | Schema + invariants |
| `queue:archive` | Scripted move row open→archive (optional but recommended) |
| `prompt:list` | List prompt templates |
| `skills:list` | List skills |
| `rules:check` | Validate rule files present/parsable |
| `audit:self` | Repo self-audit (lint + tests + queue validate + spec links) |
| `security:scan` | Wrapper for bandit/trivy/etc. as applicable |
| `image:build` | Build API container |
| `image:scan` | Scan built image |
| `release:prepare` | Changelog/staging checks |
| `release:verify` | Pre-tag verification |
| `k8s:render` | Render manifests |
| `k8s:validate` | kubeconform/kubeval |
| `docker:up` / `docker:down` | Compose |

Implementations may combine some targets internally; the spec requires **documented** equivalents if names differ slightly.

---

## 11. GitHub-centric: `.github/` layout

### 11.1 Required contents

```
.github/
├── workflows/
│   ├── ci.yml
│   ├── cd.yml
│   └── security.yml
├── ISSUE_TEMPLATE/
├── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS
├── dependabot.yml
└── labels.yml (optional)
```

### 11.2 CI stages (concrete expectations)

**Minimum stages on PR:**

1. Checkout; dependency cache.  
2. **Lint:** `ruff` + format check.  
3. **Typecheck:** per project config.  
4. **Tests:** `pytest` + coverage artifact; fail if coverage below floor (define floor in `docs/quality/`).  
5. **Build:** Docker image build; **scan** (Trivy or GitHub).  
6. **Docs:** `docs:check` if implemented.  
7. **Optional matrix:** Python versions; **SQLite job** and **Postgres job** for integration tests.  
8. **Migrations:** `alembic upgrade head --sql` dry-run or equivalent **against ephemeral DB** where applicable.

**Artifacts:** test reports, coverage, SBOM or image scan results (as available).

### 11.3 CD stages (concrete expectations)

- **Triggers:** protected `main`, semver tags, manual dispatch.  
- **Promotion:** dev → staging → prod with **environment protection**.  
- **Release:** `release:verify` before tag; container push to registry; **deploy** via Helm/Kustomize; **record** release notes in `docs/release/`.  
- **DB migrations:** job with **approval gate** for prod; **rollback** doc mandatory.

---

## 12. Backend: modular monolith and extraction

### 12.1 Principles (unchanged, tightened)

- **Bounded contexts** in `packages/` and `apps/api/src/<context>/`.  
- **Contracts:** OpenAPI + shared Pydantic models in `packages/contracts`.  
- **Data ownership:** no cross-context table access without documented FKs and ownership.  
- **Outbox** (optional) for reliable async evolution.

### 12.2 Extraction criteria

Document in `docs/architecture/modular-monolith.md`:

- Independent **deploy cadence**, **scaling**, **SLO**, or **team ownership** → candidate service.  
- **Strangler**: new deployable behind same contract; migrate clients deliberately.

### 12.3 Workers

Long work goes through **`packages/tasks`** interfaces; workers are **optional profile** with Redis/Rabbit, same validation commands.

---

## 13. Data layer: SQLite, PostgreSQL, ChromaDB

Policy unchanged from v1.0 with added **operational** requirements:

- **Migrations** must be **reviewed** in PR with **expand/contract** notes for production.  
- **SQLite→Postgres** path documented in skills + procedure.  
- **ChromaDB**: persistent volumes; backup/restore in `docs/operations/`; **AI kill switch** env documented in `docs/architecture/ai-rag-chromadb.md`.

---

## 14. Authentication and multi-tenancy

Requirements unchanged; add **explicit**:

- **Token lifecycle** documented (issue, refresh, revoke) in `docs/security/` + skills.  
- **Tenant isolation verification** steps in `test:integration` where multi-tenant.  
- **SSO** as pluggable IdP profiles; **no secrets in repo**.

---

## 15. Optional front-end and mobile

Unchanged intent; each optional app MUST state **enable/disable**, **env vars**, and **burden** in `docs/optional-clients/`.

---

## 16. Docker and Kubernetes

### 16.1 Docker

- Multi-stage non-root image; healthcheck; **same Dockerfile** used in CI build.  
- Compose **profiles**: `db`, `ai`, `worker`, etc.

### 16.2 Kubernetes

- Manifests in `deploy/k8s/`; **readiness** includes DB and critical deps.  
- **`k8s:render` + `k8s:validate`** in CI for default overlay.

### 16.3 Optional cloud

Connection strings and managed services as **swappable config**; no vendor SDK in core domain logic.

---

## 17. Queue system — operating lane (hardened)

### 17.1 Files and roles

| File | Role |
|------|------|
| `queue/queue.csv` | Open items; **first data row under header = active work item** for single-lane processing. |
| `queue/queuearchive.csv` | Historical; **append-only** for completed/cancelled/superseded. |

### 17.2 Single-lane semantics

- **At most one** active processor SHOULD hold responsibility for the top row at a time (human process + optional lock file).  
- Processor MUST read the **entire** top row and treat **`summary` as the contract** — rich enough to act without guesswork: goal, acceptance criteria, **definition of done**, out-of-scope, dependencies.

### 17.3 Lifecycle

| State | Location | Transition rules |
|-------|----------|-------------------|
| Open | `queue.csv` | Rows ordered; top = next |
| In progress | Same row (optional `status` column **or** notes + branch) | Document in QUEUE_INSTRUCTIONS |
| Blocked | Stays in `queue.csv` | `notes` MUST explain blocker, owner, next step; do **not** archive |
| Done | Move to archive | Append full row + `status=done` + `completed_date` + PR URL in `notes` |
| Cancelled / superseded | Archive | `status` set; original removed from open |

**Never delete** history without archive row.

### 17.4 Branch naming

- **`queue/<id>-short-slug`** or `cursor/<slug>-<suffix>` — **document canonical pattern** in `QUEUE_INSTRUCTIONS.md`; must include **queue `id`** when work is queue-driven.

### 17.5 PR linking

- PR MUST reference queue `id` in title or body; **paste PR URL** into `notes` or archive row.

### 17.6 Batch / phase

- **`batch`**: coordinated release train; processors MAY process **strict FIFO within batch** if policy says so — **state policy** in `QUEUE_INSTRUCTIONS.md`.  
- **`phase`**: ordering within batch when applicable.

### 17.7 Auditing and tooling

Implement **as applicable** (recommended):

- **`queue.lock`** — optional mutex (contents: owner id, ISO timestamp, branch name).  
- **`queue/audit.log`** — append-only JSON lines for claim/release/archive (optional).  
- **`queue:validate`** — schema, known categories, no duplicate `id`, top-row contract present.  
- **`queue:health`** — CI check that `queue.csv` parses and passes validate.  
- **Queue lint** — forbid empty `summary`, require minimum length or required subfields (policy-defined).

### 17.8 Conflicts

If two writers collide on `queue.csv`, **procedures** MUST define: stop, re-run `queue:validate`, merge using main as truth, **never** silently drop rows.

### 17.9 Schema

Same columns as v1.0; **`summary` MUST remain elaborative** (not a one-liner). Optional add **`status`** on open file if in-progress tracking needed — if added, **document** in validators.

### 17.10 Categories

Same MVP set as v1.0; **adding a category** requires procedure `add-queue-category.md` (validators, docs, examples).

---

## 18. Validation-first and evidence-first behavior

Agents MUST:

- **Plan** before code (procedure `plan-change.md`).  
- Work in **small validated increments** with commits that tell a story.  
- **Run** relevant checks after edits; **capture** key outputs in PR description when useful.  
- **Update docs** when behavior or ops change.  
- **Avoid scope creep**; spawn new queue/issue for unrelated work.  
- **Hand off** with: files changed, commands run + results, risks, follow-ups.

Humans MUST review for **tenant/security** and **procedure compliance**.

---

## 19. Required artifacts for meaningful changes

**Meaningful changes** (behavior, contract, security, persistence, deploy, queue policy) MUST leave:

- Code diff with tests where appropriate.  
- **Updated docs** for changed behavior or ops.  
- **Queue `notes`** or archive row when work was queue-driven.  
- **PR description** with evidence (commands run, screenshots only if UI).  
- **ADRs** for architectural shifts (`docs/adr/`).  
- Updates to **prompts/skills/rules** when the change reflects a new recurring pattern.

---

## 20. Repo governance and machine improvement loops

### 20.1 Mechanisms (required documentation)

`docs/repo-governance/` MUST describe:

- **Post-task retrospectives** — what broke, what to encode.  
- **Post-incident updates** — link to IR, update runbooks.  
- **Rule/skill/prompt refinement** — ownership and PR path.  
- **Scheduled repo audits** — `audit:self` on a cadence.  
- **Procedure drift detection** — periodic review of `docs/procedures/` vs actual CI.  
- **Documentation freshness** — `docs:check` or manual quarterly review.  
- **Stale prompt cleanup** — deprecate in favor of new templates.  
- **Command surface consistency** — names match docs; **drift is a bug**.

### 20.2 Encoding learning

When the repo sees **repeated** work or mistakes, maintainers MUST encode learning in **rules, skills, procedures, prompts, commands, or tests** — explicit policy.

---

## 21. Observability and operations

- **Structured logging**, correlation IDs, **error taxonomy** (codes stable).  
- **Metrics** (`/metrics` behind network policy if public).  
- **Tracing** optional OpenTelemetry.  
- **Runbooks** for API down, DB fail, JWT key rotation, Chroma unavailable.

---

## 22. CI/CD summary (cross-reference)

| Concern | CI | CD |
|---------|----|----|
| Lint/fmt/typecheck | PR | — |
| Unit/integration | PR | — |
| Smoke | PR or nightly | post-deploy |
| Image build/scan | PR + main | release |
| Migrations dry-run | PR | gated apply |
| k8s validate | PR | pre-deploy |

---

## 23. Legal and meta

- **LICENSE** (MIT or Apache-2.0 — pick one in implementation).  
- **CONTRIBUTING.md** — links `AGENTS.md`, queue, procedures.  
- **CODE_OF_CONDUCT.md** optional.

---

## 24. Implementation checklist — machine operability

Definition of done for generating the template from this spec:

**Structure and control plane**

- [ ] Root **`AGENTS.md`** complete per §4.  
- [ ] **`spec.md`** (canonical full spec) present at repo root.  
- [ ] **`.cursor/rules/`** with global + at least one path-scoped example.  
- [ ] Optional **`.cursor/commands/`** if tooling supports it.  
- [ ] **`prompts/`** library with **all required templates** (§7.3) + metadata convention in **`docs/prompts/`**.  
- [ ] **`docs/procedures/`** with **all required procedures** (§8.2).  
- [ ] **`docs/agents/`**, **`docs/repo-governance/`**, **`docs/quality/`**, **`docs/runbooks/`**, **`docs/release/`**, **`docs/adr/`**, **`docs/security/incident-response.md`**, **`docs/operations/rollback.md`**.  
- [ ] **`skills/`**: ≥**40** stubs, ≥**10** complete per §6.  
- [ ] **Instruction hierarchy** documented in `AGENTS.md` and **`docs/agents/`**.

**Automation and validation**

- [ ] **Canonical `Makefile` or `Taskfile`**; **minimum command catalog** (§10) implemented or explicitly aliased.  
- [ ] **`.github/workflows`** CI: lint, typecheck, tests, image build, **security scan**, migration dry-run, **k8s validate** if applicable.  
- [ ] **CD scaffold** with environments and **rollback** doc.  
- [ ] **`queue:validate`**, **`audit:self`** implemented.  
- [ ] **Release flow** documented and **`release:verify`** wired.

**Product template**

- [ ] **`apps/api`** FastAPI modular monolith: health/live/ready, auth stubs, tenant hooks.  
- [ ] **Alembic**; SQLite + Postgres documented; **migration procedure** live.  
- [ ] **`docker-compose.yml`** + **`deploy/k8s/`** base.  
- [ ] **`queue/`** full set per §2 + **hardened lifecycle** in instructions.  
- [ ] Optional **`apps/web`**, **`apps/mobile`** placeholders with **profile burden** docs.  
- [ ] **ChromaDB** stub under **`packages/ai/`** when AI profile enabled.

**Governance and evidence**

- [ ] **Repo governance** and **self-audit / improvement loop** documented.  
- [ ] **Evidence/handoff rules** in `AGENTS.md` + **`docs/procedures/handoff.md`**.  
- [ ] **Security**: dependency review, code scanning, **image scan** in CI; SBOM/attestation if policy requires.  
- [ ] **Documentation** for **optional profiles** (when to enable/not).  
- [ ] **README.md** quickstart linking **`AGENTS.md`**, **`spec.md`**, **`docs/`**.

---

## 25. Document control

| Item | Value |
|------|--------|
| **Canonical spec file** | `spec.md` |
| **Version** | 2.0 |
| **Owners** | Repository maintainers |
| **Change process** | PR with rationale; bump version header when breaking; ADR if architectural |

---

## 26. Complete file enumeration — procedural inventory

Every file that MUST or SHOULD exist in a generated template is enumerated below, organized by subsystem. Each entry states the file path, a summary of its purpose, and structural notes on how the file should be authored. Stubs are acceptable where noted; all stubs MUST contain the required section headings (even if body is `TODO`).

**Conventions:**

- **[REQUIRED]** — MUST exist for the template to be considered complete per this spec.
- **[RECOMMENDED]** — SHOULD exist; omit only with documented rationale.
- **[OPTIONAL]** — include when the relevant profile or feature is enabled.
- **Structure** notes describe the internal sections/format each file MUST follow.

---

### 26.1 Root files

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 1 | `AGENTS.md` | REQUIRED | Root agent control plane. The default policy surface for all agents operating in the repo. Defines mission, instruction hierarchy, workflows, validation, queue interaction, escalation, and anti-patterns. | Sections per §4.1: (1) Mission/philosophy, (2) Instruction hierarchy, (3) Required workflow, (4) Branch/PR policy, (5) Planning before coding, (6) Scope control, (7) Validation before handoff, (8) Documentation update requirements, (9) Queue interaction rules, (10) When to create/update skills/rules/prompts/procedures, (11) Escalation, (12) Anti-patterns. Navigation and machine-interface guidance per §4.2. |
| 2 | `spec.md` | REQUIRED | Canonical full specification (this document). Single source of truth for all repo policy, structure, and requirements. | Versioned; change via PR with rationale; bump version on breaking changes. |
| 3 | `README.md` | REQUIRED | Quickstart entry point. Links to `AGENTS.md`, `spec.md`, `docs/`, command catalog. First file a human or agent reads. | Sections: Project title, one-paragraph description, prerequisites, quickstart commands (`make dev`, `make test`), link table to key docs (`AGENTS.md`, `spec.md`, `docs/getting-started/`, command catalog), license badge. |
| 4 | `.env.example` | REQUIRED | Template for all environment variables. Never contains real secrets. Documents every env var the system reads with comments explaining purpose and default. | Format: `# SECTION_HEADER` comments grouping related vars. Each var as `VAR_NAME=default_or_placeholder` with inline `# comment`. Sections: Database, Auth/JWT, API, Optional profiles (AI, Workers), Observability, Feature flags. |
| 5 | `docker-compose.yml` | REQUIRED | Orchestrates local development and CI services. Uses profiles for optional components (db, ai, worker). | Services: `api` (build from `apps/api/Dockerfile`), `db` (Postgres, profile: db), `chroma` (ChromaDB, profile: ai), `worker` (profile: worker). Volumes for persistence. Network definition. Environment references to `.env.example`. |
| 6 | `Makefile` | REQUIRED | Single canonical command entrypoint. Every recurring operation has a named target. Agents MUST use these targets over ad hoc shell. | Targets per §10.2 (minimum 27 targets). Each target: short help comment, delegates to `scripts/` where logic is non-trivial. `.PHONY` declarations. `help` target that lists all targets with descriptions. |
| 7 | `pyproject.toml` | REQUIRED | Python project configuration. Defines dependencies, dev dependencies, tool configs (ruff, mypy/pyright, pytest). | Sections: `[project]` (name, version, python-requires, dependencies), `[project.optional-dependencies]` (dev, test, lint), `[tool.ruff]`, `[tool.mypy]` or `[tool.pyright]`, `[tool.pytest.ini_options]`. |
| 8 | `LICENSE` | REQUIRED | Open-source license. MIT or Apache-2.0 (pick one at generation time). | Standard license text with year and copyright holder placeholders. |
| 9 | `CONTRIBUTING.md` | REQUIRED | Contribution guide for humans and agents. Links to `AGENTS.md`, queue system, procedures. | Sections: How to contribute, Development setup (link to `docs/getting-started/`), Branch naming conventions, PR process (link to `docs/procedures/open-pull-request.md`), Queue-driven work (link to `queue/QUEUE_INSTRUCTIONS.md`), Code of conduct reference. |
| 10 | `CODE_OF_CONDUCT.md` | OPTIONAL | Community standards. | Standard Contributor Covenant or equivalent. |

---

### 26.2 `.cursor/` — machine-control layer files

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 11 | `.cursor/rules/global.md` | REQUIRED | Universal constraints applied to every agent interaction. Covers commit message format, scope discipline, evidence requirements, forbidden behaviors. | Frontmatter: `alwaysApply: true`. Body: numbered rules with rationale. Categories: Commit standards, Scope discipline, Evidence/handoff, Forbidden patterns (secrets in code, bypassing CI, ad hoc commands when target exists). |
| 12 | `.cursor/rules/apps-api.md` | REQUIRED | Path-scoped rules for `apps/api/`. Enforces FastAPI patterns, service/repository boundaries, import conventions, test co-location. | Frontmatter: `globs: ["apps/api/**"]`. Body: API-specific constraints — router registration pattern, dependency injection, Pydantic model location, error response shape, test file naming. |
| 13 | `.cursor/rules/security.md` | REQUIRED | Security invariants. No secrets in code, token handling rules, tenant isolation checks, dependency review triggers. | Frontmatter: `alwaysApply: true`. Body: Security rules — secret sources (env only), JWT validation requirements, tenant context propagation, prohibited patterns (raw SQL without parameterization, disabled auth in non-test code). |
| 14 | `.cursor/rules/queue.md` | REQUIRED | Queue file invariants. Lifecycle rules, schema enforcement, no row deletion without archive. | Frontmatter: `globs: ["queue/**"]`. Body: Queue CSV rules — column schema, lifecycle state transitions, archive-before-delete, summary minimum requirements, branch naming with queue ID. |
| 15 | `.cursor/rules/testing.md` | RECOMMENDED | Testing standards. Coverage expectations, naming conventions, fixture patterns, mock boundaries. | Frontmatter: `globs: ["**/tests/**", "**/test_*"]`. Body: Test naming (`test_<unit>_<scenario>_<expected>`), fixture scope rules, mock boundary policy, async test patterns. |
| 16 | `.cursor/rules/documentation.md` | RECOMMENDED | Documentation update triggers. When docs MUST be updated alongside code changes. | Frontmatter: `alwaysApply: true`. Body: Trigger conditions (new env var → `.env.example` + docs, new endpoint → API docs, behavior change → relevant docs, new error code → error taxonomy). |
| 17 | `.cursor/commands/validate.md` | OPTIONAL | Reusable command: run full validation suite (lint + typecheck + test + queue:validate). | Command metadata: name, description, steps (ordered list of make targets to run), expected output summary. |
| 18 | `.cursor/commands/queue-next.md` | OPTIONAL | Reusable command: claim and begin processing the next queue item. | Command metadata: name, description, steps (queue:peek → read row → create branch → begin work), links to `docs/procedures/start-queue-item.md`. |

---

### 26.3 `prompts/` — role template files

Each prompt template is a Markdown file with YAML front matter (metadata) per §7.2. The paired `.meta.yaml` convention is an alternative; this enumeration assumes inline YAML front matter for simplicity (document chosen convention in `docs/prompts/README.md`).

**Structure per template:** YAML front matter (`purpose`, `when_to_use`, `required_inputs`, `expected_outputs`, `validation_expectations`, `constraints`, `linked_commands`, `linked_procedures`, `linked_skills`), then the prompt body with role definition, context injection points (marked with `{{placeholders}}`), step-by-step instructions for the agent, output format requirements, and validation checklist.

| # | File | Status | Summary |
|---|------|--------|---------|
| 19 | `prompts/README.md` | REQUIRED | Prompt library overview. Documents the metadata convention (front matter vs `.meta.yaml`), how to add new templates, naming rules, and links to `docs/prompts/`. |
| 20 | `prompts/task_planner.md` | REQUIRED | Role: decompose work into scoped tasks with acceptance criteria, risks, file impact, and definition of done. |
| 21 | `prompts/implementation_agent.md` | REQUIRED | Role: execute code changes with strict scope discipline — plan, implement, validate, commit, handoff. |
| 22 | `prompts/reviewer_critic.md` | REQUIRED | Role: adversarial review of diffs against spec, security policy, tenant isolation, scope creep, and test coverage. |
| 23 | `prompts/test_writer.md` | REQUIRED | Role: author tests aligned to acceptance criteria — unit, integration, edge cases, failure paths. |
| 24 | `prompts/debugger.md` | REQUIRED | Role: systematic failure isolation — reproduce, hypothesize, instrument, verify fix, add regression test. |
| 25 | `prompts/refactorer.md` | REQUIRED | Role: behavior-preserving structural changes — identify smell, plan transformation, verify equivalence via tests. |
| 26 | `prompts/documentation_updater.md` | REQUIRED | Role: update docs to match code/ops changes — identify stale docs, edit, verify links, update indexes. |
| 27 | `prompts/migration_author.md` | REQUIRED | Role: author DB migrations with expand/contract notes, rollback plan, and CI dry-run verification. |
| 28 | `prompts/queue_processor.md` | REQUIRED | Role: execute single top-row queue item — claim, branch, implement, validate, archive, handoff. |
| 29 | `prompts/release_manager.md` | REQUIRED | Role: prepare release — changelog, version bump, tag, verification, promotion documentation. |
| 30 | `prompts/dependency_upgrade_agent.md` | REQUIRED | Role: safe dependency bumps — identify outdated, upgrade, run full CI, document breaking changes. |
| 31 | `prompts/security_review_agent.md` | REQUIRED | Role: threat-focused code review — secrets exposure, injection, auth bypass, tenant leakage, dependency CVEs. |
| 32 | `prompts/incident_triage_agent.md` | REQUIRED | Role: initial incident classification — severity, blast radius, evidence capture, escalation path, comms draft. |
| 33 | `prompts/performance_audit_agent.md` | REQUIRED | Role: latency/resource review — identify bottlenecks, profile endpoints, recommend optimizations with evidence. |
| 34 | `prompts/repo_bootstrap_agent.md` | REQUIRED | Role: take a fresh clone to green development state — install deps, configure env, run validation, verify all targets. |
| 35 | `prompts/spec_hardening_agent.md` | REQUIRED | Role: align spec with reality — find drift between spec and implementation, propose PRs to close gaps. |
| 36 | `prompts/skill_authoring_agent.md` | REQUIRED | Role: create or update skills to standard — ensure all required sections, link procedures/prompts/rules. |
| 37 | `prompts/rule_authoring_agent.md` | REQUIRED | Role: create or update `.cursor/rules` — scope correctly, test enforcement, document rationale. |

---

### 26.4 `skills/` — executable playbook files

Skills are organized by coverage category (§6.3). Each skill file follows the structure in §6.2: Purpose, When to invoke, Prerequisites, Relevant files/areas, Step-by-step method, Command examples, Validation checklist, Common failure modes, Handoff expectations, Related procedures, Related prompts, Related rules.

**Full skills** (≥10 required) are marked **[FULL]**. All others are stubs with section headings and `TODO` bodies.

| # | File | Status | Summary |
|---|------|--------|---------|
| 38 | `skills/README.md` | REQUIRED | Skills library index. Lists all skills by category, explains the skill format, links to `docs/procedures/update-or-create-skill.md`. |

#### Agent Operations (`skills/agent-ops/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 39 | `skills/agent-ops/queue-triage.md` | REQUIRED [FULL] | How to read, interpret, and prioritize queue items. Covers reading `queue.csv`, understanding summary contracts, checking dependencies, and deciding readiness. |
| 40 | `skills/agent-ops/task-planning.md` | REQUIRED [FULL] | How to decompose a task into implementable steps with acceptance criteria, file impact analysis, risk identification, and scope bounds. |
| 41 | `skills/agent-ops/implementation-handoff.md` | REQUIRED [FULL] | How to write a complete handoff: files changed, commands run with output, risks, follow-ups, PR link, queue state update. |
| 42 | `skills/agent-ops/blocked-task-recovery.md` | REQUIRED | How to handle blocked work: document blockers in queue notes, escalate, optionally requeue, never silently skip. |
| 43 | `skills/agent-ops/prompt-to-procedure-promotion.md` | REQUIRED | When and how to promote a successful one-off prompt into `prompts/` with full metadata. |
| 44 | `skills/agent-ops/rule-refinement-after-mistakes.md` | REQUIRED | After a repeated mistake: identify pattern, author or update rule in `.cursor/rules/`, link to incident. |
| 45 | `skills/agent-ops/post-pr-audit.md` | REQUIRED | How to audit a completed PR: verify acceptance criteria met, tests pass, docs updated, queue archived. |
| 46 | `skills/agent-ops/repo-self-audit.md` | REQUIRED [FULL] | Run `make audit:self`. Verify all spec sections have corresponding artifacts. Check for drift between docs and implementation. |

#### Repo Governance (`skills/repo-governance/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 47 | `skills/repo-governance/writing-agents-md.md` | REQUIRED [FULL] | How to author or update `AGENTS.md` per §4. Covers all 12 required sections, navigation guidance, and machine interface. |
| 48 | `skills/repo-governance/authoring-cursor-rules.md` | REQUIRED [FULL] | How to create or update `.cursor/rules/` files. Covers frontmatter, scoping (global vs path), testing enforcement, and avoiding contradictions. |
| 49 | `skills/repo-governance/adding-reusable-commands.md` | REQUIRED | How to add entries to `.cursor/commands/` or `Makefile` targets. Ensure no duplication, document in README. |
| 50 | `skills/repo-governance/maintaining-procedural-docs.md` | REQUIRED | How to keep `docs/procedures/` current. Covers drift detection, update triggers, linking to Make targets. |
| 51 | `skills/repo-governance/writing-adrs.md` | REQUIRED | How to author Architecture Decision Records in `docs/adr/`. Use template, link to relevant code and spec sections. |
| 52 | `skills/repo-governance/changelogs-release-notes.md` | REQUIRED | How to maintain changelogs and release notes. Format, what to include, automation hooks. |
| 53 | `skills/repo-governance/repository-hygiene.md` | REQUIRED | Periodic repo cleanup: stale branches, orphaned docs, unused dependencies, dead code detection. |

#### Backend / Platform (`skills/backend/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 54 | `skills/backend/fastapi-router-module.md` | REQUIRED [FULL] | How to add a new FastAPI router/module: file placement, router registration, dependency injection, schema definition, test scaffolding. |
| 55 | `skills/backend/service-repository-pattern.md` | REQUIRED [FULL] | How to implement service and repository layers: separation of concerns, transaction boundaries, interface contracts. |
| 56 | `skills/backend/health-readiness-liveness.md` | REQUIRED | How to implement and verify health, readiness, and liveness endpoints. Probe contracts for K8s. |
| 57 | `skills/backend/api-versioning.md` | REQUIRED | How to version API endpoints: URL prefix strategy, deprecation headers, migration path documentation. |
| 58 | `skills/backend/background-jobs.md` | REQUIRED | How to define and register background jobs via `packages/tasks` interfaces. |
| 59 | `skills/backend/worker-integration.md` | REQUIRED | How to enable the worker profile, connect to broker (Redis/Rabbit), and verify job execution. |
| 60 | `skills/backend/idempotent-tasks.md` | REQUIRED | How to design idempotent task handlers: idempotency keys, deduplication, safe retries. |
| 61 | `skills/backend/configuration-management.md` | REQUIRED | How to add new configuration: `.env.example`, `config.py`, validation, documentation. |
| 62 | `skills/backend/feature-flags.md` | REQUIRED | How to implement feature flags: env-based toggles, conditional logic, cleanup procedures. |
| 63 | `skills/backend/error-taxonomy.md` | REQUIRED | How to define and use stable error codes: error registry, response shapes, client documentation. |
| 64 | `skills/backend/structured-logging.md` | REQUIRED | How to implement structured logging: log format, correlation IDs, log levels, sensitive data masking. |
| 65 | `skills/backend/opentelemetry-tracing.md` | REQUIRED | How to add OpenTelemetry tracing: span creation, context propagation, exporter configuration. |
| 66 | `skills/backend/metrics-exposition.md` | REQUIRED | How to expose Prometheus-compatible metrics: `/metrics` endpoint, custom counters/histograms, network policy. |
| 67 | `skills/backend/rate-limiting.md` | REQUIRED | How to implement rate limiting: middleware setup, configuration, per-tenant limits, response headers. |
| 68 | `skills/backend/retries-circuit-breakers.md` | REQUIRED | How to implement retry logic and circuit breakers for external service calls. |
| 69 | `skills/backend/safe-migration-rollout.md` | REQUIRED [FULL] | How to roll out database migrations safely: expand/contract pattern, dry-run in CI, rollback plan, production gates. |
| 70 | `skills/backend/sqlite-to-postgres.md` | REQUIRED | How to migrate from SQLite to PostgreSQL: schema differences, data migration, connection string swap, validation. |

#### Security / Compliance (`skills/security/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 71 | `skills/security/secret-handling.md` | REQUIRED [FULL] | How to handle secrets: env-only sourcing, rotation procedures, never in code/logs, `.env.example` documentation. |
| 72 | `skills/security/token-lifecycle.md` | REQUIRED | JWT token lifecycle: issuance, refresh, revocation, key rotation, testing token expiry. |
| 73 | `skills/security/rbac-tenant-isolation.md` | REQUIRED | How to verify RBAC and tenant isolation: test patterns, middleware checks, query scoping. |
| 74 | `skills/security/dependency-review.md` | REQUIRED | How to review dependency changes: CVE checks, license compliance, update impact assessment. |
| 75 | `skills/security/code-scanning.md` | REQUIRED | How to run and interpret code scanning results (bandit, semgrep). Triage findings, fix or document exceptions. |
| 76 | `skills/security/image-scanning.md` | REQUIRED | How to scan container images (Trivy/GitHub): interpret results, fix critical/high, document accepted risks. |
| 77 | `skills/security/sbom-attestation.md` | RECOMMENDED | How to generate and publish SBOMs and attestations for container images. |
| 78 | `skills/security/secure-defaults-review.md` | REQUIRED | How to audit the codebase for secure defaults: auth enabled, CORS restrictive, debug off in prod, etc. |
| 79 | `skills/security/incident-evidence-capture.md` | REQUIRED | How to capture and preserve evidence during a security incident: logs, timestamps, affected scope. |

#### Testing / Quality (`skills/testing/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 80 | `skills/testing/pytest-conventions.md` | REQUIRED [FULL] | Pytest project conventions: directory structure, naming, fixtures, markers, conftest patterns, coverage configuration. |
| 81 | `skills/testing/async-testing.md` | REQUIRED | How to test async FastAPI code: `pytest-asyncio`, `httpx.AsyncClient`, event loop fixtures. |
| 82 | `skills/testing/api-contract-testing.md` | REQUIRED | How to write API contract tests: request/response schema validation, OpenAPI spec alignment. |
| 83 | `skills/testing/snapshot-testing.md` | REQUIRED | How to use snapshot testing for API responses and data structures: when to use, update workflow. |
| 84 | `skills/testing/smoke-tests.md` | REQUIRED | How to write and run smoke tests: health check, critical path verification, post-deploy validation. |
| 85 | `skills/testing/regression-harness.md` | REQUIRED | How to add regression tests after bug fixes: capture the bug, write the test, verify the fix. |
| 86 | `skills/testing/load-test-basics.md` | RECOMMENDED | How to set up and run basic load tests: tool selection (locust/k6), scenario definition, result interpretation. |
| 87 | `skills/testing/flaky-test-triage.md` | REQUIRED | How to identify, isolate, and fix flaky tests: detection, quarantine, root cause analysis. |
| 88 | `skills/testing/validation-loop-design.md` | REQUIRED | How to design validation loops for agent workflows: what to check, when to check, how to report. |

#### DevOps / Operations (`skills/devops/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 89 | `skills/devops/docker-multi-stage-builds.md` | REQUIRED | How to build efficient multi-stage Docker images: builder/runner stages, non-root user, layer caching, healthcheck. |
| 90 | `skills/devops/compose-profiles.md` | REQUIRED | How to manage Docker Compose profiles: enabling/disabling services, profile-specific env vars, testing combinations. |
| 91 | `skills/devops/k8s-probes.md` | REQUIRED | How to configure Kubernetes probes: liveness, readiness, startup — paths, thresholds, dependency checks. |
| 92 | `skills/devops/rollout-rollback.md` | REQUIRED | How to perform Kubernetes rollouts and rollbacks: strategy, monitoring, decision tree, documentation. |
| 93 | `skills/devops/github-actions-troubleshooting.md` | REQUIRED | How to debug failing GitHub Actions: log reading, local reproduction, cache issues, secret availability. |
| 94 | `skills/devops/release-promotion.md` | REQUIRED | How to promote releases through environments: dev → staging → prod gates, verification steps, approval flows. |
| 95 | `skills/devops/artifact-publishing.md` | REQUIRED | How to publish build artifacts: container registry push, Python package publishing, artifact retention. |
| 96 | `skills/devops/environment-configuration.md` | REQUIRED | How to manage environment-specific configuration: overlays, secrets injection, configuration validation. |
| 97 | `skills/devops/backup-restore-drills.md` | RECOMMENDED | How to perform backup and restore drills: database dumps, volume snapshots, verification procedures. |

#### AI / RAG (`skills/ai-rag/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 98 | `skills/ai-rag/chromadb-ingestion.md` | OPTIONAL | How to ingest documents into ChromaDB: collection creation, embedding generation, batch loading, verification. |
| 99 | `skills/ai-rag/embedding-refresh.md` | OPTIONAL | How to refresh embeddings when source documents change: staleness detection, incremental update, full rebuild. |
| 100 | `skills/ai-rag/retrieval-evaluation.md` | OPTIONAL | How to evaluate retrieval quality: relevance scoring, recall measurement, benchmark datasets. |
| 101 | `skills/ai-rag/prompt-versioning.md` | OPTIONAL | How to version AI prompts: naming conventions, A/B testing, rollback, performance tracking. |
| 102 | `skills/ai-rag/ai-kill-switch.md` | OPTIONAL | How to implement and test the AI kill switch: env var toggle, graceful degradation, monitoring. |
| 103 | `skills/ai-rag/model-provider-abstraction.md` | OPTIONAL | How to abstract model/provider dependencies: interface design, provider swap, configuration. |
| 104 | `skills/ai-rag/ai-safety-review.md` | OPTIONAL | How to review AI outputs for safety: content filtering, hallucination checks, bias detection. |

#### Frontend / Mobile (Optional) (`skills/frontend/`)

| # | File | Status | Summary |
|---|------|--------|---------|
| 105 | `skills/frontend/generated-client-usage.md` | OPTIONAL | How to use auto-generated API clients from OpenAPI spec: generation, integration, update workflow. |
| 106 | `skills/frontend/react-api-integration.md` | OPTIONAL | How to integrate React frontend with the FastAPI backend: proxy setup, auth flow, error handling. |
| 107 | `skills/frontend/expo-auth-storage.md` | OPTIONAL | How to handle auth token storage in Expo/React Native: secure storage, refresh flow, logout. |
| 108 | `skills/frontend/frontend-env-handling.md` | OPTIONAL | How to manage frontend environment variables: build-time vs runtime, .env files, CI injection. |

**Skills total: 70 files** (38–108), exceeding the §6.1 minimum of 40 stubs. At least 10 marked [FULL] must be production-usable with all §6.2 sections completed.

---

### 26.5 `docs/` — documentation tree files

#### Root and getting started

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 109 | `docs/README.md` | REQUIRED | Documentation hub. Index of all doc sections with one-line descriptions and links. | Ordered list of every `docs/` subdirectory with description and link to its README. |
| 110 | `docs/getting-started/README.md` | REQUIRED | Getting started index. Links to prerequisites and quickstart. | Link list to child docs. |
| 111 | `docs/getting-started/prerequisites.md` | REQUIRED | Required tools and versions: Python 3.12+, Docker, Make/Task, Git. Optional: Node.js (web), Expo CLI (mobile). | Checklist format with version commands to verify each tool. |
| 112 | `docs/getting-started/quickstart.md` | REQUIRED | Step-by-step from clone to running dev server with passing tests. | Numbered steps: clone, copy `.env.example`, install deps, `make migrate`, `make dev`, `make test`. Expected output for each step. |

#### Architecture

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 113 | `docs/architecture/README.md` | REQUIRED | Architecture documentation index. | Link list to child docs. |
| 114 | `docs/architecture/modular-monolith.md` | REQUIRED | Modular monolith design: bounded contexts, contract boundaries, data ownership, extraction criteria (§12). | Sections: Overview, Bounded context map, Contract layer (`packages/contracts`), Data ownership rules, Cross-context communication, Extraction criteria and decision tree, Strangler pattern guide. |
| 115 | `docs/architecture/data-layer.md` | REQUIRED | Data layer architecture: SQLite for dev/constrained MVP, PostgreSQL for production, migration strategy. | Sections: Database selection criteria, SQLite constraints, Postgres requirements, Migration path (link to skill), Connection configuration, Transaction patterns. |
| 116 | `docs/architecture/auth-multi-tenancy.md` | REQUIRED | Authentication and multi-tenancy architecture: JWT flow, token lifecycle, tenant isolation, SSO extension points (§14). | Sections: Auth flow diagram, Token lifecycle (issue/refresh/revoke), Tenant model, Isolation enforcement, SSO pluggable interface, Testing tenant boundaries. |
| 117 | `docs/architecture/ai-rag-chromadb.md` | OPTIONAL | AI/RAG architecture with ChromaDB: embedding strategy, retrieval pipeline, kill switch, provider abstraction (§13). | Sections: When to enable, Architecture overview, ChromaDB deployment, Embedding pipeline, Retrieval interface, Kill switch mechanism, Provider abstraction, Operational burden. |

#### Development

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 118 | `docs/development/README.md` | REQUIRED | Development documentation index. | Link list to child docs. |
| 119 | `docs/development/local-setup.md` | REQUIRED | Detailed local development setup. All Make/Task targets documented with expected behavior (§10.1). | Sections: Environment setup, IDE configuration, Running locally (`make dev`), All command targets with descriptions, Database setup, Running tests, Docker development. |
| 120 | `docs/development/coding-standards.md` | REQUIRED | Coding standards enforced by linters and rules. Ruff config, type checking, import conventions, naming. | Sections: Python style (Ruff rules), Type annotations, Import ordering, Naming conventions, Error handling patterns, Documentation in code. |
| 121 | `docs/development/testing-guide.md` | REQUIRED | How to write and run tests. Pytest conventions, fixtures, markers, coverage requirements. | Sections: Test directory structure, Naming conventions, Fixture patterns, Markers (unit/integration/smoke), Coverage requirements, Running subsets, CI integration. |

#### API

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 122 | `docs/api/README.md` | REQUIRED | API documentation index. | Link list to child docs. |
| 123 | `docs/api/endpoints.md` | REQUIRED | API endpoint catalog. Auto-generated or manually maintained list of all routes with request/response schemas. | Table format: Method, Path, Description, Auth required, Request body, Response schema, Error codes. |
| 124 | `docs/api/error-codes.md` | REQUIRED | Error code taxonomy. Stable codes with descriptions, HTTP status mappings, and client handling guidance. | Table format: Error code, HTTP status, Description, Client action. Organized by domain (auth, validation, system). |

#### Operations

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 125 | `docs/operations/README.md` | REQUIRED | Operations documentation index. | Link list to child docs. |
| 126 | `docs/operations/docker.md` | REQUIRED | Docker operations: building images, running containers, Compose profiles, troubleshooting. | Sections: Image build (`make image:build`), Running with Compose, Profile activation, Volume management, Troubleshooting common issues. |
| 127 | `docs/operations/kubernetes.md` | REQUIRED | Kubernetes operations: manifest rendering, deployment, scaling, monitoring. | Sections: Manifest structure (`deploy/k8s/`), Rendering (`make k8s:render`), Validation (`make k8s:validate`), Deployment procedure, Scaling, Monitoring integration. |
| 128 | `docs/operations/observability.md` | REQUIRED | Observability setup: structured logging, metrics, tracing, dashboards (§21). | Sections: Logging (format, correlation IDs, levels), Metrics (`/metrics` endpoint), Tracing (OpenTelemetry config), Dashboard recommendations, Alert rules. |
| 129 | `docs/operations/backups.md` | REQUIRED | Backup and restore procedures for databases and persistent volumes. | Sections: Backup schedule, Database backup commands, Volume snapshots, Restore procedure, Verification steps, Disaster recovery. |
| 130 | `docs/operations/rollback.md` | REQUIRED | Rollback and forward-fix decision tree. When to rollback vs fix-forward, procedures for each (§2). | Sections: Decision tree (rollback vs forward-fix), Application rollback (K8s rollout undo), Database rollback (migration downgrade), Configuration rollback, Verification after rollback, Post-incident documentation. |

#### Security

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 131 | `docs/security/README.md` | REQUIRED | Security documentation index. | Link list to child docs. |
| 132 | `docs/security/threat-model-stub.md` | REQUIRED | Threat model template. Identifies assets, threat actors, attack surfaces, and mitigations. Stub to be filled per deployment. | Sections: Assets inventory, Threat actors, Attack surfaces (API, auth, data, infra), STRIDE analysis template, Mitigation controls, Review cadence. |
| 133 | `docs/security/secrets-management.md` | REQUIRED | How secrets are managed: sourcing (env vars only), rotation procedures, CI/CD injection, never in code. | Sections: Secret sources, Rotation procedures, CI/CD secret injection, Local development (`.env.example`), Audit and detection, Prohibited patterns. |
| 134 | `docs/security/incident-response.md` | REQUIRED | Incident response plan: classification, evidence capture, communication, remediation, post-incident (§2). | Sections: Severity classification (P1-P4), Evidence capture checklist, Communication templates, Escalation path, Remediation steps, Post-incident review, Documentation updates. |
| 135 | `docs/security/token-lifecycle.md` | REQUIRED | JWT token lifecycle details: issuance parameters, refresh windows, revocation mechanism, key rotation (§14). | Sections: Token issuance (claims, expiry), Refresh flow, Revocation (blocklist/short expiry), Key rotation procedure, Testing token scenarios. |

#### Procedures (`docs/procedures/`)

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 136 | `docs/procedures/README.md` | REQUIRED | Procedures index. Lists all SOPs with one-line descriptions and links. | Ordered list of all procedure files with descriptions. |
| 137 | `docs/procedures/start-queue-item.md` | REQUIRED | SOP: Claim top queue row, create branch, read relevant docs. | Per §8.3: Purpose, Trigger, Prerequisites, Commands, Ordered steps (read queue → verify readiness → create branch `queue/<id>-slug` → read linked docs → confirm understanding), Expected artifacts, Validation, Failure handling, Handoff. |
| 138 | `docs/procedures/plan-change.md` | REQUIRED | SOP: Create implementation plan with acceptance criteria, file impact, risks, scope bounds. | Per §8.3: Purpose, Trigger, Prerequisites, Commands, Ordered steps (restate requirements → identify files → list risks → define acceptance criteria → define scope bounds → document plan), Expected artifacts (plan document in PR or notes), Validation, Failure handling, Handoff. |
| 139 | `docs/procedures/implement-change.md` | REQUIRED | SOP: Execute code changes in small validated increments with commits that tell a story. | Per §8.3: Purpose, Trigger, Prerequisites, Commands (`make lint`, `make test`), Ordered steps (implement increment → lint → test → commit → repeat), Expected artifacts (commits, passing CI), Validation, Failure handling, Handoff. |
| 140 | `docs/procedures/validate-change.md` | REQUIRED | SOP: Run full validation matrix before opening PR. | Per §8.3: Purpose, Trigger, Prerequisites, Commands (`make lint`, `make fmt`, `make typecheck`, `make test`, `make test:integration`, `make security:scan`), Ordered steps (run each target → capture output → verify all green → document results), Expected artifacts (validation report), Validation, Failure handling, Handoff. |
| 141 | `docs/procedures/open-pull-request.md` | REQUIRED | SOP: Create PR with title, description template, evidence, labels, queue linkage. | Per §8.3: Purpose, Trigger, Prerequisites (all validation passing), Commands, Ordered steps (create PR → fill template → link queue ID → add labels → request review), Expected artifacts (PR URL), Validation (CI green), Failure handling, Handoff. |
| 142 | `docs/procedures/handoff.md` | REQUIRED | SOP: Complete handoff documentation — files changed, commands run, results, risks, follow-ups. | Per §8.3: Purpose, Trigger, Prerequisites, Commands, Ordered steps (list files changed → list commands run with output → document risks → document follow-ups → update queue notes → post PR link), Expected artifacts, Validation, Failure handling, Handoff. |
| 143 | `docs/procedures/archive-queue-item.md` | REQUIRED | SOP: Move completed queue row to archive with required fields. | Per §8.3: Purpose, Trigger, Prerequisites (PR merged or item cancelled), Commands (`make queue:archive`), Ordered steps (verify completion → copy row to archive → add status/date/PR URL → remove from queue.csv → validate), Expected artifacts, Validation (`make queue:validate`), Failure handling, Handoff. |
| 144 | `docs/procedures/handle-blocked-work.md` | REQUIRED | SOP: Document blockers, escalate, optionally requeue lower items. | Per §8.3: Purpose, Trigger, Prerequisites, Commands, Ordered steps (identify blocker → document in queue notes → escalate → optionally reorder queue → do not archive), Expected artifacts, Validation, Failure handling, Handoff. |
| 145 | `docs/procedures/update-documentation.md` | REQUIRED | SOP: When and how to update docs alongside code changes. | Per §8.3: Purpose, Trigger (behavior change, new env var, new endpoint, ops change), Prerequisites, Commands (`make docs:check`), Ordered steps (identify affected docs → edit → verify links → update indexes → commit with code), Expected artifacts, Validation, Failure handling, Handoff. |
| 146 | `docs/procedures/update-or-create-skill.md` | REQUIRED | SOP: Skill lifecycle — creating new skills or updating existing ones to the standard format. | Per §8.3: Purpose, Trigger (repeated work pattern, new capability), Prerequisites, Commands (`make skills:list`), Ordered steps (identify need → choose category → create file with all §6.2 sections → link procedures/prompts/rules → add to index → PR), Expected artifacts, Validation, Failure handling, Handoff. |
| 147 | `docs/procedures/update-or-create-rule.md` | REQUIRED | SOP: Rule lifecycle — creating new `.cursor/rules` or updating existing ones. | Per §8.3: Purpose, Trigger (repeated mistake, new constraint), Prerequisites, Commands (`make rules:check`), Ordered steps (identify need → determine scope → create/edit rule file → set frontmatter → test enforcement → PR), Expected artifacts, Validation, Failure handling, Handoff. |
| 148 | `docs/procedures/dependency-upgrade.md` | REQUIRED | SOP: Upgrade dependencies safely with lockfile update and full CI verification. | Per §8.3: Purpose, Trigger (Dependabot alert, manual review), Prerequisites, Commands (`make test`, `make security:scan`), Ordered steps (identify outdated → review changelogs → upgrade → lockfile update → full CI → document breaking changes), Expected artifacts, Validation, Failure handling, Handoff. |
| 149 | `docs/procedures/database-migration.md` | REQUIRED | SOP: Author and apply database migrations with expand/contract pattern and rollback notes. | Per §8.3: Purpose, Trigger (schema change needed), Prerequisites, Commands (`make migrate:create`, `make migrate`), Ordered steps (scaffold revision → write upgrade/downgrade → expand/contract notes → CI dry-run → review → apply with approval gate for prod), Expected artifacts, Validation, Failure handling, Handoff. |
| 150 | `docs/procedures/release-preparation.md` | REQUIRED | SOP: Prepare a release — changelog, version bump, tag, verification, promotion. | Per §8.3: Purpose, Trigger (release scheduled), Prerequisites, Commands (`make release:prepare`, `make release:verify`), Ordered steps (update changelog → bump version → run verify → create tag → promote through environments), Expected artifacts, Validation, Failure handling, Handoff. |
| 151 | `docs/procedures/incident-rollback.md` | REQUIRED | SOP: Rollback during incident — ties to `docs/operations/rollback.md`. | Per §8.3: Purpose, Trigger (production incident requiring rollback), Prerequisites, Commands, Ordered steps (assess severity → decide rollback vs forward-fix per decision tree → execute rollback → verify → document → post-incident review), Expected artifacts, Validation, Failure handling, Handoff. |
| 152 | `docs/procedures/extract-service-from-monolith.md` | REQUIRED | SOP: Extract a bounded context into a standalone service using strangler pattern. | Per §8.3: Purpose, Trigger (extraction criteria met per §12.2), Prerequisites (ADR approved), Commands, Ordered steps (identify boundary → define contract → duplicate behind contract → migrate clients → verify → cutover → remove monolith code), Expected artifacts (ADR, new service, updated contracts), Validation, Failure handling, Handoff. |
| 153 | `docs/procedures/add-optional-app-profile.md` | REQUIRED | SOP: Enable an optional application profile (web, mobile, worker). | Per §8.3: Purpose, Trigger (profile needed), Prerequisites, Commands, Ordered steps (create app directory → add AGENTS.md → configure Compose profile → add env vars → document in `docs/optional-clients/` → test), Expected artifacts, Validation, Failure handling, Handoff. |
| 154 | `docs/procedures/add-queue-category.md` | REQUIRED | SOP: Add a new queue category — update validators, docs, and examples. | Per §8.3: Purpose, Trigger (new work category needed), Prerequisites, Commands (`make queue:validate`), Ordered steps (define category → update validator → update QUEUE_INSTRUCTIONS → add examples → test validation), Expected artifacts, Validation, Failure handling, Handoff. |
| 155 | `docs/procedures/add-prompt-template.md` | REQUIRED | SOP: Add a new prompt template to `prompts/` with full metadata. | Per §8.3: Purpose, Trigger (recurring prompt pattern identified), Prerequisites, Commands (`make prompt:list`), Ordered steps (create template file → add YAML front matter → write prompt body → link procedures/skills → add to index → PR), Expected artifacts, Validation, Failure handling, Handoff. |

#### ADR (Architecture Decision Records)

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 156 | `docs/adr/README.md` | REQUIRED | ADR index. Lists all decisions with status (proposed/accepted/deprecated/superseded). | Table: ADR number, Title, Status, Date, Link. |
| 157 | `docs/adr/template.md` | REQUIRED | ADR template for new decisions. | Sections: Title, Status, Context, Decision, Consequences, Alternatives considered, References. |

#### Agents (human supervision)

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 158 | `docs/agents/README.md` | REQUIRED | Agent supervision documentation index (§9.3). | Link list to child docs. |
| 159 | `docs/agents/supervision-guide.md` | REQUIRED | How a human maintainer supervises agent work: monitoring, intervention triggers, review cadence. | Sections: Supervision philosophy, Monitoring agent output, When to intervene, Review cadence, Communication with agents. |
| 160 | `docs/agents/reviewing-ai-diffs.md` | REQUIRED | How to review AI-generated diffs: security focus, tenant isolation, scope validation, test adequacy. | Sections: Review checklist, Security review points, Tenant isolation verification, Scope creep detection, Test coverage assessment. |
| 161 | `docs/agents/pr-audit-checklist.md` | REQUIRED | Checklist for auditing a PR against acceptance criteria. | Checklist format: Acceptance criteria met, Tests added/updated, Docs updated, Queue state updated, No scope creep, CI green, Evidence provided. |
| 162 | `docs/agents/quality-ratcheting.md` | REQUIRED | How to ratchet quality over time: increasing coverage floors, adding rules, tightening procedures. | Sections: Quality metrics, Ratcheting mechanism, When to tighten, How to update floors, Tracking improvement. |
| 163 | `docs/agents/evolving-from-incidents.md` | REQUIRED | How to evolve rules/skills/prompts from incidents: post-incident analysis → artifact updates. | Sections: Post-incident review process, Identifying encoding opportunities, Creating/updating artifacts, Verification, Follow-up tracking. |

#### Prompts documentation

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 164 | `docs/prompts/README.md` | REQUIRED | Prompt library conventions, metadata format, how to add templates (§7.1, §7.2). | Sections: Metadata convention (YAML front matter), Naming rules, Required fields, How to add a template (link to procedure), Template quality criteria. |
| 165 | `docs/prompts/conventions.md` | REQUIRED | Detailed prompt authoring conventions: placeholder syntax, context injection, output formatting. | Sections: Placeholder syntax (`{{variable}}`), Context injection patterns, Output format requirements, Validation expectations, Versioning approach. |
| 166 | `docs/prompts/index.md` | REQUIRED | Auto-generated or manually maintained index of all prompt templates with metadata summaries. | Table: Template name, Role, When to use, Linked procedures, Linked skills. |

#### Runbooks

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 167 | `docs/runbooks/README.md` | REQUIRED | Runbooks index. | Link list to child docs. |
| 168 | `docs/runbooks/api-down.md` | REQUIRED | Runbook: API service is down or unresponsive (§21). | Sections: Symptoms, Diagnosis steps (check pods, logs, DB connectivity), Resolution steps, Escalation path, Post-resolution. |
| 169 | `docs/runbooks/db-failure.md` | REQUIRED | Runbook: Database failure or connectivity loss. | Sections: Symptoms, Diagnosis steps, Resolution (failover, restart, restore), Escalation, Post-resolution. |
| 170 | `docs/runbooks/jwt-key-rotation.md` | REQUIRED | Runbook: JWT signing key rotation procedure. | Sections: When to rotate, Pre-rotation checklist, Rotation steps, Verification, Rollback if needed, Post-rotation. |
| 171 | `docs/runbooks/chroma-unavailable.md` | OPTIONAL | Runbook: ChromaDB unavailable — graceful degradation via kill switch. | Sections: Symptoms, Kill switch activation, Degraded mode behavior, Recovery steps, Verification. |

#### Release

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 172 | `docs/release/README.md` | REQUIRED | Release documentation index. | Link list to child docs. |
| 173 | `docs/release/versioning.md` | REQUIRED | Versioning strategy: semver, when to bump major/minor/patch, pre-release conventions. | Sections: Semver rules, Version location (pyproject.toml), Bump criteria, Pre-release tags, Breaking change policy. |
| 174 | `docs/release/promotion.md` | REQUIRED | Release promotion path: dev → staging → prod with gates and verification (§11.3). | Sections: Environment definitions, Promotion gates, Verification steps per environment, Approval requirements, Rollback triggers. |
| 175 | `docs/release/changelog-guide.md` | REQUIRED | How to maintain the changelog: format (Keep a Changelog), automation, release notes. | Sections: Changelog format, Entry categories (Added/Changed/Fixed/Removed/Security), Automation hooks, Release notes generation. |

#### Repo Governance

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 176 | `docs/repo-governance/README.md` | REQUIRED | Repo governance documentation index (§20). | Link list to child docs. |
| 177 | `docs/repo-governance/improvement-loops.md` | REQUIRED | Post-task retrospectives and encoding learning into artifacts (§20.2). | Sections: Retrospective trigger, What to capture, Encoding targets (rules, skills, prompts, procedures, tests), PR path for improvements, Tracking. |
| 178 | `docs/repo-governance/audits.md` | REQUIRED | Scheduled repo audits using `make audit:self` (§20.1). | Sections: Audit cadence, Audit scope (spec alignment, doc freshness, skill coverage, rule effectiveness), Running the audit, Reporting findings, Remediation tracking. |
| 179 | `docs/repo-governance/procedure-drift-detection.md` | REQUIRED | Detecting and fixing drift between procedures and actual CI/operations (§20.1). | Sections: What is procedure drift, Detection methods, Review cadence, Fix process, Prevention. |
| 180 | `docs/repo-governance/documentation-freshness.md` | REQUIRED | Keeping docs current: `make docs:check`, quarterly review, staleness indicators (§20.1). | Sections: Freshness criteria, Automated checks, Manual review cadence, Staleness indicators, Update triggers. |

#### Quality

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 181 | `docs/quality/README.md` | REQUIRED | Quality documentation index. | Link list to child docs. |
| 182 | `docs/quality/testing-strategy.md` | REQUIRED | Testing strategy: pyramid, what to test at each level, when to add tests (§11.2). | Sections: Test pyramid, Unit test scope, Integration test scope, Smoke test scope, When to add tests (behavior change, bug fix, new endpoint), Coverage requirements. |
| 183 | `docs/quality/coverage-policy.md` | REQUIRED | Coverage floor definition and ratcheting mechanism. | Sections: Current coverage floor, Measurement tool, CI enforcement, Ratcheting rules (floor only goes up), Exceptions process. |
| 184 | `docs/quality/flake-policy.md` | REQUIRED | Flaky test policy: detection, quarantine, fix SLA, root cause tracking. | Sections: Definition of flaky, Detection mechanism, Quarantine process, Fix SLA, Root cause categories, Prevention practices. |

#### Queue documentation

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 185 | `docs/queue/queue-system-overview.md` | REQUIRED | Queue system conceptual overview: purpose, lifecycle, single-lane semantics, tooling (§17). | Sections: Purpose (agent work orchestration, not PM), File roles (queue.csv, queuearchive.csv), Single-lane semantics, Lifecycle states, Branch naming, PR linking, Batch/phase, Auditing, Conflict resolution. |

#### Optional Clients documentation

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 186 | `docs/optional-clients/web.md` | OPTIONAL | Web frontend profile: when to enable, setup, env vars, operational burden (§15). | Sections: When to enable, When not to enable, Prerequisites, Setup steps, Environment variables, Operational burden, Monitoring. |
| 187 | `docs/optional-clients/mobile.md` | OPTIONAL | Mobile app profile: when to enable, setup, env vars, operational burden (§15). | Sections: When to enable, When not to enable, Prerequisites, Setup steps, Environment variables, Operational burden, Monitoring. |

---

### 26.6 `queue/` — work orchestration files

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 188 | `queue/queue.csv` | REQUIRED | Open work items. First data row under header is the active work item. Rows ordered by priority. Never delete without archiving. | CSV columns (per §17.9): `id`, `batch`, `phase`, `category`, `summary`, `dependencies`, `notes`, `created_date`. Optional: `status`. Header row + data rows. `summary` field MUST be elaborative (goal, acceptance criteria, definition of done, out-of-scope, dependencies). |
| 189 | `queue/queuearchive.csv` | REQUIRED | Completed/cancelled/superseded items. Append-only historical record. | Same columns as `queue.csv` plus: `status` (done/cancelled/superseded), `completed_date`, PR URL in `notes`. |
| 190 | `queue/QUEUE_INSTRUCTIONS.md` | REQUIRED | Human and agent SOP for queue operations. Canonical reference for queue lifecycle, branch naming, PR linking, conflict resolution (§17). | Sections: Overview, File roles, Schema (column definitions), Lifecycle state machine, Single-lane rules, Claiming work, Branch naming (`queue/<id>-slug`), PR linking, Blocked items, Archiving, Batch/phase policy, Conflict resolution, Validation (`make queue:validate`). |
| 191 | `queue/QUEUE_AGENT_PROMPT.md` | REQUIRED | Executable behavior contract for queue processor agents. Injected as context when an agent processes queue work. | Sections: Role definition, Read order (QUEUE_INSTRUCTIONS → top row → linked docs), Execution rules (single item, strict scope, validation before handoff), Branch naming, PR requirements, Archive procedure, Blocked handling, Evidence requirements. |
| 192 | `queue/queue.lock` | RECOMMENDED | Optional mutex file. Prevents concurrent queue processors from claiming the same item. | Format: JSON with fields: `owner` (agent/user id), `claimed_at` (ISO 8601 timestamp), `branch` (branch name), `queue_id` (item being processed). Empty file or absent = no lock. |
| 193 | `queue/audit.log` | RECOMMENDED | Append-only JSON lines log of queue operations (claim, release, archive, reorder). | One JSON object per line: `timestamp`, `action` (claim/release/archive/reorder), `queue_id`, `actor`, `branch`, `notes`. |

---

### 26.7 `.github/` — CI/CD and repository management files

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 194 | `.github/workflows/ci.yml` | REQUIRED | Continuous integration workflow. Runs on PR. Stages: checkout, deps, lint, typecheck, test (unit+integration), image build, image scan, docs check, migration dry-run, k8s validate (§11.2). | GitHub Actions YAML. Jobs: `lint` (ruff check + format check), `typecheck` (mypy/pyright), `test` (pytest with coverage, matrix for SQLite+Postgres), `build` (Docker image build + Trivy scan), `docs` (docs:check), `migrations` (alembic dry-run), `k8s` (k8s:render + k8s:validate). Artifact uploads: test reports, coverage, scan results. |
| 195 | `.github/workflows/cd.yml` | REQUIRED | Continuous deployment workflow. Triggers: main push, semver tags, manual dispatch. Promotion: dev → staging → prod with environment protection (§11.3). | GitHub Actions YAML. Jobs: `deploy-dev` (auto on main), `deploy-staging` (manual approval), `deploy-prod` (manual approval + release:verify). Environment protection rules. Container push to registry. Helm/Kustomize deploy. |
| 196 | `.github/workflows/security.yml` | REQUIRED | Security scanning workflow. Runs on PR and scheduled. Dependency review, code scanning, image scanning. | GitHub Actions YAML. Jobs: `dependency-review` (GitHub dependency review action), `code-scan` (bandit/semgrep), `image-scan` (Trivy). Schedule: weekly or configurable. |
| 197 | `.github/ISSUE_TEMPLATE/bug_report.md` | REQUIRED | Bug report issue template with structured fields. | Frontmatter: name, description, labels. Body: Description, Steps to reproduce, Expected behavior, Actual behavior, Environment, Additional context. |
| 198 | `.github/ISSUE_TEMPLATE/feature_request.md` | REQUIRED | Feature request issue template with structured fields. | Frontmatter: name, description, labels. Body: Problem statement, Proposed solution, Alternatives considered, Additional context. |
| 199 | `.github/ISSUE_TEMPLATE/queue_item.md` | RECOMMENDED | Issue template for items destined for the CSV queue. | Frontmatter: name, description, labels. Body: Summary (elaborate), Category, Dependencies, Acceptance criteria, Definition of done, Out-of-scope. |
| 200 | `.github/PULL_REQUEST_TEMPLATE.md` | REQUIRED | PR description template. Ensures evidence and traceability. | Sections: Summary of changes, Queue item ID (if applicable), Files changed, Commands run with output, Tests added/updated, Documentation updated, Risks and follow-ups, Checklist (CI green, docs updated, queue updated, no scope creep). |
| 201 | `.github/CODEOWNERS` | REQUIRED | Code ownership for review routing. | Format: path patterns → GitHub teams/users. At minimum: `*` → default reviewers, `queue/` → queue maintainers, `.cursor/` → platform maintainers, `docs/` → docs maintainers. |
| 202 | `.github/dependabot.yml` | REQUIRED | Dependabot configuration for automated dependency updates. | YAML: package ecosystems (pip, docker, github-actions), update schedule, reviewers, labels, commit message prefix. |
| 203 | `.github/labels.yml` | RECOMMENDED | Label definitions for issues and PRs. Used by CI or label-sync tools. | YAML array: name, color, description. Labels: priority (P0-P3), type (bug, feature, chore, queue), status (blocked, in-progress), scope (api, docs, infra, queue). |

---

### 26.8 `apps/` — application files

#### `apps/api/` — FastAPI modular monolith (primary)

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 204 | `apps/api/AGENTS.md` | REQUIRED | Scoped agent instructions for the API application. Narrows scope to API concerns; never contradicts root `AGENTS.md`. | Sections: API scope, Module structure, Router registration, Dependency injection patterns, Testing requirements, Import conventions. |
| 205 | `apps/api/Dockerfile` | REQUIRED | Multi-stage Docker build for the API. Non-root user, healthcheck, same image used in CI and production (§16.1). | Stages: `builder` (install deps, copy source), `runner` (minimal runtime, non-root user, HEALTHCHECK instruction, EXPOSE, CMD). |
| 206 | `apps/api/alembic.ini` | REQUIRED | Alembic configuration for database migrations. | Standard alembic.ini: script_location, sqlalchemy.url (from env), file_template, timezone. |
| 207 | `apps/api/alembic/env.py` | REQUIRED | Alembic environment configuration. Supports both SQLite and PostgreSQL connection strings. | Standard alembic env.py with: target_metadata from models, run_migrations_offline, run_migrations_online, engine configuration from env var. |
| 208 | `apps/api/alembic/script.py.mako` | REQUIRED | Alembic migration script template. | Standard Mako template for generating migration files. |
| 209 | `apps/api/alembic/versions/.gitkeep` | REQUIRED | Placeholder to ensure the versions directory exists in version control. | Empty file. |
| 210 | `apps/api/src/__init__.py` | REQUIRED | Package marker for API source. | Empty or minimal `__all__` definition. |
| 211 | `apps/api/src/main.py` | REQUIRED | FastAPI application entry point. Creates app, registers routers, configures middleware, sets up lifespan events. | Structure: app factory function, router registration (health, auth), middleware setup (CORS, tenant, logging), lifespan event handlers (startup/shutdown), error handlers. |
| 212 | `apps/api/src/config.py` | REQUIRED | Configuration management. Reads env vars with validation and defaults. Single source of truth for app configuration (§1.3). | Pydantic `BaseSettings` class with all config fields, validators, env var mappings. Sections grouped: Database, Auth, API, Optional features, Observability. |
| 213 | `apps/api/src/database.py` | REQUIRED | Database connection and session management. Supports SQLite and PostgreSQL via connection string configuration. | Structure: engine creation, session factory, dependency for request-scoped sessions, Base declarative class. |
| 214 | `apps/api/src/middleware.py` | REQUIRED | Shared middleware: CORS, request logging, correlation ID injection, error handling. | Middleware classes/functions: CORSMiddleware config, RequestLoggingMiddleware, CorrelationIdMiddleware, global exception handler. |
| 215 | `apps/api/src/health/__init__.py` | REQUIRED | Package marker for health module. | Router export. |
| 216 | `apps/api/src/health/router.py` | REQUIRED | Health, readiness, and liveness endpoints (§12.1). `/health` (basic), `/ready` (DB + critical deps), `/live` (process alive). | Three endpoints: `GET /health` (always 200), `GET /ready` (checks DB connectivity, returns 200/503), `GET /live` (returns 200). Response schemas with status field. |
| 217 | `apps/api/src/auth/__init__.py` | REQUIRED | Package marker for auth module. | Router and dependency exports. |
| 218 | `apps/api/src/auth/router.py` | REQUIRED | Auth endpoints: register, login, refresh, logout stubs. Policy-complete with extension points (§1.5). | Endpoints: `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`. Request/response schemas. JWT issuance and validation. |
| 219 | `apps/api/src/auth/models.py` | REQUIRED | Auth database models: User, RefreshToken. SQLAlchemy models. | Models: `User` (id, email, hashed_password, is_active, tenant_id, created_at), `RefreshToken` (id, user_id, token, expires_at, revoked). |
| 220 | `apps/api/src/auth/schemas.py` | REQUIRED | Auth Pydantic schemas: request/response models for auth endpoints. | Schemas: `RegisterRequest`, `LoginRequest`, `TokenResponse`, `RefreshRequest`, `UserResponse`. |
| 221 | `apps/api/src/auth/service.py` | REQUIRED | Auth business logic: password hashing, JWT creation/validation, user management. | Functions/class: `create_user`, `authenticate_user`, `create_access_token`, `create_refresh_token`, `verify_token`, `revoke_token`. |
| 222 | `apps/api/src/auth/dependencies.py` | REQUIRED | FastAPI dependencies for auth: `get_current_user`, `require_auth`, optional `require_tenant`. | Dependencies: `get_current_user` (extract and validate JWT from header), `require_auth` (raise 401 if not authenticated), `require_tenant` (extract tenant context). |
| 223 | `apps/api/src/tenancy/__init__.py` | REQUIRED | Package marker for tenancy module. | Middleware and model exports. |
| 224 | `apps/api/src/tenancy/middleware.py` | REQUIRED | Tenant context middleware: extracts tenant from JWT/header, sets request-scoped context for query filtering (§14). | Middleware: extract tenant ID from token claims, set on request state, provide to downstream dependencies. |
| 225 | `apps/api/src/tenancy/models.py` | REQUIRED | Tenant database models: Tenant, TenantMixin for scoped queries. | Models: `Tenant` (id, name, is_active, created_at), `TenantMixin` (mixin class adding tenant_id FK and query scoping). |
| 226 | `apps/api/tests/__init__.py` | REQUIRED | Package marker for tests. | Empty. |
| 227 | `apps/api/tests/conftest.py` | REQUIRED | Shared test fixtures: test client, test database, test user, auth headers. | Fixtures: `app` (FastAPI test app), `client` (httpx.AsyncClient), `db_session` (test database session), `test_user` (seeded user), `auth_headers` (valid JWT headers). |
| 228 | `apps/api/tests/test_health.py` | REQUIRED | Tests for health, readiness, and liveness endpoints. | Tests: `test_health_returns_200`, `test_ready_returns_200_when_db_up`, `test_ready_returns_503_when_db_down`, `test_live_returns_200`. |
| 229 | `apps/api/tests/test_auth.py` | REQUIRED | Tests for auth endpoints: register, login, refresh, logout, error cases. | Tests: `test_register_success`, `test_register_duplicate_email`, `test_login_success`, `test_login_invalid_credentials`, `test_refresh_success`, `test_refresh_expired_token`, `test_logout_success`, `test_protected_endpoint_without_auth`. |

#### `apps/web/` — optional web frontend placeholder

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 230 | `apps/web/README.md` | OPTIONAL | Web frontend placeholder. Documents when/how to enable, prerequisites, and links to `docs/optional-clients/web.md`. | Sections: Status (placeholder), When to enable, Setup instructions, Link to full docs. |
| 231 | `apps/web/AGENTS.md` | OPTIONAL | Scoped agent instructions for web frontend development. | Sections: Scope, Framework conventions, API integration patterns, Testing, Build and deploy. |

#### `apps/mobile/` — optional mobile app placeholder

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 232 | `apps/mobile/README.md` | OPTIONAL | Mobile app placeholder. Documents when/how to enable, prerequisites, and links to `docs/optional-clients/mobile.md`. | Sections: Status (placeholder), When to enable, Setup instructions, Link to full docs. |
| 233 | `apps/mobile/AGENTS.md` | OPTIONAL | Scoped agent instructions for mobile development. | Sections: Scope, Framework conventions, Auth storage patterns, Testing, Build and deploy. |

---

### 26.9 `packages/` — shared package files

#### `packages/contracts/` — shared Pydantic models and OpenAPI

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 234 | `packages/contracts/__init__.py` | REQUIRED | Package marker. Exports shared models and schemas. | Public API exports. |
| 235 | `packages/contracts/models.py` | REQUIRED | Shared Pydantic models used across bounded contexts and by external clients. The contract layer for the modular monolith (§12.1). | Base models, shared schemas (pagination, error responses, common fields), versioned model namespaces. |
| 236 | `packages/contracts/AGENTS.md` | REQUIRED | Scoped agent instructions for the contracts package. Emphasizes backward compatibility, versioning. | Sections: Scope, Backward compatibility rules, Versioning, Testing contract changes. |

#### `packages/tasks/` — background task interfaces

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 237 | `packages/tasks/__init__.py` | REQUIRED | Package marker. Exports task interfaces. | Public API exports. |
| 238 | `packages/tasks/interfaces.py` | REQUIRED | Abstract interfaces for background task execution. Workers are an optional profile (§12.3). | Abstract base classes: `TaskInterface` (submit, status, result), `TaskHandler` (handle), task registration mechanism. |
| 239 | `packages/tasks/AGENTS.md` | REQUIRED | Scoped agent instructions for the tasks package. | Sections: Scope, Interface contracts, Worker profile activation, Testing without workers. |

#### `packages/ai/` — ChromaDB / RAG interfaces (optional)

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 240 | `packages/ai/__init__.py` | OPTIONAL | Package marker. Exports AI/RAG interfaces. | Public API exports with graceful import failure when ChromaDB not installed. |
| 241 | `packages/ai/interfaces.py` | OPTIONAL | Abstract interfaces for AI/RAG operations: embedding, retrieval, generation. Provider-agnostic (§13). | Abstract base classes: `EmbeddingProvider`, `RetrievalProvider`, `GenerationProvider`. Kill switch check decorator. |
| 242 | `packages/ai/chromadb_client.py` | OPTIONAL | ChromaDB client implementation: collection management, ingestion, querying. Behind `packages/ai/interfaces.py`. | ChromaDB-specific implementation of `EmbeddingProvider` and `RetrievalProvider`. Connection config from env. Persistent volume support. |
| 243 | `packages/ai/AGENTS.md` | OPTIONAL | Scoped agent instructions for the AI package. | Sections: Scope, Kill switch behavior, Provider abstraction rules, Testing without AI services. |

---

### 26.10 `deploy/` — deployment configuration files

#### `deploy/docker/`

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 244 | `deploy/docker/README.md` | REQUIRED | Docker deployment documentation. References `docker-compose.yml`, profiles, image build process. | Sections: Overview, Profiles available, Build instructions, Production considerations. |

#### `deploy/k8s/` — Kubernetes manifests

| # | File | Status | Summary | Structure |
|---|------|--------|---------|-----------|
| 245 | `deploy/k8s/README.md` | REQUIRED | Kubernetes deployment documentation. Manifest structure, rendering, validation, deployment. | Sections: Directory structure, Rendering (`make k8s:render`), Validation (`make k8s:validate`), Deployment procedure, Environment overlays. |
| 246 | `deploy/k8s/base/deployment.yaml` | REQUIRED | Base Kubernetes Deployment manifest for the API. Includes probes, resource requests/limits, env vars. | Standard K8s Deployment: metadata, replicas, pod template with container spec, liveness/readiness/startup probes, resource requests/limits, env from ConfigMap/Secret. |
| 247 | `deploy/k8s/base/service.yaml` | REQUIRED | Base Kubernetes Service manifest. Exposes the API deployment. | Standard K8s Service: metadata, selector matching deployment, port configuration. |
| 248 | `deploy/k8s/base/configmap.yaml` | REQUIRED | Base ConfigMap for non-secret configuration values. | Standard K8s ConfigMap: application configuration that varies by environment. |
| 249 | `deploy/k8s/base/kustomization.yaml` | REQUIRED | Kustomize base configuration. References all base resources. | Kustomize: resources list, common labels, namespace. |
| 250 | `deploy/k8s/overlays/dev/kustomization.yaml` | REQUIRED | Dev environment Kustomize overlay. Lower resources, debug settings. | Kustomize: bases reference, patches for dev-specific values (replicas: 1, debug env vars, relaxed resources). |
| 251 | `deploy/k8s/overlays/staging/kustomization.yaml` | REQUIRED | Staging environment Kustomize overlay. Production-like with lower scale. | Kustomize: bases reference, patches for staging values (replicas: 2, staging env vars, moderate resources). |
| 252 | `deploy/k8s/overlays/prod/kustomization.yaml` | REQUIRED | Production environment Kustomize overlay. Full scale, strict settings. | Kustomize: bases reference, patches for prod values (replicas: 3+, production env vars, full resources, PDB). |

---

### 26.11 `scripts/` — command implementation files

Each script implements one or more `Makefile` targets (§10.2). Scripts are the execution layer; the `Makefile` is the interface layer. All scripts MUST be executable (`chmod +x`), use `#!/usr/bin/env bash`, and include `set -euo pipefail`.

| # | File | Status | Summary |
|---|------|--------|---------|
| 253 | `scripts/README.md` | REQUIRED | Scripts index. Documents each script, its corresponding Make target, and expected behavior. |
| 254 | `scripts/dev.sh` | REQUIRED | Start local API with hot reload. Corresponds to `make dev`. |
| 255 | `scripts/lint.sh` | REQUIRED | Run ruff lint checks. Corresponds to `make lint`. |
| 256 | `scripts/fmt.sh` | REQUIRED | Apply ruff formatting. Corresponds to `make fmt`. |
| 257 | `scripts/typecheck.sh` | REQUIRED | Run mypy or pyright type checking. Corresponds to `make typecheck`. |
| 258 | `scripts/test.sh` | REQUIRED | Run full test suite with coverage. Accepts args for `test:unit`, `test:integration`, `test:smoke` variants. Corresponds to `make test`, `make test:unit`, `make test:integration`, `make test:smoke`. |
| 259 | `scripts/migrate.sh` | REQUIRED | Apply database migrations (alembic upgrade head). Accepts `create` arg for `make migrate:create`. Corresponds to `make migrate`, `make migrate:create`. |
| 260 | `scripts/docs-check.sh` | REQUIRED | Check documentation: link validation, build if applicable. Corresponds to `make docs:check`. |
| 261 | `scripts/docs-index.sh` | RECOMMENDED | Regenerate documentation indexes. Corresponds to `make docs:index`. |
| 262 | `scripts/queue-peek.sh` | REQUIRED | Read-only: display header + first open row of queue.csv. Corresponds to `make queue:peek`. |
| 263 | `scripts/queue-validate.sh` | REQUIRED | Validate queue schema, invariants, no duplicate IDs, top-row contract. Corresponds to `make queue:validate`. |
| 264 | `scripts/queue-archive.sh` | RECOMMENDED | Scripted move of a queue row from open to archive. Corresponds to `make queue:archive`. |
| 265 | `scripts/prompt-list.sh` | REQUIRED | List all prompt templates with metadata summary. Corresponds to `make prompt:list`. |
| 266 | `scripts/skills-list.sh` | REQUIRED | List all skills with category and completion status. Corresponds to `make skills:list`. |
| 267 | `scripts/rules-check.sh` | REQUIRED | Validate rule files are present and parsable. Corresponds to `make rules:check`. |
| 268 | `scripts/audit-self.sh` | REQUIRED | Repo self-audit: lint + tests + queue validate + spec link check + artifact inventory. Corresponds to `make audit:self`. |
| 269 | `scripts/security-scan.sh` | REQUIRED | Run security scanning tools (bandit/trivy/etc.). Corresponds to `make security:scan`. |
| 270 | `scripts/image-build.sh` | REQUIRED | Build API container image. Corresponds to `make image:build`. |
| 271 | `scripts/image-scan.sh` | REQUIRED | Scan built container image for vulnerabilities. Corresponds to `make image:scan`. |
| 272 | `scripts/release-prepare.sh` | REQUIRED | Prepare release: changelog update, staging checks. Corresponds to `make release:prepare`. |
| 273 | `scripts/release-verify.sh` | REQUIRED | Pre-tag verification: all checks pass, changelog complete. Corresponds to `make release:verify`. |
| 274 | `scripts/k8s-render.sh` | REQUIRED | Render Kubernetes manifests from Kustomize overlays. Corresponds to `make k8s:render`. |
| 275 | `scripts/k8s-validate.sh` | REQUIRED | Validate rendered manifests with kubeconform/kubeval. Corresponds to `make k8s:validate`. |

---

### 26.12 Enumeration summary

| Category | File count | Required | Recommended | Optional |
|----------|-----------|----------|-------------|----------|
| Root files | 10 | 8 | 0 | 2 |
| `.cursor/` | 8 | 4 | 2 | 2 |
| `prompts/` | 19 | 19 | 0 | 0 |
| `skills/` | 71 | 60 | 4 | 7 |
| `docs/` | 79 | 75 | 0 | 4 |
| `queue/` | 6 | 4 | 2 | 0 |
| `.github/` | 10 | 8 | 2 | 0 |
| `apps/` | 30 | 26 | 0 | 4 |
| `packages/` | 10 | 6 | 0 | 4 |
| `deploy/` | 9 | 9 | 0 | 0 |
| `scripts/` | 23 | 20 | 2 | 1 |
| **TOTAL** | **275** | **239** | **12** | **24** |

---

## 27. Idea-to-repo initialization system

### 27.1 Overview

The template repository is designed to be **cloned and initialized for a specific project**. The initialization flow is:

1. **Human** fills out `idea.md` (the project intake form — §27.2).
2. **Human** opens Cursor in the cloned repo and invokes the initialization agent by referencing `idea.md` and `prompts/repo_initializer.md`.
3. **Initialization agent** reads `idea.md`, validates completeness, maps the idea to a project archetype, enables profiles, scaffolds domain modules, populates the queue, configures environment, and produces an initialization PR.
4. **Human** reviews the initialization PR and merges.
5. **Repo is live** — agents can begin processing queue items.

### 27.2 `idea.md` — project intake form

`idea.md` is a **REQUIRED** root file in the template. It is a structured form that the project owner fills out before initialization. It is the **singular point of reference** for how the repo should be configured.

**Required sections** (all must be present; mark inapplicable ones `N/A`):

| # | Section | Purpose | Initialization agent reads to determine... |
|---|---------|---------|---------------------------------------------|
| 1 | Project identity | Name, slug, one-liner | Repo naming, README content, pyproject.toml name |
| 2 | Problem and solution | What and why | README description, AGENTS.md mission |
| 3 | Project archetype | Category of project | Default profiles, module set, queue categories, deployment shape |
| 4 | Domain model | Entities, contexts, workflows | Module scaffolding in `apps/api/src/`, model files, test stubs |
| 5 | Profile selection | Which optional features to enable | docker-compose profiles, packages to include, deploy config |
| 6 | Auth and authorization | Auth model, roles, permissions | Auth module configuration, middleware, test fixtures |
| 7 | Data layer | Database, caching, external data | Database config, migration setup, connection management |
| 8 | Integrations | External services | Integration module stubs, env vars, circuit breaker setup |
| 9 | API design | Style, versioning, pagination | Router patterns, middleware, OpenAPI config |
| 10 | Non-functional requirements | Performance, compliance, availability | K8s resource config, monitoring setup, security config |
| 11 | Deployment | Target env, cloud, registry | Deploy overlays, CI/CD config, Dockerfile |
| 12 | Initial queue items | First batch of work | `queue/queue.csv` seed data |
| 13 | Constraints and non-goals | Hard limits and exclusions | Rules in `.cursor/rules/`, scope guards in AGENTS.md |
| 14 | Risk register | Known risks and mitigations | ADR stubs, skill selection, test priorities |
| 15 | Timeline and phasing | Milestones | Queue batch assignment, phase tags |
| 16 | Open questions | Unresolved items | Blocked queue items, escalation notes |
| 17 | Additional context | Links, wireframes, references | Reference material for agents |

### 27.3 Archetype-to-profile mapping

The initialization agent maps the selected archetype to default profile enablement:

| Archetype | Profiles enabled by default | Default queue categories |
|-----------|----------------------------|--------------------------|
| API service | workers (optional) | `core-api`, `infrastructure`, `testing`, `documentation` |
| Full-stack web app | web | `core-api`, `frontend`, `infrastructure`, `testing`, `documentation` |
| Full-stack with mobile | web, mobile | `core-api`, `frontend`, `mobile`, `infrastructure`, `testing`, `documentation` |
| Platform / internal tool | workers | `core-api`, `admin`, `infrastructure`, `testing`, `documentation` |
| Data pipeline / ETL | workers, scheduled-jobs | `pipeline`, `infrastructure`, `testing`, `documentation` |
| AI / ML service | ai-rag, workers | `core-api`, `ai`, `infrastructure`, `testing`, `documentation` |
| Marketplace / multi-sided | web, multi-tenancy | `core-api`, `marketplace`, `frontend`, `infrastructure`, `testing`, `documentation` |
| SaaS product | web, multi-tenancy, billing | `core-api`, `saas`, `frontend`, `billing`, `infrastructure`, `testing`, `documentation` |

Humans may override any default by explicitly toggling profiles in §5 of `idea.md`.

### 27.4 Initialization procedure

The initialization agent follows this exact sequence (see also `docs/procedures/initialize-repo.md`):

**Phase 1 — Validate and plan**
1. Read `idea.md` completely.
2. Validate all required sections are filled (not still placeholder comments).
3. Flag open questions (§16) as blockers — create blocked queue items for each.
4. Map archetype → profiles → module set.
5. Produce initialization plan (list of files to create/modify, profiles to enable, queue items to seed).

**Phase 2 — Configure root**
6. Update `README.md` with project name, description, quickstart.
7. Update `pyproject.toml` with project name, description, initial dependencies based on profiles.
8. Update `.env.example` with all required env vars for enabled profiles.
9. Update `docker-compose.yml` to enable/disable profile services.
10. Update `AGENTS.md` mission section with project-specific context from `idea.md` §2.
11. Add project-specific constraints to `.cursor/rules/` from `idea.md` §13.

**Phase 3 — Scaffold domain**
12. For each bounded context in `idea.md` §4.2, create module directory under `apps/api/src/<context>/`:
    - `__init__.py`, `router.py`, `models.py`, `schemas.py`, `service.py`
    - `tests/test_<context>.py` with stub tests for each entity
13. Register all new routers in `apps/api/src/main.py`.
14. Create initial Alembic migration for all domain models.
15. Update `docs/api/endpoints.md` with scaffolded endpoint stubs.

**Phase 4 — Configure profiles**
16. For each enabled profile, run the corresponding sub-procedure:
    - Web → `docs/procedures/add-optional-app-profile.md` for `apps/web/`
    - Mobile → same for `apps/mobile/`
    - Workers → scaffold `packages/tasks/` implementations, add worker service to Compose
    - AI/RAG → scaffold `packages/ai/` implementations, add ChromaDB to Compose
    - Multi-tenancy → verify tenant middleware active, add tenant fixtures to tests
    - Each additional profile (billing, email, search, etc.) → create integration stub under `packages/<profile>/`

**Phase 5 — Seed queue**
17. Populate `queue/queue.csv` from `idea.md` §12.
18. Add blocked items for open questions from `idea.md` §16.
19. Add standard initialization verification items (run all checks, review generated code).
20. Run `make queue:validate` to verify queue integrity.

**Phase 6 — Validate and handoff**
21. Run `make lint && make fmt && make typecheck`.
22. Run `make test` (should pass with stub tests).
23. Run `make audit:self`.
24. Create initialization PR with full evidence.

### 27.5 `prompts/repo_initializer.md` — initialization agent prompt

This is the **most important prompt** in the template. It is the entry point for turning a blank template into a configured project. It MUST be:

- **Fully enumerative** of all options (profiles, archetypes, module patterns).
- **Strictly procedural** — no ambiguity in execution order.
- **Self-validating** — includes checkpoints after each phase.
- **Token-efficient** — uses references to procedures and skills rather than inlining their content.

The prompt template MUST include:
- Role definition (initialization agent with full repo authority).
- Input: `idea.md` (read completely before any action).
- Archetype mapping table (§27.3) for quick lookup.
- Phase-by-phase execution instructions (§27.4) with command checkpoints.
- Profile enablement decision tree.
- Module scaffolding patterns (reference `skills/backend/fastapi-router-module.md`).
- Queue seeding rules (reference `queue/QUEUE_INSTRUCTIONS.md`).
- Validation checklist before PR.
- Output: initialization PR with evidence of all phases completed.

### 27.6 Post-initialization

After the initialization PR is merged:
- `idea.md` remains in the repo as **project context** — agents reference it for domain understanding.
- The first queue item is ready for processing.
- All enabled profiles have scaffolded stubs.
- CI should pass on the initialization commit.

---

## 28. Expanded file enumeration — initialization and skill machinery

This section enumerates additional files beyond §26 that are required for the initialization system, skill machinery (code backing skills), additional scripts, documentation, rules, and procedures discovered through systematic brainstorming of each folder.

**Skill machinery convention:** Skills in `skills/` are not documentation-only. Where a skill benefits from supporting code — validators, generators, linters, formatters, analyzers — the skill folder contains both the `.md` playbook and supporting code files. The `.md` file references the code; the code is invoked by scripts and Make targets. This makes skills **executable machine components**, not just prose.

---

### 28.1 New root files

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 276 | `idea.md` | REQUIRED | Project intake form. Singular input for repo initialization. Structured sections covering identity, archetype, domain model, profiles, auth, data, integrations, API design, NFRs, deployment, queue seed, constraints, risks, timeline, open questions. | All 17 sections with placeholder comments and tables. Human fills this out before initialization. See §27.2 for required sections. |
| 277 | `CHANGELOG.md` | REQUIRED | Project changelog following Keep a Changelog format. Initialized with `[Unreleased]` section. | Sections: header with format link, `[Unreleased]` with subsections (Added, Changed, Fixed, Removed, Security). Populated during releases per `docs/release/changelog-guide.md`. |

---

### 28.2 New prompts

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 278 | `prompts/repo_initializer.md` | REQUIRED | The master initialization prompt. Reads `idea.md`, maps archetype to profiles, scaffolds the entire repo. The most important prompt in the template. | YAML front matter (purpose: initialize repo from idea.md, when_to_use: first action after cloning template, required_inputs: filled idea.md, expected_outputs: initialization PR, linked_procedures: initialize-repo.md, linked_skills: all scaffolding skills). Prompt body: role definition, read order, archetype mapping table, 6-phase execution procedure, profile decision tree, validation checklist, output format. |
| 279 | `prompts/domain_modeler.md` | REQUIRED | Role: analyze `idea.md` domain model and produce bounded context map, entity relationship diagrams, and module scaffolding plan. Used during initialization and when adding new domains. | YAML front matter. Prompt body: read idea.md §4, identify entities and relationships, group into bounded contexts, propose module structure, identify shared vs context-local models, output scaffolding plan. |
| 280 | `prompts/profile_configurator.md` | REQUIRED | Role: enable/disable optional profiles based on idea.md §5 selections. Configures Compose, env vars, package stubs, and documentation for each enabled profile. | YAML front matter. Prompt body: profile decision matrix, per-profile configuration steps (files to create, env vars to add, Compose services to enable, docs to update), validation for each profile. |

---

### 28.3 New procedures

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 281 | `docs/procedures/initialize-repo.md` | REQUIRED | SOP for initializing the repo from `idea.md`. The canonical procedure the `repo_initializer` prompt follows. | Per §8.3 format. Purpose: turn blank template into configured project. Trigger: fresh clone with filled `idea.md`. Prerequisites: `idea.md` complete, template repo cloned. Commands: make targets for each phase. Ordered steps: §27.4 six-phase procedure. Expected artifacts: initialization PR. Validation: `make lint`, `make test`, `make audit:self`. |
| 282 | `docs/procedures/scaffold-domain-module.md` | REQUIRED | SOP for scaffolding a new bounded context module in `apps/api/src/`. Used during initialization and when adding new domains post-init. | Per §8.3 format. Steps: create directory, create `__init__.py` with router export, create `router.py` with CRUD endpoint stubs, create `models.py` with SQLAlchemy models from entity definitions, create `schemas.py` with Pydantic request/response models, create `service.py` with business logic stubs, register router in `main.py`, create `tests/test_<context>.py`, create Alembic migration. |
| 283 | `docs/procedures/enable-profile.md` | REQUIRED | SOP for enabling an optional profile (generalized from `add-optional-app-profile.md`). Covers all profile types with a decision matrix. | Per §8.3 format. Steps: identify profile, check prerequisites, create package/app directory, update docker-compose.yml, add env vars to .env.example, update documentation, add profile-specific tests, validate with `make test`. Per-profile checklists for web, mobile, workers, ai, multi-tenancy, billing, email, search, analytics. |
| 284 | `docs/procedures/validate-idea-md.md` | REQUIRED | SOP for validating that `idea.md` is complete enough for initialization. Lists every required field and validation rules. | Per §8.3 format. Steps: read each section, check for placeholder comments vs real content, validate entity relationships are consistent, verify archetype matches profile selections, check for contradictions between constraints and profile choices, list open questions as blockers. Output: validation report (pass/fail per section, list of blockers). |

---

### 28.4 New documentation files

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 285 | `docs/architecture/system-context.md` | REQUIRED | System context diagram and description. Shows the system boundary, external actors, and integrations. Populated from `idea.md` §8. | Sections: System boundary, External actors (users, services, data sources), Integration points, Data flows, Trust boundaries. Template with placeholders filled during initialization. |
| 286 | `docs/architecture/domain-model.md` | REQUIRED | Domain model documentation. Entity definitions, relationships, bounded context map. Populated from `idea.md` §4. | Sections: Entity catalog (table: entity, context, key fields, relationships), Bounded context map, Context interaction patterns, Aggregate roots, Domain events (if applicable). |
| 287 | `docs/architecture/api-design.md` | REQUIRED | API design decisions: style, versioning, pagination, rate limiting, error handling conventions. Populated from `idea.md` §9. | Sections: API style rationale, Versioning strategy, Pagination convention, Rate limiting policy, Error response format, Authentication header format, Content negotiation. |
| 288 | `docs/development/environment-vars.md` | REQUIRED | Complete environment variable reference. Every env var the system reads, with description, type, default, required/optional, and which profile needs it. | Table format: Variable, Description, Type, Default, Required, Profile. Generated from `.env.example` with expanded descriptions. Updated whenever new env vars are added. |
| 289 | `docs/development/module-patterns.md` | REQUIRED | Reference for the standard module structure in `apps/api/src/`. Shows the canonical file layout, naming conventions, and registration pattern. | Sections: Module directory layout, Router pattern, Model pattern, Schema pattern, Service pattern, Test pattern, Registration in main.py. Code examples for each. |
| 290 | `docs/development/dependency-management.md` | REQUIRED | How to manage Python dependencies: adding, removing, upgrading, lockfile, CI verification. | Sections: Adding a dependency (pyproject.toml), Dev vs production deps, Lockfile management, Upgrade procedure (link to procedure), CI dependency caching, Pinning policy. |
| 291 | `docs/operations/configuration.md` | REQUIRED | Operations configuration reference: how config flows from env vars through Pydantic settings to application code. | Sections: Configuration sources (env vars only — no config files in prod), Pydantic BaseSettings pattern, Validation on startup, Profile-specific config, Secrets vs config distinction. |
| 292 | `docs/operations/health-checks.md` | REQUIRED | Health check documentation: endpoint contracts, probe configuration, dependency checks, degraded states. | Sections: Endpoint reference (/health, /ready, /live), Dependency health checks, Degraded state handling, K8s probe mapping, Monitoring integration. |
| 293 | `docs/agents/initialization-guide.md` | REQUIRED | Guide for the initialization process: what `idea.md` is, how to fill it out, what the initializer does, what to review in the initialization PR. | Sections: Overview of initialization flow, How to fill out idea.md (tips per section), What the initialization agent does (summary of §27.4), How to review the initialization PR, Post-initialization next steps. |
| 294 | `docs/queue/queue-categories.md` | REQUIRED | Registry of valid queue categories with descriptions, validation rules, and examples. Extended during initialization based on archetype. | Table: Category, Description, Example summary, Added by (initialization/manual). Default categories: `core-api`, `infrastructure`, `testing`, `documentation`, `bugfix`, `refactor`, `security`, `devops`. |

---

### 28.5 New `.cursor/rules/` files

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 295 | `.cursor/rules/initialization.md` | REQUIRED | Rules active during repo initialization. Ensures the initializer follows the correct procedure, doesn't skip validation, and produces a complete initialization PR. | Frontmatter: `globs: ["idea.md", "prompts/repo_initializer.md"]`. Rules: must read idea.md completely before any file creation, must follow 6-phase procedure, must run validation after each phase, must not modify spec.md during initialization, must create initialization PR with evidence. |
| 296 | `.cursor/rules/skills.md` | REQUIRED | Rules for skill files. Ensures skills follow the §6.2 structure, include machinery code where applicable, and cross-reference procedures/prompts/rules. | Frontmatter: `globs: ["skills/**"]`. Rules: every skill .md must have all §6.2 headings, machinery code must be referenced from the .md, machinery code must be tested, skills must link to at least one procedure or prompt. |
| 297 | `.cursor/rules/prompts.md` | REQUIRED | Rules for prompt files. Ensures prompts have required YAML front matter and follow the metadata convention. | Frontmatter: `globs: ["prompts/**"]`. Rules: every prompt .md must have YAML front matter with all §7.2 fields, must use `{{placeholder}}` syntax for variable injection, must include validation checklist, must link to at least one procedure. |

---

### 28.6 New scripts

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 298 | `scripts/init-repo.sh` | REQUIRED | Repo initialization orchestrator. Validates `idea.md` is present and non-empty, runs pre-initialization checks, and provides guidance. Corresponds to `make init`. | Bash script: check idea.md exists and is not template-only (grep for un-replaced placeholders), verify Python version, verify Docker, print initialization instructions, optionally run `scripts/validate-idea.sh`. |
| 299 | `scripts/validate-idea.sh` | REQUIRED | Validates `idea.md` completeness. Checks each required section has content beyond placeholder comments. Corresponds to `make idea:validate`. | Bash script: parse idea.md, for each of the 17 sections check that content exists beyond HTML comments, report pass/fail per section, exit non-zero if any required section is empty. |
| 300 | `scripts/scaffold-module.sh` | REQUIRED | Scaffolds a new domain module directory structure. Creates all files from templates. Corresponds to `make scaffold:module`. | Bash script: accepts module name and entity list as args, creates `apps/api/src/<module>/` with `__init__.py`, `router.py`, `models.py`, `schemas.py`, `service.py`, creates `apps/api/tests/test_<module>.py`, registers router in main.py (or prints instruction). |
| 301 | `scripts/profile-enable.sh` | REQUIRED | Enables an optional profile. Modifies docker-compose.yml, .env.example, and creates package stubs. Corresponds to `make profile:enable`. | Bash script: accepts profile name as arg, validates against known profiles, enables Compose service, adds env vars, creates package directory if needed, prints post-enable instructions. |
| 302 | `scripts/idea-to-queue.sh` | RECOMMENDED | Extracts queue items from `idea.md` §12 and writes them to `queue/queue.csv`. Corresponds to `make idea:queue`. | Bash/Python script: parse idea.md §12 table, generate CSV rows with auto-incrementing IDs, batch assignment from idea.md §15, validate with `scripts/queue-validate.sh`. |
| 303 | `scripts/generate-env.sh` | REQUIRED | Generates `.env` from `.env.example` with interactive or default values. Corresponds to `make env:generate`. | Bash script: read .env.example, for each var prompt for value or use default, write .env (gitignored), validate required vars are set. |
| 304 | `scripts/inventory-check.sh` | REQUIRED | Checks that all spec-required files exist. Reports missing files. Corresponds to `make inventory:check`. | Bash script: read the required file list from spec.md §26 (or a manifest file), check each path exists, report missing files with their spec reference, exit non-zero if any required file missing. |

---

### 28.7 Skill machinery files

Skills are not just `.md` documentation — where beneficial, they include **supporting code** that makes the skill executable, more efficient, or machine-verifiable. The `.md` file is the playbook; the code files are the machinery.

**Convention:** Skill machinery code lives alongside the skill `.md` in the same directory. The `.md` references the code file with a `## Machinery` section explaining what the code does and how to invoke it.

#### Agent Operations machinery (`skills/agent-ops/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 305 | `skills/agent-ops/queue-triage.py` | REQUIRED | Queue triage analyzer. Reads `queue.csv`, parses all rows, scores readiness (dependencies met, summary quality, category valid), and outputs a prioritized triage report. Used by the queue-triage skill. | Python script: load CSV, validate schema, for each row check: summary length ≥ 100 chars, category in valid set, dependencies column parseable, no circular deps. Output: sorted triage report with readiness score per item. |
| 306 | `skills/agent-ops/handoff-template-generator.py` | REQUIRED | Generates a pre-filled handoff document from git diff, recent commands, and queue state. Reduces token cost by auto-populating boilerplate. | Python script: read git diff (subprocess), read queue.csv for current item, read recent shell history, generate Markdown handoff template with files changed, commands run, queue state, placeholder sections for risks and follow-ups. |
| 307 | `skills/agent-ops/repo-self-audit.py` | REQUIRED | Automated repo audit. Checks spec compliance: required files exist, skills have all sections, prompts have front matter, procedures have required fields, queue schema valid, Make targets documented. | Python script: inventory check (all §26 files), skill format validation (§6.2 headings present), prompt metadata validation (§7.2 fields), procedure structure validation (§8.3 fields), queue schema validation, Make target documentation check. Output: audit report with pass/fail per check. |

#### Repo Governance machinery (`skills/repo-governance/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 308 | `skills/repo-governance/rule-linter.py` | REQUIRED | Lints `.cursor/rules/` files for correct structure: frontmatter presence, valid glob patterns, no contradictions with other rules. | Python script: parse each rule file, validate YAML frontmatter (alwaysApply or globs), check glob syntax, detect potential contradictions (two rules in same scope with opposing directives), output lint report. |
| 309 | `skills/repo-governance/docs-freshness-checker.py` | REQUIRED | Checks documentation freshness. Compares doc last-modified dates against related code files. Flags docs that may be stale because their related code changed more recently. | Python script: for each doc file, find related code files (by path heuristic or explicit links), compare git timestamps, flag docs where code changed after doc, output staleness report sorted by risk. |
| 310 | `skills/repo-governance/adr-index-generator.py` | REQUIRED | Generates the ADR index (`docs/adr/README.md`) from ADR files. Parses status, title, and date from each ADR and produces a formatted index table. | Python script: scan `docs/adr/` for `*.md` (excluding README.md and template.md), parse title, status, date from each, generate Markdown table sorted by number, write to `docs/adr/README.md`. |

#### Backend / Platform machinery (`skills/backend/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 311 | `skills/backend/module-scaffolder.py` | REQUIRED | Generates a new FastAPI module from templates. Creates router, models, schemas, service, tests with proper imports and registration. More detailed than `scripts/scaffold-module.sh` — produces production-quality stubs. | Python script: accepts module name, entity definitions (name + fields as args or JSON), generates all module files from embedded templates, includes proper imports, type hints, docstrings, test stubs with parametrized cases, outputs file manifest. |
| 312 | `skills/backend/error-code-registry.py` | REQUIRED | Error code registry validator and generator. Maintains a central error code catalog, detects duplicates, generates error documentation, and produces client-facing error reference. | Python script: scan codebase for error code definitions (by convention: `ERROR_` prefix or error enum), validate uniqueness, check all codes are documented in `docs/api/error-codes.md`, generate updated error docs if gaps found. |
| 313 | `skills/backend/env-var-sync.py` | REQUIRED | Synchronizes `.env.example` with actual env var usage in code. Detects vars used in code but missing from `.env.example`, and vars in `.env.example` not used anywhere. | Python script: scan Python files for `os.getenv`, `os.environ`, and Pydantic `Field(env=...)` patterns, compare against `.env.example`, report missing/orphaned vars, optionally auto-add missing vars with `TODO` comments. |
| 314 | `skills/backend/openapi-diff.py` | RECOMMENDED | Compares current OpenAPI spec against a baseline to detect breaking changes. Used before releases and in CI. | Python script: generate current OpenAPI JSON from FastAPI app, compare against stored baseline (`docs/api/openapi-baseline.json`), classify changes as breaking/non-breaking per OpenAPI compatibility rules, output diff report. |

#### Security machinery (`skills/security/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 315 | `skills/security/secret-scanner.py` | REQUIRED | Scans codebase for potential secrets: high-entropy strings, known secret patterns (API keys, tokens, passwords), and env vars with default values that look like secrets. | Python script: regex patterns for common secret formats (AWS keys, JWT tokens, base64 blobs > 40 chars, password= assignments), scan all Python/YAML/JSON/MD files, exclude `.env.example` intentional placeholders, output findings with file:line references. |
| 316 | `skills/security/dependency-audit.py` | REQUIRED | Audits Python dependencies for known vulnerabilities. Wraps `pip-audit` or `safety` with structured output and severity classification. | Python script: run pip-audit (subprocess), parse output, classify by severity (critical/high/medium/low), cross-reference with project's accepted-risk list (`docs/security/accepted-risks.md` if exists), output actionable report. |
| 317 | `skills/security/tenant-isolation-checker.py` | REQUIRED | Static analysis for tenant isolation. Scans SQLAlchemy queries for missing tenant filters, checks that all tenant-scoped models use TenantMixin, verifies middleware is applied to relevant routes. | Python script: parse Python AST, find all query expressions, check for tenant_id filter on tenant-scoped models, verify TenantMixin inheritance, check router dependency chains include tenant middleware, output isolation report. |

#### Testing machinery (`skills/testing/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 318 | `skills/testing/test-scaffolder.py` | REQUIRED | Generates test stubs for a given module. Analyzes router endpoints and service methods, produces parametrized test functions with descriptive names and TODO bodies. | Python script: parse router file for endpoint decorators, parse service file for public methods, generate test functions following naming convention (`test_<unit>_<scenario>_<expected>`), include fixture usage, output test file content. |
| 319 | `skills/testing/coverage-ratchet.py` | REQUIRED | Reads current coverage, compares against floor defined in `docs/quality/coverage-policy.md`, updates the floor if coverage improved, fails if coverage dropped below floor. | Python script: parse coverage report (JSON or XML), read current floor from policy doc, compare, if coverage > floor update policy doc floor value, if coverage < floor exit non-zero with gap report. |
| 320 | `skills/testing/flaky-detector.py` | RECOMMENDED | Detects potentially flaky tests by running the test suite N times and identifying tests that sometimes pass and sometimes fail. | Python script: run pytest N times (configurable, default 5), collect per-test pass/fail results, identify tests with inconsistent results, output flaky test report with failure patterns. |

#### DevOps machinery (`skills/devops/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 321 | `skills/devops/dockerfile-linter.py` | REQUIRED | Lints Dockerfiles for best practices: multi-stage build, non-root user, no `latest` tags, HEALTHCHECK present, layer ordering for cache efficiency. | Python script: parse Dockerfile, check for required directives (USER non-root, HEALTHCHECK, multi-stage FROM), warn on anti-patterns (COPY before dependency install, RUN with `apt-get` without cleanup, `latest` image tags), output lint report. |
| 322 | `skills/devops/k8s-manifest-validator.py` | REQUIRED | Validates Kubernetes manifests beyond schema: checks for resource requests/limits, probe configuration, security context, namespace consistency. | Python script: parse YAML manifests, validate: all Deployments have resource requests+limits, all containers have liveness+readiness probes, securityContext.runAsNonRoot set, namespace matches overlay, output validation report. |
| 323 | `skills/devops/compose-profile-matrix.py` | RECOMMENDED | Tests Docker Compose profile combinations. Validates that each profile can be enabled independently and in common combinations without conflicts. | Python script: enumerate profiles from docker-compose.yml, test each individual profile and key combinations (`docker compose config --profiles X`), validate no port conflicts or missing dependency services, output compatibility matrix. |

#### Initialization machinery (`skills/init/`)

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 324 | `skills/init/README.md` | REQUIRED | Index for initialization skills. Lists all skills used during the repo initialization process from `idea.md`. | Skill index with links to each init skill file and its machinery. |
| 325 | `skills/init/idea-validator.md` | REQUIRED [FULL] | Skill: validate `idea.md` completeness and consistency. Uses `skills/init/idea-validator.py` machinery. | Full §6.2 skill format. Purpose: ensure idea.md is complete before initialization. Steps: run validator, review report, resolve issues with human. Machinery section references `idea-validator.py`. |
| 326 | `skills/init/idea-validator.py` | REQUIRED | Validates `idea.md` structure and content completeness. Checks every required section has real content (not just HTML comment placeholders), validates internal consistency (archetype matches profiles, entities match contexts). | Python script: parse Markdown sections, for each section check content length > threshold, detect un-replaced placeholder patterns (`<!-- ... -->`), validate archetype-profile consistency, validate entity-context coverage (every entity appears in at least one context), output validation report with section-by-section pass/fail. |
| 327 | `skills/init/archetype-mapper.md` | REQUIRED [FULL] | Skill: map idea.md archetype and profile selections to concrete file scaffolding plan. Uses `skills/init/archetype-mapper.py` machinery. | Full §6.2 skill format. Purpose: translate abstract idea into concrete file list. Steps: read archetype, apply profile defaults, generate file manifest, output module plan. |
| 328 | `skills/init/archetype-mapper.py` | REQUIRED | Maps project archetype to default profiles, queue categories, module set, and file manifest. Produces a structured initialization plan as JSON. | Python script: archetype-to-profile mapping table (§27.3), profile-to-files mapping (which files each profile requires), module template for each bounded context, output JSON plan: `{profiles: [], modules: [], queue_categories: [], files_to_create: [], files_to_modify: []}`. |
| 329 | `skills/init/module-template-generator.md` | REQUIRED [FULL] | Skill: generate all files for a new domain module from entity definitions. Uses `skills/backend/module-scaffolder.py` machinery. | Full §6.2 skill format. References the backend module scaffolder for actual file generation. Adds initialization-specific concerns: bulk module creation, router registration order, migration sequencing. |
| 330 | `skills/init/queue-seeder.md` | REQUIRED | Skill: populate `queue/queue.csv` from idea.md §12 and §15. Assigns batch IDs from phases, generates proper summaries, validates with `make queue:validate`. | Skill format with steps: parse idea.md §12, assign IDs, map phases to batches, generate elaborative summaries from user's input, add standard initialization verification items, run `make queue:validate`. |
| 331 | `skills/init/queue-seeder.py` | REQUIRED | Extracts queue items from idea.md and generates properly formatted queue.csv rows. Assigns IDs, batches from phases, and validates summaries meet minimum quality bar. | Python script: parse idea.md §12 Markdown table, extract rows, assign sequential IDs, map priority to phase/batch, expand terse summaries with context from idea.md §4 (entities) and §9 (API), validate summary length ≥ 100 chars, output CSV rows. |
| 332 | `skills/init/profile-resolver.md` | REQUIRED | Skill: resolve profile enablement from idea.md §5 and archetype defaults. Handles conflicts and dependencies between profiles (e.g., billing requires multi-tenancy for SaaS). | Skill format with steps: read archetype defaults (§27.3), overlay explicit selections from §5, check profile dependencies (billing requires auth, workers requires broker choice, ai requires ChromaDB), flag conflicts, output resolved profile set. |
| 333 | `skills/init/profile-resolver.py` | REQUIRED | Resolves profile enablement with dependency checking. Profiles can have dependencies (billing → auth + multi-tenancy), conflicts (SQLite-only + multi-tenancy at scale), and defaults per archetype. | Python script: profile dependency graph (dict of profile → required profiles), conflict rules, archetype defaults, merge algorithm: archetype defaults + explicit overrides, expand dependencies, check conflicts, output resolved set with warnings. |
| 334 | `skills/init/env-generator.md` | REQUIRED | Skill: generate `.env.example` tailored to enabled profiles. Each profile adds its required env vars with documentation comments. | Skill format with steps: start with base env vars (DB, Auth, API), add per-profile vars, organize into sections with comments, validate no duplicate var names, output `.env.example`. |
| 335 | `skills/init/env-generator.py` | REQUIRED | Generates `.env.example` content based on enabled profiles. Each profile has a defined set of env vars with defaults and documentation. | Python script: base vars dict (DATABASE_URL, JWT_SECRET, etc.), per-profile var dicts, merge based on enabled profiles, format with section headers and inline comments, output `.env.example` content. |

---

### 28.8 New Makefile targets

The following additional Make targets are required to support initialization and skill machinery:

| Target | Purpose | Script |
|--------|---------|--------|
| `init` | Run initialization pre-checks and guidance | `scripts/init-repo.sh` |
| `idea:validate` | Validate idea.md completeness | `scripts/validate-idea.sh` |
| `scaffold:module` | Scaffold a new domain module | `scripts/scaffold-module.sh` |
| `profile:enable` | Enable an optional profile | `scripts/profile-enable.sh` |
| `idea:queue` | Extract queue items from idea.md | `scripts/idea-to-queue.sh` |
| `env:generate` | Generate .env from .env.example | `scripts/generate-env.sh` |
| `inventory:check` | Verify all spec-required files exist | `scripts/inventory-check.sh` |

---

### 28.9 New `.cursor/commands/`

| # | File | Status | Summary | Initial content |
|---|------|--------|---------|-----------------|
| 336 | `.cursor/commands/initialize.md` | REQUIRED | Reusable command: run the full repo initialization flow. Reads idea.md, invokes repo_initializer prompt, follows 6-phase procedure. | Command metadata: name "Initialize Repo", description, steps (validate idea.md → read repo_initializer prompt → execute 6-phase procedure), links to `prompts/repo_initializer.md` and `docs/procedures/initialize-repo.md`. |
| 337 | `.cursor/commands/scaffold-module.md` | REQUIRED | Reusable command: scaffold a new domain module from entity definitions. | Command metadata: name "Scaffold Module", description, args (module name, entities), steps (run scaffolder → register router → create migration → add tests), links to `skills/backend/module-scaffolder.py`. |
| 338 | `.cursor/commands/audit.md` | REQUIRED | Reusable command: run comprehensive repo self-audit. | Command metadata: name "Repo Audit", steps (make audit:self → review report → create issues for findings), links to `skills/agent-ops/repo-self-audit.py`. |

---

### 28.10 Enumeration summary update

| Category | Previous count | New files | Updated total |
|----------|---------------|-----------|---------------|
| Root files | 10 | 2 (idea.md, CHANGELOG.md) | 12 |
| `.cursor/rules/` | 6 | 3 | 9 |
| `.cursor/commands/` | 2 | 3 | 5 |
| `prompts/` | 19 | 3 | 22 |
| `skills/` (with machinery) | 71 | 31 | 102 |
| `docs/` | 79 | 14 | 93 |
| `queue/` | 6 | 0 | 6 |
| `.github/` | 10 | 0 | 10 |
| `apps/` | 30 | 0 | 30 |
| `packages/` | 10 | 0 | 10 |
| `deploy/` | 9 | 0 | 9 |
| `scripts/` | 23 | 7 | 30 |
| **TOTAL** | **275** | **63** | **338** |

---

## 29. Full repository file and folder structure (updated)

```
repo-root/
├── AGENTS.md
├── spec.md
├── README.md
├── idea.md                                         # project intake form
├── CHANGELOG.md
├── .env.example
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md                              # optional
│
├── .cursor/
│   ├── rules/
│   │   ├── global.md
│   │   ├── apps-api.md
│   │   ├── security.md
│   │   ├── queue.md
│   │   ├── testing.md                              # recommended
│   │   ├── documentation.md                        # recommended
│   │   ├── initialization.md
│   │   ├── skills.md
│   │   └── prompts.md
│   └── commands/
│       ├── validate.md                             # optional
│       ├── queue-next.md                           # optional
│       ├── initialize.md
│       ├── scaffold-module.md
│       └── audit.md
│
├── prompts/
│   ├── README.md
│   ├── repo_initializer.md                         # master initialization prompt
│   ├── domain_modeler.md
│   ├── profile_configurator.md
│   ├── task_planner.md
│   ├── implementation_agent.md
│   ├── reviewer_critic.md
│   ├── test_writer.md
│   ├── debugger.md
│   ├── refactorer.md
│   ├── documentation_updater.md
│   ├── migration_author.md
│   ├── queue_processor.md
│   ├── release_manager.md
│   ├── dependency_upgrade_agent.md
│   ├── security_review_agent.md
│   ├── incident_triage_agent.md
│   ├── performance_audit_agent.md
│   ├── repo_bootstrap_agent.md
│   ├── spec_hardening_agent.md
│   ├── skill_authoring_agent.md
│   └── rule_authoring_agent.md
│
├── skills/
│   ├── README.md
│   ├── init/                                       # initialization skills + machinery
│   │   ├── README.md
│   │   ├── idea-validator.md
│   │   ├── idea-validator.py
│   │   ├── archetype-mapper.md
│   │   ├── archetype-mapper.py
│   │   ├── module-template-generator.md
│   │   ├── queue-seeder.md
│   │   ├── queue-seeder.py
│   │   ├── profile-resolver.md
│   │   ├── profile-resolver.py
│   │   ├── env-generator.md
│   │   └── env-generator.py
│   ├── agent-ops/
│   │   ├── queue-triage.md
│   │   ├── queue-triage.py                         # machinery
│   │   ├── task-planning.md
│   │   ├── implementation-handoff.md
│   │   ├── handoff-template-generator.py           # machinery
│   │   ├── blocked-task-recovery.md
│   │   ├── prompt-to-procedure-promotion.md
│   │   ├── rule-refinement-after-mistakes.md
│   │   ├── post-pr-audit.md
│   │   ├── repo-self-audit.md
│   │   └── repo-self-audit.py                      # machinery
│   ├── repo-governance/
│   │   ├── writing-agents-md.md
│   │   ├── authoring-cursor-rules.md
│   │   ├── adding-reusable-commands.md
│   │   ├── maintaining-procedural-docs.md
│   │   ├── writing-adrs.md
│   │   ├── changelogs-release-notes.md
│   │   ├── repository-hygiene.md
│   │   ├── rule-linter.py                          # machinery
│   │   ├── docs-freshness-checker.py               # machinery
│   │   └── adr-index-generator.py                  # machinery
│   ├── backend/
│   │   ├── fastapi-router-module.md
│   │   ├── service-repository-pattern.md
│   │   ├── health-readiness-liveness.md
│   │   ├── api-versioning.md
│   │   ├── background-jobs.md
│   │   ├── worker-integration.md
│   │   ├── idempotent-tasks.md
│   │   ├── configuration-management.md
│   │   ├── feature-flags.md
│   │   ├── error-taxonomy.md
│   │   ├── structured-logging.md
│   │   ├── opentelemetry-tracing.md
│   │   ├── metrics-exposition.md
│   │   ├── rate-limiting.md
│   │   ├── retries-circuit-breakers.md
│   │   ├── safe-migration-rollout.md
│   │   ├── sqlite-to-postgres.md
│   │   ├── module-scaffolder.py                    # machinery
│   │   ├── error-code-registry.py                  # machinery
│   │   ├── env-var-sync.py                         # machinery
│   │   └── openapi-diff.py                         # machinery (recommended)
│   ├── security/
│   │   ├── secret-handling.md
│   │   ├── token-lifecycle.md
│   │   ├── rbac-tenant-isolation.md
│   │   ├── dependency-review.md
│   │   ├── code-scanning.md
│   │   ├── image-scanning.md
│   │   ├── sbom-attestation.md                     # recommended
│   │   ├── secure-defaults-review.md
│   │   ├── incident-evidence-capture.md
│   │   ├── secret-scanner.py                       # machinery
│   │   ├── dependency-audit.py                     # machinery
│   │   └── tenant-isolation-checker.py             # machinery
│   ├── testing/
│   │   ├── pytest-conventions.md
│   │   ├── async-testing.md
│   │   ├── api-contract-testing.md
│   │   ├── snapshot-testing.md
│   │   ├── smoke-tests.md
│   │   ├── regression-harness.md
│   │   ├── load-test-basics.md                     # recommended
│   │   ├── flaky-test-triage.md
│   │   ├── validation-loop-design.md
│   │   ├── test-scaffolder.py                      # machinery
│   │   ├── coverage-ratchet.py                     # machinery
│   │   └── flaky-detector.py                       # machinery (recommended)
│   ├── devops/
│   │   ├── docker-multi-stage-builds.md
│   │   ├── compose-profiles.md
│   │   ├── k8s-probes.md
│   │   ├── rollout-rollback.md
│   │   ├── github-actions-troubleshooting.md
│   │   ├── release-promotion.md
│   │   ├── artifact-publishing.md
│   │   ├── environment-configuration.md
│   │   ├── backup-restore-drills.md                # recommended
│   │   ├── dockerfile-linter.py                    # machinery
│   │   ├── k8s-manifest-validator.py               # machinery
│   │   └── compose-profile-matrix.py               # machinery (recommended)
│   ├── ai-rag/                                     # optional profile
│   │   ├── chromadb-ingestion.md
│   │   ├── embedding-refresh.md
│   │   ├── retrieval-evaluation.md
│   │   ├── prompt-versioning.md
│   │   ├── ai-kill-switch.md
│   │   ├── model-provider-abstraction.md
│   │   └── ai-safety-review.md
│   └── frontend/                                   # optional profile
│       ├── generated-client-usage.md
│       ├── react-api-integration.md
│       ├── expo-auth-storage.md
│       └── frontend-env-handling.md
│
├── docs/
│   ├── README.md
│   ├── getting-started/
│   │   ├── README.md
│   │   ├── prerequisites.md
│   │   └── quickstart.md
│   ├── architecture/
│   │   ├── README.md
│   │   ├── modular-monolith.md
│   │   ├── data-layer.md
│   │   ├── auth-multi-tenancy.md
│   │   ├── ai-rag-chromadb.md                      # optional
│   │   ├── system-context.md
│   │   ├── domain-model.md
│   │   └── api-design.md
│   ├── development/
│   │   ├── README.md
│   │   ├── local-setup.md
│   │   ├── coding-standards.md
│   │   ├── testing-guide.md
│   │   ├── environment-vars.md
│   │   ├── module-patterns.md
│   │   └── dependency-management.md
│   ├── api/
│   │   ├── README.md
│   │   ├── endpoints.md
│   │   └── error-codes.md
│   ├── operations/
│   │   ├── README.md
│   │   ├── docker.md
│   │   ├── kubernetes.md
│   │   ├── observability.md
│   │   ├── backups.md
│   │   ├── rollback.md
│   │   ├── configuration.md
│   │   └── health-checks.md
│   ├── security/
│   │   ├── README.md
│   │   ├── threat-model-stub.md
│   │   ├── secrets-management.md
│   │   ├── incident-response.md
│   │   └── token-lifecycle.md
│   ├── procedures/
│   │   ├── README.md
│   │   ├── initialize-repo.md
│   │   ├── scaffold-domain-module.md
│   │   ├── enable-profile.md
│   │   ├── validate-idea-md.md
│   │   ├── start-queue-item.md
│   │   ├── plan-change.md
│   │   ├── implement-change.md
│   │   ├── validate-change.md
│   │   ├── open-pull-request.md
│   │   ├── handoff.md
│   │   ├── archive-queue-item.md
│   │   ├── handle-blocked-work.md
│   │   ├── update-documentation.md
│   │   ├── update-or-create-skill.md
│   │   ├── update-or-create-rule.md
│   │   ├── dependency-upgrade.md
│   │   ├── database-migration.md
│   │   ├── release-preparation.md
│   │   ├── incident-rollback.md
│   │   ├── extract-service-from-monolith.md
│   │   ├── add-optional-app-profile.md
│   │   ├── add-queue-category.md
│   │   └── add-prompt-template.md
│   ├── adr/
│   │   ├── README.md
│   │   └── template.md
│   ├── agents/
│   │   ├── README.md
│   │   ├── initialization-guide.md
│   │   ├── supervision-guide.md
│   │   ├── reviewing-ai-diffs.md
│   │   ├── pr-audit-checklist.md
│   │   ├── quality-ratcheting.md
│   │   └── evolving-from-incidents.md
│   ├── prompts/
│   │   ├── README.md
│   │   ├── conventions.md
│   │   └── index.md
│   ├── runbooks/
│   │   ├── README.md
│   │   ├── api-down.md
│   │   ├── db-failure.md
│   │   ├── jwt-key-rotation.md
│   │   └── chroma-unavailable.md                   # optional
│   ├── release/
│   │   ├── README.md
│   │   ├── versioning.md
│   │   ├── promotion.md
│   │   └── changelog-guide.md
│   ├── repo-governance/
│   │   ├── README.md
│   │   ├── improvement-loops.md
│   │   ├── audits.md
│   │   ├── procedure-drift-detection.md
│   │   └── documentation-freshness.md
│   ├── quality/
│   │   ├── README.md
│   │   ├── testing-strategy.md
│   │   ├── coverage-policy.md
│   │   └── flake-policy.md
│   ├── queue/
│   │   ├── queue-system-overview.md
│   │   └── queue-categories.md
│   └── optional-clients/
│       ├── web.md                                  # optional
│       └── mobile.md                               # optional
│
├── queue/
│   ├── queue.csv
│   ├── queuearchive.csv
│   ├── QUEUE_INSTRUCTIONS.md
│   ├── QUEUE_AGENT_PROMPT.md
│   ├── queue.lock                                  # recommended
│   └── audit.log                                   # recommended
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── cd.yml
│   │   └── security.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── queue_item.md                           # recommended
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   └── labels.yml                                  # recommended
│
├── apps/
│   ├── api/
│   │   ├── AGENTS.md
│   │   ├── Dockerfile
│   │   ├── alembic.ini
│   │   ├── alembic/
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions/
│   │   │       └── .gitkeep
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── middleware.py
│   │   │   ├── health/
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   └── dependencies.py
│   │   │   └── tenancy/
│   │   │       ├── __init__.py
│   │   │       ├── middleware.py
│   │   │       └── models.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       ├── test_health.py
│   │       └── test_auth.py
│   ├── web/                                        # optional profile
│   │   ├── README.md
│   │   └── AGENTS.md
│   └── mobile/                                     # optional profile
│       ├── README.md
│       └── AGENTS.md
│
├── packages/
│   ├── contracts/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── AGENTS.md
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── interfaces.py
│   │   └── AGENTS.md
│   └── ai/                                        # optional profile
│       ├── __init__.py
│       ├── interfaces.py
│       ├── chromadb_client.py
│       └── AGENTS.md
│
├── deploy/
│   ├── docker/
│   │   └── README.md
│   └── k8s/
│       ├── README.md
│       ├── base/
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   ├── configmap.yaml
│       │   └── kustomization.yaml
│       └── overlays/
│           ├── dev/
│           │   └── kustomization.yaml
│           ├── staging/
│           │   └── kustomization.yaml
│           └── prod/
│               └── kustomization.yaml
│
└── scripts/
    ├── README.md
    ├── dev.sh
    ├── lint.sh
    ├── fmt.sh
    ├── typecheck.sh
    ├── test.sh
    ├── migrate.sh
    ├── docs-check.sh
    ├── docs-index.sh                               # recommended
    ├── queue-peek.sh
    ├── queue-validate.sh
    ├── queue-archive.sh                            # recommended
    ├── prompt-list.sh
    ├── skills-list.sh
    ├── rules-check.sh
    ├── audit-self.sh
    ├── security-scan.sh
    ├── image-build.sh
    ├── image-scan.sh
    ├── release-prepare.sh
    ├── release-verify.sh
    ├── k8s-render.sh
    ├── k8s-validate.sh
    ├── init-repo.sh
    ├── validate-idea.sh
    ├── scaffold-module.sh
    ├── profile-enable.sh
    ├── idea-to-queue.sh                            # recommended
    ├── generate-env.sh
    └── inventory-check.sh
```

---

## 30. Folder summary table

| # | Folder | Purpose |
|---|--------|---------|
| 1 | `/` (repo root) | Top-level control plane and configuration. Contains `AGENTS.md`, `spec.md`, `idea.md`, `README.md`, `Makefile`, `pyproject.toml`, `docker-compose.yml`, `.env.example`, `CHANGELOG.md`, and legal files. Everything an agent or human needs to orient and begin work. |
| 2 | `.cursor/` | Machine-control layer for Cursor IDE. Houses persistent rules and reusable commands that shape agent behavior during development sessions. |
| 3 | `.cursor/rules/` | Always-on and path-scoped constraints. Global rules apply everywhere; path-scoped rules activate only in matching directories. Agents load these automatically. Includes initialization, skills, and prompts rules. |
| 4 | `.cursor/commands/` | Reusable Cursor command definitions. Shortcuts that invoke canonical scripts or document exact command sequences. Includes initialization, scaffolding, and audit commands. |
| 5 | `prompts/` | Reusable, versioned prompt templates for recurring agent roles. Each template has metadata (purpose, inputs, outputs, linked procedures/skills) and a prompt body with placeholders. Includes the master `repo_initializer` prompt. |
| 6 | `skills/` | Executable playbooks organized by category. Each skill has a `.md` playbook and may include supporting code (machinery) for automation, validation, and generation. |
| 7 | `skills/init/` | Initialization skills and machinery. Used during repo initialization from `idea.md`: validation, archetype mapping, module scaffolding, queue seeding, profile resolution, env generation. |
| 8 | `skills/agent-ops/` | Skills for agent-specific operations: queue triage, task planning, handoffs, blocked recovery, prompt promotion, rule refinement, auditing. Includes Python machinery for queue analysis, handoff generation, and self-audit. |
| 9 | `skills/repo-governance/` | Skills for maintaining the repository machine: writing `AGENTS.md`, authoring rules, maintaining procedures, writing ADRs, changelogs, hygiene. Includes machinery for rule linting, docs freshness checking, and ADR index generation. |
| 10 | `skills/backend/` | Skills for backend/platform development: FastAPI patterns, service layers, health endpoints, API versioning, background jobs, configuration, logging, metrics, tracing, rate limiting, migrations. Includes machinery for module scaffolding, error code registry, env var sync, and OpenAPI diffing. |
| 11 | `skills/security/` | Skills for security and compliance: secret handling, token lifecycle, RBAC/tenant isolation, dependency review, code/image scanning, SBOM, incident evidence. Includes machinery for secret scanning, dependency auditing, and tenant isolation checking. |
| 12 | `skills/testing/` | Skills for testing and quality: pytest conventions, async testing, contract testing, snapshots, smoke tests, regression, load testing, flaky triage, validation loops. Includes machinery for test scaffolding, coverage ratcheting, and flaky detection. |
| 13 | `skills/devops/` | Skills for DevOps and operations: Docker builds, Compose profiles, K8s probes, rollout/rollback, GitHub Actions, release promotion, artifact publishing, env config, backup/restore. Includes machinery for Dockerfile linting, K8s manifest validation, and Compose profile testing. |
| 14 | `skills/ai-rag/` | Skills for AI/RAG operations (optional profile): ChromaDB ingestion, embedding refresh, retrieval evaluation, prompt versioning, kill switch, provider abstraction, safety review. |
| 15 | `skills/frontend/` | Skills for optional frontend/mobile profiles: generated clients, React API integration, Expo auth storage, frontend env handling. |
| 16 | `docs/` | Documentation hub. All conceptual and operational documentation organized by subsystem. Every major subsystem has both a conceptual explanation (why) and an operational explanation (how). |
| 17 | `docs/getting-started/` | Onboarding documentation: prerequisites, quickstart from clone to running dev server with passing tests. |
| 18 | `docs/architecture/` | Architecture documentation: modular monolith design, data layer strategy, auth/multi-tenancy, AI/RAG architecture, system context, domain model, API design. |
| 19 | `docs/development/` | Development documentation: local setup with all Make targets, coding standards, testing guide, env var reference, module patterns, dependency management. |
| 20 | `docs/api/` | API documentation: endpoint catalog, error code taxonomy. |
| 21 | `docs/operations/` | Operations documentation: Docker, Kubernetes, observability, backups, rollback, configuration, health checks. |
| 22 | `docs/security/` | Security documentation: threat model, secrets management, incident response, token lifecycle. |
| 23 | `docs/procedures/` | Standard Operating Procedures. Canonical workflows written for agents first, usable by humans. Includes initialization, scaffolding, profile enablement, and idea validation procedures alongside all original SOPs. |
| 24 | `docs/adr/` | Architecture Decision Records. Index of all architectural decisions with template for new ones. |
| 25 | `docs/agents/` | Agent supervision documentation for human maintainers: initialization guide, supervision, review AI diffs, audit PRs, ratchet quality, evolve from incidents. |
| 26 | `docs/prompts/` | Prompt library documentation: conventions, metadata format, authoring guide, index of all templates. |
| 27 | `docs/runbooks/` | Operational runbooks for specific failure scenarios: API down, DB failure, JWT key rotation, ChromaDB unavailable. |
| 28 | `docs/release/` | Release documentation: versioning strategy, promotion path (dev → staging → prod), changelog guide. |
| 29 | `docs/repo-governance/` | Repository governance documentation: improvement loops, audits, procedure drift detection, documentation freshness. |
| 30 | `docs/quality/` | Quality documentation: testing strategy, coverage policy and floors, flaky test policy. |
| 31 | `docs/queue/` | Queue system documentation: conceptual overview of the CSV-based agent work orchestration system, queue category registry. |
| 32 | `docs/optional-clients/` | Documentation for optional application profiles (web, mobile): when to enable, setup, operational burden. |
| 33 | `queue/` | Agent work orchestration lane. CSV-based queue with strict lifecycle, single-lane processing, audit logging, and validation tooling. |
| 34 | `.github/` | GitHub repository management: CI/CD workflows, issue templates, PR template, code ownership, dependency management, labels. |
| 35 | `.github/workflows/` | GitHub Actions workflow definitions: CI (lint, typecheck, test, build, scan), CD (deploy through environments), security scanning. |
| 36 | `.github/ISSUE_TEMPLATE/` | GitHub issue templates: structured forms for bug reports, feature requests, and queue items. |
| 37 | `apps/` | Application code. Contains the primary API and optional frontend/mobile profiles. Each app may have its own scoped `AGENTS.md`. |
| 38 | `apps/api/` | FastAPI modular monolith — the primary application. Health endpoints, auth stubs, tenant hooks, Alembic migrations, Docker build, tests. |
| 39 | `apps/api/alembic/` | Database migration configuration and version scripts (Alembic). |
| 40 | `apps/api/alembic/versions/` | Individual migration version files. Starts with `.gitkeep`; populated as schema evolves. |
| 41 | `apps/api/src/` | API application source code organized by bounded context (health, auth, tenancy). |
| 42 | `apps/api/src/health/` | Health module: health, readiness, and liveness endpoints for operational monitoring and K8s probes. |
| 43 | `apps/api/src/auth/` | Authentication module: register, login, refresh, logout endpoints with JWT token management. Policy-complete stubs with extension points. |
| 44 | `apps/api/src/tenancy/` | Multi-tenancy module: tenant context middleware, tenant models, query scoping mixin. |
| 45 | `apps/api/tests/` | API test suite: health endpoint tests, auth endpoint tests, shared fixtures and configuration. |
| 46 | `apps/web/` | Optional web frontend placeholder. Contains README and scoped AGENTS.md when profile is enabled. |
| 47 | `apps/mobile/` | Optional mobile app placeholder. Contains README and scoped AGENTS.md when profile is enabled. |
| 48 | `packages/` | Shared packages used across bounded contexts and applications. Contracts, task interfaces, AI interfaces. |
| 49 | `packages/contracts/` | Shared Pydantic models and OpenAPI schemas. The contract layer for the modular monolith — backward compatibility is mandatory. |
| 50 | `packages/tasks/` | Background task interfaces. Abstract base classes for task submission and handling. Workers are an optional profile. |
| 51 | `packages/ai/` | AI/RAG interfaces (optional profile). Provider-agnostic abstractions for embedding, retrieval, and generation with ChromaDB implementation. |
| 52 | `deploy/` | Deployment configuration for Docker and Kubernetes. |
| 53 | `deploy/docker/` | Docker-specific deployment documentation and configurations. |
| 54 | `deploy/k8s/` | Kubernetes manifests organized with Kustomize: base resources and environment-specific overlays. |
| 55 | `deploy/k8s/base/` | Base Kubernetes manifests: Deployment, Service, ConfigMap, Kustomization. Shared across all environments. |
| 56 | `deploy/k8s/overlays/` | Environment-specific Kustomize overlays that patch base manifests for dev, staging, and production. |
| 57 | `deploy/k8s/overlays/dev/` | Dev environment overlay: single replica, debug settings, relaxed resource limits. |
| 58 | `deploy/k8s/overlays/staging/` | Staging environment overlay: production-like configuration at lower scale. |
| 59 | `deploy/k8s/overlays/prod/` | Production environment overlay: full scale, strict settings, pod disruption budgets. |
| 60 | `scripts/` | Shell script implementations backing Makefile targets. The execution layer for all canonical commands including initialization and scaffolding. |

---

## 31. File summary table — every file

| # | File path | Purpose | Spec reference |
|---|-----------|---------|----------------|
| 1 | `AGENTS.md` | Root agent control plane: mission, hierarchy, workflows, validation, queue, escalation, anti-patterns | §4 |
| 2 | `spec.md` | Canonical full specification — this document | §25 |
| 3 | `README.md` | Quickstart entry point with links to key docs and command catalog | §3 |
| 4 | `.env.example` | Environment variable template with all vars documented | §3 |
| 5 | `docker-compose.yml` | Docker Compose orchestration with profiles for optional services | §16.1 |
| 6 | `Makefile` | Single canonical command entrypoint — all 27+ Make targets | §10 |
| 7 | `pyproject.toml` | Python project config: deps, dev tools (ruff, mypy, pytest) | §3 |
| 8 | `LICENSE` | Open-source license (MIT or Apache-2.0) | §23 |
| 9 | `CONTRIBUTING.md` | Contribution guide linking AGENTS.md, queue, procedures | §23 |
| 10 | `CODE_OF_CONDUCT.md` | Community standards (optional) | §23 |
| 11 | `.cursor/rules/global.md` | Universal agent constraints: commits, scope, evidence, forbidden patterns | §5 |
| 12 | `.cursor/rules/apps-api.md` | Path-scoped API rules: router patterns, DI, Pydantic models, test naming | §5 |
| 13 | `.cursor/rules/security.md` | Security invariants: secret sources, JWT, tenant isolation, prohibited patterns | §5, §14 |
| 14 | `.cursor/rules/queue.md` | Queue invariants: schema, lifecycle, archive-before-delete, summary requirements | §5, §17 |
| 15 | `.cursor/rules/testing.md` | Testing standards: naming, fixtures, mock boundaries, async patterns (recommended) | §5 |
| 16 | `.cursor/rules/documentation.md` | Documentation update triggers: when docs must change with code (recommended) | §5 |
| 17 | `.cursor/commands/validate.md` | Reusable command: full validation suite (optional) | §5.1 |
| 18 | `.cursor/commands/queue-next.md` | Reusable command: claim next queue item (optional) | §5.1 |
| 19 | `prompts/README.md` | Prompt library overview: metadata convention, naming, adding templates | §7 |
| 20 | `prompts/task_planner.md` | Role template: decompose work, acceptance criteria, risks | §7.3 |
| 21 | `prompts/implementation_agent.md` | Role template: code change execution with scope discipline | §7.3 |
| 22 | `prompts/reviewer_critic.md` | Role template: adversarial review against spec and security | §7.3 |
| 23 | `prompts/test_writer.md` | Role template: tests aligned to acceptance criteria | §7.3 |
| 24 | `prompts/debugger.md` | Role template: systematic failure isolation | §7.3 |
| 25 | `prompts/refactorer.md` | Role template: behavior-preserving structural changes | §7.3 |
| 26 | `prompts/documentation_updater.md` | Role template: docs aligned to code and ops | §7.3 |
| 27 | `prompts/migration_author.md` | Role template: DB migrations with rollback notes | §7.3 |
| 28 | `prompts/queue_processor.md` | Role template: single top-row queue execution | §7.3 |
| 29 | `prompts/release_manager.md` | Role template: versioning, changelog, release verification | §7.3 |
| 30 | `prompts/dependency_upgrade_agent.md` | Role template: safe dep bumps with CI evidence | §7.3 |
| 31 | `prompts/security_review_agent.md` | Role template: threat-focused review | §7.3 |
| 32 | `prompts/incident_triage_agent.md` | Role template: initial classification and evidence | §7.3 |
| 33 | `prompts/performance_audit_agent.md` | Role template: latency/resource review | §7.3 |
| 34 | `prompts/repo_bootstrap_agent.md` | Role template: new clone to green dev | §7.3 |
| 35 | `prompts/spec_hardening_agent.md` | Role template: spec/procedure alignment PRs | §7.3 |
| 36 | `prompts/skill_authoring_agent.md` | Role template: new or updated skills to standard | §7.3 |
| 37 | `prompts/rule_authoring_agent.md` | Role template: new or updated rules, scoped | §7.3 |
| 38 | `skills/README.md` | Skills library index by category with format guide | §6 |
| 39 | `skills/agent-ops/queue-triage.md` | Skill [FULL]: read, interpret, prioritize queue items | §6.3 |
| 40 | `skills/agent-ops/task-planning.md` | Skill [FULL]: decompose task into steps with acceptance criteria | §6.3 |
| 41 | `skills/agent-ops/implementation-handoff.md` | Skill [FULL]: write complete handoff documentation | §6.3 |
| 42 | `skills/agent-ops/blocked-task-recovery.md` | Skill: handle blocked work — document, escalate, requeue | §6.3 |
| 43 | `skills/agent-ops/prompt-to-procedure-promotion.md` | Skill: promote successful one-off prompt to prompts/ | §6.3 |
| 44 | `skills/agent-ops/rule-refinement-after-mistakes.md` | Skill: author/update rules after repeated mistakes | §6.3 |
| 45 | `skills/agent-ops/post-pr-audit.md` | Skill: audit completed PR against acceptance criteria | §6.3 |
| 46 | `skills/agent-ops/repo-self-audit.md` | Skill [FULL]: run audit:self, verify spec alignment, find drift | §6.3 |
| 47 | `skills/repo-governance/writing-agents-md.md` | Skill [FULL]: author/update AGENTS.md per §4 | §6.3 |
| 48 | `skills/repo-governance/authoring-cursor-rules.md` | Skill [FULL]: create/update .cursor/rules files | §6.3 |
| 49 | `skills/repo-governance/adding-reusable-commands.md` | Skill: add entries to commands/ or Makefile | §6.3 |
| 50 | `skills/repo-governance/maintaining-procedural-docs.md` | Skill: keep docs/procedures/ current and linked | §6.3 |
| 51 | `skills/repo-governance/writing-adrs.md` | Skill: author Architecture Decision Records | §6.3 |
| 52 | `skills/repo-governance/changelogs-release-notes.md` | Skill: maintain changelogs and release notes | §6.3 |
| 53 | `skills/repo-governance/repository-hygiene.md` | Skill: periodic cleanup — stale branches, orphaned docs, dead code | §6.3 |
| 54 | `skills/backend/fastapi-router-module.md` | Skill [FULL]: add new FastAPI router/module end-to-end | §6.3 |
| 55 | `skills/backend/service-repository-pattern.md` | Skill [FULL]: implement service/repository layers | §6.3 |
| 56 | `skills/backend/health-readiness-liveness.md` | Skill: implement and verify health/ready/live endpoints | §6.3 |
| 57 | `skills/backend/api-versioning.md` | Skill: version API endpoints with deprecation path | §6.3 |
| 58 | `skills/backend/background-jobs.md` | Skill: define and register background jobs | §6.3 |
| 59 | `skills/backend/worker-integration.md` | Skill: enable worker profile, connect broker, verify | §6.3 |
| 60 | `skills/backend/idempotent-tasks.md` | Skill: design idempotent task handlers | §6.3 |
| 61 | `skills/backend/configuration-management.md` | Skill: add new configuration end-to-end | §6.3 |
| 62 | `skills/backend/feature-flags.md` | Skill: implement env-based feature flags | §6.3 |
| 63 | `skills/backend/error-taxonomy.md` | Skill: define stable error codes and response shapes | §6.3 |
| 64 | `skills/backend/structured-logging.md` | Skill: implement structured logging with correlation IDs | §6.3 |
| 65 | `skills/backend/opentelemetry-tracing.md` | Skill: add OpenTelemetry tracing spans and context | §6.3 |
| 66 | `skills/backend/metrics-exposition.md` | Skill: expose Prometheus metrics endpoint | §6.3 |
| 67 | `skills/backend/rate-limiting.md` | Skill: implement rate limiting middleware | §6.3 |
| 68 | `skills/backend/retries-circuit-breakers.md` | Skill: implement retry logic and circuit breakers | §6.3 |
| 69 | `skills/backend/safe-migration-rollout.md` | Skill [FULL]: roll out DB migrations safely (expand/contract) | §6.3 |
| 70 | `skills/backend/sqlite-to-postgres.md` | Skill: migrate from SQLite to PostgreSQL | §6.3 |
| 71 | `skills/security/secret-handling.md` | Skill [FULL]: handle secrets — env-only, rotation, documentation | §6.3 |
| 72 | `skills/security/token-lifecycle.md` | Skill: JWT token lifecycle management | §6.3, §14 |
| 73 | `skills/security/rbac-tenant-isolation.md` | Skill: verify RBAC and tenant isolation | §6.3, §14 |
| 74 | `skills/security/dependency-review.md` | Skill: review dependency changes for CVEs and licenses | §6.3 |
| 75 | `skills/security/code-scanning.md` | Skill: run and triage code scanning results | §6.3 |
| 76 | `skills/security/image-scanning.md` | Skill: scan container images and triage findings | §6.3 |
| 77 | `skills/security/sbom-attestation.md` | Skill: generate SBOMs and attestations (recommended) | §6.3 |
| 78 | `skills/security/secure-defaults-review.md` | Skill: audit codebase for secure defaults | §6.3 |
| 79 | `skills/security/incident-evidence-capture.md` | Skill: capture and preserve incident evidence | §6.3 |
| 80 | `skills/testing/pytest-conventions.md` | Skill [FULL]: pytest project conventions and patterns | §6.3 |
| 81 | `skills/testing/async-testing.md` | Skill: test async FastAPI code with pytest-asyncio | §6.3 |
| 82 | `skills/testing/api-contract-testing.md` | Skill: API contract tests and OpenAPI alignment | §6.3 |
| 83 | `skills/testing/snapshot-testing.md` | Skill: snapshot testing for API responses | §6.3 |
| 84 | `skills/testing/smoke-tests.md` | Skill: write and run smoke tests | §6.3 |
| 85 | `skills/testing/regression-harness.md` | Skill: add regression tests after bug fixes | §6.3 |
| 86 | `skills/testing/load-test-basics.md` | Skill: basic load testing setup (recommended) | §6.3 |
| 87 | `skills/testing/flaky-test-triage.md` | Skill: identify, isolate, and fix flaky tests | §6.3 |
| 88 | `skills/testing/validation-loop-design.md` | Skill: design validation loops for agent workflows | §6.3 |
| 89 | `skills/devops/docker-multi-stage-builds.md` | Skill: build efficient multi-stage Docker images | §6.3 |
| 90 | `skills/devops/compose-profiles.md` | Skill: manage Docker Compose profiles | §6.3 |
| 91 | `skills/devops/k8s-probes.md` | Skill: configure Kubernetes probes | §6.3 |
| 92 | `skills/devops/rollout-rollback.md` | Skill: perform K8s rollouts and rollbacks | §6.3 |
| 93 | `skills/devops/github-actions-troubleshooting.md` | Skill: debug failing GitHub Actions | §6.3 |
| 94 | `skills/devops/release-promotion.md` | Skill: promote releases through environments | §6.3 |
| 95 | `skills/devops/artifact-publishing.md` | Skill: publish build artifacts to registries | §6.3 |
| 96 | `skills/devops/environment-configuration.md` | Skill: manage environment-specific configuration | §6.3 |
| 97 | `skills/devops/backup-restore-drills.md` | Skill: perform backup and restore drills (recommended) | §6.3 |
| 98 | `skills/ai-rag/chromadb-ingestion.md` | Skill: ingest documents into ChromaDB (optional) | §6.3 |
| 99 | `skills/ai-rag/embedding-refresh.md` | Skill: refresh embeddings when sources change (optional) | §6.3 |
| 100 | `skills/ai-rag/retrieval-evaluation.md` | Skill: evaluate retrieval quality (optional) | §6.3 |
| 101 | `skills/ai-rag/prompt-versioning.md` | Skill: version AI prompts with A/B testing (optional) | §6.3 |
| 102 | `skills/ai-rag/ai-kill-switch.md` | Skill: implement and test AI kill switch (optional) | §6.3 |
| 103 | `skills/ai-rag/model-provider-abstraction.md` | Skill: abstract model/provider dependencies (optional) | §6.3 |
| 104 | `skills/ai-rag/ai-safety-review.md` | Skill: review AI outputs for safety (optional) | §6.3 |
| 105 | `skills/frontend/generated-client-usage.md` | Skill: use auto-generated API clients (optional) | §6.3 |
| 106 | `skills/frontend/react-api-integration.md` | Skill: integrate React with FastAPI backend (optional) | §6.3 |
| 107 | `skills/frontend/expo-auth-storage.md` | Skill: handle auth tokens in Expo (optional) | §6.3 |
| 108 | `skills/frontend/frontend-env-handling.md` | Skill: manage frontend env vars (optional) | §6.3 |
| 109 | `docs/README.md` | Documentation hub index with links to all sections | §9 |
| 110 | `docs/getting-started/README.md` | Getting started section index | §9 |
| 111 | `docs/getting-started/prerequisites.md` | Required tools, versions, and verification commands | §9 |
| 112 | `docs/getting-started/quickstart.md` | Step-by-step from clone to running dev with passing tests | §9 |
| 113 | `docs/architecture/README.md` | Architecture section index | §9 |
| 114 | `docs/architecture/modular-monolith.md` | Modular monolith design, boundaries, extraction criteria | §9, §12 |
| 115 | `docs/architecture/data-layer.md` | Data layer: SQLite vs Postgres, migration strategy | §9, §13 |
| 116 | `docs/architecture/auth-multi-tenancy.md` | Auth flow, JWT lifecycle, tenant isolation, SSO hooks | §9, §14 |
| 117 | `docs/architecture/ai-rag-chromadb.md` | AI/RAG with ChromaDB: architecture, kill switch (optional) | §9, §13 |
| 118 | `docs/development/README.md` | Development section index | §9 |
| 119 | `docs/development/local-setup.md` | Local dev setup, all Make targets documented | §9, §10 |
| 120 | `docs/development/coding-standards.md` | Coding standards enforced by ruff, mypy, conventions | §9 |
| 121 | `docs/development/testing-guide.md` | How to write and run tests: conventions, fixtures, coverage | §9 |
| 122 | `docs/api/README.md` | API documentation section index | §9 |
| 123 | `docs/api/endpoints.md` | API endpoint catalog with request/response schemas | §9 |
| 124 | `docs/api/error-codes.md` | Error code taxonomy with HTTP status mappings | §9 |
| 125 | `docs/operations/README.md` | Operations section index | §9 |
| 126 | `docs/operations/docker.md` | Docker operations: build, run, profiles, troubleshooting | §9 |
| 127 | `docs/operations/kubernetes.md` | K8s operations: rendering, validation, deployment, scaling | §9 |
| 128 | `docs/operations/observability.md` | Observability: logging, metrics, tracing, dashboards, alerts | §9, §21 |
| 129 | `docs/operations/backups.md` | Backup/restore procedures for databases and volumes | §9 |
| 130 | `docs/operations/rollback.md` | Rollback vs forward-fix decision tree and procedures | §2, §9 |
| 131 | `docs/security/README.md` | Security section index | §9 |
| 132 | `docs/security/threat-model-stub.md` | Threat model template: assets, actors, surfaces, mitigations | §9 |
| 133 | `docs/security/secrets-management.md` | Secrets management: sources, rotation, CI injection, audit | §9 |
| 134 | `docs/security/incident-response.md` | Incident response plan: classification, evidence, comms, remediation | §2, §9 |
| 135 | `docs/security/token-lifecycle.md` | JWT lifecycle details: issuance, refresh, revocation, rotation | §9, §14 |
| 136 | `docs/procedures/README.md` | Procedures index listing all SOPs | §8 |
| 137 | `docs/procedures/start-queue-item.md` | SOP: claim top queue row, create branch, read docs | §8.2 |
| 138 | `docs/procedures/plan-change.md` | SOP: create implementation plan with criteria and risks | §8.2 |
| 139 | `docs/procedures/implement-change.md` | SOP: execute code changes in small validated increments | §8.2 |
| 140 | `docs/procedures/validate-change.md` | SOP: run full validation matrix before PR | §8.2 |
| 141 | `docs/procedures/open-pull-request.md` | SOP: create PR with template, evidence, labels, queue link | §8.2 |
| 142 | `docs/procedures/handoff.md` | SOP: complete handoff — files, commands, results, risks | §8.2 |
| 143 | `docs/procedures/archive-queue-item.md` | SOP: move completed row to archive with required fields | §8.2 |
| 144 | `docs/procedures/handle-blocked-work.md` | SOP: document blockers, escalate, optionally requeue | §8.2 |
| 145 | `docs/procedures/update-documentation.md` | SOP: when and how to update docs alongside code | §8.2 |
| 146 | `docs/procedures/update-or-create-skill.md` | SOP: skill lifecycle — create/update to standard format | §8.2 |
| 147 | `docs/procedures/update-or-create-rule.md` | SOP: rule lifecycle — create/update with proper scoping | §8.2 |
| 148 | `docs/procedures/dependency-upgrade.md` | SOP: safe dependency upgrade with lockfile and CI | §8.2 |
| 149 | `docs/procedures/database-migration.md` | SOP: author migrations with expand/contract and rollback | §8.2 |
| 150 | `docs/procedures/release-preparation.md` | SOP: prepare release — changelog, tag, verification | §8.2 |
| 151 | `docs/procedures/incident-rollback.md` | SOP: rollback during incident, ties to rollback.md | §8.2 |
| 152 | `docs/procedures/extract-service-from-monolith.md` | SOP: extract bounded context via strangler pattern | §8.2 |
| 153 | `docs/procedures/add-optional-app-profile.md` | SOP: enable optional app profile (web/mobile/worker) | §8.2 |
| 154 | `docs/procedures/add-queue-category.md` | SOP: add queue category — validators, docs, examples | §8.2 |
| 155 | `docs/procedures/add-prompt-template.md` | SOP: add prompt template with full metadata | §8.2 |
| 156 | `docs/adr/README.md` | ADR index: all decisions with status and dates | §9 |
| 157 | `docs/adr/template.md` | ADR template: title, status, context, decision, consequences | §9 |
| 158 | `docs/agents/README.md` | Agent supervision documentation index | §9.3 |
| 159 | `docs/agents/supervision-guide.md` | How to supervise agent work: monitoring, intervention | §9.3 |
| 160 | `docs/agents/reviewing-ai-diffs.md` | How to review AI diffs: security, tenant, scope, tests | §9.3 |
| 161 | `docs/agents/pr-audit-checklist.md` | PR audit checklist against acceptance criteria | §9.3 |
| 162 | `docs/agents/quality-ratcheting.md` | How to ratchet quality: coverage floors, rules, procedures | §9.3 |
| 163 | `docs/agents/evolving-from-incidents.md` | How to evolve artifacts from incidents | §9.3 |
| 164 | `docs/prompts/README.md` | Prompt library conventions and metadata format | §7 |
| 165 | `docs/prompts/conventions.md` | Detailed prompt authoring conventions | §7 |
| 166 | `docs/prompts/index.md` | Index of all prompt templates with metadata summaries | §7 |
| 167 | `docs/runbooks/README.md` | Runbooks index | §9, §21 |
| 168 | `docs/runbooks/api-down.md` | Runbook: API down — diagnosis, resolution, escalation | §21 |
| 169 | `docs/runbooks/db-failure.md` | Runbook: DB failure — failover, restart, restore | §21 |
| 170 | `docs/runbooks/jwt-key-rotation.md` | Runbook: JWT key rotation procedure | §14, §21 |
| 171 | `docs/runbooks/chroma-unavailable.md` | Runbook: ChromaDB unavailable — kill switch (optional) | §13, §21 |
| 172 | `docs/release/README.md` | Release documentation index | §9 |
| 173 | `docs/release/versioning.md` | Versioning strategy: semver rules, bump criteria | §9, §11.3 |
| 174 | `docs/release/promotion.md` | Release promotion: dev → staging → prod gates | §9, §11.3 |
| 175 | `docs/release/changelog-guide.md` | Changelog format, automation, release notes generation | §9 |
| 176 | `docs/repo-governance/README.md` | Repo governance documentation index | §20 |
| 177 | `docs/repo-governance/improvement-loops.md` | Post-task retrospectives and encoding learning | §20 |
| 178 | `docs/repo-governance/audits.md` | Scheduled repo audits with audit:self | §20 |
| 179 | `docs/repo-governance/procedure-drift-detection.md` | Detecting drift between procedures and reality | §20 |
| 180 | `docs/repo-governance/documentation-freshness.md` | Keeping docs current: checks, reviews, staleness | §20 |
| 181 | `docs/quality/README.md` | Quality documentation index | §9 |
| 182 | `docs/quality/testing-strategy.md` | Testing strategy: pyramid, scopes, when to add tests | §9, §11.2 |
| 183 | `docs/quality/coverage-policy.md` | Coverage floor, measurement, CI enforcement, ratcheting | §9 |
| 184 | `docs/quality/flake-policy.md` | Flaky test policy: detection, quarantine, fix SLA | §9 |
| 185 | `docs/queue/queue-system-overview.md` | Queue system overview: purpose, lifecycle, semantics | §9, §17 |
| 186 | `docs/optional-clients/web.md` | Web frontend profile: enable/disable, burden (optional) | §9, §15 |
| 187 | `docs/optional-clients/mobile.md` | Mobile app profile: enable/disable, burden (optional) | §9, §15 |
| 188 | `queue/queue.csv` | Open work items — top data row is active item | §17 |
| 189 | `queue/queuearchive.csv` | Completed/cancelled items — append-only history | §17 |
| 190 | `queue/QUEUE_INSTRUCTIONS.md` | Human + agent queue SOP: lifecycle, naming, conflicts | §17 |
| 191 | `queue/QUEUE_AGENT_PROMPT.md` | Agent behavior contract for queue processing | §17 |
| 192 | `queue/queue.lock` | Optional mutex preventing concurrent queue claims (recommended) | §17.7 |
| 193 | `queue/audit.log` | Append-only JSON lines log of queue operations (recommended) | §17.7 |
| 194 | `.github/workflows/ci.yml` | CI workflow: lint, typecheck, test, build, scan, docs, migrations, k8s | §11.2 |
| 195 | `.github/workflows/cd.yml` | CD workflow: deploy dev → staging → prod with gates | §11.3 |
| 196 | `.github/workflows/security.yml` | Security workflow: dependency review, code scan, image scan | §11.1 |
| 197 | `.github/ISSUE_TEMPLATE/bug_report.md` | Bug report template with structured fields | §11.1 |
| 198 | `.github/ISSUE_TEMPLATE/feature_request.md` | Feature request template with structured fields | §11.1 |
| 199 | `.github/ISSUE_TEMPLATE/queue_item.md` | Queue item template for CSV queue intake (recommended) | §11.1 |
| 200 | `.github/PULL_REQUEST_TEMPLATE.md` | PR template: summary, evidence, checklist, queue link | §11.1 |
| 201 | `.github/CODEOWNERS` | Code ownership for review routing | §11.1 |
| 202 | `.github/dependabot.yml` | Dependabot config: pip, docker, github-actions ecosystems | §11.1 |
| 203 | `.github/labels.yml` | Label definitions for issues and PRs (recommended) | §11.1 |
| 204 | `apps/api/AGENTS.md` | Scoped agent instructions for API application | §3 |
| 205 | `apps/api/Dockerfile` | Multi-stage Docker build: builder + runner, non-root, healthcheck | §16.1 |
| 206 | `apps/api/alembic.ini` | Alembic migration configuration | §13 |
| 207 | `apps/api/alembic/env.py` | Alembic environment: SQLite + Postgres support | §13 |
| 208 | `apps/api/alembic/script.py.mako` | Alembic migration script template | §13 |
| 209 | `apps/api/alembic/versions/.gitkeep` | Migration versions directory placeholder | §13 |
| 210 | `apps/api/src/__init__.py` | API source package marker | §12 |
| 211 | `apps/api/src/main.py` | FastAPI entry point: app factory, routers, middleware, lifespan | §12 |
| 212 | `apps/api/src/config.py` | Configuration via Pydantic BaseSettings, env var validation | §12 |
| 213 | `apps/api/src/database.py` | Database engine, session factory, Base class | §13 |
| 214 | `apps/api/src/middleware.py` | Shared middleware: CORS, logging, correlation IDs, error handling | §12, §21 |
| 215 | `apps/api/src/health/__init__.py` | Health module package marker | §12 |
| 216 | `apps/api/src/health/router.py` | Health, readiness, and liveness endpoints | §12 |
| 217 | `apps/api/src/auth/__init__.py` | Auth module package marker | §14 |
| 218 | `apps/api/src/auth/router.py` | Auth endpoints: register, login, refresh, logout | §14 |
| 219 | `apps/api/src/auth/models.py` | Auth DB models: User, RefreshToken | §14 |
| 220 | `apps/api/src/auth/schemas.py` | Auth Pydantic schemas: request/response models | §14 |
| 221 | `apps/api/src/auth/service.py` | Auth business logic: passwords, JWT, user management | §14 |
| 222 | `apps/api/src/auth/dependencies.py` | FastAPI auth dependencies: get_current_user, require_auth | §14 |
| 223 | `apps/api/src/tenancy/__init__.py` | Tenancy module package marker | §14 |
| 224 | `apps/api/src/tenancy/middleware.py` | Tenant context extraction and request-scoped state | §14 |
| 225 | `apps/api/src/tenancy/models.py` | Tenant DB models: Tenant, TenantMixin for query scoping | §14 |
| 226 | `apps/api/tests/__init__.py` | Test package marker | §12 |
| 227 | `apps/api/tests/conftest.py` | Shared test fixtures: client, DB, test user, auth headers | §12 |
| 228 | `apps/api/tests/test_health.py` | Health endpoint tests: health, ready, live | §12 |
| 229 | `apps/api/tests/test_auth.py` | Auth endpoint tests: register, login, refresh, errors | §14 |
| 230 | `apps/web/README.md` | Web frontend placeholder and setup guide (optional) | §15 |
| 231 | `apps/web/AGENTS.md` | Scoped agent instructions for web frontend (optional) | §15 |
| 232 | `apps/mobile/README.md` | Mobile app placeholder and setup guide (optional) | §15 |
| 233 | `apps/mobile/AGENTS.md` | Scoped agent instructions for mobile app (optional) | §15 |
| 234 | `packages/contracts/__init__.py` | Contracts package marker with public API exports | §12.1 |
| 235 | `packages/contracts/models.py` | Shared Pydantic models: pagination, errors, common fields | §12.1 |
| 236 | `packages/contracts/AGENTS.md` | Scoped instructions: backward compat, versioning | §12.1 |
| 237 | `packages/tasks/__init__.py` | Tasks package marker with interface exports | §12.3 |
| 238 | `packages/tasks/interfaces.py` | Abstract task interfaces: submit, handle, status | §12.3 |
| 239 | `packages/tasks/AGENTS.md` | Scoped instructions: interface contracts, worker profile | §12.3 |
| 240 | `packages/ai/__init__.py` | AI package marker with graceful import (optional) | §13 |
| 241 | `packages/ai/interfaces.py` | AI/RAG abstract interfaces: embed, retrieve, generate (optional) | §13 |
| 242 | `packages/ai/chromadb_client.py` | ChromaDB implementation of AI interfaces (optional) | §13 |
| 243 | `packages/ai/AGENTS.md` | Scoped instructions: kill switch, provider abstraction (optional) | §13 |
| 244 | `deploy/docker/README.md` | Docker deployment documentation and profile reference | §16.1 |
| 245 | `deploy/k8s/README.md` | K8s deployment documentation: structure, render, validate, deploy | §16.2 |
| 246 | `deploy/k8s/base/deployment.yaml` | Base K8s Deployment: probes, resources, env vars | §16.2 |
| 247 | `deploy/k8s/base/service.yaml` | Base K8s Service: expose API deployment | §16.2 |
| 248 | `deploy/k8s/base/configmap.yaml` | Base K8s ConfigMap: non-secret configuration | §16.2 |
| 249 | `deploy/k8s/base/kustomization.yaml` | Kustomize base: resource list, labels, namespace | §16.2 |
| 250 | `deploy/k8s/overlays/dev/kustomization.yaml` | Dev overlay: single replica, debug settings | §16.2 |
| 251 | `deploy/k8s/overlays/staging/kustomization.yaml` | Staging overlay: production-like, lower scale | §16.2 |
| 252 | `deploy/k8s/overlays/prod/kustomization.yaml` | Prod overlay: full scale, strict settings, PDB | §16.2 |
| 253 | `scripts/README.md` | Scripts index: each script, its Make target, expected behavior | §10 |
| 254 | `scripts/dev.sh` | Start local API with hot reload → `make dev` | §10.2 |
| 255 | `scripts/lint.sh` | Run ruff lint checks → `make lint` | §10.2 |
| 256 | `scripts/fmt.sh` | Apply ruff formatting → `make fmt` | §10.2 |
| 257 | `scripts/typecheck.sh` | Run type checking → `make typecheck` | §10.2 |
| 258 | `scripts/test.sh` | Run tests with coverage (unit/integration/smoke variants) → `make test` | §10.2 |
| 259 | `scripts/migrate.sh` | Apply or create DB migrations → `make migrate` / `make migrate:create` | §10.2 |
| 260 | `scripts/docs-check.sh` | Check documentation links and build → `make docs:check` | §10.2 |
| 261 | `scripts/docs-index.sh` | Regenerate doc indexes → `make docs:index` (recommended) | §10.2 |
| 262 | `scripts/queue-peek.sh` | Read-only queue peek → `make queue:peek` | §10.2 |
| 263 | `scripts/queue-validate.sh` | Validate queue schema and invariants → `make queue:validate` | §10.2 |
| 264 | `scripts/queue-archive.sh` | Scripted queue archive move → `make queue:archive` (recommended) | §10.2 |
| 265 | `scripts/prompt-list.sh` | List prompt templates → `make prompt:list` | §10.2 |
| 266 | `scripts/skills-list.sh` | List skills by category → `make skills:list` | §10.2 |
| 267 | `scripts/rules-check.sh` | Validate rule files → `make rules:check` | §10.2 |
| 268 | `scripts/audit-self.sh` | Repo self-audit → `make audit:self` | §10.2 |
| 269 | `scripts/security-scan.sh` | Security scanning wrapper → `make security:scan` | §10.2 |
| 270 | `scripts/image-build.sh` | Build API container image → `make image:build` | §10.2 |
| 271 | `scripts/image-scan.sh` | Scan container image → `make image:scan` | §10.2 |
| 272 | `scripts/release-prepare.sh` | Prepare release: changelog, staging → `make release:prepare` | §10.2 |
| 273 | `scripts/release-verify.sh` | Pre-tag verification → `make release:verify` | §10.2 |
| 274 | `scripts/k8s-render.sh` | Render K8s manifests → `make k8s:render` | §10.2 |
| 275 | `scripts/k8s-validate.sh` | Validate K8s manifests → `make k8s:validate` | §10.2 |
| 276 | `idea.md` | Project intake form — singular input for repo initialization | §27.2 |
| 277 | `CHANGELOG.md` | Project changelog (Keep a Changelog format) | §28.1 |
| 278 | `prompts/repo_initializer.md` | Master initialization prompt — reads idea.md, scaffolds entire repo | §27.5 |
| 279 | `prompts/domain_modeler.md` | Role: analyze domain model, produce bounded context map and scaffolding plan | §28.2 |
| 280 | `prompts/profile_configurator.md` | Role: enable/disable profiles based on idea.md selections | §28.2 |
| 281 | `docs/procedures/initialize-repo.md` | SOP: initialize repo from idea.md (6-phase procedure) | §27.4 |
| 282 | `docs/procedures/scaffold-domain-module.md` | SOP: scaffold new bounded context module in apps/api/src/ | §28.3 |
| 283 | `docs/procedures/enable-profile.md` | SOP: enable optional profile with dependency checking | §28.3 |
| 284 | `docs/procedures/validate-idea-md.md` | SOP: validate idea.md completeness before initialization | §28.3 |
| 285 | `docs/architecture/system-context.md` | System context: boundary, actors, integrations, data flows | §28.4 |
| 286 | `docs/architecture/domain-model.md` | Domain model: entities, relationships, bounded context map | §28.4 |
| 287 | `docs/architecture/api-design.md` | API design decisions: style, versioning, pagination, rate limiting | §28.4 |
| 288 | `docs/development/environment-vars.md` | Environment variable reference with types, defaults, and profiles | §28.4 |
| 289 | `docs/development/module-patterns.md` | Standard module structure reference for apps/api/src/ | §28.4 |
| 290 | `docs/development/dependency-management.md` | Dependency management: adding, removing, upgrading, lockfile | §28.4 |
| 291 | `docs/operations/configuration.md` | Configuration flow: env vars → Pydantic settings → app code | §28.4 |
| 292 | `docs/operations/health-checks.md` | Health endpoint contracts, probe config, degraded states | §28.4 |
| 293 | `docs/agents/initialization-guide.md` | Guide for the initialization process and idea.md | §28.4 |
| 294 | `docs/queue/queue-categories.md` | Queue category registry with descriptions and validation | §28.4 |
| 295 | `.cursor/rules/initialization.md` | Rules for repo initialization: procedure compliance, validation | §28.5 |
| 296 | `.cursor/rules/skills.md` | Rules for skill files: structure, machinery, cross-references | §28.5 |
| 297 | `.cursor/rules/prompts.md` | Rules for prompt files: metadata, placeholders, validation | §28.5 |
| 298 | `scripts/init-repo.sh` | Initialization pre-checks and guidance → `make init` | §28.6 |
| 299 | `scripts/validate-idea.sh` | Validate idea.md completeness → `make idea:validate` | §28.6 |
| 300 | `scripts/scaffold-module.sh` | Scaffold domain module → `make scaffold:module` | §28.6 |
| 301 | `scripts/profile-enable.sh` | Enable optional profile → `make profile:enable` | §28.6 |
| 302 | `scripts/idea-to-queue.sh` | Extract queue items from idea.md → `make idea:queue` (recommended) | §28.6 |
| 303 | `scripts/generate-env.sh` | Generate .env from .env.example → `make env:generate` | §28.6 |
| 304 | `scripts/inventory-check.sh` | Verify spec-required files exist → `make inventory:check` | §28.6 |
| 305 | `skills/agent-ops/queue-triage.py` | Machinery: queue readiness analyzer and triage report generator | §28.7 |
| 306 | `skills/agent-ops/handoff-template-generator.py` | Machinery: auto-generate handoff docs from git diff and queue state | §28.7 |
| 307 | `skills/agent-ops/repo-self-audit.py` | Machinery: automated spec compliance checker and audit reporter | §28.7 |
| 308 | `skills/repo-governance/rule-linter.py` | Machinery: lint .cursor/rules/ for structure, globs, contradictions | §28.7 |
| 309 | `skills/repo-governance/docs-freshness-checker.py` | Machinery: detect stale docs by comparing git timestamps | §28.7 |
| 310 | `skills/repo-governance/adr-index-generator.py` | Machinery: generate ADR index from ADR files | §28.7 |
| 311 | `skills/backend/module-scaffolder.py` | Machinery: generate FastAPI module from templates (router, models, schemas, service, tests) | §28.7 |
| 312 | `skills/backend/error-code-registry.py` | Machinery: validate error code uniqueness and documentation coverage | §28.7 |
| 313 | `skills/backend/env-var-sync.py` | Machinery: sync .env.example with actual env var usage in code | §28.7 |
| 314 | `skills/backend/openapi-diff.py` | Machinery: detect breaking API changes against baseline (recommended) | §28.7 |
| 315 | `skills/security/secret-scanner.py` | Machinery: scan codebase for potential secrets and high-entropy strings | §28.7 |
| 316 | `skills/security/dependency-audit.py` | Machinery: audit Python deps for CVEs with severity classification | §28.7 |
| 317 | `skills/security/tenant-isolation-checker.py` | Machinery: static analysis for missing tenant filters in queries | §28.7 |
| 318 | `skills/testing/test-scaffolder.py` | Machinery: generate test stubs from router/service analysis | §28.7 |
| 319 | `skills/testing/coverage-ratchet.py` | Machinery: enforce and update coverage floor | §28.7 |
| 320 | `skills/testing/flaky-detector.py` | Machinery: detect flaky tests via repeated runs (recommended) | §28.7 |
| 321 | `skills/devops/dockerfile-linter.py` | Machinery: lint Dockerfiles for best practices | §28.7 |
| 322 | `skills/devops/k8s-manifest-validator.py` | Machinery: validate K8s manifests beyond schema compliance | §28.7 |
| 323 | `skills/devops/compose-profile-matrix.py` | Machinery: test Compose profile combinations (recommended) | §28.7 |
| 324 | `skills/init/README.md` | Initialization skills index | §28.7 |
| 325 | `skills/init/idea-validator.md` | Skill [FULL]: validate idea.md completeness and consistency | §28.7 |
| 326 | `skills/init/idea-validator.py` | Machinery: parse and validate idea.md structure and content | §28.7 |
| 327 | `skills/init/archetype-mapper.md` | Skill [FULL]: map archetype to profiles, modules, and file plan | §28.7 |
| 328 | `skills/init/archetype-mapper.py` | Machinery: archetype-to-profile mapping with JSON plan output | §28.7 |
| 329 | `skills/init/module-template-generator.md` | Skill [FULL]: generate all files for domain module from entities | §28.7 |
| 330 | `skills/init/queue-seeder.md` | Skill: populate queue.csv from idea.md | §28.7 |
| 331 | `skills/init/queue-seeder.py` | Machinery: extract and format queue items from idea.md | §28.7 |
| 332 | `skills/init/profile-resolver.md` | Skill: resolve profile enablement with dependency checking | §28.7 |
| 333 | `skills/init/profile-resolver.py` | Machinery: profile dependency graph resolution | §28.7 |
| 334 | `skills/init/env-generator.md` | Skill: generate .env.example for enabled profiles | §28.7 |
| 335 | `skills/init/env-generator.py` | Machinery: profile-aware env var generation | §28.7 |
| 336 | `.cursor/commands/initialize.md` | Command: run full repo initialization flow | §28.9 |
| 337 | `.cursor/commands/scaffold-module.md` | Command: scaffold new domain module | §28.9 |
| 338 | `.cursor/commands/audit.md` | Command: run comprehensive repo self-audit | §28.9 |

---

## 32. Document control (updated)

| Item | Value |
|------|--------|
| **Canonical spec file** | `spec.md` |
| **Version** | 3.0 |
| **Owners** | Repository maintainers |
| **Change process** | PR with rationale; bump version header when breaking; ADR if architectural |
| **Total enumerated files** | 338 |
| **Total enumerated folders** | 60 |

---

*End of specification.*
