---
name: "pb-testing"
title: "Advanced Testing Scenarios"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-cycle', 'pb-review-tests', 'pb-standards', 'pb-debug']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Advanced Testing Scenarios

Move beyond unit tests. Test behavior, catch mutations, verify contracts, stress systems.

**Mindset:** Testing embodies `/pb-preamble` thinking (challenge assumptions, surface flaws) and `/pb-design-rules` thinking (tests should verify Clarity, verify Robustness, check that failures are loud).

Your tests should challenge assumptions about code behavior. Find edge cases you didn't think of. Question whether tests are actually testing behavior, not just hitting lines of code. Write tests that surface flawed thinking and verify design rules are honored.

**Resource Hint:** sonnet — test strategy design and implementation patterns

---

## When to Use

- Moving beyond unit tests to property-based, mutation, or contract testing
- Designing test strategy for a new service or critical path
- Strengthening weak tests identified by code review or mutation analysis

---

## Purpose

Unit tests find bugs in code. Advanced testing finds bugs in:
- **Property-based tests:** Edge cases you didn't think of
- **Mutation tests:** Tests that are too weak
- **Contract tests:** Integration between services
- **Chaos tests:** Failure scenarios
- **Performance tests:** Degradation under load

---

## Property-Based Testing

### The Problem with Example-Based Tests

```python
# Example-based test (traditional)
def test_sort():
    assert sort([3, 1, 2]) == [1, 2, 3]  # One example
    assert sort([]) == []  # Another example

# Problem: What about edge cases you didn't think of?
# - Negative numbers? Duplicates? Very large lists? Mixed types?
```

### Property-Based Testing Solution

Generate many random inputs, verify property holds for all.

```python
from hypothesis import given, strategies as st

# Property: After sorting, all elements in order
@given(st.lists(st.integers()))
def test_sort_property(unsorted_list):
    sorted_list = sort(unsorted_list)
    # Verify property for ANY input
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]
    # Hypothesis generates 100+ random inputs automatically

# Hypothesis finds edge cases:
# - Empty list: [] → []
# - Single item: [1] → [1]
# - Duplicates: [1, 1, 2] → [1, 1, 2]
# - Negative: [-5, 0, 3] → [-5, 0, 3]
# - Large list: [9123, -4, ...] → sorted
```

### More Property Examples

```python
# Property: Reversing twice gives original
@given(st.lists(st.integers()))
def test_reverse_twice(lst):
    assert reverse(reverse(lst)) == lst

# Property: Adding to set then checking membership is True
@given(st.lists(st.integers()))
def test_set_membership(lst):
    s = set(lst)
    for item in lst:
        assert item in s

# Property: JSON encode then decode gives original
@given(st.lists(st.dictionaries(st.text(), st.integers())))
def test_json_roundtrip(data):
    json_str = json.dumps(data)
    decoded = json.loads(json_str)
    assert decoded == data
```

### When to Use Property-Based Testing

[YES] **DO** use for:
- Utility functions (sort, parse, format)
- Mathematical functions
- Data structure operations
- Encoding/decoding

[NO] **DON'T** use for:
- Functions with complex business logic
- Functions with side effects
- Database queries
- External API calls

---

## Mutation Testing

### The Problem: Weak Tests

```python
# Code being tested
def is_adult(age):
    return age >= 18

# Traditional test (looks good)
def test_is_adult():
    assert is_adult(20) == True
    assert is_adult(10) == False

# Problem: These tests would PASS for ANY implementation
def is_adult_broken(age):
    return True  # Always returns True, test still passes!

def is_adult_broken2(age):
    return age >= 21  # Wrong threshold, test still passes!
```

### Mutation Testing Solution

Mutate code (change >= to >, = to !=, etc) and verify tests fail.

```python
# Mutation testing with mutmut (Python)
# 1. Run tests normally: all pass
pytest

# 2. mutmut finds all code mutations
# 3. Runs tests for each mutation
# 4. Reports which mutations "survived" (tests still pass)

mutmut run

# Results:
# - Mutation: age >= 18 → age > 18
#   Tests: FAIL (good, test caught mutation)
# - Mutation: age >= 18 → age <= 18
#   Tests: FAIL (good, test caught mutation)
# - Mutation: age >= 18 → age >= 17
#   Tests: PASS (BAD, test didn't catch this mutation!)
#   SCORE: 66% (2/3 mutations caught)
```

### Fixing Weak Tests

