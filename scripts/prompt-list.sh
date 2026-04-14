#!/usr/bin/env bash
# scripts/prompt-list.sh
# List prompt templates under prompts/ (excludes README).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/prompts"

echo "Prompt templates:"
find . -maxdepth 1 -name '*.md' ! -name 'README.md' -print | sed 's|^\./||' | sort
