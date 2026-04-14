# skills/testing/coverage-ratchet.py
"""Read coverage.xml and fail if total line-rate is below --min (default from pyproject)."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml", type=Path, default=Path("coverage.xml"))
    parser.add_argument("--min", type=float, default=55.0, dest="min_cov")
    args = parser.parse_args()
    if not args.xml.is_file():
        print(f"Missing {args.xml} — run pytest with coverage first.", file=sys.stderr)
        return 1
    tree = ET.parse(args.xml)
    root = tree.getroot()
    rate = float(root.attrib.get("line-rate", "0")) * 100
    print(f"Total line coverage: {rate:.2f}%")
    if rate < args.min_cov:
        print(f"Below floor {args.min_cov}%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
