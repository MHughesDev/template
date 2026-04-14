#!/usr/bin/env bash
# scripts/scaffold-module.sh
# Stub: invoke skills/backend/module-scaffolder.py when MODULE is set.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${MODULE:-}" ]]; then
  echo "Usage: MODULE=mycontext make scaffold:module" >&2
  exit 1
fi

echo "Module scaffolding: run scripts/skills/backend/module-scaffolder.py or implement in follow-up."
echo "Requested MODULE=$MODULE"
exit 0
