# Observability & Monitoring Design

Build visibility into your system's behavior: metrics, logs, and traces that help you understand what's happening in production.

---

## Observability vs Monitoring

**Monitoring** (narrow):
- Check if something is working (alerts on thresholds)
- Passive: respond to alerts
- Example: "CPU is above 80%, send alert"

**Observability** (broad):
- Understand why it's happening (diagnose issues)
- Active: explore and investigate
- Example: "CPU is high, let's trace which requests caused it"

**The goal**: Observability → Monitoring → Alerting

---

## The Three Pillars of Observability

### 1. Metrics (Numbers)
What is happening? Volume, rate, performance.
- Request count, latency, error rate
- CPU, memory, disk usage
- Database connections, queue depth
- Business metrics (user signups, transactions)

### 2. Logs (Events)
What happened? When? Why?
- Request logs (who, what, when)
- Error logs (what went wrong)
- Application events (user actions, state changes)
- Infrastructure events (deployments, failures)

### 3. Traces (Flows)
How did a request flow through the system?
- Request trace: client → web → database → cache
- Latency breakdown: 100ms total (20ms web, 60ms DB, 10ms cache)
- Failures: where did it break?

---

## Metrics: What to Track

### Request Metrics (Always)

**Latency** (how fast):
- P50 (median), P95, P99 latencies
- By endpoint or operation
- Alert on: P99 > 1000ms (for web API)

```
Example tracking:
  GET /api/users: P99 = 120ms
  POST /api/users: P99 = 450ms (includes email send)
  GET /api/users/{id}: P99 = 80ms
```

**Throughput** (how much):
- Requests per second (RPS)
- By endpoint, status code, method
- Alert on: sudden drop (possible crash)

```
Example tracking:
  Total RPS: 1,200/sec
  GET requests: 800/sec (67%)
  POST requests: 300/sec (25%)
  DELETE requests: 100/sec (8%)
```

**Error Rate** (what breaks):
- 4xx errors (client issues): 1% acceptable
- 5xx errors (server issues): <0.1% target
- By endpoint, error type
- Alert on: 5xx > 0.5%

```
Example tracking:
  GET /api/users: 0.02% 5xx (acceptable)
  POST /api/users: 0.08% 5xx (high!)
    - 401 Unauthorized: 45%
    - 400 Bad Request: 35%
    - 500 Internal Error: 20%
```

### Resource Metrics

**CPU/Memory**:
- Usage percentage (alert on >80% sustained)
- By service, pod, host
- Trending (is it growing?)

**Database**:
- Connection count (alert on >90% of pool)
- Query latency (P95, P99)
- Slow queries (>1s)
- Row counts (growing tables)

**Disk**:
- Used space (alert on >85%)
- Inode usage
- I/O operations

### Business Metrics

Track what matters to business:
- Signups, active users, retention
- Revenue, transactions, conversion rate
- Error impact (transactions failed)
- Feature usage (adoption of new features)

```
Example:
  Signups: 150/day (down 20% from week ago)
  Active users: 25,000 (stable)
  Failed transactions: 12 (0.03%, acceptable)
  → Investigate signup drop, not necessarily an outage
```

---

## Logging: Structured Logs

### Anti-pattern: Unstructured Logs

```
2026-01-11 14:23:45 ERROR User login failed
2026-01-11 14:23:46 User 12345 password incorrect
2026-01-11 14:23:47 WARNING High memory usage
```

Problems:
- Hard to search ("which users failed to login today?")
- Hard to aggregate (metrics require regex parsing)
- Slow (parsing strings is expensive)

### Pattern: Structured Logs (JSON)

```json
{
  "timestamp": "2026-01-11T14:23:45Z",
  "level": "error",
  "service": "auth-service",
  "event": "user_login_failed",
  "user_id": 12345,
  "reason": "incorrect_password",
  "attempt_number": 3,
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "duration_ms": 142
}
```

Benefits:
- Easy to search: `user_login_failed AND user_id:12345`
- Easy to aggregate: count by reason, by service
- Fast: structured data, not regex parsing
- Queryable: `SELECT COUNT(*) WHERE level=error AND duration_ms>1000`

### Log Levels

```
DEBUG    Use: Development, detailed tracing
         Don't: Log in production (too verbose)

INFO     Use: Major events (startup, shutdown, deployments)
         Example: "User 123 logged in"

WARNING  Use: Potentially problematic situations
         Example: "Cache miss rate > 20%"

ERROR    Use: Something failed, but system still works
         Example: "Failed to send email to user 123, will retry"

CRITICAL Use: System is down or degraded
         Example: "Database connection pool exhausted"
```

