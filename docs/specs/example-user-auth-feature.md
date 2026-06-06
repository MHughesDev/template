# Example Spec — Delete This File After Reading

> This file exists to show the format. Replace it with your own specs.

---

# Spec: User Authentication Flow

**Type:** Feature
**Status:** Approved
**Date:** 2024-03-10
**Author:** Agent

## Related
- ADR: [adr/0001-example-use-clerk-for-auth.md](../adr/0001-example-use-clerk-for-auth.md)
- Research: [research/example-auth-provider-comparison.md](../research/example-auth-provider-comparison.md)
- Plan: [plans/example-task-management-app.md](../plans/example-task-management-app.md)

---

## Overview

Defines how users sign up, log in, and access their workspace in the task management app.
Authentication is handled by Clerk. This spec covers the user-facing flows only —
the workspace data model is covered in a separate data spec.

## Goals

- Let users create an account and reach their workspace in under 2 minutes
- Support email/password and Google OAuth at launch
- Enforce workspace isolation — a user can only see workspaces they belong to

## Non-Goals (Out of Scope)

- SSO / SAML enterprise login (post-launch)
- Passwordless / magic link login (post-launch)
- Session management internals (handled by Clerk — not owned by this app)

---

## User Stories

### Sign Up
**As a** new user  
**I want to** create an account with my email or Google  
**So that** I can access my workspace and start using the app

### Log In
**As a** returning user  
**I want to** log in with my email/password or Google  
**So that** I can resume my work

### Workspace Access
**As a** logged-in user  
**I want to** land on my workspace dashboard after login  
**So that** I can immediately see my tasks

---

## Behavior

### Happy Path — Email Sign Up
1. User visits `/sign-up`
2. User enters email and password and submits
3. Clerk sends a verification email
4. User clicks verification link
5. App creates a default workspace for the user
6. User is redirected to their workspace dashboard

### Happy Path — Google OAuth
1. User clicks "Continue with Google"
2. Google OAuth consent screen appears
3. User grants permission
4. App creates a workspace if first login; skips if returning user
5. User is redirected to their workspace dashboard

### Edge Cases
- **Email already registered:** Show "An account with this email already exists. Log in instead." Link to `/login`
- **Google account previously used for email sign-up:** Merge accounts via Clerk's account linking
- **Verification email not received:** Show resend link after 60 seconds

### Error States
- **Clerk API unavailable:** Show "Sign-in is temporarily unavailable. Try again in a moment." Do not expose internal error.
- **Invalid credentials:** Show "Incorrect email or password." after 1 failed attempt; add 30s lockout after 5 consecutive failures

---

## Acceptance Criteria

- [ ] AC-1: A new user can complete email sign-up and reach their workspace in under 2 minutes on a standard connection
- [ ] AC-2: A new user can sign up via Google OAuth with no form fields required
- [ ] AC-3: A logged-in user cannot access any route belonging to a workspace they are not a member of (returns 403)
- [ ] AC-4: After 5 consecutive failed login attempts, the account is locked for 30 seconds
- [ ] AC-5: The "email already registered" error message appears within 1 second of form submission

---

## Open Questions

- [ ] Should workspace creation on first login be automatic or prompted? (current spec assumes automatic)

## Assumptions

- Clerk handles all session token issuance, storage, and rotation
- The app trusts Clerk's authentication state and does not implement its own session layer
