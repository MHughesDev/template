#!/usr/bin/env bash
# scripts/implementation-plan-ci.sh
# CI helper: verify IMPLEMENTATION_PLAN checked paths exist (inventory_check.py).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/inventory_check.py" --root "$ROOT"
