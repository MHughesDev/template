# scripts/init-from-idea.py
"""Orchestrator: execute init-manifest.json resolved_decisions (stdlib only)."""

from __future__ import annotations

import hashlib
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


def _compose_active_service_names(root: Path, profiles_csv: str) -> list[str]:
    """Resolve active service names via `docker compose config --services` (Step 3 visibility)."""

    env = os.environ.copy()
    if profiles_csv:
        env["COMPOSE_PROFILES"] = profiles_csv
    try:
        proc = subprocess.run(
            ["docker", "compose", "config", "--services"],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log_msg = f"STEP 3: could not list Compose services (docker unavailable): {exc}"
        print(log_msg, flush=True)
        return []
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        print(
            f"STEP 3: docker compose config --services failed: {err}",
            flush=True,
        )
        return []
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


def _verify_manifest_hash(manifest: dict[str, Any], manifest_path: Path) -> list[str]:
    """Re-compute SHA-256 of manifest (sans hash field) and compare to stored value."""
    stored_hash = (manifest.get("meta") or {}).get("init_manifest_hash")
    if not stored_hash:
        return ["init-manifest.json: init_manifest_hash is missing — re-run 'make idea:parse'."]
    meta_without_hash = dict(manifest.get("meta") or {})
    meta_without_hash.pop("init_manifest_hash", None)
    manifest_for_hash = {**manifest, "meta": meta_without_hash}
    raw = json.dumps(manifest_for_hash, sort_keys=True, ensure_ascii=False).encode()
    computed = hashlib.sha256(raw).hexdigest()
    if computed != stored_hash:
        return [
            f"init-manifest.json hash mismatch — file may have been edited after parsing.\n"
            f"  stored:   {stored_hash}\n"
            f"  computed: {computed}\n"
            "Re-run 'make idea:parse' to regenerate a clean manifest."
        ]
    return []


def _pr_already_exists(root: Path, branch: str) -> bool:
    """Return True if a PR for this branch already exists (via gh CLI)."""
    gh = shutil.which("gh")
    if not gh:
        return False
    result = subprocess.run(
        [gh, "pr", "list", "--head", branch, "--json", "number"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return False
    try:
        items = json.loads(result.stdout or "[]")
        return len(items) > 0
    except json.JSONDecodeError:
        return False


def main() -> int:
    import argparse as _argparse

    ap = _argparse.ArgumentParser(description="Execute init-manifest.json resolved decisions")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without modifying any files",
    )
    args = ap.parse_args()
    dry_run: bool = args.dry_run

    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    log_path = root / "init-manifest.log"
    manifest_path = root / "init-manifest.json"

    def log(msg: str) -> None:
        line = f"{datetime.now(tz=UTC).isoformat()} {msg}\n"
        if not dry_run:
            with log_path.open("a", encoding="utf-8") as f:
                f.write(line)
        print(("[DRY-RUN] " if dry_run else "") + msg, flush=True)

    if not manifest_path.is_file():
        print("Run 'make idea:parse' first.", file=sys.stderr)
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in init-manifest.json: {e}", file=sys.stderr)
        return 1

    # Verify manifest integrity before executing anything
    hash_errors = _verify_manifest_hash(manifest, manifest_path)
    if hash_errors:
        for err in hash_errors:
            print(f"✗ {err}", file=sys.stderr)
        return 1
    log("Manifest hash verified OK")

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

    if dry_run:
        print("\n--- DRY-RUN: planned actions ---")
        print(f"STEP 2: source enable scripts for: {', '.join(profiles_enabled)}")
        print(f"STEP 2: source discard scripts for: {', '.join(profiles_discarded)}")
        print(f"STEP 4: append python deps: {', '.join(py_deps) or '(none)'}")
        print(f"STEP 5: append env vars: {', '.join(sorted(env_vars)) or '(none)'}")
        print(f"STEP 6: scaffold modules: {', '.join(modules) or '(none)'}")
        print(f"STEP 7: seed {len(queue_rows)} queue row(s)")
        print("STEP 8: make codebase-summary")
        print("STEP 9: make lint fmt-check typecheck test queue-validate audit-self")
        print("STEP 10: git commit + open PR")
        print("--- end dry-run ---")
        return 0

    log("STEP 2: profile scripts")
    profiles_dir = root / "scripts" / "profiles"
    for p in profiles_enabled:
        _source_script(root, profiles_dir / f"enable-{p}.sh")
    for p in profiles_discarded:
        _source_script(root, profiles_dir / f"discard-{p}.sh")

    prof_csv = _compose_profiles_from_services(compose_services)
    if prof_csv:
        _set_compose_profiles_env(root, prof_csv)
    log(f"Compose services (logical from manifest): {', '.join(compose_services)}")
    active = _compose_active_service_names(root, prof_csv)
    if active:
        log(
            "STEP 3: active Compose service names (docker compose config --services): "
            + ", ".join(active)
        )
    else:
        log(
            "STEP 3: active Compose services — (skipped: Docker CLI unavailable or compose failed)"
        )

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
        qproc = subprocess.run(
            [
                sys.executable,
                str(root / "skills" / "init" / "queue-seeder.py"),
                "--repo-root",
                str(root),
                "--from-manifest",
                str(manifest_path),
            ],
            cwd=str(root),
            check=False,
            capture_output=True,
            text=True,
        )
        if qproc.stdout:
            print(qproc.stdout, end="")
        if qproc.stderr:
            print(qproc.stderr, end="", file=sys.stderr)
        if qproc.returncode != 0:
            print(
                "queue-seeder.py --from-manifest failed — fix manifest or queue.csv",
                file=sys.stderr,
            )
            return 1
        m = re.search(r"Appended (\d+) row", qproc.stdout or "")
        seeded = int(m.group(1)) if m else len(queue_rows)
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
    # Only commit if there are staged changes (idempotency guard)
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True, text=True, check=False,
    )
    if status.stdout.strip():
        subprocess.run(
            ["git", "-C", str(root), "commit", "-m", commit_msg],
            check=False,
        )
    else:
        print("Nothing to commit — working tree clean after initialization.")

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

**After merge — delete the initialization branch locally and on the remote:**

```bash
git checkout main
git pull origin main
git branch -d feature/idea-init-engine
git push origin --delete feature/idea-init-engine
```
"""
    gh = shutil.which("gh")
    current_branch = subprocess.check_output(
        ["git", "-C", str(root), "branch", "--show-current"],
        text=True,
    ).strip()
    if gh:
        if _pr_already_exists(root, current_branch):
            print(
                f"PR already exists for branch '{current_branch}' — skipping PR creation. "
                "Run 'gh pr list' to see it."
            )
        else:
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
            f"gh CLI not found — open a PR manually from branch '{current_branch}'"
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
