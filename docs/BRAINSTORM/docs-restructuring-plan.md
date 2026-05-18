---
doc_id: "19.5"
title: "docs restructuring plan"
section: "BRAINSTORM"
status: "draft"
updated: "2026-05-17"
---

# Docs Restructuring Plan

## Executive Summary

Current state: ~100 docs files across 22 sections with redundancy, overlap, and inconsistent depth.
Target state: ~60-70 files with clear boundaries, no redundancy, fully built-out procedures.

## Problem Analysis

### 1. Redundancy & Overlap

| Files | Issue | Resolution |
|-------|-------|------------|
| `ai-rag-chromadb.md` (2.1) vs `ai-rag.md` (2.11) | Duplicate topic | **Merge**: Keep 2.11 as canonical, delete 2.1 |
| `auth-multi-tenancy.md` (2.3) vs `auth.md` (2.13) + `multi-tenancy.md` (2.19) | Split then overlap | **Delete 2.3**: Content moved to 2.13 + 2.19 |
| `data-layer.md` (2.4) vs `data-model.md` (2.16) + schema.md (21.1) | Legacy pointer | **Delete 2.4**: Obsolete |
| `domain-model.md` (2.6) vs `data-model.md` (2.16) | Overlap | **Merge into 2.16**: Single model doc |
| `system-context.md` (2.9) vs `overview.md` (2.20) | Legacy pointer | **Delete 2.9**: Obsolete |
| `testing-guide.md` (3.9) vs `testing-strategy.md` (11.3) | Split coverage | **Merge**: Keep in Quality (11.3), reference from Dev |
| `security/overview.md` (16.7) vs `security/README.md` (16.0) | Index vs content | **Merge**: README should have content, not be index |

### 2. Empty/Placeholder Procedures

These procedures exist but contain only "Procedure reference retained..." with no actual procedure:

| File | Current State | Action |
|------|---------------|--------|
| `add-optional-app-profile.md` (5.3) | Placeholder | **Write full procedure** |
| `add-queue-category.md` (5.5) | Placeholder | **Write full procedure** |
| `dependency-upgrade.md` (5.8) | Placeholder | **Write full procedure** |
| `enable-profile.md` (5.9) | Placeholder | **Write full procedure** |
| `extract-service-from-monolith.md` (5.10) | Stub only | **Write full procedure** |
| `incident-rollback.md` (5.14) | Placeholder | **Write full procedure** |
| `release-preparation.md` (5.19) | Placeholder | **Write full procedure** |
| `scaffold-domain-module.md` (5.20) | Stub only | **Write full procedure** |

### 3. Missing Critical Procedures

| Needed Procedure | Why | Suggested ID |
|------------------|-----|--------------|
| Add a procedure | Meta-procedure | 5.30 |
| Delete/merge docs | This restructuring | 5.31 |
| Add a skill | Skill creation SOP | 5.32 |
| Security incident response | Security needs | 5.33 |
| Create ADR | ADR authoring | 5.34 |
| Code review | Human process | 5.35 |
| Database rollback | Beyond incident | 5.36 |
| Feature flag management | Enable/disable | 5.37 |

### 4. Queue Documentation Chaos

Root level queue docs:
- `docs/queue/QUEUE_INSTRUCTIONS.md`
- `docs/queue/QUEUE_SPLIT_TRIGGERS.md`
- `docs/queue/QUEUE_SYSTEM_REPLICATION_SPEC.md`

Plus folder: `docs/queue/*.md`

**Resolution:**
- Move all to `docs/queue/` folder
- Rename to lowercase-hyphen format
- `QUEUE_INSTRUCTIONS.md` → `instructions.md` (but keep doc_id 12.3)
- `QUEUE_SPLIT_TRIGGERS.md` → `split-triggers.md` (assign doc_id)
- `QUEUE_SYSTEM_REPLICATION_SPEC.md` → `replication-spec.md` (assign doc_id)

