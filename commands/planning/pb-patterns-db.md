# Database Patterns

Patterns for efficient, scalable database operations.

**Caveat:** Database patterns solve specific problems. Use `/pb-preamble` thinking (question assumptions) and `/pb-design-rules` thinking (especially Simplicity and Transparency—can you keep it simple and observable?).

Challenge the assumption that the database is the bottleneck. Question whether you need this complexity. Measure before optimizing.

**Resource Hint:** sonnet — Database pattern reference; implementation-level data layer decisions.

---

## Purpose

Database patterns:
- **Maximize throughput** - More requests per second
- **Minimize latency** - Faster response times
- **Ensure consistency** - Data integrity
- **Enable scalability** - Handle growth without redesign
- **Prevent failures** - Graceful degradation

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

**How it works:**
```
Without pooling:
  Request 1 → Create connection → Query → Close → Response (slow)
  Request 2 → Create connection → Query → Close → Response (slow)

With pooling:
  Pool: [Connection 1] [Connection 2] [Connection 3]

  Request 1 → Borrow Connection 1 → Query → Return Connection 1
  Request 2 → Borrow Connection 2 → Query → Return Connection 2
  Request 3 → Borrow Connection 3 → Query → Return Connection 3
  Request 4 → Wait for Connection 1 to be free → Borrow → Query → Return
```

**Python Example (using psycopg2 with built-in pooling):**
```python
from psycopg2 import pool
import psycopg2

# Create connection pool
import os

connection_pool = pool.SimpleConnectionPool(
    minconn=5,      # Minimum 5 connections kept
    maxconn=20,     # Maximum 20 connections
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST", "localhost"),
    database=os.environ.get("DB_NAME", "myapp")
)

def get_user(user_id):
    # Borrow connection from pool
    conn = connection_pool.getconn()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        return user
    finally:
        # Return connection to pool (important!)
        connection_pool.putconn(conn)
```

**JavaScript:** Use `pg.Pool` with `max`, `idleTimeoutMillis` configuration. Always `client.release()` in finally block.

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
- `min_connections`: Start with (CPU cores * 2) + extra for spikes
- `max_connections`: Set based on database max connections
- `idle_timeout`: 30 seconds (PostgreSQL default)
- Monitor: Pool usage, connection creation rate, slow queries

**Pros:**
- Huge performance improvement (10-100x faster than creating connections)
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

```
Find user (1 query)
Find user's orders (N queries, one per user)
Total: 1 + N queries (bad!)
```

**Solution:** Fetch related data in single query (JOIN) or batch.

**Bad Example:**
```python
# [NO] N+1 queries
users = db.query("SELECT * FROM users")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)
    user.orders = orders
    # Result: 1 query for users + N queries for orders = N+1 total
```

**Good Solution 1: JOIN Query**
```python
# [YES] 1 query using JOIN
query = """
SELECT users.*, orders.* FROM users
LEFT JOIN orders ON orders.user_id = users.id
"""
results = db.query(query)

# Group results
users_dict = {}
for row in results:
    user_id = row['user_id']
    if user_id not in users_dict:
        users_dict[user_id] = {'id': row['user_id'], 'orders': []}
    users_dict[user_id]['orders'].append({'id': row['order_id']})

users = list(users_dict.values())
```

**Good Solution 2: Batch Query**
```python
# [YES] 2 queries: one for users, one for all orders
users = db.query("SELECT * FROM users")
user_ids = [u.id for u in users]

orders = db.query(
    "SELECT * FROM orders WHERE user_id IN (?)",
    [user_ids]  # Batch all IDs in one query
)

# Group orders by user
orders_by_user = {}
for order in orders:
    if order.user_id not in orders_by_user:
        orders_by_user[order.user_id] = []
    orders_by_user[order.user_id].append(order)

# Attach to users
for user in users:
    user.orders = orders_by_user.get(user.id, [])
```

