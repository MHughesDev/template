# docs/procedures/update-documentation.md

<!-- CROSS-REFERENCES -->
<!-- - Rule: .cursor/rules/documentation.md -->
<!-- - Skill: skills/repo-governance/maintaining-procedural-docs.md -->

> PURPOSE: SOP: When and how to update docs alongside code changes. Per spec §26.5 item 147 and §8.3.

## Purpose

> CONTENT: Documentation updated alongside the code change it describes keeps the system self-consistent. Deferred documentation updates always drift.

## Trigger / When to Use

> CONTENT: Per .cursor/rules/documentation.md triggers: new env var, new endpoint, behavior change, ops change, new error code, architectural decision.

## Prerequisites

> CONTENT: Code change implemented. Affected docs identified.

## Exact Commands

> CONTENT: `make docs:check`, `make docs:generate`, `make docs:index`

## Ordered Steps

> CONTENT:
> 1. Identify all affected docs using .cursor/rules/documentation.md trigger list
> 2. For generated docs (endpoints.md, environment-vars.md, error-codes.md): update the source, then `make docs:generate`
> 3. For manual docs: edit the specific sections that changed
> 4. Update doc indexes if new files were added
> 5. Run `make docs:check` — verify no broken links
> 6. For generated docs: verify make docs:check shows no drift
> 7. Commit docs changes alongside the code change (same PR or immediate follow-up)

## Expected Artifacts / Outputs

> CONTENT: Updated documentation files. make docs:check passing.

## Validation Checks

> CONTENT:
> - [ ] All trigger conditions checked
> - [ ] Generated docs regenerated via make docs:generate
> - [ ] Manual docs updated with specific changed sections
> - [ ] make docs:check passes

## Rollback or Failure Handling

> CONTENT: If make docs:check fails on broken links: fix the link or the referenced file.

## Handoff Expectations

> CONTENT: Docs updated, check passing, docs changes in same PR as code changes.
