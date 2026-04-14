# apps/api/src/health/router.py
"""
BLUEPRINT: apps/api/src/health/router.py

PURPOSE:
Health, readiness, and liveness endpoints. Provides three endpoints:
/health (always 200), /ready (checks DB and critical deps), /live (process alive).
Used by K8s probes and Docker HEALTHCHECK. Per spec §26.8 item 218.

DEPENDS ON:
- fastapi — APIRouter, Depends
- sqlalchemy.ext.asyncio — AsyncSession
- apps.api.src.dependencies — get_db
- apps.api.src.exceptions — ExternalServiceError
- apps.api.src.database — engine (for readiness check)

DEPENDED ON BY:
- apps.api.src.main — registers this router

ENDPOINTS:

  GET /health -> HealthResponse:
    PURPOSE: Basic health check. Always returns 200 if the process is alive.
    STEPS: Return {"status": "ok"} immediately — no DB check.
    RETURNS: HealthResponse with status="ok"
    NOTES: K8s liveness probe uses this; must be fast and never depend on external services

  GET /ready -> ReadinessResponse:
    PURPOSE: Readiness check. Returns 200 if DB is accessible, 503 if not.
    STEPS:
      1. Execute a lightweight DB query (SELECT 1)
      2. If success: return {"status": "ready", "checks": {"database": "ok"}}
      3. If DB fails: return 503 with {"status": "not_ready", "checks": {"database": "error: <reason>"}}
    RETURNS: ReadinessResponse (200 or 503)
    NOTES: K8s readiness probe uses this; if not ready, K8s stops sending traffic

  GET /live -> LivenessResponse:
    PURPOSE: Liveness check. Returns 200 to confirm process is running.
    STEPS: Return {"status": "alive"} — no external checks.
    RETURNS: LivenessResponse with status="alive"
    NOTES: K8s liveness probe; if this fails, K8s restarts the pod

CLASSES:

  HealthResponse(BaseModel):
    PURPOSE: Response schema for GET /health.
    FIELDS: status: Literal["ok"]

  ReadinessResponse(BaseModel):
    PURPOSE: Response schema for GET /ready.
    FIELDS:
      - status: Literal["ready", "not_ready"]
      - checks: dict[str, str] — per-dependency status

  LivenessResponse(BaseModel):
    PURPOSE: Response schema for GET /live.
    FIELDS: status: Literal["alive"]

DESIGN DECISIONS:
- /health and /live: no DB dependency — must succeed even when DB is down (critical for K8s restart cycle)
- /ready: DB check — pod not ready when DB unreachable (K8s won't send traffic)
- 503 for /ready failure (not 200 with error body): clients and load balancers understand 503
- Endpoints not under /api/v1 prefix: health checks are meta-API, not versioned
"""
