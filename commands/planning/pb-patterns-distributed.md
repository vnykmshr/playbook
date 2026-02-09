---
name: "pb-patterns-distributed"
title: "Distributed Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-async', 'pb-observability']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Distributed Patterns

Patterns for coordinating operations across multiple services/databases.

**Caveat:** Distributed patterns add significant complexity. Use `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (especially Simplicity and Resilience—can you achieve your goals with simpler approaches?).

Question whether you truly need distributed systems. Challenge the assumption that you can't keep things simple. Understand the real constraints before choosing.

**Resource Hint:** sonnet — Distributed pattern reference; implementation-level coordination decisions.

---

## Purpose

Distributed patterns:
- **Maintain consistency** across services
- **Handle failures** gracefully (one service down doesn't cascade)
- **Manage complexity** of distributed systems
- **Enable scalability** without data consistency nightmare
- **Provide visibility** into system state

---

## When to Use Distributed Patterns

**Use when:**
- System spans multiple services/databases
- Operations must coordinate across boundaries
- Consistency matters but flexibility needed
- Need visibility into distributed transactions

**Don't use when:**
- Single database sufficient
- Operations are local
- Simple solutions available
- System complexity not justified

---

## Saga Pattern

**Problem:** Multi-step transaction spans multiple services. Standard ACID transaction won't work.

**Solution:** Choreograph steps, with compensating actions for rollback.

**How it works:**
```
Saga: Fulfilling an order across multiple services

Step 1: Order Service creates order
Step 2: Payment Service charges payment
Step 3: Inventory Service decrements stock
Step 4: Shipping Service creates shipment

Problem: What if Payment fails after Order created?
Solution: Compensating transactions (reverse steps)

Order created → Payment fails → Order compensating action (cancel order)
```

**Two Approaches:**

### 1. Choreography (Event-Based)

Services listen for events and trigger next step.

**Example: Order Fulfillment**
```
1. Order Service receives order → publishes "order.created"
2. Payment Service listens → charges payment → publishes "payment.processed" OR "payment.failed"
3. If "payment.processed":
     Inventory Service listens → decrements stock → publishes "stock.decremented"
4. If "payment.failed":
     Order Service listens → publishes "order.cancelled"
     (No need to decrement stock, order was never created)
```

**JavaScript Example:**
```javascript
// Order Service
eventBus.subscribe('order.requested', async (event) => {
  try {
    const order = await createOrder(event);
    await eventBus.publish('order.created', { orderId: order.id });
  } catch (error) {
    await eventBus.publish('order.failed', { error });
  }
});

// Payment Service
eventBus.subscribe('order.created', async (event) => {
  try {
    const payment = await chargePayment(event.customerId, event.amount);
    await eventBus.publish('payment.processed', {
      orderId: event.orderId,
      paymentId: payment.id
    });
  } catch (error) {
    // Compensating: notify order service to cancel
    await eventBus.publish('payment.failed', { orderId: event.orderId });
  }
});

