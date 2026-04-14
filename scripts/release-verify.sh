#!/usr/bin/env bash
# scripts/release-verify.sh
# Run full validation matrix before tagging.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

make fmt
make lint
make typecheck
make test
make queue-validate
make audit-self
echo "release-verify: OK"
