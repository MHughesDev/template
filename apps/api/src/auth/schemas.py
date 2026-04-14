# apps/api/src/auth/schemas.py
"""
BLUEPRINT: apps/api/src/auth/schemas.py

PURPOSE:
Auth Pydantic schemas for request and response models at auth endpoints.
All request schemas frozen=True. Per spec §26.8 item 222.

DEPENDS ON:
- pydantic — BaseModel, ConfigDict, Field, field_validator, EmailStr

DEPENDED ON BY:
- apps.api.src.auth.router — uses all schemas as request/response types
- apps.api.src.auth.service — uses RegisterRequest, LoginRequest as typed inputs
- apps.api.tests.test_auth — creates instances for tests

CLASSES:

  RegisterRequest(BaseModel):
    PURPOSE: Request body for POST /auth/register.
    FIELDS:
      - email: EmailStr — must be valid email format
      - password: str — min 8 chars, max 128 chars
    VALIDATORS:
      - field_validator("password") — check min length (8), max length (128),
        and presence of at least one non-alpha char (strength requirement)
    CONFIG: frozen=True (input boundary schema)

  LoginRequest(BaseModel):
    PURPOSE: Request body for POST /auth/login.
    FIELDS:
      - email: EmailStr
      - password: str
    CONFIG: frozen=True

  TokenResponse(BaseModel):
    PURPOSE: Response body for login and refresh endpoints.
    FIELDS:
      - access_token: str — short-lived JWT access token
      - refresh_token: str — longer-lived opaque refresh token
      - token_type: Literal["bearer"] = "bearer"
      - expires_in: int — access token lifetime in seconds

  RefreshRequest(BaseModel):
    PURPOSE: Request body for POST /auth/refresh and POST /auth/logout.
    FIELDS:
      - refresh_token: str — the refresh token to use/revoke
    CONFIG: frozen=True

  UserResponse(BaseModel):
    PURPOSE: Public representation of a user (no password, no internal fields).
    FIELDS:
      - id: UUID
      - email: str
      - is_active: bool
      - tenant_id: UUID | None
      - created_at: datetime
    CONFIG: from_attributes=True (enables model_validate from SQLAlchemy model)

  LogoutResponse(BaseModel):
    PURPOSE: Confirmation response for logout.
    FIELDS:
      - status: Literal["logged_out"]

DESIGN DECISIONS:
- Email validated as EmailStr (pydantic-email-validator): catches invalid formats at boundary
- frozen=True on all input schemas: inputs are immutable once validated
- UserResponse: from_attributes=True allows direct validation from User ORM instance
- No raw password in any response: never exposed after registration
"""
