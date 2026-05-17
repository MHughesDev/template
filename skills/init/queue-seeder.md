# skills/init/queue-seeder.md

**Purpose:** Populate `queue/queue.csv` from initialized project documentation, using `idea.md` section 12 only as optional prioritization hints. Queue rows must be derived from the architecture/API/ops docs produced during initialization.

## When to Invoke

- During initialization after `skills/init/initialize-repo.md` has completed.
- Before final initialization handoff.

## Source of truth

1. Primary: initialized docs under `docs/` (architecture, api, operations, testing, security).
2. Secondary hints: `idea.md` §12 (priority hints) and §16 (open questions).

## Prerequisites

- Initialization docs are complete and marked `status: current` where applicable.
- `queue/queue.csv` exists with valid header.

## Step-by-Step Method

1. Read initialized docs and extract implementation workstreams into queue-sized items.
2. Use `idea.md` §12 only to refine priority/order; do not require it.
3. Create blocked items for unresolved `idea.md` §16 questions when they block execution.
4. Ensure each row has clear `goal` + `acceptance_criteria` and executor-ready scope.
5. Run `make queue:validate`.

## Command Examples

- `make queue:validate`
- `make queue:top-item`

## Validation Checklist

- [ ] Queue items are derivable from initialized docs even if `idea.md` §12 is empty.
- [ ] Every row has concrete acceptance criteria.
- [ ] Blocked rows exist for true blockers from open questions.
- [ ] `make queue:validate` passes.

## Common Failure Modes

- Treating §12 as required input.
- Writing vague summaries without acceptance criteria.
- Missing blocked rows for known unresolved questions.

## Handoff Expectations

- Queue seeded and validated.
- First executable item is ready for claim.
