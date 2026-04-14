# skills/repo-governance/writing-adrs.md

<!-- CROSS-REFERENCES -->
<!-- - Template: docs/adr/template.md -->
<!-- - Index machinery: skills/repo-governance/adr-index-generator.py -->

**Purpose:** How to author Architecture Decision Records in docs/adr/. Use template, link to relevant code and spec sections. Per spec §26.4 item 52.

## Purpose

One paragraph. ADRs document significant architectural decisions with context, alternatives considered, and consequences. They prevent re-litigating settled decisions and provide new contributors/agents with the reasoning behind the system's shape.

## When to Invoke

When making an architectural decision (choosing a framework, selecting a database, deciding on a security pattern). When deprecating a major feature. When a significant design constraint is accepted. Per AGENTS.md §8 (Documentation update requirements).

## Prerequisites

docs/adr/template.md read. docs/adr/README.md (index) read. The decision is made and rationale is clear.

## Relevant Files/Areas

docs/adr/, skills/repo-governance/adr-index-generator.py

## Step-by-Step Method

Numbered steps:
1. Determine ADR number: next sequential number from docs/adr/README.md index
2. Create docs/adr/ADR-<NNN>-<kebab-case-title>.md
3. Fill all sections from the template:
   - Title: ADR-NNN: Decision Title
   - Status: Proposed/Accepted/Deprecated/Superseded
   - Context: why this decision was needed
   - Decision: what was decided (specific and concrete)
   - Consequences: trade-offs, risks, follow-up work
   - Alternatives considered: what was rejected and why
   - References: links to relevant code, spec sections, prior ADRs
4. Run `python skills/repo-governance/adr-index-generator.py` to update docs/adr/README.md
5. PR with PR description linking to the code change that prompted the ADR

## Command Examples

`python skills/repo-governance/adr-index-generator.py`

## Validation Checklist

- [ ] All template sections filled (no TODO remaining)
- [ ] Status field set (not left blank)
- [ ] Alternatives considered (minimum 2)
- [ ] References link to relevant code/spec
- [ ] docs/adr/README.md index updated (via generator)

## Common Failure Modes

Skipping "Alternatives considered" → ADR reads as if the decision was obvious. Fix: always document at least 2 rejected alternatives with reasons.

## Handoff Expectations

ADR committed, index updated, PR linked to the implementation it governs.

## Related Procedures

docs/procedures/implement-change.md (ADR before implementation)

## Related Prompts

prompts/implementation_agent.md

## Related Rules

AGENTS.md §8 (ADR required for architectural decisions)
