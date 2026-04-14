# apps/api/src/auth/dependencies.py
"""
BLUEPRINT: apps/api/src/auth/dependencies.py

PURPOSE:
FastAPI dependencies for auth: get_current_user (extract and validate JWT),
require_auth (raises 401 if not authenticated), get_auth_service (factory).
Per spec §26.8 item 224.

DEPENDS ON:
- fastapi — Depends, HTTPBearer, HTTPAuthorizationCredentials, HTTPException
- sqlalchemy.ext.asyncio — AsyncSession
- apps.api.src.auth.service — AuthService
- apps.api.src.auth.models — User
- apps.api.src.dependencies — get_db, get_settings
- apps.api.src.exceptions — AuthenticationError

DEPENDED ON BY:
- apps.api.src.auth.router — uses get_current_user, get_auth_service
- apps.api.src.*/router.py — all protected routes use get_current_user
- apps.api.src.auth.__init__ — re-exports get_current_user

FUNCTIONS:

  get_auth_service(
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings)
  ) -> AuthService:
    PURPOSE: Factory dependency that creates AuthService with injected dependencies.
    STEPS: Return AuthService(session=session, settings=settings)
    RETURNS: AuthService instance

  async get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_db),
  ) -> User:
    PURPOSE: Extract and validate JWT, return current User.
    STEPS:
      1. If no credentials provided: raise AuthenticationError (401)
      2. Validate the Bearer token via service.verify_token(credentials.credentials)
      3. Extract user_id from claims
      4. Query User by user_id
      5. If not found or not active: raise AuthenticationError
      6. Return User instance
    RETURNS: User (always active — service raises if not)
    RAISES: AuthenticationError (401) for any failure

  async require_auth(
    current_user: User = Depends(get_current_user)
  ) -> User:
    PURPOSE: Alias for get_current_user. Use for explicit documentation of auth requirement.
    RETURNS: User (same as get_current_user)
    NOTES: Semantically equivalent; helps make auth requirement explicit in route signatures

  async require_tenant(
    current_user: User = Depends(get_current_user),
    request: Request = None,
  ) -> tuple[User, UUID]:
    PURPOSE: Require auth AND tenant context. Returns (user, tenant_id) pair.
    STEPS:
      1. Get current_user (from get_current_user)
      2. Get tenant_id from request.state.tenant_id (set by TenantContextMiddleware)
      3. Validate tenant_id is not None
      4. Return (user, tenant_id)
    RETURNS: tuple[User, UUID]
    RAISES: AuthenticationError if not authenticated; AuthorizationError if no tenant context

DESIGN DECISIONS:
- auto_error=False on HTTPBearer: allows returning 401 with our error shape (not starlette default)
- Query user on each request: ensures is_active check; DB hit is acceptable (add cache if needed)
- require_tenant: separate from require_auth to make multi-tenancy explicit in route signatures
- All auth dependencies return User: consistent throughout; caller checks user.tenant_id as needed
"""
