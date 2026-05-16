---
doc_id: "arch-multi-tenancy"
title: "multi-tenancy"
section: "Architecture"
status: "pending-init"
summary: "Tenant isolation model, how tenant context propagates through the stack, and what data is shared vs isolated. Not applicable if not enabled."
---

# Multi-Tenancy
<!-- status: pending-init -->
<!-- initialized-by: skills/init/initialize-repo.md -->

> **Pending initialization.** This document is written by the `initialize-repo` skill.
> Run `make init:from-idea` to populate from `idea.md`.
>
> If multi-tenancy is not enabled, this file will contain: `Not applicable — multi-tenancy not enabled for this project.`

## Purpose

Documents the tenancy model: whether isolation is row-level or schema-level, how tenant context is extracted from requests and propagated through the service layer, what data is shared across tenants vs isolated per tenant, and how tenant provisioning works.
