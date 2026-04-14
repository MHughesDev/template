# CHANGELOG.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/release/changelog-guide.md, Makefile release:prepare target -->
<!-- - Links to: https://keepachangelog.com/en/1.1.0/, https://semver.org/ -->

> PURPOSE: Project changelog following Keep a Changelog format (https://keepachangelog.com/en/1.1.0/). Maintained by agents and humans during releases. Every meaningful change is recorded here. Per spec §28.1 item 277.

## Format Header

> CONTENT: Standard Keep a Changelog header with links to format spec and semver spec. State the format version (1.1.0) and the semver version of this project. Include the standard note: "All notable changes to this project will be documented in this file."

## [Unreleased]

> CONTENT: The always-present Unreleased section. Contains subsections for each change category. Per Keep a Changelog format, subsections are only included when they have entries:
>
> ### Added
> (new features)
>
> ### Changed
> (changes to existing functionality)
>
> ### Fixed
> (bug fixes)
>
> ### Removed
> (removed features)
>
> ### Security
> (security fixes and vulnerability disclosures)
>
> ### Deprecated
> (soon-to-be removed features)
>
> Start with empty subsections or placeholder comment. Entries added during development before each release.

## [0.1.0] — YYYY-MM-DD (Initial Template)

> CONTENT: The first version entry documenting the template initialization. Subsections:
>
> ### Added
> - Initial repository template structure per spec v4.0
> - FastAPI modular monolith scaffolding (health, auth, tenancy modules)
> - Queue-driven agent work orchestration system
> - Full documentation and governance machine
> - Skill library with 70+ skill playbooks and machinery
> - CI/CD pipeline (GitHub Actions: lint, typecheck, test, build, scan)
> - Kubernetes deployment manifests with Kustomize overlays
> - Cross-platform bootstrap scripts (setup.sh/bat, run.sh/bat)
> - Documentation generation pipeline (docs:generate, docs:check)
> - Queue intelligence system (DAG, complexity, batching, conflict detection)

## Version Links Section

> CONTENT: Standard Keep a Changelog version comparison links at the bottom of the file. Format:
> [Unreleased]: https://github.com/{{ORG}}/{{REPO}}/compare/v0.1.0...HEAD
> [0.1.0]: https://github.com/{{ORG}}/{{REPO}}/releases/tag/v0.1.0
>
> Placeholders {{ORG}} and {{REPO}} are filled during initialization from idea.md §1.
