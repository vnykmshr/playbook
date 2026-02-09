---
name: "pb-patterns-core"
title: "Core Architecture & Design Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-patterns-resilience', 'pb-patterns-async', 'pb-patterns-db', 'pb-patterns-distributed', 'pb-adr']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Core Architecture & Design Patterns

Proven solutions to recurring problems. Patterns speed up design and prevent mistakes.

---

## Purpose

Patterns:
- **Accelerate design**: Don't solve the same problem twice
- **Share knowledge**: Common vocabulary for discussion
- **Prevent mistakes**: Patterns have gotchas documented
- **Improve quality**: Use proven solutions, not experimental ones
- **Enable communication**: "Let's use the retry pattern" means something

**Mindset:** Every pattern has trade-offs. Use `/pb-preamble` thinking (challenge assumptions, surface costs) and `/pb-design-rules` thinking (does this pattern serve Clarity, Simplicity, Modularity?).

Challenge whether this pattern is the right fit for your constraints. Surface the actual costs. Understand the alternatives. A pattern is a starting point, not a law.

**Resource Hint:** sonnet — Pattern reference and application; implementation-level design decisions.

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
- Independent scaling (payment service under load? Scale just that)
- Independent deployment (order service update doesn't affect payments)
- Technology flexibility (use Node for one, Python for another)
- Clear boundaries (easy to understand what each does)

**Cons:**
- Operational complexity (many services to manage)
- Network latency (services talking over network)
- Data consistency harder (each has own database)
- Debugging harder (request spans multiple services)

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
  "total": 99.99,
  "version": 1
}
```

**Note:** Include `version` field for event versioning (critical for schema evolution)

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
- Loose coupling (services don't know about each other)
- Scalable (can add listeners without changing publisher)
- Resilient (if one service is slow, doesn't block others)
- Debuggable (event history is audit trail)

**Cons:**
- Harder to debug (request spans multiple services asynchronously)
- Eventual consistency (order created, payment might fail later)
- Operational complexity (need event broker)
- Ordering challenges (events might arrive out of order)

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

## Resilience Patterns

See `/pb-patterns-resilience` for Retry, Circuit Breaker, Rate Limiting, Cache-Aside, and Bulkhead patterns -- defensive patterns for making systems reliable under failure.

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
- Centralized data access (one place to change queries)
- Easy to test (mock repository for unit tests)
- Easy to swap databases (change repository, not whole app)
- Consistency (same query patterns everywhere)

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
- Security (don't expose internal fields)
- Flexibility (database schema ≠ API contract)
- Clarity (API shows exactly what's available)

---

## API Design Patterns

See `/pb-patterns-api` for API design patterns including Pagination, Versioning, REST, GraphQL, and gRPC.

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
- No downtime (systems run in parallel)
- Gradual migration (low risk)
- Ability to rollback (old system still there)
- Real traffic testing (new system handles real requests)

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

## Pattern Interactions: How Patterns Work Together

Real systems combine multiple patterns. Understanding how they interact prevents conflicts.

### Example: E-Commerce Order Processing

**Architectural Level:**
- **SOA**: Separate Order, Payment, Inventory services
- **Event-Driven**: Services communicate via events (not direct calls)

**Service Internal Level:**
- **Repository Pattern**: Data access layer in each service
- **Cache-Aside**: Redis cache in front of database
- **Connection Pooling**: Database connection reuse

**Communication Level:**
- **Retry with Backoff**: Retry failed calls to other services
- **Circuit Breaker**: Stop calling failed service for a time
- **Bulkhead**: Thread pool per service prevents resource starvation

**Data Level:**
- **DTO**: API returns only public fields
- **Pagination**: List endpoints return pages, not all records

**System Design:**
```
User Request
  ↓
API Gateway (Rate limiting, auth)
  ↓
[Order Service]
  • Repository for data access
  • Cache-Aside for product cache
  • Connection pool for DB
  ↓
[Event: order.created]
  ↓