```python
# Weak test (mutant age >= 17 survives)
def test_is_adult():
    assert is_adult(20) == True
    assert is_adult(10) == False

# Better test (catches age >= 17 mutation)
def test_is_adult():
    assert is_adult(20) == True
    assert is_adult(18) == True   # Boundary: 18 should be True
    assert is_adult(17) == False  # Boundary: 17 should be False
    assert is_adult(10) == False  # Below boundary

# Now mutation age >= 17 is caught!
```

### Mutation Testing Across Languages

**JavaScript:**
```bash
npm install stryker
npx stryker run
# Reports mutation score: % of mutations caught
```

**Python:**
```bash
pip install mutmut
mutmut run --html-report
# Reports detailed mutations and survival
```

**Java:**
```bash
mvn install pitest:mutationCoverage
# Generates HTML report of mutations
```

### When to Use Mutation Testing

[YES] **DO** use for:
- Critical code paths
- Mathematical/utility functions
- Security code
- Data validation

[NO] **DON'T** use for:
- Every function (slow, overkill)
- Integration tests
- UI code

---

## Contract Testing

### The Problem: Integration Breaks

```
Service A (depends on B)
├─ Expects: GET /users returns {"id": int, "name": string}
└─ Tests: Mocks this response, all pass

Service B (provides API)
├─ Implements: GET /users returns {"userId": int, "fullName": string}
└─ Tests: All pass

Problem: Service A calls Service B in production
         API contract changed (id → userId, name → fullName)
         Integration breaks in production
         Tests in both services passed!
```

### Contract Testing Solution

Define contract, both services test against it.

```python
# Shared contract definition
# contracts/user_service_contract.py

USER_CONTRACT = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["id", "name"]
}
```

**Service B (Provider) Tests Contract**

```python
# Service B: Verify API returns contract
import json_schema_validator

def test_get_user_matches_contract():
    response = client.get('/users/123')
    # Verify response matches contract
    validate(response.json(), USER_CONTRACT)
    # If contract defines: {"id": int, "name": string}
    # But code returns: {"userId": int, "fullName": string}
    # Test FAILS (caught before shipping)
```

**Service A (Consumer) Tests Contract**

```python
# Service A: Verify mocks match contract
def test_get_user():
    with mock_user_service(returns=CONTRACT):  # Mock uses contract
        response = user_service.get_user(123)
        # Test uses actual contract, not hand-written mock
        assert response['id'] == 123
        assert response['name'] == 'John'

# If contract changes in Service B, contract definition updates
# Both services see the change, both update their code/tests
```

### Contract Testing Tools

**Pact (Most popular):**
```python
# Provider: Verify API matches consumer contract
from pact import Provider
pact = Provider("UserService")

# Consumer recorded contract expectations
pact.upon_receiving('a request for user 123') \
    .with_request('get', '/users/123') \
    .will_respond_with(200, body={"id": 123, "name": "John"})

# Provider tests: Does our API match consumer expectations?
pact.verify()  # PASS or FAIL
```

### When to Use Contract Testing

[YES] **DO** use for:
- Microservices communication
- Public APIs
- Third-party integrations
- Service boundaries

[NO] **DON'T** use for:
- Internal functions
- Single-service monoliths
- Unit tests

---

## Chaos Engineering

### The Problem: Untested Failure Modes

```python
def get_user_with_orders(user_id):
    user = user_service.get(user_id)      # What if this fails?
    orders = order_service.get(user_id)   # What if this fails?
    recommendations = ai_service.recommend(user_id)  # What if this fails?
    return {user, orders, recommendations}

# Tests: All services work → all tests pass
# Production: AI service is slow one day → what happens?
# Answer: We don't know (and users find out)
```

### Chaos Testing Solution

Intentionally break things, verify system handles gracefully.

```python
# Chaos test: Order service is slow
@chaos_test(failure_mode='latency', service='order_service', latency=10_000)
def test_order_service_slow():
    response = client.get('/users/123')
    # Service should handle gracefully:
    # - Return user with empty orders (fallback)
    # - OR return user without recommendations
    # - OR timeout after 5 seconds with cached data
    # - NOT return error 500
    assert response.status_code == 200
    assert 'user' in response.json()
    assert response.elapsed < 5  # Timeout after 5 seconds

# Chaos test: Database down
@chaos_test(failure_mode='error', service='database', error='connection refused')
def test_database_down():
    response = client.get('/users/123')
    # Should handle gracefully (use cache, return degraded data, etc)
    assert response.status_code in [200, 503]  # OK or degraded service

# Chaos test: External API returns 500
@chaos_test(failure_mode='error_rate', service='payment', error_rate=0.5)
def test_payment_errors():
    # When payment API fails 50% of time:
    results = [client.post('/checkout') for _ in range(100)]
    # Should handle: retry, fallback, queue for later, etc
    # Not just return 500 errors
```

