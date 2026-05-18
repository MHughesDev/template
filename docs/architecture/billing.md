---
doc_id: "2.14"
title: "billing and payments"
section: "Architecture"
status: "pending-init"
summary: "Payment provider integration, webhook handling, subscription model, and failure/retry strategy. Not applicable if no billing profile."
---

# Billing and Payments
<!-- status: pending-init -->
<!-- initialized-by: skills/init/initialize-repo.md -->

> **Pending initialization.** This document is written by the `initialize-repo` skill.
> Run `make init:from-idea` to populate from `idea.md`.
>
> If no billing profile is enabled, this file will contain: `Not applicable — no billing profile enabled for this project.`

## Purpose

Documents the billing layer: which payment provider is used, how webhooks are handled and verified, what the subscription or payment model looks like, how payment failures and retries are managed, and which entities in the data model carry billing state.
