---
name: "pb-database-ops"
title: "Database Operations"
category: "deployment"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-db', 'pb-dr', 'pb-deployment']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Database Operations

Operate databases reliably: migrations, backups, performance tuning, and failover. This guide covers the full lifecycle of database operations in production.

**Mindset:** Database operations embody `/pb-design-rules` thinking: Repair (databases should recover from failures), Transparency (make database health visible), and Least Surprise (changes should be predictable). Use `/pb-preamble` thinking to challenge "it works on my machine" assumptions.

Data is the most valuable asset. Treat database operations with appropriate care.

**Resource Hint:** sonnet — database operations, migration design, and performance tuning

---

## When to Use This Command

- **Planning database migration** — Schema changes, data migrations
- **Setting up backups** — Establishing backup and recovery strategy
- **Performance issues** — Database slow, queries timing out
- **Disaster recovery** — Failover planning and testing
- **Pre-deployment** — Reviewing database changes for safety

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

For deployment-time migration patterns, see `/pb-deployment`. This section covers migration design and safety.

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

**Example: Renaming a column**

```sql
-- Phase 1: EXPAND - Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Application writes to both:
-- UPDATE users SET name = ?, full_name = ? WHERE id = ?;

-- Phase 2: MIGRATE - Backfill
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Phase 3: CONTRACT (later deployment) - Remove old
ALTER TABLE users DROP COLUMN name;
```

### Zero-Downtime Migrations

**Safe operations (no lock, no downtime):**
- Adding a nullable column
- Adding an index concurrently
- Adding a new table
- Adding a column with a default (PostgreSQL 11+)

```sql
-- Safe: Add nullable column
ALTER TABLE users ADD COLUMN email_verified BOOLEAN;

-- Safe: Add index concurrently (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Safe: Add column with default (PostgreSQL 11+)
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
```

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

```
Deploy sequence:
1. Deploy code that works with old AND new schema
2. Run migration
3. Deploy code that only uses new schema
4. (Later) Drop old schema elements
```

**Anti-pattern:**
```
1. Run migration that breaks old code
2. Deploy new code
   → GAP: Old code is broken during deployment
```

### Migration Rollback

Always have a rollback plan:

```sql
-- Forward migration
-- up.sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Rollback migration
-- down.sql
ALTER TABLE users DROP COLUMN phone;
```

**Test rollbacks before production:**
```bash
# Apply migration
psql -f migrations/001_add_phone.up.sql

# Verify application works
./verify_app.sh

# Test rollback
psql -f migrations/001_add_phone.down.sql

# Verify application still works
./verify_app.sh
```

---

## Backup Automation

For backup strategy (3-2-1 rule, retention), see `/pb-dr`. This section covers implementation.

### PostgreSQL Backup

**Logical backup (pg_dump):**
```bash
#!/bin/bash
# backup.sh - Daily logical backup

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql.gz"

# Dump with compression
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > /backups/$BACKUP_FILE

# Upload to object storage
aws s3 cp /backups/$BACKUP_FILE s3://backups/daily/

# Clean local file
rm /backups/$BACKUP_FILE

# Verify upload
aws s3 ls s3://backups/daily/$BACKUP_FILE || exit 1
```

**Physical backup (pg_basebackup):**
```bash
#!/bin/bash
# For point-in-time recovery

pg_basebackup -h $DB_HOST -U replication -D /backups/base \
  --checkpoint=fast --wal-method=stream

# Archive WAL files continuously
archive_command = 'cp %p /backups/wal/%f'
```

**Continuous archiving with WAL:**
```
postgresql.conf:
  archive_mode = on
  archive_command = 'cp %p /backup/wal/%f'
  archive_timeout = 300  # 5 minutes max
```

### Backup Verification Script

```bash
#!/bin/bash
# verify_backup.sh - Weekly verification

echo "=== Backup Verification $(date) ==="

# Download latest backup
LATEST=$(aws s3 ls s3://backups/daily/ | tail -1 | awk '{print $4}')
aws s3 cp s3://backups/daily/$LATEST /tmp/verify/

# Restore to test database
gunzip /tmp/verify/$LATEST
psql -h test-db -U admin -d verify_test -f /tmp/verify/*.sql

# Check row counts
EXPECTED_USERS=100000
ACTUAL_USERS=$(psql -h test-db -U admin -d verify_test -t -A -c \
  "SELECT COUNT(*) FROM users")

if [ "$ACTUAL_USERS" -lt "$EXPECTED_USERS" ]; then
  echo "ERROR: User count too low: $ACTUAL_USERS < $EXPECTED_USERS"
  exit 1
fi

# Check recent data exists (should have data from yesterday)
RECENT=$(psql -h test-db -U admin -d verify_test -t -A -c \
  "SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL '2 days'")

if [ "$RECENT" -eq "0" ]; then
  echo "ERROR: No recent data found"
  exit 1
fi

echo "=== Backup verification PASSED ==="

# Cleanup
psql -h test-db -U admin -c "DROP DATABASE verify_test"
```

### Backup Monitoring

Alert on backup failures:

```yaml
# Prometheus alert rules
groups:
- name: backup
  rules:
  - alert: BackupMissing
    expr: time() - backup_last_success_timestamp > 86400
    for: 1h
    labels:
      severity: critical
    annotations:
      summary: "No successful backup in 24 hours"

  - alert: BackupSizeAnomaly
    expr: backup_size_bytes < backup_size_bytes offset 1d * 0.5
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Backup size dropped by >50%"
```

---

## Performance Baselines

### Establishing Baselines

Before tuning, know what "normal" looks like:

```sql
-- Query performance baseline
SELECT
  calls,
  mean_exec_time,
  total_exec_time,
  rows,
  query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

**Document baselines:**
```markdown
## Performance Baseline: 2026-01-20

### Query Performance
| Query Pattern | Avg Time | P99 Time | Calls/day |
|---------------|----------|----------|-----------|
| User lookup by ID | 2ms | 10ms | 1M |
| User search | 50ms | 200ms | 100K |
| Report generation | 5s | 30s | 1K |

### Resource Utilization
| Metric | Avg | Peak |
|--------|-----|------|
| CPU | 40% | 70% |
| Memory | 60% | 80% |
| Connections | 50 | 100 |
| Disk IOPS | 1000 | 3000 |
```

### Query Performance Monitoring

```sql
-- Find slow queries (PostgreSQL)
SELECT
  (total_exec_time / 1000 / 60)::numeric(10,2) as total_min,
  mean_exec_time::numeric(10,2) as avg_ms,
  calls,
  query
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- Queries averaging > 100ms
ORDER BY total_exec_time DESC
LIMIT 10;

-- Find queries with high I/O
SELECT
  shared_blks_read + shared_blks_hit as total_blocks,
  shared_blks_read as disk_reads,
  query
FROM pg_stat_statements
ORDER BY shared_blks_read DESC
LIMIT 10;
```

### Index Optimization

**Find missing indexes:**
```sql
-- Tables with sequential scans (might need index)
SELECT
  schemaname,
  relname,
  seq_scan,
  seq_tup_read,
  idx_scan,
  idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;
```

**Find unused indexes:**
```sql
-- Indexes that are never used (candidates for removal)
SELECT
  schemaname,
  relname,
  indexrelname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Connection Tuning

```
# postgresql.conf

# Max connections (conservative)
max_connections = 200

# Connection-related memory
shared_buffers = 4GB                # 25% of RAM
effective_cache_size = 12GB         # 75% of RAM
work_mem = 64MB                     # Per-operation memory
maintenance_work_mem = 1GB          # For maintenance ops

# Connection reuse
tcp_keepalives_idle = 600
tcp_keepalives_interval = 30
tcp_keepalives_count = 10
```

---

## Failover Patterns

For DR-level failover planning, see `/pb-dr`. This section covers database-specific patterns.

### Primary/Replica Architecture

```
         ┌─────────────┐
         │   Primary   │ ← All writes
         │  (Leader)   │
         └──────┬──────┘
                │ Replication
        ┌───────┴───────┐
        ▼               ▼
┌─────────────┐  ┌─────────────┐
│  Replica 1  │  │  Replica 2  │ ← Read traffic
│  (Follower) │  │  (Follower) │
└─────────────┘  └─────────────┘
```

**PostgreSQL streaming replication:**
```
# Primary: postgresql.conf
wal_level = replica
max_wal_senders = 10
synchronous_commit = on          # For zero data loss
synchronous_standby_names = '*'  # Any replica

# Replica: postgresql.conf (PostgreSQL 12+)
# Note: recovery.conf was removed in PostgreSQL 12
primary_conninfo = 'host=primary port=5432 user=replication'
restore_command = 'cp /backup/wal/%f %p'
# Create standby signal file: touch $PGDATA/standby.signal
```

### Connection Routing

**PgBouncer for connection pooling:**
```ini
# pgbouncer.ini
[databases]
mydb = host=primary port=5432 dbname=mydb

[pgbouncer]
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50
```

**Application-level read/write splitting:**
```python
# Python example
import psycopg2

PRIMARY_URL = "postgresql://primary:5432/mydb"
REPLICA_URL = "postgresql://replica:5432/mydb"

def get_connection(readonly=False):
    if readonly:
        return psycopg2.connect(REPLICA_URL)
    return psycopg2.connect(PRIMARY_URL)

# Usage
with get_connection(readonly=True) as conn:
    # Read queries go to replica
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

with get_connection(readonly=False) as conn:
    # Writes go to primary
    cursor.execute("INSERT INTO users (...) VALUES (...)")
```

### Manual Failover Procedure

