#!/usr/bin/env python3
"""Replace stub skill files with bodies derived from spec/spec.md summaries."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "spec.md"

FULL_ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*[^|]*\[FULL\][^|]*\|\s*([^|]+)\|\s*$",
    re.MULTILINE,
)


def load_full_skill_paths() -> set[str]:
    text = SPEC.read_text(encoding="utf-8")
    return {
        p
        for p, _ in FULL_ROW_RE.findall(text)
        if p.startswith("skills/") and p.endswith(".md")
    }

STUB_PATTERNS = (
    "Operational skill for this topic",
    "What this testing skill enables",
    "One paragraph describing what this skill enables",
)


def load_skill_summaries() -> dict[str, str]:
    """Same table parsing as enrich-docs-from-spec: path=col2, summary=col4."""
    text = SPEC.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 6:
            continue
        raw_path = parts[2].strip("` ").strip()
        if not raw_path.startswith("skills/") or not raw_path.endswith(".md"):
            continue
        summary = parts[4].strip()
        if not summary or summary == "---":
            continue
        if raw_path not in out:
            out[raw_path] = summary
    return out


def extract_header_comment(text: str) -> tuple[str, str, str]:
    """Return (title_line, comment_block, rest_of_file)."""
    lines = text.splitlines()
    if not lines:
        return "", "", ""
    title = lines[0]
    i = 1
    if i < len(lines) and lines[i].strip() == "":
        i += 1
    comment_lines: list[str] = []
    while i < len(lines) and lines[i].strip().startswith("<!--"):
        comment_lines.append(lines[i])
        i += 1
    if i < len(lines) and lines[i].strip() == "":
        i += 1
    comment = "\n".join(comment_lines)
    rest = "\n".join(lines[i:])
    return title, comment, rest


def is_stub(text: str) -> bool:
    return any(p in text for p in STUB_PATTERNS)


def category(rel: str) -> str:
    parts = rel.split("/")
    return parts[1] if len(parts) > 1 else "general"


def when_invoke(cat: str, summary: str) -> str:
    lines = [
        "- You are implementing or testing a change that matches the summary above.",
        "- You need a checklist before merging or handing off work in this area.",
    ]
    if cat == "testing":
        lines.insert(
            0,
            "- You are adding or changing async tests, HTTP client tests, or pytest-asyncio configuration.",
        )
    elif cat == "backend":
        lines.insert(
            0,
            "- You are changing FastAPI modules, configuration, jobs, or API behavior described in this skill.",
        )
    elif cat == "security":
        lines.insert(
            0,
            "- You are changing auth, secrets, dependencies, containers, or security documentation.",
        )
    elif cat == "devops":
        lines.insert(
            0,
            "- You are changing Docker, Kubernetes, CI workflows, or release automation.",
        )
    elif cat == "init":
        lines.insert(
            0,
            "- You are validating `idea.md`, seeding the queue, or running initialization scaffolding.",
        )
    elif cat == "frontend":
        lines.insert(
            0,
            "- The web or mobile profile is enabled and you are changing client integration code.",
        )
    elif cat == "ai-rag":
        lines.insert(
            0,
            "- The AI profile is enabled and you are changing RAG, embeddings, or model integration.",
        )
    elif cat == "repo-governance":
        lines.insert(
            0,
            "- You are editing AGENTS.md, rules, procedures, ADRs, or changelog policy.",
        )
    elif cat == "agent-ops":
        lines.insert(
            0,
            "- You are triaging queue items, planning work, or writing handoffs and audits.",
        )
    return "\n".join(f"{ln}" for ln in lines)


def prerequisites(cat: str) -> str:
    base = [
        "- Read root `AGENTS.md` and complete the mandatory skill search (`make skills-list` or `skills/README.md`).",
        "- Install dev dependencies: `pip install -e \".[dev]\"` (or use `./setup.sh`).",
    ]
    extra: list[str] = []
    if cat == "testing":
        extra.append("- `make test` runs clean locally before you push.")
    elif cat == "devops":
        extra.append("- Docker and/or `kubectl` available if you touch deploy manifests.")
    elif cat == "security":
        extra.append("- No secrets in code; use `.env` and `apps/api/src/config.py` only for settings.")
    return "\n".join(base + extra)


def relevant_files(cat: str, rel: str) -> str:
    common = [
        "- This skill file and `skills/README.md`",
        "- `docs/procedures/implement-change.md` and `docs/procedures/validate-change.md`",
    ]
    by_cat: dict[str, list[str]] = {
        "backend": [
            "- `apps/api/src/`",
            "- `packages/tasks/`",
            "- `apps/api/tests/`",
        ],
        "testing": [
            "- `apps/api/tests/`",
            "- `pyproject.toml` (pytest / asyncio)",
            "- `docs/quality/testing-strategy.md`",
        ],
        "security": [
            "- `docs/security/`",
            "- `.env.example`",
            "- `apps/api/src/auth/`",
        ],
        "devops": [
            "- `deploy/docker/`",
            "- `deploy/k8s/`",
            "- `.github/workflows/`",
        ],
        "init": [
            "- `idea.md`",
            "- `queue/queue.csv`",
            "- `scripts/`",
        ],
        "frontend": [
            "- `apps/web/` or `apps/mobile/` (when enabled)",
            "- `docs/optional-clients/`",
        ],
        "ai-rag": ["- `packages/ai/`", "- `docs/architecture/ai-rag-chromadb.md`"],
        "repo-governance": [
            "- `AGENTS.md`",
            "- `.cursor/rules/`",
            "- `docs/procedures/`",
        ],
        "agent-ops": [
            "- `queue/queue.csv`",
            "- `queue/QUEUE_INSTRUCTIONS.md`",
        ],
    }
    lines = common + by_cat.get(cat, ["- Repository paths implied by the task"])
    return "\n".join(lines)


def build_steps(cat: str) -> str:
    steps = [
        "1. Read the **Purpose** and **When to Invoke** sections above — confirm this skill applies.",
        "2. Inspect the code and docs listed under **Relevant Files/Areas**.",
        "3. Apply the change in small commits; keep scope aligned with `AGENTS.md` §6.",
        "4. Run `make lint`, `make fmt`, `make typecheck`, and `make test` (add focused pytest if needed).",
        "5. Update user-facing or operator docs if behavior changed.",
    ]
    if cat == "devops":
        steps.insert(4, "4b. Run `make k8s-validate` or `make image-build` when deploy artifacts change.")
    return "\n".join(steps)


def command_examples(cat: str) -> str:
    cmds = [
        "`make lint` — Ruff",
        "`make fmt` — format check",
        "`make typecheck` — mypy",
        "`make test` — full suite",
    ]
    if cat == "testing":
        cmds.append("`pytest apps/api/tests/ -q` — focused run")
    if cat == "devops":
        cmds.extend(["`make docker-up` / `make docker-down`", "`make k8s-validate`"])
    if cat == "agent-ops":
        cmds.extend(["`make queue-peek`", "`make queue-validate`", "`make audit-self`"])
    return "\n".join(f"- {c}" for c in cmds)


def render_skill(title: str, comment: str, rel: str, summary: str) -> str:
    cat = category(rel)
    parts: list[str] = [title]
    if comment:
        parts.extend(["", comment])
    parts.append("")
    parts.extend(
        [
            f"**Purpose:** {summary}",
            "",
            "## Purpose",
            "",
            summary,
            "",
            "## When to Invoke",
            "",
            when_invoke(cat, summary),
            "",
            "## Prerequisites",
            "",
            prerequisites(cat),
            "",
            "## Relevant Files/Areas",
            "",
            relevant_files(cat, rel),
            "",
            "## Step-by-Step Method",
            "",
            build_steps(cat),
            "",
            "## Command Examples",
            "",
            command_examples(cat),
            "",
            "## Validation Checklist",
            "",
            "- [ ] Change matches the skill summary and acceptance criteria for the task",
            "- [ ] `make lint`, `make fmt`, `make typecheck`, and `make test` pass",
            "- [ ] Docs or queue notes updated if required by the change",
            "",
            "## Common Failure Modes",
            "",
            "- **Scope creep**: fix unrelated issues in the same PR — split work per `AGENTS.md` §6.",
            "- **Skipping validation**: run the full `make` checks above before handoff.",
            "",
            "## Handoff Expectations",
            "",
            "- List files changed, commands run with key output, risks, and follow-ups (see `skills/agent-ops/implementation-handoff.md`).",
            "",
            "## Related Procedures",
            "",
            "`docs/procedures/implement-change.md`, `docs/procedures/validate-change.md`",
            "",
            "## Related Prompts",
            "",
            "`prompts/implementation_agent.md`, `prompts/task_planner.md`",
            "",
            "## Related Rules",
            "",
            "`.cursor/rules/global.md`, `PYTHON_PROCEDURES.md` where applicable",
            "",
        ]
    )
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    summaries = load_skill_summaries()
    full_paths = load_full_skill_paths()
    updated = 0
    for md in sorted((ROOT / "skills").rglob("*.md")):
        if md.name == "README.md":
            continue
        rel = str(md.relative_to(ROOT)).replace("\\", "/")
        if rel in full_paths:
            continue
        summary = summaries.get(rel)
        if not summary:
            print(f"skip (no spec row): {rel}", file=sys.stderr)
            continue
        text = md.read_text(encoding="utf-8")
        if not is_stub(text):
            continue
        title, comment, _rest = extract_header_comment(text)
        if not title.startswith("# "):
            continue
        new_body = render_skill(title, comment, rel, summary)
        md.write_text(new_body, encoding="utf-8")
        print(rel)
        updated += 1
    print(f"Patched {updated} stub skill files.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
