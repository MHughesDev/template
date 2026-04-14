# queue/QUEUE_AGENT_PROMPT.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Read by: agents processing queue items (injected as context) -->
<!-- - Referenced by: queue/QUEUE_INSTRUCTIONS.md, prompts/queue_processor.md -->
<!-- - Per spec §26.6 item 193 -->

> PURPOSE: Executable behavior contract for agents processing queue work. Injected as context when an agent processes queue items. Per spec §2 and §26.6 item 193.

## Role Definition

> CONTENT: State the agent's role and authority scope: "You are processing a queue item from queue/queue.csv. Your authority is bounded by the queue item's summary — you implement exactly what the summary describes, no more, no less. You are not authorized to silently expand scope or skip the mandatory skill search."

## Required Read Order

> CONTENT: Ordered list of what must be read before processing begins:
> 1. This file (QUEUE_AGENT_PROMPT.md) — complete
> 2. queue/QUEUE_INSTRUCTIONS.md — complete
> 3. The top data row of queue/queue.csv — complete (every column)
> 4. All files/docs referenced in the summary column
> 5. Skills (mandatory search — see below)

## MANDATORY SKILL SEARCH (Non-Negotiable)

> CONTENT: Per spec §4.1 item 13 and AGENTS.md §13 — this step is mandatory and non-negotiable.
>
> Before planning or writing any code:
> 1. Identify the task domain from the summary (backend, security, testing, infrastructure, etc.)
> 2. Run `make skills:list` OR read skills/README.md
> 3. Scan the "When to invoke" section of ALL skills in the relevant category
> 4. Read every HIGH-relevance skill in FULL before proceeding
> 5. Note machinery (.py files) as available automation tools
> 6. Document which skills were found in your handoff notes
>
> **An agent that skips this step is operating out of policy. Stop and complete this step.**

## Execution Rules

> CONTENT: Numbered rules for queue item execution:
> 1. Process ONE item at a time — never start a second item until the first is archived
> 2. Read the COMPLETE summary — it is the work contract; partial reads cause scope failures
> 3. Verify ALL dependencies in queuearchive.csv with status=done before starting
> 4. If any dependency not met: document in notes as `blocked_by:`, STOP, do not start
> 5. Plan before coding: acceptance criteria, file impact, risks, scope bounds
> 6. Validate after each increment: `make lint && make test`
> 7. Full validation before PR: `make audit:self`
> 8. STOP and escalate if security or tenancy semantics are ambiguous

## Branch Naming

> CONTENT: Required format: `queue/<id>-short-slug` where id is the exact value from the id column. Example: `queue/Q-001-add-invoice-endpoint`.

## PR Requirements

> CONTENT: Every PR must have:
> - Queue ID in title: `[Q-001] feat(invoices): implement invoice CRUD endpoints`
> - Evidence in description: files changed, commands run with output, acceptance criteria met
> - All CI checks green
> - PR URL pasted into queue item notes before or during archiving

## Archive Procedure

> CONTENT: After PR merged:
> 1. Run `make queue:archive QUEUE_ID=<id>`
> 2. Verify in queuearchive.csv: status=done, completed_date=YYYY-MM-DD, PR URL in notes
> 3. Run `make queue:validate`
> 4. Confirm queue.csv no longer contains this row

## Blocked Handling

> CONTENT: If blocked during work:
> 1. Document in queue.csv notes: `blocked_by: <reason> | owner: <who> | next_step: <what>`
> 2. Leave item in queue.csv (do NOT archive)
> 3. Create GitHub issue or escalation
> 4. Write partial handoff document

## Evidence Requirements

> CONTENT: Every queue item completion requires:
> - Handoff document (per docs/procedures/handoff.md)
> - In PR description: files changed list + commands run + acceptance criteria verification
> - In queue notes: PR URL + completion date
> - In queuearchive.csv: full row with status=done