Payment Service (Circuit Breaker)
  • Retry with backoff on failure
  • Bulkhead prevents thread exhaustion
  ↓
[Event: payment.processed] OR [Event: payment.failed]
  ↓
Inventory Service
  • Same pattern repetition
  ↓
[Event: order.completed]
  ↓
Notification Service
  • Job queue for emails (don't block response)
```

For resilience pattern interactions (Circuit Breaker + Retry, Cache-Aside + Bulkhead), see `/pb-patterns-resilience`.

### SOA + Event-Driven + Saga Pattern

**Real-World Scenario: Payment Processing**
```
Service A (Order Service):
  Receives order
  Publishes: "payment_required"
  State: AWAITING_PAYMENT

Service B (Payment Service):
  Listens: "payment_required"
  Attempts payment with Retry + Circuit Breaker
  If success: Publishes "payment_received"
  If failure after retries: Publishes "payment_failed"

Service A (compensation):
  Listens: "payment_failed"
  Performs compensating action: Cancel order

Service C (Inventory):
  Listens: "payment_received"
  Decrements stock with Repository pattern
  Publishes: "stock_decremented"
```

### DTO + Pagination + API Versioning

For Pagination and Versioning details, see `/pb-patterns-api`.

**Real-World API Response**
```
Old API (v1):
GET /users?page=1&per_page=20
{
  "users": [{id, email, password_hash, created_at, ...}],
  "page": 1,
  "per_page": 20,
  "total": 523
}

New API (v2, with DTO):
GET /v2/users?page=1&per_page=20
{
  "data": [{id, email, name}],  // DTO, no password_hash
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 523,
    "has_next": true
  }
}

Benefits:
- DTO: Security (password_hash not exposed)
- Pagination: Prevents huge responses
- Versioning: Can change API without breaking v1 clients
```

---

## When to Apply Patterns

**Too many patterns:**
```
[NO] Every new problem → find a pattern
[NO] Using Strangler Fig, Event-Driven, Microservices, Circuit Breaker, etc.
[NO] System is complex to understand
```

**Right amount of patterns:**
```
[YES] Use patterns for recurring problems
[YES] Only when simpler solution doesn't work
[YES] Understand pattern before using it
[YES] Document why pattern was chosen
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

**Pattern Family:**
This is the core patterns command. It covers foundational architectural, design, data access, and API patterns.

**Related Pattern Commands (Pattern Family):**
- `/pb-patterns-async` — Async patterns (callbacks, promises, async/await, reactive, workers, job queues)
- `/pb-patterns-db` — Database patterns (connection pooling, optimization, replication, sharding)
- `/pb-patterns-distributed` — Distributed patterns (saga, CQRS, eventual consistency, 2PC)

**How They Work Together:**
```
pb-patterns-core → Foundation (SOA, Event-Driven, Repository, DTO, Strangler Fig)
    ↓
pb-patterns-async → Async operations (implement Event-Driven, job queues)
    ↓
pb-patterns-db → Database implementation (pooling for performance)
    ↓
pb-patterns-distributed → Multi-service coordination (saga, CQRS)
```

**Architecture & Design Decision:**
- `/pb-adr` — Document why specific patterns chosen
- `/pb-guide` — System design and pattern selection
- `/pb-deployment` — How patterns affect deployment strategy

**Testing & Operations:**
- `/pb-security` — Security patterns and secure code
- `/pb-performance` — Performance optimization using patterns
- `/pb-testing` — Testing pattern implementations
- `/pb-incident` — Handling pattern failures

---

## Related Commands

- `/pb-patterns-resilience` — Resilience patterns (Retry, Circuit Breaker, Rate Limiting, Cache-Aside, Bulkhead)
- `/pb-patterns-async` — Async patterns for non-blocking operations
- `/pb-patterns-db` — Database patterns for data access
- `/pb-patterns-distributed` — Distributed patterns for multi-service coordination
- `/pb-adr` — Document pattern selection decisions

---

*Created: 2026-01-11 | Category: Architecture | Tier: L*