### 5. Over-Granularity Issues

| Current | Problem | Resolution |
|---------|---------|------------|
| `add-make-target.md` (5.1) | Too small? | Keep - it's a complete procedure |
| `add-mcp-tool.md` (5.2) | Standalone | Keep |
| `add-optional-app-profile.md` (5.3) | Should merge with `enable-profile.md` | **Merge into single "Manage Profiles" procedure** |
| `add-queue-category.md` (5.5) | Could be part of queue management | Keep separate - queue is critical |
| `add-prompt-template.md` (5.4) | Standalone | Keep |

### 6. Missing Section: Meta/Repo Maintenance

No home for:
- How to restructure docs (this work)
- How to audit docs
- How to deprecate docs
- How to split/combine docs

**Resolution:** Add Section 23: Maintenance (or extend Repo Governance)

## Target Docs Structure (60-70 files)

### Section 1: Getting Started (3 files) ✓
- 1.0 README
- 1.1 Prerequisites
- 1.2 Quickstart

### Section 2: Architecture (12 files, down from 19)
**Keep:**
- 2.0 README
- 2.2 API design
- 2.7 Error handling
- 2.8 Modular monolith
- 2.10 Profile interactions
- 2.11 AI/RAG
- 2.12 Async workers
- 2.13 Auth
- 2.14 Billing
- 2.15 Bounded contexts
- 2.16 Data model (merged with 2.6)
- 2.17 Frontend
- 2.18 Mobile
- 2.19 Multi-tenancy
- 2.20 System overview

**Delete/Merge:**
- 2.1 → merged into 2.11
- 2.3 → merged into 2.13 + 2.19
- 2.4 → deleted (obsolete)
- 2.5 → could merge diagrams into 2.20
- 2.6 → merged into 2.16
- 2.9 → deleted (obsolete)

### Section 3: Development (10 files)
**Keep all, reorganize:**
- 3.0 README
- 3.1 Coding standards
- 3.3 Docs generation
- 3.4 Environment vars
- 3.5 Git workflow
- 3.6 Init manifest schema
- 3.7 Local setup
- 3.8 Module patterns
- 3.10 CI
- 3.11 Commands

**Move/Delete:**
- 3.9 Testing guide → **merge into 11.3**, keep brief reference here

### Section 4: API (4 files) ✓
Keep all.

### Section 5: Procedures (25 files, up from 22, all fully populated)

**Current with content:**
- 5.1 Add make target ✓
- 5.2 Add MCP tool ✓
- 5.4 Add prompt template ✓
- 5.6 Archive queue item ✓
- 5.7 Database migration ✓
- 5.11 Handle blocked work ✓
- 5.12 Handoff ✓
- 5.13 Implement change ✓
- 5.16 Initialize repo ✓
- 5.17 Open pull request ✓
- 5.18 Plan change ✓
- 5.21 Start queue item ✓
- 5.22 Update documentation ✓
- 5.23 Update/create rule ✓
- 5.24 Update/create skill ✓
- 5.25 Validate change ✓
- 5.26 Implementation loop ✓
- 5.27 MicroFast MCP ✓
- 5.28 Queue decomposition ✓
- 5.29 Template upgrade ✓

**Rewrite from placeholder (8 files):**
- 5.3 Add/manage profiles (merge 5.3 + 5.9)
- 5.5 Add queue category
- 5.8 Dependency upgrade
- 5.10 Extract service from monolith
- 5.14 Incident rollback
- 5.15 NEW: Add ADR
- 5.19 Release preparation
- 5.20 Scaffold domain module

**NEW procedures (5 files):**
- 5.30 Add a procedure (meta)
- 5.31 Restructure docs (this work)
- 5.32 Create a skill
- 5.33 Security incident response
- 5.34 Code review

