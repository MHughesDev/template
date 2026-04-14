#!/usr/bin/env bash
# scripts/inventory-check.sh
# Verify spec/IMPLEMENTATION_PLAN.md file checklist rows exist on disk.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/inventory_check.py" --root "$ROOT"