### What to Log

✅ **DO Log**:
- Errors and exceptions (with stack traces)
- Major state changes (user logged in, order placed)
- Performance concerns (slow queries, timeouts)
- Security events (login attempts, permission denials)
- Debugging info (request IDs, user context)

❌ **DON'T Log**:
- User passwords, API keys, tokens
- Full credit card numbers (log last 4 digits only)
- Personally identifiable info (unless required)
- Debug output from third-party libraries
- Everything (too much log = can't find signal)

### Structured Log Example (Python)

```python
import json
import logging

# Configure structured logging
logger = logging.getLogger(__name__)

def handle_user_login(username, password, ip_address):
    try:
        user = User.find_by_username(username)
        if not user:
            logger.warning(
                json.dumps({
                    "event": "user_not_found",
                    "username": username,  # OK: not sensitive
                    "ip_address": ip_address,
                    "timestamp": datetime.utcnow().isoformat()
                })
            )
            return {"error": "Invalid credentials"}

        if not user.verify_password(password):
            logger.warning(
                json.dumps({
                    "event": "invalid_password",
                    "user_id": user.id,
                    "attempt_number": user.failed_attempts + 1,
                    "ip_address": ip_address
                })
            )
            user.failed_attempts += 1
            return {"error": "Invalid credentials"}

        # Success
        logger.info(
            json.dumps({
                "event": "user_logged_in",
                "user_id": user.id,
                "ip_address": ip_address,
                "session_duration_ms": 0
            })
        )
        return {"success": True, "session_id": create_session(user)}

    except Exception as e:
        logger.error(
            json.dumps({
                "event": "login_error",
                "error": str(e),
                "error_type": type(e).__name__,
                "username": username
            })
        )
        return {"error": "Internal error"}
```

---

## Tracing: End-to-End Visibility

### The Problem (Without Tracing)

User reports: "My request takes 30 seconds!"

Without tracing:
```
Total time: 30 seconds
... but where is it slow?
- API server: ?
- Database: ?
- Cache: ?
- External API: ?
→ Need to guess, investigate each component
```

### The Solution (With Tracing)

```
Request trace ID: 550e8400-e29b-41d4-a716-446655440000

Timeline:
  0ms:     HTTP request arrives
  5ms:     Authentication check (5ms)
  10ms:    Authorization check (5ms)
  200ms:   Database query (190ms) ← SLOW!
  210ms:   Cache update (10ms)
  220ms:   Format response (10ms)
  225ms:   HTTP response sent

Result: Database query is the bottleneck (190ms of 225ms)
Action: Optimize slow query or add index
```

### Distributed Tracing (Microservices)

```
User request to user-service: 100ms

Breakdown:
  10ms: Call auth-service (20ms)
          ├─ 5ms: Call database
          └─ 15ms: Call cache
  40ms: Call order-service (50ms)
          ├─ 30ms: Call payments-api
          └─ 20ms: Call database
  50ms: Format response

Result: Slowest part is payments-api (30ms)
Action: Optimize payments API or add timeout
```

### Implementing Tracing

```python
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup trace exporter (send to Jaeger)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# Instrument HTTP library
RequestsInstrumentor().instrument()

# Create tracer
tracer = trace.get_tracer(__name__)

# Use in code
with tracer.start_as_current_span("database_query") as span:
    span.set_attribute("query", "SELECT * FROM users")
    span.set_attribute("duration_ms", 150)
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
```

---

## Alerting: From Metrics to Actions

### Alert Philosophy

**Good alerts**:
- Actionable (not "something might be wrong")
- Rare (not noisy/flaky)
- Severity-appropriate (critical = page-on-call, warning = slack)

**Bad alerts**:
- "CPU is above 50%" (not specific, not actionable)
- "Error rate changed" (by how much? is it significant?)
- "Database query took 2 seconds" (sometimes OK, depends on query)

### Alert Examples

```
Alert: API P99 Latency High
Condition: P99 latency > 1 second for >= 5 minutes
Severity: WARNING
Action: Check database/cache metrics, review recent deployments

Alert: Database Connection Pool Critical
Condition: Used connections > 90% for >= 2 minutes
Severity: CRITICAL (pages on-call)
Action: Check slow queries, close abandoned connections, scale up

Alert: Error Rate Spike
Condition: 5xx error rate > 1% for >= 1 minute
Severity: CRITICAL
Action: Check recent deployments, review error logs, rollback if needed

Alert: Disk Space Critical
Condition: Disk usage > 90% for >= 10 minutes
Severity: CRITICAL
Action: Delete old logs, archive data, scale storage
```

### Alert Severity Levels

```
CRITICAL (page on-call immediately)
  - System is down or degraded
  - User-facing feature broken
  - Data loss risk
  - Security incident

WARNING (notify team, can wait)
  - Performance issue (but system works)
  - Resource usage high (but not critical)
  - Unusual patterns (but maybe intentional)

INFO (log for reference)
  - Deployments, configuration changes
  - Regular maintenance, backups
  - Scheduled events
```

---

## Dashboards: Visualization

### Key Metrics Dashboard

```
┌─ Service Status ─────────────────────┐
│ ✓ API Server (green)                │
│ ✓ Database (green)                  │
│ ⚠ Cache (yellow - slow response)    │
│ ✓ Queue Workers (green)             │
└─────────────────────────────────────┘

┌─ Request Metrics ────────────────────┐
│ Throughput: 1,200 req/sec            │
│ Latency P50: 80ms                    │
│ Latency P99: 450ms                   │
│ Error Rate: 0.08%                    │
│ 5xx Errors: 10/min                   │
└─────────────────────────────────────┘

┌─ Resources ──────────────────────────┐
│ CPU: 45% (healthy)                   │
│ Memory: 72% (normal)                 │
│ Disk: 58% (OK)                       │
│ Database Connections: 87/100         │
└─────────────────────────────────────┘
```

### Troubleshooting Dashboard

When alert fires, have dashboard that shows:
- Timeline of what happened
- Related metrics (error rate, latency, resources)
- Recent deployments
- Top errors in last hour
- Slow queries
- Resource constraints

---

## On-Call Runbook Template

When alert fires, on-call engineer needs a runbook:

```markdown
# Alert: API P99 Latency High

## Quick Diagnosis (5 min)

1. Check if it's real
   - Is P99 actually > 1s? (might be metric glitch)
   - Is it affecting real users? (check error logs)

2. Gather context
   - Did we deploy recently? (check deployments)
   - Is database slow? (check DB metrics)
   - Is cache down? (check cache metrics)
   - Is there a traffic spike? (check RPS)

## If Database is Slow

1. Connect to database
   ```sql
   SHOW PROCESSLIST;  -- see current queries
   SHOW SLOW LOG;     -- see recent slow queries
   ```

2. Identify slow query
   - Look for query taking > 500ms
   - Check if index missing
   - Check if N+1 queries

3. Options
   - Kill long-running query (if safe)
   - Add index (if appropriate)
   - Scale database (if overloaded)

## If It's a Traffic Spike

1. Is it legitimate?
   - Check graphs (should match user activity)
   - Check recent marketing (PR, social media)
   - Check competitors (did they mention us?)

2. What to do
   - Scale up (if unexpected)
   - Accept it (if expected/temporary)
   - Optimize (if sustained)

## Escalation

If you can't diagnose in 10 minutes:
- Page database expert (if DB slow)
- Page infrastructure expert (if resource constrained)
- Declare incident if affecting customers
```

---

## Integration with Playbook

**Part of design and planning:**
- `/pb-plan` — Include observability in feature planning
- `/pb-guide` — Section 4.4 covers monitoring design
- `/pb-review-code` — Code review checks for logging
- `/pb-release` — Release checklist includes dashboard setup

**Related Commands:**
- `/pb-plan` — Feature planning (include observability)
- `/pb-guide` — SDLC workflow
- `/pb-adr` — Architecture decision (monitoring tools)

---

## Observability Checklist

For each new feature:

Planning Phase:
- [ ] What metrics matter? (latency, errors, business)
- [ ] What events to log? (state changes, errors)
- [ ] How to trace? (request flow, external calls)
- [ ] What to alert on? (when is this broken?)

Implementation Phase:
- [ ] Add metric instrumentation
- [ ] Add structured logging
- [ ] Add distributed tracing
- [ ] Create dashboards

Deployment Phase:
- [ ] Verify metrics are flowing
- [ ] Test alerts (trigger intentionally, verify notification)
- [ ] Create runbooks (for when things break)
- [ ] Document dashboards (what does each chart mean?)

---

## Tools (Popular Options)

**Metrics**: Prometheus, Datadog, New Relic, CloudWatch
**Logs**: ELK Stack, Splunk, Datadog, CloudWatch Logs
**Traces**: Jaeger, Datadog, New Relic, Lightstep
**Alerting**: PagerDuty, Opsgenie, VictorOps
**Dashboards**: Grafana, Kibana, Datadog, New Relic

---

*Created: 2026-01-11 | Category: Planning | Tier: M/L*
