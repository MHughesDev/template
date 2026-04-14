# skills/ai-rag/ai-kill-switch.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Profile: optional AI/RAG profile -->
<!-- - Related docs: docs/architecture/ai-rag-chromadb.md -->

> PURPOSE: [OPTIONAL] TODO — Composer 2 implements full §6.2 skill content for ai-kill-switch in the AI/RAG domain. Only relevant when the ai-rag profile is enabled.

## Purpose
> CONTENT: What this AI/RAG skill enables.

## When to Invoke
> CONTENT: Specific triggers (only when AI profile is enabled).

## Prerequisites
> CONTENT: AI profile enabled, ChromaDB running, packages/ai/ configured.

## Relevant Files/Areas
> CONTENT: packages/ai/, docs/architecture/ai-rag-chromadb.md

## Step-by-Step Method
> CONTENT: Numbered AI/RAG procedure steps.

## Command Examples
> CONTENT: docker compose --profile ai up, relevant Python CLI commands.

## Validation Checklist
> CONTENT:
> - [ ] AI profile enabled and configured
> - [ ] ChromaDB accessible
> - [ ] Kill switch tested

## Common Failure Modes
> CONTENT: ChromaDB connectivity, embedding failures.

## Handoff Expectations
> CONTENT: AI feature verified, kill switch tested.

## Related Procedures
> CONTENT: docs/procedures/enable-profile.md

## Related Prompts
> CONTENT: prompts/implementation_agent.md

## Related Rules
> CONTENT: .cursor/rules/security.md (AI_ENABLED kill switch)
