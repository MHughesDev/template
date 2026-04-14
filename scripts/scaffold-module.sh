#!/usr/bin/env bash
# scripts/scaffold-module.sh
# Scaffold a bounded-context module under apps/api/src/<module>/.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MODULE="${MODULE:-}"
if [[ -z "$MODULE" ]]; then
  echo "Usage: MODULE=<name> make scaffold:module" >&2
  exit 1
fi

exec python3 "$ROOT/skills/backend/module-scaffolder.py" --repo-root "$ROOT" --module "$MODULE"
