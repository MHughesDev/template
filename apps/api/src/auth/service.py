# apps/api/src/auth/service.py
"""
BLUEPRINT: apps/api/src/auth/service.py

PURPOSE:
Auth business logic: password hashing/verification, JWT creation/validation,
user management (create, authenticate, find), and token lifecycle (issue, refresh, revoke).
Per spec §26.8 item 223 and PYTHON_PROCEDURES.md §6 (Domain Separation).

DEPENDS ON:
- passlib.context — CryptContext for bcrypt hashing
- jose — jwt (python-jose) for JWT encoding/decoding
- datetime — timedelta for token expiry
- uuid — UUID4 for token IDs
- sqlalchemy.ext.asyncio — AsyncSession
- apps.api.src.auth.models — User, RefreshToken
- apps.api.src.auth.schemas — RegisterRequest, LoginRequest, TokenResponse
- apps.api.src.exceptions — AuthenticationError, ConflictError
- apps.api.src.config — Settings (for JWT config)

DEPENDED ON BY:
- apps.api.src.auth.router — calls all service functions
- apps.api.src.auth.dependencies — calls verify_token for get_current_user

CLASSES:

  AuthService:
    PURPOSE: Authentication business logic. Injected into routes via Depends(get_auth_service).
    FIELDS:
      - _session: AsyncSession — injected, used for DB operations
      - _settings: Settings — injected, for JWT configuration
      - _pwd_context: CryptContext — bcrypt context (class-level singleton)
    METHODS:

      async create_user(request: RegisterRequest) -> User:
        PURPOSE: Create a new user with hashed password.
        STEPS:
          1. Check if email already exists (query by email)
          2. Raise ConflictError if email taken
          3. Hash password with bcrypt
          4. Create User instance and add to session
          5. Commit and return User
        RAISES: ConflictError if email already registered

      async authenticate_user(email: str, password: str) -> User:
        PURPOSE: Verify credentials and return User if valid.
        STEPS:
          1. Query User by email
          2. If not found: raise AuthenticationError (same error as wrong password — prevents enumeration)
          3. If not active: raise AuthenticationError
          4. Verify password with bcrypt.verify
          5. If wrong: raise AuthenticationError
          6. Return User
        RAISES: AuthenticationError for any credential failure

      def create_access_token(user: User) -> str:
        PURPOSE: Create a signed JWT access token.
        STEPS:
          1. Build claims: sub=str(user.id), email=user.email, tenant_id=str(user.tenant_id), exp=now+expiry
          2. Encode with jwt.encode(claims, secret, algorithm)
          3. Return token string
        RETURNS: JWT access token string

      async create_refresh_token(user: User) -> str:
        PURPOSE: Create and persist a refresh token.
        STEPS:
          1. Generate random opaque token (secrets.token_urlsafe(32))
          2. Create RefreshToken record (expires_at = now + days)
          3. Add to session, commit
          4. Return token string
        RETURNS: Opaque refresh token string

      def verify_token(token: str) -> dict:
        PURPOSE: Verify and decode a JWT access token.
        STEPS:
          1. jwt.decode(token, secret, algorithms=[algorithm])
          2. Validate exp claim (jose handles this)
          3. Return claims dict
        RAISES: AuthenticationError if token is invalid, expired, or tampered

      async refresh_access_token(refresh_token: str) -> TokenResponse:
        PURPOSE: Exchange a refresh token for a new access token.
        STEPS:
          1. Query RefreshToken by token value
          2. If not found or revoked: raise AuthenticationError
          3. If expired: raise AuthenticationError
          4. Load associated User
          5. Issue new access token
          6. Optionally: rotate refresh token (issue new, revoke old)
          7. Return TokenResponse
        RAISES: AuthenticationError for any invalid refresh token state

      async revoke_token(refresh_token: str, user_id: UUID) -> None:
        PURPOSE: Revoke a specific refresh token (logout).
        STEPS:
          1. Query RefreshToken by token AND user_id (user can only revoke own tokens)
          2. Set revoked=True
          3. Commit
        RAISES: AuthenticationError if token not found or doesn't belong to user

DESIGN DECISIONS:
- Same error message for "user not found" and "wrong password": prevents email enumeration
- Opaque refresh tokens (not JWT): server-side revocation without shared state
- bcrypt: industry-standard; passlib handles work factor and salt
- JWT claims include tenant_id: extracted by TenantContextMiddleware without extra DB query
- Token rotation on refresh: optional but recommended (refreshes the long-lived token)
"""