// Inventory Service
eventBus.subscribe('payment.processed', async (event) => {
  try {
    await decrementStock(event.orderId);
    await eventBus.publish('stock.decremented', { orderId: event.orderId });
  } catch (error) {
    // If inventory unavailable, compensate: refund payment
    await eventBus.publish('stock.failed', { orderId: event.orderId });
    await refundPayment(event.paymentId);
  }
});
```

**Pros:**
- Loose coupling (services don't know about each other)
- Scalable (add new steps without changing others)
- Decentralized (no orchestrator)

**Cons:**
- Hard to track state (which step are we in?)
- Hard to debug (events scattered across services)
- Difficult to add timeouts/retries

### 2. Orchestration (Centralized)

One service orchestrates the saga steps.

**Example:**
```javascript
// Order Orchestrator Service
async function fulfillOrder(order) {
  const sagaState = {
    orderId: order.id,
    state: 'pending',
    completedSteps: [],
    failedAt: null
  };

  try {
    // Step 1: Create order
    sagaState.state = 'creating_order';
    const createdOrder = await orderService.create(order);
    sagaState.completedSteps.push('order_created');

    // Step 2: Charge payment
    sagaState.state = 'charging_payment';
    const payment = await paymentService.charge(order.customerId, order.amount);
    sagaState.completedSteps.push('payment_charged');

    // Step 3: Decrement inventory
    sagaState.state = 'decrementing_stock';
    await inventoryService.decrement(order.itemIds);
    sagaState.completedSteps.push('stock_decremented');

    // Step 4: Create shipment
    sagaState.state = 'creating_shipment';
    await shippingService.create(order.id, order.items);
    sagaState.completedSteps.push('shipment_created');

    sagaState.state = 'completed';
    return sagaState;

  } catch (error) {
    // Compensate: undo steps in reverse order
    sagaState.failedAt = sagaState.state;

    if (sagaState.completedSteps.includes('shipment_created')) {
      await shippingService.cancel(order.id);
    }

    if (sagaState.completedSteps.includes('stock_decremented')) {
      await inventoryService.increment(order.itemIds);
    }

    if (sagaState.completedSteps.includes('payment_charged')) {
      await paymentService.refund(payment.id);
    }

    if (sagaState.completedSteps.includes('order_created')) {
      await orderService.cancel(order.id);
    }

    throw new SagaFailedError(sagaState);
  }
}
```

**Pros:**
- Easy to track state (one place)
- Easy to debug (centralized logic)
- Easy to add timeouts/retries

**Cons:**
- Tight coupling (orchestrator knows all services)
- Single point of failure (orchestrator goes down)
- Orchestrator becomes bottleneck

**Gotchas:**
```
1. "Idempotency"
   Bad: If step retries, might charge payment twice
   Good: Make operations idempotent (same operation twice = safe)

2. "Timeout"
   Bad: Payment charged but timeout before marking complete
   Good: Set timeouts, have compensating action for timeout

3. "Cascading failures"
   Bad: One service down brings whole saga down
   Good: Timeouts and fallbacks
```

### Saga Idempotency Pattern

**Problem:** Saga step retries. Payment charged twice. Inventory decremented twice.

**Solution:** Ensure each step is idempotent. Running same operation twice = running it once.

**Approaches:**

**1. Request Deduplication (Recommended)**
```
Track request ID. If request ID seen before, return cached result.

Payment Service:
  Request: POST /charge with requestId=abc123
  Service stores: requestId → paymentId=pay_xyz

  Retry: POST /charge with requestId=abc123 (same ID)
  Service checks: I've seen abc123 before
  Returns cached: paymentId=pay_xyz (no new charge)
```

**2. Idempotent Operations**
```
Design operation to be idempotent:

  Bad (not idempotent):
    inventory.count = 100
    inventory.count -= 10  // Decremented to 90
    [retry happens]
    inventory.count -= 10  // Now 80 (wrong!)

  Good (idempotent):
    UPDATE inventory SET count = count - 10
    WHERE product_id = 123
    [retry happens]
    UPDATE inventory SET count = count - 10
    WHERE product_id = 123
    (Both decrements happen, but only once because of logic)
```

**JavaScript example with idempotency:**
```javascript
// Payment Service with idempotency
const paymentRegistry = new Map(); // requestId → result

async function chargePayment(customerId, amount, requestId) {
  // Check if already processed
  if (paymentRegistry.has(requestId)) {
    console.log("Idempotent: Returning cached payment");
    return paymentRegistry.get(requestId);
  }

  try {
    // Process payment
    const payment = await paymentGateway.charge(customerId, amount);

    // Cache result before returning
    paymentRegistry.set(requestId, payment);
    return payment;
  } catch (error) {
    // Don't cache failures - allow retry
    throw error;
  }
}

