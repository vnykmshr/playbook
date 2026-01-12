# **Engineering SDLC Playbook**

A reusable end-to-end guide for any feature, enhancement, refactor, or bug fix.
Right-size your process using **Change Tiers**, then follow required sections.

**Mindset:** This framework assumes you're operating from `/pb-preamble`. Challenge the tiers, rearrange gates, adapt to your team—this is a starting point, not dogma.

---

## **Quick Reference: Change Tiers**

Determine tier FIRST, then follow only required sections.

| Tier | Examples | Required Sections | Approvals |
|------|----------|-------------------|-----------|
| **XS** | Typo fix, config tweak, dependency bump | 1.1, 5.2, 8.1, 10.2 | Self |
| **S** | Bug fix, small UI change, single-file refactor | 1, 3, 5, 6.1, 8, 10 | Peer review |
| **M** | New endpoint, feature enhancement, multi-file change | 1-6, 7.1, 8, 10, 11 | Tech lead |
| **L** | New service, architectural change, breaking changes | All sections | Tech lead + Product |

**Default to one tier higher if uncertain.**

---

## **Definition of Ready (Before Starting)**

Before starting implementation, confirm:

- [ ] Tier determined and documented
- [ ] Scope documented (in-scope / out-of-scope)
- [ ] Acceptance criteria defined and agreed
- [ ] Dependencies identified and unblocked
- [ ] Security implications assessed (see Appendix A)

---

## **Definition of Done (Before Release)**

Before marking complete:

- [ ] All acceptance criteria met
- [ ] Tests passing (per tier requirements)
- [ ] Security checklist completed (Appendix A)
- [ ] Documentation updated (if applicable)
- [ ] Monitoring/alerting configured (M/L tiers)
- [ ] PR approved and merged
- [ ] Deployed and smoke tested

---

## **Checkpoints & Gates**

| Gate | After Section | Who Signs Off | Tier |
|------|---------------|---------------|------|
| **Scope Lock** | §3 | Product + Engineering | M, L |
| **Design Approval** | §4 | Tech Lead | M, L |
| **Ready for QA** | §5 | Developer (self-review) | S, M, L |
| **Ready for Release** | §6 | QA + Product | M, L |
| **Post-Release OK** | §10.3 | On-call / Developer | M, L |

Do not proceed past a gate without sign-off.

---

## **0. Emergency Path (Hotfixes Only)**

For P0/P1 production incidents requiring immediate fixes:

**Process:**
1. Fix the immediate problem (minimal change)
2. Get expedited review (sync, not async)
3. Deploy with rollback ready
4. Backfill documentation within 24 hours
5. Schedule post-incident review

**Required:** §1.1 (brief), §5.2, §8.2 (rollback), §10.2, §10.3

**Skip:** §2 (most), §4 (most), §9

**Post-hotfix:** Create follow-up ticket to address root cause properly.

---

## **1. Intake & Clarification**

Before starting any work:

**1.1 Restate the request**

Document:
* What is asked
* Why it matters (business value)
* Expected outcome
* Success criteria (measurable)
* Assumptions requiring validation
* **Tier assignment** (XS/S/M/L)

**1.2 Clarification checklist**

Ask for details on:
* Missing acceptance criteria
* Ambiguities in requirements
* Conflicting requirements
* Third-party constraints
* Dependencies on other teams or systems

**If anything is unclear, stop and clarify.**

---

## **2. Stakeholder Involvement & Alignment**

*Required for: M, L tiers*

Every significant change needs validation from multiple angles.

**2.1 Product**
* Confirm user story
* Confirm acceptance criteria
* Define measurable success metrics
* Check interactions with existing features
* Confirm visual/UI/UX expectations (if applicable)

**2.2 Engineering (Backend, Frontend, Infra)**
* Impact on architecture
* Data flow changes
* Service boundary / API changes
* Storage requirements
* Observability needs
* Performance expectations

**2.3 Business & Operations**
* Risk assessment
* Compliance (PII, audit, GDPR if applicable)
* Revenue or cost implications
* Customer impact and rollout timing

**Output:** Single aligned understanding documented before proceeding.

---

## **3. Requirements & Scope Definition**

*Required for: S, M, L tiers*

Create a clear boundary so the team knows what to deliver.

**3.1 In-scope**
Everything this change must include.

**3.2 Out-of-scope**
Anything explicitly excluded to avoid scope creep.

**3.3 Edge cases**
List special scenarios: failures, retries, degraded modes, empty states.

**3.4 Dependencies**
* API or service dependencies
* Schema updates
* External systems
* Libraries/packages
* Feature flag or config dependencies

**CHECKPOINT: Scope Lock (M/L tiers) - Get sign-off before proceeding.**

---

## **4. Architecture & Design Preparation**

*Required for: M, L tiers*

Provide a solid technical foundation.

**4.1 High-level architecture**
Include:
* Diagrams (flow, sequence, state as needed)
* Inputs, outputs, transformations
* Error pathways
* Retry/timeout/circuit breaker behavior