### Chaos Engineering Tools

**Gremlin (Commercial):**
- Inject failures: latency, packet loss, CPU spike, memory leak
- Gradual rollout: 5% of traffic → 25% → 100%
- Automated recovery

**Chaos Toolkit (Open Source):**
```yaml
# chaos-experiment.yml
title: "Order Service Handles Payment Failures"
description: "Verify orders queue when payment API down"

probes:
- type: http
  name: "Get orders"
  method: GET
  url: http://api/orders

actions:
- type: "latency"
  duration: 5000  # 5 second latency
  target: "payment-api"
  percentage: 100

rollbacks:
- type: "stop"
  target: "payment-api-failure"
```

### When to Use Chaos Testing

[YES] **DO** use for:
- Distributed systems
- Microservices
- Critical paths
- Before major incidents happen

[NO] **DON'T** use for:
- Development environments
- Simple systems
- Nice-to-have features

---

## Performance Testing

### Beyond Load Testing

Load testing answers: "Can it handle 10,000 users?"

Performance testing answers: "Is it still fast with 10,000 users? What breaks first?"

```python
# Load test: Can it handle the load?
wrk -c 1000 http://localhost:8000/
# Result: 100 req/sec, system handling

# Performance test: What degrades first?
# 100 users: P99 = 50ms, CPU 20%, Memory 30%, DB connections 10
# 500 users: P99 = 150ms, CPU 60%, Memory 60%, DB connections 50
# 1000 users: P99 = 800ms, CPU 95%, Memory 85%, DB connections 90
# 1500 users: P99 = 8000ms, CPU 100%, Memory 100%, DB connections 100 (LIMIT!)

# Finding: Database connection pool is bottleneck at 1500 users
# Solution: Increase pool size, use connection pooling, optimize queries
```

### Stress Testing (Finding Breaking Points)

```bash
# Start slow, gradually increase load until something breaks
# 10 req/sec → all pass
# 50 req/sec → all pass
# 100 req/sec → all pass
# 500 req/sec → 5% errors (connection pool limit?)
# 750 req/sec → 20% errors
# 1000 req/sec → 50% errors (broken)

# Breaking point found at 500 req/sec (connection pool limit)
```

### Soak Testing (Finding memory leaks)

```bash
# Run constant load for long time (hours, days)
# 100 req/sec for 24 hours

# Monitor:
# Hour 0: Memory 500MB
# Hour 6: Memory 550MB
# Hour 12: Memory 650MB
# Hour 24: Memory 950MB (memory leak!)

# Finding: Memory growing 20MB/hour
# Solution: Find memory leak, fix it
```

---

## Testing in Production

### Safe Practices

[YES] **Production Testing:**
- Real traffic reveals real issues
- Catch edge cases not seen in tests
- Validate actual performance
- Test real integrations

[NO] **But be careful:**
- Don't corrupt user data
- Don't expose security issues
- Have rollback ready
- Monitor closely

### A/B Testing Framework

```python
# Serve two versions, compare metrics
def checkout():
    user = get_user()

    # 50% of users get new checkout, 50% get old
    if user.id % 2 == 0:
        version = 'new_checkout'
        checkout_flow = new_checkout(user)
    else:
        version = 'old_checkout'
        checkout_flow = old_checkout(user)

    # Log which version, then track metrics
    metrics.record('checkout_version', version)
    metrics.record('checkout_success', checkout_flow.succeeded)
    metrics.record('checkout_latency', checkout_flow.duration)

    return checkout_flow

# After 1 week:
# Old: 85% success, 1500ms avg latency
# New: 92% success, 800ms avg latency (BETTER!)
# → Rollout new_checkout to 100%
```

### Synthetic Monitoring (Test Production Regularly)

```python
# Run automated test against production periodically
@schedule(every_5_minutes)
def synthetic_test_production():
    # Test critical user flows
    user = create_test_user()

    # Signup flow
    signup_response = requests.post(
        'https://prod.example.com/api/signup',
        json={'email': user.email, 'password': user.password}
    )
    assert signup_response.status_code == 200

    # Login flow
    login_response = requests.post(
        'https://prod.example.com/api/login',
        json={'email': user.email, 'password': user.password}
    )
    assert login_response.status_code == 200

    # Checkout flow
    checkout_response = requests.post(
        'https://prod.example.com/api/checkout',
        json={'user_id': user.id, 'items': [1, 2, 3]}
    )
    assert checkout_response.status_code == 200

    # If any fail, alert on-call
```

