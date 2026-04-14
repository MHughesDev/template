# docs/procedures/start-queue-item.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §9, prompts/queue_processor.md -->
<!-- - Skill: skills/agent-ops/queue-triage.md -->

> PURPOSE: SOP: Claim top queue row, create branch, read relevant docs. Per spec §26.5 item 139 and §8.3.

## Purpose

> CONTENT: Correctly starting a queue item prevents the most common failure modes: starting blocked work, missing acceptance criteria, or skipping the mandatory skill search.

## Trigger / When to Use

> CONTENT: When ready to begin processing the next queue item. After any previous item is archived or when assigned to queue processing.

## Prerequisites

> CONTENT: queue/QUEUE_INSTRUCTIONS.md read. Previous queue item archived (or confirmed none). make queue:validate passes.

## Exact Commands

> CONTENT: `make queue:peek`, `make queue:validate`, `make skills:list`, `git checkout -b queue/<id>-slug`

## Ordered Steps

> CONTENT:
> 1. Run `make queue:peek` — read the header row + first data row completely
> 2. Read the COMPLETE summary column — this is the work contract; do not skip
> 3. Parse the `dependencies` column — check each ID against queuearchive.csv
> 4. Run `make queue:validate` — verify queue schema before starting
> 5. If any dependency not in archive with status=done: update notes with `blocked_by: [IDs]` and STOP (see handle-blocked-work.md)
> 6. Run `make skills:list` — identify relevant skills for the task domain
> 7. Read ALL relevant skills in full
> 8. Read all files referenced in the summary
> 9. Create branch: `git checkout -b queue/<id>-short-slug`
> 10. Document understanding: list acceptance criteria, files to change, risks
> 11. Store plan in PR description draft or queue notes

## Expected Artifacts / Outputs

> CONTENT: Branch created with correct naming. Plan documented. Relevant skills read and noted.

## Validation Checks

> CONTENT:
> - [ ] Top item read completely
> - [ ] Dependencies verified in queuearchive.csv
> - [ ] Mandatory skill search completed
> - [ ] Branch named queue/<id>-slug
> - [ ] Plan documented

## Rollback or Failure Handling

> CONTENT: If blocked: follow docs/procedures/handle-blocked-work.md. Do not start implementation on a blocked item.

## Handoff Expectations

> CONTENT: Branch created, plan documented, ready to begin implementation.
