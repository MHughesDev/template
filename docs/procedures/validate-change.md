# docs/procedures/validate-change.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §7, prompts/reviewer_critic.md -->
<!-- - Uses: make audit:self -->

> PURPOSE: SOP: Run full validation matrix before opening PR. Per spec §26.5 item 142 and §8.3.

## Purpose

> CONTENT: Full validation before PR prevents CI failures and reviewer-discovered issues that waste cycles. This is the last checkpoint before the change is shared.

## Trigger / When to Use

> CONTENT: After implement-change.md is complete. Before running open-pull-request.md.

## Prerequisites

> CONTENT: All implementation commits on branch. Tests written and expected to pass.

## Exact Commands

> CONTENT: `make fmt`, `make lint`, `make typecheck`, `make test`, `make queue:validate`, `make docs:check`, `make security:scan`, `make audit:self`

## Ordered Steps

> CONTENT:
> 1. `make fmt` — apply formatting (auto-fix mode); commit if changes made
> 2. `make lint` — must produce zero errors
> 3. `make typecheck` — must produce zero errors
> 4. `make test` — all tests pass, coverage above floor
> 5. (If queue files touched) `make queue:validate` — queue schema valid
> 6. (If docs updated) `make docs:check` — no broken links, generated docs match source
> 7. (If security-adjacent) `make security:scan` — no unaccepted HIGH/CRITICAL findings
> 8. `make audit:self` — spec compliance check
> 9. Capture all output — paste key lines in PR description

## Expected Artifacts / Outputs

> CONTENT: Validation report with all commands run and their pass/fail status. To be included in PR description.

## Validation Checks

> CONTENT:
> - [ ] make fmt: no formatting changes
> - [ ] make lint: zero errors
> - [ ] make typecheck: zero errors
> - [ ] make test: all pass, coverage above floor
> - [ ] make audit:self: no BLOCKING findings

## Rollback or Failure Handling

> CONTENT: If any check fails: fix before opening PR. Do not open PRs with known failures — document why if exception is needed.

## Handoff Expectations

> CONTENT: All checks passing. Validation report ready for PR description.
