---
name: "pb-review-microservice"
title: "Microservice Architecture Review"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-resilience', 'pb-patterns-distributed', 'pb-observability', 'pb-incident']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Microservice Architecture Review

Framework for reviewing microservice design, implementation, and operations.

**Mindset:** Microservice reviews embody `/pb-preamble` thinking (question service boundaries) and `/pb-design-rules` thinking (especially Modularity and Separation: are services correctly decoupled?).

Question whether the service boundary is correct. Challenge the coupling assumptions. Surface design flaws before they become operational problems.

**Resource Hint:** opus — microservice review requires deep analysis of boundaries, coupling, data ownership, and operational concerns

---

## When to Use

- Evaluating a new service before it goes to production
- Periodic architecture review of existing microservices
- After splitting a monolith or extracting a new service
- When inter-service communication issues arise

---

## Purpose

Microservice reviews ensure:
- **Clear boundaries** - Service owns specific business domain
- **Loose coupling** - Services don't depend on each other's internals
- **Scalability** - Service can scale independently
- **Resilience** - Service failures don't cascade
- **Observability** - Can debug issues across services
- **Deployability** - Can deploy independently

---

## Review Checklist

### 1. Service Boundaries

**Question: Is this the right scope for a service?**

**Bad Service Boundaries:**
- Service per function (getUser, createUser, deleteUser = 3 services)
- Service per tier (frontend, backend, database services)
- Service per database table
- Shared database between services

**Good Service Boundaries:**
- Service per business domain (User Service, Order Service, Payment Service)
- Service owns its data (no shared database)
- Service encapsulates related functionality
- Service is independently deployable

**Checklist:**
```
☐ Service boundary aligns with business domain
☐ Service has clear responsibility
☐ Service owns its data (no shared database)
☐ Service can be deployed independently
☐ Service makes sense to teams (not fragmented across 10 teams)
☐ Not too big (>3 teams can't understand it)
☐ Not too small (<1 person can't maintain it)
```

**Example: Good vs Bad Boundaries**

**[NO] Bad:**
```
UserService:
  - User authentication
  - User profile
  - User permissions
  - User sessions
  - User roles

(Too big, mixing auth + profile + permissions)
```

**[YES] Good:**
```
Identity Service:
  - User authentication
  - User sessions
  - Token generation

User Service:
  - User profile
  - User data management

Authorization Service:
  - Permissions
  - Role-based access control

(Each service has focused responsibility)
```

---

### 2. API Contract & Versioning

**Question: Is the service API stable and well-defined?**

**API Checklist:**
```
☐ API endpoints documented with examples
☐ Request/response formats defined (JSON schema)
☐ Authentication mechanism documented
☐ Error responses documented (what can fail?)
☐ Rate limiting defined (requests/sec)
☐ Timeout values defined
☐ Retry policy defined
☐ API versioning strategy (v1, v2, etc.)
☐ Deprecation timeline documented
```

**Good API Design:**

```javascript
// Example: Well-documented API

/**
 * Get user by ID
 *
 * Endpoint: GET /api/v1/users/:id
 *
 * Response: 200 OK
 * {
 *   "id": "uuid",
 *   "email": "user@example.com",
 *   "name": "John Doe"
 * }
 *
 * Errors:
 * - 404 Not Found: User doesn't exist
 * - 401 Unauthorized: Missing auth token
 * - 403 Forbidden: No permission to view user
 *
 * Rate limit: 100 requests/min
 * Timeout: 5 seconds
 * Retry: Idempotent (safe to retry)
 */
async function getUser(userId) {
  if (!userId) throw new BadRequest("userId required");
  const user = await db.users.findById(userId);
  if (!user) throw new NotFound("User not found");
  return {
    id: user.id,
    email: user.email,
    name: user.name
  };
}
```

**Python Example:**

```python
from flask import jsonify, request
from functools import wraps

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Missing auth token"}), 401
        return f(*args, **kwargs)
    return decorated

@app.get('/api/v1/users/<user_id>')
@require_auth
def get_user(user_id):
    """
    Get user by ID

    Response: 200 OK {id, email, name}
    Errors: 404 Not Found, 401 Unauthorized, 403 Forbidden
    Rate limit: 100 requests/min
    Timeout: 5 seconds
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check permissions
    current_user = get_current_user()
    if not can_view_user(current_user, user):
        return jsonify({"error": "Permission denied"}), 403

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name
    })
```

**API Versioning Strategy:**

