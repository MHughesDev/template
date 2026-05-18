---
doc_id: "2.19"
title: "multi tenancy"
section: "Architecture"
status: "pending-init"
summary: "Isolation model, tenant context propagation, shared-vs-isolated data, tenant provisioning. Populated during initialization from IDEA.md §10 when multi-tenancy is enabled."
updated: "2026-05-17"
---

# Multi-Tenancy
<!-- derived from: IDEA.md §10 — populated by repo_initialize -->

## Isolation model

_[e.g., Row-level with tenant_id columns]_

## Tenant context propagation

_[How is tenant context passed through the system? e.g., JWT claim → middleware context → query filters]_

## Shared vs. isolated data

| Data | Type | Notes |
|------|------|-------|
| _[Entity 1]_ | Shared | _[Available to all tenants]_ |
| _[Entity 2]_ | Isolated | _[tenant_id filtered]_ |

## Tenant provisioning

_[How are new tenants created?]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization when multi-tenancy is enabled.]_
