# apps/api/src/auth/models.py
"""
BLUEPRINT: apps/api/src/auth/models.py

PURPOSE:
Auth database models: User and RefreshToken. SQLAlchemy async-compatible models
inheriting from Base. Per spec §26.8 item 221.

DEPENDS ON:
- sqlalchemy — Column, String, Boolean, DateTime, ForeignKey, Index
- sqlalchemy.dialects.postgresql — UUID (PostgreSQL-specific)
- sqlalchemy.orm — relationship, Mapped, mapped_column
- apps.api.src.database — Base

DEPENDED ON BY:
- apps.api.src.auth.service — queries User and RefreshToken
- apps.api.src.tenancy.models — User has optional tenant_id FK
- alembic env.py — must import this module for autogenerate

CLASSES:

  User(Base):
    PURPOSE: Registered user account with hashed credentials.
    FIELDS:
      - id: UUID (primary key, default=uuid4)
      - email: str (unique, not null) — indexed for login lookup
      - hashed_password: str (not null) — bcrypt hash, never raw password
      - is_active: bool = True — soft disable without deletion
      - tenant_id: UUID | None — FK to Tenant.id (nullable for non-multi-tenant deployments)
      - created_at: datetime (server_default=utcnow)
      - updated_at: datetime (onupdate=utcnow)
    RELATIONSHIPS:
      - refresh_tokens: list[RefreshToken] (one-to-many)
    TABLE: users
    INDEXES: email (unique), tenant_id

  RefreshToken(Base):
    PURPOSE: Stored refresh token for server-side revocation tracking.
    FIELDS:
      - id: UUID (primary key)
      - user_id: UUID (FK to User.id, cascade delete)
      - token: str (unique) — the opaque refresh token value
      - expires_at: datetime — when the token expires
      - revoked: bool = False — True if explicitly revoked (logout)
      - created_at: datetime
    TABLE: refresh_tokens
    INDEXES: token (unique), user_id, expires_at

DESIGN DECISIONS:
- UUID primary keys: globally unique, no information leakage, safe to expose in APIs
- Hashed passwords only: service is responsible for hashing; model never sees plaintext
- soft delete via is_active: never delete users, just deactivate (audit trail)
- RefreshToken table: enables server-side revocation without shared state
- tenant_id nullable: supports non-multi-tenant deployments without schema change
"""
