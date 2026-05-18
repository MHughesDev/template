# packages/queue_ops/test_queue_ops.py
"""Tests for queue CSV helpers used by Make scripts."""

from __future__ import annotations

import csv
from pathlib import Path

from packages.queue_ops import OPEN_FIELDS, load_open_rows, validate_open


def _minimal_row(**overrides: str) -> dict[str, str]:
    row = dict.fromkeys(OPEN_FIELDS, "")
    row.update(
        {
            "id": "Q-999",
            "batch": "b1",
            "phase": "1",
            "category": "infrastructure",
            "complexity": "S",
            "goal": "Example goal",
            "acceptance_criteria": "1. First criterion is met",
            "touch_files": "README.md",
        }
    )
    row.update(overrides)
    return row


def test_load_open_rows_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "queue.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OPEN_FIELDS)
        w.writeheader()
        w.writerow(_minimal_row(goal="Round-trip goal"))
    rows = load_open_rows(p)
    assert len(rows) == 1
    assert rows[0]["id"] == "Q-999"
    assert rows[0]["goal"] == "Round-trip goal"


def test_validate_open_passes_minimal_row(tmp_path: Path) -> None:
    p = tmp_path / "queue.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OPEN_FIELDS)
        w.writeheader()
        w.writerow(_minimal_row())
    assert validate_open(p) == []


def test_validate_open_rejects_acceptance_without_numbered_item(tmp_path: Path) -> None:
    p = tmp_path / "queue.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OPEN_FIELDS)
        w.writeheader()
        w.writerow(_minimal_row(acceptance_criteria="no numbered prefix here"))
    errs = validate_open(p)
    assert errs
    assert any("acceptance_criteria must contain" in e for e in errs)
