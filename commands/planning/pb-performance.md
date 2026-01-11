# Performance Optimization & Scalability

Make systems faster without breaking them. Measure, optimize the right thing, verify improvements.

---

## Purpose

Performance matters:
- Users leave sites that are slow (every 100ms delay = 1% users gone)
- Slow systems cost money (more servers, more bandwidth)
- Performance bugs are production bugs (optimize before scaling)

**Key principle:** Measure first, optimize what matters, prove it works.

---

## When to Optimize

### [NO] DON'T Optimize:

- Too early: Before you have users / load
- Without measurement: Guessing slows you down more
- Working features: If it works fine for current users, leave it
- Premature: "This might be slow someday"
- Diminishing returns: Optimizing 1% of total time

### [YES] DO Optimize:

- When users complain: "Site is slow"
- When metrics show problem: P99 latency > target
- When load tests show bottleneck: Load test reveals breaking point
- When cost is high: More servers than should be needed
- Hot paths: Code that runs for every user request

---

## Performance Profiling: Find the Problem

### Rule 1: Measure First

Most developers guess wrong about what's slow.

```
Without profiling (80% wrong):
  "The database must be slow"
  → Actually: JSON serialization is slow (60% of time)

With profiling (100% correct):
  "Database queries are 15% of time, JSON serialization is 60%"
  → Optimize JSON serialization first (biggest payoff)
```

### Tools by Layer

**Frontend Performance:**
- Chrome DevTools > Performance tab (record, identify slow frames)
- Lighthouse (scores performance, provides fixes)
- WebPageTest (waterfall chart of load time)
- Bundle analyzer (webpack-bundle-analyzer shows package size)

**Backend Performance:**
- Profilers: py-spy (Python), node --prof (Node), JProfiler (Java)
- Benchmarking: timeit (Python), benchmark (Node), JMH (Java)
- Database: EXPLAIN ANALYZE (query plan), slow query log
- Tracing: See `/pb-observability` for OpenTelemetry

**Load Testing:**
- ab (Apache Bench) - simple HTTP load
- wrk - fast, scriptable load testing
- k6 - load testing as code
- Locust - Python-based, distributed load testing

### Profiling Example: Python

```python
# Quick profiling with cProfile
import cProfile
import pstats

cProfile.run('my_function()', 'output.prof')
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative').print_stats(10)  # Show top 10 by time

# Result:
#   ncalls  tottime  cumtime
#   100     0.050    2.340  <- Slow! 2.3 seconds per 100 calls
#   100000  1.500    1.800  <- Hot! 1.8 seconds across 100k calls
```

### Profiling Example: Node.js

```bash
# Run with profiler
node --prof app.js

# Process output
node --prof-process isolate-*.log > profile.txt

# Shows:
# [Shared libraries]: 50ms
# app.js:123 handleRequest(): 450ms  <- HOT SPOT
# database.js:45 query(): 320ms      <- Second hottest
```

---

## Common Performance Bottlenecks

### Bottleneck 1: Database Queries (Often 60-80% of time)

**Symptoms:**
- P99 latency high
- Database CPU at 100%
- Slow query log full

**Root causes:**
```
1. N+1 queries: Loop and query inside loop
   Bad:    for user in users:
             user.orders = db.query("SELECT * FROM orders WHERE user_id = ?")
   Good:   orders = db.query("SELECT * FROM orders WHERE user_id IN (?)", user_ids)

2. Missing index: Query scans whole table
   Bad:    SELECT * FROM users WHERE created_at > ?  (no index)
   Good:   CREATE INDEX idx_created_at ON users(created_at)

3. SELECT * with large tables
   Bad:    SELECT * FROM users  (returns 50 columns, but you use 5)
   Good:   SELECT id, name, email FROM users

4. Slow JOIN: Join large tables with poor keys
   Bad:    SELECT * FROM users JOIN orders ON users.id = orders.user_id WHERE status IN (...)
   Good:   Add index on orders(user_id, status)
```

**Solutions:**
```python
# N+1 solution: Batch load
users = db.query("SELECT * FROM users LIMIT 100")
user_ids = [u.id for u in users]
orders = db.query("SELECT * FROM orders WHERE user_id IN ?", user_ids)
for user in users:
    user.orders = [o for o in orders if o.user_id == user.id]

# Missing index solution
db.execute("CREATE INDEX idx_email ON users(email)")
db.execute("ANALYZE TABLE users")  # Update stats

# SELECT * solution
cursor.execute("SELECT id, name, email FROM users")  # Only columns needed
```

