#!/usr/bin/env bash
# scripts/queue-analyze.sh
# Queue intelligence summary (skills/agent-ops/queue-intelligence.py).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QI="$ROOT/skills/agent-ops/queue-intelligence.py"

if [[ -f "$QI" ]]; then
  if [[ -f "$ROOT/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "$ROOT/.venv/bin/activate"
  fi
  exec python3 "$QI" "$@"
fi

echo "error: queue-intelligence.py not implemented" >&2
exit 1
