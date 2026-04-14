# skills/devops/dockerfile-linter.py
"""

PURPOSE:
Lints Dockerfiles for best practices: multi-stage build presence, non-root user
enforcement, no 'latest' image tags, HEALTHCHECK instruction, and layer ordering
for cache efficiency. Used by skills/devops/docker-multi-stage-builds.md.

DEPENDS ON:
- pathlib (stdlib) — file paths
- re (stdlib) — pattern matching
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/devops/docker-multi-stage-builds.md — references as machinery

FUNCTIONS:

  lint_dockerfile(dockerfile_path: Path) -> list[dict[str, str]]:
    PURPOSE: Lint a single Dockerfile and return findings.
    STEPS:
      1. Read file content
      2. Parse into instructions (FROM, RUN, COPY, etc.)
      3. Check: at least 2 FROM instructions (multi-stage)
      4. Check: USER instruction sets non-root user
      5. Check: no FROM with :latest tag
      6. Check: HEALTHCHECK instruction present
      7. Check: COPY instructions come after dependency install (cache efficiency)
      8. Check: RUN apt-get has cleanup (rm -rf /var/lib/apt/lists/*)
    RETURNS: list of finding dicts with severity and message

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: dockerfile_path (default apps/api/Dockerfile)
      2. Run lint_dockerfile()
      3. Print findings
      4. Exit 1 if any HIGH findings

DESIGN DECISIONS:
- HIGH findings: :latest tag, missing non-root USER, missing HEALTHCHECK
- WARNING findings: missing multi-stage, cache-inefficient COPY order
"""