// Saga orchestrator
async function fulfillOrder(order) {
  const sagaId = order.id;
  const requestIds = {
    payment: `${sagaId}-payment-${order.customerId}`,
    inventory: `${sagaId}-inventory`,
    shipping: `${sagaId}-shipping`
  };

  try {
    // Payment (retry safe - idempotent)
    const payment = await chargePayment(
      order.customerId,
      order.total,
      requestIds.payment  // Same ID for retries
    );

    // Inventory (retry safe)
    await inventoryService.decrement(
      order.items,
      requestIds.inventory
    );

    // Shipping (retry safe)
    await shippingService.create(
      order.id,
      order.items,
      requestIds.shipping
    );

    return { success: true };
  } catch (error) {
    // Compensation on failure
    await compensate(sagaId);
    throw error;
  }
}
```

**When to implement:**
- All saga steps (payment, inventory, shipping)
- Any operation that might retry
- Multi-step workflows

---

## Event Versioning

**Problem:** Event format changes. Old events become unreadable. New services can't handle old events.

**Solution:** Version events. Support multiple versions simultaneously.

**Strategies:**

**1. Version Field (Simplest)**
```json
{
  "version": 2,
  "type": "order.created",
  "order_id": "order_123",
  "customer_id": "cust_456",
  "amount": 99.99,
  "currency": "USD"
}

vs.

Version 1 (old):
{
  "type": "order.created",
  "order_id": "order_123",
  "amount": 99.99
}
```

**2. Schema Evolution Map**
```
v1 → v2: Add currency field (default: USD)
v2 → v3: Split amount into amount + tax
v3 → v4: Add shipping_address field
```

**JavaScript example:**
```javascript
class EventVersionHandler {
  constructor() {
    this.handlers = {
      1: this.handleV1,
      2: this.handleV2,
      3: this.handleV3
    };
  }

  // v1: Basic order data
  handleV1(event) {
    return {
      orderId: event.order_id,
      customerId: event.customer_id,
      amount: event.amount,
      currency: 'USD' // Default
    };
  }

  // v2: Added currency field explicitly
  handleV2(event) {
    return {
      orderId: event.order_id,
      customerId: event.customer_id,
      amount: event.amount,
      currency: event.currency || 'USD'
    };
  }

  // v3: Split amount and tax
  handleV3(event) {
    return {
      orderId: event.order_id,
      customerId: event.customer_id,
      amount: event.amount,
      tax: event.tax || 0,
      currency: event.currency || 'USD'
    };
  }

  process(event) {
    const version = event.version || 1; // Default to v1
    const handler = this.handlers[version];

    if (!handler) {
      throw new Error(`Unknown event version: ${version}`);
    }

    return handler.call(this, event);
  }
}

// Usage
const eventHandler = new EventVersionHandler();

// Old v1 event
const oldEvent = {
  type: 'order.created',
  order_id: 'order_123',
  customer_id: 'cust_456',
  amount: 99.99
};

const normalized = eventHandler.process(oldEvent);
console.log(normalized);
// { orderId: 'order_123', customerId: 'cust_456', amount: 99.99, currency: 'USD' }

// New v3 event
const newEvent = {
  version: 3,
  type: 'order.created',
  order_id: 'order_123',
  customer_id: 'cust_456',
  amount: 95.00,
  tax: 4.99,
  currency: 'USD'
};

const normalized2 = eventHandler.process(newEvent);
console.log(normalized2);
// { orderId: 'order_123', customerId: 'cust_456', amount: 95.00, tax: 4.99, currency: 'USD' }
```

**Python example - Upcasting old events:**
```python
class EventUpgrader:
    """Convert old event versions to new format."""

    @staticmethod
    def upgrade_to_latest(event):
        """Upgrade event to latest version."""
        version = event.get('version', 1)

        # Chain upgrades
        if version == 1:
            event = EventUpgrader._upgrade_v1_to_v2(event)
        if version == 2:
            event = EventUpgrader._upgrade_v2_to_v3(event)

        return event

    @staticmethod
    def _upgrade_v1_to_v2(event):
        """v1 → v2: Add currency field."""
        event['currency'] = event.get('currency', 'USD')
        event['version'] = 2
        return event

    @staticmethod
    def _upgrade_v2_to_v3(event):
        """v2 → v3: Split amount and tax."""
        if 'tax' not in event:
            event['tax'] = 0
        event['version'] = 3
        return event

