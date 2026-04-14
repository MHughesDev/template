#!/usr/bin/env python3
"""Replace generic **Purpose:** stubs in docs/ with summaries from spec/spec.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "spec.md"
STUB_PHRASE = "Reference material for this topic. Align changes with spec/spec.md and AGENTS.md."
GENERIC_TAIL = (
    "See [AGENTS.md](../../AGENTS.md) for validation commands and "
    "[spec/spec.md](../../spec/spec.md) for the full specification."
)


def needs_refresh(text: str) -> bool:
    if STUB_PHRASE in text:
        return True
    if "**Purpose:** §" in text:
        return True
    if "Key content for " in text and "including commands" in text:
        return True
    return False

def load_doc_summaries() -> dict[str, str]:
    """Parse spec tables: path is column 2, summary is column 4 (0-based split after leading |)."""
    text = SPEC.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # ['', '125', '`docs/...`', 'REQUIRED', 'Summary...', 'Optional structure...', '']
        if len(parts) < 6:
            continue
        raw_path = parts[2].strip("` ").strip()
        if not raw_path.startswith("docs/") or not raw_path.endswith(".md"):
            continue
        summary = parts[4].strip()
        if not summary or summary == "---":
            continue
        if raw_path not in out:
            out[raw_path] = summary
    return out


def main() -> int:
    summaries = load_doc_summaries()
    updated = 0
    for md in sorted((ROOT / "docs").rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        if not needs_refresh(text):
            continue
        rel = str(md.relative_to(ROOT)).replace("\\", "/")
        summary = summaries.get(rel)
        if not summary:
            summary = (
                f"Documentation for `{rel}`. Align content with the implementation and "
                "`spec/spec.md`."
            )

        lines = text.splitlines()
        # Preserve title + optional <!-- --> block
        out: list[str] = []
        i = 0
        if lines:
            out.append(lines[0])
            i = 1
        if i < len(lines) and lines[i].strip() == "":
            out.append(lines[i])
            i += 1
        while i < len(lines) and lines[i].strip().startswith("<!--"):
            out.append(lines[i])
            i += 1
        if i < len(lines) and lines[i].strip() == "":
            out.append(lines[i])
            i += 1

        out.extend(
            [
                f"**Purpose:** {summary}",
                "",
                "## Overview",
                "",
                f"{summary} {GENERIC_TAIL}",
                "",
            ]
        )

        # Append any trailing content after the stub block (non-generic sections)
        rest = "\n".join(lines[i:])
        # Drop old **Purpose** through generic ## Content / ## Overview blocks
        rest = re.sub(
            r"\*\*Purpose:\*\*.*?## (?:Overview|Content|Key Sections)\s*\n.*?(?=\n## |\Z)",
            "",
            rest,
            flags=re.DOTALL,
        )
        rest = rest.strip()
        if rest:
            out.append(rest)
            if not rest.endswith("\n"):
                out.append("")

        new_text = "\n".join(out).rstrip() + "\n"
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            print(rel)
            updated += 1

    print(f"Updated {updated} docs.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
