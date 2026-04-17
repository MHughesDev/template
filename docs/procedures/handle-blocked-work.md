# docs/procedures/handle-blocked-work.md

<!-- CROSS-REFERENCES -->
<!-- - Skill: skills/agent-ops/blocked-task-recovery.md -->
<!-- - Rule: .cursor/rules/queue.md (blocked state) -->

**Purpose:** SOP: Document blockers, escalate, optionally requeue lower items. Per spec §26.5 item 146 and §8.3.

## Purpose

Blocked work must be documented explicitly rather than silently skipped or ignored. The blocker must be escalated to whoever can unblock it.

## Trigger / When to Use

When the top queue item has unmet dependencies, awaits an external decision, or lacks a required resource.

## Prerequisites

Blocker clearly identified. queue.csv writable.

## Exact Commands

`make queue:validate` (after updating notes), **`make queue:top-item`** (next ready item as JSON)

## Ordered Steps

1. Identify the specific blocker: missing dependency, external API, human decision needed
2. Update the `notes` column of the blocked item:
   `blocked_by: <reason> | owner: <who can unblock> | next_step: <what triggers unblocking>`
3. Do NOT archive the item — it stays in queue.csv
4. Create escalation: GitHub issue OR reply to the relevant PR/discussion
5. Run `make queue:validate` to verify the updated notes are valid
6. (Optional) If policy allows: identify and process next READY item (skip blocked)
7. Document the skip decision in PR notes or AGENTS.md handoff

## Expected Artifacts / Outputs

queue.csv notes column updated with blocker info. Escalation created (issue or comment).

## Validation Checks

- [ ] Blocker documented in notes (reason + owner + next step)
- [ ] Item NOT archived
- [ ] Escalation created
- [ ] make queue:validate passes

## Rollback or Failure Handling

If no next ready item exists and all items are blocked: document in AGENTS.md handoff and wait for human direction.

## Handoff Expectations

Queue notes updated. Escalation created. Handoff document states which item is blocked, why, and who can unblock.