**Good Solution 3: ORM With Eager Loading**
```python
# [YES] 1 query (ORM handles JOIN)
from sqlalchemy.orm import joinedload

users = db.query(User).options(joinedload(User.orders)).all()
# ORM automatically fetches orders with users
```

### Problem: Missing Indexes

**Problem:** Queries scan entire table (slow).

**Solution:** Create indexes on frequently queried columns.

**Example:**
```sql
-- [NO] Without index: Full table scan (1,000,000 rows scanned)
SELECT * FROM orders WHERE customer_id = 123;

-- [YES] With index: Direct lookup (10 rows scanned)
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
SELECT * FROM orders WHERE customer_id = 123;
```

**Index Checklist:**
```
☐ WHERE clause columns - indexed?
☐ JOIN columns - indexed?
☐ ORDER BY columns - indexed?
☐ Too many indexes? (slows down writes)
☐ Unused indexes? (delete them)
```

**Query Analysis:**
```python
# Use EXPLAIN to see execution plan
import psycopg2

conn = psycopg2.connect(...)
cursor = conn.cursor()

# Show execution plan
cursor.execute("EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123")
plan = cursor.fetchall()
for row in plan:
    print(row)

# Look for: "Seq Scan" (bad, no index) vs "Index Scan" (good)
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

**How it works:**
```
Primary Database:
  - Receives writes
  - Logs all changes
  - Sends log to replicas

Replica 1 (Read-only):
  - Receives log from primary
  - Applies changes
  - Serves read queries

Replica 2 (Read-only):
  - Receives log from primary
  - Applies changes
  - Serves read queries
```

**Architecture:**
```
Writes → [Primary Database] → Replication Log
                                ↓
                        [Replica 1] (reads)
                        [Replica 2] (reads)
                        [Replica 3] (reads)

Application:
  - Write queries → Primary
  - Read queries → Replica (round-robin or least-connections)
```

**Implementation:**
```python
from psycopg2 import pool

import os

# Connection to primary (for writes)
primary_pool = pool.SimpleConnectionPool(
    minconn=5, maxconn=10,
    host=os.environ.get("DB_PRIMARY_HOST", "primary.db.example.com"),
    database=os.environ.get("DB_NAME", "myapp"),
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD")
)

# Connection to replicas (for reads)
replica_hosts = [
    os.environ.get("DB_REPLICA_1", "replica1.db.example.com"),
    os.environ.get("DB_REPLICA_2", "replica2.db.example.com"),
]

replica_pools = [
    pool.SimpleConnectionPool(
        minconn=5, maxconn=10,
        host=host,
        database=os.environ.get("DB_NAME", "myapp"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD")
    )
    for host in replica_hosts
]

def get_write_connection():
    """Get connection to primary for writes."""
    return primary_pool.getconn()

def get_read_connection():
    """Get connection to replica for reads (round-robin)."""
    import random
    replica_pool = random.choice(replica_pools)
    return replica_pool.getconn()

# Usage
async def get_user(user_id):
    # Read from replica
    conn = get_read_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()

async def update_user(user_id, name):
    # Write to primary
    conn = get_write_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = %s WHERE id = %s",
            (name, user_id)
        )
        conn.commit()
    finally:
        conn.close()
```

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

**How it works:**
```
Sharding by customer_id:

Shard 1 (customers 1-1000):
  [Orders for customer 1-1000]
  [Payments for customer 1-1000]

Shard 2 (customers 1001-2000):
  [Orders for customer 1001-2000]
  [Payments for customer 1001-2000]

Application:
  shard_id = customer_id % num_shards  (or hash(customer_id))
  Connect to shard_id database
  Execute query
```

**Implementation:**
```python
def get_shard_id(customer_id, num_shards=4):
    """Determine which shard this customer belongs to."""
    return customer_id % num_shards