**For async and event-driven systems, reference `/pb-patterns-async`, `/pb-patterns-distributed`:**

**Async Patterns (Callbacks, Promises, Async/Await, Job Queues):**

When handling non-blocking operations, choose the appropriate async pattern:

```python
# Python: Async/await for cleaner code
import asyncio
import aiohttp

async def fetch_user_and_posts(user_id):
    """Fetch user data and posts concurrently."""
    async with aiohttp.ClientSession() as session:
        # Fetch in parallel instead of sequentially
        user_task = fetch_from_api(session, f'/users/{user_id}')
        posts_task = fetch_from_api(session, f'/users/{user_id}/posts')

        user, posts = await asyncio.gather(user_task, posts_task)
        return {'user': user, 'posts': posts}

async def fetch_from_api(session, endpoint):
    """Fetch from API with timeout and error handling."""
    try:
        async with session.get(endpoint, timeout=5) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise ValueError(f"API returned {resp.status}")
    except asyncio.TimeoutError:
        # Log, notify, or retry with backoff
        logger.error(f"Request to {endpoint} timed out")
        raise
```

```javascript
// JavaScript: Promise with proper error handling
function fetchUserAndPosts(userId) {
  // Fetch in parallel instead of sequentially
  return Promise.all([
    fetch(`/api/users/${userId}`).then(r => r.json()),
    fetch(`/api/users/${userId}/posts`).then(r => r.json())
  ])
  .then(([user, posts]) => {
    return { user, posts };
  })
  .catch(error => {
    logger.error('Failed to fetch user data:', error);
    // Decide: retry, fallback, or propagate error
    throw error;
  });
}

// Or with async/await (preferred)
async function fetchUserAndPosts(userId) {
  try {
    const [user, posts] = await Promise.all([
      fetch(`/api/users/${userId}`).then(r => r.json()),
      fetch(`/api/users/${userId}/posts`).then(r => r.json())
    ]);
    return { user, posts };
  } catch (error) {
    logger.error('Failed to fetch user data:', error);
    throw error;
  }
}
```

```go
// Go: Goroutines and channels for concurrent operations
func fetchUserAndPosts(ctx context.Context, userID int) (User, []Post, error) {
    // Use channels to coordinate goroutines
    userChan := make(chan User)
    postsChan := make(chan []Post)
    errChan := make(chan error)

    // Fetch user concurrently
    go func() {
        user, err := fetchUser(ctx, userID)
        if err != nil {
            errChan <- err
            return
        }
        userChan <- user
    }()

    // Fetch posts concurrently
    go func() {
        posts, err := fetchPosts(ctx, userID)
        if err != nil {
            errChan <- err
            return
        }
        postsChan <- posts
    }()

    // Wait for both with timeout context
    var user User
    var posts []Post

    for i := 0; i < 2; i++ {
        select {
        case u := <-userChan:
            user = u
        case p := <-postsChan:
            posts = p
        case err := <-errChan:
            return User{}, nil, fmt.Errorf("fetch failed: %w", err)
        case <-ctx.Done():
            return User{}, nil, fmt.Errorf("request cancelled or timed out")
        }
    }

    return user, posts, nil
}
```

**Job Queues for background processing:**

```python
# Python: Using task queue (Celery) for long-running operations
from celery import shared_task
from time import sleep

@shared_task(max_retries=3)
def send_email_notification(user_id, email_type):
    """Send email asynchronously with automatic retries."""
    try:
        user = User.query.get(user_id)
        email_service.send(user.email, email_type)
        logger.info(f"Email sent to user {user_id}")
    except Exception as exc:
        # Retry with exponential backoff
        logger.error(f"Email send failed: {exc}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

# Queue task from request handler (non-blocking)
def handle_user_signup(request):
    user = create_user(request.data)
    # Queue email asynchronously - request returns immediately
    send_email_notification.delay(user.id, 'welcome')
    return {'user_id': user.id}
```

```javascript
// JavaScript: Using job queue (Bull for Redis) for background work
const emailQueue = new Queue('emails', {
  redis: { host: 'localhost', port: 6379 }
});

// Process jobs from the queue
emailQueue.process(5, async (job) => {
  // Job contains: { userId, emailType }
  const user = await User.findById(job.data.userId);
  await emailService.send(user.email, job.data.emailType);
  return { sent: true };
});

// Handle failed jobs with retries
emailQueue.on('failed', (job, err) => {
  logger.error(`Job ${job.id} failed:`, err);
  // Bull automatically retries with exponential backoff
});

// Queue job from request handler (non-blocking)
app.post('/signup', async (req, res) => {
  const user = await createUser(req.body);
  // Add job to queue - returns immediately
  await emailQueue.add(
    { userId: user.id, emailType: 'welcome' },
    { attempts: 3, backoff: { type: 'exponential', delay: 2000 } }
  );
  res.json({ user_id: user.id });
});
```

