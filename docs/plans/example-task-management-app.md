# Example Formal Plan — Delete This File After Reading

> This file exists to show the format. Replace it with your own plan.

---

# Task Management App — Launch Plan

**Date:** 2024-03-05
**Type:** Formal
**Author:** Agent
**Status:** Draft
**Derivation Status:** Current

## Goal

Ship a working multi-tenant task management app to the first 10 paying customers within 6 months,
with core task creation, assignment, and completion tracking functional at launch.
(Derived from the artifact's success conditions.)

## Derived From

This plan sequences work already established in the following artifacts — it invents nothing:
- Artifact: [docs/artifact.md](../artifact.md) — success conditions (launch, core task flow) and failure modes
- Architecture: [docs/architecture.md](../architecture.md) — auth → workspaces → tasks → notifications build order
- Specs: [FEAT-001 User Authentication](../specs/FEAT-001-user-authentication.md) (and pending `DATA-001`, `FEAT-002`)
- ADR: [adr/0001-example-use-clerk-for-auth.md](../adr/0001-example-use-clerk-for-auth.md)
- Research: [research/example-auth-provider-comparison.md](../research/example-auth-provider-comparison.md)

## Scope

**In scope:**
- User authentication and multi-tenant workspace management (FEAT-001)
- Task creation, assignment, status tracking, and archiving (FEAT-002, DATA-001 — pending)
- Email notifications for task assignment and due-date reminders

**Out of scope:**
- Mobile apps (web only at launch — see FEAT-001 §2.2)
- Time tracking and billing integrations
- Public API for third-party integrations

## Dependencies

- Auth provider selected and integrated → [adr/0001-example-use-clerk-for-auth.md](../adr/0001-example-use-clerk-for-auth.md)
- `DATA-001` tasks/workspaces schema must be written and approved before Milestone 2
- Open questions gating this plan: [open-questions.md](../open-questions.md) — Q-1 (resolved), email provider (open)

## Risks

(Derived from the artifact's failure modes and open questions.)
- **Risk:** Auth integration takes longer than estimated → **Mitigation:** 2-day Clerk POC already completed; spike time is known
- **Risk:** Multi-tenancy data isolation has a bug at launch → **Mitigation:** Synthetic-data test workspace in pre-launch QA (traces to FEAT-001 §3.1.C)
- **Risk:** Team bandwidth — 2 engineers, 6 months → **Mitigation:** No mobile; scope strictly bounded above

## Milestones

| # | Milestone | Source (spec / architecture / success condition) | Success Signal |
|---|-----------|--------------------------------------------------|----------------|
| 1 | Auth + Workspaces | FEAT-001; architecture §2 (foundational) | A user can create a workspace and invite one teammate |
| 2 | Core Task Flow | FEAT-002, DATA-001; artifact success condition "core task flow" | A user can create a task, assign it, and mark it complete |
| 3 | Notifications | FEAT-003 (pending); artifact "assignment reminders" | Assigned user receives email within 60 seconds |
| 4 | Beta Launch | artifact success condition "first pilot customers" | 3 workspaces active with real tasks |
| 5 | Paid Launch | artifact success condition "10 paying customers" | 10 active paid workspaces |

## Tasks by Milestone

### Milestone 1: Auth + Workspaces
- `NOT STARTED` Integrate Clerk with the app (→ FEAT-001 §5.1)
- `NOT STARTED` Implement default workspace creation on first login (→ FEAT-001 §3.1.B)
- `NOT STARTED` Enforce workspace membership access control (→ FEAT-001 §3.1.C / §6.1.C)
- `NOT STARTED` Write `DATA-001` workspace schema spec (→ architecture §2 — missing source, create before Milestone 2)

### Milestone 2: Core Task Flow
- `NOT STARTED` Write `FEAT-002` task feature spec and `DATA-001` tasks schema (→ artifact success condition "core task flow" — sources must exist first)
- `NOT STARTED` Implement task create / assign / status / archive (→ FEAT-002 §6.1 — blocked on FEAT-002 spec)
- `NOT STARTED` Build task list and status filter views (→ FEAT-002 §6.1 — blocked on FEAT-002 spec)

### Milestone 3: Notifications
- `NOT STARTED` Research and choose an email provider (→ open-questions.md Q-2 — write research brief first)
- `NOT STARTED` Write `FEAT-003` notifications spec, then implement against it (→ artifact "assignment reminders" — blocked on email research)

### Milestone 4: Beta Launch
- `NOT STARTED` Onboard pilot customers manually (→ artifact success condition "first pilot customers") `BLOCKED:HUMAN` — requires manual customer outreach
- `NOT STARTED` Bug bash against each spec's acceptance criteria (→ FEAT-001 §6.1, FEAT-002 §6.1) `BLOCKED:TESTING` — requires running application

### Milestone 5: Paid Launch
- `NOT STARTED` Write `INTG-001` Stripe billing spec, then integrate (→ artifact success condition "10 paying customers")
- `NOT STARTED` Launch marketing page (→ artifact success condition "10 paying customers") `BLOCKED:HUMAN` — requires content approval

## Open Questions

- [ ] Which email provider should we use? (→ research brief needed)
- [ ] What is the data retention policy for archived tasks?

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2024-03-05 | Initial draft | Agent |