```
Option 1: URL Versioning (Simple)
GET /v1/users/123
GET /v2/users/123

Option 2: Header Versioning (Clean)
GET /users/123
Header: API-Version: 2

Option 3: Content Negotiation
GET /users/123
Header: Accept: application/vnd.myapp.v2+json

Recommend: URL versioning (simple, clear)
Deprecation: Support v1 for 6 months, then remove
```

---

### 3. Data Management

**Question: How does service manage data?**

**Checklist:**
```
☐ Service owns its data (no shared database)
☐ Data migrations documented
☐ Backup strategy defined
☐ Data retention policy defined
☐ Database indexes optimized (EXPLAIN ANALYZE run)
☐ Connection pooling configured
☐ Read replicas set up (if needed)
```

**Good Data Practice:**

```python
# Service owns its database (no shared access)

class UserService:
    def __init__(self, db_pool):
        # Own database, not shared
        self.db_pool = db_pool

    def get_user(self, user_id):
        """Query from own database."""
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            conn.release()

# [NO] Bad: Sharing database
# Both services query same database
class OrderService:
    def __init__(self, shared_db_pool):
        self.db_pool = shared_db_pool

    def create_order(self, user_id):
        # Querying shared database
        cursor = self.db_pool.query("SELECT * FROM users WHERE id = ?", user_id)
        # Coupled to User Service's schema
```

---

### 4. Service Communication

**Question: How do services talk to each other?**

**Checklist:**
```
☐ Communication pattern documented (sync vs async)
☐ Service discovery mechanism (DNS, Consul, etc.)
☐ Resilience patterns (Circuit Breaker, Retry)
☐ Timeout values set
☐ Error handling defined
☐ Cascading failure prevention (bulkheads)
```

**Good Communication Pattern:**

```python
from circuitbreaker import circuit

class OrderService:
    def __init__(self, payment_service):
        self.payment_service = payment_service

    @circuit(failure_threshold=5, recovery_timeout=60)
    def process_payment(self, amount):
        """Call Payment Service with Circuit Breaker."""
        try:
            # Call with timeout
            result = self.payment_service.charge(
                amount=amount,
                timeout=5
            )
            return result
        except ServiceUnavailable:
            # Service down, circuit breaker will open
            # Next call fails immediately without trying
            raise
        except Exception as e:
            # Log and fail
            logger.error(f"Payment failed: {e}")
            raise

    def create_order(self, customer_id, items):
        try:
            # Try to charge payment
            payment = self.process_payment(total_amount)

            # Create order asynchronously
            self.queue_order_creation(customer_id, items, payment.id)

            return {"success": True, "payment_id": payment.id}

        except ServiceUnavailable:
            # Circuit breaker open, service down
            return {"success": False, "error": "Payment service unavailable"}

        except Exception:
            # Unexpected error, fail the order
            raise
```

**Service Discovery:**

```python
# Using Consul for service discovery
from consul import Consul

class ServiceDiscovery:
    def __init__(self):
        self.consul = Consul(host='consul.example.com')

    def get_service(self, service_name):
        """Get service address from Consul."""
        _, services = self.consul.health.service(service_name, passing=True)
        if not services:
            raise ServiceNotFound(f"{service_name} not available")

        # Pick a service (round-robin)
        service = services[0]
        return f"http://{service['Service']['Address']}:{service['Service']['Port']}"

# Usage
discovery = ServiceDiscovery()
payment_service_url = discovery.get_service('payment-service')
response = requests.get(f"{payment_service_url}/api/charge", ...)
```

---

### 5. Health & Observability

**Question: Can we monitor and debug the service?**

**Health Checks:**

```
Checklist:
☐ Health check endpoint (GET /health)
☐ Readiness probe (can handle requests?)
☐ Liveness probe (is service alive?)
☐ Dependency health (can reach database? Other services?)
```

**Example Health Endpoint:**

```python
@app.get('/health')
def health_check():
    """Service health status."""
    checks = {}

    # Check database connectivity
    try:
        db.query("SELECT 1")
        checks['database'] = 'healthy'
    except Exception as e:
        checks['database'] = f'unhealthy: {e}'

    # Check cache connectivity
    try:
        cache.ping()
        checks['cache'] = 'healthy'
    except Exception as e:
        checks['cache'] = f'unhealthy: {e}'

    # Check downstream service
    try:
        requests.get('http://payment-service/health', timeout=2)
        checks['payment_service'] = 'healthy'
    except Exception as e:
        checks['payment_service'] = f'unhealthy: {e}'

    # Overall status
    is_healthy = all(v == 'healthy' for v in checks.values())
    status = 200 if is_healthy else 503

    return jsonify({
        'status': 'healthy' if is_healthy else 'unhealthy',
        'checks': checks
    }), status

@app.get('/ready')
def readiness():
    """Is service ready to handle requests?"""
    # Check critical dependencies only
    if not database_available():
        return jsonify({'ready': False}), 503
    return jsonify({'ready': True}), 200

@app.get('/live')
def liveness():
    """Is service alive?"""
    # Simple check, doesn't verify dependencies
    return jsonify({'alive': True}), 200
```