```go
// Go: Using worker pool pattern with channels
type JobQueue struct {
    jobs    chan Job
    workers int
}

type Job struct {
    UserID    int
    EmailType string
}

func (q *JobQueue) Start(ctx context.Context) {
    for i := 0; i < q.workers; i++ {
        go q.worker(ctx)
    }
}

func (q *JobQueue) worker(ctx context.Context) {
    for {
        select {
        case job := <-q.jobs:
            if err := sendEmailJob(ctx, job); err != nil {
                logger.Errorf("Job failed for user %d: %v", job.UserID, err)
                // Requeue or log failure for monitoring
            }
        case <-ctx.Done():
            return
        }
    }
}

// Queue job from request (non-blocking)
func handleSignup(w http.ResponseWriter, r *http.Request) {
    user := createUser(r)
    // Send job to queue channel (doesn't block)
    jobQueue.jobs <- Job{UserID: user.ID, EmailType: "welcome"}
    json.NewEncoder(w).Encode(user)
}
```

**Distributed Systems & Event-Driven Patterns:**

For systems spanning multiple services, use Saga patterns for multi-step transactions. See `/pb-patterns-distributed` for detailed guidance.

```python
# Python: Saga pattern for multi-service transactions
class OrderSaga:
    """Orchestrates multi-step order fulfillment across services."""

    def __init__(self, event_bus, order_service, payment_service, inventory_service):
        self.event_bus = event_bus
        self.order_service = order_service
        self.payment_service = payment_service
        self.inventory_service = inventory_service

    def execute(self, order):
        """Execute order saga with compensating transactions."""
        saga_state = {'order_id': order.id, 'steps_completed': []}

        try:
            # Step 1: Create order
            self.order_service.create(order)
            saga_state['steps_completed'].append('order_created')

            # Step 2: Process payment
            payment = self.payment_service.charge(order.customer_id, order.total)
            saga_state['steps_completed'].append('payment_charged')

            # Step 3: Deduct inventory
            self.inventory_service.deduct(order.items)
            saga_state['steps_completed'].append('inventory_deducted')

            # Publish completion event
            self.event_bus.publish('order.completed', {
                'order_id': order.id,
                'customer_id': order.customer_id
            })

            return saga_state

        except Exception as error:
            # Compensate: undo steps in reverse order
            logger.error(f"Saga failed at step: {error}")

            if 'inventory_deducted' in saga_state['steps_completed']:
                self.inventory_service.restore(order.items)

            if 'payment_charged' in saga_state['steps_completed']:
                self.payment_service.refund(payment.id)

            # Publish failure event
            self.event_bus.publish('order.failed', {
                'order_id': order.id,
                'reason': str(error)
            })

            raise
```

```javascript
// JavaScript: Saga pattern with event orchestration
class OrderSaga {
  constructor(orderService, paymentService, inventoryService, eventBus) {
    this.orderService = orderService;
    this.paymentService = paymentService;
    this.inventoryService = inventoryService;
    this.eventBus = eventBus;
  }

  async execute(order) {
    const sagaState = {
      orderId: order.id,
      stepsCompleted: []
    };

    try {
      // Step 1: Create order
      await this.orderService.create(order);
      sagaState.stepsCompleted.push('order_created');

      // Step 2: Process payment
      const payment = await this.paymentService.charge(
        order.customerId,
        order.total
      );
      sagaState.stepsCompleted.push('payment_charged');

      // Step 3: Deduct inventory
      await this.inventoryService.deduct(order.items);
      sagaState.stepsCompleted.push('inventory_deducted');

      // Publish completion event
      this.eventBus.publish('order.completed', {
        orderId: order.id,
        customerId: order.customerId
      });

      return sagaState;
    } catch (error) {
      logger.error(`Saga failed: ${error.message}`);

      // Compensate: undo steps in reverse order
      if (sagaState.stepsCompleted.includes('inventory_deducted')) {
        await this.inventoryService.restore(order.items);
      }

      if (sagaState.stepsCompleted.includes('payment_charged')) {
        await this.paymentService.refund(payment.id);
      }

      // Publish failure event
      this.eventBus.publish('order.failed', {
        orderId: order.id,
        reason: error.message
      });

      throw error;
    }
  }
}
```

