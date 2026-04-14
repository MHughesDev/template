# skills/agent-ops/queue-intelligence.py
"""Parse queue.csv; detect cycles via Kahn's algorithm; print a safe processing order."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict, deque
from pathlib import Path


def load_graph(path: Path) -> dict[str, list[str]]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    start = 1 if lines and lines[0].startswith("#") else 0
    reader = csv.DictReader(io.StringIO("\n".join(lines[start:])))
    rows = list(reader)
    ids = {(row.get("id") or "").strip() for row in rows if (row.get("id") or "").strip()}
    graph: dict[str, list[str]] = {}
    for row in rows:
        qid = (row.get("id") or "").strip()
        if not qid:
            continue
        deps = [d.strip() for d in (row.get("dependencies") or "").split(",") if d.strip()]
        graph[qid] = [d for d in deps if d in ids]
    return graph


def kahn(graph: dict[str, list[str]]) -> tuple[list[str] | None, bool]:
    """Return (topological_order, has_cycle)."""
    indeg = {n: 0 for n in graph}
    adj: dict[str, list[str]] = defaultdict(list)
    for n, deps in graph.items():
        for d in deps:
            if d in graph:
                indeg[n] += 1
                adj[d].append(n)
    q: deque[str] = deque(sorted(k for k, v in indeg.items() if v == 0))
    out: list[str] = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(out) != len(graph):
        return None, True
    return out, False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    path = args.repo_root / "queue" / "queue.csv"
    if not path.is_file():
        print(f"Missing {path}", file=sys.stderr)
        return 1
    graph = load_graph(path)
    if not graph:
        print("No queue rows with ids.")
        return 0
    order, cyc = kahn(graph)
    if cyc or order is None:
        print("Cycle detected in queue dependencies.")
        return 1
    print("OK — dependency DAG has no cycles.")
    print("Suggested order:", ", ".join(order))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
