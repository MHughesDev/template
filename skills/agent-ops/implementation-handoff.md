# skills/agent-ops/implementation-handoff.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/agent-ops/handoff-template-generator.py -->
<!-- - Related procedure: docs/procedures/handoff.md -->
<!-- - Related prompt: prompts/implementation_agent.md -->

**Purpose:** [FULL SKILL] How to write a complete handoff document: files changed, commands run with output, risks, follow-ups, PR link, and queue state update. Per spec §26.4 item 42.

## Purpose

One paragraph. A handoff document is the evidence artifact that makes the next agent or human reviewer able to understand exactly what happened, verify the work, assess residual risks, and continue from where this agent stopped. It is non-optional for any meaningful change.

## When to Invoke

- After implementation is complete, before opening PR
- After archiving a queue item
- When handing off to a human reviewer
- When work is blocked and you must stop (partial handoff)

## Prerequisites

- Implementation complete or explicitly blocked
- All validation commands run (make lint, make typecheck, make test, or noting which failed)
- Queue notes updated
- PR opened (or in progress)

## Relevant Files/Areas

- `queue/queue.csv` — notes column to update
- `queue/queuearchive.csv` — where completed row goes
- `.github/PULL_REQUEST_TEMPLATE.md` — the PR template this populates
- `skills/agent-ops/handoff-template-generator.py` — machinery to auto-populate from git

## Step-by-Step Method

Numbered steps:
1. Run `python skills/agent-ops/handoff-template-generator.py` to generate a pre-populated template
2. **Files changed**: list every file with a one-line description of the change
3. **Commands run**: for each command run during implementation, paste the key output (not full — just pass/fail line and any errors)
4. **Acceptance criteria verification**: for each criterion from the plan, state met/not-met with evidence
5. **Risks**: list any residual risks discovered during implementation
6. **Follow-ups**: list any out-of-scope findings that became queue items or issues
7. **PR link**: paste the PR URL
8. **Queue state**: confirm the queue row's notes column has been updated with PR URL

## Command Examples

- `python skills/agent-ops/handoff-template-generator.py` — generate template
- `git diff --stat HEAD~<n>` — summarize file changes
- `make queue:archive` — archive completed item

## Validation Checklist

- [ ] Files changed list is complete (no files missing)
- [ ] Commands run section has key output for each validation command
- [ ] All acceptance criteria addressed (met/not-met/partial with evidence)
- [ ] Residual risks documented
- [ ] Follow-up queue items or issues created and referenced
- [ ] PR URL included
- [ ] Queue notes updated with PR URL

## Common Failure Modes

- **Partial handoff**: listing files but not commands run — reviewer cannot verify. Fix: always include commands + key output.
- **Missing residual risks**: hiding discovered problems. Fix: surface all risks even if they're "probably fine".
- **Queue not updated**: leaving queue row without PR URL → next agent can't find the work. Fix: always update notes before closing.

## Handoff Expectations

The handoff document is a complete audit trail. A human reviewer should be able to: (1) understand what changed, (2) verify it worked (from commands output), (3) know what risks remain, (4) know what follow-up is needed — without talking to the agent.

## Related Procedures

docs/procedures/handoff.md, docs/procedures/archive-queue-item.md

## Related Prompts

prompts/implementation_agent.md, prompts/queue_processor.md

## Related Rules

AGENTS.md §Navigation (handoff format), .cursor/rules/global.md (Evidence requirements)

## Machinery

`skills/agent-ops/handoff-template-generator.py` — reads git diff, recent commands from shell history, queue.csv for current item, and generates a pre-filled Markdown handoff template. Invoke: `python skills/agent-ops/handoff-template-generator.py --queue-id Q-001`
