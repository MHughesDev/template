# MicroFast dev MCP

Development-only **stdio** MCP server for coding agents (Cursor, Claude, Codex, …).

## Layout

| Path | Role |
|------|------|
| `server.py` | FastMCP app: tools, resources, prompts |
| `__main__.py` | `python -m dev_mcp` |
| `run.sh` | Launcher (used by `.cursor/mcp.json`) |
| `queue_ops/` | Queue CSV helpers shared with `scripts/queue_top_item.py` and `scripts/queue_validate.py` |

Run: `./dev_mcp/run.sh` or `make dev-mcp` (prints the command). Full procedure: [docs/procedures/microfast-dev-mcp.md](../docs/procedures/microfast-dev-mcp.md).
