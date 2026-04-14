# skills/repo-governance/maintaining-procedural-docs.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Related procedure: docs/procedures/update-documentation.md -->
<!-- - Machinery: skills/repo-governance/docs-freshness-checker.py -->

> PURPOSE: How to keep docs/procedures/ current: drift detection, update triggers, linking to Make targets. Per spec §26.4 item 51.

## Purpose

> CONTENT: One paragraph. Procedures in docs/procedures/ are the canonical SOPs for agents. If they drift from the actual CI commands or system behavior, agents follow wrong steps and produce wrong results. This skill prevents procedure drift through systematic review and update triggers.

## When to Invoke

> CONTENT: When any Make target changes behavior. When a CI stage is added/removed. When a procedure's prerequisites change. On quarterly documentation freshness review.

## Prerequisites

> CONTENT: docs/procedures/README.md read. The changed behavior is clearly identified. skills/repo-governance/docs-freshness-checker.py available.

## Relevant Files/Areas

> CONTENT: docs/procedures/ directory, scripts/docs-freshness-checker.py (machinery), Makefile (source of truth for commands)

## Step-by-Step Method

> CONTENT: Numbered steps:
> 1. Run `python skills/repo-governance/docs-freshness-checker.py` to identify potentially stale procedures
> 2. For each flagged procedure: read the procedure and compare with actual current behavior
> 3. Identify specific outdated steps: commands that changed, prerequisites that changed
> 4. Edit the procedure file: update the Commands section with exact current make targets
> 5. Update Prerequisites section if setup requirements changed
> 6. Update Ordered Steps to match actual current behavior
> 7. Run `make docs:check` to verify no broken links
> 8. PR with rationale (what changed in the system that prompted the update)

## Command Examples

> CONTENT: `python skills/repo-governance/docs-freshness-checker.py`, `make docs:check`

## Validation Checklist

> CONTENT:
> - [ ] All procedure steps match actual system behavior
> - [ ] All Command examples are current make targets
> - [ ] make docs:check passes
> - [ ] Related procedures linked correctly

## Common Failure Modes

> CONTENT: Updating command names without updating the step that uses them → procedure is internally inconsistent. Fix: update both the Commands section and every Step that uses the command.

## Handoff Expectations

> CONTENT: Procedure updated, docs:check passes, change rationale documented.

## Related Procedures

> CONTENT: docs/procedures/update-documentation.md

## Related Prompts

> CONTENT: prompts/documentation_updater.md

## Related Rules

> CONTENT: .cursor/rules/documentation.md (procedure drift trigger)
