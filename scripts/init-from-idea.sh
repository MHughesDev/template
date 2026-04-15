#!/usr/bin/env bash
# scripts/init-from-idea.sh
# Run initialization orchestrator (see scripts/init-from-idea.py).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/init-from-idea.py" "$@"