```go
// Go: Saga pattern with error recovery
type OrderSaga struct {
    orderService     OrderService
    paymentService   PaymentService
    inventoryService InventoryService
    eventBus         EventBus
}

func (s *OrderSaga) Execute(ctx context.Context, order *Order) error {
    steps := []string{} // Track completed steps for compensation

    // Step 1: Create order
    if err := s.orderService.Create(ctx, order); err != nil {
        s.eventBus.Publish("order.failed", map[string]interface{}{
            "orderId": order.ID,
            "reason":  err.Error(),
        })
        return fmt.Errorf("order creation failed: %w", err)
    }
    steps = append(steps, "order_created")

    // Step 2: Process payment
    payment, err := s.paymentService.Charge(ctx, order.CustomerID, order.Total)
    if err != nil {
        s.compensate(ctx, steps, order)
        s.eventBus.Publish("order.failed", map[string]interface{}{
            "orderId": order.ID,
            "reason":  err.Error(),
        })
        return fmt.Errorf("payment failed: %w", err)
    }
    steps = append(steps, "payment_charged")

    // Step 3: Deduct inventory
    if err := s.inventoryService.Deduct(ctx, order.Items); err != nil {
        s.compensate(ctx, steps, order)
        s.eventBus.Publish("order.failed", map[string]interface{}{
            "orderId": order.ID,
            "reason":  err.Error(),
        })
        return fmt.Errorf("inventory deduction failed: %w", err)
    }
    steps = append(steps, "inventory_deducted")

    // Publish completion event
    s.eventBus.Publish("order.completed", map[string]interface{}{
        "orderId":    order.ID,
        "customerId": order.CustomerID,
    })

    return nil
}

func (s *OrderSaga) compensate(ctx context.Context, steps []string, order *Order) {
    // Undo steps in reverse order
    for i := len(steps) - 1; i >= 0; i-- {
        switch steps[i] {
        case "inventory_deducted":
            if err := s.inventoryService.Restore(ctx, order.Items); err != nil {
                logger.Errorf("Failed to restore inventory: %v", err)
            }
        case "payment_charged":
            if err := s.paymentService.Refund(ctx, order.PaymentID); err != nil {
                logger.Errorf("Failed to refund payment: %v", err)
            }
        }
    }
}
```

**Event-Driven Architecture:**

Use event-driven patterns when services need loose coupling. Publish domain events and let interested services react.

```python
# Python: Event-driven service communication
class UserService:
    def __init__(self, event_bus, db):
        self.event_bus = event_bus
        self.db = db

    def create_user(self, user_data):
        """Create user and publish event for other services."""
        user = self.db.create_user(user_data)

        # Publish event - other services listen and react independently
        self.event_bus.publish('user.created', {
            'user_id': user.id,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        })

        return user

# Other services can subscribe to events without coupling
class NotificationService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        # Listen for user creation events
        self.event_bus.subscribe('user.created', self.send_welcome_email)

    def send_welcome_email(self, event):
        """React to user.created event."""
        user_id = event['user_id']
        email = event['email']
        # Send welcome email asynchronously
        send_email_task.delay(email, 'Welcome to our service!')
```

```go
// Go: Event-driven service communication with channels
type Event struct {
    Type    string
    Payload map[string]interface{}
}

type UserService struct {
    eventBus chan Event
    db       Database
}

func (s *UserService) CreateUser(ctx context.Context, userData map[string]interface{}) (*User, error) {
    user, err := s.db.CreateUser(ctx, userData)
    if err != nil {
        return nil, err
    }

    // Publish event - non-blocking (buffered channel)
    select {
    case s.eventBus <- Event{
        Type: "user.created",
        Payload: map[string]interface{}{
            "user_id":   user.ID,
            "email":     user.Email,
            "created_at": user.CreatedAt,
        },
    }:
    case <-ctx.Done():
        return user, fmt.Errorf("context cancelled while publishing event")
    }

    return user, nil
}

// Other services listen for events
type NotificationService struct {
    eventBus chan Event
}

func (s *NotificationService) Start(ctx context.Context) {
    for {
        select {
        case event := <-s.eventBus:
            if event.Type == "user.created" {
                s.handleUserCreated(event)
            }
        case <-ctx.Done():
            return
        }
    }
}

func (s *NotificationService) handleUserCreated(event Event) {
    email := event.Payload["email"].(string)
    // Send welcome email asynchronously
    go sendWelcomeEmail(email)
}
```

**4.2 Data Model Design**
* Schema updates
* Indexing strategy
* Backward compatibility
* Migration approach (online/offline, rollout steps)

**4.3 API/Interface Design**
* Request/response format
* Error codes and messages
* Pagination, filtering, sorting
* Idempotency requirements
* Compatibility with existing consumers

**4.4 Performance & Reliability**
* Expected load
* Stress points
* Concurrency handling
* Latency targets
* Resource usage (CPU, RAM, DB connections)

**4.5 Security Design**
Reference **Appendix A: Security Checklist** and document:
* How each applicable item is addressed
* Any security trade-offs or accepted risks

**CHECKPOINT: Design Approval (M/L tiers) - Get tech lead sign-off.**

---

## **5. Development Plan**

*Required for: S, M, L tiers*

Break work into implementable steps.

**5.1 Implementation roadmap**

For each component:
* Backend tasks
* Frontend tasks
* Infra tasks
* Data migration tasks
* Monitoring/logging tasks

**5.2 Coding practices**

Follow standards:
* Clean, readable structure
* Type safety
* Error handling with context
* Proper logging (no sensitive data)
* Retry & timeout patterns
* Minimize duplication
* Graceful degradation paths

**5.3 Developer checklist**