### Section 6: Operations (13 files)
**Keep:**
- 6.0 README
- 6.1 Backups
- 6.2 Configuration
- 6.3 Database operations
- 6.4 Docker
- 6.5 Health checks
- 6.6 Kubernetes
- 6.7 Observability
- 6.8 Rollback
- 6.9 Scaling
- 6.10 Deployment
- 6.11 Monitoring

**Move runbooks:**
- 6.12 Incident response runbook → **move to Runbooks 15.x**
- 6.13 Rollback runbook → **move to Runbooks 15.x**

### Section 7: ADR (4 files) ✓
Keep all.

### Section 8: Agents (7 files) ✓
Keep all.

### Section 9: Optional Clients (2 files) ✓
Keep all.

### Section 10: Prompts (3 files) ✓
Keep all.

### Section 11: Quality (3 files) ✓
**Keep:**
- 11.0 README
- 11.1 Coverage policy
- 11.2 Flake policy

**Merged:**
- 11.3 Testing strategy ← **merge 3.9 here**

### Section 12: Queue (6 files, organized)
**Reorganize root → folder:**
- 12.1 Categories ✓
- 12.2 Intelligence ✓
- 12.3 Instructions (was QUEUE_INSTRUCTIONS.md)
- 12.4 Split triggers (was QUEUE_SPLIT_TRIGGERS.md)
- 12.5 Replication spec (was QUEUE_SYSTEM_REPLICATION_SPEC.md)
- 12.6 System overview (merge/move from root)

### Section 13: Release (4 files) ✓
Keep all.

### Section 14: Repo Governance (5 files) ✓
**Consider adding:**
- 14.5 Docs restructuring (this work)

### Section 15: Runbooks (6 files, expanded)
**Move from Operations:**
- 15.0 README
- 15.1 API down
- 15.2 Chroma unavailable
- 15.3 DB failure
- 15.4 JWT key rotation
- 15.5 Incident response (was 6.12)
- 15.6 Rollback (was 6.13)

### Section 16: Security (7 files)
**Merge:**
- 16.0 README ← **merge 16.7 content here**
- 16.1 Accepted risks
- 16.2 CORS policy
- 16.3 Incident response
- 16.4 Secrets management
- 16.6 Token lifecycle
- 16.8 Threat model

**Delete:**
- 16.7 → merged into 16.0

### Section 17: Troubleshooting (2 files) ✓
Keep.

### Section 18: Root (4 files) ✓
Keep all.

### Section 19: BRAINSTORM (5 files) ✓
Keep.

### Section 20: Integrations (1 file) ✓
Keep.

### Section 21: Data (3 files) ✓
Keep.

### Section 22: Testing (2 files) ✓
**Merged into Quality 11.x**
- 22.1 → merged into 11.3
- 22.2 → merged into 11.1

**Delete Section 22 entirely**

## Procedure Sizing Philosophy

A procedure should be **one complete workflow** that a human or agent can execute start-to-finish.

### Good procedure size:
- **Too small:** "How to add a comment to code" - too granular
- **Too large:** "How to build the entire app" - too broad
- **Just right:** "How to add a make target" - discrete, bounded, complete

### Procedure sizing rules:
1. **Single outcome**: One thing gets done/created/changed
2. **Bounded steps**: 3-15 steps is the sweet spot
3. **Clear entry/exit**: Know when to start and when done
4. **Referenceable**: Can be invoked from multiple contexts
5. **Composable**: Can be referenced by other procedures

### Examples of properly-sized procedures:
- "Add a procedure" (meta, but discrete)
- "Database migration" (bounded workflow)
- "Open a pull request" (clear start/end)
- "Handle blocked work" (specific situation)

### Examples of procedures that should be merged:
- "Add profile" + "Enable profile" → "Manage profiles"
- "Database migration" + "Database rollback" → Could be one doc with both

## Implementation Phases

### Phase 1: Preparation
1. Create this plan document ✓
2. Create "Add Procedure" procedure
3. Create "Add Procedure" skill
4. Update DOCS_MAP.md with new structure