```bash
#!/bin/bash
# failover.sh - Manual database failover

echo "=== Starting database failover ==="

# 1. Verify primary is truly down
pg_isready -h primary -p 5432
if [ $? -eq 0 ]; then
  echo "ERROR: Primary appears to be up. Aborting."
  exit 1
fi

# 2. Check replica lag
LAG=$(psql -h replica -t -A -c "SELECT pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn())")
echo "Replica lag: $LAG bytes"

if [ "$LAG" -gt 1048576 ]; then  # 1MB
  echo "WARNING: High replication lag. Potential data loss."
  read -p "Continue? (yes/no) " CONFIRM
  if [ "$CONFIRM" != "yes" ]; then
    exit 1
  fi
fi

# 3. Promote replica
psql -h replica -c "SELECT pg_promote();"

# 4. Verify promotion
pg_isready -h replica -p 5432
IS_PRIMARY=$(psql -h replica -t -A -c "SELECT NOT pg_is_in_recovery()")

if [ "$IS_PRIMARY" = "t" ]; then
  echo "Replica promoted successfully"
else
  echo "ERROR: Promotion failed"
  exit 1
fi

# 5. Update connection strings (application-specific)
echo "Update APPLICATION_DATABASE_URL to point to replica"

echo "=== Failover complete ==="
```

---

## Connection Pooling

### Why Pooling Matters

Database connections are expensive:
- Memory per connection (~10MB for PostgreSQL)
- Process per connection (PostgreSQL)
- Connection setup time (~100ms)

**Without pooling:**
```
100 app instances × 10 connections each = 1000 DB connections
1000 connections × 10MB = 10GB just for connections
```

**With pooling:**
```
100 app instances → PgBouncer → 100 DB connections
```

### PgBouncer Configuration

```ini
# pgbouncer.ini

[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Pool modes:
# session: Connection held for entire client session (default, safest)
# transaction: Connection held for transaction only (most efficient)
# statement: Connection held for single statement (dangerous)
pool_mode = transaction

# Pool sizing
default_pool_size = 50         # Connections per database
min_pool_size = 10             # Keep this many warm
reserve_pool_size = 10         # Extra connections for bursts
max_client_conn = 1000         # Max client connections to pooler

# Timeouts
server_lifetime = 3600         # Recycle connections hourly
server_idle_timeout = 600      # Close idle server connections
client_idle_timeout = 300      # Close idle client connections

# Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
```

### Pool Monitoring

```sql
-- PgBouncer stats
SHOW POOLS;
SHOW STATS;
SHOW CLIENTS;
SHOW SERVERS;

-- Key metrics to monitor
-- cl_active: Active client connections
-- sv_active: Active server connections
-- sv_idle: Idle server connections
-- maxwait: Max time client waited for connection
```

**Alert on pool exhaustion:**
```yaml
# Prometheus alert
- alert: PgBouncerPoolExhausted
  expr: pgbouncer_pools_sv_active / pgbouncer_pools_max_connections > 0.9
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "PgBouncer pool near capacity"
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

### PostgreSQL Monitoring Queries

```sql
-- Connection usage
SELECT
  count(*) as total_connections,
  count(*) FILTER (WHERE state = 'active') as active,
  count(*) FILTER (WHERE state = 'idle') as idle,
  max_conn.setting::int as max_connections
FROM pg_stat_activity
CROSS JOIN (SELECT setting FROM pg_settings WHERE name = 'max_connections') max_conn
GROUP BY max_conn.setting;

-- Replication lag (on replica)
SELECT
  CASE
    WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0
    ELSE EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp())
  END AS lag_seconds;

-- Cache hit ratio (handles zero activity case)
SELECT
  CASE
    WHEN sum(heap_blks_hit) + sum(heap_blks_read) = 0 THEN NULL
    ELSE sum(heap_blks_hit)::float / (sum(heap_blks_hit) + sum(heap_blks_read))
  END as cache_hit_ratio
FROM pg_statio_user_tables;

-- Lock contention
SELECT
  relation::regclass,
  mode,
  count(*) as lock_count
FROM pg_locks
WHERE granted = false
GROUP BY relation, mode;
```

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

## Integration with Playbook

**Part of operational excellence:**
- `/pb-deployment` — Migration deployment patterns
- `/pb-dr` — Database disaster recovery
- `/pb-observability` — Database metrics and alerting
- `/pb-database-ops` — Full database operations (this command)

---

## Related Commands

- `/pb-patterns-db` — Database architecture and design patterns
- `/pb-dr` — Disaster recovery planning and backup verification
- `/pb-deployment` — Deploy database migrations safely

**Workflow:**
```
Schema design → Migration development
    ↓
Migration testing (staging)
    ↓
Production deployment (/pb-deployment)
    ↓
Monitoring (/pb-observability)
    ↓
Operational issues → These runbooks
    ↓
Major failures → /pb-dr
```

---

## Quick Reference

| Operation | Command/Query |
|-----------|---------------|
| Check connections | `SELECT count(*) FROM pg_stat_activity;` |
| Check replication lag | `SELECT now() - pg_last_xact_replay_timestamp();` |
| Find slow queries | `SELECT * FROM pg_stat_statements ORDER BY mean_exec_time DESC;` |
| Kill connection | `SELECT pg_terminate_backend(pid);` |
| Promote replica | `SELECT pg_promote();` |
| Create index concurrently | `CREATE INDEX CONCURRENTLY ...;` |
| Check locks | `SELECT * FROM pg_locks WHERE NOT granted;` |

---

*Data is the most valuable asset. Treat it with care.*
