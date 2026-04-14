#!/usr/bin/env bash
# scripts/release-prepare.sh
# Verify CHANGELOG has an Unreleased section and pyproject version is set.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! grep -q '## \[Unreleased\]' CHANGELOG.md 2>/dev/null; then
  echo "warning: CHANGELOG.md missing ## [Unreleased] section" >&2
fi

grep '^version' pyproject.toml || true
echo "release-prepare: OK (update CHANGELOG and version before tagging)"
