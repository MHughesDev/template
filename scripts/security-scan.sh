#!/usr/bin/env bash
# scripts/security-scan.sh
# Run bandit on apps/api/src and pip-audit if available.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .bandit.yml ]]; then
  python3 -m bandit -c .bandit.yml -r apps/api/src packages || true
else
  python3 -m bandit -r apps/api/src packages || true
fi

if python3 -m pip_audit --version >/dev/null 2>&1; then
  python3 -m pip_audit || true
else
  echo "pip-audit not installed; skipping dependency audit." >&2
fi

echo "security:scan complete (review output above)"
