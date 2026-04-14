#!/usr/bin/env bash
# scripts/audit-self.sh
# Run repository self-audit (spec compliance).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

exec python3 "$ROOT/skills/agent-ops/repo-self-audit.py" --repo-root "$ROOT" "$@"