# Usage
old_event_v1 = {
    'type': 'order.created',
    'order_id': 'order_123',
    'amount': 99.99
}

upgraded = EventUpgrader.upgrade_to_latest(old_event_v1)
print(upgraded)
# {'type': 'order.created', 'order_id': 'order_123', 'amount': 99.99, 'currency': 'USD', 'tax': 0, 'version': 3}
```

**Migration strategy:**
```
Phase 1: Add version field to events
  Existing events: version = 1
  New events: version = 2

Phase 2: Support both versions in consumers
  Consumers handle v1 and v2

Phase 3: Migrate old events
  Background job upgrades v1 → v2

Phase 4: Remove v1 support
  Only v2+ consumers exist
```

---

## Outbox Pattern

**Problem:** Publishing event fails after database commit. Event lost. Inconsistency.

**Scenario:**
```
Transaction 1: Update order status + publish "order.shipped" event
  1. UPDATE orders SET status='shipped'
  2. Publish event to message broker
  3. If 2 fails: Event never published, but order already updated

Result: Order shipped but nobody notified → inconsistency
```

**Solution:** Write event to database first, then publish from database.

**How it works:**
```
Transaction 1: Write to outbox
  1. BEGIN TRANSACTION
  2. UPDATE orders SET status='shipped'
  3. INSERT INTO outbox (event_type, payload) VALUES (...)
  4. COMMIT (atomic)

Background process:
  1. SELECT * FROM outbox WHERE published=false
  2. FOR EACH event: Publish to message broker
  3. UPDATE outbox SET published=true
```

**PostgreSQL example:**
```python
import json
import time
from datetime import datetime

class OrderService:
    def __init__(self, db, event_publisher):
        self.db = db
        self.event_publisher = event_publisher

    def ship_order(self, order_id):
        """Ship order and publish event atomically."""
        with self.db.transaction():
            # Update order status
            self.db.execute(
                "UPDATE orders SET status='shipped', updated_at=NOW() WHERE id=%s",
                order_id
            )

            # Write event to outbox (same transaction)
            self.db.execute(
                """INSERT INTO outbox (event_type, payload, created_at)
                   VALUES (%s, %s, NOW())""",
                'order.shipped',
                json.dumps({
                    'order_id': order_id,
                    'status': 'shipped',
                    'timestamp': datetime.now().isoformat()
                })
            )
            # Transaction commits atomically
            # If either fails, both rolled back

    def poll_and_publish(self):
        """Background process: Poll outbox, publish events."""
        while True:
            try:
                # Fetch unpublished events
                events = self.db.query(
                    "SELECT id, event_type, payload FROM outbox WHERE published=false LIMIT 100"
                )

                for event in events:
                    try:
                        # Publish to message broker
                        self.event_publisher.publish(
                            event['event_type'],
                            json.loads(event['payload'])
                        )

                        # Mark as published
                        self.db.execute(
                            "UPDATE outbox SET published=true, published_at=NOW() WHERE id=%s",
                            event['id']
                        )

                    except Exception as e:
                        # Log but continue (handle next event)
                        print(f"Failed to publish event {event['id']}: {e}")

                # Sleep before next poll
                time.sleep(1)

            except Exception as e:
                print(f"Outbox poll failed: {e}")
                time.sleep(5)

# Database schema
"""
CREATE TABLE outbox (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP
);

CREATE INDEX idx_outbox_unpublished ON outbox(published) WHERE published = false;
"""
```

**JavaScript/Node.js:** Same pattern - use `BEGIN`/`COMMIT` transaction with INSERT to outbox, then setInterval polling.

**Benefits:**
- Atomic writes and events
- No lost events
- Guaranteed eventual consistency
- Simple to implement

**Gotchas:**
```
1. "Polling lag"
   Bad: Polling every 10 seconds, events delayed
   Good: Poll every 1-5 seconds, or use change data capture

2. "Outbox grows unbounded"
   Bad: Published events never deleted
   Good: Archive/delete old published events after 1-2 weeks

3. "Duplicate publishing"
   Bad: Network hiccup, publish twice
   Good: Message broker deduplicates by requestId
