#!/usr/bin/env bash
# scripts/test.sh
# Run pytest with coverage.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TEST_TYPE="${TEST_TYPE:-all}"

if [[ "$TEST_TYPE" == "unit" ]]; then
  python3 -m pytest apps/api/tests -m unit
elif [[ "$TEST_TYPE" == "integration" ]]; then
  python3 -m pytest apps/api/tests -m integration
elif [[ "$TEST_TYPE" == "smoke" ]]; then
  python3 -m pytest apps/api/tests -m smoke
else
  python3 -m pytest apps/api/tests
fi
