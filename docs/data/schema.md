---
doc_id: "21.1"
title: "schema"
section: "Data"
status: "pending-init"
summary: "Plain-language description of the physical schema, join patterns, index rationale. Populated during initialization from IDEA.md §8."
updated: "2026-05-17"
---

# Database Schema
<!-- derived from: IDEA.md §8 — populated by repo_initialize -->

## Overview

_[Database type: PostgreSQL/SQLite/etc.]_

## Tables

### _[table_name]_

_[Description of this table's purpose]_

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Primary key |
| `created_at` | timestamp | NOT NULL | Creation time |
| `updated_at` | timestamp | NOT NULL | Last update |

**Indexes:**
- PRIMARY on `id`
- _[Additional indexes with rationale]_

## Join patterns

_[Common query patterns and recommended joins]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
