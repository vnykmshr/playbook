---
name: "pb-observability"
title: "Observability & Monitoring Design"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-logging', 'pb-incident', 'pb-sre-practices', 'pb-performance', 'pb-maintenance']
last_reviewed: "2026-11-05"
version: "1.1.0"
version_notes: "v1.1.0: One 5xx alert threshold; resource alerts use the /pb-sre-practices thresholds; the error budget arithmetic is fixed (43.2 min); Log Levels point at /pb-logging; the login sample logs no username; tracing names OpenTelemetry over OTLP instead of the removed Jaeger exporter; PromQL cut to five valid SLO queries; Integration with Playbook section removed."
breaking_changes: []
---
# Observability & Monitoring Design

Build visibility into your system's behavior: metrics, logs, and traces that help you understand what's happening in production.

**Mindset:** Observability is multi-perspective understanding. You need metrics, logs, and traces - different views of the same system. This embodies `/pb-preamble` thinking (no single perspective is complete) and `/pb-design-rules` thinking (especially Transparency: design for visibility to make debugging easier).

Question your assumptions about what's happening in production. Systems should be observable; you shouldn't need to guess.

**Resource Hint:** sonnet - Observability design follows structured instrumentation patterns.

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
- Alert on: 5xx > 1% for 1 minute

```
Example tracking:
  GET /api/users: 0.02% 5xx (acceptable)
  POST /api/users: 0.08% 5xx (high!)
    - 401 Unauthorized: 45%
    - 400 Bad Request: 35%
    - 500 Internal Error: 20%
```

### Resource Metrics

Alert thresholds for CPU, memory, disk and connections are the `/pb-sre-practices` Capacity Metrics table's.

**CPU/Memory**:
- Usage percentage, sustained
- By service, pod, host
- Trending (is it growing?)

**Database**:
- Connection count (share of pool)
- Query latency (P95, P99)
- Slow queries (>1s)
- Row counts (growing tables)

**Disk**:
- Used space
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

Levels and what each means in production: `/pb-logging`.

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
                    "ip_address": ip_address
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
                "error_type": type(e).__name__
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

Instrument with OpenTelemetry (SDK plus auto-instrumentation for your HTTP and database libraries) and export over OTLP to the backend: Jaeger, Grafana Tempo, Honeycomb, Datadog. Jaeger ingests OTLP directly; its dedicated exporter is gone.

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
Condition: Used connections > 85% for >= 2 minutes
Severity: CRITICAL (pages on-call)
Action: Check slow queries, close abandoned connections, scale up

Alert: Error Rate Spike
Condition: 5xx error rate > 1% for >= 1 minute
Severity: CRITICAL
Action: Check recent deployments, review error logs, rollback if needed

Alert: Disk Space Critical
Condition: Disk usage > 85% for >= 10 minutes
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

**SLI (Service Level Indicator)** - A metric that measures performance:
- Example: "API P99 latency is 120ms" or "System uptime is 99.95%"
- Measurable using monitoring data (from metrics/logs)
- You measure the actual SLI value

**SLO (Service Level Objective)** - A target for your SLI:
- Example: "API P99 latency should be < 200ms" or "System uptime target: 99.95%"
- What you promise to users (in SLA) or commit internally
- SLO is the target; SLI is the measurement against it

**SLA (Service Level Agreement)** - A contract with customers:
- What happens if you miss SLO (refunds, credits, penalties)
- External promise (affects revenue/reputation)
- Optional: Many internal services don't have SLAs

**Error Budget** - How much you can fail and still meet SLO:
- If SLO is 99.9% uptime, error budget is 0.1%
- Over 30 days: 0.1% of 2,592,000 s = 2,592 s ≈ 43.2 minutes of allowed downtime
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

````markdown
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
   SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;  -- needs log_output=TABLE
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
````

---

## Prometheus Queries for SLOs

```promql
# Request rate per second
sum(rate(http_requests_total[5m]))

# 5xx error ratio (alert above 0.01)
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# P99 latency by endpoint (sum the buckets by le before the quantile)
histogram_quantile(0.99, sum by (le, endpoint) (rate(http_request_duration_seconds_bucket[5m])))

# Availability over 30 days, percent
avg_over_time(up[30d]) * 100

# Burn rate against a 99.9% SLO (1 = spending the budget exactly on pace)
(sum(rate(http_requests_total{status=~"5.."}[1h])) / sum(rate(http_requests_total[1h]))) / 0.001
```

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

- `/pb-logging` - Logging strategy and standards for structured logging
- `/pb-incident` - Incident response when observability alerts fire
- `/pb-sre-practices` - SRE operational practices and error budgets
- `/pb-performance` - Performance optimization using observability data
- `/pb-maintenance` - Preventive maintenance (monitoring detects; maintenance prevents)