### Bottleneck 2: Serialization/Deserialization (Often 30-40% of time)

**Symptoms:**
- CPU high but database responsive
- Memory usage spiking
- Frontend slow receiving responses

**Root causes:**
```
1. Serializing large objects
   Bad:    return User.objects.all()  (serializes 100k users)
   Good:   return User.objects.all()[:100]  (paginate)

2. JSON serialization inefficient
   Bad:    json.dumps(large_dict)  (Python's json is slow)
   Good:   import ujson; ujson.dumps(large_dict)  (3x faster)

3. Encoding/decoding mismatch
   Bad:    UTF-8 → Latin-1 → UTF-8 conversion
   Good:   Use UTF-8 consistently

4. Compression disabled
   Bad:    Response Content-Length: 5MB (no compression)
   Good:   Content-Encoding: gzip, Size: 500KB (100x smaller)
```

**Solutions:**
```python
# Pagination solution
# Before: 10 seconds to serialize 100k users
users = User.objects.all()  # DON'T
users = User.objects.all()[:100]  # DO

# Fast JSON solution
import ujson  # or orjson, which is even faster
response = ujson.dumps(data)  # 3-5x faster

# Enable compression
from flask import Flask, compress
app = Flask(__name__)
compress = Compress(app)  # Automatic gzip on responses

# Selective serialization
# Bad: serialize everything
return User.to_dict()  # includes password, tokens, etc

# Good: serialize only needed fields
return {
    'id': user.id,
    'name': user.name,
    'email': user.email
}
```

### Bottleneck 3: Caching Missing (40-60% speedup possible)

**Symptoms:**
- Same queries running repeatedly
- Same calculations done repeatedly
- Database CPU high from repeated work

**Solutions by layer:**

**1. HTTP Caching (Fastest, on client)**
```python
# Tell browsers to cache responses
@app.route('/api/products/<id>')
def get_product(id):
    resp = make_response(product_json)
    resp.cache_control.max_age = 3600  # Cache 1 hour
    resp.cache_control.public = True   # OK to cache in CDN
    return resp

# Result: 99% of requests served from browser cache, 0 DB queries
```

**2. CDN Caching (Very fast, geographic distribution)**
```python
# Cloudflare, CloudFront, Fastly configure:
# - Cache static assets forever (add hash to filename for updates)
# - Cache API responses (5-60 minutes)
# - Gzip compression automatic

GET /api/products/123
# First request: 200ms (origin)
# Next 1000 requests: 5ms (CDN in user's region)
```

**3. Application Caching (In-memory, very fast)**
```python
# Redis cache expensive queries
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/trending')
@cache.cached(timeout=300)  # Cache 5 minutes
def get_trending():
    # This query runs once every 5 minutes (not 1000x/minute)
    return db.query("SELECT * FROM products ORDER BY views DESC LIMIT 10")

# Result: 30 seconds → 30ms (1000x faster)
```

**Cache invalidation:**
See `/pb-adr` for cache invalidation patterns (event-driven, TTL, manual, hybrid).

### Bottleneck 4: Inefficient Algorithms (Often 10-20% of time)

**Symptoms:**
- CPU high, database responsive
- Scales poorly (10x users → 100x slower)
- Memory usage high

**Examples:**
```python
# BAD: O(n²) algorithm
def find_duplicates(items):
    result = []
    for i, item1 in enumerate(items):
        for j, item2 in enumerate(items):  # WRONG: Inner loop
            if item1 == item2 and i != j:
                result.append(item1)
    return result
# 10,000 items = 100M comparisons

# GOOD: O(n) algorithm
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates
# 10,000 items = 10k comparisons (10,000x faster!)

# BAD: String concatenation in loop
result = ""
for line in lines:
    result += line  # Creates new string each time, O(n²)

# GOOD: List join
result = "".join(lines)  # Single allocation, O(n)
```

### Bottleneck 5: Synchronous I/O (Often 70-90% of time)

**Symptoms:**
- Server CPU low (40% used)
- But slow requests (P99 > 1s)
- Can't handle concurrent users

