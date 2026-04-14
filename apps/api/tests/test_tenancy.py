# apps/api/tests/test_tenancy.py
"""
BLUEPRINT: apps/api/tests/test_tenancy.py

PURPOSE:
Tenant isolation tests: middleware behavior, query scoping, cross-tenant prevention.
Per spec §26.12 item 344.

DEPENDS ON:
- pytest — test runner
- httpx — AsyncClient
- apps.api.tests.conftest — client, db_session, test_user, test_tenant fixtures
- apps.api.tests.factories — create_test_user, create_test_tenant

TEST FUNCTIONS:

  test_tenant_middleware_sets_tenant_id(client: AsyncClient, auth_headers: dict) -> None:
    PURPOSE: Verify TenantContextMiddleware extracts tenant_id from JWT and sets on request state.
    STEPS:
      1. Create user with tenant_id
      2. GET /api/v1/users/me with auth headers (JWT contains tenant_id claim)
      3. Assert response.json()["tenant_id"] matches expected tenant
    NOTES: Requires MULTI_TENANCY_ENABLED=true in test settings

  test_cross_tenant_access_returns_404(client: AsyncClient, db_session) -> None:
    PURPOSE: Verify user from tenant A cannot access resources belonging to tenant B.
    STEPS:
      1. Create two tenants: tenant_a, tenant_b
      2. Create user_a (tenant_a) and user_b (tenant_b)
      3. Create a resource belonging to tenant_b
      4. GET /api/v1/<resource>/<b_resource_id> with user_a's auth headers
      5. Assert status_code == 404 (not found, not 403 — don't leak existence)

  test_tenant_scoped_list_only_returns_own_resources(client: AsyncClient, db_session) -> None:
    PURPOSE: Verify list endpoints only return resources from the authenticated user's tenant.
    STEPS:
      1. Create tenant_a and tenant_b with different resources
      2. GET list endpoint with tenant_a user auth
      3. Assert response only contains tenant_a resources
      4. Assert no tenant_b resource IDs appear

  test_create_resource_assigns_correct_tenant(client: AsyncClient, auth_headers: dict, db_session) -> None:
    PURPOSE: Verify creating a resource assigns it to the authenticated user's tenant.
    STEPS:
      1. POST to create a new resource (with auth headers for tenant_a user)
      2. Assert status_code == 201
      3. Query DB: verify created resource has tenant_id == tenant_a

DESIGN DECISIONS:
- 404 (not 403) for cross-tenant access: don't reveal that the resource exists in another tenant
- All tests skip if MULTI_TENANCY_ENABLED=False in test settings (via pytest.mark.skipif)
- Isolation is tested at the API boundary, not just the repository layer
"""
