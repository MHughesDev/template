# Example Research Brief — Delete This File After Reading

> This file exists to show the format. Replace it with your own research.

---

# Auth Provider Comparison: Auth0 vs. Clerk vs. Roll Our Own

**Date:** 2024-03-01
**Researcher:** Agent
**Status:** Complete

## Question

Which authentication provider best fits a B2B SaaS app with multi-tenant requirements,
a two-person team, and a hard 6-month launch timeline?

## Scope

**In scope:**
- Auth0, Clerk, and a custom JWT implementation
- Multi-tenancy support, developer ergonomics, pricing at scale, migration risk

**Out of scope:**
- SSO-only enterprise solutions (Okta, OneLogin) — out of budget for initial launch
- Passwordless-only approaches — email/password is a launch requirement

## Method

- Read official documentation for Auth0 (Nov 2023), Clerk (Feb 2024), and OWASP JWT guidance
- Reviewed pricing calculators at 10k, 50k, and 100k MAU
- Tested Clerk's Next.js SDK in a 2-hour proof of concept

## Findings

### Auth0

- Mature platform with extensive docs and enterprise track record
- Multi-tenancy supported via Organizations (available on paid plans from $240/month)
- Developer experience is verbose — integration requires significant boilerplate
- Cold start time on free tier can cause latency spikes

### Clerk

- Purpose-built for modern stacks (Next.js, React, Remix) with first-class SDK support
- Multi-tenancy supported natively with Organizations
- Pricing is per-MAU with a generous free tier (10k MAU free as of Feb 2024)
- Less mature — fewer enterprise integrations, smaller community

### Roll Our Own (JWT)

- Maximum flexibility and zero recurring cost
- Significant implementation surface: token rotation, revocation, refresh flows, storage
- Two-person team would spend 3–5 weeks on auth alone before any product work
- Security risk if not implemented carefully

## Comparison Matrix

| Criterion | Auth0 | Clerk | Roll Our Own |
|-----------|-------|-------|--------------|
| Multi-tenancy | Yes (paid) | Yes (native) | Manual |
| Time to integrate | ~1 week | ~2 days | 3–5 weeks |
| Cost at 10k MAU | $240/month | $0 | $0 + dev time |
| Cost at 100k MAU | ~$1,500/month | ~$350/month | $0 + ongoing maintenance |
| Migration risk | Medium | Low | High (fully owned) |

## Recommendation

Use **Clerk** for the initial launch. The SDK integration is fast enough to fit the 6-month timeline,
multi-tenancy is built in, and pricing is manageable at early scale. Revisit Auth0 if enterprise SSO
becomes a requirement after launch.

## Open Questions

- Does Clerk's SOC 2 Type II certification satisfy the compliance requirement from the artifact?
- What is Clerk's data residency story for EU customers?

## References

- Clerk pricing: https://clerk.com/pricing
- Auth0 Organizations: https://auth0.com/docs/manage-users/organizations
- OWASP JWT Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
