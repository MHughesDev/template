# skills/init/queue-seeder.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/init/queue-seeder.py -->
<!-- - Related procedure: docs/procedures/initialize-repo.md (Phase 5) -->

> PURPOSE: Populate queue/queue.csv from idea.md §12 and §15. Assigns batch IDs from phases, generates proper summaries, validates with make queue:validate. Per spec §28.7 item 334.

## Purpose

> CONTENT: One paragraph. The queue seeder converts the human's work prioritization in idea.md §12 into properly formatted queue.csv rows with sequential IDs, batch assignments from phases (idea.md §15), and summaries that meet the minimum quality bar (≥100 chars with acceptance criteria).

## When to Invoke

> CONTENT: During initialization Phase 5 (Seed Queue). After all profiles are configured. Before running make queue:validate.

## Prerequisites

> CONTENT: idea.md §12 filled with at least one work item. idea.md §15 (phases) optional but used for batch assignment. queue/queue.csv exists with correct header.

## Relevant Files/Areas

> CONTENT: idea.md §12 and §15, queue/queue.csv, queue/QUEUE_INSTRUCTIONS.md, skills/init/queue-seeder.py

## Step-by-Step Method

> CONTENT: Numbered steps:
> 1. Run `make idea:queue` which calls `scripts/idea-to-queue.sh`
> 2. Review generated rows: verify summaries are ≥100 chars
> 3. Manually add acceptance criteria if summaries are too brief
> 4. Run `make queue:validate` to verify schema
> 5. Add standard initialization verification items (review init PR, verify all tests pass)
> 6. For any open question from idea.md §16: add blocked queue item with notes explaining the blocker

## Command Examples

> CONTENT: `make idea:queue`, `make queue:validate`, `make queue:peek`

## Validation Checklist

> CONTENT:
> - [ ] All items from idea.md §12 appear in queue.csv
> - [ ] All summaries ≥100 chars with acceptance criteria
> - [ ] make queue:validate passes
> - [ ] Batch values assigned from idea.md §15 phases
> - [ ] Blocked items created for open questions in idea.md §16

## Common Failure Modes

> CONTENT: Summary too short → make queue:validate fails. Fix: expand summary to include goal, acceptance criteria, definition of done.

## Handoff Expectations

> CONTENT: queue.csv seeded, make queue:validate passes, first item ready for processing.

## Related Procedures

> CONTENT: docs/procedures/initialize-repo.md (Phase 5)

## Related Prompts

> CONTENT: prompts/repo_initializer.md

## Related Rules

> CONTENT: .cursor/rules/queue.md (summary quality requirements)
