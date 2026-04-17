# dev_mcp/server.py
"""FastMCP (stdio) development server: queue, repo docs, prompts, validation."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from dev_mcp.queue_ops import peek_queue_csv_head, top_item_json_line, validate_queue_files

_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[1]

_INSTRUCTIONS = """\
Software-factory dev assistant for this repository. Use tools to read the active \
queue item, validate the queue, load AGENTS.md and skills index, and run canonical \
make targets. Queue CSV files are never modified through this server — operators \
own the ledger. Prefer make targets over ad hoc shell."""

mcp = FastMCP(
    name="microfast-dev",
    instructions=_INSTRUCTIONS,
)

_READ_MAX_DEFAULT = 256_000
_MAKE_TARGET_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9:_-]*$")


def _safe_repo_path(relative: str) -> Path:
    """Resolve ``relative`` under the repo root; reject traversal."""

    rel = relative.strip().replace("\\", "/").lstrip("/")
    if ".." in rel.split("/"):
        msg = "path must not contain '..'"
        raise ValueError(msg)
    candidate = (_REPO_ROOT / rel).resolve()
    try:
        candidate.relative_to(_REPO_ROOT)
    except ValueError as e:
        msg = "path escapes repository root"
        raise ValueError(msg) from e
    return candidate


@mcp.tool()
def queue_top_item() -> str:
    """Top open queue row as one JSON line (same as ``make queue:top-item``)."""

    return str(top_item_json_line(_REPO_ROOT))


@mcp.tool()
def queue_peek(lines: int = 3) -> str:
    """Return the first ``lines`` of ``queue/queue.csv`` (peek raw CSV header + row)."""

    if lines < 1 or lines > 50:
        return "lines must be between 1 and 50"
    return str(peek_queue_csv_head(_REPO_ROOT, lines=lines))


@mcp.tool()
def queue_validate() -> str:
    """Validate open + archive queue CSVs; return OK or errors."""

    errs = validate_queue_files(_REPO_ROOT)
    if errs:
        return "Validation failed:\n" + "\n".join(errs)
    return "Queue OK"


@mcp.tool()
def read_repo_file(relative_path: str, max_bytes: int = _READ_MAX_DEFAULT) -> str:
    """Read a UTF-8 file under the repo (e.g. AGENTS.md, skills/README.md)."""

    if max_bytes < 1024 or max_bytes > 2_000_000:
        return "max_bytes must be between 1024 and 2000000"
    path = _safe_repo_path(relative_path)
    if not path.is_file():
        return f"Not a file: {relative_path}"
    raw = path.read_bytes()
    if len(raw) > max_bytes:
        return f"File exceeds max_bytes ({len(raw)} > {max_bytes}): {relative_path}"
    return raw.decode(encoding="utf-8", errors="replace")


@mcp.tool()
def list_prompt_files() -> str:
    """List ``prompts/*.md`` files (names only), one per line."""

    prompts_dir = _REPO_ROOT / "prompts"
    if not prompts_dir.is_dir():
        return "prompts/ not found"
    names = sorted(p.name for p in prompts_dir.glob("*.md") if p.is_file())
    return "\n".join(names) if names else "(no prompts/*.md)"


@mcp.tool()
def run_make_target(
    target: str,
    timeout_seconds: int = 180,
) -> str:
    """Run ``make <target>`` at repo root (allowed chars per regex)."""

    if not _MAKE_TARGET_RE.match(target):
        return (
            "Invalid target: use only letters, digits, underscore, hyphen, "
            "and single colons (e.g. queue:top-item, lint)."
        )
    if timeout_seconds < 5 or timeout_seconds > 600:
        return "timeout_seconds must be between 5 and 600"
    try:
        proc = subprocess.run(
            ["make", target],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"make {target}: timed out after {timeout_seconds}s"
    out = []
    if proc.stdout:
        out.append(proc.stdout)
    if proc.stderr:
        out.append("--- stderr ---\n" + proc.stderr)
    tail = "\n".join(out).strip()
    if len(tail) > 120_000:
        tail = tail[:120_000] + "\n... (truncated)"
    status = f"exit_code={proc.returncode}"
    return f"{status}\n{tail}" if tail else status


@mcp.resource("repo://AGENTS.md")
def resource_agents_md() -> str:
    """AGENTS.md — authoritative agent contract for this repository."""

    p = _REPO_ROOT / "AGENTS.md"
    return p.read_text(encoding="utf-8") if p.is_file() else "Missing AGENTS.md"


@mcp.resource("repo://README.md")
def resource_readme() -> str:
    """README.md — repository map and essential commands."""

    p = _REPO_ROOT / "README.md"
    return p.read_text(encoding="utf-8") if p.is_file() else "Missing README.md"


@mcp.resource("repo://skills/README.md")
def resource_skills_index() -> str:
    """skills/README.md — mandatory skill search index."""

    p = _REPO_ROOT / "skills" / "README.md"
    return p.read_text(encoding="utf-8") if p.is_file() else "Missing skills/README.md"


@mcp.resource("repo://queue/QUEUE_INSTRUCTIONS.md")
def resource_queue_instructions() -> str:
    """Queue SOP — lifecycle, schema, executor vs operator."""

    p = _REPO_ROOT / "queue" / "QUEUE_INSTRUCTIONS.md"
    return (
        p.read_text(encoding="utf-8")
        if p.is_file()
        else "Missing queue/QUEUE_INSTRUCTIONS.md"
    )


@mcp.resource("repo://queue/QUEUE_AGENT_PROMPT.md")
def resource_queue_agent_prompt() -> str:
    """Executable queue agent behavior contract."""

    p = _REPO_ROOT / "queue" / "QUEUE_AGENT_PROMPT.md"
    return (
        p.read_text(encoding="utf-8")
        if p.is_file()
        else "Missing queue/QUEUE_AGENT_PROMPT.md"
    )


@mcp.resource("repo://prompts/queue_worker_executor.md")
def resource_queue_worker_executor_prompt() -> str:
    """Queue worker executor prompt (implementation agents)."""

    p = _REPO_ROOT / "prompts" / "queue_worker_executor.md"
    return (
        p.read_text(encoding="utf-8")
        if p.is_file()
        else "Missing prompts/queue_worker_executor.md"
    )


@mcp.resource("repo://prompts/skill_searcher.md")
def resource_skill_searcher_prompt() -> str:
    """Skill searcher subroutine — mandatory skill discovery."""

    p = _REPO_ROOT / "prompts" / "skill_searcher.md"
    return (
        p.read_text(encoding="utf-8")
        if p.is_file()
        else "Missing prompts/skill_searcher.md"
    )


@mcp.resource("repo://PYTHON_PROCEDURES.md")
def resource_python_procedures() -> str:
    """Python implementation procedures for API code."""

    p = _REPO_ROOT / "PYTHON_PROCEDURES.md"
    return (
        p.read_text(encoding="utf-8") if p.is_file() else "Missing PYTHON_PROCEDURES.md"
    )


@mcp.resource("repo://spec/spec.md")
def resource_spec() -> str:
    """Canonical full specification (large file)."""

    p = _REPO_ROOT / "spec" / "spec.md"
    return p.read_text(encoding="utf-8") if p.is_file() else "Missing spec/spec.md"


@mcp.prompt()
def start_queue_item() -> str:
    """Instructions to begin the top queue item without editing queue CSV."""

    return "\n".join(
        [
            "You are implementing work for this software-factory template repo.",
            "",
            "1. Read repo://queue/QUEUE_INSTRUCTIONS.md and",
            "   repo://queue/QUEUE_AGENT_PROMPT.md completely.",
            "2. Call tool queue_top_item() — **summary** in the JSON is the contract.",
            "3. Read every path in **related_files** via read_repo_file.",
            "4. Mandatory skill search: repo://skills/README.md or",
            '   run_make_target("skills:list").',
            "5. Branch: git checkout -b queue/<id>-short-slug using **id** from JSON.",
            "6. Do not edit queue CSV files (operators own the ledger).",
            "7. Before handoff: lint, typecheck, test (run_make_target).",
            "",
            "Put PR link in handoff; operators update queue notes if needed.",
        ],
    )


@mcp.prompt()
def mandatory_skill_search(task_description: str) -> str:
    """Structured skill search preamble for a concrete task."""

    return f"""Task (one paragraph): {task_description}

Follow prompts/skill_searcher.md:
1. Read repo://skills/README.md (full index).
2. Identify PRIMARY and SECONDARY domains for this task.
3. List at least 3 relevant skill paths from skills/ with one-line rationale each.
4. Read the full body of every high-relevance skill before planning code changes.

Do not skip categories — check init, agent-ops, repo-governance, backend, security,
testing, devops as applicable."""


@mcp.prompt()
def implement_feature_plan(feature_name: str) -> str:
    """Plan template aligned with AGENTS.md (acceptance, files, risks, scope bounds)."""

    return f"""Plan the following feature before writing code: {feature_name}

Include:
- Acceptance criteria (testable, from the task or queue summary).
- Files to create or modify (exhaustive list).
- Risks (security, tenancy, API contract, migrations).
- Scope bounds — what this change explicitly does not do.
- Definition of done (tests, docs, validation commands).

Follow PYTHON_PROCEDURES.md and apps/api router → service → repository layering."""


def main() -> None:
    """Entry point: stdio transport for Cursor / Claude / Codex MCP clients."""

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