def get_shard_connection(customer_id):
    """Get connection to appropriate shard."""
    import os
    shard_id = get_shard_id(customer_id)
    hosts = [
        os.environ.get("DB_SHARD_0", "shard0.db.example.com"),
        os.environ.get("DB_SHARD_1", "shard1.db.example.com"),
        os.environ.get("DB_SHARD_2", "shard2.db.example.com"),
        os.environ.get("DB_SHARD_3", "shard3.db.example.com"),
    ]
    shard_host = hosts[shard_id]
    return psycopg2.connect(
        host=shard_host,
        database=os.environ.get("DB_NAME", "myapp"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD")
    )

async def get_customer_orders(customer_id):
    """Get orders for customer from correct shard."""
    conn = get_shard_connection(customer_id)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM orders WHERE customer_id = %s",
            (customer_id,)
        )
        return cursor.fetchall()
    finally:
        conn.close()
```

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

**Python Example:**
```python
def transfer_money(from_account_id, to_account_id, amount):
    """Transfer money from one account to another."""
    conn = db.connect()

    try:
        # Start transaction
        cursor = conn.cursor()

        # Deduct from source account
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s",
            (amount, from_account_id)
        )

        # Check balance is not negative
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (from_account_id,))
        balance = cursor.fetchone()[0]
        if balance < 0:
            raise ValueError("Insufficient funds")

        # Add to destination account
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s",
            (amount, to_account_id)
        )

        # Commit all changes together
        conn.commit()
        return {"success": True}

    except Exception as e:
        # Rollback on any error
        conn.rollback()
        return {"success": False, "error": str(e)}

    finally:
        conn.close()
```

**Isolation Levels:**
```
READ UNCOMMITTED:
  Can read uncommitted changes (dirty reads) - avoid

READ COMMITTED (Default):
  Can't read uncommitted changes
  But can see committed changes during transaction (non-repeatable reads)

REPEATABLE READ:
  Snapshot of data at transaction start
  Consistent view throughout transaction

SERIALIZABLE:
  Complete isolation (as if transactions run one at a time)
  Slowest, but safest
```

**PostgreSQL Example:**
```python
cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
# Now all queries in this transaction see consistent data snapshot
```

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

**Bad (Slow):**
```python
# [NO] N individual queries (slow)
for user in users:
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (user.name, user.email)
    )
    conn.commit()
```

**Good (Fast):**
```python
# [YES] 1 batch query (fast)
cursor.executemany(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    [(user.name, user.email) for user in users]
)
conn.commit()
```

**Multi-Row Insert (Fastest):**
```python
# [YES] Super fast - single SQL statement
query = """
INSERT INTO users (name, email) VALUES
(%s, %s),
(%s, %s),
(%s, %s),
...
"""
values = []
for user in users:
    values.extend([user.name, user.email])

cursor.execute(query, values)
conn.commit()
```

**Performance Comparison:**
```
Individual inserts: 1000 rows → 10 seconds
Batch inserts (50 rows per batch): 1000 rows → 200ms
Multi-row insert: 1000 rows → 50ms
```

---

## Caching Strategies

### Write-Through Cache

**How it works:**
```
Write:
  1. Write to cache
  2. Write to database (synchronously)
  3. Return to client

Read:
  1. Check cache
  2. If miss, query database
  3. Store in cache
  4. Return to client
```

**Pros:**
- Data always consistent (cache = database)
- Simple to reason about

**Cons:**
- Every write hits database (slower)

### Write-Behind Cache

**How it works:**
```
Write:
  1. Write to cache only
  2. Return to client immediately
  3. Asynchronously flush to database (background)

Read:
  1. Check cache
  2. If miss, query database
  3. Store in cache
  4. Return to client
```

**Pros:**
- Very fast writes (cache only)
- Database load spread out

**Cons:**
- Data inconsistency if cache crashes before flush
- Complex implementation

---

## Denormalization & Materialized Views

**Problem:** Normalized database is slow for reads. Too many JOINs, too slow.

**Scenario:**
```
Normalized schema:
  Users table
  Orders table
  Order_Items table
  Products table

