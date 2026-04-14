# apps/api/src/auth/router.py
"""
BLUEPRINT: apps/api/src/auth/router.py

PURPOSE:
Auth endpoints: register, login, refresh, logout. Policy-complete stubs with
extension points for OAuth2, SSO, and MFA. Per spec §26.8 item 220.

DEPENDS ON:
- fastapi — APIRouter, Depends, HTTPException
- apps.api.src.auth.schemas — RegisterRequest, LoginRequest, TokenResponse, etc.
- apps.api.src.auth.service — AuthService
- apps.api.src.auth.dependencies — get_auth_service, get_current_user
- apps.api.src.dependencies — get_db

DEPENDED ON BY:
- apps.api.src.main — registers this router under /api/v1/auth

ENDPOINTS:

  POST /register -> UserResponse:
    PURPOSE: Register a new user account.
    STEPS:
      1. Validate RegisterRequest body (email, password)
      2. Inject AuthService via get_auth_service
      3. Call service.create_user(body)
      4. Return UserResponse (no tokens — user must login)
    RAISES: ConflictError (409) if email already registered
    AUTH: None required

  POST /login -> TokenResponse:
    PURPOSE: Authenticate user and return JWT tokens.
    STEPS:
      1. Validate LoginRequest body (email, password)
      2. Call service.authenticate_user(email, password)
      3. Generate access token and refresh token
      4. Return TokenResponse (access_token, refresh_token, token_type, expires_in)
    RAISES: AuthenticationError (401) if invalid credentials
    AUTH: None required

  POST /refresh -> TokenResponse:
    PURPOSE: Exchange a refresh token for a new access token.
    STEPS:
      1. Validate RefreshRequest body (refresh_token)
      2. Call service.refresh_access_token(refresh_token)
      3. Return new TokenResponse
    RAISES: AuthenticationError (401) if refresh token invalid/expired/revoked
    AUTH: None (refresh token in body)

  POST /logout -> LogoutResponse:
    PURPOSE: Revoke the current user's refresh token.
    STEPS:
      1. Extract current user via get_current_user
      2. Extract refresh token from RefreshRequest body
      3. Call service.revoke_token(refresh_token, user_id)
      4. Return {"status": "logged_out"}
    AUTH: Bearer token required (get_current_user)

DESIGN DECISIONS:
- No cookies: stateless JWT in Authorization header (easier for API clients)
- Refresh tokens stored in DB (RefreshToken model): enables server-side revocation
- Password complexity: enforced in RegisterRequest Pydantic validator (not shown here)
- SSO extension point: additional POST /auth/sso/{provider} endpoint stub for OAuth2 IdP
"""
