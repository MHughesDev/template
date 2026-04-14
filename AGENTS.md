# AGENTS.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Canonical spec: spec/spec.md §4 -->
<!-- - Scoped agents: apps/api/AGENTS.md, packages/contracts/AGENTS.md, packages/tasks/AGENTS.md -->
<!-- - Queue SOP: queue/QUEUE_INSTRUCTIONS.md -->
<!-- - Procedures: docs/procedures/ -->

> PURPOSE: Root agent control plane. This is the default policy surface for all agents operating in this repository. Defines mission, instruction hierarchy, required workflows, validation, queue interaction, escalation, and anti-patterns. All agents read this file before any other. Per spec §4 — required sections 1–14 must all be present.

---

## 1. Repository Mission and Operating Philosophy

> CONTENT: Agent-primary mission statement. State that primary operators are coding agents (Cursor and compatible tooling); humans are reviewers, supervisors, and policy maintainers. The repository is a software factory — an "operating system for agents" where every recurring workflow is a documented, reusable machine procedure. Emphasize evidence-first behavior: every meaningful change must leave a trace (commands run, results captured, docs updated, queue state updated). Ref spec §1.1 and §1.4. State the core stack: Python 3.12+, FastAPI, optional React/Expo. State that ambiguity and tribal knowledge are failure modes.

## 2. Instruction Hierarchy

> CONTENT: Short summary of the precedence table from spec §0 (Instruction hierarchy section). List all 8 levels in order: (1) Explicit task prompt, (2) Root AGENTS.md (this file), (3) Scoped AGENTS.md files, (4) .cursor/rules/, (5) docs/procedures/, (6) skills/, (7) prompts/, (8) General docs/. State: "Link to authoritative source: spec/spec.md (canonical full specification)." State conflict handling rule: two sources at same rank → stop and escalate; do not guess.

## 3. Required Workflow for Agents

> CONTENT: Step-by-step required read order and action sequence that every agent MUST follow for any task. Steps:
> 1. Read this AGENTS.md completely
> 2. Read the task/queue item
> 3. Read queue/QUEUE_INSTRUCTIONS.md if this is queue work
> 4. **MANDATORY: Search skills/ for relevant skills** (run `make skills:list` or read skills/README.md; scan all "When to invoke" sections; read every relevant skill in full before planning or writing code)
> 5. Read relevant docs/procedures/ for the task type
> 6. Read relevant source files and tests
> 7. Plan — list files to touch, acceptance criteria, scope bounds, risks
> 8. Implement in small validated increments
> 9. Validate (make lint, make typecheck, make test, make queue:validate if queue work)
> 10. Update documentation if behavior/ops changed
> 11. Update queue state
> 12. Handoff — commands run with output, files changed, PR link, risks, follow-ups
>
> State explicitly: "The mandatory skill search in step 4 is non-negotiable for every invocation regardless of trigger type."

## 4. Branch and PR Policy

> CONTENT: Branch naming conventions — two patterns:
> - Queue-driven work: `queue/<id>-short-slug` (must include the queue item ID)
> - Agent/Cursor work: `cursor/<descriptive-slug>-<4-char-suffix>`
>
> PR requirements:
> - One logical change per PR where possible
> - All required CI checks must be green before merge
> - PR title must reference queue ID if queue-driven
> - PR description must use the .github/PULL_REQUEST_TEMPLATE.md format
> - Evidence required: commands run with output, files changed, risks
>
> Branch protection: main is protected; no direct push; require PR review.

## 5. Planning Before Coding

> CONTENT: Requirements for planning before writing any code. Must produce a plan that states:
> - Exact acceptance criteria (from queue summary or task prompt) — restated, not paraphrased
> - Exhaustive list of files that will be created or modified
> - Named risks: security, tenancy, data integrity, API contract, migration safety
> - Explicit scope bounds: what this change does NOT do
> - Definition of done: what "complete" looks like (passing tests, updated docs, queue archived)
>
> Plan goes in PR description or queue notes. Agents must not start implementation until plan is documented.

