# skills/init/idea-validator.py
"""Validate idea.md structure and content completeness (sections 1–17)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_SECTIONS = tuple(range(1, 18))

MIN_CONTENT_LENGTH: dict[int, int] = {
    1: 30,
    2: 80,
    3: 20,
    4: 40,
    5: 30,
    6: 20,
    7: 20,
    8: 20,
    9: 20,
    10: 20,
    11: 20,
    12: 40,
    13: 20,
    14: 20,
    15: 10,
    16: 10,
    17: 10,
}


@dataclass
class SectionResult:
    """Validation result for one idea.md section."""

    section_number: int
    section_title: str
    passed: bool
    issues: list[str] = field(default_factory=list)
    content_length: int = 0


@dataclass
class ValidationReport:
    """Complete validation report for idea.md."""

    sections: list[SectionResult]
    consistency_issues: list[str]
    passed: bool

    def to_text(self) -> str:
        lines = ["idea.md validation report", "=" * 40, ""]
        for s in self.sections:
            status = "PASS" if s.passed else "FAIL"
            lines.append(
                f"§{s.section_number} {s.section_title!r} [{status}] "
                f"(len={s.content_length})"
            )
            for issue in s.issues:
                lines.append(f"  - {issue}")
            lines.append("")
        if self.consistency_issues:
            lines.append("Consistency (informational):")
            for c in self.consistency_issues:
                lines.append(f"  - {c}")
            lines.append("")
        lines.append(f"Overall: {'PASS' if self.passed else 'FAIL'}")
        return "\n".join(lines)

    def to_json(self) -> str:
        payload = {
            "passed": self.passed,
            "sections": [
                {
                    "section_number": s.section_number,
                    "section_title": s.section_title,
                    "passed": s.passed,
                    "issues": s.issues,
                    "content_length": s.content_length,
                }
                for s in self.sections
            ],
            "consistency_issues": self.consistency_issues,
        }
        return json.dumps(payload, indent=2)


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def has_real_content(section_content: str, min_length: int = 50) -> bool:
    cleaned = strip_comments(section_content)
    cleaned = re.sub(r"\|[-:\s|]+\|", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return len(cleaned) >= min_length


def parse_sections(idea_content: str) -> dict[int, str]:
    """Split idea.md into sections keyed by leading H2 number (## N.)."""
    text = idea_content
    pattern = re.compile(r"^##\s+(\d+)\.\s+", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return {}

    sections: dict[int, str] = {}
    for i, m in enumerate(matches):
        num = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[num] = text[start:end].strip()
    return sections


def validate_section(number: int, content: str) -> SectionResult:
    first_line = content.splitlines()[0] if content else ""
    title_match = re.match(r"^##\s+\d+\.\s+(.+)$", first_line)
    title = title_match.group(1).strip() if title_match else f"section {number}"
    min_len = MIN_CONTENT_LENGTH.get(number, 50)
    issues: list[str] = []
    if not has_real_content(content, min_len):
        issues.append(
            f"insufficient content (need ≥{min_len} chars beyond comments/tables)"
        )

    body = strip_comments(content)
    low = body.lower()

    if number == 1 and "`" not in body and not re.search(
        r"\b[a-z0-9-]{3,}/[a-z0-9-]{3,}", low
    ):
        issues.append(
            "§1 should include filled project name / slug (placeholders detected)"
        )

    if number == 3 and not re.search(r"\[[xX]\]", body):
        issues.append("§3: select exactly one archetype with [x]")

    if (
        number == 4
        and ("bounded contexts" in low or "## 4.2" in content.lower())
        and ("| `<!--" in body or body.count("|") < 8)
    ):
        issues.append("§4.2: add at least one bounded context row with real text")

    if number == 5 and not re.search(
        r"\[\s*\]\s*yes|\[\s*x\s*\]\s*yes", low, re.IGNORECASE
    ):
        issues.append("§5: mark profile rows yes/no (placeholders only)")

    if number == 12 and "| 1 |" not in body and not re.search(
        r"\|\s*1\s*\|", body
    ):
        issues.append(
            "§12: add at least one queue seed row with priority and summary"
        )

    passed = len(issues) == 0
    cleaned = strip_comments(content)
    content_length = len(re.sub(r"\s+", " ", cleaned).strip())

    return SectionResult(
        section_number=number,
        section_title=title,
        passed=passed,
        issues=issues,
        content_length=content_length,
    )


def check_consistency(sections: dict[int, str]) -> list[str]:
    issues: list[str] = []
    s3 = sections.get(3, "")
    s5 = sections.get(5, "")
    if (
        "saas" in s3.lower()
        and "multi-tenancy" in s5.lower()
        and "[x]" not in s5.lower()
        and "yes" not in s5.lower()
    ):
        issues.append(
            "Archetype SaaS usually enables multi-tenancy profile — verify §5."
        )
    return issues


def validate_idea_md(idea_path: Path) -> ValidationReport:
    raw = idea_path.read_text(encoding="utf-8", errors="replace")
    parsed = parse_sections(raw)
    results: list[SectionResult] = []
    for n in REQUIRED_SECTIONS:
        if n not in parsed:
            results.append(
                SectionResult(
                    section_number=n,
                    section_title="(missing)",
                    passed=False,
                    issues=["section heading not found (expected ## N. ...)"],
                    content_length=0,
                )
            )
            continue
        results.append(validate_section(n, parsed[n]))

    consistency = check_consistency(parsed)
    passed = all(s.passed for s in results)
    return ValidationReport(
        sections=results,
        consistency_issues=consistency,
        passed=passed,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate idea.md for repo initialization.",
    )
    parser.add_argument("idea_path", nargs="?", default="idea.md", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    path = args.idea_path
    if not path.is_file():
        print(f"error: {path} not found", file=sys.stderr)  # noqa: T201
        sys.exit(1)

    report = validate_idea_md(path)
    if args.format == "json":
        print(report.to_json())  # noqa: T201
    else:
        print(report.to_text())  # noqa: T201

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
