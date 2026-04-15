#!/usr/bin/env bash
# scripts/validate-idea.sh
# Pre-parse validation for idea.md — deterministic checks before init-manifest generation.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FILE="$ROOT/idea.md"

if [[ ! -f "$FILE" ]]; then
  echo "✗ ERROR: idea.md not found in repo root." >&2
  exit 1
fi

exec python3 - "$FILE" <<'PY'
"""Validate idea.md for initialization (pre-parse). Exit 1 if any hard errors."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    def check_meta() -> None:
        if re.search(r"<!--\s*INIT_META", text):
            print("✓ INIT_META block is present")
        else:
            errors.append(
                "INIT_META block missing — add <!-- INIT_META ... --> after the H1 in idea.md."
            )

    def check_initialized() -> None:
        m = re.search(r"initialized:\s*(\S+)", text)
        if m and m.group(1).strip().lower() not in ("false", "no", "0"):
            errors.append(
                "This repo is already initialized. To re-initialize, set initialized: false in "
                "idea.md and confirm you understand this will re-run initialization."
            )
        else:
            print("✓ INIT_META initialized is false (or unset)")

    def section_span(num: int) -> str:
        sec_m = re.search(rf"^##\s+{num}\.", text, re.MULTILINE)
        if not sec_m:
            return ""
        start = sec_m.start()
        rest = text[start:]
        next_m = re.search(r"^##\s+", rest[1:], re.MULTILINE)
        return rest[: next_m.start() + 1] if next_m else rest

    def check_placeholders_required() -> None:
        bad = False
        for num in (1, 3, 4, 6, 7, 9):
            sec = section_span(num)
            if sec and "<!--" in sec:
                errors.append(
                    f"Section {num} still contains `<!--` HTML comment placeholders — "
                    "replace with real content."
                )
                bad = True
        if not bad:
            print("✓ Required sections (1, 3, 4, 6, 7, 9) have no <!-- placeholders")

    def warn_optional_placeholders() -> None:
        for num in (2, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17):
            sec = section_span(num)
            if sec and "<!--" in sec:
                warnings.append(
                    f"Section {num} still contains HTML comment placeholders (warning only)."
                )

    def check_archetype() -> None:
        sec3 = section_span(3)
        selected = 0
        for line in sec3.splitlines():
            if not line.strip().startswith("|"):
                continue
            if "Archetype" in line and "Select" in line:
                continue
            if "|---" in line or re.match(r"^\|\s*[-:]+", line):
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2 and "[x]" in parts[1].lower():
                selected += 1
        if selected == 1:
            print("✓ §3 Archetype: exactly one [x] in Select column")
        else:
            errors.append(
                f"§3 Archetype: exactly one row must have [x] in the Select column (found {selected})."
            )

    def check_profiles() -> None:
        sec5 = section_span(5)
        unanswered: list[str] = []
        in_table = False
        header = False
        for line in sec5.splitlines():
            if "| Profile |" in line or ("Profile" in line and "Enable?" in line):
                in_table = True
                continue
            if not in_table:
                continue
            if "|---" in line or line.strip().startswith("|---"):
                header = True
                continue
            if not header or not line.strip().startswith("|"):
                break
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 2:
                continue
            label = parts[0].strip("*").strip()
            cell = parts[1]
            if re.search(r"\[x\]\s*yes", cell, re.I) or re.search(r"\[x\]\s*no", cell, re.I):
                continue
            if re.search(r"\[\s*\]", cell) and "[x]" not in cell.lower():
                unanswered.append(label)
            else:
                unanswered.append(f"{label} (invalid Enable? cell)")
        if not unanswered:
            print("✓ §5 Profiles: every row answered with [x] yes or [x] no")
        else:
            errors.append(
                "§5 Profiles: every row must be `[x] yes` or `[x] no` — unanswered or invalid: "
                + "; ".join(unanswered)
            )

    def check_bounded_contexts() -> None:
        sub_m = re.search(r"^###\s+4\.2", text, re.MULTILINE)
        ctx_names: list[str] = []
        if sub_m:
            lines = text[sub_m.start() :].splitlines()
            header_seen = False
            for line in lines[1:]:
                if line.startswith("### "):
                    break
                if line.strip().startswith("|") and "Context name" in line:
                    header_seen = True
                    continue
                if "|---" in line or line.strip().startswith("|---"):
                    continue
                if not header_seen or not line.strip().startswith("|"):
                    continue
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) < 3:
                    continue
                name = parts[0].strip("`").strip()
                if not name or name.startswith("<!--") or "e.g." in name.lower() or "<!--" in name:
                    continue
                ctx_names.append(name.lower())
        if ctx_names:
            print("✓ §4.2 Bounded contexts: at least one non-placeholder row")
        else:
            errors.append(
                "§4.2 Bounded contexts: at least one non-placeholder row is required in the table."
            )
        dupes = {n for n in ctx_names if ctx_names.count(n) > 1}
        if dupes:
            errors.append(f"§4.2 Duplicate context names: {sorted(dupes)}")
        elif ctx_names:
            print("✓ §4.2 No duplicate context names")

    def check_queue() -> None:
        qrows = 0
        in12 = False
        h12 = False
        for line in text.splitlines():
            if re.match(r"^##\s+12\.", line):
                in12 = True
                continue
            if in12 and line.startswith("## ") and not re.match(r"^##\s+12\.", line):
                break
            if not in12:
                continue
            if "Priority" in line and "Category" in line and "Summary" in line:
                h12 = True
                continue
            if "|---" in line or line.strip().startswith("|---"):
                continue
            if not h12 or "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 3:
                continue
            pr, summ = parts[0], parts[2]
            if pr.startswith("<!--") or "add rows" in pr.lower():
                continue
            if not summ or summ.startswith("<!--"):
                continue
            qrows += 1
        if qrows >= 1:
            print("✓ §12 Initial queue items: at least one non-placeholder row")
        else:
            errors.append(
                "§12 Initial queue items: at least one non-placeholder row is required."
            )

    check_meta()
    check_initialized()
    check_placeholders_required()
    warn_optional_placeholders()
    check_archetype()
    check_profiles()
    check_bounded_contexts()
    check_queue()

    for w in warnings:
        print(f"⚠ WARNING: {w}", file=sys.stderr)

    for e in errors:
        print(f"✗ ERROR: {e}", file=sys.stderr)

    if errors:
        return 1
    print("idea:validate OK — zero errors (warnings are acceptable).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
PY
