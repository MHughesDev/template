#!/usr/bin/env bash
# scripts/queue-validate.sh
# Validate queue CSV schema, categories, summary length, and dependency graph.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

exec python3 - "$ROOT" <<'PY'
"""Queue CSV validation (invoked from queue-validate.sh)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(sys.argv[1])

QUEUE_HEADER = (
    "id",
    "batch",
    "phase",
    "category",
    "summary",
    "dependencies",
    "notes",
    "created_date",
)
ARCHIVE_HEADER = QUEUE_HEADER + ("status", "completed_date")

DEFAULT_CATEGORIES = frozenset(
    {
        "core-api",
        "infrastructure",
        "testing",
        "documentation",
        "bugfix",
        "refactor",
        "security",
        "devops",
    }
)


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        raise SystemExit(f"error: {path} has no data rows")
    reader = csv.DictReader(lines)
    header = reader.fieldnames
    if header is None:
        raise SystemExit(f"error: {path} missing header")
    rows = [row for row in reader if any(v.strip() for v in row.values())]
    return list(header), rows


def validate_file(path: Path, expected: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing file: {path.relative_to(REPO)}"]

    header, rows = load_rows(path)
    if tuple(header) != expected:
        errors.append(
            f"{path.relative_to(REPO)}: header mismatch — expected {expected}, got {tuple(header)}"
        )
        return errors

    ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        qid = row.get("id", "").strip()
        if not qid:
            errors.append(f"{path.relative_to(REPO)}: row {i}: empty id")
            continue
        if qid in ids:
            errors.append(f"{path.relative_to(REPO)}: row {i}: duplicate id {qid}")
        ids.add(qid)

        cat = row.get("category", "").strip()
        if not cat:
            errors.append(f"{path.relative_to(REPO)}: row {i} ({qid}): category required")
        elif cat not in DEFAULT_CATEGORIES:
            errors.append(
                f"{path.relative_to(REPO)}: row {i} ({qid}): unknown category {cat!r} "
                f"(must be listed in docs/queue/queue-categories.md)"
            )

        summary = row.get("summary", "").strip()
        if summary and len(summary) < 100:
            errors.append(
                f"{path.relative_to(REPO)}: row {i} ({qid}): summary must be ≥100 characters "
                f"(found {len(summary)})"
            )

        deps = row.get("dependencies", "").strip()
        if deps:
            for d in [x.strip() for x in deps.split(",") if x.strip()]:
                if d == qid:
                    errors.append(
                        f"{path.relative_to(REPO)}: row {i} ({qid}): self-dependency {d}"
                    )

    # Cycle detection: prerequisite u must complete before dependent v (edge u -> v).
    if path.name == "queue.csv" and rows:
        from collections import defaultdict

        adj: dict[str, list[str]] = defaultdict(list)
        nodes: set[str] = set()
        for r in rows:
            rid = r.get("id", "").strip()
            if not rid:
                continue
            nodes.add(rid)
            raw = r.get("dependencies", "").strip()
            for u in [x.strip() for x in raw.split(",") if x.strip()]:
                nodes.add(u)
                adj[u].append(rid)

        state: dict[str, str] = {}

        def dfs(u: str) -> bool:
            state[u] = "gray"
            for v in adj.get(u, []):
                if state.get(v) == "gray":
                    return True
                if state.get(v) == "black":
                    continue
                if dfs(v):
                    return True
            state[u] = "black"
            return False

        for n in sorted(nodes):
            if n not in state:
                if dfs(n):
                    errors.append(f"{path.relative_to(REPO)}: circular dependencies detected")
                    break

    if path.name == "queuearchive.csv":
        for i, row in enumerate(rows, start=2):
            qid = row.get("id", "").strip()
            st = row.get("status", "").strip().lower()
            if st not in {"done", "cancelled", "superseded"}:
                errors.append(
                    f"{path.relative_to(REPO)}: row {i} ({qid}): invalid status {st!r}"
                )
            cd = row.get("completed_date", "").strip()
            if st and not cd:
                errors.append(
                    f"{path.relative_to(REPO)}: row {i} ({qid}): completed_date required when status set"
                )

    return errors


def main() -> None:
    q = REPO / "queue" / "queue.csv"
    a = REPO / "queue" / "queuearchive.csv"
    err: list[str] = []
    err.extend(validate_file(q, QUEUE_HEADER))
    err.extend(validate_file(a, ARCHIVE_HEADER))

    if err:
        print("queue validation failed:", file=sys.stderr)
        for e in err:
            print(f"  - {e}", file=sys.stderr)
        raise SystemExit(1)
    print("queue validation OK")


if __name__ == "__main__":
    main()
PY
