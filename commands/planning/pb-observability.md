---
name: "pb-observability"
title: "Observability & Monitoring Design"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-logging', 'pb-incident', 'pb-sre-practices', 'pb-performance', 'pb-maintenance']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Observability & Monitoring Design

Build visibility into your system's behavior: metrics, logs, and traces that help you understand what's happening in production.

**Mindset:** Observability is multi-perspective understanding. You need metrics, logs, and traces—different views of the same system. This embodies `/pb-preamble` thinking (no single perspective is complete) and `/pb-design-rules` thinking (especially Transparency: design for visibility to make debugging easier).

Question your assumptions about what's happening in production. Systems should be observable; you shouldn't need to guess.

**Resource Hint:** sonnet — Observability design follows structured instrumentation patterns.

## When to Use

- Designing monitoring and observability for a new service
- Diagnosing gaps in production visibility (missing metrics, logs, or traces)
- Planning instrumentation before a major deployment

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

[YES] **DO Log**:
- Errors and exceptions (with stack traces)
- Major state changes (user logged in, order placed)
- Performance concerns (slow queries, timeouts)
- Security events (login attempts, permission denials)
- Debugging info (request IDs, user context)

[NO] **DON'T Log**:
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

## SLI, SLO, and Error Budgets

### Definitions

**SLI (Service Level Indicator)** — A metric that measures performance:
- Example: "API P99 latency is 120ms" or "System uptime is 99.95%"
- Measurable using monitoring data (from metrics/logs)
- You measure the actual SLI value

**SLO (Service Level Objective)** — A target for your SLI:
- Example: "API P99 latency should be < 200ms" or "System uptime target: 99.95%"
- What you promise to users (in SLA) or commit internally
- SLO is the target; SLI is the measurement against it

**SLA (Service Level Agreement)** — A contract with customers:
- What happens if you miss SLO (refunds, credits, penalties)
- External promise (affects revenue/reputation)
- Optional: Many internal services don't have SLAs

**Error Budget** — How much you can fail and still meet SLO:
- If SLO is 99.9% uptime, error budget is 0.1%
- Over 30 days: 0.1% of 30 days × 24h × 3600s = 25,920 seconds ≈ 7.2 hours of allowed downtime
- Use error budget to decide: Ship risky feature? Take infrastructure down? Run load tests?

### Setting SLIs & SLOs

**Step 1: Identify critical user journeys**
- Example: User signup, product search, checkout, payment processing
- Not every endpoint needs an SLO (focus on critical paths)

**Step 2: Choose meaningful SLIs for each journey**

```
Critical Journey: User Payment
├─ SLI 1: API latency (P99)
│  └─ SLO: < 500ms for 99.9% of requests
├─ SLI 2: Success rate
│  └─ SLO: > 99.99% (< 0.01% failure)
└─ SLI 3: Data freshness
   └─ SLO: Payment recorded within 5 seconds

Critical Journey: Product Search
├─ SLI 1: Search latency (P95)
│  └─ SLO: < 200ms for 95% of requests
├─ SLI 2: Search accuracy
│  └─ SLO: > 95% of results relevant
└─ SLI 3: Availability
   └─ SLO: 99.9% uptime
```

**Step 3: Be realistic**
- Don't promise 99.99% if you have external dependencies you don't control
- Start conservative (99.5%); tighten as confidence grows
- Remember: 99.9% means ~43 minutes downtime/month; 99.99% means ~4 minutes/month

### Error Budget Example

**SLO:** 99.9% uptime for payment processing (0.1% error budget)

**Budget allocation over month (30 days × 24h × 3600s = 2,592,000s total):**
```
Total allowed downtime: 0.1% × 2,592,000s = 2,592 seconds ≈ 43.2 minutes

Allocation:
  Scheduled maintenance:     15 minutes (35% of budget)
  Unplanned incidents:       15 minutes (35% of budget)
  Load testing/risky deploys: 13 minutes (30% of budget)
  Reserve:                    0 minutes (fully allocated)
```

**Decision-making:**
- "Should we deploy the risky feature?" → Check error budget
  - If budget remaining > 13 min, OK. Otherwise, wait for next month
- "Is this incident worth investigating?" → If it consumed budget, yes
- "Can we do maintenance?" → Only if budget allows

### Monitoring SLIs & SLOs

Use alerts to catch SLO violations early:

```
Alert: Approaching SLO Violation
Condition: If current rate would miss SLO by end of day
Action: Page on-call to prevent further failures
Example: 5xx rate is 0.08% (approaching 0.1% daily limit)

Alert: SLO Violated
Condition: SLI has exceeded SLO for 5 minutes
Action: Immediate incident response
Example: Latency P99 exceeded 500ms for 5+ minutes
```

Track error budget burn rate:

