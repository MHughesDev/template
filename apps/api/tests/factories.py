# apps/api/tests/factories.py
"""
BLUEPRINT: apps/api/tests/factories.py

PURPOSE:
Test data factories using factory patterns (factory_boy-inspired or simple factory
functions). Creates test instances of User, Tenant, and other models with sensible
defaults that can be overridden per-test. Per spec §26.12 item 372.

DEPENDS ON:
- uuid — UUID4 generation
- datetime — for created_at fields
- passlib.context — CryptContext for password hashing in test users
- apps.api.src.auth.models — User, RefreshToken
- apps.api.src.tenancy.models — Tenant

DEPENDED ON BY:
- apps.api.tests.conftest — uses UserFactory, TenantFactory in fixtures
- apps.api.tests.test_*.py — test files use factories for test data

FUNCTIONS:

  create_test_user(
    email: str = "test@example.com",
    password: str = "testpassword123",
    is_active: bool = True,
    tenant_id: UUID | None = None,
  ) -> User:
    PURPOSE: Create a User ORM instance with hashed password (not yet persisted).
    STEPS:
      1. Hash password with bcrypt (test-appropriate rounds=4 for speed)
      2. Create User with provided fields and defaults
      3. Return User instance (caller adds to session)
    RETURNS: User instance
    NOTES: rounds=4 (not production 12) for fast tests

  create_test_tenant(
    name: str = "Test Organization",
    slug: str = "test-org",
    is_active: bool = True,
  ) -> Tenant:
    PURPOSE: Create a Tenant ORM instance (not yet persisted).
    RETURNS: Tenant instance

  create_test_refresh_token(
    user: User,
    token: str | None = None,
    revoked: bool = False,
    expires_days: int = 30,
  ) -> RefreshToken:
    PURPOSE: Create a RefreshToken ORM instance.
    RETURNS: RefreshToken instance

DESIGN DECISIONS:
- Factory functions (not factory_boy classes): simpler dependency tree
- Passwords NOT hardcoded: each factory call can specify; defaults are clearly fake
- Low bcrypt rounds in tests: 4 vs 12 production = 8x faster test execution
- instances returned (not persisted): caller controls when to add to session
- Unique defaults via uuid: email = f"test-{uuid4().hex[:8]}@example.com" prevents conflicts
"""
