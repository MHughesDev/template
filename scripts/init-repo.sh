#!/usr/bin/env bash
# scripts/init-repo.sh
# Initialization pre-checks: Python env, idea validation, queue validate.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Python"
if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 not found" >&2
  exit 1
fi

echo "==> Optional: validate idea.md"
scripts/validate-idea.sh || echo "idea.md validation reported issues (fill idea.md before init)"

echo "==> Queue"
scripts/queue-validate.sh || true

echo "init-repo: pre-checks complete — follow docs/procedures/initialize-repo.md"
