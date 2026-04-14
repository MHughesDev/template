# docs/operations/database-operations.md

<!-- Optional per spec §26.12 item 402 -->

**Purpose:** Database operations: VACUUM, indexes, pool tuning, slow queries. Per spec §26.12 item 402.

## VACUUM and ANALYZE

PostgreSQL maintenance: when to run VACUUM ANALYZE, autovacuum settings, monitoring table bloat.

## Index Management

Creating indexes safely in production: CREATE INDEX CONCURRENTLY, monitoring usage, removing unused indexes.

## Connection Pool Tuning

SQLAlchemy pool_size, max_overflow, pool_timeout settings. How to diagnose pool exhaustion.

## Slow Query Identification

Enable pg_stat_statements, identify slow queries via pg_slow_statements, explain analyze patterns.