## 6. Scope Control

> CONTENT: Rules to prevent scope creep. Agents must:
> - Only change files directly in scope of the current task
> - When discovering out-of-scope issues: stop, create a new queue row or GitHub issue, document in PR notes, do NOT fix silently
> - Never "fix unrelated bugs while I'm here" without explicit approval
> - Never expand accepted criteria without updating the queue row and getting implicit approval via PR
>
> State: "Silent scope creep is a bug in agent behavior. If it appears twice, encode a rule to prevent it."

## 7. Validation Before Handoff

> CONTENT: Minimum validation commands that MUST pass before any PR is opened. List:
> - `make lint` — ruff lint
> - `make fmt` — format check (CI mode, not auto-fix)
> - `make typecheck` — mypy --strict
> - `make test` — full test suite with coverage
> - `make queue:validate` — if any queue files were touched
> - `make docs:check` — if any docs were updated
> - `make security:scan` — for any auth, tenancy, or security-adjacent changes
>
> State when to add tests: any behavior change, any new endpoint, any bug fix (regression first), any new module.
> State documentation update triggers: new env var, new endpoint, behavior change, ops procedure change.

## 8. Documentation Update Requirements

> CONTENT: Specific triggers that require documentation updates alongside code changes. Must update:
> - `.env.example` + `docs/development/environment-vars.md` → when adding/removing any env var
> - `docs/api/endpoints.md` → when adding/removing/changing any API endpoint
> - `docs/api/error-codes.md` → when adding/changing any error code
> - `docs/operations/` relevant file → when changing deployment, Docker, K8s configuration
> - `docs/procedures/` relevant file → when a procedure's commands or steps change
> - `CHANGELOG.md` → for every meaningful change; required before release
> - `docs/adr/` → for architectural decisions
>
> State: "Docs are not optional. Undocumented behavior is an agent failure."

## 9. Queue Interaction Rules

> CONTENT: Pointer to queue/QUEUE_INSTRUCTIONS.md as the canonical reference. Summary of key rules:
> - Top data row of queue.csv = the active work item for single-lane processing
> - Read the ENTIRE top row — summary is the contract; it must be rich enough to act without guesswork
> - Never delete a queue row without archiving first
> - Blocked items stay in queue.csv with notes explaining the blocker
> - Done items move to queuearchive.csv with status=done, completed_date, PR URL in notes
> - Run `make queue:validate` after any queue modification
> - Use `make queue:peek` to read the current top item safely
> - Conflict resolution: if two writers collide, stop, re-run validate, merge using main as truth

## 10. When to Create or Update Skills, Rules, Prompts, Procedures

> CONTENT: Decision rules for when to encode learning. State: "If the same class of work or mistake appears twice, encode it — do not rely on memory or repeat instructions."
>
> Triggers:
> - Repeated mistake → update or create `.cursor/rules/` entry (procedure: docs/procedures/update-or-create-rule.md)
> - New recurring work pattern → create or update `skills/` entry (procedure: docs/procedures/update-or-create-skill.md)
> - Successful one-off prompt → promote to `prompts/` with metadata (skill: skills/agent-ops/prompt-to-procedure-promotion.md)
> - New canonical workflow → create `docs/procedures/` entry
> - New Make target → document in Makefile + README + local-setup.md
>
> Link to: skills/agent-ops/rule-refinement-after-mistakes.md

## 11. Escalation of Uncertainty

> CONTENT: Protocol for when an agent is uncertain. Escalation triggers:
> - Security or tenancy semantics are ambiguous
> - A change could affect data integrity
> - Spec and implementation disagree and it's unclear which is correct
> - Two instructions at the same rank conflict
> - A required credential or external service is unavailable
>
> Escalation action: STOP. Do not guess. Document the uncertainty in PR description or queue notes with:
> - What is unclear
> - What options exist
> - What information is needed to resolve
> - Recommendation if any
>
> State: "Guessing on security, tenancy, or data integrity is forbidden. Document and wait."

## 12. Anti-Patterns and Forbidden Behaviors

