---
doc_id: "16.8"
title: "threat model"
section: "Security"
status: "pending-init"
summary: "Project-specific top threats, mitigations, accepted residual risks, out-of-scope threats. Populated during initialization from IDEA.md §14."
updated: "2026-05-17"
---

# Threat Model
<!-- derived from: IDEA.md §14 — populated by repo_initialize -->

## Top threats

| Threat | Severity | Mitigation | Status |
|--------|----------|------------|--------|
| _[e.g., SQL Injection]_ | High | _[Parameterized queries]_ | Mitigated |
| _[e.g., XSS]_ | Medium | _[Output encoding]_ | Mitigated |

## Accepted risks

| Risk | Rationale | Review date |
|------|-----------|-------------|
| _[e.g., No WAF in v1]_ | _[Cost/complexity]_ | _[2026-06-01]_ |

## Out of scope

_[Threats explicitly not addressed in v1]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
