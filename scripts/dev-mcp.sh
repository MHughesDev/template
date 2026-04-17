#!/usr/bin/env bash
# Run the MicroFast development MCP server (stdio). Use from Cursor MCP config.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
exec python3 -m dev_mcp "$@"
