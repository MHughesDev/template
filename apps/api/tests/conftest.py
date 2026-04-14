# apps/api/tests/conftest.py
"""
BLUEPRINT: apps/api/tests/conftest.py

PURPOSE:
Shared test fixtures for the entire API test suite. Provides: FastAPI test app,
async HTTP client, test database session (with rollback), test user, and auth headers.
Per spec §26.8 item 229.

DEPENDS ON:
- pytest — fixtures
- pytest_asyncio — async fixtures (asyncio_mode="auto" assumed)
- httpx — AsyncClient for async API testing
- sqlalchemy.ext.asyncio — AsyncSession for test DB session
- apps.api.src.main — create_app() for test app instance
- apps.api.src.database — engine, Base (for table creation/rollback)
- apps.api.src.auth.models — User (for test user creation)
- apps.api.src.auth.service — AuthService (for test token generation)
- apps.api.src.config — Settings (for test settings override)
- apps.api.tests.factories — UserFactory, TenantFactory

FIXTURES:

  settings() -> Settings:
    PURPOSE: Override settings for testing.
    SCOPE: session
    STEPS:
      1. Return Settings(database_url="sqlite+aiosqlite:///./test.db", jwt_secret_key="test-secret", api_debug=True)
    NOTES: Overrides production settings; uses SQLite for fast isolated tests

  engine(settings) -> AsyncEngine:
    PURPOSE: Create test database engine and schema.
    SCOPE: session
    STEPS:
      1. Create async engine from settings.database_url
      2. Create all tables (Base.metadata.create_all)
      3. Yield engine
      4. Drop all tables on teardown
    NOTES: Session scope: one DB for all tests; function-scope rollback prevents state leakage

  db_session(engine) -> AsyncSession:
    PURPOSE: Provide a per-test DB session with automatic rollback.
    SCOPE: function
    STEPS:
      1. Begin a transaction on the engine
      2. Create session bound to that transaction
      3. Yield session
      4. Rollback the transaction (all test changes discarded)
    NOTES: Uses nested transactions for isolation; safe for concurrent test discovery

  app(settings) -> FastAPI:
    PURPOSE: Create FastAPI test app with test settings.
    SCOPE: session
    STEPS:
      1. Override get_settings with test settings
      2. create_app() with test settings
      3. Return app

  client(app, db_session) -> AsyncClient:
    PURPOSE: Async HTTP test client for API requests.
    SCOPE: function
    STEPS:
      1. Override get_db with db_session fixture
      2. Create AsyncClient(app=app, base_url="http://test")
      3. Yield client
    NOTES: Each test gets a fresh client with its own rollback session

  test_user(db_session) -> User:
    PURPOSE: Create a test user for use in auth tests.
    SCOPE: function
    STEPS:
      1. Use UserFactory to create a User with test email and password
      2. Add to db_session
      3. Return User
    NOTES: Created fresh per test (function scope)

  auth_headers(test_user, settings) -> dict[str, str]:
    PURPOSE: Generate valid JWT auth headers for the test user.
    SCOPE: function
    STEPS:
      1. Use AuthService.create_access_token(test_user)
      2. Return {"Authorization": f"Bearer {token}"}

  test_tenant(db_session) -> Tenant (if MULTI_TENANCY_ENABLED):
    PURPOSE: Create a test tenant for tenant isolation tests.
    SCOPE: function
    NOTES: Optional fixture; activated for multi-tenant tests

DESIGN DECISIONS:
- Rollback via nested transactions: faster than recreating tables per test
- AsyncClient: required for async route testing (not httpx.Client)
- Function scope for user/session/client: prevents test contamination
- Session scope for engine/app: expensive to recreate per test
"""
