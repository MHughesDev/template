# skills/repo-governance/changelogs-release-notes.md

<!-- CROSS-REFERENCES -->
<!-- - Related procedure: docs/procedures/release-preparation.md -->
<!-- - Docs: docs/release/changelog-guide.md -->

**Purpose:** How to maintain CHANGELOG.md and release notes following Keep a Changelog format. Per spec §26.4 item 53.

## Purpose

One paragraph. A well-maintained changelog is the communication artifact for releases. It tells users and agents what changed, when, and at what version. Following the Keep a Changelog format (https://keepachangelog.com) ensures machine-readable, predictable structure.

## When to Invoke

When any meaningful change is made (add entry to [Unreleased]). When preparing a release (move [Unreleased] to versioned section). After security fixes (Security category). When a feature is deprecated.

## Prerequisites

docs/release/changelog-guide.md read. CHANGELOG.md exists (from template). Keep a Changelog format understood.

## Relevant Files/Areas

CHANGELOG.md (root), docs/release/changelog-guide.md, docs/release/versioning.md

## Step-by-Step Method

Numbered steps — two scenarios:

**During development (add entry)**:
1. Identify category: Added, Changed, Fixed, Removed, Security, Deprecated
2. Add entry under [Unreleased] → appropriate category subsection
3. Format: `- Brief description of the change (PR #NNN)`

**Release preparation (cut release)**:
1. Determine version bump: major/minor/patch from semver rules
2. Add new section header: `## [X.Y.Z] - YYYY-MM-DD`
3. Move all [Unreleased] entries under the new version header
4. Reset [Unreleased] section to empty subsections
5. Add version comparison link at bottom of file
6. Run `make release:prepare` which may automate some of these steps

## Command Examples

`make release:prepare`, `make release:verify`

## Validation Checklist

- [ ] Follows Keep a Changelog format (https://keepachangelog.com)
- [ ] [Unreleased] section always present at top
- [ ] Entries in correct category (Added/Changed/Fixed/Removed/Security)
- [ ] Version links at bottom of file
- [ ] No empty version sections (all entries meaningful)

## Common Failure Modes

Mixing breaking changes into "Changed" instead of creating a new major version entry → users don't know about breaking changes. Fix: security and breaking changes always get their own entries; major version bumps for breaking changes.

## Handoff Expectations

CHANGELOG.md updated, entry references PR number, format valid.

## Related Procedures

docs/procedures/release-preparation.md

## Related Prompts

prompts/release_manager.md

## Related Rules

AGENTS.md §8 (CHANGELOG.md update triggers)
