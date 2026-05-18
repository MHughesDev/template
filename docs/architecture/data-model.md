---
doc_id: "2.16"
title: "data model"
section: "Architecture"
status: "pending-init"
summary: "Complete entity definitions: every field, type, constraint, enum, and relationship across all bounded contexts."
---

# Data Model
<!-- status: pending-init -->
<!-- initialized-by: skills/init/initialize-repo.md -->

> **Pending initialization.** This document is written by the `initialize-repo` skill.
> Run `make init:from-idea` to populate from `idea.md`.

## Purpose

The canonical reference for every entity in the system: all fields with types and nullability, all enum definitions with values, all relationships with cardinality and cascade rules, and an ER diagram. This is the source of truth that migrations and SQLAlchemy models are derived from.
