# skills/init/queue-seeder.py
"""Seed queue/queue.csv from idea.md section 12 (Initial queue items) or --spec file."""

from __future__ import annotations

import argparse
import csv
import io
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


def _run_queue_validate(repo_root: Path) -> int:
    script = repo_root / "scripts" / "queue_validate.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(repo_root),
        check=False,
    )
    return proc.returncode


def _parse_idea_section_12(text: str) -> list[tuple[str, str, str]]:
    """Return (priority, category, summary) rows from markdown table under section 12."""

    lines = text.splitlines()
    in_section = False
    header_seen = False
    rows: list[tuple[str, str, str]] = []
    for line in lines:
        if re.match(r"^##\s+12\.(\s|$)", line):
            in_section = True
            continue
        if in_section and line.startswith("## ") and not re.match(r"^##\s+12\.", line):
            break
        if not in_section:
            continue
        if "Priority" in line and "Category" in line and "Summary" in line:
            header_seen = True
            continue
        if "|---" in line or line.strip().startswith("|---"):
            continue
        if not header_seen or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3:
            continue
        priority, category, summary = parts[0], parts[1], parts[2]
        if priority.startswith("<!--") or "add rows" in priority.lower():
            continue
        if not summary or summary.startswith("<!--"):
            continue
        rows.append((priority, category, summary))
    return rows


def _append_rows_from_idea(
    repo_root: Path, idea_path: Path, replace_existing: bool
) -> int:
    text = idea_path.read_text(encoding="utf-8")
    parsed = _parse_idea_section_12(text)
    if not parsed:
        print(
            "No queue rows parsed from idea.md §12 (table with Priority | Category | Summary).",
            file=sys.stderr,
        )
        return 1

    qpath = repo_root / "queue" / "queue.csv"
    raw = qpath.read_text(encoding="utf-8")
    lines = raw.splitlines()
    start = 1 if lines and lines[0].startswith("#") else 0
    comment = (lines[0] + "\n") if start else ""
    reader = csv.DictReader(io.StringIO("\n".join(lines[start:])))
    fieldnames = list(reader.fieldnames or [])
    existing = [] if replace_existing else list(reader)

    today = date.today().isoformat()
    batch = 1
    for i, (priority, category, summary) in enumerate(parsed, start=1):
        qid = f"IDEA-{i:03d}"
        existing.append(
            {
                "id": qid,
                "batch": str(batch),
                "phase": str(priority).strip() or "1",
                "category": category.strip() or "init",
                "summary": summary.strip(),
                "dependencies": "",
                "notes": "from idea.md §12",
                "created_date": today,
            },
        )

    buf = io.StringIO()
    if comment:
        buf.write(comment)
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(existing)
    qpath.write_text(buf.getvalue(), encoding="utf-8")
    print(f"Wrote {len(parsed)} rows to {qpath}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed queue from idea.md or spec file")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--spec", type=Path, help="Lines: id|long summary text")
    parser.add_argument(
        "--from-idea",
        action="store_true",
        help="Parse idea.md section 12 and append/replace queue rows",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="With --from-idea: replace existing data rows (default: append IDEA-* rows)",
    )
    args = parser.parse_args()
    qpath = args.repo_root / "queue" / "queue.csv"
    if not qpath.is_file():
        print("Missing queue.csv", file=sys.stderr)
        return 1

    if args.from_idea:
        idea = args.repo_root / "idea.md"
        if not idea.is_file():
            print("Missing idea.md", file=sys.stderr)
            return 1
        rc = _append_rows_from_idea(args.repo_root, idea, args.replace)
        if rc != 0:
            return rc
        v = _run_queue_validate(args.repo_root)
        return v

    if not args.spec or not args.spec.is_file():
        print("Provide --from-idea or --spec file with rows id|summary")
        return 0

    raw = qpath.read_text(encoding="utf-8")
    lines = raw.splitlines()
    start = 1 if lines and lines[0].startswith("#") else 0
    comment = (lines[0] + "\n") if start else ""
    reader = csv.DictReader(io.StringIO("\n".join(lines[start:])))
    fieldnames = list(reader.fieldnames or [])
    existing = list(reader)
    today = date.today().isoformat()
    for line in args.spec.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 1)
        if len(parts) != 2:
            continue
        qid, summary = parts[0].strip(), parts[1].strip()
        existing.append(
            {
                "id": qid,
                "batch": "1",
                "phase": "1",
                "category": "init",
                "summary": summary,
                "dependencies": "",
                "notes": "",
                "created_date": today,
            },
        )
    buf = io.StringIO()
    if comment:
        buf.write(comment)
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(existing)
    qpath.write_text(buf.getvalue(), encoding="utf-8")
    print(f"Updated {qpath}")
    return _run_queue_validate(args.repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
