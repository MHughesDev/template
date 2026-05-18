---
doc_id: "6.11"
title: "monitoring"
section: "Operations"
status: "pending-init"
summary: "What is instrumented, alert conditions and thresholds, first-look checklist, dashboards. Populated during initialization from IDEA.md §13."
updated: "2026-05-17"
---

# Monitoring
<!-- derived from: IDEA.md §13 — populated by repo_initialize -->

## Metrics

| Metric | Source | Alert threshold |
|--------|--------|-----------------|
| _[Request rate]_ | _[API]_ | _[Baseline + 50%]_ |
| _[Error rate]_ | _[API]_ | _[>1%]_ |
| _[Latency p99]_ | _[API]_ | _[>500ms]_ |

## Dashboards

_[Links or description of monitoring dashboards]_

## First-look checklist

1. _[Check error rate]_
2. _[Check resource utilization]_
3. _[Check upstream dependencies]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
