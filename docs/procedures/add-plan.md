# Procedure: Add Plan

## Purpose
Create a plan document — either a lightweight working plan or a formal versioned project plan — in `plans/`.

> **Plans are derived, never assumed.** A formal plan does not invent work — it sequences work that
> the artifact, architecture, specs, ADRs, and research have already established. Every milestone and
> task must trace back to a source artifact. If you find yourself planning work that no spec or
> decision supports, stop: the gap belongs upstream (a missing spec, ADR, or research brief), not in
> the plan.

## Trigger
Use this procedure when:
- Scoping work for a session or sprint (Working plan)
- Defining a multi-phase technical approach (Formal plan)
- Breaking down a large feature or migration into sequenced steps (Formal plan)
- Capturing open questions before diving into specs (Working plan)

## Inputs
Before starting, determine:
- **Type**: Working (transient scratchpad) or Formal (persistent, versioned)
- **Source artifacts**: the artifact, architecture, specs, ADRs, and research this plan is derived from
- **Goal**: what does success look like at the end of this plan?
- **Scope**: what is in and out of scope?
- **Known dependencies**: what must be true or complete before this plan can execute?

---

## Steps

### 0. Gather the source artifacts (MANDATORY for formal plans)
Before drafting, read what the plan must be derived from and list the relevant pieces:
- `docs/artifact.md` — success conditions become milestones; failure modes become risks
- `docs/architecture.md` — components and dependencies set the build order
- `docs/specs/` — each spec (and its acceptance criteria) becomes one or more tasks
- `docs/adr/` — accepted decisions constrain how the work is done
- `docs/research/` and `docs/open-questions.md` — unresolved forks become dependencies or risks

If the artifacts needed to plan a piece of work do not exist yet, do not assume them — go create the
missing spec, ADR, or research brief first, then return here. A working plan may be rougher, but a
formal plan with no sources is a guess, not a plan.

### 1. Choose the plan type

| If the plan is... | Use type |
|-------------------|----------|
| A session scratchpad, quick scope outline, or spike note | Working |
| A formal roadmap, release plan, or multi-phase migration | Formal |

All plans go in `plans/`. The `Type:` field in the file header distinguishes them.

### 2. Create the plan file

**For working plans:**
- Name: `kebab-case-description.md` or `YYYY-MM-DD-description.md`
- Example: `2024-03-15-auth-service-spike.md`

**For formal plans:**
- Name: `kebab-case-plan-title.md`
- Example: `api-rate-limiting-rollout.md`

### 3. Fill in the plan template

**Working plan template:**
```markdown
# [Plan Title]

**Date:** YYYY-MM-DD
**Type:** Working
**Status:** Active | Complete | Abandoned

## Goal
[One sentence: what are we trying to achieve or figure out?]

## Scope
- In: [what is included]
- Out: [what is excluded]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Steps / Notes
[Freeform working notes, task list, or outline]

## Outcome
[Fill this in when the plan is complete or abandoned]
```

**Formal plan template:**
```markdown
# [Plan Title]

**Date:** YYYY-MM-DD
**Type:** Formal
**Author:** [name or "Agent"]
**Status:** Draft | Active | Complete | Superseded

## Goal

[What does success look like at the end of this plan? Make it measurable.
Derive this from the artifact's success conditions — do not invent a new goal here.]

## Derived From

[The artifacts this plan sequences. Every milestone and task below must trace to one of these.]
- Artifact: [docs/artifact.md](../artifact.md) — success conditions and failure modes
- Architecture: [docs/architecture.md](../architecture.md) — components and build order
- Specs: [FEAT-001](../specs/FEAT-001-...md), [DATA-001](../specs/DATA-001-...md)
- ADRs: [adr/NNNN-title.md](../adr/NNNN-title.md)
- Research: [research/file.md](../research/file.md)

## Scope

**In scope:**
- [Item — traceable to a spec or success condition]

**Out of scope:**
- [Item — often a spec's Non-Goals, or work deferred to a later plan]

## Dependencies

- [What must be true or done before this plan begins?]
- Open questions that gate this plan: [open-questions.md](../open-questions.md) — Q-N

## Risks

[Derive from the artifact's failure modes and open questions; add plan-specific risks as needed.]
- Risk: [description] → Mitigation: [approach]

## Milestones

[Each milestone advances a success condition and is built from specs. The Source column makes the
derivation explicit — a milestone with no source does not belong in the plan.]

| # | Milestone | Source (spec / §, architecture, success condition) | Success Signal |
|---|-----------|---------------------------------------------------|----------------|
| 1 | [Name] | [e.g. FEAT-001, artifact success condition #2] | [How you know it's done] |
| 2 | [Name] | [e.g. DATA-001, architecture §2] | [How you know it's done] |

## Tasks by Milestone

[Each task traces to a spec's acceptance criteria or an architecture component.]

### Milestone 1: [Name]
- [ ] Task 1 (→ FEAT-001 §6.1.A)
- [ ] Task 2

### Milestone 2: [Name]
- [ ] Task 1 (→ DATA-001 §3.1.A)
- [ ] Task 2

## Open Questions

- [ ] [Question that must be resolved before or during execution]

## Change Log

| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial draft | [name] |
```

### 4. Update the folder index
1. Open `plans/README.md`.
2. Add a row to the Index table with the file name, type, description, and status.

---

## Outputs
- A new file in `plans/`
- Updated index in `plans/README.md`

## Checklist
- [ ] `Type:` field is set (Working or Formal)
- [ ] (Formal) A **Derived From** section lists the source artifacts
- [ ] Every milestone names its source (spec / architecture / success condition)
- [ ] Every task traces to a spec's acceptance criteria or an architecture component
- [ ] No milestone or task plans work that no spec, ADR, or decision supports
- [ ] Goal is derived from the artifact's success conditions, not invented
- [ ] Scope explicitly states what is out of scope
- [ ] Dependencies and gating open questions are listed and linked
- [ ] Index row added to the folder README

## Related
- Skill: `skills/create-plan.md`
- Procedure: `procedures/add-research.md` (plans should reference prior research)
- Procedure: `procedures/add-spec.md` (plans often spawn specs)
- Procedure: `procedures/add-adr.md` (plans often surface decisions that need ADRs)
