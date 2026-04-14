# docs/procedures/plan-change.md

<!-- CROSS-REFERENCES -->
<!-- - Skill: skills/agent-ops/task-planning.md -->
<!-- - Prompt: prompts/task_planner.md -->

> PURPOSE: SOP: Create implementation plan with acceptance criteria, file impact, risks, scope bounds. Per spec §26.5 item 140 and §8.3.

## Purpose

> CONTENT: The plan is the contract between planning and implementation. Without it, agents scope-creep, miss criteria, and produce unverifiable changes.

## Trigger / When to Use

> CONTENT: After start-queue-item.md (branch created, queue item read). Before any code is written.

## Prerequisites

> CONTENT: Queue item read completely. Relevant skills read. Source files read. AGENTS.md §5 read.

## Exact Commands

> CONTENT: No make targets for planning itself. All commands are for reading: `make queue:peek`, `make skills:list`.

## Ordered Steps

> CONTENT:
> 1. Restate acceptance criteria VERBATIM from the queue summary — no paraphrasing
> 2. Read every file mentioned in the summary (and their imports)
> 3. List every file that must be created or modified (exhaustive list — include tests and docs)
> 4. For each file: describe the specific change in one sentence
> 5. Identify risks: security, tenant isolation, API contract, migration safety, test coverage
> 6. For each risk: state a mitigation
> 7. List 3-5 explicit non-goals (what this change does NOT do)
> 8. Write definition of done: verifiable criteria for "complete"
> 9. Break into ordered, independently-committable steps

## Expected Artifacts / Outputs

> CONTENT: Plan document stored in PR description draft or queue notes. Format per skills/agent-ops/task-planning.md output section.

## Validation Checks

> CONTENT:
> - [ ] Acceptance criteria verbatim from task
> - [ ] File list exhaustive (no surprises)
> - [ ] Risks have mitigations
> - [ ] Scope bounds explicit (3+ non-goals)
> - [ ] Definition of done is verifiable

## Rollback or Failure Handling

> CONTENT: If plan reveals the task is larger than expected: split into smaller tasks, create additional queue items, get approval before proceeding.

## Handoff Expectations

> CONTENT: Plan document complete and stored. Ready to begin implementation.
