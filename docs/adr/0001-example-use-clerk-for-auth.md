# Example ADR — Delete This File After Reading

> This file exists to show the format. Replace it with your own ADRs.

---

# ADR-0001: Use Clerk for Authentication

**Status:** Accepted
**Date:** 2024-03-08
**Deciders:** Engineering team

## Context

The task management app requires multi-tenant authentication with workspace isolation.
The team is two engineers with a 6-month launch timeline. Authentication needs to support
email/password and Google OAuth at minimum, with enterprise SSO possible post-launch.

Three options were evaluated: Auth0, Clerk, and a custom JWT implementation.
See [research/example-auth-provider-comparison.md](../research/example-auth-provider-comparison.md) for the full analysis.

## Decision

Use Clerk for authentication and session management.

## Rationale

Clerk integrates with the Next.js stack in approximately 2 days (verified by a proof of concept),
supports multi-tenant Organizations natively, and is free up to 10,000 MAU — covering the entire
beta period. The team does not have bandwidth to build and maintain a custom auth system without
sacrificing core product features.

## Consequences

**Positive:**
- Auth integration takes days, not weeks, freeing the team to focus on product
- Multi-tenancy and session security are handled by a maintained third-party service
- SOC 2 Type II compliance is inherited from Clerk (pending confirmation for EU data residency)

**Negative:**
- Vendor dependency — migrating away from Clerk later would require reworking all auth flows
- Pricing increases significantly at 100k+ MAU (~$350/month) versus $0 for custom
- Less control over session behavior, token format, and revocation granularity

**Neutral:**
- Clerk's APIs are documented but not stable across major versions — upgrades require attention

## Alternatives Considered

### Option A: Auth0
Mature platform with enterprise features, but $240/month minimum for multi-tenancy,
and integration is significantly more verbose than Clerk. Rejected for timeline and cost reasons.

### Option B: Custom JWT Implementation
Maximum flexibility and zero recurring cost, but estimated 3–5 weeks of implementation time
for a secure, production-grade auth system. Rejected — the team cannot afford to spend that
time before the product is built.

## References

- Research: [research/example-auth-provider-comparison.md](../research/example-auth-provider-comparison.md)
- Spec: [specs/FEAT-001-user-authentication.md](../specs/FEAT-001-user-authentication.md)