**Root cause:** Waiting for I/O (database, API calls, disk)

**Solutions:**

```python
# BAD: Synchronous, blocks everything
@app.route('/checkout')
def checkout():
    validate_cart()        # 50ms
    charge_card()          # 500ms (blocked, waiting for payment processor)
    send_email()           # 200ms (blocked, waiting for mail server)
    return "Done"          # 750ms total

# GOOD: Async, parallelizes I/O
import asyncio

@app.route('/checkout')
async def checkout():
    await asyncio.gather(
        validate_cart(),   # 50ms
        charge_card(),     # 500ms (parallel)
        send_email()       # 200ms (parallel)
    )
    return "Done"          # 500ms total (payment time, email parallel)

# GOOD: Queue for non-blocking
@app.route('/checkout')
def checkout():
    validate_cart()        # 50ms
    charge_card()          # 500ms
    queue_email_job.delay(user_id)  # 5ms (async task queue)
    return "Done"          # 555ms (email sent in background)
```

---

## Load Testing: Find Breaking Point

### Before Optimizing

Run load test to find what breaks under load.

```bash
# Simple load test: 1000 requests, 10 concurrent
wrk -t 10 -c 10 -d 10s http://localhost:8000/

# Results:
Requests/sec:   150.5  (good, or slow?)
Latency avg:    66ms
Latency max:    250ms
99th percentile: 195ms

# Question: Is this good?
# Answer: Depends on target
#   If target is 1000 req/sec: FAIL (150 vs 1000)
#   If target is 500 users: FAIL (need to handle 500x more)
#   If current is 50 req/sec: PASS (3x improvement)
```

### Load Test Your Bottleneck

```bash
# Test specific endpoint known to be slow
wrk -t 20 -c 100 -d 60s -s optimize.lua http://localhost:8000/api/search

# Results before optimization: 150 req/sec, P99 = 800ms
# Run optimization...
# Results after optimization: 500 req/sec, P99 = 150ms
# Improvement: 3.3x throughput, 5.3x latency (GOOD)
```

---

## Optimization by Layer

### Layer 1: Frontend (Browsers, 30-50% of load time)

**Don't optimize if:**
- Server latency is 500ms, frontend is 100ms (server is bigger problem)
- Users complain about features, not speed (add features first)

**Do optimize if:**
- Frontend is > 40% of total time
- Users complain "site feels slow" (even if server fast)
- Lighthouse score is red (< 50)

**Quick wins:**
```
1. Lazy load images (Intersection Observer)
   Before: Load 50 images on page load
   After: Load only visible images, rest on scroll
   Impact: 50% faster initial load

2. Code splitting (load JS only for pages needed)
   Before: app.js (5MB) - load everything
   After: app.js (500KB) + pages/*js (500KB each)
   Impact: 90% faster initial page load

3. Defer non-critical CSS
   Before: <link rel="stylesheet" href="style.css">
   After: <link rel="stylesheet" href="critical.css"> (in head)
          <link rel="stylesheet" href="non-critical.css"> (defer loading)
   Impact: 30% faster first paint

4. Remove unused dependencies
   Before: moment.js (67KB) for date formatting
   After: date-fns (5KB) or native Date
   Impact: 90% smaller bundle
```

### Layer 2: API Server (30-50% of load time)

**Quick wins:**
```
1. Add caching (HTTP, CDN, Redis)
   Before: Every request hits database
   After: 95% served from cache
   Impact: 10-100x faster

2. Add compression (gzip)
   Before: 5MB response
   After: 500KB (gzipped)
   Impact: 10x smaller, 100x faster on slow networks

3. Batch API calls (N+1 → N/10)
   Before: 100 requests to load 100 users' orders
   After: 10 batch requests
   Impact: 90% fewer connections

4. Increase parallelization (async/await)
   Before: Chain calls (call A, then B, then C = A+B+C time)
   After: Parallel calls (call A, B, C together = MAX(A,B,C) time)
   Impact: 50-70% faster if A=B=C
```

### Layer 3: Database (40-70% of load time)

