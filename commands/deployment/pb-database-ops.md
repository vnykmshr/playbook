---
name: "pb-database-ops"
title: "Database Operations"
category: "deployment"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-db', 'pb-dr', 'pb-deployment']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 865 to 296 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Database Operations

Operate databases reliably: migrations, backups, performance tuning, and failover. This guide covers the full lifecycle of database operations in production.

**Mindset:** Database operations embody `/pb-design-rules` thinking: Repair (databases should recover from failures), Transparency (make database health visible), and Least Surprise (changes should be predictable). Use `/pb-preamble` thinking to challenge "it works on my machine" assumptions.

Data is the most valuable asset. Treat database operations with appropriate care.

**Resource Hint:** sonnet - database operations, migration design, and performance tuning

---

## When to Use This Command

- **Planning database migration** - Schema changes, data migrations
- **Setting up backups** - Establishing backup and recovery strategy
- **Performance issues** - Database slow, queries timing out
- **Disaster recovery** - Failover planning and testing
- **Pre-deployment** - Reviewing database changes for safety

---

## Quick Reference

| Operation | Frequency | Risk Level |
|-----------|-----------|------------|
| Migrations | Per deployment | Medium-High |
| Backups | Continuous/Daily | Low (verify!) |
| Performance tuning | As needed | Low-Medium |
| Failover | When required | High |
| Maintenance | Weekly/Monthly | Low |

---

## Migration Strategies

### Expand/Contract Pattern

The safest approach for schema changes:

```
Phase 1: EXPAND (add new, keep old)
  - Add new column/table
  - Application writes to both old and new
  - No breaking changes

Phase 2: MIGRATE (move data)
  - Backfill data from old to new
  - Verify data integrity

Phase 3: CONTRACT (remove old)
  - Application uses only new
  - Remove old column/table (separate deployment)
```

### Zero-Downtime Migrations

**Safe operations (no lock, no downtime):**
- Adding a nullable column
- Adding an index concurrently
- Adding a new table
- Adding a column with a default (PostgreSQL 11+)

**Dangerous operations (can lock or break):**
- Adding NOT NULL constraint to existing column
- Changing column type
- Dropping column used by running code
- Adding unique constraint on large table

```sql
-- DANGEROUS: This locks the table
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- SAFER: Add constraint as NOT VALID first
ALTER TABLE users ADD CONSTRAINT users_email_not_null
  CHECK (email IS NOT NULL) NOT VALID;

-- Then validate in background (PostgreSQL)
ALTER TABLE users VALIDATE CONSTRAINT users_email_not_null;
```

### Backward-Compatible Changes

Every migration should be backward compatible with the previous code version.

**Rule:** Code version N-1 must work with schema version N.

---

## Backup Automation

For backup strategy (3-2-1 rule, retention), see `/pb-dr`. This section covers implementation.

---

## Failover Patterns

For DR-level failover planning, see `/pb-dr`. This section covers database-specific patterns.

---

## Connection Pooling

### Why Pooling Matters

**Without pooling:**
```
100 app instances × 10 connections each = 1000 DB connections
```

**With pooling:**
```
100 app instances → PgBouncer → 100 DB connections
```

---

## Monitoring & Alerting

### Key Database Metrics

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Connection count | > 70% max | > 85% max | Scale pool or optimize |
| Replication lag | > 1 second | > 10 seconds | Investigate network/load |
| Transaction rate | Varies | Sudden drop | Possible lock or issue |
| Query latency P99 | > 2x baseline | > 5x baseline | Investigate queries |
| Disk usage | > 70% | > 85% | Expand or clean |
| Cache hit ratio | < 95% | < 90% | Increase shared_buffers |

---

## Common Runbooks

### Slow Query Diagnosis

```markdown
## Runbook: Slow Query Investigation

### Symptoms
- High latency alerts
- Users reporting slow pages
- Database CPU elevated

### Investigation

1. **Identify slow queries**
   ```sql
   SELECT query, mean_exec_time, calls
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 5;
   ```

2. **Check for locks**
   ```sql
   SELECT * FROM pg_stat_activity
   WHERE wait_event_type = 'Lock';
   ```

3. **Analyze query plan**
   ```sql
   EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
   ```

4. **Check for missing indexes**
   ```sql
   SELECT * FROM pg_stat_user_tables
   WHERE seq_scan > idx_scan;
   ```

### Resolution
- Add missing index
- Optimize query
- Increase work_mem for specific query
- Kill blocking query if necessary

### Escalation
If not resolved in 30 minutes, escalate to database team.
```

### Connection Exhaustion

```markdown
## Runbook: Connection Exhaustion

### Symptoms
- "too many connections" errors
- Application unable to connect
- Connection count at max_connections

### Investigation

1. **Check current connections**
   ```sql
   SELECT state, count(*)
   FROM pg_stat_activity
   GROUP BY state;
   ```

2. **Find connection leaks**
   ```sql
   SELECT client_addr, usename, count(*)
   FROM pg_stat_activity
   GROUP BY client_addr, usename
   ORDER BY count DESC;
   ```

3. **Find idle in transaction**
   ```sql
   SELECT pid, now() - xact_start as duration, query
   FROM pg_stat_activity
   WHERE state = 'idle in transaction'
   ORDER BY xact_start;
   ```

### Resolution
- Kill idle connections: `SELECT pg_terminate_backend(pid);`
- Increase max_connections (temporary)
- Fix application connection leaks
- Add/configure connection pooler

### Prevention
- Use connection pooling (PgBouncer)
- Set statement_timeout
- Set idle_in_transaction_session_timeout
```

### Replication Lag

```markdown
## Runbook: Replication Lag

### Symptoms
- Replica lag alerts
- Read queries returning stale data
- pg_stat_replication shows lag

### Investigation

1. **Check lag on primary**
   ```sql
   SELECT
     client_addr,
     state,
     pg_wal_lsn_diff(sent_lsn, replay_lsn) as byte_lag
   FROM pg_stat_replication;
   ```

2. **Check lag on replica**
   ```sql
   SELECT
     now() - pg_last_xact_replay_timestamp() as lag_seconds;
   ```

3. **Check replica I/O**
   Is replica disk saturated? Check iowait.

4. **Check network**
   Is there packet loss between primary and replica?

### Resolution
- If disk I/O: Increase replica IOPS
- If network: Fix network issues
- If recovery: Wait for replica to catch up
- If write load: Add more replicas

### Escalation
If lag > 5 minutes and not recovering, escalate.
```

---

## Related Commands

- `/pb-patterns-db` - Database architecture and design patterns
- `/pb-dr` - Disaster recovery planning and backup verification
- `/pb-deployment` - Deploy database migrations safely

---

*Data is the most valuable asset. Treat it with care.*
