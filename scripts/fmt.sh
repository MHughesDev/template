#!/usr/bin/env bash
# scripts/fmt.sh
# Verify Ruff formatting (CI mode — does not modify files).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m ruff format --check apps/api/src packages/contracts packages/tasks
