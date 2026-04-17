# AGENTS.md

Root agent control plane. This is the default policy surface for all agents operating in this repository. It defines mission, instruction hierarchy, required workflows, validation, queue interaction, escalation, and anti-patterns. **Read [README.md](README.md) first for repository orientation, then read this file (`AGENTS.md`) completely before any other policy or code.** Per [spec/spec.md](spec/spec.md) section 4 — sections 1–14 below are all required.

**Standing requirement:** Consult **`AGENTS.md` again** whenever the instruction hierarchy is unclear, a task touches policy (branch/PR, queue, security, docs), or you are about to **merge** or **hand off** — do not rely on memory from an earlier read.

**Authoritative specification:** [spec/spec.md](spec/spec.md) (canonical full specification).

---

## 1. Repository mission and operating philosophy

Primary operators are **coding agents** (Cursor and compatible tooling). Humans are **reviewers, supervisors, and policy maintainers** — not the default execution path.

This repository is a **software factory**: an operating system for agents where every recurring workflow is a documented, reusable machine procedure (prompts, skills, rules, commands, procedures, tests).

**Evidence-first:** every meaningful change must leave a trace — commands run and results captured, documentation updated when behavior changes, queue state updated when doing queue work, and handoffs that list files changed and risks.

**Core stack:** Python 3.12+, FastAPI modular monolith, optional React/Expo client profiles. **Ambiguity and tribal knowledge are failure modes**; prefer explicit procedures and canonical commands.

---

## 2. Instruction hierarchy

When instructions conflict, resolve in this order (higher overrides lower):

1. Explicit task prompt (current run)
2. Root **AGENTS.md** (this file)
3. Scoped **AGENTS.md** files (e.g. `apps/api/AGENTS.md`)
4. **`.cursor/rules/`**
5. **`docs/procedures/`**
6. **`skills/`**
7. **`prompts/`**
8. General documentation under **`docs/`**

**Link to authoritative source:** [spec/spec.md](spec/spec.md) (canonical full specification).

**Conflict handling:** if two sources at the **same** rank disagree, **stop and escalate** — do not guess. Document the conflict in a PR or queue notes.

---

## 3. Required workflow for agents

For **every** task, follow this sequence:

1. Read **[README.md](README.md)** (repository map, quickstart, key resources — required for every agent session).
2. Read this **[AGENTS.md](AGENTS.md)** completely (the authoritative agent contract).
3. Read the task description or queue item.
4. If the task is queue work, read **`queue/QUEUE_INSTRUCTIONS.md`**.
5. **Mandatory — search `skills/` for relevant skills:** run `make skills:list` or read **`skills/README.md`**; scan titles and every **When to invoke** section; read every relevant skill in full **before** planning or writing code.
6. Read relevant **`docs/procedures/`** for the task type.
7. Read relevant source files and tests.
8. **Plan** — files to touch, acceptance criteria, scope bounds, risks.
9. **Implement** in small validated increments.
10. **Validate** — `make lint`, `make fmt`, `make typecheck`, `make test`; if queue files changed, `make queue:validate`.
11. **Update documentation** if behavior or operational assumptions changed.
12. **Update queue state** when finishing queue items (per `queue/QUEUE_INSTRUCTIONS.md`).
13. **Hand off** — commands run with key output, files changed, PR link, risks, follow-ups.

The mandatory skill search in step 5 is **non-negotiable** for every invocation (queue item, prompt template, Cursor command, manual instruction, or any other trigger).

---

## 4. Branch and PR policy

**Branch naming:**

| Pattern | Use |
|--------|-----|
| `queue/<id>-short-slug` | Queue-driven work; **must** include the queue item ID |
| `cursor/<descriptive-slug>-<4-char-suffix>` | Agent/Cursor work not tied to a queue row |

**Pull requests:**

- Prefer **one logical change** per PR.
- All required **CI checks must pass** before merge.
- Queue-driven PR **titles** should reference the queue ID when applicable.
- PR **descriptions** should follow **`.github/PULL_REQUEST_TEMPLATE.md`**.
- Include **evidence**: commands run (with key output), files changed, risks.

**After merge:** Delete the **feature branch** on the remote (and locally) so the next run starts from a fresh branch off `main`. Do not accumulate long-lived agent branches.

**Branch protection:** `main` is protected — no direct push; changes land via PR and review.

