---
doc_id: "21.4"
title: "bounded contexts"
section: "Architecture"
status: "pending-init"
summary: "Bounded context map: every context, what it owns, what it does not own, and how contexts communicate."
---

# Bounded Contexts
<!-- status: pending-init -->
<!-- initialized-by: skills/init/initialize-repo.md -->

> **Pending initialization.** This document is written by the `initialize-repo` skill.
> Run `make init:from-idea` to populate from `idea.md`.

## Purpose

Defines every bounded context in this system: its name, the entities it owns, the workflows it is responsible for, the interfaces it exposes to other contexts, and which module path it maps to under `apps/api/src/`.
