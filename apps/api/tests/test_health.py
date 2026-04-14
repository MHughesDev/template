# apps/api/tests/test_health.py
"""
BLUEPRINT: apps/api/tests/test_health.py

PURPOSE:
Tests for the health, readiness, and liveness endpoints. Covers happy paths
and failure modes per spec §26.8 item 230.

DEPENDS ON:
- pytest — test runner
- httpx — AsyncClient (from client fixture)
- apps.api.tests.conftest — client fixture

DEPENDED ON BY:
- make test — runs this as part of test suite

TEST FUNCTIONS:

  test_health_returns_200(client: AsyncClient) -> None:
    PURPOSE: Verify GET /health always returns 200 with status=ok.
    STEPS:
      1. GET /health
      2. Assert status_code == 200
      3. Assert response.json()["status"] == "ok"

  test_ready_returns_200_when_db_accessible(client: AsyncClient) -> None:
    PURPOSE: Verify GET /ready returns 200 when DB is accessible.
    STEPS:
      1. GET /ready (test DB is accessible via conftest)
      2. Assert status_code == 200
      3. Assert response.json()["status"] == "ready"
      4. Assert "database" in response.json()["checks"]

  test_ready_returns_503_when_db_down(client: AsyncClient, monkeypatch) -> None:
    PURPOSE: Verify GET /ready returns 503 when DB is inaccessible.
    STEPS:
      1. Monkeypatch DB to raise SQLAlchemy error
      2. GET /ready
      3. Assert status_code == 503
      4. Assert response.json()["status"] == "not_ready"

  test_live_returns_200(client: AsyncClient) -> None:
    PURPOSE: Verify GET /live always returns 200.
    STEPS:
      1. GET /live
      2. Assert status_code == 200
      3. Assert response.json()["status"] == "alive"

  test_health_no_auth_required(client: AsyncClient) -> None:
    PURPOSE: Verify health endpoints are accessible without authentication.
    STEPS:
      1. GET /health (no Authorization header)
      2. Assert status_code != 401 (must not require auth)

DESIGN DECISIONS:
- Tests grouped by endpoint (no test classes needed for simple health tests)
- test_ready_db_down: uses monkeypatch to inject DB failure without actual DB shutdown
- All tests are @pytest.mark.unit (no external deps beyond test DB fixture)
"""
