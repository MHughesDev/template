# skills/init/profile-resolver.py
"""Resolve optional project profiles (web, mobile, ai, worker) and optional --apply scaffolding."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KNOWN_PROFILES = frozenset({"web", "mobile", "ai", "worker"})

PROFILE_DIRS: dict[str, list[str]] = {
    "web": ["apps/web"],
    "mobile": ["apps/mobile"],
    "ai": ["packages/ai"],
    "worker": ["packages/tasks"],
}


def _detect_from_idea(text: str) -> set[str]:
    t = text.lower()
    found: set[str] = set()
    if re.search(r"\b(next\.js|react|vite|web frontend|frontend)\b", t):
        found.add("web")
    if re.search(r"\b(expo|react native|mobile app|ios|android)\b", t):
        found.add("mobile")
    if re.search(r"\b(chroma|vector|embedding|rag|openai|llm)\b", t):
        found.add("ai")
    if re.search(r"\b(worker|celery|redis broker|rabbitmq|background job)\b", t):
        found.add("worker")
    return found


def _apply(repo_root: Path, profiles: set[str]) -> None:
    compose = repo_root / "docker-compose.yml"
    marker = "\n# Profile markers (added by profile-resolver --apply)\n"
    for p in sorted(profiles):
        for rel in PROFILE_DIRS.get(p, []):
            path = repo_root / rel
            path.mkdir(parents=True, exist_ok=True)
            gitkeep = path / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.write_text("", encoding="utf-8")
            print(f"Ensured directory {rel}/")
        marker += f"# enabled profile: {p}\n"
    if compose.is_file():
        text = compose.read_text(encoding="utf-8")
        if "Profile markers" not in text:
            compose.write_text(text.rstrip() + marker, encoding="utf-8")
            print(f"Appended profile markers to {compose}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve optional profiles for the template")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--profile",
        action="append",
        dest="profiles",
        help="Profile name (repeatable): web, mobile, ai, worker",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create placeholder directories and annotate docker-compose.yml",
    )
    args = parser.parse_args()
    repo_root: Path = args.repo_root

    selected: set[str] = set(args.profiles or [])
    if not selected:
        idea = repo_root / "idea.md"
        if idea.is_file():
            selected = _detect_from_idea(idea.read_text(encoding="utf-8"))
            print("Detected from idea.md:", ", ".join(sorted(selected)) or "(none)")
        else:
            print("No --profile and no idea.md — nothing to do.", file=sys.stderr)
            return 1

    bad = selected - KNOWN_PROFILES
    if bad:
        print(f"Unknown profile(s): {', '.join(sorted(bad))}", file=sys.stderr)
        print(f"Known: {', '.join(sorted(KNOWN_PROFILES))}", file=sys.stderr)
        return 1

    print("Enabled profiles:", ", ".join(sorted(selected)))
    for p in sorted(selected):
        print(f"  - {p}: directories {PROFILE_DIRS.get(p, [])}")

    if args.apply:
        _apply(repo_root, selected)
    else:
        print("(dry-run — pass --apply to create directories and update compose notes)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
