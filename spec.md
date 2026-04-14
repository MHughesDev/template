# Template Repository Specification — Agent-Operated Machine

**Version:** 2.0  
**Stack:** Python 3.12+, FastAPI, optional React/Expo front-ends  
**Primary operators:** Coding agents (Cursor and compatible tooling). Humans are **reviewers, supervisors, and policy maintainers**, not the default execution path.

This document is the **authoritative specification** for a batteries-included template repository designed as a **Cursor-first, agentic-coding-centric repository machine**: a software factory where subsystems have explicit **purpose, inputs, outputs, invariants, commands, failure modes, tests, related prompts, and handoff rules**.

Implementers treat this spec as a **checklist and process contract**. Ambiguity and tribal knowledge are **failure modes**; recurring work must become **documented, reusable machine procedures** (prompts, skills, rules, commands, checklists, tests).

**Canonical spec file:** `spec.md` (this file).  
**Supersedes:** prior `downloadable.md` content for template definition; see `downloadable.md` for redirect note.

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
├── spec.md                     # This specification
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
2. **Instruction hierarchy** — short pointer to this spec’s precedence table; link to `spec.md`.  
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
- [ ] **`spec.md`** present (this document).  
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

*End of specification.*
