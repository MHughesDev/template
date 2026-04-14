# apps/api/src/tenancy/models.py
"""
BLUEPRINT: apps/api/src/tenancy/models.py

PURPOSE:
Tenant database models: Tenant entity and TenantMixin for query scoping.
TenantMixin adds tenant_id FK to any model that needs tenant isolation.
Per spec §26.8 item 227.

DEPENDS ON:
- sqlalchemy — Column, String, Boolean, DateTime, ForeignKey, UUID
- sqlalchemy.orm — DeclarativeMixin, declared_attr, Mapped, mapped_column
- apps.api.src.database — Base

DEPENDED ON BY:
- apps.api.src.auth.models — User optionally references tenant_id
- apps.api.src.*/models.py — any tenant-scoped model inherits TenantMixin
- alembic env.py — must import for autogenerate

CLASSES:

  Tenant(Base):
    PURPOSE: Organization/tenant entity for multi-tenant deployments.
    FIELDS:
      - id: UUID (primary key, default=uuid4)
      - name: str — tenant display name (not null)
      - slug: str (unique) — URL-safe identifier for the tenant
      - is_active: bool = True — soft disable without data deletion
      - created_at: datetime
      - updated_at: datetime
    TABLE: tenants
    INDEXES: slug (unique)
    NOTES: Provisioned at organization onboarding; not user-created

  TenantMixin:
    PURPOSE: SQLAlchemy mixin that adds tenant_id FK and query scoping to any model.
    FIELDS (via @declared_attr):
      - tenant_id: UUID (FK to tenants.id, not null, indexed)
    NOTES:
      - Add to any model that is tenant-scoped: class Invoice(Base, TenantMixin): ...
      - Enforces that all queries on the model include WHERE tenant_id = current_tenant
      - Static analysis: skills/security/tenant-isolation-checker.py scans for missing mixin

DESIGN DECISIONS:
- TenantMixin not Tenant subclass: cleaner multiple inheritance
- tenant_id is not null in TenantMixin: tenant-scoped models always have a tenant
- Soft delete (is_active): tenant data preserved for audit; never hard-deleted
- Slug: human-readable identifier for tenant (e.g., in subdomain routing)
"""
