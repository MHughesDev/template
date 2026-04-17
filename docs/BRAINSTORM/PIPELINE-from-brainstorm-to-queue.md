# Pipeline: brainstorm → queue → code → spec/docs

**Purpose:** Reusable steps to move from a **finished** brainstorm (ready for implementation) to **queue rows**, then **implementation**, then **documentation/spec alignment**. Use this for any brainstorm; only the content of the brainstorm changes.

**Ordering rule (required):** **Implement and land code first** (per queue items and PRs). **After** behavior is merged, **update `spec/spec.md` and other docs** so they describe what the repo actually does. Do **not** edit `spec/spec.md` (or authoritative specs) *before* writing code for this feature unless you are documenting behavior that already exists.

---

## Step 0 — Gate: only “ready” brainstorms enter the pipeline

**Input:** A brainstorm file under `docs/BRAINSTORM/ideas/` using [`TEMPLATE-brainstorm.md`](TEMPLATE-brainstorm.md).

**Exit criteria:**

- **Status** in the brainstorm metadata is **`ready for implementation`** (or equivalent).
- **Section 6 (Acceptance criteria)** is concrete enough to derive testable checks.
- **Section 7 (Risks)** has no unresolved **blockers** for your environment (or blockers are documented and accepted).

If not ready, keep editing the brainstorm file or split into smaller brainstorms.

---

## Step 1 — Freeze the implementation contract

**Goal:** Turn the brainstorm into a **stable contract** for queue rows.

**Actions:**

1. Copy the brainstorm **Id**, **Goal**, **Acceptance criteria**, and **Non-goals** into a short planning note (PR draft, ticket, or the brainstorm’s section 10).
2. List **bounded contexts** or modules likely touched (`apps/api/...`, `packages/...`, etc.).
3. List **external dependencies** (new services, flags, migrations) explicitly.
4. Decide **one** primary **outcome** for the first mergeable slice (vertical slice if the idea is large).

**Output:** A bullet list: *what must be true when we are done* (no code yet).

---

## Step 2 — Decompose into queue items

**Goal:** Map the contract to **one or more** `queue/queue.csv` rows.

**Rules:**

- Each queue row must follow [`queue/QUEUE_INSTRUCTIONS.md`](../../queue/QUEUE_INSTRUCTIONS.md): valid **category**, **summary ≥ 100 characters**, clear **dependencies**.
- Prefer **small** items that each end in a mergeable PR over one vague mega-row.
- Order matters: **dependencies** column references other queue **ids** that must be **archived as done** first.

**Typical split (reuse as needed):**

| Queue item (example pattern) | What it usually contains |
|-------------------------------|---------------------------|
| **Design / spike** (optional) | Time-boxed exploration only if unknowns remain; still must end with written decisions in the brainstorm or an ADR |
| **Core implementation** | Code + tests that satisfy acceptance criteria |
| **Migrations / data** | Separate row if risky or needs review |
| **Docs / spec alignment** | **After** core implementation — see Step 6 |
| **Follow-up / hardening** | Performance, observability, cleanup |

**Output:** A table of proposed `id`, `summary` (draft), `dependencies`, `related_files` (must include the brainstorm path and key code paths).

---

## Step 3 — Validate and insert queue rows

**Actions:**

1. Run `make queue:validate` (after editing CSV per [`queue/QUEUE_INSTRUCTIONS.md`](../../queue/QUEUE_INSTRUCTIONS.md)).
2. Ensure **related_files** includes: `docs/BRAINSTORM/ideas/<your-file>.md` and the relevant spec/code paths.
3. Set **batch** / **phase** if you use release trains.

**Output:** Valid `queue/queue.csv` with new rows ready to be processed top-down.

---

## Step 4 — Execute each queue item (implementation lane)

For each item in dependency order:

1. Follow [`docs/procedures/start-queue-item.md`](../procedures/start-queue-item.md): branch `queue/<id>-slug`, read skills, read `related_files`.
2. Implement **code and tests** to satisfy the **summary** contract.
3. Open PR; get review; merge per repo policy.
4. Archive the queue row per [`queue/QUEUE_INSTRUCTIONS.md`](../../queue/QUEUE_INSTRUCTIONS.md).

**Do not** use this step to rewrite `spec/spec.md` to “pretend” the feature exists before it is merged.

---

## Step 5 — Mark brainstorm “in progress” / link tracking

**Actions:**

1. In the brainstorm file, set **Status** to **`in progress`** when the first queue item is claimed.
2. Fill **Section 10 — Implementation tracking** with queue IDs and PR links as they complete.

---

## Step 6 — Spec and documentation alignment (after code is in place)

**Goal:** Make **specs and docs** match **merged** behavior.

**When:** After the **core implementation** queue item(s) are **done** and merged (or after each slice if you split releases).

**Actions (typical order):**

1. Update **`spec/spec.md`** only to reflect **actual** behavior and contracts (not aspirational text).
2. Update other affected docs per [`docs/procedures/update-documentation.md`](../procedures/update-documentation.md) and repo rules (e.g. `docs/api/endpoints.md`, `CHANGELOG.md` if applicable).
3. Run `make docs:check` (and any doc-generation targets your change requires).

**Optional:** Add or update an **ADR** under `docs/adr/` if the brainstorm implied a durable architectural decision.

**Output:** Docs/spec match the repo; reviewers can see doc-only PRs or commits clearly separated from code PRs if you prefer.

---

## Step 7 — Close the loop on the brainstorm

**Actions:**

1. Set brainstorm **Status** to **`implemented`** (or **`superseded`** if replaced).
2. Final line in **Section 11 — Changelog** with completion date and pointer to last PR.
3. If the idea spawned future work, open **new** brainstorm files or queue rows; do not stretch one file forever without structure.

---

## Quick reference — agent checklist

- [ ] Brainstorm status = ready; acceptance criteria are testable
- [ ] Queue rows added with categories, long summaries, dependencies, `related_files` including brainstorm path
- [ ] `make queue:validate` passes
- [ ] Code + tests merged per queue order
- [ ] **Then** `spec/spec.md` and other docs updated
- [ ] Brainstorm tracking table and status updated

---

## Relationship to root policy

Root [`AGENTS.md`](../../AGENTS.md) still governs branches, PRs, validation commands, and escalation. This pipeline **does not** bypass the queue or merge requirements.
