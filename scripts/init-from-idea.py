# scripts/init-from-idea.py
"""Orchestrator: execute init-manifest.json resolved_decisions (stdlib only)."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd), check=True)


def _append_pyproject_dependency(pyproject: Path, dep: str) -> bool:
    text = pyproject.read_text(encoding="utf-8")
    if dep in text:
        print(f"dependency already in pyproject.toml: {dep}")
        return False
    m = re.search(
        r"(dependencies = \[\n)([\s\S]*?)(\n\]\n\n\[project\.optional-dependencies\])",
        text,
    )
    if not m:
        raise RuntimeError(
            "Could not find [project] dependencies block in pyproject.toml"
        )
    inner = m.group(2).rstrip()
    line = f'  "{dep}",'
    new_inner = inner + "\n" + line if inner else line
    new_text = m.group(1) + new_inner + m.group(3)
    pyproject.write_text(
        text[: m.start()] + new_text + text[m.end() :], encoding="utf-8"
    )
    return True


def _append_env(path: Path, key: str, value: str, added_keys: list[str]) -> None:
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8")
    if re.search(rf"^{re.escape(key)}=", content, re.MULTILINE):
        print(f"already present: {key} ({path.name})")
        return
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n# Added by init-from-idea\n{key}={value}\n")
    added_keys.append(key)


def _source_script(root: Path, path: Path) -> None:
    if not path.is_file():
        print(f"WARN: missing {path}")
        return
    quoted = str(path).replace("'", "'\"'\"'")
    subprocess.run(
        ["/usr/bin/env", "bash", "-c", f"set -euo pipefail; source '{quoted}'"],
        cwd=str(root),
        check=True,
    )


def _update_idea_md(
    idea: Path,
    *,
    init_version: str,
    profiles_enabled: str,
    modules_str: str,
    queue_count: str,
) -> None:
    text = idea.read_text(encoding="utf-8")
    ts = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = re.sub(r"(initialized:\s*)\S+", r"\1true", text, count=1)
    text = re.sub(r"(init_completed_at:\s*)\S+", rf'\1"{ts}"', text, count=1)
    text = re.sub(
        r"(\|\s*Status\s*\|\s*`)([^`]+)(`\s*\|)",
        r"\1initialized\3",
        text,
        count=1,
    )
    text = re.sub(
        r"(\|\s*Manifest version\s*\|\s*)([^|]+)(\|)",
        rf"\1`{init_version}`\3",
        text,
        count=1,
    )
    text = re.sub(
        r"(\|\s*Executed at\s*\|\s*)([^|]+)(\|)",
        rf"\1`{ts}`\3",
        text,
        count=1,
    )
    text = re.sub(
        r"(\|\s*Profiles enabled\s*\|\s*)([^|]+)(\|)",
        rf"\1`{profiles_enabled}`\3",
        text,
        count=1,
    )
    text = re.sub(
        r"(\|\s*Contexts scaffolded\|\s*)([^|]+)(\|)",
        rf"\1`{modules_str}`\3",
        text,
        count=1,
    )
    text = re.sub(
        r"(\|\s*Queue rows seeded\s*\|\s*)([^|]+)(\|)",
        rf"\1`{queue_count}`\3",
        text,
        count=1,
    )
    text = re.sub(
        r"(\|\s*Init PR\s*\|\s*)([^|]+)(\|)",
        r"\1— pending PR\3",
        text,
        count=1,
    )
    idea.write_text(text, encoding="utf-8")


def _seed_queue(root: Path, rows: list[dict[str, str]]) -> int:
    qpath = root / "queue" / "queue.csv"
    raw = qpath.read_text(encoding="utf-8").splitlines()
    start = 1 if raw and raw[0].startswith("#") else 0
    comment = (raw[0] + "\n") if start else ""
    reader = csv.DictReader(io.StringIO("\n".join(raw[start:])))
    fieldnames = list(reader.fieldnames or [])
    existing = list(reader)
    have = {r.get("id", "") for r in existing}
    added = 0
    for r in rows:
        rid = r.get("id", "")
        if rid in have:
            print(f"skip queue row (exists): {rid}")
            continue
        row = {k: r.get(k, "") for k in fieldnames}
        existing.append(row)
        have.add(rid)
        added += 1
    buf = io.StringIO()
    if comment:
        buf.write(comment)
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(existing)
    qpath.write_text(buf.getvalue(), encoding="utf-8")
    return added


def _compose_profiles_from_services(services: list[str]) -> str:
    parts: list[str] = []
    if "db" in services:
        parts.append("db")
    if "redis" in services or "worker" in services:
        parts.append("worker")
    if "chroma" in services:
        parts.append("ai")
    if "nginx" in services:
        parts.append("web")
    return ",".join(parts)


def _set_compose_profiles_env(root: Path, profiles_csv: str) -> None:
    env_path = root / ".env"
    line = f"COMPOSE_PROFILES={profiles_csv}\n"
    if env_path.is_file():
        text = env_path.read_text(encoding="utf-8")
        if re.search(r"^COMPOSE_PROFILES=", text, re.MULTILINE):
            print("COMPOSE_PROFILES already in .env")
            return
        with env_path.open("a", encoding="utf-8") as f:
            f.write("\n# Added by init-from-idea\n" + line)
    else:
        env_path.write_text("# Added by init-from-idea\n" + line, encoding="utf-8")
    print(f"Set COMPOSE_PROFILES={profiles_csv} in .env")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    log_path = root / "init-manifest.log"
    manifest_path = root / "init-manifest.json"

    def log(msg: str) -> None:
        line = f"{datetime.now(tz=UTC).isoformat()} {msg}\n"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line)
        print(msg, flush=True)

    if not manifest_path.is_file():
        print("Run 'make idea:parse' first.", file=sys.stderr)
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in init-manifest.json: {e}", file=sys.stderr)
        return 1

    rd = manifest.get("resolved_decisions") or {}
    meta = manifest.get("meta") or {}
    project = manifest.get("project") or {}
    archetype = str(manifest.get("archetype", ""))

    profiles_enabled: list[str] = list(rd.get("profiles_enabled") or [])
    profiles_discarded: list[str] = list(rd.get("profiles_discarded") or [])
    compose_services: list[str] = list(rd.get("compose_services") or ["api"])
    py_deps: list[str] = list(rd.get("python_dependencies") or [])
    env_vars: dict[str, str] = dict(rd.get("env_vars") or {})
    modules: list[str] = list(rd.get("modules_to_scaffold") or [])
    queue_rows: list[dict[str, str]] = list(rd.get("queue_seed_rows") or [])

    deps_added: list[str] = []
    env_keys_added: list[str] = []

    log("STEP 2: profile scripts")
    profiles_dir = root / "scripts" / "profiles"
    for p in profiles_enabled:
        _source_script(root, profiles_dir / f"enable-{p}.sh")
    for p in profiles_discarded:
        _source_script(root, profiles_dir / f"discard-{p}.sh")

    prof_csv = _compose_profiles_from_services(compose_services)
    if prof_csv:
        _set_compose_profiles_env(root, prof_csv)
    log(f"Compose services (logical): {', '.join(compose_services)}")

    log("STEP 4: Python dependencies")
    pyproject = root / "pyproject.toml"
    for dep in py_deps:
        if _append_pyproject_dependency(pyproject, dep):
            deps_added.append(dep)
    if deps_added:
        _run([sys.executable, "-m", "pip", "install", "-e", ".[dev]", "--quiet"], root)

    log("STEP 5: env vars")
    for k, v in env_vars.items():
        _append_env(root / ".env.example", k, v, env_keys_added)
        _append_env(root / ".env", k, v, env_keys_added)

    log("STEP 6: scaffold modules")
    for mod in modules:
        mod_path = root / "apps" / "api" / "src" / mod
        if mod_path.is_dir():
            print(f"skip scaffold: module already exists: {mod}")
            continue
        env = os.environ.copy()
        env["MODULE"] = mod
        subprocess.run(
            ["make", "-C", str(root), "scaffold-module"],
            env=env,
            check=True,
        )

    log("STEP 7: queue seeding")
    seeded = 0
    if queue_rows:
        seeded = _seed_queue(root, queue_rows)
    _run(["make", "-C", str(root), "queue-validate"], root)

    log("STEP 8: codebase summary")
    _run(["make", "-C", str(root), "codebase-summary"], root)

    log("STEP 9: validation suite")
    for target in (
        "lint",
        "fmt-check",
        "typecheck",
        "test",
        "queue-validate",
        "audit-self",
    ):
        _run(["make", "-C", str(root), target], root)

    init_version = str(meta.get("init_version", "2.0"))
    _update_idea_md(
        root / "idea.md",
        init_version=init_version,
        profiles_enabled=", ".join(profiles_enabled),
        modules_str=", ".join(modules),
        queue_count=str(len(queue_rows)),
    )

    mhash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    display_name = str(project.get("display_name", "project"))
    commit_msg = (
        f"feat(init): execute initialization from idea.md manifest\n\n"
        f"Archetype: {archetype}\n"
        f"Profiles enabled: {', '.join(profiles_enabled)}\n"
        f"Profiles discarded: {', '.join(profiles_discarded)}\n"
        f"Contexts scaffolded: {', '.join(modules)}\n"
        f"Queue rows seeded: {len(queue_rows)}\n\n"
        f"Generated by: make idea:execute\n"
        f"Manifest hash: {mhash}\n"
    )
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=False)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", commit_msg],
        check=False,
    )

    pr_body = f"""## Initialization PR — {display_name}

