# scripts/queue_validate.py
"""Validate queue/queue.csv and queue/queuearchive.csv schema and invariants."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

OPEN_HEADER = [
    "id",
    "batch",
    "phase",
    "category",
    "summary",
    "agent_instructions",
    "dependencies",
    "related_files",
    "notes",
    "created_date",
]
ARCHIVE_HEADER = OPEN_HEADER + ["status", "completed_date"]
MIN_SUMMARY_LEN = 100


def _read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = 0
    if lines and lines[0].startswith("#"):
        start = 1
    reader = csv.DictReader(lines[start:])
    if reader.fieldnames is None:
        msg = f"{path}: missing header"
        raise ValueError(msg)
    header = [h.strip() for h in reader.fieldnames]
    rows = list(reader)
    return header, rows


def validate_open(path: Path) -> list[str]:
    errors: list[str] = []
    header, rows = _read_rows(path)
    if header != OPEN_HEADER:
        errors.append(f"{path}: expected header {OPEN_HEADER}, got {header}")
        return errors
    for i, row in enumerate(rows, start=1):
        summary = (row.get("summary") or "").strip()
        if summary and len(summary) < MIN_SUMMARY_LEN:
            errors.append(
                f"{path} row {i}: summary must be empty or >= {MIN_SUMMARY_LEN} chars (got {len(summary)})",
            )
    return errors


def validate_archive(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return errors
    header, _rows = _read_rows(path)
    if header != ARCHIVE_HEADER:
        errors.append(f"{path}: expected header {ARCHIVE_HEADER}, got {header}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    q_open = root / "queue" / "queue.csv"
    q_arch = root / "queue" / "queuearchive.csv"
    errs: list[str] = []
    errs.extend(validate_open(q_open))
    errs.extend(validate_archive(q_arch))
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 1
    print("Queue OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
