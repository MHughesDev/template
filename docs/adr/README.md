---
doc_id: "7.0"
title: "ADR index"
section: "ADR"
summary: "ADR index. Lists architecture decisions recorded for this template."
updated: "2026-05-17"
---

# 7.0 — ADR index

**Purpose:** Index of Architecture Decision Records (ADRs) for this template repository. The template ships with **one** ADR — the founding template-architecture record. Product-specific ADRs are created inside an initialized product, not here.

## Records

| Number | Title | Status | Date |
|--------|-------|--------|------|
| [0001](0001-initial-template-architecture.md) | Initial template architecture | Accepted | 2026-05-17 |

## Adding a new ADR

A new ADR in **this** repository should only be added when a decision changes the template's own architecture (initialization model, baseline app substitution, queue semantics, skill/prompt division, etc.). For product-level decisions, add the ADR inside the initialized product instead.

1. Copy [`template.md`](template.md) to `docs/adr/<NNNN>-<kebab-case-title>.md` (next sequential number).
2. Fill every section. Do not leave placeholder text.
3. Update this index.