This PR was generated by `make idea:execute` from `idea.md`.

### Archetype
{archetype}

### Resolved profile decisions
| Profile | Decision | Source |
|---|---|---|
| (see `init-manifest.json` → `profiles`) | | |

### Modules scaffolded
{", ".join(modules)}

### Dependencies added
{", ".join(deps_added) or "none"}

### Env vars added (keys only)
{", ".join(env_keys_added) or "none"}

### Queue seeded
{len(queue_rows)} items. Run `make queue:peek` to inspect.

### Open questions requiring human resolution
See `idea.md` §16.

### Validation evidence
- [x] `make lint` — passed
- [x] `make fmt-check` — passed
- [x] `make typecheck` — passed
- [x] `make test` — passed
- [x] `make queue:validate` — passed
- [x] `make audit:self` — passed

### Merge instructions
Review the diff carefully. Pay special attention to:
1. Module scaffolding under `apps/api/src/`
2. New env vars in `.env.example`
3. Queue state in `queue/queue.csv`
4. Open questions in `idea.md` §16 — resolve before building

After merging: `git branch -d feature/idea-init-engine && git push origin --delete feature/idea-init-engine`
"""
    gh = shutil.which("gh")
    if gh:
        pr_cmd = [
            gh,
            "pr",
            "create",
            "--title",
            f"feat: initialize repository from idea.md — {display_name}",
            "--body",
            pr_body,
            "--base",
            "main",
            "--label",
            "initialization",
            "--label",
            "automated",
        ]
        subprocess.run(pr_cmd, cwd=str(root), check=False)
    else:
        print(
            "gh CLI not found — open a PR manually from branch "
            + subprocess.check_output(
                ["git", "-C", str(root), "branch", "--show-current"],
                text=True,
            ).strip(),
        )

    print("✓ Profiles enabled     :", ", ".join(profiles_enabled))
    print("✓ Profiles discarded   :", ", ".join(profiles_discarded))
    print("✓ Modules scaffolded   :", ", ".join(modules))
    print("✓ Queue rows seeded    :", len(queue_rows), f"(new rows appended: {seeded})")
    print("✓ Dependencies added   :", ", ".join(deps_added) or "(none)")
    print("✓ Env vars added       :", ", ".join(env_keys_added) or "(none)")
    print("✓ All validation passed")
    print("→ PR: see gh output above or create manually")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
