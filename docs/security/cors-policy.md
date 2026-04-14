# docs/security/cors-policy.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- Optional per spec §26.12 item 403 -->

> PURPOSE: CORS origins and security rationale. Per spec §26.12 item 403.

## CORS Configuration

> CONTENT: Allowed origins are defined in settings.api_cors_origins (env var API_CORS_ORIGINS). Never "*" in production. Local dev: http://localhost:3000, http://localhost:8000.

## Security Rationale

> CONTENT: Why we restrict CORS: prevent cross-origin requests from malicious sites. Allow credentials=True: needed for cookie-based auth if ever implemented. Allowed methods and headers list.

## Per-Environment Settings

> CONTENT: Dev: permissive (multiple localhost origins). Staging: staging domain only. Prod: production domain(s) only.