Before marking code complete:
- [ ] Handle success path
- [ ] Handle failure paths
- [ ] Handle malformed/unexpected inputs
- [ ] Handle concurrency and race conditions
- [ ] Add cleanup logic where needed
- [ ] Add idempotency where needed
- [ ] Confirm testability

**5.4 Iteration protocol**

During implementation, if scope or design changes are needed:
* **Minor adjustment:** Document in PR description, proceed
* **Significant change:** Return to §3 or §4, get re-approval before continuing

Don't silently expand scope.

**CHECKPOINT: Ready for QA - Self-review complete.**

---

## **6. Testing & Quality Assurance**

*Required for: S, M, L tiers (scope varies by tier)*

**6.1 Test Philosophy: Quality Over Quantity**

Tests should catch bugs, not just increase coverage numbers.

**DO Test:**
- Error handling and edge cases
- State transitions and side effects
- Business logic and calculations
- Integration points (API calls, storage)
- Security-sensitive paths (auth, validation)

**DON'T Test:**
- Static data structures (config, constants)
- Implementation details / internal functions
- Every permutation of valid inputs
- UI rendering details (prefer visual regression or E2E)
- Trivial getters/setters

**Anti-patterns to avoid:**
- Re-implementing internal functions in test files to test them
- Testing that data exists (instead of testing behavior)
- Over-parameterized tests for diminishing returns
- Slow integration tests that should be unit tests

**6.2 Test requirements by tier**

| Tier | Required Tests |
|------|----------------|
| **XS** | Existing tests pass |
| **S** | Unit tests for changed code + manual verification |
| **M** | Unit + Integration + QA scenarios |
| **L** | Unit + Integration + E2E + Load tests (if perf-critical) |

**6.2a Integration Testing Patterns**

Integration tests verify that multiple components work together correctly. They're essential for M/L tier work where components interact through databases, external APIs, queues, or caches.

**Definition & When to Use:**
- **Integration tests** test component interactions (e.g., API → Database, Service A → Service B, Frontend → Backend)
- Use when: Components depend on each other, external system calls occur, business logic spans multiple services
- Avoid overusing: If a unit test with mocks provides the same confidence, stick with unit tests (faster, more focused)

**Test Database Setup:**

For database-dependent integration tests, isolate each test:

```python
# Python pytest example
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

@pytest.fixture(scope="function")  # Fresh DB per test
def test_db():
    """Create isolated test database."""
    engine = create_engine("sqlite:///:memory:")  # Use in-memory for speed
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    session.close()

def test_user_creation_with_email_verification(test_db):
    """Integration: Create user, verify email sent, confirm verification."""
    user = User(email="test@example.com", name="Test User")
    test_db.add(user)
    test_db.commit()

    # Verify side effects: email sent, user marked unverified
    assert user.id is not None
    assert user.email_verified == False
    assert EmailQueue.count_pending(test_db) > 0
```

**Pattern: Test Data Factories:**

Instead of manually creating test data in each test, use factories:

```python
# Avoid: Manual test data in each test
def test_user_payment():
    user = User(email="test@example.com", name="Test", ...)
    db.add(user)
    db.commit()
    # ... many lines duplicated across tests

# Prefer: Reusable factory
from factory.alchemy import SQLAlchemyModelFactory

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_db

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = "Test User"
    email_verified = False

def test_user_payment():
    user = UserFactory(email_verified=True)  # Override as needed
    # Simpler, more readable
```

**Mocking External Services:**

Integration tests use real databases but mock external APIs (to avoid dependencies, speed, cost):

```python
import requests
from unittest.mock import patch, MagicMock

@patch('requests.post')  # Mock the HTTP call
def test_payment_webhook_processing(mock_post):
    """Integration: Process payment event from external provider."""
    # Setup: Mock returns success
    mock_post.return_value = MagicMock(status_code=200, json={
        "transaction_id": "tx_123",
        "status": "completed",
        "amount": 9999
    })

    # Execute: Call our webhook handler
    response = webhook_handler({"transaction_id": "tx_123"})

    # Verify: DB was updated, user notified
    assert response.status_code == 200
    assert Payment.query.filter_by(tx_id="tx_123").count() > 0
    assert mock_post.called  # Verify we called the external service
```

**JavaScript/TypeScript Integration Tests:**

For Node.js/TypeScript projects, use Jest with a real test database:

```typescript
// Integration test with real database
import { Database } from './db';
import { UserService } from './services/user';
import { EmailService } from './services/email';

describe('User signup integration', () => {
  let db: Database;
  let userService: UserService;

  beforeEach(async () => {
    // Fresh database for each test
    db = new Database(':memory:'); // Use SQLite in-memory
    await db.connect();
    userService = new UserService(db);
  });

  afterEach(async () => {
    await db.close();
  });

  it('should create user and queue email verification', async () => {
    // Setup: Mock external email service
    const emailServiceMock = jest.fn().mockResolvedValue({ sent: true });
    userService.emailService = { send: emailServiceMock };

    // Execute
    const user = await userService.signup({
      email: 'test@example.com',
      password: 'test_password_12345'  // Test data, not real password
    });

    // Verify: User created in DB
    expect(user.id).toBeDefined();
    expect(user.emailVerified).toBe(false);

    // Verify: Email sent (mocked)
    expect(emailServiceMock).toHaveBeenCalledWith(
      expect.objectContaining({ to: 'test@example.com' })
    );

    // Verify: Verification token created
    const token = await db.query(
      'SELECT * FROM email_verification_tokens WHERE user_id = ?',
      [user.id]
    );
    expect(token).toBeDefined();
  });
});
```

