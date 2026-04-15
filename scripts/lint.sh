#!/usr/bin/env bash
# scripts/lint.sh
# Run Ruff linter on application and package sources.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m ruff check apps/api/src packages \
  scripts/idea-parser.py scripts/scaffold-module.py scripts/init-from-idea.py
