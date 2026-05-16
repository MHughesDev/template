---
doc_id: "arch-ai-rag"
title: "ai and rag architecture"
section: "Architecture"
status: "pending-init"
summary: "Ingestion pipeline, embedding strategy, retrieval approach, model provider, and kill switch behavior. Not applicable if no AI/RAG profile."
---

# AI and RAG Architecture
<!-- status: pending-init -->
<!-- initialized-by: skills/init/initialize-repo.md -->

> **Pending initialization.** This document is written by the `initialize-repo` skill.
> Run `make init:from-idea` to populate from `idea.md`.
>
> If no AI/RAG profile is enabled, this file will contain: `Not applicable — no AI/RAG profile enabled for this project.`

## Purpose

Documents the AI/RAG layer: what data is ingested and when, how embeddings are generated and refreshed, how retrieval is structured, which model provider is used and through which abstraction, and how the kill switch is wired.