**Test Database Setup (TypeScript/TypeORM example):**

```typescript
// test/database-fixture.ts
import { createConnection, Connection } from 'typeorm';

export async function setupTestDatabase(): Promise<Connection> {
  return createConnection({
    type: 'sqlite',
    database: ':memory:',
    entities: [User, Payment, EmailQueue],
    synchronize: true, // Create schema from entities
    logging: false
  });
}

// In test
beforeEach(async () => {
  db = await setupTestDatabase();
});

afterEach(async () => {
  await db.dropDatabase();
  await db.close();
});
```

**Running Integration Tests in CI/CD:**

Integration tests are slower than unit tests. Manage them carefully:

```bash
# Separate test runs by speed
make test-unit       # Fast unit tests (30s)
make test-int        # Slower integration tests (5min)
make test-all        # Both (5.5min, full suite)

# In CI/CD:
# - Run unit tests on every commit (fail fast)
# - Run integration tests on PR/merge (comprehensive)
# - Run load/E2E tests pre-release only (very slow)
```

CI/CD configuration example (GitHub Actions):

```yaml
# For PR: Quick feedback (unit tests only)
- name: Run unit tests
  run: make test-unit

# For merge to main: Full integration
- name: Run integration tests
  run: make test-int
  timeout-minutes: 15

# For release: Everything
- name: Run load tests
  run: make test-load
  if: github.event_name == 'release'
```

**Containerized Test Databases (Docker):**

For teams using Docker, run databases in containers during testing:

Docker Compose for test environment:

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_INITDB_ARGS: "-U postgres"  # Default user
      POSTGRES_DB: test_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Using Docker Compose in tests:

```bash
# Start test containers
docker-compose -f docker-compose.test.yml up -d

# Run tests (containers are ready via healthchecks)
npm test

# Clean up
docker-compose -f docker-compose.test.yml down -v
```

In CI/CD (GitHub Actions):

```yaml
services:
  postgres:
    image: postgres:14-alpine
    env:
      POSTGRES_HOST_AUTH_METHOD: trust  # Allow connections without password
      POSTGRES_DB: test_db
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432

  redis:
    image: redis:7-alpine
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 6379:6379

steps:
  - name: Run integration tests
    run: npm test
    env:
      DATABASE_URL: postgres://postgres@localhost:5432/test_db
      REDIS_URL: redis://localhost:6379
```

**Alternative: Testcontainers (Automatic Container Management):**

Libraries like Testcontainers handle container lifecycle automatically:

```python
# Python example with testcontainers
from testcontainers.postgres import PostgresContainer

def test_with_testcontainers():
    with PostgresContainer("postgres:14") as postgres:
        # Container automatically starts, creates, and cleans up
        db = psycopg2.connect(postgres.get_connection_url())

        # Run test
        cursor = db.cursor()
        cursor.execute("CREATE TABLE users (id SERIAL, name TEXT)")
        # ... test code ...

        # Container automatically cleaned up on exit
```

Benefits of containerized databases:
- Matches production environment exactly
- No version mismatches (SQLite vs PostgreSQL)
- Easy to test against multiple DB versions
- Works well with CI/CD services
- Scales to multi-container integration tests (microservices)

**Common Integration Test Pitfalls:**

| Problem | Solution |
|---------|----------|
| Tests interact (previous test data affects next) | Use `scope="function"` per-test isolation, clean up after each test |
| Tests are slow (whole test suite takes 30min) | Use in-memory DB, mock slow external services, parallelize tests |
| Tests are flaky (pass sometimes, fail sometimes) | Avoid timing assumptions, use explicit waits, avoid test interdependencies |
| Too many integration tests (100+) | Keep only critical paths; use unit tests for edge cases |

**6.3 Test types reference**

* **Unit tests** - Isolated function/method testing
* **Integration tests** - Component interaction testing
* **End-to-end tests** - Full user flow testing
* **API contract tests** - Request/response validation
* **Regression tests** - Ensure existing functionality unbroken
* **Negative tests** - Invalid inputs, error conditions
* **Load tests** - Performance under expected/peak load

**6.4 QA scenarios (M/L tiers)**

Document actual test cases covering:
* Happy path
* Alternate flows
* Error scenarios
* State transitions
* Data consistency checks
* Frontend usability (if applicable)

**6.5 Test data**

Create controlled, realistic test datasets. Never use production PII.

**6.6 Test maintenance**