### Phase 2: Consolidation (reduces file count)
1. Merge architecture legacy files
2. Merge security overview files
3. Merge testing docs into Quality
4. Delete obsolete files

### Phase 3: Expansion (procedures)
1. Rewrite 8 placeholder procedures with full content
2. Create 5 new procedures
3. Move runbooks to dedicated section

### Phase 4: Reorganization
1. Move queue docs to folder
2. Delete Section 22 (Testing) after merge
3. Renumber if needed
4. Update all cross-references

### Phase 5: Validation
1. Run docs:map-check
2. Verify all doc_ids unique
3. Check for broken links
4. AGENTS.md review

## Skill: Add Procedure

The skill should:
1. Read this plan for procedure sizing guidance
2. Check if procedure already exists (avoid duplication)
3. Determine correct section and doc_id
4. Apply procedure template
5. Update DOCS_MAP.md
6. Create cross-references from relevant skills/prompts

### Skill capabilities:
- `add_procedure --name "procedure-name" --section 5 --based-on "similar-procedure"`
- Validate procedure size (flag if too large/small)
- Auto-generate doc_id
- Update indexes
- Create minimal viable procedure with TODO markers

## Files to Delete (9)

1. `docs/architecture/ai-rag-chromadb.md` (2.1) - merged into 2.11
2. `docs/architecture/auth-multi-tenancy.md` (2.3) - merged into 2.13/2.19
3. `docs/architecture/data-layer.md` (2.4) - obsolete
4. `docs/architecture/domain-model.md` (2.6) - merged into 2.16
5. `docs/architecture/system-context.md` (2.9) - obsolete
6. `docs/development/testing-guide.md` (3.9) - merged into 11.3
7. `docs/security/overview.md` (16.7) - merged into 16.0
8. `docs/testing/strategy.md` (22.1) - merged into 11.3
9. `docs/testing/coverage.md` (22.2) - merged into 11.1

## Files to Merge (8 merges → 4 files)

1. 5.3 + 5.9 → "Manage profiles" (5.3)
2. 3.9 + 11.3 → "Testing strategy" (11.3)
3. 16.0 + 16.7 → "Security overview" (16.0)
4. 22.1 + 22.2 + 11.1 + 11.3 → Quality consolidated (3 files)

## Files to Move (6)

1. `docs/queue/QUEUE_INSTRUCTIONS.md` → `docs/queue/instructions.md` (12.3)
2. `docs/queue/QUEUE_SPLIT_TRIGGERS.md` → `docs/queue/split-triggers.md` (12.4)
3. `docs/queue/QUEUE_SYSTEM_REPLICATION_SPEC.md` → `docs/queue/replication-spec.md` (12.5)
4. `docs/operations/runbooks/incident-response.md` → `docs/runbooks/incident-response.md` (15.5)
5. `docs/operations/runbooks/rollback.md` → `docs/runbooks/rollback.md` (15.6)
6. `docs/queue/queue-system-overview.md` (if exists at root) → `docs/queue/overview.md` (12.6)

## Files to Create (13 new)

Procedures:
1. 5.30 Add a procedure (meta)
2. 5.31 Restructure docs
3. 5.32 Create a skill
4. 5.33 Security incident response
5. 5.34 Code review
6. 5.15 Add ADR

Rewritten placeholders:
7. 5.3 Manage profiles (full content)
8. 5.5 Add queue category (full content)
9. 5.8 Dependency upgrade (full content)
10. 5.10 Extract service (full content)
11. 5.14 Incident rollback (full content)
12. 5.19 Release prep (full content)
13. 5.20 Scaffold module (full content)

## Net Change

- **Before:** ~100 files
- **Delete:** 9 files
- **Merge (net):** -4 files (8→4)
- **Move:** 0 net change (reorganize)
- **Create:** 13 files
- **After:** ~75-80 files

Plus: All procedures fully populated, clear structure, no redundancy.
