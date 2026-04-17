# queue_ops/test_queue_ops.py
"""Tests for shared queue CSV helpers."""

from __future__ import annotations

import csv
from pathlib import Path

from queue_ops import OPEN_FIELDS, load_open_rows, validate_open


def test_load_open_rows_roundtrip(tmp_path: Path) -> None:
    long_summary = "x" * 100
    p = tmp_path / "queue.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OPEN_FIELDS)
        w.writeheader()
        w.writerow(
            dict.fromkeys(OPEN_FIELDS, "") | {"id": "Q-999", "summary": long_summary}
        )
    rows = load_open_rows(p)
    assert len(rows) == 1
    assert rows[0]["id"] == "Q-999"
    assert rows[0]["summary"] == long_summary


def test_validate_open_rejects_short_non_empty_summary(tmp_path: Path) -> None:
    p = tmp_path / "queue.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OPEN_FIELDS)
        w.writeheader()
        w.writerow(dict.fromkeys(OPEN_FIELDS, "") | {"id": "Q-001", "summary": "short"})
    errs = validate_open(p)
    assert errs
