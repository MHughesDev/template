#!/usr/bin/env bash
# scripts/inventory-check.sh
# Verify critical spec paths exist (inventory check only).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

exec python3 "$ROOT/skills/agent-ops/repo-self-audit.py" --repo-root "$ROOT" --inventory-only "$@"