Periodically review test suite for:
* Low-value tests to prune (static data tests, over-parameterized tests)
* Slow tests to speed up (missing mocks, over-integrated)
* Flaky tests to fix or quarantine
* Coverage gaps in critical paths

**Target:** Fewer, faster, more meaningful tests.

**CHECKPOINT: Ready for Release (M/L tiers) - QA sign-off.**

---

## **7. Infra, Deployment & Security Readiness**

*Required for: M, L tiers (7.1 always; 7.2-7.3 for L)*

**7.1 Infrastructure changes**
* New services or containers
* New environment variables
* New storage (DB, cache, files)
* New queues/topics
* Additional monitoring or logs

**7.2 Security hardening**

Reference **Appendix A** and confirm:
* All applicable items addressed
* No new attack surfaces introduced
* Secrets properly managed

**7.3 Observability**
* New dashboards needed?
* Alert rules defined?
* Log retention configured?
* SLO metrics identified?

---

## **8. CI/CD Requirements**

*Required for: All tiers*

**8.1 CI (All tiers)**
* Linting passes
* Type checks pass
* Automated tests pass
* Build succeeds

**8.2 CD (S, M, L tiers)**
* Deployment sequencing defined
* Feature flag plan (if applicable)
* **Rollback plan documented**
* Health checks in place
* Canary/phased rollout (L tier)

---

## **9. Documentation**

*Required for: M, L tiers*

**9.1 Developer documentation**
* Architecture notes
* Code flow explanation
* Important decisions and trade-offs

**9.2 API docs (if API changed)**
* Updated schemas
* Example requests/responses
* Error structures
* Versioning notes

**9.3 Operational docs (L tier)**
* Runbooks for common issues
* Monitoring instructions
* Scaling guidelines

**9.4 User/business documentation (if user-facing)**
* Release notes
* Customer-facing updates

---

## **10. Release & Post-Deployment**

*Required for: All tiers (scope varies)*

**10.1 Pre-release checklist (M/L tiers)**
- [ ] All tests passed
- [ ] All approvals obtained
- [ ] Monitoring/alerting configured
- [ ] Feature flags tested (if used)
- [ ] Rollback validated

**10.2 Release execution (All tiers)**
* Deploy
* Validate live metrics (M/L)
* Validate logs
* Smoke test

**10.3 Post-release monitoring (M/L tiers)**

Observe for at least 1 hour (L tier: 24 hours):
* Error rates
* Latency
* Resource usage
* DB load
* Logs for anomalies
* SLO adherence

**10.4 Follow-up work**
* Bugs discovered
* Optimizations identified
* Out-of-scope items to backlog
* Tech debt created

**CHECKPOINT: Post-Release OK - Confirm stable before moving on.**

---

## **11. Deliverable Summary Template**

*Required for: M, L tiers*

Copy and fill for each significant change:

```markdown
## Deliverable Summary: [Feature/Change Name]

**Tier:** [XS/S/M/L]
**Date:** [YYYY-MM-DD]
**Author:** [Name]

### What & Why
[One paragraph: what was built and the business value]

### How It Works
[Brief technical explanation of the approach]

### Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [e.g., Auth method] | [e.g., JWT] | [Why this choice] |

### Files Changed
[List key files or link to PR]

### Config Changes
- Environment variables: [List]
- Feature flags: [List or N/A]

### Migration
- Required: [Yes/No]
- Rollback steps: [Description]

### Testing Evidence
- Unit tests: [X added/modified]
- Integration tests: [X scenarios]
- Manual QA: [Link to test results or N/A]

### Monitoring
- Dashboard: [Link or N/A]
- Alerts: [List or N/A]

### Known Limitations
[What doesn't work yet or known issues]

### Follow-up Items
[Backlog tickets created for future work]
```

---

## **Appendix A: Security Checklist**

**See `/pb-security` command** for comprehensive security guidance and checklists.

For quick reference during development:
- Use `/docs/checklists.md` Quick Security Checklist (5 min) for S tier work
- Use `/pb-security` Standard Checklist (20 min) for M tier features
- Use `/pb-security` Deep Dive (1+ hour) for L tier or security-critical work

This covers:
- Input validation, SQL injection, XSS prevention, secrets management
- Authentication, authorization, cryptography
- Error handling, logging, API security, and compliance frameworks (PCI-DSS, HIPAA, SOC2, GDPR)

---

## **Appendix B: Quick Checklist by Tier**

### XS Tier
- [ ] Change described (§1.1)
- [ ] Coding standards followed (§5.2)
- [ ] CI passes (§8.1)
- [ ] Deployed and verified (§10.2)

### S Tier
- [ ] Request restated (§1)
- [ ] Scope defined (§3)
- [ ] Implementation complete (§5)
- [ ] Unit tests added (§6.1)
- [ ] CI/CD passes (§8)
- [ ] Deployed and verified (§10)

