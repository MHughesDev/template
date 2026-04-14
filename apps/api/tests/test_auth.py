# apps/api/tests/test_auth.py
"""
BLUEPRINT: apps/api/tests/test_auth.py

PURPOSE:
Tests for auth endpoints: register, login, refresh, logout. Covers success cases,
error cases, and edge cases. Per spec §26.8 item 231.

DEPENDS ON:
- pytest — test runner
- httpx — AsyncClient
- apps.api.tests.conftest — client, test_user, auth_headers, db_session
- apps.api.tests.factories — create_test_user

TEST FUNCTIONS:

  test_register_success(client: AsyncClient, db_session) -> None:
    PURPOSE: Verify POST /auth/register creates a user and returns 201.
    STEPS:
      1. POST /auth/register with valid email and password
      2. Assert status_code == 201
      3. Assert response.json() contains id, email fields
      4. Assert no password in response
      5. Assert user exists in DB

  test_register_duplicate_email_returns_409(client: AsyncClient, test_user, db_session) -> None:
    PURPOSE: Verify POST /auth/register with existing email returns 409.
    STEPS:
      1. POST /auth/register with test_user.email
      2. Assert status_code == 409
      3. Assert response.json()["error"]["code"] == "CONFLICT"

  test_login_success(client: AsyncClient, test_user, db_session) -> None:
    PURPOSE: Verify POST /auth/login returns tokens on valid credentials.
    STEPS:
      1. POST /auth/login with valid email and password
      2. Assert status_code == 200
      3. Assert access_token and refresh_token in response
      4. Assert token_type == "bearer"

  test_login_invalid_password_returns_401(client: AsyncClient, test_user, db_session) -> None:
    PURPOSE: Verify POST /auth/login with wrong password returns 401.
    STEPS:
      1. POST /auth/login with correct email but wrong password
      2. Assert status_code == 401
      3. Assert response.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"

  test_login_nonexistent_email_returns_401(client: AsyncClient) -> None:
    PURPOSE: Verify POST /auth/login with unknown email returns 401 (no enumeration).
    STEPS:
      1. POST /auth/login with email that doesn't exist
      2. Assert status_code == 401 (same as wrong password — no enumeration)

  test_refresh_success(client: AsyncClient, test_user, db_session) -> None:
    PURPOSE: Verify POST /auth/refresh exchanges refresh token for new access token.
    STEPS:
      1. Login to get refresh_token
      2. POST /auth/refresh with refresh_token
      3. Assert status_code == 200
      4. Assert new access_token in response

  test_refresh_invalid_token_returns_401(client: AsyncClient) -> None:
    PURPOSE: Verify POST /auth/refresh with invalid token returns 401.
    STEPS:
      1. POST /auth/refresh with "invalid-token"
      2. Assert status_code == 401

  test_logout_success(client: AsyncClient, test_user, auth_headers, db_session) -> None:
    PURPOSE: Verify POST /auth/logout revokes refresh token and returns 200.
    STEPS:
      1. Login to get refresh_token
      2. POST /auth/logout with auth_headers and refresh_token body
      3. Assert status_code == 200
      4. Assert status=logged_out in response
      5. Verify refresh_token is revoked (try to use it again → 401)

  test_protected_endpoint_without_auth_returns_401(client: AsyncClient) -> None:
    PURPOSE: Verify any protected endpoint returns 401 without Authorization header.
    STEPS:
      1. GET /api/v1/users/me (or any authenticated-only endpoint)
      2. Assert status_code == 401

DESIGN DECISIONS:
- Test login before refresh (dependency between scenarios)
- Same 401 for unknown email and wrong password: both test the same security invariant
- Verify revocation by re-using the revoked token: end-to-end correctness test
- All tests in isolation: each creates its own test data via factories
"""
