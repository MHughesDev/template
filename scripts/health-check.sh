#!/usr/bin/env bash
# scripts/health-check.sh
# GET /health, /ready, /live on local API (default http://127.0.0.1:8000).

set -euo pipefail

BASE="${HEALTHCHECK_BASE_URL:-http://127.0.0.1:8000}"

for path in /health /ready /live; do
  url="${BASE}${path}"
  echo "GET $url"
  code=$(curl -s -o /tmp/health.json -w "%{http_code}" "$url" || true)
  if [[ "$code" != "200" ]]; then
    echo "error: expected HTTP 200, got $code for $url" >&2
    exit 1
  fi
  cat /tmp/health.json
  echo ""
done
echo "health-check OK"