```

---

## CQRS (Command Query Responsibility Segregation)

**Problem:** Same data model used for reads and writes. Causes complexity and inconsistency.

**Solution:** Separate models - one for writes, one for reads.

**How it works:**
```
Traditional (Same model):
  Write Request → Business Logic → Update Model → Read Model (same as write)
  Problem: Complex logic, slow reads, hard to optimize

CQRS (Separate models):
  Write Request → Business Logic → Write Model (optimized for writes)
                                 → Event Stream
                                 → Read Model (optimized for reads)

  Read Request → Read Model (optimized for reads)
  Benefit: Can optimize each independently
```

**Example: Event Sourcing + CQRS**

```javascript
// Command: Update user profile
async function updateUserProfile(userId, name, email) {
  // Write to write model: append event
  const event = {
    type: 'UserProfileUpdated',
    userId,
    name,
    email,
    timestamp: new Date()
  };

  // Store event in event store
  await eventStore.append(userId, event);

  // Event triggers read model update asynchronously
  return { success: true, eventId: event.id };
}

// Read: Get user profile
async function getUserProfile(userId) {
  // Read from read model (optimized, denormalized)
  return await readModel.getUser(userId);
}

// Eventual consistency: read model updates asynchronously
eventBus.subscribe('UserProfileUpdated', async (event) => {
  // Update read model
  await readModel.updateUser(event.userId, {
    name: event.name,
    email: event.email
  });
});
```

**Pros:**
- Optimize reads and writes separately
- Read model can be denormalized (fast reads)
- Event sourcing enables audit trail
- Scale reads and writes independently

**Cons:**
- Eventual consistency (read model behind write model)
- Complex to implement
- More storage (storing events + read model)
- Hard to delete data (audit trail preserved)

**Gotchas:**
```
1. "Eventual consistency"
   Bad: Write data, read immediately sees old data
   Good: Accept slight delay, or read from write model

2. "Event versioning"
   Bad: Change event format, old events can't be read
   Good: Version events, have migration logic

3. "Read model rebuild"
   Bad: Read model corrupted, no way to recover
   Good: Rebuild from event stream (events are source of truth)
```

---

## Eventual Consistency

**Problem:** Can't always have strong consistency across services. Too slow, too complex.

**Solution:** Accept eventual consistency. Data will be consistent eventually.

**How it works:**
```
Scenario: Update user profile

Strong consistency:
  1. Update primary database
  2. Wait for all replicas to update (slow!)
  3. Return to user

  Latency: 500ms+

Eventual consistency:
  1. Update primary database
  2. Return to user immediately
  3. Background process updates replicas/caches/read models

  Latency: <10ms
  Eventual: Replicas catch up within seconds
```

**Example: Updating user's follower count**

```javascript
// Strong consistency (slow):
async function followUser(currentUserId, targetUserId) {
  // Acquire lock on both users
  // Update follower count
  // Update following count
  // Wait for all replicas
  // Release locks
  // Return (500ms+ latency)
}

// Eventual consistency (fast):
async function followUser(currentUserId, targetUserId) {
  // Publish event immediately
  await eventBus.publish('user.followed', {
    follower: currentUserId,
    target: targetUserId
  });

  // Return immediately
  return { success: true };  // <10ms latency

  // Asynchronously update counts
  // (user sees count update within seconds)
}

// Background processor
eventBus.subscribe('user.followed', async (event) => {
  await Promise.all([
    // Increment target's follower count
    userService.incrementFollowerCount(event.target),
    // Increment follower's following count
    userService.incrementFollowingCount(event.follower),
    // Update caches/replicas
    // Update search index
  ]);
});
```

**Guarantees:**
- Fast writes (return immediately)
- Eventual reads (data consistent within seconds)
- Scalable (no locking)

**Trade-offs:**
- Users see temporary inconsistency
- Complex to reason about
- Requires compensating actions for errors

---

## Two-Phase Commit (2PC)

**Problem:** Transaction spans multiple databases. Need all-or-nothing.

**Solution:** Coordinator asks all parties to prepare, then commit/rollback.

**How it works:**
```
Phase 1: Prepare (can we commit?)
  Coordinator asks: "Can you commit this transaction?"
  Service A: "Yes, I've locked resources"
  Service B: "Yes, I've locked resources"
  Service C: "No, constraint violation"

