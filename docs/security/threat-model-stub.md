# docs/security/threat-model-stub.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/security/README.md, AGENTS.md §11 (Escalation) -->

**Purpose:** Generic threat model for FastAPI applications built on this template. Identifies assets, threat actors, attack surfaces, and mitigations. Customise per deployment in §9.

## 1. Assets

| Asset | Classification | Location |
|-------|---------------|----------|
| User credentials (hashed passwords, tokens) | Critical | Database — `users` table |
| JWT signing secret (`SECRET_KEY`) | Critical | Environment variable — never in code |
| Database connection string (`DATABASE_URL`) | Critical | Environment variable |
| API keys to third-party services (Stripe, SendGrid) | Critical | Environment variables |
| Tenant data (rows scoped by `tenant_id`) | High | Database — all tenant-partitioned tables |
| PII (email, name, address) | High | Database — `users` + profile tables |
| Application source code | Medium | Git — protected by branch policies |
| CI/CD secrets (deployment keys, registry credentials) | Critical | GitHub Actions secrets store |
| Audit logs / queue history | Medium | `queue/queue.csv`, CI logs |

## 2. Threat actors

| Actor | Motivation | Capability |
|-------|-----------|------------|
| **Unauthenticated external attacker** | Data theft, service disruption | Script-kiddie to skilled; automated scanners |
| **Authenticated low-privilege user** | Privilege escalation, access to other tenants' data | Internal knowledge of API shape |
| **Compromised tenant admin** | Lateral movement across tenants | API access + social engineering |
| **Malicious dependency (supply chain)** | Backdoor, credential theft, data exfiltration | Transitive npm/PyPI package |
| **Insider (developer/agent)** | Accidental data leak, misconfig | Direct repo and infra access |
| **Automated scanner** | Exploit known CVEs, brute force | High volume, low precision |

## 3. Attack surfaces

### 3.1 HTTP API (FastAPI)

| Surface | Risk | Relevant mitigations |
|---------|------|---------------------|
| Authentication endpoints (`/auth/token`, `/auth/register`) | Credential stuffing, brute force | Rate limiting (see §4); account lockout |
| All authenticated routes | JWT forgery, token replay | Short-lived tokens (15 min); refresh token rotation |
| Tenant-scoped routes (`/api/v1/{resource}`) | Horizontal privilege escalation (tenant A reads tenant B) | `tenant_id` claim in JWT; query filter on every repo method |
| File upload endpoints (if enabled) | Malicious file, path traversal | Allowlist MIME types; store outside web root; virus scan |
| Admin-only routes | Vertical privilege escalation | `is_superuser` / role check; separate admin prefix |
| CORS-unprotected origins | Cross-site request forgery | `API_CORS_ORIGINS` env var; never `*` in prod (see `docs/security/cors-policy.md`) |
| OpenAPI schema (`/docs`, `/openapi.json`) | Information disclosure | Disable in production via `DISABLE_DOCS=true` env var |

### 3.2 Database

| Surface | Risk | Mitigation |
|---------|------|-----------|
| ORM queries | SQL injection (low risk with SQLAlchemy; still possible with raw `text()`) | Never use `text()` with user input unparameterised |
| Connection string in env | Credential exposure | Rotate on suspected compromise; use managed secrets (AWS SM, GCP SM) |
| Migrations (Alembic) | Accidental data destruction | Dry-run in CI (`make ci-migrate-dry-run`); backup before prod migration |
| Direct DB access from CI | Credential leakage in logs | Use read-only CI user; never log connection strings |

### 3.3 Authentication & session

| Surface | Risk | Mitigation |
|---------|------|-----------|
| JWT `SECRET_KEY` | Token forgery if leaked | ≥ 32 random bytes; rotate quarterly; stored only in env |
| Refresh token storage | Token theft from client storage | HttpOnly cookie or SecureStore (mobile); never localStorage |
| Password storage | Rainbow table, credential stuffing | bcrypt with `rounds ≥ 12` (enforced in `auth/service.py`) |
| Password reset flow | Token enumeration | Constant-time comparison; short TTL (15 min) |

### 3.4 Infrastructure & CI/CD

