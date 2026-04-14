# SECURITY.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: README.md, docs/security/README.md, .github/CODEOWNERS -->
<!-- - Links to: docs/security/incident-response.md, docs/security/secrets-management.md -->

> PURPOSE: Public vulnerability disclosure policy for GitHub Security tab. Tells security researchers how to report vulnerabilities. Required by spec §26.12 item 362. Referenced by GitHub's Security Advisories feature.

## Supported Versions

> CONTENT: Table showing which versions receive security updates. Columns: Version, Supported. Use semver ranges (e.g., >= 1.0.0 = :white_check_mark:, < 1.0.0 = :x:). At template initialization, this will list only the current version. Updated with each major release.

## Reporting a Vulnerability

> CONTENT: Clear, actionable instructions for reporting vulnerabilities. Key points:
>
> 1. **Do NOT** open a public GitHub issue for security vulnerabilities
> 2. Use GitHub's Security Advisory feature: "Report a vulnerability" button in the Security tab
> 3. Alternative: email security contact at {{SECURITY_EMAIL}} (filled during initialization)
> 4. Include in your report: description of the vulnerability, steps to reproduce, potential impact, suggested fix if any
> 5. Expected response time: acknowledgment within 48 hours, status update within 7 days
> 6. Responsible disclosure: please allow 90 days for remediation before public disclosure
>
> Placeholder {{SECURITY_EMAIL}} filled from idea.md during initialization.

## Security Policy

> CONTENT: Brief summary of the project's security stance. Key points:
> - Secrets are never stored in the repository (env vars only, enforced by CI secret scanning)
> - Dependencies are reviewed for CVEs via Dependabot and CI security scans
> - Container images are scanned with Trivy before deployment
> - JWT tokens have explicit expiry; no long-lived tokens without rotation
> - Multi-tenant data isolation is enforced at the query layer
>
> Link to `docs/security/` for detailed security documentation.

## Accepted Risks

> CONTENT: Brief note that accepted risks (known CVEs that are not fixable or are accepted) are documented in `docs/security/accepted-risks.md`. Link to that file. State that all accepted risks have a review date and justification.