**Observability Checklist:**

```
☐ Structured logging (JSON with correlation ID)
☐ Metrics exported (Prometheus, StatsD)
☐ Distributed tracing configured (Jaeger, Zipkin)
☐ Alerts defined (high error rate, latency, etc.)
☐ SLI/SLO defined (what's success?)
```

**Example: Structured Logging**

```python
import logging
import json
from uuid import uuid4

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'service': 'user-service',
            'request_id': getattr(record, 'request_id', None),
            'user_id': getattr(record, 'user_id', None),
            'extra': getattr(record, 'extra', {})
        })

logger = logging.getLogger('user-service')
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Usage with correlation ID
def process_request(request):
    request_id = str(uuid4())
    logger.info(
        "Processing request",
        extra={'request_id': request_id}
    )
    try:
        # Process...
        logger.info("Request succeeded", extra={'request_id': request_id})
    except Exception as e:
        logger.error(
            f"Request failed: {e}",
            extra={'request_id': request_id}
        )
```

---

### 6. Deployment & Operations

**Question: Can we deploy and operate this service independently?**

**Checklist:**
```
☐ Service can be deployed without deploying others
☐ Backward compatibility maintained (old and new versions work)
☐ Database migrations handled gracefully
☐ Canary deployment tested
☐ Rollback procedure documented
☐ Monitoring/alerting in place before deployment
```

**Good Deployment Practice:**

```yaml
# Kubernetes Deployment

apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: myregistry.azurecr.io/user-service:v1.2.3
        ports:
        - containerPort: 8080

        # Health checks
        livenessProbe:
          httpGet:
            path: /live
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5

        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 3

        # Resource limits (prevent resource exhaustion)
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Environment variables
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-service-secret
              key: database-url
        - name: CACHE_REDIS_URL
          value: "redis://cache:6379"
```

**Canary Deployment Script (Go Example):**

```go
package main

import (
    "fmt"
    "log"
    "time"
)

func canaryDeploy(serviceName, newVersion string) error {
    log.Printf("Starting canary deployment of %s:%s", serviceName, newVersion)

    // Step 1: Deploy new version with 10% traffic
    fmt.Printf("Deploying %s:%s with 10%% traffic\n", serviceName, newVersion)
    if err := setTrafficSplit(serviceName, oldVersion=90, newVersion=10); err != nil {
        return fmt.Errorf("failed to set traffic split: %w", err)
    }

    // Step 2: Monitor for 5 minutes
    fmt.Println("Monitoring new version for 5 minutes...")
    time.Sleep(5 * time.Minute)

    // Step 3: Check error rate
    errorRate := getErrorRate(serviceName, newVersion)
    if errorRate > 0.05 { // >5% error rate
        log.Printf("Error rate too high (%.2f%%), rolling back", errorRate*100)
        return rollback(serviceName)
    }

    // Step 4: Increase to 50% traffic
    fmt.Printf("Increasing %s to 50%% traffic\n", newVersion)
    if err := setTrafficSplit(serviceName, oldVersion=50, newVersion=50); err != nil {
        return fmt.Errorf("failed to increase traffic: %w", err)
    }

    // Step 5: Monitor for 10 minutes
    time.Sleep(10 * time.Minute)

    // Step 6: Check again
    errorRate = getErrorRate(serviceName, newVersion)
    if errorRate > 0.05 {
        log.Printf("Error rate too high, rolling back")
        return rollback(serviceName)
    }

    // Step 7: Full deployment
    fmt.Printf("Full deployment of %s:%s\n", serviceName, newVersion)
    if err := setTrafficSplit(serviceName, oldVersion=0, newVersion=100); err != nil {
        return fmt.Errorf("failed to finalize deployment: %w", err)
    }

    log.Printf("Successfully deployed %s:%s", serviceName, newVersion)
    return nil
}
```

---

### 7. Testing

**Question: Is the service tested thoroughly?**

**Checklist:**
```
☐ Unit tests cover critical paths
☐ Integration tests with real database
☐ Contract tests with other services
☐ Load tests show performance baseline
☐ Chaos testing (what if service X is slow?)
☐ Error scenarios tested
```

**Example: Contract Test**