---

## Test Data Strategies

### Problem: Production Data in Tests

```python
# [NO] BAD: Using real production data
def test_checkout():
    user = User.objects.get(id=12345)  # Real user
    checkout = checkout_flow(user)
    # Problem: If test changes data, affects real user
```

### Solution: Test Data Builders

```python
# [YES] GOOD: Build test data on demand
class UserBuilder:
    def __init__(self):
        self.email = f"test_{uuid4()}@example.com"
        self.age = 30
        self.balance = 100

    def with_age(self, age):
        self.age = age
        return self

    def build(self):
        return User.create(**self.__dict__)

def test_checkout():
    user = UserBuilder().with_age(25).build()  # Fresh test user
    checkout = checkout_flow(user)
    assert checkout.succeeded
    # Test data cleaned up after test
```

### Factories for Complex Objects

```python
from factory import Factory, SubFactory

class UserFactory(Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    age = 30
    balance = Decimal('100.00')

class OrderFactory(Factory):
    class Meta:
        model = Order

    user = SubFactory(UserFactory)
    total = Decimal('50.00')
    status = 'pending'

# Usage:
user = UserFactory(age=25)  # Create user with custom age
order = OrderFactory(user=user)  # Create order linked to user
orders = OrderFactory.create_batch(10)  # Create 10 orders
```

---

## Testing Pyramid & Strategy

```
         ┌─────────────────────────┐
         │    E2E Tests (10%)      │  Slow, brittle, but test real flows
         ├─────────────────────────┤
         │ Integration Tests (30%) │  Test component interaction
         ├─────────────────────────┤
         │  Unit Tests (60%)       │  Fast, isolated, unit level
         └─────────────────────────┘
```

**Advanced testing adds:**
```
         ┌──────────────────────────────┐
         │  Chaos/Chaos (5%)            │  Failure scenarios
         ├──────────────────────────────┤
         │  Contract Tests (10%)        │  Integration boundaries
         ├──────────────────────────────┤
         │  Mutation Tests (5%)         │  Test strength
         ├──────────────────────────────┤
         │  Property-Based (10%)        │  Edge cases
         ├──────────────────────────────┤
         │  Synthetic Monitoring (5%)   │  Production health
         ├──────────────────────────────┤
         │  Traditional (65%)           │  Unit/Integration/E2E
         └──────────────────────────────┘
```

---

## Advanced Testing Checklist

### For Utility Functions

- [ ] Unit tests: Happy path + edge cases
- [ ] Property-based tests: Verify properties hold for any input
- [ ] Mutation tests: Verify tests are strong enough

### For Microservices

- [ ] Unit tests: Service logic
- [ ] Contract tests: API contracts with other services
- [ ] Integration tests: With databases/caches
- [ ] Chaos tests: Failure scenarios
- [ ] Synthetic monitoring: Production health

### For Critical Paths

- [ ] Unit tests: Individual components
- [ ] Integration tests: End-to-end flow
- [ ] Performance tests: Can it handle load?
- [ ] Chaos tests: What if external service fails?
- [ ] A/B testing: Real user validation

---

## Integration with Playbook

**Part of quality and testing:**
- `/pb-guide` — Section 6 covers testing strategy
- `/pb-cycle` — Includes testing in peer review
- `/pb-review-tests` — Periodic test review
- `/pb-observability` — Monitoring catches regression

## Related Commands

- `/pb-cycle` — Testing as part of development iteration
- `/pb-review-tests` — Periodic test coverage review
- `/pb-standards` — Code quality and testing principles
- `/pb-debug` — Debugging methodology when tests fail

---

## Advanced Testing Checklist

### Setup

- [ ] Property-based testing framework installed (Hypothesis, QuickCheck, etc)
- [ ] Mutation testing tool configured (mutmut, Stryker, etc)
- [ ] Contract testing tool ready (Pact, Spring Cloud Contract)
- [ ] Chaos engineering platform available (Chaos Toolkit, Gremlin)
- [ ] Load testing tool configured (wrk, k6, Locust)

### Implementation

- [ ] Property-based tests for utility functions
- [ ] Mutation tests on critical code (target > 90% mutation score)
- [ ] Contract tests on service boundaries
- [ ] Chaos tests for failure scenarios
- [ ] Synthetic monitoring on critical paths

### Validation

- [ ] Property tests find edge cases
- [ ] Mutation tests catch weak tests
- [ ] Contract tests prevent integration breaks
- [ ] Chaos tests verify graceful degradation
- [ ] Synthetic tests verify production health

---

*Created: 2026-01-11 | Category: Development | Tier: M/L*

