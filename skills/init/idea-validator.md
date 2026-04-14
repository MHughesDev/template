# skills/init/idea-validator.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/init/idea-validator.py -->
<!-- - Related procedure: docs/procedures/validate-idea-md.md -->

**Purpose:** [FULL SKILL] Validate idea.md completeness and consistency before initialization. Uses idea-validator.py machinery. Per spec §28.7 item 329.

## Purpose

One paragraph. This skill prevents partial or inconsistent idea.md files from being fed to the initialization agent, which would result in a half-configured repository. Every required section must have real content (not placeholder HTML comments), internal consistency (entities match contexts), and archetype-profile alignment.

## When to Invoke

- First step of every initialization attempt (mandatory)
- When any section of idea.md is updated post-initialization
- Before re-running any initialization phase

## Prerequisites

idea.md exists. Python 3.12+ available. The human who filled out idea.md has confirmed it's ready.

## Relevant Files/Areas

idea.md (root), skills/init/idea-validator.py, docs/procedures/validate-idea-md.md

## Step-by-Step Method

Numbered steps:
1. Run `make idea:validate` which calls `scripts/validate-idea.sh`
2. Review the validation report: per-section pass/fail
3. For each FAILING section: the specific requirement that isn't met
4. Return to human with the failing section list — do NOT proceed with initialization
5. If all sections pass: proceed to archetype-mapper.md (next skill in sequence)

## Command Examples

- `make idea:validate` — run validation
- `python skills/init/idea-validator.py idea.md` — direct validation

## Validation Checklist

- [ ] All 17 sections present
- [ ] No HTML comment placeholders remaining (<!-- ... -->)
- [ ] Project identity fields filled (name, display name, pitch)
- [ ] Archetype selected (exactly one checkbox)
- [ ] At least one bounded context in §4.2
- [ ] Profile selections filled (yes/no for each)
- [ ] Archetype-profile consistency verified
- [ ] At least one queue item in §12
- [ ] No open questions in §16 that block initialization

## Common Failure Modes

- **Placeholder HTML comments remaining**: most common. Fix: grep idea.md for "<!--" and fill remaining sections.
- **Multiple archetypes selected**: Fix: select exactly one.
- **Entity not in any context**: entity in §4.1 but not assigned to a context in §4.2. Fix: assign each entity to one context.

## Handoff Expectations

Validation report produced. Either: all-pass → proceed to archetype-mapper.md, or: failures listed → return to human.

## Related Procedures

docs/procedures/validate-idea-md.md

## Related Prompts

prompts/repo_initializer.md

## Related Rules

.cursor/rules/initialization.md (pre-initialization requirements)

## Machinery

`skills/init/idea-validator.py` — parses idea.md, checks each section for completeness and consistency, produces per-section validation report. Invoke: `python skills/init/idea-validator.py idea.md` or `make idea:validate`.
