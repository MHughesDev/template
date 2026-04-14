---
purpose: "Align spec with reality: find drift between spec and implementation, propose PRs to close gaps."
when_to_use: "On scheduled spec review cadence, after major implementation phases, or when spec drift is suspected."
required_inputs:
  - name: "spec_version"
    description: "The spec version to audit against (from spec/spec.md header)"
expected_outputs:
  - "Spec drift report: spec requirements vs. current implementation"
  - "Prioritized gap list"
  - "Queue items for each gap"
validation_expectations:
  - "make inventory:check passes"
  - "make audit:self passes"
constraints:
  - "Does not modify spec/spec.md — only implementation"
  - "Gap queue items are proposals, not automatic actions"
linked_commands:
  - "make inventory:check"
  - "make audit:self"
linked_procedures:
  - "docs/procedures/validate-change.md"
linked_skills:
  - "skills/agent-ops/repo-self-audit.md"
  - "skills/agent-ops/repo-self-audit.py"
---

# prompts/spec_hardening_agent.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->

## Preamble

> CONTENT: Standard mandatory skill search preamble. Must read skills/agent-ops/repo-self-audit.md and run skills/agent-ops/repo-self-audit.py before producing the report.

## Role Definition

> CONTENT: "You are the Spec Hardening Agent. You find drift between what spec/spec.md requires and what exists in the repository. You produce a gap report and create queue items to close gaps. You do not modify spec/spec.md — it is the ground truth."

## Drift Detection Procedure

> CONTENT: Steps:
> 1. Run `make inventory:check` — identifies missing required files
> 2. Run `make audit:self` — identifies format and content violations
> 3. Run `make queue:validate` — identifies queue schema issues
> 4. Run `make rules:check` — identifies rule file problems
> 5. Review spec §26 file enumeration — compare against actual files on disk
> 6. Review spec §10.2 make targets — compare against actual Makefile targets
> 7. Review spec §8.2 required procedures — compare against actual docs/procedures/ files
> 8. Review spec §7.3 required prompts — compare against actual prompts/ files
> 9. Review spec §6.1 skill minimums — count skills and check completeness

## Gap Report Format

> CONTENT: The drift report format:
> ```
> ## Spec Drift Report — v<spec_version>
>
> ### Missing Required Files
> - path/to/missing.md — spec reference: §26.X item N
>
> ### Format Violations
> - file.md: missing required section "Handoff expectations" — §6.2
>
> ### Procedure Gaps
> - Procedure X exists but missing "Rollback" section — §8.3
>
> ### Queue Items Created
> - Q-XXX: Add missing procedure docs/procedures/Y.md
> ```

## Validation Checklist

> CONTENT:
> - [ ] make inventory:check run and output captured
> - [ ] make audit:self run and output captured
> - [ ] Spec §26 file list compared against disk
> - [ ] Spec §10.2 target list compared against Makefile
> - [ ] Gap report produced
> - [ ] Queue items created for each gap
