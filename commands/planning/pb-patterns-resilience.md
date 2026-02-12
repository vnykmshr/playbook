---
name: "pb-patterns-resilience"
title: "Resilience & Protection Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-distributed', 'pb-patterns-async', 'pb-hardening', 'pb-incident']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Resilience & Protection Patterns

Patterns for making systems reliable under failure. These are defensive patterns added during or after implementation to protect against transient failures, cascading outages, resource exhaustion, and abuse.

---

## Purpose

Resilience patterns:
- **Protect against transient failures**: External services time out, networks flap
- **Prevent cascading outages**: One service down shouldn't take everything down
- **Control resource usage**: Rate limiting, connection isolation
- **Improve perceived reliability**: Caching reduces dependency on slow backends

**Mindset:** Use `/pb-preamble` thinking (challenge assumptions — do you actually need this pattern, or is the root cause fixable?) and `/pb-design-rules` thinking (Fail noisily and early; patterns should add clarity, not hide problems).

**Resource Hint:** sonnet — Pattern reference and application; implementation-level design decisions.

---

## When to Use

- Service calls fail intermittently and you need retry/backoff logic
- External dependencies go down and you need to prevent cascading failures
- API needs protection against abuse or resource exhaustion
- Adding a caching layer for performance and reliability

---

### Pattern: Retry with Exponential Backoff

**Problem:** External service timeout. Should we fail immediately or retry?

**Solution:** Retry a few times, wait longer between each attempt.

**How it works:**
```
Attempt 1: Fail immediately, wait 1 second
Attempt 2: Try again, wait 2 seconds
Attempt 3: Try again, wait 4 seconds
Attempt 4: Try again, wait 8 seconds
Attempt 5: Fail permanently

Why exponential? Gives external service time to recover.
Why 5? More than 5 usually means service is down.
```

**Python example:**
```python
import time

def call_with_retry(func, max_retries=5):
    """Call function with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, fail

            wait_time = 2 ** attempt  # 1, 2, 4, 8 seconds
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s")
            time.sleep(wait_time)

# Usage
def charge_payment():
    return payment_api.charge(amount=99.99)

call_with_retry(charge_payment)
```

