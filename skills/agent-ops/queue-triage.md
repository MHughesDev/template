# skills/agent-ops/queue-triage.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/agent-ops/queue-triage.py -->
<!-- - Related procedure: docs/procedures/start-queue-item.md -->
<!-- - Related prompt: prompts/queue_processor.md -->

> PURPOSE: [FULL SKILL] How to read, interpret, and prioritize queue items. Covers reading queue.csv, understanding the summary contract, checking dependencies, and deciding readiness. Per spec §26.4 item 40.

## Purpose

> CONTENT: One paragraph describing what this skill enables. State: This skill enables an agent to correctly interpret the queue state, identify the next ready item, check dependency readiness, and assess item quality (summary completeness, category validity). Use this skill every time you process the queue.

## When to Invoke

> CONTENT: Specific triggers:
> - Before claiming any queue item (mandatory)
> - When the top item appears blocked and you need to find the next ready item
> - When assessing the overall queue health
> - Before running `make queue:analyze`

## Prerequisites

> CONTENT: Required before starting:
> - `queue/queue.csv` exists and is accessible
> - `queue/queuearchive.csv` exists (for dependency checking)
> - `make queue:validate` passes (queue schema valid)
> - Python and pandas/csv module available for machinery

## Relevant Files/Areas

> CONTENT: Files involved:
> - `queue/queue.csv` — open items
> - `queue/queuearchive.csv` — completed items (for dependency verification)
> - `queue/QUEUE_INSTRUCTIONS.md` — full SOP
> - `scripts/queue-peek.sh` — read top item
> - `skills/agent-ops/queue-triage.py` — triage analyzer machinery

## Step-by-Step Method

> CONTENT: Numbered steps:
> 1. Run `make queue:peek` — read the header and first data row
> 2. Read the COMPLETE `summary` column — this is the work contract
> 3. Check `dependencies` column: parse comma-separated IDs
> 4. For each dependency ID: verify it exists in `queuearchive.csv` with `status=done`
> 5. If any dependency not met: item is NOT READY — document `blocked_by: [IDs]` in notes
> 6. Check `category` column: verify it is in the valid set from `docs/queue/queue-categories.md`
> 7. Check `summary` length ≥ 100 characters with goal, acceptance criteria, definition of done
> 8. Run `skills/agent-ops/queue-triage.py` for automated triage report
> 9. If top item is not ready: identify the next ready item (scan remaining rows)
> 10. Document your triage decision in PR notes or queue notes

## Command Examples

> CONTENT: Exact commands:
> - `make queue:peek` — read top item
> - `make queue:validate` — validate entire queue schema
> - `make queue:analyze` — full intelligence analysis (deps, complexity)
> - `python skills/agent-ops/queue-triage.py` — automated triage report

## Validation Checklist

> CONTENT:
> - [ ] Top item read completely (not just the first column)
> - [ ] All dependencies verified in queuearchive.csv
> - [ ] Summary quality assessed (≥100 chars, includes goal + criteria + done definition)
> - [ ] Category is valid
> - [ ] Triage decision documented

## Common Failure Modes

> CONTENT:
> - **Dependencies not checked**: starting work on an item with unmet dependencies → causes conflicts and incomplete implementation. Fix: always check dependencies before branching.
> - **Partial summary read**: reading only the first 50 chars of a long summary → misses acceptance criteria. Fix: read the ENTIRE summary column value.
> - **Category typo**: category not in valid set → `make queue:validate` will catch but delays work. Fix: check `docs/queue/queue-categories.md` before adding rows.

## Handoff Expectations

> CONTENT: What the next agent needs after triage:
> - Clear statement of which item is being processed (ID + one-line summary)
> - Confirmation of dependency readiness
> - Triage report if multiple items were assessed
> - Branch name for the item being processed

## Related Procedures

> CONTENT: docs/procedures/start-queue-item.md, docs/procedures/handle-blocked-work.md

## Related Prompts

> CONTENT: prompts/queue_processor.md, prompts/task_planner.md

## Related Rules

> CONTENT: .cursor/rules/queue.md (queue invariants), AGENTS.md §9 (queue interaction rules)

## Machinery

> CONTENT: `skills/agent-ops/queue-triage.py` — reads queue.csv and queuearchive.csv, validates schema, checks dependencies, scores item readiness, outputs triage report. Invoked via: `python skills/agent-ops/queue-triage.py` or `make queue:analyze` (as part of analysis).