```python
import requests
import pytest

class PaymentServiceContractTest:
    """Test contract between Order Service and Payment Service."""

    @pytest.fixture
    def payment_service_url(self):
        return 'http://localhost:8082'

    def test_charge_payment_success(self, payment_service_url):
        """Test successful payment charge."""
        response = requests.post(
            f'{payment_service_url}/api/v1/charges',
            json={
                'amount': 99.99,
                'currency': 'USD',
                'customer_id': 'cust_123'
            }
        )

        assert response.status_code == 200
        assert 'charge_id' in response.json()
        assert response.json()['amount'] == 99.99

    def test_charge_payment_insufficient_funds(self, payment_service_url):
        """Test payment failure (insufficient funds)."""
        response = requests.post(
            f'{payment_service_url}/api/v1/charges',
            json={
                'amount': 999999.99,
                'currency': 'USD',
                'customer_id': 'cust_poor'
            }
        )

        assert response.status_code == 400
        assert 'insufficient_funds' in response.json()['error']

    def test_charge_payment_timeout(self, payment_service_url):
        """Test payment service timeout."""
        response = requests.post(
            f'{payment_service_url}/api/v1/charges',
            json={'amount': 99.99, 'customer_id': 'cust_123'},
            timeout=5
        )

        # Service should timeout, not hang
        assert response.status_code in [408, 504]
```

---

## Common Microservice Issues

### Issue 1: Shared Database

**Problem:**
```
User Service → Shared Database ← Order Service
              (tight coupling)
```

**Why Bad:**
- User Service can't change schema without coordinating
- Order Service depends on User database being up
- Scaling difficult (can't scale User db independently)

**Fix:**
```
User Service → User Database
Order Service → Order Database

Services communicate via API (loose coupling)
```

### Issue 2: Cascading Failures

**Problem:**
```
Request → Service A → Service B (down) → Timeout → Request hangs
(Service B down affects Service A)
```

**Why Bad:**
- One service down cascades to all upstream services
- Whole system becomes slow/unavailable

**Fix:**
```
Request → Service A
          (with Circuit Breaker, Retry, Timeout)
          → Service B

If Service B down:
- Circuit breaker opens
- Service A fails fast (doesn't hang)
- System stays responsive
```

### Issue 3: Data Consistency

**Problem:**
```
Order created in Order Service
Payment processed in Payment Service
(Events arrive out of order, data inconsistent)
```

**Why Bad:**
- Payment might be processed before order exists
- Orphaned payments, invalid orders

**Fix:**
```
Use Saga pattern:
1. Order Service receives order
2. Publishes "order.created" event
3. Payment Service listens, validates order exists
4. Publishes "payment.processed" or "payment.failed"
5. If failed, Order Service compensates (cancels order)
```

---

## Review Template

**Use this template to review a microservice:**

```markdown
# Review: [Service Name]

## Service Boundaries
- [ ] Domain clearly defined
- [ ] Owns its data
- [ ] Independently deployable

## API Contract
- [ ] Endpoints documented
- [ ] Response formats defined
- [ ] Error handling defined
- [ ] Versioning strategy defined

## Data Management
- [ ] Own database (no shared)
- [ ] Migrations handled
- [ ] Indexes optimized
- [ ] Connection pooling configured

## Communication
- [ ] Pattern documented (sync/async)
- [ ] Resilience patterns implemented
- [ ] Timeouts configured
- [ ] Error handling defined

## Health & Observability
- [ ] Health checks implemented
- [ ] Logging configured (JSON, correlation IDs)
- [ ] Metrics exported
- [ ] Tracing configured
- [ ] Alerts defined

## Deployment
- [ ] Independent deployment tested
- [ ] Backward compatibility maintained
- [ ] Canary deployment documented
- [ ] Rollback procedure documented

## Testing
- [ ] Unit tests adequate
- [ ] Integration tests in place
- [ ] Contract tests with dependencies
- [ ] Load tests performed
- [ ] Error scenarios tested

## Issues Found
1. [Issue]: [Description] [Severity: P1/P2/P3]
2. ...

## Recommendations
1. [Recommendation]
2. ...

## Sign-off
Reviewed by: [Name]
Date: [Date]
Status: APPROVED / APPROVED WITH CONDITIONS / REJECTED
```

---

## Related Commands

- `/pb-patterns-core` — SOA and Event-Driven architecture
- `/pb-patterns-resilience` — Resilience patterns (Circuit Breaker, Retry, Rate Limiting)
- `/pb-patterns-distributed` — Saga, CQRS patterns
- `/pb-observability` — Health checks, monitoring
- `/pb-incident` — Handling microservice failures

---

*Created: 2026-01-11 | Category: Architecture | Tier: L*

