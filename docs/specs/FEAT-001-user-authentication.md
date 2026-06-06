# Example Spec — Delete This File After Reading

> This file exists to show the naming convention (`FEAT-001-…`) and the numbered section format.
> Replace it with your own specs.

---

# Spec: FEAT-001 — User Authentication

**Spec ID:** FEAT-001
**Type:** Feature
**Status:** Approved
**Date:** 2024-03-10
**Author:** Agent

## 1. Overview

1.1 Purpose — Defines how users sign up, log in, and access their workspace. Authentication is handled by Clerk; this spec covers the user-facing flows only.

1.2 Context — First feature in the task management app; everything else sits behind it. The workspace data model is specified separately in `DATA-001`.

1.3 Related artifacts
   1.3.A ADR: [adr/0001-example-use-clerk-for-auth.md](../adr/0001-example-use-clerk-for-auth.md)
   1.3.B Research: [research/example-auth-provider-comparison.md](../research/example-auth-provider-comparison.md)
   1.3.C Open questions: [open-questions.md](../open-questions.md) — Q-1
   1.3.D Plan: [plans/example-task-management-app.md](../plans/example-task-management-app.md)

## 2. Scope

2.1 Goals
   2.1.A Let a user create an account and reach their workspace in under 2 minutes.
   2.1.B Support email/password and Google OAuth at launch.
   2.1.C Enforce workspace isolation — a user can only see workspaces they belong to.

2.2 Non-Goals (out of scope)
   2.2.A SSO / SAML enterprise login (post-launch).
   2.2.B Passwordless / magic-link login (post-launch).
   2.2.C Session-management internals (owned by Clerk, not this app).

## 3. Requirements

3.1 Functional requirements
   3.1.A A user can create an account using email/password or Google OAuth.
   3.1.B A verified new user is placed into a default workspace on first login.
   3.1.C A user can only access workspaces they are a member of.

3.2 Non-functional requirements
   3.2.A Repeated failed logins are rate-limited: 30-second lockout after 5 consecutive failures.
   3.2.B The "email already registered" error renders within 1 second of submission.

## 4. Interface / Data

4.1 User stories
   4.1.A As a new user, I want to create an account with email or Google, so that I can access my workspace.
   4.1.B As a returning user, I want to log in, so that I can resume my work.
   4.1.C As a logged-in user, I want to land on my workspace dashboard, so that I see my tasks immediately.

## 5. Behavior

5.1 Happy path — email sign up
   5.1.A User visits `/sign-up`, enters email and password, submits.
   5.1.B Clerk sends a verification email; user clicks the link.
   5.1.C App creates a default workspace (§3.1.B) and redirects to the dashboard.

5.2 Edge cases
   5.2.A Email already registered: show "An account with this email already exists. Log in instead." linking to `/login`.
   5.2.B Google account previously used for email sign-up: merge via Clerk account linking.
   5.2.C Verification email not received: show a resend link after 60 seconds.

5.3 Error states
   5.3.A Clerk API unavailable: show "Sign-in is temporarily unavailable. Try again in a moment." Do not expose internal errors.
   5.3.B Invalid credentials: show "Incorrect email or password." and apply the §3.2.A lockout.

## 6. Acceptance Criteria

6.1 Criteria
   6.1.A [ ] A new user completes email sign-up and reaches their workspace in under 2 minutes (verifies §3.1.A, §3.1.B).
   6.1.B [ ] A new user can sign up via Google OAuth with no form fields (verifies §3.1.A).
   6.1.C [ ] A logged-in user cannot access a workspace they are not a member of — returns 403 (verifies §3.1.C).
   6.1.D [ ] After 5 consecutive failed logins, the account is locked for 30 seconds (verifies §3.2.A).
   6.1.E [ ] The "email already registered" error appears within 1 second of submission (verifies §3.2.B).

## 7. Open Questions & Assumptions

7.1 Open questions — tracked centrally in [open-questions.md](../open-questions.md) (Q-1, auth provider — resolved).

7.2 Assumptions
   7.2.A Clerk handles all session token issuance, storage, and rotation.
   7.2.B The app trusts Clerk's auth state and does not implement its own session layer.
