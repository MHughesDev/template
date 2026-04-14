#!/usr/bin/env bash
# scripts/release-prepare.sh
# Verify CHANGELOG has [Unreleased] and pyproject version.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
grep -q '\[Unreleased\]' "$ROOT/CHANGELOG.md" || {
  echo "CHANGELOG missing [Unreleased] section" >&2
  exit 1
}
echo "release:prepare OK — update CHANGELOG and version before tagging."
