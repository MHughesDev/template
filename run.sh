#!/usr/bin/env bash
# run.sh
# Start the API (delegates to scripts/dev.sh).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  echo "No .env — run ./setup.sh or: cp .env.example .env" >&2
  exit 1
fi

if [[ -f .venv/bin/activate ]]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

exec "$ROOT/scripts/dev.sh"
