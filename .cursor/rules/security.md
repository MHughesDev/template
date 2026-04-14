---
alwaysApply: true
description: Security invariants. No secrets in code, token handling rules, tenant isolation checks, dependency review triggers.
---

# .cursor/rules/security.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §12 (Anti-patterns), PYTHON_PROCEDURES.md §9 (Error Policy) -->
<!-- - Skills: skills/security/secret-handling.md, skills/security/rbac-tenant-isolation.md -->
<!-- - Procedures: docs/procedures/validate-change.md (security:scan step) -->

> PURPOSE: Security invariants enforced on every agent interaction. Covers secret sourcing, JWT validation requirements, tenant context propagation, and prohibited patterns. Per spec §26.2 item 13.

## Section: Secret Sourcing Rules

> CONTENT: Rules for how secrets are sourced and handled. Rules:
> 1. Secrets are ONLY read from environment variables via Pydantic `BaseSettings` in `apps/api/src/config.py`
> 2. NEVER hardcode any secret, credential, API key, token, or password in any file — including tests
> 3. Test secrets use fixed test values defined in `conftest.py` with clearly fake values (not real format)
> 4. `.env.example` documents every secret with a `CHANGEME-*` placeholder — never real values
> 5. `scripts/secret-scanner.py` and `.pre-commit-config.yaml` enforce this on every commit
> 6. If a secret is accidentally committed: STOP, rotate immediately, document in `docs/security/incident-response.md`

## Section: JWT Validation Requirements

> CONTENT: Rules for JWT token handling. Rules:
> 1. JWT tokens MUST be validated on every protected endpoint via `Depends(get_current_user)`
> 2. Token validation MUST check: signature, expiry, issuer, audience (if applicable)
> 3. Access tokens expire in `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` (from config, not hardcoded)
> 4. Refresh tokens expire in `JWT_REFRESH_TOKEN_EXPIRE_DAYS` (from config)
> 5. Token revocation is tracked in the database (RefreshToken model); check `revoked` field on refresh
> 6. NEVER log JWT token values — log `user_id` and `tenant_id` from claims instead
> 7. Key rotation procedure is documented in `docs/runbooks/jwt-key-rotation.md`

## Section: Tenant Context Propagation

> CONTENT: Rules for multi-tenancy enforcement. Rules:
> 1. Tenant ID is extracted from the JWT claims by `TenantContextMiddleware` in `apps/api/src/tenancy/middleware.py`
> 2. All database queries on tenant-scoped models MUST include `.where(Model.tenant_id == tenant_id)` — use `TenantMixin` to enforce this
> 3. NEVER assume a user has access to resources of another tenant — always filter by `request.state.tenant_id`
> 4. Cross-tenant operations (admin-only) MUST be explicitly gated by an admin role check, not just auth check
> 5. Integration tests for tenant isolation live in `apps/api/tests/test_tenancy.py` — these MUST pass before PR merge
> 6. `skills/security/tenant-isolation-checker.py` validates tenant isolation statically

## Section: Dependency Review Triggers

> CONTENT: Rules for when dependency review is required. Rules:
> 1. Any change to `pyproject.toml` requires running `make security:scan` before merge
> 2. Dependabot PRs require human review of the changelog and CVE check before auto-merge is enabled
> 3. New direct dependencies require documentation in `docs/development/dependency-management.md`
> 4. Dependencies with known CVEs are only accepted via the `docs/security/accepted-risks.md` process
> 5. Pin versions for security-critical packages (cryptography, python-jose, passlib)

## Section: Prohibited Patterns

> CONTENT: Security anti-patterns that are NEVER acceptable. Rules:
> 1. NEVER use raw SQL string concatenation — always use parameterized queries via SQLAlchemy ORM
> 2. NEVER disable authentication on non-test endpoints (no `skip_auth=True` outside of test configuration)
> 3. NEVER expose stack traces to API clients — use structured error responses only
> 4. NEVER use `DEBUG=true` in production (enforced by config validation)
> 5. NEVER store passwords in plaintext — always use `passlib` hashing with bcrypt
> 6. NEVER use `eval()`, `exec()`, or `pickle` on user-controlled input
> 7. NEVER use MD5 or SHA1 for cryptographic purposes (use SHA-256 or better)
> 8. NEVER log user passwords, raw JWT tokens, or API keys at any log level