> CONTENT: Explicit list of behaviors that are NEVER acceptable. Format as a checklist of prohibitions:
> - NEVER commit secrets, credentials, API keys, or tokens to the repository
> - NEVER bypass CI (no --no-verify, no force push to main, no direct push to main)
> - NEVER delete queue rows without archiving
> - NEVER silently expand scope
> - NEVER run ad hoc shell commands when a canonical `make` target exists
> - NEVER use `os.getenv()` outside config.py
> - NEVER add `# type: ignore` without an explanatory comment
> - NEVER catch and swallow exceptions silently (`except Exception: pass`)
> - NEVER query the database directly in a router handler
> - NEVER hardcode tenant IDs, user IDs, or environment-specific values
> - NEVER skip the mandatory skill search before beginning work
> - NEVER fix unrelated bugs in the same PR without approval

## 13. Mandatory Skill Search Before Execution

> CONTENT: The mandatory skill search procedure in full detail, per spec §4.1 item 13.
>
> Required procedure for EVERY task (non-negotiable):
> 1. Identify the task domain (e.g., "adding a FastAPI endpoint", "modifying queue CSV", "security review")
> 2. Run `make skills:list` OR read `skills/README.md` to see all skills by category
> 3. Scan the title and "When to invoke" section of each skill in the relevant category
> 4. Read every relevant skill in full before planning or writing any code
> 5. Note associated machinery files (`.py` files alongside the skill `.md`) as available automated tools
> 6. For unfamiliar domains, also check `prompts/skill_searcher.md` for subroutine search guidance
>
> State: "This step is mandatory regardless of whether the task arrives via queue item, prompt template, Cursor command, manual instruction, or any other trigger. An agent that skips this step is operating out of policy."

## 14. Prompt Preamble and Skill-Search Reference

> CONTENT: Every prompt template body used by agents MUST include or reference a standard preamble that:
> - Points agents to the mandatory skill search (§4.1 item 13 / section 13 above)
> - References `prompts/skill_searcher.md` as the subroutine for task-to-skill matching
> - Reminds agents to read this AGENTS.md before execution
>
> State that prompt authors are responsible for including this preamble in new prompt templates. Reference `docs/procedures/add-prompt-template.md` for the procedure.

---

## Navigation and Machine Interface

> CONTENT: Per spec §4.2 — guide agents on navigating and operating the repository. Cover:
>
> **Directory navigation:**
> - API source code: `apps/api/src/` (bounded by context: health/, auth/, tenancy/, and future contexts)
> - Shared packages: `packages/contracts/` (shared Pydantic models), `packages/tasks/` (task interfaces), `packages/ai/` (AI/RAG, optional)
> - Deployment: `deploy/docker/`, `deploy/k8s/` (base + overlays)
> - Documentation hub: `docs/` (see docs/README.md for structure)
> - Skills library: `skills/` (see skills/README.md for index)
> - Prompt templates: `prompts/` (see prompts/README.md)
> - Queue: `queue/queue.csv` (open), `queue/queuearchive.csv` (archive)
> - Scripts: `scripts/` (implementations backing Makefile targets)
> - Machine control: `.cursor/rules/` (constraints), `.cursor/commands/` (reusable commands)
>
> **Canonical commands (prefer these over ad hoc shell):**
> - See Makefile for full target list
> - Key targets: `make dev`, `make lint`, `make fmt`, `make typecheck`, `make test`, `make migrate`, `make queue:peek`, `make queue:validate`, `make audit:self`, `make skills:list`, `make prompt:list`
>
> **Validation workflow:** `make audit:self` runs the comprehensive check. Use it before any PR.
>
> **Queue operations:** `make queue:peek` (read-only), `make queue:validate` (schema check), `make queue:archive` (scripted move)
>
> **Handoff format:** Files changed (list), commands run with key output (paste), PR link, residual risks, follow-up queue items or issues.
>
> **Docs/tests/skills update check:** After any meaningful change, ask: "Did I update docs? Did I add tests? Does this work pattern deserve a skill or rule?"
