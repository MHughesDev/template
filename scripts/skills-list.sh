#!/usr/bin/env bash
# scripts/skills-list.sh
# Print skills index (delegates to canonical file).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec cat "$ROOT/skills/README.md"