Phase 2: Commit or Rollback
  Coordinator: "Service C said no, ROLLBACK"
  Service A: "Releasing locks"
  Service B: "Releasing locks"
  Service C: "Releasing locks"

Result: All-or-nothing, consistent across databases
```

**Example:**
```python
class DistributedTransaction:
    def __init__(self, services):
        self.services = services
        self.prepared = []

    async def execute(self, operations):
        try:
            # Phase 1: Prepare
            for service, operation in zip(self.services, operations):
                result = await service.prepare(operation)
                if not result['ready']:
                    raise Exception(f"{service} not ready")
                self.prepared.append(service)

            # Phase 2: Commit
            for service in self.prepared:
                await service.commit()

            return {'success': True}

        except Exception as e:
            # Rollback all
            for service in self.prepared:
                await service.rollback()

            return {'success': False, 'error': str(e)}

# Usage
txn = DistributedTransaction([service_a, service_b, service_c])
result = await txn.execute([
    operation_a,
    operation_b,
    operation_c
])
```

**Pros:**
- Strong consistency (all-or-nothing)
- ACID guarantees across services

**Cons:**
- Slow (two round-trips)
- Blocking (locks held during prepare phase)
- Coordinator failure means stuck transaction
- Poor availability (one service down fails whole transaction)

**Gotchas:**
```
1. "Heuristic completion"
   Problem: Coordinator crashes after services prepare but before commit
   Services locked, manual intervention needed

2. "Timeout"
   Bad: Service takes too long to prepare, whole transaction blocks
   Good: Timeouts, fallback to eventual consistency

3. "Deadlock"
   Bad: Multiple concurrent transactions, resources locked in different order
   Good: Consistent lock ordering, or use MVCC
```

**When to use:**
- Strong consistency critical (financial transactions)
- Prefer Saga for loosely coupled services

---

## Pattern Interactions

### How patterns work together:

**Saga + Event-Driven Architecture**
```
Order Fulfillment using Saga + Events:

1. Frontend → Order Service
2. Order Service publishes "order.created" event
3. Payment Service listens → processes payment
4. If payment succeeds → publishes "payment.processed"
5. Inventory Service listens → decrements stock
6. If stock available → publishes "stock.decremented"
7. If payment fails → publishes "payment.failed"
8. Order Service compensates (cancels order)

Result: Distributed transaction using events (loose coupling)
```

**CQRS + Saga**
```
User Profile Updates + Follower Count:

Write side (Command: Follow User):
1. Append event to event store
2. Publish "user.followed" event
3. Return immediately

Event processor (Saga orchestrator):
1. Listen for "user.followed"
2. Coordinate updates across services
3. Update follower/following counts
4. Update caches

Read side (Query: Get user profile):
1. Read from optimized read model
2. Shows follower count (eventually consistent)
```

**Circuit Breaker + Saga Retry**
```
Service calling another service in Saga:

try {
  const result = await circuitBreaker.call(
    () => paymentService.charge(amount)
  );
} catch (CircuitBreakerOpen) {
  // Service is down
  // Saga handler: mark saga as "retrying"
  // Retry with exponential backoff
  // Or compensate if max retries exceeded
}
```

---

## Antipatterns

**Using 2PC with loosely coupled services:**
```
[NO] Bad: Tight coupling, poor availability
Service A → Coordinator → Service B → Service C
(All must be up and responsive)

[YES] Good: Use Saga + events instead
Service A → Event → Service B
Event → Service C
(Services can be down independently)
```

**Ignoring eventual consistency window:**
```
[NO] Bad: Write data, immediate read assumes consistent
data = write(user, 'John')
user = read(user)  // Might be old data!

