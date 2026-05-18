---
doc_id: "1.1"
title: "prerequisites"
section: "Getting Started"
summary: "Required tools and versions. Python 3.12+, Docker, Make/Task, Git."
updated: "2026-05-17"
---

# 1.1 — prerequisites

**Purpose:** Required tools and versions. Python 3.12+, Docker, Make/Task, Git. Per spec §26.5 item 113.

## 1.1.1 Required Tools
Checklist format with version verification commands for each tool:
- Python 3.12+: `python --version` — must be 3.12 or higher
- Docker 24+: `docker --version`
- Docker Compose v2+: `docker compose version` — note: v2 is `docker compose` not `docker-compose`
- Make: `make --version`
- Git: `git --version`
- Optional (web profile): Node.js 20+: `node --version`
- Optional (mobile profile): Expo CLI: `npx expo --version`

## 1.1.2 Installation Guide (per OS)
Links to official installation docs for each tool on Linux, macOS, and Windows.

## 1.1.3 Coding agents (Cursor / automation)

- **No bundled “dev MCP”** for this repository: orchestration uses **Make**, **`scripts/`**, and **`packages/queue_ops`** per **[AGENTS.md](../../AGENTS.md)** and **[local-setup.md](../development/local-setup.md)**.
- You may still attach **optional** MCP servers in Cursor (plugins, vendor integrations). They are **not** part of the template contract.
