# Example Formal Plan — Delete This File After Reading

> This file exists to show the format. Replace it with your own plan.

---

# Task Management App — Launch Plan

**Date:** 2024-03-05
**Type:** Formal
**Author:** Agent
**Status:** Draft

## Goal

Ship a working multi-tenant task management app to the first 10 paying customers within 6 months,
with core task creation, assignment, and completion tracking functional at launch.

## Scope

**In scope:**
- User authentication and multi-tenant workspace management
- Task creation, assignment, status tracking, and archiving
- Email notifications for task assignment and due-date reminders

**Out of scope:**
- Mobile apps (web only at launch)
- Time tracking and billing integrations
- Public API for third-party integrations

## Dependencies

- Auth provider selected and integrated → see [research/example-auth-provider-comparison.md](../research/example-auth-provider-comparison.md)
- Database schema for tasks and workspaces finalized before Milestone 2

## Risks

- **Risk:** Auth provider integration takes longer than estimated → **Mitigation:** 2-day Clerk POC already completed; spike time is known
- **Risk:** Multi-tenancy data isolation has a bug at launch → **Mitigation:** Separate test workspace with synthetic data in pre-launch QA
- **Risk:** Team bandwidth — 2 engineers, 6 months → **Mitigation:** No mobile; launch feature set is strictly scoped above

## Milestones

| # | Milestone | Description | Success Signal |
|---|-----------|-------------|----------------|
| 1 | Auth + Workspaces | User sign-up, login, workspace creation and switching | A user can create a workspace and invite one teammate |
| 2 | Core Task Flow | Task create, assign, status update, archive | A user can create a task, assign it, and mark it complete |
| 3 | Notifications | Email on assignment and due-date reminder | Assigned user receives email within 60 seconds |
| 4 | Beta Launch | Onboard 3 pilot customers | 3 workspaces active with real tasks |
| 5 | Paid Launch | First 10 paying customers | 10 active paid workspaces |

## Tasks by Milestone

### Milestone 1: Auth + Workspaces
- [ ] Integrate Clerk with Next.js app
- [ ] Implement workspace creation flow
- [ ] Implement workspace switching in nav
- [ ] Write workspace data spec
- [ ] Write auth integration ADR

### Milestone 2: Core Task Flow
- [ ] Design and implement tasks schema
- [ ] Build task creation UI
- [ ] Build task assignment UI
- [ ] Build task list and status filter views
- [ ] Write task feature spec

### Milestone 3: Notifications
- [ ] Choose email provider (research brief needed)
- [ ] Implement assignment notification trigger
- [ ] Implement due-date reminder scheduled job

### Milestone 4: Beta Launch
- [ ] Onboard pilot customers manually
- [ ] Bug bash based on pilot feedback

### Milestone 5: Paid Launch
- [ ] Integrate Stripe for subscription billing
- [ ] Launch marketing page

## Open Questions

- [ ] Which email provider should we use? (→ research brief needed)
- [ ] What is the data retention policy for archived tasks?

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2024-03-05 | Initial draft | Agent |
