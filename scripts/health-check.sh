#!/usr/bin/env bash
# scripts/health-check.sh
# GET /health on local API (default http://127.0.0.1:8000).

set -euo pipefail

BASE="${HEALTHCHECK_URL:-http://127.0.0.1:8000}"
curl -fsS "$BASE/health" | head -c 200
echo