---

## 5. Planning before coding

Before writing code, produce a plan (in the PR description or queue notes) that includes:

- **Acceptance criteria** — restated exactly from the queue summary or task prompt (not vague paraphrase).
- **Files** — exhaustive list of files to create or modify.
- **Risks** — security, tenancy, data integrity, API contract, migration safety.
- **Scope bounds** — what this change explicitly does **not** do.
- **Definition of done** — e.g. tests passing, docs updated, queue row archived when applicable.

Do not start implementation until the plan is written down.

---

## 6. Scope control

- Change only files in scope for the current task.
- Out-of-scope issues: **stop**, open a new queue row or GitHub issue, note in the PR — **do not fix silently**.
- Do not bundle unrelated bug fixes without explicit approval.
- Do not expand acceptance criteria without updating the queue row and getting review on that scope.

Silent scope creep is a bug in agent behavior. If the same class of mistake repeats, encode a **rule** or **procedure** to prevent it (see section 10).

---

## 7. Validation before handoff

Minimum checks before opening a PR:

| Command | Purpose |
|---------|---------|
| `make lint` | Ruff lint |
| `make fmt` | Apply Ruff formatting |
| `make fmt-check` | Ruff format verify (CI mode) |
| `make typecheck` | mypy strict |
| `make test` | Full test suite with coverage |
| `make queue:validate` | If any queue CSV or queue docs were touched |
| `make docs:check` | If documentation content changed |
| `make security:scan` | Auth, tenancy, secrets, or security-sensitive changes |

**When to add tests:** any behavior change, new endpoint, bug fix (regression test first), new module.

**When to update docs:** new or removed env var, new/changed endpoint, behavior change, deployment or ops procedure change.

---

## 8. Documentation update requirements

Update docs alongside code when:

- **`.env.example`** and **`docs/development/environment-vars.md`** — any env var added or removed.
- **`docs/api/endpoints.md`** — any API route added, removed, or changed.
- **`docs/api/error-codes.md`** — any error code added or changed.
- **`docs/operations/`** — deployment, Docker, or Kubernetes behavior changes.
- **`docs/procedures/`** — procedure steps or commands change.
- **`CHANGELOG.md`** — every meaningful user-visible or operator-visible change; required before release.
- **`docs/adr/`** — significant architectural decisions.

**Docs are not optional. Undocumented behavior is an agent failure.**

---

## 9. Queue interaction rules

Canonical reference: **`queue/QUEUE_INSTRUCTIONS.md`**.

Summary:

- The **top data row** of `queue/queue.csv` is the **active** work item for single-lane processing.
- Read the **entire** top row — the summary is the contract and must be actionable without guesswork.
- **Never delete** a queue row without archiving per procedure.
- **Blocked** items stay in `queue.csv` with clear notes.
- **Done** items move to **`queue/queuearchive.csv`** with status, completion metadata, and PR URL in notes as required.
- Run **`make queue:validate`** after any queue file change.
- Use **`make queue:peek`** for a safe read-only view of the current item.
- If two writers collide: stop, re-validate, reconcile using **`main`** as the integration truth.

---

## 10. When to create or update skills, rules, prompts, procedures

**Rule:** If the same class of work or mistake appears twice, **encode it** — do not rely on memory or one-off reminders.

| Trigger | Action |
|---------|--------|
| Repeated mistake | Update or add **`.cursor/rules/`** — see **`docs/procedures/update-or-create-rule.md`** |
| New recurring workflow | Create or update **`skills/`** — see **`docs/procedures/update-or-create-skill.md`** |
| Successful one-off prompt | Promote to **`prompts/`** — see **`skills/agent-ops/prompt-to-procedure-promotion.md`** |
| New canonical workflow | Add **`docs/procedures/`** |
| New `make` target | Document in **Makefile**, **README**, **`docs/development/local-setup.md`** |

See also **`skills/agent-ops/rule-refinement-after-mistakes.md`**.

---

## 11. Escalation of uncertainty

**Stop and escalate** (do not guess) when:

- Security or tenancy semantics are unclear.
- A change could affect data integrity.
- Spec and code disagree and it is unclear which wins.
- Two instructions at the same rank conflict.
- A required credential or external service is unavailable.

Document in the PR or queue notes: what is unclear, options, what information is needed, and a recommendation if any.

