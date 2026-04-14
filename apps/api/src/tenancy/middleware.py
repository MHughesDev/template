# apps/api/src/tenancy/middleware.py
"""
BLUEPRINT: apps/api/src/tenancy/middleware.py

PURPOSE:
Tenant context middleware. Extracts tenant ID from the JWT claims, sets it
on request.state for downstream dependencies. All tenant-scoped queries
use request.state.tenant_id via the require_tenant dependency.
Per spec §26.8 item 226.

DEPENDS ON:
- starlette.middleware.base — BaseHTTPMiddleware
- fastapi — Request
- jose — jwt (for lightweight claim extraction without full auth)
- apps.api.src.config — settings

DEPENDED ON BY:
- apps.api.src.main — registered as middleware when MULTI_TENANCY_ENABLED=true
- apps.api.src.auth.dependencies — require_tenant reads request.state.tenant_id

CLASSES:

  TenantContextMiddleware(BaseHTTPMiddleware):
    PURPOSE: Extract tenant_id from JWT and set on request.state.
    FIELDS:
      - settings: Settings — JWT config for lightweight claim extraction
    METHODS:
      - dispatch(request: Request, call_next) -> Response
        STEPS:
          1. Extract Authorization header
          2. If present: decode JWT (lightweight — no signature verify, claims extraction only)
          3. Set request.state.tenant_id = claims.get("tenant_id")
          4. If no auth or no tenant claim: request.state.tenant_id = None
          5. Call next middleware
    NOTES:
      - Does NOT authenticate: that's auth/dependencies.py get_current_user
      - Does NOT raise on missing tenant: routes that need tenant use require_tenant dep
      - Lightweight JWT decode: no signature verify here (auth dep does full verify)

DESIGN DECISIONS:
- Set request.state.tenant_id = None if no token: routes decide if tenant is required
- Lightweight decode: avoid duplicate signature verification in middleware + dependency
- Only active when settings.multi_tenancy_enabled = True: zero overhead for single-tenant
- Claims extraction (not full auth): middleware is not the auth gate; dependencies are
"""