[YES] Good: Accept delay or read from write model
write(user, 'John')  // Async
return { success: true }  // Don't promise immediate visibility
// Client retries read in UI if needed
```

**Creating saga with too many steps:**
```
[NO] Bad: 20-step saga, hard to debug
Step 1 → Step 2 → ... → Step 20
(If step 15 fails, debugging nightmare)

[YES] Good: Break into smaller sagas
Saga 1: Order fulfillment (5 steps)
Saga 2: Inventory management (3 steps)
(Each saga can be tested independently)
```

---

## Go Examples

**Saga Pattern with Compensation:**

```go
// Go: Order saga with distributed transaction
package main

import (
    "context"
    "fmt"
    "log"
)

type OrderSaga struct {
    orderService     OrderService
    paymentService   PaymentService
    inventoryService InventoryService
}

type Order struct {
    ID         string
    CustomerID string
    Items      []Item
    Total      float64
}

// Execute saga with compensation on failure
func (s *OrderSaga) Execute(ctx context.Context, order *Order) error {
    completed := []string{} // Track completed steps for compensation

    // Step 1: Create order
    if err := s.orderService.CreateOrder(ctx, order); err != nil {
        return fmt.Errorf("order creation failed: %w", err)
    }
    completed = append(completed, "order_created")

    // Step 2: Process payment
    payment, err := s.paymentService.Charge(ctx, order.CustomerID, order.Total)
    if err != nil {
        s.compensate(ctx, completed, order, payment)
        return fmt.Errorf("payment failed: %w", err)
    }
    completed = append(completed, "payment_charged")

    // Step 3: Deduct inventory
    if err := s.inventoryService.DeductInventory(ctx, order.Items); err != nil {
        s.compensate(ctx, completed, order, payment)
        return fmt.Errorf("inventory deduction failed: %w", err)
    }
    completed = append(completed, "inventory_deducted")

    // Step 4: Update shipping
    if err := s.orderService.UpdateShippingStatus(ctx, order.ID, "confirmed"); err != nil {
        s.compensate(ctx, completed, order, payment)
        return fmt.Errorf("shipping update failed: %w", err)
    }

    log.Printf("Order %s completed successfully", order.ID)
    return nil
}

// Compensate: undo steps in reverse order
func (s *OrderSaga) compensate(ctx context.Context, completed []string, order *Order, payment *Payment) {
    // Undo steps in reverse order
    for i := len(completed) - 1; i >= 0; i-- {
        step := completed[i]

        switch step {
        case "inventory_deducted":
            if err := s.inventoryService.RestoreInventory(ctx, order.Items); err != nil {
                log.Printf("Failed to restore inventory: %v", err)
            }

        case "payment_charged":
            if err := s.paymentService.Refund(ctx, payment.ID); err != nil {
                log.Printf("Failed to refund payment: %v", err)
            }

        case "order_created":
            if err := s.orderService.CancelOrder(ctx, order.ID); err != nil {
                log.Printf("Failed to cancel order: %v", err)
            }
        }
    }

    log.Printf("Compensation completed for order %s", order.ID)
}
```

Other patterns (Event-Driven, Outbox, CQRS, Eventual Consistency) follow similar Go idioms—use channels for events, context for cancellation, and interfaces for testability.

---

## Integration with Playbook
- `/pb-patterns-core` — SOA and Event-Driven (foundation)
- `/pb-patterns-async` — Async operations (needed for Saga)
- `/pb-guide` — Distributed systems design
- `/pb-incident` — Handling distributed failures
- `/pb-observability` — Tracing sagas across services
- `/pb-deployment` — Coordinating deployments across services

**Decision points:**
- When to use Saga vs 2PC
- When to accept eventual consistency
- How to handle distributed failures
- How to monitor saga execution
- gRPC vs REST for inter-service communication

---

## Related Commands

- `/pb-patterns-core` — Foundation patterns (SOA, Event-Driven)
- `/pb-patterns-async` — Async patterns needed for distributed operations
- `/pb-observability` — Tracing and monitoring distributed systems

---

*Created: 2026-01-11 | Category: Distributed Systems | Tier: L*
*Updated: 2026-01-11 | Added Go examples*