| Surface | Risk | Mitigation |
|---------|------|-----------|
| GitHub Actions secrets | Exfiltration via malicious PR | No secrets in pull_request_target triggers; environment protection rules |
| Docker image | Dependency CVEs; secrets baked in | Multi-stage build (no dev deps in prod image); no COPY of `.env` |
| Third-party actions | Supply chain compromise | Pin to SHA (`uses: actions/checkout@abc1234`); audit quarterly |
| Container registry | Image tampering | Use digest pinning in production deployments |

### 3.5 Dependencies (PyPI / npm)

| Surface | Risk | Mitigation |
|---------|------|-----------|
| Transitive Python packages | CVE exploit, typosquat | `pip-audit` in CI; `dependabot` alerts enabled |
| Frontend npm packages | Prototype pollution, XSS via bundled code | `npm audit`; lock file committed |

## 4. Mitigations inventory

| Mitigation | Status | Implementation location |
|-----------|--------|------------------------|
| JWT authentication | Implemented | `apps/api/src/auth/` |
| Tenant isolation via `tenant_id` | Implemented | All repository methods + JWT claim |
| bcrypt password hashing (`rounds=12`) | Implemented | `apps/api/src/auth/service.py` |
| CORS origin allowlist | Implemented | `settings.api_cors_origins` → FastAPI middleware |
| Rate limiting on auth endpoints | **Required** | Add `slowapi` or NGINX rate limiting in deployment |
| Input validation (Pydantic schemas) | Implemented | All request schemas in `*/schemas.py` |
| SQL parameterisation (SQLAlchemy ORM) | Implemented | ORM queries only; raw `text()` prohibited |
| Secrets via env vars only | Implemented | `.env.example` documents all vars; `.env` in `.gitignore` |
| Multi-stage Docker build | Implemented | `Dockerfile` — `builder` + `runtime` stages |
| Alembic migration dry-run in CI | Implemented | `.github/workflows/ci.yml` → `ci-migrate-dry-run` |
| OpenAPI docs disabled in prod | **Required** | Set `DISABLE_DOCS=true` in production env |
| `pip-audit` in CI | **Required** | Add `pip-audit` step to CI workflow |
| Action SHA pinning | **Required** | Audit `.github/workflows/` and pin third-party actions |

**Required** mitigations are not yet implemented and must be completed before production deployment.

## 5. Data flow diagram (simplified)

```
Browser / Mobile App
        │  HTTPS
        ▼
   Load Balancer (TLS termination)
        │  HTTP (internal)
        ▼
   FastAPI container  ──── JWT validation ──── Redis (token denylist, optional)
        │
        ├── SQLAlchemy ORM ──► PostgreSQL (prod) / SQLite (dev/test)
        │
        ├── Stripe SDK ──────► Stripe API (billing profile only)
        │
        └── SendGrid / SMTP ► Email provider (notifications profile only)
```

All external calls use HTTPS. Internal services communicate over the private network only.

## 6. Security boundaries

1. **Authentication boundary** — every route behind `Depends(get_current_user)` requires a valid JWT.
2. **Tenant boundary** — every DB query filters by `tenant_id` extracted from the JWT; cross-tenant reads are a P0 security bug.
3. **Admin boundary** — routes under `/api/v1/admin/` require `current_user.is_superuser == True`.
4. **Infrastructure boundary** — the DB is not publicly accessible; only the API container has a DB connection.

## 7. Incident response

See `docs/security/incident-response.md` for the full incident response playbook.

**Quick escalation path:**
1. Detect anomaly (unusual query volume, auth failures, unknown tenant access).
2. Rotate affected secrets immediately (JWT key, DB password).
3. Revoke all active tokens (flush Redis denylist or change `SECRET_KEY`).
4. Preserve logs before any remediation that would overwrite them.
5. File a P0 incident issue; notify maintainers.

## 8. Accepted risks

Risks accepted with rationale are documented in `docs/security/accepted-risks.md`. Review quarterly or after any significant architectural change.

## 9. Deployment-specific customisation

This is a **template** threat model. When deploying for a real project, add:

- Specific IP allowlists for admin access.
- Third-party services introduced by enabled profiles (e.g., Stripe endpoints for billing).
- Infrastructure-specific surfaces (AWS S3 bucket policies, GCP IAM).
- Compliance requirements (SOC 2, GDPR, HIPAA) that constrain mitigations.
- Penetration test findings and their remediation status.

Update this file as part of the post-initialization PR (after `make idea:execute`).