```
Prometheus query:
  rate(errors_total[5m]) / rate(requests_total[5m])  # Current 5-min error rate

If SLO allows 0.1% errors:
  - Current burn rate > 0.1%: Burning budget fast (yellow alert)
  - Current burn rate > 0.5%: Burning budget very fast (red alert)
```

### SLI/SLO Template

Copy this for each critical service:

```markdown
## Service: [Payment Processing]

### SLOs (What we promise)

| SLI | Target | Why | Owner |
|-----|--------|-----|-------|
| Latency P99 | < 500ms | Users expect responsive checkout | Payments team |
| Success rate | > 99.99% | Failed charges damage trust | Payments team |
| Data freshness | < 5s | Reconciliation depends on accuracy | Finance + Payments |
| Availability | 99.9% | 43 min downtime/month acceptable | Infrastructure |

### Error Budget (monthly)

| Category | Time | % of Budget |
|----------|------|------------|
| Scheduled maintenance | 15 min | 35% |
| Incident response | 15 min | 35% |
| Risky deployments | 13 min | 30% |
| **Total** | **43.2 min** | **100%** |

### Current Status (this month)

| SLI | Target | Actual | Status | Burn |
|-----|--------|--------|--------|------|
| Latency P99 | < 500ms | 185ms | [YES] Green | Good |
| Success rate | > 99.99% | 99.991% | [YES] Green | Good |
| Availability | 99.9% | 99.94% | [YES] Green | Good |
| Budget remaining | 43.2 min | 38 min | ⚠️ Yellow | Normal |

### Actions

- [ ] If budget < 10 min: Freeze risky deployments
- [ ] If any SLI approaching SLO: Incident response
- [ ] Weekly review of burn rate vs. targets
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

## Prometheus Query Examples

If using Prometheus, these PromQL queries are commonly useful:

### Request Rate & Errors

```promql
# Request rate per second (5-minute average)
rate(http_requests_total[5m])

# Error rate (5xx only)
rate(http_requests_total{status=~"5.."}[5m])

# Error rate as percentage
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100

# 4xx vs 5xx error rates
rate(http_requests_total{status=~"4.."}[5m]) # Client errors
rate(http_requests_total{status=~"5.."}[5m]) # Server errors

# Requests by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Errors by endpoint (find problematic endpoints)
sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint)
```

### Latency (Duration)

```promql
# P95 latency (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# P99 latency (99th percentile)
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Average latency
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Latency by endpoint
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) by (endpoint)

# Slow requests (> 1 second)
rate(http_request_duration_seconds_bucket{le="+Inf"}[5m]) - rate(http_request_duration_seconds_bucket{le="1"}[5m])
```

### Resource Usage

```promql
# CPU usage percentage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage percentage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk usage percentage
(node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes * 100

# Database connections in use
pg_stat_activity_count # PostgreSQL
OR mysql_global_status_threads_connected # MySQL
```

### Database Performance

```promql
# Query execution rate
rate(mysql_global_status_queries[5m])

# Slow query rate
rate(mysql_global_status_slow_queries[5m])

# Connection pool usage
mysql_global_status_threads_connected / mysql_global_variables_max_connections

# Replication lag (MySQL)
mysql_slave_status_seconds_behind_master
```

### SLO Monitoring

```promql
# Error budget burn rate (5-minute)
rate(errors_total[5m]) / rate(requests_total[5m])

# SLO status: Is P99 latency within SLO? (SLO: 500ms)
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) < 0.5

# Availability (uptime) over last month
avg_over_time((up[1m])[30d:1m]) * 100
```

### Useful Query Patterns

```promql
# Alert if any endpoint has > 1% error rate
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) > 0.01

# Alert if P99 latency > 1 second
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1

# Alert if CPU > 80% for more than 5 minutes
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80

# Alert if disk > 85%
(node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes > 0.85
```

---

## Integration with Playbook

**Part of design and planning:**
- `/pb-plan` — Include observability in feature planning
- `/pb-guide` — Section 4.4 covers monitoring design
- `/pb-review-hygiene` — Code review checks for logging
- `/pb-release` — Release checklist includes dashboard setup

**Related Commands:**
- `/pb-plan` — Feature planning (include observability)
- `/pb-guide` — SDLC workflow
- `/pb-adr` — Architecture decision (monitoring tools)
- `/pb-sre-practices` — SRE operational practices, error budgets

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

## Related Commands

- `/pb-logging` — Logging strategy and standards for structured logging
- `/pb-incident` — Incident response when observability alerts fire
- `/pb-sre-practices` — SRE operational practices and error budgets
- `/pb-performance` — Performance optimization using observability data
- `/pb-maintenance` — Preventive maintenance (monitoring detects; maintenance prevents)

---

*Created: 2026-01-11 | Category: Planning | Tier: M/L*
