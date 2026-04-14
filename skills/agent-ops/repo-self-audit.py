# skills/agent-ops/repo-self-audit.py
"""Repository spec-compliance audit."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

SKIP_DIRS = frozenset(
    {
        ".git",
        ".venv",
        "node_modules",
        "__pycache__",
        "htmlcov",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }
)

QUEUE_COLUMNS = (
    "id",
    "batch",
    "phase",
    "category",
    "summary",
    "dependencies",
    "notes",
    "created_date",
)

QUEUE_ARCHIVE_EXTRA = ("status", "completed_date")

REQUIRED_PROMPT_FIELDS: tuple[str, ...] = (
    "purpose",
    "when_to_use",
    "required_inputs",
    "expected_outputs",
    "validation_expectations",
    "constraints",
    "linked_commands",
    "linked_procedures",
    "linked_skills",
)

# spec §10 / AGENTS.md — canonical Make targets (see Makefile escaped colons).
REQUIRED_MAKE_TARGETS: tuple[str, ...] = (
    "lint",
    "fmt",
    "typecheck",
    "test",
    "migrate",
    "queue-peek",
    "queue-validate",
    "audit-self",
    "security-scan",
    "skills-list",
    "help",
    "dev",
)

# Critical paths from spec §26 / implementation plan (existence check).
REQUIRED_PATHS: tuple[str, ...] = (
    "AGENTS.md",
    "README.md",
    "Makefile",
    "pyproject.toml",
    "spec/spec.md",
    "queue/queue.csv",
    "queue/queuearchive.csv",
    "queue/QUEUE_INSTRUCTIONS.md",
    "apps/api/src/main.py",
    "apps/api/src/config.py",
    "packages/contracts/__init__.py",
    "packages/tasks/__init__.py",
    "skills/README.md",
    "prompts/README.md",
    "docs/procedures/README.md",
)


@dataclass(frozen=True, slots=True)
class AuditFinding:
    """Single audit finding."""

    severity: Literal["BLOCKING", "WARNING"]
    check: str
    path: str
    message: str
    spec_reference: str


@dataclass
class AuditReport:
    """Aggregated audit results."""

    timestamp: datetime
    findings: list[AuditFinding]
    checks_run: list[str]

    def blocking_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "BLOCKING")

    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "WARNING")

    def passed(self) -> bool:
        return self.blocking_count() == 0

    def to_markdown(self) -> str:
        lines = [
            "# Repository self-audit",
            "",
            f"- **Run at:** {self.timestamp.isoformat()}",
            f"- **Checks:** {', '.join(self.checks_run)}",
            f"- **Blocking:** {self.blocking_count()} | "
            f"**Warnings:** {self.warning_count()}",
            "",
        ]
        if not self.findings:
            lines.append("No findings.")
            return "\n".join(lines)

        for f in self.findings:
            lines.append(f"## [{f.severity}] {f.check}: {f.path}")
            lines.append("")
            lines.append(f.message)
            lines.append("")
            lines.append(f"*Spec: {f.spec_reference}*")
            lines.append("")
        return "\n".join(lines)

    def to_json(self) -> str:
        payload = {
            "timestamp": self.timestamp.isoformat(),
            "checks_run": self.checks_run,
            "findings": [
                {
                    "severity": f.severity,
                    "check": f.check,
                    "path": f.path,
                    "message": f.message,
                    "spec_reference": f.spec_reference,
                }
                for f in self.findings
            ],
        }
        return json.dumps(payload, indent=2)


def _iter_files(repo_root: Path) -> list[Path]:
    out: list[Path] = []
    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return out


def check_file_inventory(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    for rel in REQUIRED_PATHS:
        path = repo_root / rel
        if not path.is_file():
            findings.append(
                AuditFinding(
                    severity="BLOCKING",
                    check="inventory",
                    path=rel,
                    message=f"Required file missing: {rel}",
                    spec_reference="§26",
                )
            )
    return findings


def check_title_comments(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    for path in _iter_files(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        suffix = path.suffix.lower()
        if suffix == ".json":
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="title-comments",
                    path=rel,
                    message=f"Could not read file: {exc}",
                    spec_reference="§1.7",
                )
            )
            continue

        lines = raw.splitlines()
        if not lines:
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="title-comments",
                    path=rel,
                    message="Empty file has no title comment",
                    spec_reference="§1.7",
                )
            )
            continue

        first = lines[0].strip()
        ok = False
        if suffix == ".py":
            ok = first.startswith("# ")
        elif suffix in {".md", ".mdc"}:
            ok = first.startswith("# ") or first.startswith("<!--")
        elif suffix in {".yml", ".yaml"}:
            ok = first.startswith("# ")
        elif suffix == ".sh":
            second = lines[1].strip() if len(lines) > 1 else ""
            ok = first.startswith("#!/") and second.startswith("# ")
        elif suffix == ".csv":
            ok = first.startswith("# ")
        elif suffix == ".bat":
            ok = first.upper().startswith("REM ")
        elif suffix in {".toml", ".ini", "dockerfile"} or path.name == "Dockerfile":
            ok = first.startswith("# ")
        elif suffix == ".typed":
            ok = True  # PEP 561 marker may be empty
        else:
            ok = first.startswith("# ") or first.startswith("<!--")

        if not ok:
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="title-comments",
                    path=rel,
                    message="First line does not match §1.7 title-comment convention",
                    spec_reference="§1.7",
                )
            )
    return findings


def check_skill_format(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return findings

    for md in skills_dir.rglob("*.md"):
        if md.name == "README.md":
            continue
        rel = md.relative_to(repo_root).as_posix()
        text = md.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        if not re.search(r"^##\s+.*purpose", text, re.IGNORECASE | re.MULTILINE):
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="skill-format",
                    path=rel,
                    message='Missing "## Purpose" section (§6.2)',
                    spec_reference="§6.2",
                )
            )
        if not re.search(r"^##\s+.*when to invoke", text, re.IGNORECASE | re.MULTILINE):
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="skill-format",
                    path=rel,
                    message='Missing "## When to invoke" section (§6.2)',
                    spec_reference="§6.2",
                )
            )
    return findings


def check_prompt_metadata(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    prompts_dir = repo_root / "prompts"
    if not prompts_dir.is_dir():
        return findings

    for md in prompts_dir.glob("*.md"):
        if md.name == "README.md":
            continue
        rel = md.relative_to(repo_root).as_posix()
        text = md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="prompt-metadata",
                    path=rel,
                    message="Missing YAML front matter (§7.2)",
                    spec_reference="§7.2",
                )
            )
            continue
        end = text.find("\n---", 3)
        if end == -1:
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="prompt-metadata",
                    path=rel,
                    message="Malformed YAML front matter closing ---",
                    spec_reference="§7.2",
                )
            )
            continue
        fm = text[3:end]
        for field in REQUIRED_PROMPT_FIELDS:
            if not re.search(rf"^{re.escape(field)}\s*:", fm, re.MULTILINE):
                findings.append(
                    AuditFinding(
                        severity="WARNING",
                        check="prompt-metadata",
                        path=rel,
                        message=f"Front matter missing field: {field}",
                        spec_reference="§7.2",
                    )
                )
    return findings


def check_procedure_structure(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    proc_dir = repo_root / "docs" / "procedures"
    if not proc_dir.is_dir():
        return findings

    required_any = (
        "purpose",
        "prerequisite",
        "step",
        "validation",
        "handoff",
        "rollback",
        "failure",
    )
    for md in proc_dir.glob("*.md"):
        if md.name == "README.md":
            continue
        rel = md.relative_to(repo_root).as_posix()
        text = md.read_text(encoding="utf-8", errors="replace").lower()
        if not any(k in text for k in required_any):
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="procedure-structure",
                    path=rel,
                    message=(
                        "Procedure should include Purpose, Prerequisites, Steps, "
                        "Validation, Handoff (§8.3)"
                    ),
                    spec_reference="§8.3",
                )
            )
    return findings


def _read_csv_header(path: Path) -> list[str] | None:
    if not path.is_file():
        return None
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or not row[0].strip():
                continue
            if row[0].strip().startswith("#"):
                continue
            return [c.strip() for c in row]
    return None


def check_queue_schema(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    qc = _read_csv_header(repo_root / "queue" / "queue.csv")
    if qc is None:
        findings.append(
            AuditFinding(
                severity="BLOCKING",
                check="queue-schema",
                path="queue/queue.csv",
                message="queue.csv missing or empty",
                spec_reference="§17",
            )
        )
    elif list(QUEUE_COLUMNS) != qc:
        findings.append(
            AuditFinding(
                severity="BLOCKING",
                check="queue-schema",
                path="queue/queue.csv",
                message=f"Header mismatch. Expected {list(QUEUE_COLUMNS)}, got {qc}",
                spec_reference="§17",
            )
        )

    qa = _read_csv_header(repo_root / "queue" / "queuearchive.csv")
    expected_archive = list(QUEUE_COLUMNS) + list(QUEUE_ARCHIVE_EXTRA)
    if qa is None:
        findings.append(
            AuditFinding(
                severity="BLOCKING",
                check="queue-schema",
                path="queue/queuearchive.csv",
                message="queuearchive.csv missing or empty",
                spec_reference="§17",
            )
        )
    elif qa != expected_archive:
        findings.append(
            AuditFinding(
                severity="BLOCKING",
                check="queue-schema",
                path="queue/queuearchive.csv",
                message=f"Header mismatch. Expected {expected_archive}, got {qa}",
                spec_reference="§17",
            )
        )
    return findings


def check_make_targets(repo_root: Path) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    makefile = repo_root / "Makefile"
    if not makefile.is_file():
        return [
            AuditFinding(
                severity="WARNING",
                check="make-targets",
                path="Makefile",
                message="Makefile missing",
                spec_reference="§10.2",
            )
        ]
    text = makefile.read_text(encoding="utf-8", errors="replace")
    # Makefile uses escaped colons; substring match is enough.
    for req in REQUIRED_MAKE_TARGETS:
        if req not in text:
            findings.append(
                AuditFinding(
                    severity="WARNING",
                    check="make-targets",
                    path="Makefile",
                    message=f"Expected Make target not found (substring): {req}",
                    spec_reference="§10.2",
                )
            )
    return findings


CHECK_REGISTRY: dict[str, object] = {
    "inventory": check_file_inventory,
    "title-comments": check_title_comments,
    "skill-format": check_skill_format,
    "prompt-metadata": check_prompt_metadata,
    "procedure-structure": check_procedure_structure,
    "queue-schema": check_queue_schema,
    "make-targets": check_make_targets,
}


def run_audit(repo_root: Path, checks: list[str] | None = None) -> AuditReport:
    """Run selected or all audit checks."""
    ts = datetime.now(tz=UTC)
    to_run = list(CHECK_REGISTRY.keys()) if checks is None else checks
    findings: list[AuditFinding] = []
    for name in to_run:
        fn = CHECK_REGISTRY.get(name)
        if fn is None:
            continue
        findings.extend(fn(repo_root))  # type: ignore[operator]
    return AuditReport(timestamp=ts, findings=findings, checks_run=to_run)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repository self-audit (spec compliance).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    parser.add_argument(
        "--check",
        action="append",
        help="Run only this check (repeatable). Default: all checks.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--inventory-only",
        action="store_true",
        help="Shortcut for --check inventory",
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    checks: list[str] | None = None
    if args.inventory_only:
        checks = ["inventory"]
    elif args.check:
        checks = args.check

    report = run_audit(repo_root, checks)
    if args.format == "json":
        print(report.to_json())  # noqa: T201
    else:
        print(report.to_markdown())  # noqa: T201

    if not report.passed():
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
