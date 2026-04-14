# docs/procedures/archive-queue-item.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Rule: .cursor/rules/queue.md (archive-before-delete policy) -->
<!-- - Make target: make queue:archive -->

> PURPOSE: SOP: Move completed queue row to archive with required fields. Per spec §26.5 item 145 and §8.3.

## Purpose

> CONTENT: Proper archiving ensures queue history is preserved and the next queue item becomes the active one. Missing or partial archiving leads to queue confusion.

## Trigger / When to Use

> CONTENT: After PR is merged (or item is cancelled/superseded). Never archive before PR is merged for done items.

## Prerequisites

> CONTENT: PR merged (for done items). Queue item ID known. queuearchive.csv exists with correct header.

## Exact Commands

> CONTENT: `make queue:archive` (scripted move) or manual CSV editing, then `make queue:validate`.

## Ordered Steps

> CONTENT:
> 1. Verify the PR is merged and all acceptance criteria confirmed
> 2. Run `make queue:archive QUEUE_ID=<id>` — scripted move from queue.csv to queuearchive.csv
>    OR manually: copy the full row from queue.csv to queuearchive.csv, add status, completed_date, PR URL
> 3. Verify in queuearchive.csv: row has status=done, completed_date=YYYY-MM-DD, PR URL in notes
> 4. Remove the row from queue.csv
> 5. Run `make queue:validate` — must pass with no errors
> 6. Run `make queue:peek` — verify next item is now the top row

## Expected Artifacts / Outputs

> CONTENT: Row in queuearchive.csv with all fields. Row removed from queue.csv. make queue:validate passing.

## Validation Checks

> CONTENT:
> - [ ] Row in queuearchive.csv with status=done, completed_date, PR URL in notes
> - [ ] Row removed from queue.csv
> - [ ] make queue:validate passes

## Rollback or Failure Handling

> CONTENT: If queue:validate fails after archiving: check for schema errors in the archive row; fix and re-run.

## Handoff Expectations

> CONTENT: Queue archived. Next queue item visible at top of queue.csv.
