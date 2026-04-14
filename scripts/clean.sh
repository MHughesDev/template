#!/usr/bin/env bash
# scripts/clean.sh
# Remove Python caches and common build artifacts.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
rm -rf htmlcov .coverage coverage.xml dist build *.egg-info 2>/dev/null || true
echo "clean: OK"
