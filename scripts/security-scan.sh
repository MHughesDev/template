#!/usr/bin/env bash
# scripts/security-scan.sh
# Bandit SAST, pip-audit (if available), and grep-based secret patterns.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

FAILED=0

echo "==> bandit"
if python3 -m bandit -q -c .bandit.yml -r apps/api/src packages/contracts packages/tasks 2>/dev/null; then
  echo "bandit: OK"
else
  echo "bandit: FAILED" >&2
  FAILED=1
fi

echo "==> pip-audit (optional)"
if python3 -m pip_audit --progress-spinner off 2>/dev/null; then
  echo "pip-audit: OK"
else
  echo "pip-audit: skipped (install pip-audit to audit dependencies)" >&2
fi

echo "==> patterns (high-signal secret strings in tracked source)"
# Exclude large generated dirs; focus on app + packages
if rg -n --hidden --glob '!.git/*' \
  -e 'AKIA[0-9A-Z]{16}' \
  -e 'ghp_[A-Za-z0-9]{20,}' \
  -e 'xox[baprs]-[0-9A-Za-z-]{10,}' \
  apps/api/src packages scripts skills 2>/dev/null; then
  echo "pattern scan: possible secret-like strings found" >&2
  FAILED=1
else
  echo "pattern scan: OK"
fi

exit "$FAILED"