**Quick wins:**
```
1. Add indexes
   Before: Full table scan 50,000 rows
   After: Index lookup 1 row
   Impact: 100-1000x faster

2. Fix N+1 queries
   Before: 100 separate queries for 100 items
   After: 1 query with batch load
   Impact: 100x fewer DB connections

3. Denormalize data
   Before: JOIN 5 tables to get one row of data
   After: Precompute and cache joined result
   Impact: 10-50x faster queries

4. Shard data
   Before: All 100M users in one table
   After: 100 shards (1M users each)
   Impact: Parallel queries, better scalability
```

### Layer 4: Infrastructure (Rare, only if other layers maxed)

**Quick wins:**
```
1. Increase instance size (vertical scaling)
   Before: t2.small (1 CPU, 1GB RAM)
   After: t3.xlarge (4 CPU, 16GB RAM)
   Impact: 3-4x more throughput (diminishing)

2. Add more instances (horizontal scaling)
   Before: 1 server serving 1000 users
   After: 10 servers serving 1000 users each
   Impact: Linear scaling (10x throughput)

3. Use better algorithm for infrastructure
   Before: Single database with replicas
   After: Sharded database (parallel queries)
   Impact: 10-100x more throughput
```

---

## Optimization Checklist

### Before Optimizing

- [ ] Measure current performance (baseline)
- [ ] Define target (P99 < 200ms? Throughput > 10k req/sec?)
- [ ] Profile to find bottleneck
- [ ] Run load test to see breaking point

### While Optimizing

- [ ] Change one thing at a time (measure impact of each)
- [ ] Run load test after each change
- [ ] Keep track of improvements
- [ ] Don't over-optimize (diminishing returns)

### After Optimizing

- [ ] Verify improvement with load test
- [ ] Set up monitoring for metric (so it doesn't regress)
- [ ] Document changes (what changed, why, what improved)
- [ ] Check side effects (did you break something else?)

---

## Common Optimization Mistakes

### [NO] Mistake 1: Optimize Wrong Layer

```
Problem: "Website slow"
Blind optimization: Spend 2 weeks optimizing frontend
Measure first: Actually, frontend 100ms, API 800ms
Right fix: Optimize API (80% of problem)
Lesson: Measure first, optimize biggest impact
```

### [NO] Mistake 2: Optimize Before Growth

```
Situation: Brand new startup, 10 users
Blind: Spend 3 months optimizing for 10k users
Reality: Spend time on features instead
Lesson: Optimize when you need to (when traffic grows or metrics slip)
```

### [NO] Mistake 3: Premature Microservices

```
Problem: App slow
Blind: "Let's use microservices!"
Reality: Microservices slower (network latency between services)
Lesson: Monolith fast, microservices slow (use when you need independent scaling)
```

### [NO] Mistake 4: Cache Everything

```
Problem: "Cache will make it faster"
Blind: Cache expensive query (updates hourly)
Reality: Cache becomes stale, users see wrong data
Lesson: Cache read-heavy data, not mutable data
```

---

## Integration with Playbook

**Part of design and deployment:**
- `/pb-guide` — Section 4.4 covers performance requirements
- `/pb-observability` — Set up monitoring to catch performance regressions
- `/pb-adr` — Architecture decisions affect performance
- `/pb-release` — Load test before releasing at scale

**Related Commands:**
- `/pb-observability` — Monitor P99 latency and throughput
- `/pb-guide` — Performance requirements during design phase
- `/pb-incident` — Performance degradation is incident (if sudden)

---

## Performance Optimization Checklist

### Planning Phase

- [ ] Define performance targets (P99, throughput, user experience)
- [ ] Benchmark current state (baseline)
- [ ] Profile to identify bottleneck
- [ ] Run load test to see current breaking point

### Optimization Phase

- [ ] Optimize Layer 1 (if 40%+ of time): Frontend, bundle size
- [ ] Optimize Layer 2 (if 40%+ of time): API caching, compression, batching
- [ ] Optimize Layer 3 (if 40%+ of time): Database indexes, N+1 fixes
- [ ] Optimize Layer 4 (if other layers maxed): Infrastructure scaling
- [ ] Measure impact after each change
- [ ] Don't over-optimize (diminishing returns)

### Verification Phase

- [ ] Load test reaches target throughput
- [ ] P99 latency < target
- [ ] No side effects (features still work)
- [ ] Set up monitoring to track metric
- [ ] Document changes (what and why)

---

*Created: 2026-01-11 | Category: Planning | Tier: M/L*