**Guessing on security, tenancy, or data integrity is forbidden. Document and wait.**

---

## 12. Anti-patterns and forbidden behaviors

- Never commit secrets, credentials, API keys, or tokens.
- Never bypass CI (`--no-verify`), force-push to `main`, or push directly to `main`.
- Never delete queue rows without archiving per lifecycle rules.
- Never silently expand scope.
- Never run ad hoc shell when a canonical **`make`** target exists.
- Never use **`os.getenv()`** outside **`apps/api/src/config.py`** (single Settings object).
- Never add **`# type: ignore`** without an explanatory comment.
- Never swallow exceptions (`except Exception: pass`).
- Never query the database directly in a router handler.
- Never hardcode tenant IDs, user IDs, or environment-specific values in code.
- Never skip the mandatory **skill search** before execution.
- Never fix unrelated bugs in the same PR without approval.

---

## 13. Mandatory skill search before execution

Per spec §4.1 item 13 — required for **every** task:

1. Identify the task domain (e.g. FastAPI endpoint, queue CSV edit, security review).
2. Run **`make skills:list`** or read **`skills/README.md`** for the skill index.
3. Scan **When to invoke** for skills in relevant categories.
4. Read every relevant skill **in full** before planning or coding.
5. Note **machinery** (`.py` files next to skills) as optional automation.
6. For unfamiliar domains, use **`prompts/skill_searcher.md`** as a subroutine.

This step applies whether the task arrives via queue, prompt, command, or chat. **An agent that skips this step is operating out of policy.**

---

## 14. Prompt preamble and skill-search reference

Every prompt template used by agents must include or reference a short preamble that:

- Points to the mandatory skill search (section 13 / spec §4.1 item 13).
- References **`prompts/skill_searcher.md`** for task-to-skill matching.
- Reminds agents to read **AGENTS.md** before execution.

Prompt authors follow **`docs/procedures/add-prompt-template.md`**.

---

## 15. Python implementation procedures

All Python code in this repository MUST follow **[PYTHON_PROCEDURES.md](PYTHON_PROCEDURES.md)** — the 18 implementation procedures that govern type safety, boundary definitions, import direction, error handling, configuration, async patterns, and testing.

Key rules enforced:

- Every public function is fully typed (params, return, errors).
- Boundary shapes (requests, responses, config) defined as Pydantic models before logic.
- Import direction: `router` → `service` → `repository`. Never reverse.
- No `os.getenv()` outside `apps/api/src/config.py`.
- State modeled with `Enum` and explicit transition maps where applicable.
- `None` handled explicitly; never used as an error signal.

See the full document for all 18 procedures, the condensed 12-point rule set, and refactor triggers. Code review (procedure 18) checks compliance with all of these.

---

## Navigation and machine interface

### Directory navigation

| Area | Location |
|------|----------|
| API source | `apps/api/src/` — contexts include `health/`, `auth/`, `tenancy/` |
| Shared contracts | `packages/contracts/` |
| Task interfaces | `packages/tasks/` |
| AI/RAG (optional) | `packages/ai/` |
| Deploy | `deploy/docker/`, `deploy/k8s/` (base + overlays) |
| Documentation | `docs/` — start with **`docs/README.md`** |
| Skills | `skills/` — **`skills/README.md`** |
| Prompts | `prompts/` — **`prompts/README.md`** |
| Queue (open / archive) | `queue/queue.csv`, `queue/queuearchive.csv` |
| Scripts (Make backends) | `scripts/` |
| Machine control | `.cursor/rules/`, `.cursor/commands/` |

### Canonical commands

Prefer **`make`** targets over ad hoc commands. See the **Makefile** for the full catalog. Frequently used:

`make dev`, `make lint`, `make fmt`, `make typecheck`, `make test`, `make migrate`, `make queue:peek`, `make queue:validate`, `make audit:self`, `make skills:list`, `make prompt:list`

**Validation:** `make audit:self` runs a comprehensive check — use before merging substantial work.

**Queue:** `make queue:peek` (read-only), `make queue:validate`, **`make queue:archive-top`** (archive first open row — no id), `make queue:archive` where implemented.

### Handoff format

Include: files changed, commands run with key output, PR link, residual risks, follow-up issues or queue items.

### After any meaningful change

Ask: did I update docs? Add tests? Should this pattern become a **skill** or **rule**?
