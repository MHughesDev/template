# docs/procedures/handle-blocked-work.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Skill: skills/agent-ops/blocked-task-recovery.md -->
<!-- - Rule: .cursor/rules/queue.md (blocked state) -->

> PURPOSE: SOP: Document blockers, escalate, optionally requeue lower items. Per spec §26.5 item 146 and §8.3.

## Purpose

> CONTENT: Blocked work must be documented explicitly rather than silently skipped or ignored. The blocker must be escalated to whoever can unblock it.

## Trigger / When to Use

> CONTENT: When the top queue item has unmet dependencies, awaits an external decision, or lacks a required resource.

## Prerequisites

> CONTENT: Blocker clearly identified. queue.csv writable.

## Exact Commands

> CONTENT: `make queue:validate` (after updating notes), `make queue:peek` (to see next ready item)

## Ordered Steps

> CONTENT:
> 1. Identify the specific blocker: missing dependency, external API, human decision needed
> 2. Update the `notes` column of the blocked item:
>    `blocked_by: <reason> | owner: <who can unblock> | next_step: <what triggers unblocking>`
> 3. Do NOT archive the item — it stays in queue.csv
> 4. Create escalation: GitHub issue OR reply to the relevant PR/discussion
> 5. Run `make queue:validate` to verify the updated notes are valid
> 6. (Optional) If policy allows: identify and process next READY item (skip blocked)
> 7. Document the skip decision in PR notes or AGENTS.md handoff

## Expected Artifacts / Outputs

> CONTENT: queue.csv notes column updated with blocker info. Escalation created (issue or comment).

## Validation Checks

> CONTENT:
> - [ ] Blocker documented in notes (reason + owner + next step)
> - [ ] Item NOT archived
> - [ ] Escalation created
> - [ ] make queue:validate passes

## Rollback or Failure Handling

> CONTENT: If no next ready item exists and all items are blocked: document in AGENTS.md handoff and wait for human direction.

## Handoff Expectations

> CONTENT: Queue notes updated. Escalation created. Handoff document states which item is blocked, why, and who can unblock.
