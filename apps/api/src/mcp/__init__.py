# apps/api/src/mcp/__init__.py
"""MCP (Model Context Protocol) integration via fastapi-mcp.

Mounts an MCP server onto the FastAPI application. Endpoints are exposed as MCP
tools from the app's OpenAPI schema (see FastAPI-MCP docs). Add dedicated
routes in this module when you need a tool that should not live in a domain
router.

Usage:
    from apps.api.src.mcp import mount_mcp

    mount_mcp(app)

MCP HTTP transport: ``/mcp`` (default for ``mount_http``).

Dependencies: ``fastapi-mcp`` (see ``pyproject.toml``).
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field

# --- Custom routes that become MCP tools (OpenAPI operation IDs) ----------------
# fastapi-mcp builds tools from OpenAPI; there is no @mcp.tool() decorator in
# this library. Register a small route here so it appears as a named tool.
_mcp_custom_router = APIRouter(prefix="/mcp-tools", tags=["mcp"])


class McpHealthCheckResponse(BaseModel):
    """Payload for the MCP-oriented health check tool."""

    status: Literal["ok"] = "ok"
    service: str = Field(
        default="template-api",
        description="Logical service name for clients and agents.",
    )


@_mcp_custom_router.get(
    "/health_check",
    response_model=McpHealthCheckResponse,
    operation_id="mcp_health_check",
    summary="MCP health check",
)
async def mcp_health_check() -> McpHealthCheckResponse:
    """Return a simple server status for MCP clients (custom tool).

    Use this to verify MCP connectivity without hitting domain APIs.
    """

    return McpHealthCheckResponse()


def mount_mcp(app: FastAPI) -> FastApiMCP:
    """Mount MCP HTTP server and register MCP-specific routes on ``app``.

    Auto-generates MCP tools from FastAPI's OpenAPI schema (all routes, including
    those registered before this call). Routes added here are included because
    they are registered before ``FastApiMCP`` reads the schema.

    Args:
        app: The FastAPI application instance.

    Returns:
        Configured :class:`FastApiMCP` instance (already mounted at ``/mcp``).
    """
    app.include_router(_mcp_custom_router)

    mcp = FastApiMCP(
        app,
        name="template-mcp-server",
        description="MCP server exposing API endpoints as tools for AI agents",
        # Endpoint filtering (uncomment as needed):
        # include_tags=["estimates", "quotes"],
        # exclude_tags=["internal", "admin", "Health"],
        # include_operations=["get_estimate", "create_quote"],
        # exclude_operations=["debug_info"],
    )

    # --- Custom tools (beyond auto-generated endpoint tools) ---
    # fastapi-mcp derives tools from OpenAPI. Add routes (e.g. under
    # ``/mcp-tools``) above, or use existing routers — each operation becomes a
    # tool. For multi-step workflows, prefer calling service layers from a
    # dedicated route rather than putting logic in this package.

    # --- Auth (uncomment to protect MCP HTTP endpoints) ---
    # from fastapi import Depends
    # from fastapi_mcp.types import AuthConfig
    # from apps.api.src.auth.dependencies import get_current_user
    #
    # mcp = FastApiMCP(
    #     app,
    #     name="template-mcp-server",
    #     description="...",
    #     auth_config=AuthConfig(dependencies=[Depends(get_current_user)]),
    # )
    # app.include_router(_mcp_custom_router)  # keep before FastApiMCP init

    mcp.mount_http(mount_path="/mcp")
    return mcp