**When to use:**
- Calling external APIs (network timeouts happen)
- Database operations (short temporary outages)
- NOT for validation errors (retrying won't help)
- NOT for authorization failures (retrying won't help)

**Gotchas:**
```
1. "Retry forever"
   Bad: Server stuck in retry loop
   Good: Max retries (usually 3-5)

2. "Retry synchronously"
   Bad: User waits 15 seconds (1+2+4+8) for result
   Good: Fail fast, queue for async retry

3. "No jitter"
   Bad: All clients retry at exact same time, thundering herd
   Good: Add random jitter (retry at 1-2 seconds, not exactly 1)
```

---

### Pattern: Circuit Breaker

**Problem:** External service is down. Calling it repeatedly wastes time, resources.

**Solution:** After N failures, stop calling for a while. Check periodically.

**States:**
```
Closed (Normal):
  Service working
  Calls go through
  Count failures

Open (Broken):
  Service down
  Fail immediately (don't try calling)
  After timeout, try one request

Half-Open (Testing):
  One request allowed through
  If succeeds: Close (back to normal)
  If fails: Open again (still broken)
```

**Visual:**
```
Normal state (Closed):
  Request → External Service → Success

Service goes down (Open after 5 failures):
  Request → Circuit Breaker → Fail Immediately
  (Don't even try calling service)

After timeout, test recovery (Half-Open):
  Request → Circuit Breaker → Try once → Success
  Circuit Closed (back to normal)
```

**Python example:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open

    def call(self, func):
        if self.state == 'open':
            # Check if timeout passed
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'half-open'
            else:
                raise CircuitBreakerOpen("Service unavailable")

        try:
            result = func()
            if self.state == 'half-open':
                self.state = 'closed'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
            raise

# Usage
breaker = CircuitBreaker()
try:
    breaker.call(lambda: external_api.get_data())
except CircuitBreakerOpen:
    # Service is down, use fallback or fail gracefully
    return cached_data_or_default
```

**When to use:**
- Calling external APIs (prevent cascading failures)
- Database connection pooling
- Any resource that might be temporarily down
- NOT for immediate failures you want to handle differently

---

### Pattern: Rate Limiting

**Problem:** API being abused. Too many requests from one client. Resources exhausted (CPU, memory, database).

**Solution:** Limit requests per time window. Too many requests? Reject or delay.

**Strategies:**

**1. Token Bucket (Recommended)**
```
Bucket holds N tokens
Every request uses 1 token
Tokens refill at rate R per second

Example: 100 tokens, refill 10/second
  Request 1: 100 → 99 tokens (OK)
  Request 2: 99 → 98 tokens (OK)
  ...
  Request 100: 1 → 0 tokens (OK)
  Request 101: 0 tokens (REJECTED)
  After 1 second: Refilled to 10 tokens
  After 10 seconds: Refilled to 100 tokens
```

**2. Sliding Window (Simple but Less Accurate)**
```
Count requests in last N seconds
Too many requests? Reject

Example: Max 100 requests per minute
  11:00:00 - 11:00:59: 100 requests (at limit)
  11:01:00: First old request falls out
  Request 101 now allowed (oldest expired)
```

**3. Leaky Bucket (Fair, Process at Constant Rate)**
```
Requests arrive at variable rate
Leak (process) at constant rate

Like a queue:
  Requests → [Bucket] → Processing at constant rate
  If bucket full: Reject or queue (backpressure)
```

**Python token bucket example:**
```python
import time
from threading import Lock

class RateLimiter:
    def __init__(self, capacity=100, refill_rate=10):
        """
        capacity: max tokens in bucket
        refill_rate: tokens per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()
        self.lock = Lock()

    def allow_request(self):
        """Check if request allowed."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill_time

            # Refill tokens
            refilled = elapsed * self.refill_rate
            self.tokens = min(
                self.capacity,
                self.tokens + refilled
            )
            self.last_refill_time = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def wait_if_needed(self):
        """Wait until request is allowed."""
        while not self.allow_request():
            time.sleep(0.1)

# Usage
limiter = RateLimiter(capacity=100, refill_rate=10)

if limiter.allow_request():
    print("Request allowed")
else:
    print("Rate limit exceeded")
    # Return 429 Too Many Requests
```

**Where to implement:**

1. **API Gateway (Best):** Rate limit before hitting services
   - All services protected
   - Single configuration point
   - Can reject early

2. **Individual Service:** Rate limit per service
   - Finer control (payment service stricter than logging)
   - Redundant (if gateway exists)

3. **Redis (Distributed):** Share limits across servers
   - Multiple API instances
   - Fair across load balancer

**Levels of rate limiting:**

```
Global (All users): 10,000 requests/minute
Per user: 100 requests/minute
Per IP: 50 requests/minute
Per endpoint: Payment API strict (10/minute), Logging lenient (1000/minute)
```

**HTTP Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1673456789 (unix timestamp)

429 Too Many Requests
Retry-After: 60
```

**When to use:**
- Public APIs (prevent abuse)
- Resource-intensive endpoints (batch processing, exports)
- Protecting against DDoS
- Fair-sharing (one user can't monopolize)
- Cost control (if calls cost money)

**Gotchas:**
```
1. "Too strict, blocks legitimate traffic"
   Bad: 1 request/minute on public API
   Good: Match expected usage (100/minute for public, 10,000 for internal)

2. "No distinction between client types"
   Bad: Free user and premium user same limit
   Good: Premium gets higher limit, free gets lower

3. "Rate limits not visible"
   Bad: Client gets 429 with no explanation
   Good: Send X-RateLimit headers + Retry-After

4. "In-memory only on single server"
   Bad: Multiple servers, each has separate limits
   Good: Use Redis for distributed counting

5. "No graceful degradation"
   Bad: Instant reject when at limit
   Good: Queue requests, process in order
```

---

### Pattern: Cache-Aside

**Problem:** Database is slow, customers wait. Same queries run repeatedly.

**Solution:** Check cache first, if miss, fetch from DB and cache it.

**How it works:**
```
Request arrives:
  1. Check cache: Is data there?
  2. Hit: Return immediately
  3. Miss: Query database, store in cache, return

Next request for same data:
  1. Check cache: Is data there?
  2. Hit: Return immediately (much faster)
```

**Code:**
```python
def get_user(user_id):
    # Check cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return cached

    # Cache miss, query database
    user = database.query(f"SELECT * FROM users WHERE id = {user_id}")

    # Store in cache for 5 minutes
    cache.set(f"user:{user_id}", user, expire=300)

    return user
```

**Tools:**
- Redis (fast, flexible, recommended)
- Memcached (simple, fast)
- Database query cache (depends on database)

**Pros:**
- Simple to implement
- Huge performance improvement (10-100x faster)
- Scales well (distribute caches across servers)

**Cons:**
- Stale data (cache might be old)
- Cache invalidation (when data changes)
- Memory cost (storing data twice)

**Gotchas:**
```
1. "Cache stampede"
   Bad: Key expires, 100 requests hit DB simultaneously
   Good: Use locks (only 1 request queries DB, others wait for cache)

2. "Stale data"
   Bad: User updates profile, sees old data
   Good: Invalidate cache on write (delete from cache)

3. "Unbounded growth"
   Bad: Cache grows until server runs out of memory
   Good: Set TTL (time to live) on all cache entries
```

---

### Pattern: Bulkhead

**Problem:** One part fails, brings down whole system. (If payments service crashes, orders service affected?)

**Solution:** Isolate resources. If one part is slow, doesn't affect others.

**How it works:**
```
Without Bulkheads (Shared Resources):
  [Payment Service] ← Slow API
  [Order Service]   ← Shares connection pool

Result: Payment service uses all connections, Order service blocked

With Bulkheads (Isolated Resources):
  [Payment Service] ← Slow API, own connection pool
  [Order Service]   ← Uses different connection pool

Result: Payment slow, but Order service unaffected
```

**Implementation:**
```python
# Without bulkheads (bad)
pool = ConnectionPool(size=10)  # Shared

def process_payment():
    # Might use 10 connections, starve other services
    for i in range(10):
        conn = pool.get_connection()

def process_order():
    # Can't get connections because payment took them all
    conn = pool.get_connection()


# With bulkheads (good)
payment_pool = ConnectionPool(size=5)
order_pool = ConnectionPool(size=5)

def process_payment():
    # Can use at most 5 connections
    for i in range(5):
        conn = payment_pool.get_connection()

def process_order():
    # Guaranteed at least 5 connections
    conn = order_pool.get_connection()
```

**Thread pool bulkhead:**
```python
from concurrent.futures import ThreadPoolExecutor

# Each service has own thread pool
payment_executor = ThreadPoolExecutor(max_workers=5)
order_executor = ThreadPoolExecutor(max_workers=5)

def slow_payment_api_call():
    # Can use at most 5 threads
    return payment_executor.submit(call_api)

def order_processing():
    # Guaranteed to have threads available
    return order_executor.submit(process)
```

**When to use:**
- Protecting against resource exhaustion
- Services with different loads (payment slow, orders fast)
- Critical systems that must stay available

---

## Pattern Interactions

### Circuit Breaker + Retry Interaction

**Wrong:** Retry without Circuit Breaker
```
[NO] Bad: Keep retrying failed service
Request 1 → Wait 1s, fail
Request 2 → Wait 2s, fail
Request 3 → Wait 4s, fail
...
Result: Slow cascading failure
```

**Right:** Circuit Breaker first, Retry later
```
[YES] Good: Circuit breaker detects failure, stops retrying
Request 1-5 → All fail → Circuit Breaker opens
Request 6 → Fail immediately (don't even try)
Request 7 → Half-open test → Success → Circuit closes
Retry: Automatic with exponential backoff for transient failures
```

### Cache-Aside + Bulkhead Interaction

**Problem:** Cache stampede with bulkhead
```
Key expires, 100 requests hit database
Bulkhead: Only 5 threads available
95 requests queued, 5 in progress
Database overloaded
```

**Solution:** Lock-based cache repopulation
```
Request 1: Cache miss → Gets lock → Queries DB
Requests 2-100: Cache miss → Wait for lock → Get value from request 1
Result: Only 1 database query, others served from cache
```

---

## Antipattern: Circuit Breaker Gone Wrong

**What happened:** Misconfigured protection

```
Scenario:
  Service B goes down
  Service A opens Circuit Breaker (stops calling B)
  Service A's request queue backs up
  Service A becomes slow

Cascade:
  Service C times out waiting for Service A
  Service C opens its Circuit Breaker
  Now both A and C affected because B is down

Lesson:
  Circuit Breaker helps temporarily
  Fix the root cause (why is Service B down?)
  Use async messaging to decouple
  Don't hide problems, solve them
```

---

## Related Commands

- `/pb-patterns-core` — Core architectural patterns (SOA, Event-Driven, Repository, DTO)
- `/pb-patterns-distributed` — Distributed patterns (Saga, CQRS, Eventual Consistency)
- `/pb-patterns-async` — Asynchronous patterns (Job Queues, Reactive Streams)
- `/pb-hardening` — Production security hardening
- `/pb-incident` — Incident response and recovery

---

*Created: 2026-02-07 | Category: Architecture | Tier: L*