### M Tier
- [ ] All S tier items
- [ ] Stakeholders aligned (§2)
- [ ] Design documented (§4)
- [ ] Integration tests added (§6.1)
- [ ] QA scenarios tested (§6.3)
- [ ] Infra changes documented (§7.1)
- [ ] Documentation updated (§9)
- [ ] Deliverable summary complete (§11)
- [ ] Post-release monitoring done (§10.3)

### L Tier
- [ ] All M tier items
- [ ] All checkpoints passed with sign-off
- [ ] Security checklist complete (Appendix A)
- [ ] Load testing done (if applicable)
- [ ] Operational docs created (§9.3)
- [ ] 24-hour post-release monitoring

---

## **Appendix C: Operational Practices**

### Deployment

- **Use standardized deploy command** (e.g., `make deploy`) - Single command that handles git push, server pull, secrets decryption, and container rebuild.
- **Root access** - Only use root/SSH when deploy command cannot perform a specific action (e.g., debugging container issues, manual restarts).
- **Verify after deploy** - Always check service health after deployment via dashboard or container status.

### Secrets Management

- **Use standardized secrets command** (e.g., `make secrets-add`) - Add production secrets to encrypted secrets file.
- **Keep secrets in sync** - Always maintain consistency across:
  - `.env` (local development)
  - `.env.example` (template with placeholder values)
  - Encrypted secrets file for production
- **Never commit plaintext secrets** - All production secrets must be encrypted.

### Git Commit Practices

- **Never use `git add .`** - Considered risky; can accidentally stage unintended files.
- **Make logical commits** - Add specific files that belong together logically.
- **Use descriptive commit messages** - Follow conventional commits format (feat, fix, chore, etc.).
- **Review staged changes** - Always run `git status` and `git diff --staged` before committing.

### Configuration & Templating

- **Provisioning files** - YAML/config provisioning files may not support environment variable interpolation. Use deploy-time substitution with `sed` for dynamic values.
- **Personal/sensitive info** - Never hardcode personal email addresses or identifiable info in repo files. Use environment variables with deploy-time substitution.

### Monitoring & Observability

- **Background workers** - Workers without HTTP endpoints cannot be scraped directly. Monitor via queue/job metrics from the message broker.
- **Prometheus targets** - Only add services that expose `/metrics` endpoints.
- **Dashboard panels** - Ensure metrics exist before adding panels; missing metrics show as "No data".

### Frontend Compatibility

- **Check browser support** - Newer language features may not work in older browsers.
- **Use polyfills or alternatives** - When using cutting-edge features, verify browser compatibility or use libraries with broader support.
- **Test in multiple browsers** - Especially for user-facing features.

### Accessibility (WCAG 2.1 AA)

- **Keyboard navigation** - All interactive elements must be keyboard accessible. Every `onClick` needs a keyboard equivalent (`onKeyDown` for Enter/Space).
- **Focus management** - Modals/drawers must trap focus and restore it on close.
- **ARIA labels** - Icon-only buttons require `aria-label`. Hide decorative icons with `aria-hidden="true"`.
- **Focus visibility** - Focus indicators must be visible in both light and dark modes.
- **Semantic HTML** - Use appropriate elements (`button` not `div` with onClick).
- **Touch targets** - Minimum 44x44px for mobile touch targets.

### Troubleshooting

- **Container crash loops** - Check container logs to identify startup failures.
- **Provisioning errors** - Often caused by invalid YAML syntax or missing required fields. Check for proper indentation and required settings.
- **Environment variable issues** - Shell sourcing may fail with special characters. Use `grep` + `cut` instead of `source` for robust extraction.

---

## Integration with Playbook Ecosystem

**This is the master SDLC framework.** All 45 other commands implement phases described in this guide.

**Key command integrations by phase:**

- **§1 Intake & Planning** → `/pb-plan`, `/pb-adr`, `/pb-patterns-core`
- **§2 Team & Estimation** → `/pb-team`, `/pb-onboarding`, `/pb-knowledge-transfer`
- **§3 Architecture & Design** → `/pb-patterns-core`, `/pb-patterns-async`, `/pb-patterns-db`, `/pb-patterns-distributed`
- **§4 Implementation** → `/pb-start`, `/pb-cycle`, `/pb-testing`, `/pb-commit`, `/pb-todo-implement`
- **§5 Code Review** → `/pb-review-code`, `/pb-security`, `/pb-logging`, `/pb-review-product`
- **§6 Quality Gates** → `/pb-review-tests`, `/pb-review-hygiene`, `/pb-review-microservice`
- **§7 Observability** → `/pb-observability`, `/pb-logging`, `/pb-performance`
- **§8 Deployment** → `/pb-deployment`, `/pb-release`, `/pb-review-prerelease`
- **§9 Post-Release** → `/pb-incident`, `/pb-observability` (monitoring)
- **Team & Growth** → `/pb-team`, `/pb-onboarding`, `/pb-documentation`

**See also:**
- `/docs/integration-guide.md` — Comprehensive guide showing all commands, workflows, and how they work together
- `/docs/command-index.md` — Quick reference by category
