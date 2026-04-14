#!/usr/bin/env bash
# scripts/docs-generate.sh
# Run documentation generation pipeline (skills/repo-governance/docs-generator.py).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/skills/repo-governance/docs-generator.py" --mode generate --repo-root "$ROOT"
