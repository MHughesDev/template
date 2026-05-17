---
doc_id: "21.1"
title: "async workers"
section: "Architecture"
status: "pending-init"
summary: "Every async task: trigger, payload shape, retry policy, failure handling, and idempotency approach. Not applicable if no workers profile."
---

# Async Workers
<!-- status: pending-init -->
<!-- initialized-by: skills/init/initialize-repo.md -->

> **Pending initialization.** This document is written by the `initialize-repo` skill.
> Run `make init:from-idea` to populate from `idea.md`.
>
> If no workers profile is enabled, this file will contain: `Not applicable — no workers profile enabled for this project.`

## Purpose

Documents every async task in the system: what triggers it, what payload it receives, its retry policy and backoff strategy, how failures are handled and surfaced, and how idempotency is enforced.
