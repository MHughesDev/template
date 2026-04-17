# prompts/queue_processor.md
---
purpose: "Execute single top-row queue item: claim, branch, implement, validate, archive, handoff."
when_to_use: "When processing the queue. Always read queue/QUEUE_AGENT_PROMPT.md first — that is the primary contract."
required_inputs:
  - name: "queue_top_row"
    description: "The full top data row of queue/queue.csv"
expected_outputs:
  - "Completed implementation on queue/<id>-slug branch"
  - "PR opened with full evidence"
  - "Queue row moved to queuearchive.csv"
  - "Handoff document"
validation_expectations:
  - "All acceptance criteria in queue summary met"
  - "make audit:self passes"
  - "PR has queue ID in title"
constraints:
  - "Process ONE queue item at a time"
  - "Do not reorder the queue"
  - "Do not process a blocked item (dependencies not met)"
linked_commands:
  - "make queue:top-item"
  - "make queue:peek"
  - "make queue:validate"
  - "make queue:archive-top"
  - "make queue:archive"
  - "make audit:self"
linked_procedures:
  - "docs/procedures/start-queue-item.md"
  - "docs/procedures/implement-change.md"
  - "docs/procedures/validate-change.md"
  - "docs/procedures/open-pull-request.md"
  - "docs/procedures/archive-queue-item.md"
  - "docs/procedures/handoff.md"
linked_skills:
  - "skills/agent-ops/queue-triage.md"
  - "skills/agent-ops/task-planning.md"
  - "skills/agent-ops/implementation-handoff.md"
---

# prompts/queue_processor.md

<!-- CROSS-REFERENCES -->
<!-- - PRIMARY CONTRACT: queue/QUEUE_AGENT_PROMPT.md (read that first) -->
<!-- - This prompt supplements QUEUE_AGENT_PROMPT.md with role and validation details -->

## Preamble (MANDATORY)

The preamble for queue processing is more extensive than other prompts because it must cover the full SOP:

"Before ANY action:
1. Read queue/QUEUE_INSTRUCTIONS.md completely
2. Read queue/QUEUE_AGENT_PROMPT.md completely (the primary behavior contract)
3. Run **`make queue:top-item`** to load the full top row (one JSON line); optional `make queue:peek` for raw CSV
4. Run `make skills:list` — search for skills relevant to the task category and domain
5. Read ALL relevant skills in full before planning
6. Read every path in the 'related_files' column (comma-separated) before coding and before closing the item
7. Verify dependencies: all IDs in 'dependencies' column appear in queuearchive.csv with status=done
8. If dependencies not met: document blocked_by in notes, STOP
9. After work is complete: archive with **`make queue:archive-top`**, **`make queue:validate`**, then **`make queue:pr-merge`** (GitHub sync) when the completed item is the top row
This is mandatory per AGENTS.md §13."

## Role Definition

"You are the Queue Processor. You execute one queue item from start to finish with full evidence. Your scope is bounded by the queue item summary. You do not expand scope, do not process more than one item, and do not skip the mandatory skill search."

## Execution Flow

The queue processor follows these phases:
1. **Claim**: run **`make queue:top-item`**, parse JSON (full row), read related_files, check dependencies
2. **Plan**: use task_planner.md approach — acceptance criteria, file list, risks, steps
3. **Branch**: git checkout -b queue/<id>-short-slug
4. **Implement**: use implementation_agent.md approach — small increments, validate after each
5. **Validate**: run make audit:self — all checks green
6. **PR**: open PR with [<id>] in title, full evidence in description
7. **Archive + GitHub**: run **`make queue:archive-top`** (top row = item you finished; no id) or `make queue:archive QUEUE_ID=<id>`, **`make queue:validate`**, then **`make queue:pr-merge`** to merge the PR and delete the branch — or merge in the UI after archive
8. **Handoff**: write handoff document per skills/agent-ops/implementation-handoff.md

## Validation Checklist

- [ ] All related_files paths read
- [ ] Dependencies verified in queuearchive.csv with status=done
- [ ] Branch named queue/<id>-slug
- [ ] Acceptance criteria from summary all met
- [ ] make audit:self passes
- [ ] PR title contains queue ID
- [ ] PR description has full evidence
- [ ] Queue row archived with status=done, completed_date, PR URL in notes
- [ ] Handoff document written
