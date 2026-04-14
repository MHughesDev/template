#!/usr/bin/env bash
# scripts/docs-generate.sh
# Regenerate docs from source when generators exist (placeholder for OpenAPI export).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "docs:generate — no generators configured in template; export OpenAPI manually if needed."
exit 0
