---
name: "pb-patterns-db"
title: "Database Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-distributed', 'pb-database-ops', 'pb-performance', 'pb-patterns']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 1046 to 307 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Database Patterns

Patterns for efficient, scalable database operations.

**Caveat:** Database patterns solve specific problems. Use `/pb-preamble` thinking (question assumptions) and `/pb-design-rules` thinking (especially Simplicity and Transparency: can you keep it simple and observable?).

Challenge the assumption that the database is the bottleneck. Question whether you need this complexity. Measure before optimizing.

**Resource Hint:** sonnet - Database pattern reference; implementation-level data layer decisions.

---

## When to Use Database Patterns

**Use database patterns when:**
- Database is performance bottleneck
- System scales beyond single database
- Need high availability or disaster recovery
- Consistency requirements are critical

**Don't use when:**
- Database is not bottleneck
- System is small (single database sufficient)
- Complexity outweighs benefits

---

## Connection Pooling

**Problem:** Creating new database connection for each request is slow. Connections are expensive.

**Solution:** Reuse connections. Pool holds ready-to-use connections.

**Gotchas:**
```
1. "Connection leak"
   Bad: Borrow connection but never return it
   Good: Always use try/finally to return connection

2. "Pool exhaustion"
   Bad: All connections in use, new requests blocked
   Good: Monitor pool usage, increase max connections if needed

3. "Timeout on borrow"
   Bad: Application waits forever for available connection
   Good: Set timeout, fail fast if no connection available
```

**Configuration Tips:**
- `max_connections`: Set based on database max connections
- Monitor: Pool usage, connection creation rate, slow queries

**Pros:**
- Simple to implement (most libraries have built-in)
- Automatic connection reuse

**Cons:**
- Requires tuning (finding right pool size)
- Easy to leak connections
- Resource overhead (idle connections consume memory)

---

## Query Optimization

### Problem: N+1 Query Problem

**Problem:** Fetching objects and then related objects one at a time.

**Solution:** Fetch related data in single query (JOIN) or batch.

### Problem: Missing Indexes

**Problem:** Queries scan entire table (slow).

**Solution:** Create indexes on frequently queried columns.

**Index Checklist:**
```
☐ WHERE clause columns - indexed?
☐ JOIN columns - indexed?
☐ ORDER BY columns - indexed?
☐ Too many indexes? (slows down writes)
☐ Unused indexes? (delete them)
```

**Gotchas:**
```
1. "Over-indexing"
   Bad: Index on every column
   Good: Index only on columns used in WHERE/JOIN/ORDER BY

2. "Composite index wrong order"
   Bad: CREATE INDEX (city, name) but query only by name
   Good: Index order matches query patterns

3. "Index fragmentation"
   Bad: Index becomes fragmented over time
   Good: Rebuild indexes periodically (REINDEX)
```

---

## Database Replication

**Problem:** Single database is single point of failure. High load on single instance.

**Solution:** Copy data to replicas. Route reads to replicas, writes to primary.

**Gotchas:**
```
1. "Replication lag"
   Problem: Write to primary, read from replica immediately sees old data
   Solution: Read from primary after write, or wait for replica to catch up

2. "Replica failure"
   Problem: Replica goes down, application still tries to read from it
   Solution: Health check, route around failed replica

3. "Data inconsistency"
   Problem: Replica is behind primary
   Solution: Accept eventual consistency, or read from primary
```

**Pros:**
- Scale reads (many replicas)
- High availability (replicas become primary if primary fails)
- Analytics (dedicated replica for reporting)

**Cons:**
- Eventual consistency (replicas behind)
- Operational complexity (more servers to manage)
- Replication lag issues

---

## Database Sharding

**Problem:** Database too large for single server. Need to scale writes.

**Solution:** Split data across multiple databases based on shard key.

**Choosing Shard Key:**
- Good: `customer_id`, `user_id`, `company_id` (queries naturally by this key)
- Bad: `order_id` (hard to query across shards later)
- Bad: `timestamp` (uneven distribution, hot shards)

**Gotchas:**
```
1. "Queries across shards"
   Problem: Need data from multiple shards
   Solution: Scatter-gather (query all shards, merge results)

2. "Resharding"
   Problem: Need to add more shards as system grows
   Solution: Planned, use consistent hashing, plan ahead

3. "Hot shards"
   Problem: Some shards get more traffic than others
   Solution: Better shard key choice, or pre-split shards

4. "Distributed transactions"
   Problem: Transaction spans multiple shards
   Solution: Avoid if possible, use eventual consistency
```

**Pros:**
- Scale writes (each shard handles portion)
- Scale storage (data distributed)
- Performance (smaller databases faster)

**Cons:**
- Complex queries (might span shards)
- Resharding painful (moving data)
- Distributed transactions difficult

---

## Transaction Management

**Problem:** Multiple operations need to succeed or fail together.

**Solution:** Use transactions. All-or-nothing.

**Gotchas:**
```
1. "Long transactions"
   Bad: Transaction holds locks for too long
   Good: Keep transactions short, minimize work in transaction

2. "Deadlocks"
   Bad: Transaction A waits for Transaction B, B waits for A
   Good: Always acquire locks in same order

3. "Lost updates"
   Bad: Transaction 1 reads value, Transaction 2 updates it, Transaction 1 overwrites
   Good: Use SELECT FOR UPDATE to lock row during transaction
```

---

## Batch Operations

**Problem:** Inserting/updating many rows one at a time is slow.

**Solution:** Batch multiple operations in single call.

---

## Caching Strategies

### Write-Through Cache

**Pros:**
- Data always consistent (cache = database)
- Simple to reason about

**Cons:**
- Every write hits database (slower)

### Write-Behind Cache

**Pros:**
- Very fast writes (cache only)
- Database load spread out

**Cons:**
- Data inconsistency if cache crashes before flush
- Complex implementation

---

## Denormalization & Materialized Views

**Problem:** Normalized database is slow for reads. Too many JOINs, too slow.

**Solution:** Denormalize - store pre-computed results for fast reads.

**Two Approaches:**

**1. Denormalized Table (Application-Managed)**

Store copied data in a denormalized table. Application keeps it in sync.

**Pros:**
- Fast reads (no JOINs)
- Simple queries
- Flexible (store whatever denormalization needed)

**Cons:**
- Data duplication (extra storage)
- Consistency risks (keep in sync manually)
- Complex updates (change in one place affects multiple tables)

**2. Materialized Views (Database-Managed)**

Database creates and maintains denormalized view.

**When to use:**

- Normalized queries have too many JOINs (>3)
- Read performance critical (reporting, analytics)
- Data doesn't change frequently
- Can tolerate slight inconsistency

**Gotchas:**
```
1. "Stale data"
   Bad: Materialized view not refreshed, shows old data
   Good: Schedule refreshes, or refresh on data change

2. "Storage bloat"
   Bad: Denormalized tables duplicate all data
   Good: Only denormalize frequently-read columns

3. "Consistency nightmare"
   Bad: Denormalized data out of sync with source
   Good: Automate refresh, use database triggers

4. "Complex updates"
   Bad: Update one table, must update denormalized copies
   Good: Use application transactions, or database constraints
```

---

## Related Commands

- `/pb-patterns-core` - Core architectural and design patterns
- `/pb-patterns-distributed` - Distributed patterns (saga, CQRS, eventual consistency)
- `/pb-database-ops` - Database operations (migrations, backups, connection pooling)
- `/pb-performance` - Performance optimization and profiling strategies
- `/pb-patterns` - Pattern overview and quick reference
