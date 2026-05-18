---
doc_id: "23.0"
title: "research workspace"
section: "Research"
status: "current"
summary: "Pre-initialization research workspace: decisions, sources, notes, and external references."
updated: "2026-05-17"
---

# Research Workspace

This folder holds research and decision-making artifacts created **before** repository initialization. Once initialization runs, key findings are synthesized into `IDEA.md` and design docs.

## Structure

| Folder | Purpose |
|--------|---------|
| [`notes/`](notes/) | Themed synthesis notes from research |
| [`reference/`](reference/) | External reference registry and upstream digests |
| [`queries/`](queries/) | Search logs and query results |
| [`external/`](external/) | Policy for external resource linking |

## Key files

- [`SOURCES.md`](SOURCES.md) — Bibliography with `[Snnn]` citation convention
- [`open_ended_question.md`](open_ended_question.md) — Decision table with confidence levels
- [`reference/EXTERNAL_REFERENCE.md`](reference/EXTERNAL_REFERENCE.md) — Tracked upstream registry

## Usage

1. Research topics relevant to the product
2. Record findings in appropriate subfolders
3. Cite sources as `[S001]`, `[S002]`, etc. in `SOURCES.md`
4. Document decisions in `open_ended_question.md`
5. When complete, run `skills/init/repo_initialize.md`