Query: Get user with all order details
  SELECT users.*, orders.*, order_items.*, products.*
  FROM users
  JOIN orders ON users.id = orders.user_id
  JOIN order_items ON orders.id = order_items.order_id
  JOIN products ON order_items.product_id = products.id
  (4 table JOINs = slow!)
```

**Solution:** Denormalize - store pre-computed results for fast reads.

**Two Approaches:**

**1. Denormalized Table (Application-Managed)**

Store copied data in a denormalized table. Application keeps it in sync.

**Example:**
```sql
-- Normalized: 4 JOINs to get order details
SELECT users.*, orders.*, order_items.*, products.*
FROM users
JOIN orders ...
JOIN order_items ...
JOIN products ...

-- Denormalized: 1 simple query
CREATE TABLE user_orders_denormalized (
  id BIGINT PRIMARY KEY,
  user_id INT,
  user_name VARCHAR(255),
  order_id INT,
  order_total DECIMAL(10, 2),
  order_created_at TIMESTAMP,
  item_name VARCHAR(255),
  item_quantity INT,
  item_price DECIMAL(10, 2),
  product_category VARCHAR(100)
);

-- Fast read: Single table query
SELECT * FROM user_orders_denormalized WHERE user_id = 123;
```

**Keeping denormalized table in sync:**
```python
def create_order(user_id, items):
    """Create order and update denormalized table."""
    with db.transaction():
        # Insert into normalized tables
        order = insert_order(user_id, items)

        # Denormalize: Copy relevant data
        user = get_user(user_id)
        for item in items:
            product = get_product(item.product_id)

            db.execute(
                """INSERT INTO user_orders_denormalized
                   (user_id, user_name, order_id, order_total, item_name, item_quantity, item_price, product_category)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                user.id, user.name, order.id, order.total,
                product.name, item.quantity, item.price, product.category
            )

        return order
```

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

**SQL Example:**
```sql
-- Create materialized view (pre-computed result)
CREATE MATERIALIZED VIEW user_orders_mv AS
SELECT
  users.id as user_id,
  users.name as user_name,
  orders.id as order_id,
  orders.total as order_total,
  orders.created_at as order_created_at,
  products.name as item_name,
  order_items.quantity as item_quantity,
  products.price as item_price,
  categories.name as product_category
FROM users
JOIN orders ON users.id = orders.user_id
JOIN order_items ON orders.id = order_items.order_id
JOIN products ON order_items.product_id = products.id
JOIN categories ON products.category_id = categories.id;

-- Create index on materialized view for fast lookups
CREATE INDEX idx_user_orders_mv_user_id ON user_orders_mv(user_id);

-- Fast read: Query materialized view
SELECT * FROM user_orders_mv WHERE user_id = 123;

-- Refresh materialized view (recompute)
REFRESH MATERIALIZED VIEW user_orders_mv;
```

**PostgreSQL Incremental Refresh (Efficient):**
```sql
-- Create materialized view with no data
CREATE MATERIALIZED VIEW user_orders_mv AS
SELECT ... FROM ...;

-- PostgreSQL extension for incremental refresh
CREATE OR REPLACE FUNCTION refresh_user_orders_mv()
RETURNS void AS
'SELECT count(*) FROM pg_matviews WHERE matviewname = ''user_orders_mv'''
LANGUAGE SQL;

-- Refresh only changed data (more efficient than full refresh)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_orders_mv;
```

**Refresh Strategies:**

1. **Full Refresh (Slow but Complete)**
```
REFRESH MATERIALIZED VIEW user_orders_mv;
-- Recomputes entire view (might be slow for large datasets)
```

2. **Scheduled Refresh (Periodic)**
```python
import schedule
import time

def refresh_materialized_views():
    """Refresh views every hour."""
    with db.connect() as conn:
        conn.execute("REFRESH MATERIALIZED VIEW user_orders_mv")
        conn.execute("REFRESH MATERIALIZED VIEW product_analytics_mv")
    print("Materialized views refreshed")

# Schedule every hour
schedule.every(1).hours.do(refresh_materialized_views)

while True:
    schedule.run_pending()
    time.sleep(60)
```

3. **Event-Driven Refresh (Real-time)**
```python
def create_order(user_id, items):
    """Create order and refresh materialized view."""
    with db.transaction():
        # Create order
        order = insert_order(user_id, items)

        # Refresh only relevant materialized view
        db.execute("REFRESH MATERIALIZED VIEW user_orders_mv")

    return order
```

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

**Comparison:**

```
Denormalized Table (Application-managed):
  Pros: Flexible, can store anything
  Cons: Must keep in sync manually, risk of inconsistency

Materialized View (Database-managed):
  Pros: Simpler, database maintains, can refresh incrementally
  Cons: Less flexible, refresh overhead
```

---

## Pattern Interactions

**Typical Production Database Setup:**

```
Application
    ↓
[Connection Pool] (reuses connections)
    ↓
[Read/Write Router]
    ↓
Primary Database          Replica 1          Replica 2
(Write queries)          (Read queries)     (Read queries)
    ↓                         ↓                  ↓
(Optimized indexes)  (Replication lag 1-2 sec)
    ↓
[Application Cache]
(Redis, Memcached)
    ↓
[Batch Operations]
(reduce query count)
```

---

## Antipatterns

**Unoptimized Queries:**
```python
# [NO] No indexes, full table scans
SELECT * FROM orders WHERE customer_id = 123;

# [YES] With index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Connection Leak:**
```python
# [NO] Connection never returned to pool
conn = get_connection()
result = conn.query("...")
# Forgot to close/return!

# [YES] Always return connection
try:
    conn = get_connection()
    result = conn.query("...")
finally:
    return_connection(conn)
```

**Reading after write without waiting:**
```python
# [NO] Replication lag - might read old data from replica
write_to_primary(data)
read_from_replica(id)  # Might not see write yet!

# [YES] Read from primary after write
write_to_primary(data)
read_from_primary(id)  # Guaranteed to see write
```

---

## Go Examples

**Connection Pooling with database/sql:**

```go
// Go: Built-in connection pooling with database/sql
package main

import (
    "database/sql"
    "fmt"
    "os"
    "time"

    _ "github.com/lib/pq" // PostgreSQL driver
)

func main() {
    // database/sql automatically manages connection pooling
    db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil {
        panic(err)
    }
    defer db.Close()

    // Configure connection pool
    db.SetMaxOpenConns(25)          // Max 25 open connections
    db.SetMaxIdleConns(5)            // Keep 5 idle connections
    db.SetConnMaxLifetime(5 * time.Minute) // Close connections after 5 min

    // Health check - verify connection pool is working
    if err := db.Ping(); err != nil {
        panic(err)
    }

    // Query with automatic connection pooling
    row := db.QueryRow("SELECT id, name FROM users WHERE id = $1", 123)
    var id int
    var name string
    if err := row.Scan(&id, &name); err != nil {
        fmt.Println("Query failed:", err)
        return
    }

    fmt.Printf("User %d: %s\n", id, name)
}
```

Other patterns (Query Optimization, Replication, Sharding, Transactions, Batch Operations, Caching) follow similar Go idioms using `database/sql`. Key points:
- Use prepared statements for repeated queries
- Use transactions (`db.Begin()`) for multi-step operations
- Use batch operations for bulk inserts
- Always close rows with `defer rows.Close()`

---

## Related Commands

- `/pb-patterns-core` — Core architectural and design patterns
- `/pb-patterns-distributed` — Distributed patterns (saga, CQRS, eventual consistency)
- `/pb-database-ops` — Database operations (migrations, backups, connection pooling)
- `/pb-performance` — Performance optimization and profiling strategies
- `/pb-patterns` — Pattern overview and quick reference
