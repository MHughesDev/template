# docs/queue/queue-intelligence.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Per spec §17.11 and §26.12 item 355 -->
<!-- - Machinery: skills/agent-ops/queue-intelligence.py -->

> PURPOSE: Conceptual documentation for the queue intelligence layer: DAG, complexity, batching, conflict detection. Per spec §17.11.

## Overview

> CONTENT: One paragraph. The intelligence layer extends the queue beyond naive FIFO with dependency-aware ordering, complexity estimation, batch suggestions, and conflict detection. It informs human decisions without auto-editing the CSV.

## Dependency Graph Resolution (§17.11.1)

> CONTENT: How the DAG is built from the dependencies column. How readiness is determined (all deps in archive with status=done). Cycle detection. The make queue:graph output format (Mermaid).

## Complexity Estimation (§17.11.2)

> CONTENT: How advisory complexity scores (S/M/L/XL or 1-10) are derived: summary keyword analysis, git history, transitive dependency depth, category heuristics. Advisory only — does not reorder CSV.

## Automatic Batching (§17.11.3)

> CONTENT: How batch suggestions are made: same module context, shared prerequisites, schema+API pairs, test+implementation pairs. Humans confirm by setting the same batch value — system does not auto-edit.

## Conflict Detection (§17.11.4)

> CONTENT: How file overlap is detected across open items. How merge conflict risk is flagged. Ordering suggestions (fewer shared files second).

## Using the Intelligence Tools

> CONTENT: Step-by-step guide for human maintainers:
> 1. make queue:graph → review dependency visualization
> 2. make queue:analyze → read batch and conflict suggestions
> 3. Review and manually set batch values in queue.csv based on suggestions
> 4. Agents then process items in batch order
