# docs/operations/database-operations.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- Optional per spec §26.12 item 402 -->

> PURPOSE: Database operations: VACUUM, indexes, pool tuning, slow queries. Per spec §26.12 item 402.

## VACUUM and ANALYZE

> CONTENT: PostgreSQL maintenance: when to run VACUUM ANALYZE, autovacuum settings, monitoring table bloat.

## Index Management

> CONTENT: Creating indexes safely in production: CREATE INDEX CONCURRENTLY, monitoring usage, removing unused indexes.

## Connection Pool Tuning

> CONTENT: SQLAlchemy pool_size, max_overflow, pool_timeout settings. How to diagnose pool exhaustion.

## Slow Query Identification

> CONTENT: Enable pg_stat_statements, identify slow queries via pg_slow_statements, explain analyze patterns.
