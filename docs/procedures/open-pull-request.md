# docs/procedures/open-pull-request.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Template: .github/PULL_REQUEST_TEMPLATE.md -->
<!-- - Referenced by: AGENTS.md §4 (Branch and PR Policy) -->

> PURPOSE: SOP: Create PR with title, description template, evidence, labels, queue linkage. Per spec §26.5 item 143 and §8.3.

## Purpose

> CONTENT: A well-formed PR provides all context needed for review without the reviewer asking questions. Evidence is embedded in the description.

## Trigger / When to Use

> CONTENT: After validate-change.md passes. All CI checks expected to be green.

## Prerequisites

> CONTENT: All validation passing. Branch pushed to origin. PR template (.github/PULL_REQUEST_TEMPLATE.md) read.

## Exact Commands

> CONTENT: `git push -u origin <branch>`, then open PR via GitHub UI or `gh pr create`.

## Ordered Steps

> CONTENT:
> 1. Push branch: `git push -u origin queue/<id>-slug`
> 2. Open PR targeting `main` branch
> 3. Title format: `[<queue-id>] <type>(<scope>): <description>` (max 72 chars)
> 4. Fill description using .github/PULL_REQUEST_TEMPLATE.md:
>    - Summary of changes (one paragraph)
>    - Queue item ID with link to row
>    - Files changed list
>    - Commands run with key output (paste validation results)
>    - Tests added/updated
>    - Documentation updated
>    - Risks and follow-ups
>    - Completion checklist
> 5. Add labels: category (api, docs, infra), type (feature, fix, chore, security)
> 6. Wait for CI to complete — if CI fails, fix before requesting review

## Expected Artifacts / Outputs

> CONTENT: Open PR with green CI, queue ID in title, full evidence in description.

## Validation Checks

> CONTENT:
> - [ ] PR title contains queue ID
> - [ ] CI passing (all checks green)
> - [ ] Description has evidence (commands run, output)
> - [ ] Labels added

## Rollback or Failure Handling

> CONTENT: If CI fails after PR opened: fix on the same branch (add more commits), do not reopen.

## Handoff Expectations

> CONTENT: PR URL in queue notes. Human reviewer can approve and merge.
