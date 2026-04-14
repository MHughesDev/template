# docs/procedures/update-or-create-rule.md

<!-- CROSS-REFERENCES -->
<!-- - Skill: skills/agent-ops/rule-refinement-after-mistakes.md -->
<!-- - Skill: skills/repo-governance/authoring-cursor-rules.md -->

**Purpose:** SOP: Rule lifecycle — creating new .cursor/rules or updating existing ones. Per spec §26.5 item 149 and §8.3.

## Purpose

Rules prevent recurrence of known failure modes. Adding them correctly ensures they are enforceable, auditable, and non-contradictory.

## Trigger / When to Use

After a repeated mistake is identified. When a new constraint needs encoding. Per AGENTS.md §10 policy.

## Prerequisites

Specific behavior to prevent is clearly defined. All existing .cursor/rules files read.

## Exact Commands

`make rules:check`, `python skills/repo-governance/rule-linter.py`

## Ordered Steps

1. Identify the specific pattern/mistake (link to the PR or incident)
2. Determine scope: global (alwaysApply) or path-scoped (globs)
3. Choose existing file to update OR create new .cursor/rules/<name>.md
4. Write YAML frontmatter: alwaysApply or globs, description
5. Write rule(s) as numbered list with NEVER/MUST/ALWAYS + specific pattern
6. Read ALL other rule files: check for contradictions
7. Run `make rules:check`
8. Run `python skills/repo-governance/rule-linter.py` — verify no findings
9. PR with rationale linking to the incident/pattern

## Expected Artifacts / Outputs

New or updated rule file. make rules:check passing.

## Validation Checks

- [ ] Rule is specific and actionable
- [ ] No contradictions with other rules
- [ ] make rules:check passes
- [ ] Rationale links to incident

## Rollback or Failure Handling

If rule causes lint errors in legitimate code: rule is too broad. Narrow the scope with globs.

## Handoff Expectations

Rule committed, enforcement verified, PR links to motivating incident.
