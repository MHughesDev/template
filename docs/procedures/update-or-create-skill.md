# docs/procedures/update-or-create-skill.md

<!-- CROSS-REFERENCES -->
<!-- - Skill: skills/agent-ops/prompt-to-procedure-promotion.md -->
<!-- - Rule: .cursor/rules/skills.md -->

**Purpose:** SOP: Skill lifecycle — creating new skills or updating existing ones to the standard format. Per spec §26.5 item 148 and §8.3.

## Purpose

Skills encode recurring knowledge. Adding or updating them correctly ensures future agents can find and use the skill. A skill with missing sections is as bad as no skill.

## Trigger / When to Use

When a recurring work pattern is identified (same class of task done 2+ times). When an existing skill needs to reflect changed tooling or commands.

## Prerequisites

The skill need is clear. Correct category identified (agent-ops, backend, security, etc.). skills/README.md read.

## Exact Commands

`make skills:list` (verify new skill appears), `make rules:check`

## Ordered Steps

1. Identify the skill category directory: skills/<category>/
2. Create skills/<category>/<skill-name>.md with all 12 §6.2 sections
3. For each section: write substantive content (not just headings)
4. If machinery needed: create skills/<category>/<skill-name>.py with typed functions
5. Add ## Machinery section to .md referencing the .py file
6. Update skills/README.md index with new entry
7. Run `make skills:list` — verify new skill appears
8. PR with rationale: what recurring pattern prompted this skill

## Expected Artifacts / Outputs

New skill .md (and optional .py) file. Updated skills/README.md index.

## Validation Checks

- [ ] All 12 §6.2 sections present with substantive content
- [ ] Machinery .py follows PYTHON_PROCEDURES.md
- [ ] skills/README.md updated
- [ ] make skills:list shows new skill

## Rollback or Failure Handling

If skill format is wrong: refer to .cursor/rules/skills.md for required sections.

## Handoff Expectations

New skill committed, index updated, rationale in PR.
