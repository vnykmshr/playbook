# Common Architecture & Design Patterns

Proven solutions to recurring problems. Patterns speed up design and prevent mistakes.

---

## Purpose

Patterns:
- **Accelerate design**: Don't solve the same problem twice
- **Share knowledge**: Common vocabulary for discussion
- **Prevent mistakes**: Patterns have gotchas documented
- **Improve quality**: Use proven solutions, not experimental ones
- **Enable communication**: "Let's use the retry pattern" means something

---

## When to Use Patterns

**Use patterns when:**
- Problem is common (many projects have this issue)
- Solution is proven (multiple implementations work well)
- Trade-offs are understood (know pros/cons)
- Context fits (pattern matches your system)

**Don't use patterns when:**
- Problem is unique (no precedent)
- Pattern seems forced (doesn't fit naturally)
- Simple solution exists (YAGNI - You Aren't Gonna Need It)
- System is too small (overkill)

---

## Architectural Patterns

### Pattern: Service-Oriented Architecture (SOA)

**Problem:** Monolithic system is too big, scales badly, hard to test.

**Solution:** Break into independent services, each handling one thing.

**Structure:**
```
Monolith:
  [All code - Orders, Payments, Users, Inventory in one codebase]

SOA:
  [Order Service] ←→ [Payment Service]
       ↓ API calls
  [User Service] ←→ [Inventory Service]
```

**How it works:**
```
1. Each service owns its data (no shared database)
2. Services communicate via API (HTTP, gRPC, etc.)
3. Each service deployed independently
4. Each service has its own database
```

**Example: E-commerce**
```
- Order Service: Creates orders, tracks status
- Payment Service: Processes payments, refunds
- Inventory Service: Tracks stock, decrements
- User Service: Manages users, profiles
- Notification Service: Sends emails, SMS

Each service:
  - Has own database
  - Exposed via REST API
  - Deployed separately
  - Developed by own team
```

**Pros:**
- ✅ Independent scaling (payment service under load? Scale just that)
- ✅ Independent deployment (order service update doesn't affect payments)
- ✅ Technology flexibility (use Node for one, Python for another)
- ✅ Clear boundaries (easy to understand what each does)

**Cons:**
- ❌ Operational complexity (many services to manage)
- ❌ Network latency (services talking over network)
- ❌ Data consistency harder (each has own database)
- ❌ Debugging harder (request spans multiple services)

**When to use:**
- Team size > 10 people (each team owns a service)
- Different parts scale differently (payments need more resources)
- Different parts use different tech stacks
- System is too large for one team

**Gotchas:**
```
1. "Too fine-grained services" — 20 services, each service per endpoint
   Bad: Too much operational overhead
   Good: 3-5 services, each service per business domain

2. "Synchronous everywhere" — Service A calls B calls C
   Bad: Slow, cascading failures
   Good: Async messaging (service A publishes event, B listens)

3. "Sharing databases" — All services use same DB
   Bad: Defeats purpose (tightly coupled)
   Good: Each service owns its data
```

---

### Pattern: Event-Driven Architecture

**Problem:** Systems are tightly coupled (Order service must know about Payment service).

**Solution:** Services publish events, others listen. No direct coupling.

**How it works:**
```
Traditional (Tightly coupled):
  1. User submits order
  2. Order Service calls Payment Service
  3. Payment Service calls Inventory Service
  4. Inventory Service calls Notification Service

Problem: If Payment Service is slow, Order Service blocks

Event-Driven (Loosely coupled):
  1. User submits order
  2. Order Service creates order → publishes "order.created" event
  3. Payment Service listens, charges payment
  4. Inventory Service listens, decrements stock
  5. Notification Service listens, sends email

Benefit: Services don't know about each other
```

**Technology:**
- Event bus: RabbitMQ, Kafka, AWS SNS/SQS, Google Pub/Sub
- Event format: JSON events with type and data

**Example event:**
```json
{
  "type": "order.created",
  "timestamp": "2026-01-11T14:30:00Z",
  "order_id": "order_123",
  "customer_id": "cust_456",
  "items": [
    {"product_id": "prod_1", "quantity": 2}
  ],
  "total": 99.99
}
```

**Service subscribing:**
```javascript
eventBus.subscribe('order.created', async (event) => {
  console.log(`Processing order ${event.order_id}`);

  // Decrement inventory
  await inventoryService.decrementStock(event.items);

  // Publish event for others
  await eventBus.publish('inventory.updated', {
    order_id: event.order_id,
    status: 'decremented'
  });
});
```

**Pros:**
- ✅ Loose coupling (services don't know about each other)
- ✅ Scalable (can add listeners without changing publisher)
- ✅ Resilient (if one service is slow, doesn't block others)
- ✅ Debuggable (event history is audit trail)

**Cons:**
- ❌ Harder to debug (request spans multiple services asynchronously)
- ❌ Eventual consistency (order created, payment might fail later)
- ❌ Operational complexity (need event broker)
- ❌ Ordering challenges (events might arrive out of order)

**Gotchas:**
```
1. "Event published but nobody listening"
   Bad: Event disappears, nobody processes it
   Good: Monitor for unprocessed events, alert if missing listeners

2. "Event processed twice"
   Bad: Payment processed twice, customer charged twice
   Good: Idempotent processing (processing same event twice = safe)

3. "No ordering guarantees"
   Bad: "order.created" arrives before "order.confirmed"
   Good: Listeners handle events arriving in any order
```

---

## Design Patterns

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

**TypeScript example:**
```typescript
async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 5
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      const waitTime = Math.pow(2, attempt) * 1000; // milliseconds
      console.log(`Attempt ${attempt + 1} failed, retrying in ${waitTime}ms`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
  }
}

// Usage
await callWithRetry(() => paymentService.charge(99.99));
```

**When to use:**
- ✅ Calling external APIs (network timeouts happen)
- ✅ Database operations (short temporary outages)
- ❌ NOT for validation errors (retrying won't help)
- ❌ NOT for authorization failures (retrying won't help)

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
- ✅ Calling external APIs (prevent cascading failures)
- ✅ Database connection pooling
- ✅ Any resource that might be temporarily down
- ❌ NOT for immediate failures you want to handle differently

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
- ✅ Simple to implement
- ✅ Huge performance improvement (10-100x faster)
- ✅ Scales well (distribute caches across servers)

**Cons:**
- ❌ Stale data (cache might be old)
- ❌ Cache invalidation (when data changes)
- ❌ Memory cost (storing data twice)

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
- ✅ Protecting against resource exhaustion
- ✅ Services with different loads (payment slow, orders fast)
- ✅ Critical systems that must stay available

---

## Data Access Patterns

### Pattern: Repository Pattern

**Problem:** Data access code scattered everywhere. Hard to test. Hard to change database.

**Solution:** Central place for data access. All queries go through repository.

**Structure:**
```
Without Repository:
  User Service → SQL queries directly → Database
  Order Service → SQL queries directly → Database
  (Duplication, hard to test)

With Repository:
  User Service → User Repository → Database
  Order Service → Order Repository → Database
  (Centralized, easy to test)
```

**Example:**
```python
class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, user_id):
        """Get user by ID."""
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)

    def create(self, email, name):
        """Create new user."""
        result = self.db.execute(
            "INSERT INTO users (email, name) VALUES (?, ?)",
            email, name
        )
        return result.lastrowid

    def update(self, user_id, email=None, name=None):
        """Update user."""
        if email:
            self.db.execute("UPDATE users SET email = ? WHERE id = ?", email, user_id)
        if name:
            self.db.execute("UPDATE users SET name = ? WHERE id = ?", name, user_id)

    def delete(self, user_id):
        """Delete user."""
        self.db.execute("DELETE FROM users WHERE id = ?", user_id)

# Usage
repo = UserRepository(db)
user = repo.get_by_id(123)
repo.update(123, name="New Name")
```

**Benefits:**
- ✅ Centralized data access (one place to change queries)
- ✅ Easy to test (mock repository for unit tests)
- ✅ Easy to swap databases (change repository, not whole app)
- ✅ Consistency (same query patterns everywhere)

---

### Pattern: DTO (Data Transfer Object)

**Problem:** Return database object directly. If database schema changes, API breaks.

**Solution:** Create separate object for API responses. API only returns DTOs.

**How it works:**
```
Without DTO (Tight coupling):
  Database: user {id, email, password_hash, created_at, updated_at}
  API returns entire user object
  Client sees password_hash (security issue!)
  Schema change breaks API

With DTO (Loose coupling):
  Database: user {id, email, password_hash, created_at, updated_at}
  API: class UserDTO {id, email, name}
  API returns only DTO fields
  Schema changes, API unchanged
```

**Example:**
```python
# Database model (has extra fields)
class User:
    id: int
    email: str
    password_hash: str  # Don't expose!
    created_at: datetime
    updated_at: datetime
    last_login: datetime

# API DTO (only expose necessary)
class UserDTO:
    id: int
    email: str
    name: str

# API endpoint
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    # Convert to DTO
    dto = UserDTO(
        id=user.id,
        email=user.email,
        name=user.name
    )

    return dto  # Only return DTO, not User object
```

**Benefits:**
- ✅ Security (don't expose internal fields)
- ✅ Flexibility (database schema ≠ API contract)
- ✅ Clarity (API shows exactly what's available)

---

## API Design Patterns

### Pattern: Pagination

**Problem:** Endpoint returns 100,000 records. Client's browser crashes.

**Solution:** Return records in pages. Client requests page by page.

**Implementation:**
```
GET /users?page=1&per_page=20

Response:
{
  "data": [{user1}, {user2}, ...],
  "page": 1,
  "per_page": 20,
  "total": 523,
  "pages": 27
}

Next page: GET /users?page=2&per_page=20
```

**Cursor-based (better for large datasets):**
```
GET /users?limit=20

First request:
{
  "data": [{user1}, {user2}, ...],
  "next_cursor": "abc123xyz"
}

Next request: GET /users?cursor=abc123xyz&limit=20
{
  "data": [{next set of users}],
  "next_cursor": "def456uvw"
}
```

---

### Pattern: API Versioning

**Problem:** Need to change API (remove field, rename endpoint). Don't want to break clients.

**Solution:** Version API. Old and new versions coexist.

**Approaches:**

**1. URL Versioning (Simple)**
```
GET /v1/users/123  → Old format
GET /v2/users/123  → New format
```

**2. Header Versioning (Clean)**
```
GET /users/123
Header: API-Version: 2
```

**3. Deprecation Period**
```
v1 available (old clients use this)
v2 available (new clients use this, better)
After 6 months: Remove v1 (clients must upgrade)
```

**When to version:**
- Removing fields
- Changing response format
- Renaming endpoints
- Changing behavior

**When NOT to version:**
- Adding optional field
- Adding new endpoint
- Internal changes (clients don't see)

---

## Integration Patterns

### Pattern: Strangler Fig Pattern

**Problem:** Have old system, want to replace with new one. Can't rewrite everything at once.

**Solution:** New system gradually takes over. Old and new run together.

**How it works:**
```
Phase 1: Build new system alongside old
  Requests → Old System (still handling everything)
            → New System (not used yet)

Phase 2: Migrate one thing at a time
  Requests → Router → New System (for payments)
                   → Old System (for everything else)

Phase 3: Keep migrating
  Requests → Router → New System (for payments, orders)
                   → Old System (for legacy parts)

Phase 4: Remove old system when everything migrated
  Requests → New System (complete replacement)
```

**Benefits:**
- ✅ No downtime (systems run in parallel)
- ✅ Gradual migration (low risk)
- ✅ Ability to rollback (old system still there)
- ✅ Real traffic testing (new system handles real requests)

---

## Antipatterns: When Patterns Fail

Patterns are powerful but can backfire. Learn from failures.

### SOA Gone Wrong: Too Many Services

**What happened:** Uber's early architecture (2009-2011)

```
Decision: "Decompose everything into services"
Result: 200+ services, too fine-grained

Problems:
- Service discovery nightmare (which service talks to which?)
- Testing hell (integration tests spanning 200 services)
- Deployment chaos (coordinating 200 deploys)
- Latency spikes (request spans 15 services)
- Ops complexity (200 services to monitor)

Lesson:
  Services should map to business domains, not functions
  Keep manageable: 3-10 services per team
  Not every function deserves its own service
```

### Event-Driven Gone Wrong: Ordering Problems

**What happened:** Payment system with async events

```
Expected:
  1. order.created
  2. payment.processed
  3. order.confirmed

What actually happened:
  1. payment.processed ← arrived first!
  2. order.created
  3. order.confirmed

Why:
  Different services publish events asynchronously
  Network jitter (payment response faster)
  Message broker delays

Problem:
  Processing payment for order that doesn't exist
  Orphaned payments (no matching order)
  Data inconsistency

Lesson:
  Design events to handle out-of-order arrival
  Use idempotent processing (same event twice = safe)
  Add timestamp/sequence numbers to events
```

### Circuit Breaker Gone Wrong: Cascading Failures

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

### Repository Pattern Gone Wrong: Over-Abstraction

**What happened:** Repository for every entity

```
Result: 50+ Repository classes, all similar
  class UserRepository { ... }
  class AddressRepository { ... }
  class PaymentRepository { ... }
  ... 47 more ...

Problems:
- Boilerplate explosion
- Hides details under abstraction
- Over-generalized
- Slow to change (modify 50 files)

Lesson:
  Use Repository for complex entities
  Simple queries? Direct database calls are fine
  Patterns are tools, not dogma
  Sometimes simple > abstract
```

---

## When to Apply Patterns

**Too many patterns:**
```
❌ Every new problem → find a pattern
❌ Using Strangler Fig, Event-Driven, Microservices, Circuit Breaker, etc.
❌ System is complex to understand
```

**Right amount of patterns:**
```
✅ Use patterns for recurring problems
✅ Only when simpler solution doesn't work
✅ Understand pattern before using it
✅ Document why pattern was chosen
```

**Pattern checklist:**
```
☐ Problem is common (not unique to this system)
☐ Pattern is proven (multiple successful implementations)
☐ Context fits (system matches pattern requirements)
☐ Trade-offs understood (know pros and cons)
☐ Simpler solution tried (patterns are last resort)
☐ Team understands (can maintain, debug, extend)
```

---

## Integration with Playbook

**Part of architecture & design:**
- `/pb-adr` — Document why patterns chosen
- `/pb-guide` — Design requirements
- `/pb-deployment` — How patterns affect deployment

**Related Commands:**
- `/pb-adr` — When to document pattern decisions
- `/pb-security` — Patterns for security
- `/pb-performance` — Patterns for performance
- `/pb-testing` — Testing patterns

---

*Created: 2026-01-11 | Category: Architecture | Tier: L*

