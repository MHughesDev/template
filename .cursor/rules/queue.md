---
globs:
  - "queue/**"
description: Queue file invariants. Lifecycle rules, schema enforcement, no row deletion without archive.
---

# .cursor/rules/queue.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §9 (Queue Interaction Rules) -->
<!-- - Procedures: docs/procedures/archive-queue-item.md, docs/procedures/handle-blocked-work.md -->
<!-- - Validation: scripts/queue-validate.sh, make queue:validate -->

> PURPOSE: Queue CSV file invariants. Enforces lifecycle state transitions, schema column requirements, archive-before-delete policy, summary quality requirements, and branch naming with queue ID. Per spec §26.2 item 14.

## Section: Column Schema Rules

> CONTENT: Rules for the CSV column schema. Rules:
> 1. `queue/queue.csv` MUST have these columns as the header row (in order): `id,batch,phase,category,summary,dependencies,notes,created_date`
> 2. `queue/queuearchive.csv` MUST have the same columns PLUS: `status,completed_date`
> 3. `id` column: unique string ID per row; format: sequential number or descriptive slug (e.g., `Q-001` or `init-001`)
> 4. `category` column: MUST be one of the valid categories defined in `docs/queue/queue-categories.md`
> 5. `summary` column: MUST be ≥100 characters containing goal, acceptance criteria, and definition of done
> 6. `dependencies` column: comma-separated list of queue IDs that must be `done` before this item can start (or empty)
> 7. `notes` column: updated with blocker info (blocked items) or PR URL + completion notes (done items)

## Section: Lifecycle State Transition Rules

> CONTENT: Rules for queue item lifecycle. Rules:
> 1. Items start in `queue/queue.csv` (Open state)
> 2. Active (In Progress): documented by creating a branch with the queue ID; optionally add `status=in_progress` in `notes` column
> 3. Blocked: item STAYS in `queue/queue.csv`; `notes` column MUST explain: blocker description, owner, next step, and expected resolution
> 4. Done: item is MOVED (not deleted) to `queue/queuearchive.csv`; add `status=done`, `completed_date=YYYY-MM-DD`, PR URL in `notes`
> 5. Cancelled: MOVE to archive with `status=cancelled` and reason in `notes`
> 6. Superseded: MOVE to archive with `status=superseded` and ID of the superseding item in `notes`
> 7. NEVER delete a row from `queue/queue.csv` without creating an archive row first

## Section: Archive-Before-Delete Policy

> CONTENT: Rules specifically about deletion prohibition. Rules:
> 1. The `queue/queue.csv` file is append-managed; rows are only REMOVED when MOVED to archive
> 2. `queue/queuearchive.csv` is APPEND-ONLY — never edit or delete existing rows
> 3. Moving a row means: copy the entire row to archive with status fields → then remove from queue.csv
> 4. Use `make queue:archive` or `scripts/queue-archive.sh` for scripted moves to prevent manual errors
> 5. If an item was created by mistake: use `status=cancelled` with reason, then move to archive

## Section: Summary Quality Requirements

> CONTENT: Rules for the summary column content. Rules:
> 1. Summary MUST be ≥100 characters (enforced by `make queue:validate`)
> 2. Summary MUST include: goal (what to accomplish), acceptance criteria (how to verify done), definition of done
> 3. Summary SHOULD include: out-of-scope items, dependencies, expected file impact
> 4. Summary MUST NOT be: a one-liner, a vague verb-noun ("implement feature"), or a copy of the title
> 5. Agents treat the summary as the contract — if it's ambiguous, block and document rather than guess

## Section: Branch Naming with Queue ID

> CONTENT: Rules for branch names for queue-driven work. Rules:
> 1. Branch name for queue work MUST include the queue item ID: `queue/<id>-short-slug`
> 2. Example: if queue ID is `Q-012`, branch is `queue/Q-012-add-invoice-endpoint`
> 3. The slug should be 3-5 words, kebab-case, describing the work
> 4. PR title MUST include the queue ID: `[Q-012] Add invoice endpoint`
> 5. PR body MUST include a link or reference to the queue row being processed
> 6. Agents MUST NOT start a branch without the queue ID in the name for queue-driven work
