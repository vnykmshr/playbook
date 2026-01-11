# Distributed Patterns

Patterns for coordinating operations across multiple services/databases.

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

**Event-Driven Architecture with gRPC:**

```go
// Go: Event-driven service communication with gRPC
package main

import (
    "context"
    "fmt"
    "log"
    "google.golang.org/grpc"
)

// User service publishes events
type UserService struct {
    eventPublisher EventPublisher
    userStore      Database
}

// Create user and publish event
func (s *UserService) CreateUser(ctx context.Context, user *User) (*User, error) {
    created, err := s.userStore.Create(ctx, user)
    if err != nil {
        return nil, err
    }

    // Publish event for other services to react
    if err := s.eventPublisher.Publish(ctx, &Event{
        Type:      "user.created",
        UserID:    created.ID,
        Email:     created.Email,
        Timestamp: time.Now(),
    }); err != nil {
        // Log but don't fail - event publishing is async
        log.Printf("Failed to publish event: %v", err)
    }

    return created, nil
}

// Notification service listens for events
type NotificationService struct {
    eventSubscriber EventSubscriber
}

// Start consuming events
func (s *NotificationService) Start(ctx context.Context) {
    events, errs := s.eventSubscriber.Subscribe(ctx, "user.created")

    go func() {
        for {
            select {
            case event := <-events:
                s.handleUserCreated(ctx, event)
            case err := <-errs:
                log.Printf("Event subscription error: %v", err)
            case <-ctx.Done():
                return
            }
        }
    }()
}

func (s *NotificationService) handleUserCreated(ctx context.Context, event *Event) {
    // Send welcome email
    if err := sendWelcomeEmail(ctx, event.Email); err != nil {
        log.Printf("Failed to send welcome email: %v", err)
    }
}

// gRPC server for inter-service communication
type OrderServiceServer struct{}

func (s *OrderServiceServer) CreateOrder(ctx context.Context, req *CreateOrderRequest) (*Order, error) {
    // Call payment service via gRPC
    // NOTE: Use proper TLS credentials in production (not shown for brevity)
    conn, err := grpc.Dial("payment-service:50051")
    if err != nil {
        return nil, fmt.Errorf("failed to connect to payment service: %w", err)
    }
    defer conn.Close()

    client := NewPaymentServiceClient(conn)
    payment, err := client.ChargePayment(ctx, &ChargeRequest{
        Amount: req.Total,
    })
    if err != nil {
        return nil, fmt.Errorf("payment failed: %w", err)
    }

    // Create order with payment ID
    return &Order{
        ID:        generateID(),
        Total:     req.Total,
        PaymentID: payment.ID,
    }, nil
}
```

**Eventual Consistency Handling:**

```go
// Go: Handling eventual consistency
package main

import (
    "context"
    "database/sql"
    "fmt"
    "time"
)

// User service writes to primary, reads from replicas (may be stale)
type UserStore struct {
    primary  *sql.DB
    replicas []*sql.DB
}

// Write to primary
func (s *UserStore) UpdateUserFollowCount(ctx context.Context, userID string, delta int) error {
    _, err := s.primary.ExecContext(ctx,
        "UPDATE users SET follower_count = follower_count + $1 WHERE id = $2",
        delta, userID,
    )
    return err
}

// Read from replica (may be behind)
func (s *UserStore) GetUserFollowCount(ctx context.Context, userID string) (int, error) {
    // Try replica first (may be stale)
    replica := s.replicas[0] // Round-robin in production
    var count int
    err := replica.QueryRowContext(ctx,
        "SELECT follower_count FROM users WHERE id = $1",
        userID,
    ).Scan(&count)

    if err == sql.ErrNoRows {
        // User not found on replica, try primary
        err = s.primary.QueryRowContext(ctx,
            "SELECT follower_count FROM users WHERE id = $1",
            userID,
        ).Scan(&count)
    }

    return count, err
}

// Read-after-write consistency: Check primary if stale data detected
func (s *UserStore) GetUserProfile(ctx context.Context, userID string) (*User, error) {
    // First read from replica (fast)
    replica := s.replicas[0]
    user := &User{}
    err := replica.QueryRowContext(ctx,
        "SELECT id, name, follower_count, updated_at FROM users WHERE id = $1",
        userID,
    ).Scan(&user.ID, &user.Name, &user.FollowerCount, &user.UpdatedAt)

    // If data is too old, read from primary to ensure consistency
    if err == nil && time.Since(user.UpdatedAt) > 10*time.Second {
        // Stale data, read from primary
        err = s.primary.QueryRowContext(ctx,
            "SELECT id, name, follower_count, updated_at FROM users WHERE id = $1",
            userID,
        ).Scan(&user.ID, &user.Name, &user.FollowerCount, &user.UpdatedAt)
    }

    return user, err
}

// Polling pattern: Client retries until data is consistent
func (s *UserStore) WaitForFollowCountUpdate(ctx context.Context, userID string, expectedCount int, timeout time.Duration) bool {
    deadline := time.Now().Add(timeout)

    for time.Now().Before(deadline) {
        count, err := s.GetUserFollowCount(ctx, userID)
        if err == nil && count == expectedCount {
            return true // Replica caught up
        }

        select {
        case <-time.After(100 * time.Millisecond):
            // Retry
        case <-ctx.Done():
            return false
        }
    }

    return false // Timeout
}
```

**CQRS with Event Sourcing:**

```go
// Go: CQRS - separate read and write models
package main

import (
    "context"
    "time"
)

// Write side: Append-only event log
type EventStore struct {
    db Database
}

func (es *EventStore) AppendEvent(ctx context.Context, event *Event) error {
    // Only write operations - no deletes, no updates
    return es.db.InsertEvent(ctx, event)
}

// Read side: Optimized for queries
type UserReadModel struct {
    db Database
}

func (rm *UserReadModel) GetUserProfile(ctx context.Context, userID string) (*UserProfile, error) {
    // Read from denormalized view (fast, optimized for reading)
    return rm.db.QueryUserProfile(ctx, userID)
}

// Event processor: Keep read model in sync
type EventProcessor struct {
    eventStore *EventStore
    readModel  *UserReadModel
}

func (ep *EventProcessor) Start(ctx context.Context) {
    // Listen for events
    events := ep.eventStore.StreamEvents(ctx)

    for event := range events {
        switch event.Type {
        case "user.created":
            // Update read model
            ep.readModel.db.InsertUserProfile(ctx, &UserProfile{
                UserID:    event.UserID,
                Email:     event.Email,
                CreatedAt: event.Timestamp,
            })

        case "user.follow":
            // Update follower count in read model
            ep.readModel.db.IncrementFollowerCount(ctx, event.TargetUserID)

        case "post.created":
            // Update post count in read model
            ep.readModel.db.IncrementPostCount(ctx, event.UserID)
        }
    }
}
```

---

## Integration with Playbook

**Related to distributed patterns:**
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

*Created: 2026-01-11 | Category: Distributed Systems | Tier: L*
*Updated: 2026-01-11 | Added Go examples*

