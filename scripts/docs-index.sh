#!/usr/bin/env bash
# scripts/docs-index.sh
# Refresh documentation indexes (delegates to docs-generator when available).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/scripts/docs-generate.sh"
