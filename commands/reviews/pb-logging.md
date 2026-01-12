# Logging Strategy & Standards

Comprehensive guidance for designing effective logging that aids troubleshooting without creating noise.

**Principle:** Good logging embodies `/pb-preamble` thinking (reveal assumptions, surface problems) and `/pb-design-rules` thinking (especially Transparency and Silence: systems should be observable when important, quiet otherwise).

Logs must invite scrutiny. They should reveal assumptions and make failures obvious, not hide them with verbosity or silence.

---

## Purpose

Logging is critical for observability in production. This guide helps you:
- Determine appropriate log levels for different events
- Eliminate redundant and noisy logs
- Ensure logs are actionable and context-rich
- Standardize logging across your codebase
- Verify security and compliance requirements

---

## Log Levels: When to Use Each

### DEBUG
**Use for**: Detailed troubleshooting information

```python
logger.debug("Entered function process_order()", extra={"user_id": 123})
logger.debug("Query took 45ms", extra={"query": "SELECT ...", "rows": 50})
logger.debug("Cache hit for key: user_profile_123")
```

**Characteristics:**
- Enabled only during development or when investigating specific issues
- Includes variable values, loop iterations, internal state
- Should not be logged to production by default (configure via log level)

**Pitfalls:**
- Not useful in production (logging is disabled anyway)
- Creates noise if left at DEBUG level unnecessarily

---

### INFO
**Use for**: Important business events and state changes

```python
logger.info("User registered", extra={"user_id": 456, "email": "user@example.com"})
logger.info("Order created", extra={"order_id": "ORD-789", "customer_id": 456, "total": 99.99})
logger.info("Payment processed successfully", extra={"payment_id": "PAY-123", "amount": 99.99})
logger.info("Job completed", extra={"job_id": 999, "duration_ms": 5000, "status": "success"})
```

**Characteristics:**
- Visible in production
- Tracks user-visible actions and business events
- Includes IDs and relevant context
- Follows "Verb + noun + context" pattern

**Pitfalls:**
- "Processing user" - too vague
- "Got here" - non-actionable
- "User registration initiated" - clear and actionable

---

### WARNING
**Use for**: Recoverable problems and unexpected but handled situations

```python
logger.warning("Slow database query detected", extra={
    "query_ms": 2500,
    "threshold_ms": 1000,
    "query": "SELECT ... FROM orders WHERE customer_id = ?"
})
logger.warning("External service degraded, retrying", extra={
    "service": "payment_provider",
    "retry_count": 2,
    "timeout_ms": 5000
})
logger.warning("Cache miss spike detected", extra={
    "miss_rate": 0.45,
    "threshold": 0.20,
    "duration_sec": 60
})
```

**Characteristics:**
- Indicates something unexpected happened but the system recovered
- Usually indicates fallback behavior
- Includes metrics or context for investigation

**Pitfalls:**
- Warning for every retried request (too noisy)
- Warning for expected rate limit responses (should be INFO if handled)
- Warning for unusual patterns: slow queries, high error rates

---

### ERROR
**Use for**: Genuine error conditions that need attention

```python
logger.error("Failed to charge payment", extra={
    "payment_id": "PAY-456",
    "reason": "Card declined",
    "error_code": "card_declined",
    "stack_trace": "..." # Include only if helpful for root cause
})
logger.error("Database connection failed", extra={
    "host": "db.prod.example.com",
    "error": "connection timeout",
    "timeout_ms": 5000,
    "attempt": 3
})
```

**Characteristics:**
- Operation failed; action is required
- Include enough context to investigate without access to customer data
- Include error codes, error messages, and relevant context
- Stack traces helpful only for unexpected errors

**Critical:**
- Never log passwords, API keys, PII, or sensitive data
- Log error codes and codes that help identify the issue

---

### CRITICAL
**Use for**: System-wide failures requiring immediate action

```python
logger.critical("Database unavailable - all requests failing", extra={
    "service": "primary_database",
    "status": "connection_refused",
    "impact": "total_outage"
})
logger.critical("Authentication service down", extra={
    "service": "auth_service",
    "response_code": 503,
    "health_check": "failed"
})
```

**Characteristics:**
- System is down or severely degraded
- Triggers page/alert to on-call
- Should be rare (aim for < 1 per month)

**Pitfalls:**
- Using CRITICAL for issues that only affect one user
- Using CRITICAL only for platform-wide outages

---

## Common Logging Patterns

### Authentication & Authorization

```python
# [YES] Good: Log security events without exposing credentials
logger.info("User login successful", extra={
    "user_id": 789,
    "login_method": "email_password",
    "ip_address": "203.0.113.42"
})

logger.warning("Failed login attempt", extra={
    "email": "user@example.com",  # OK to log email, not password
    "attempt": 3,
    "reason": "invalid_password"
})

logger.error("Account locked after failed attempts", extra={
    "user_id": 789,
    "failed_attempts": 5,
    "lockout_duration_min": 30
})

# [NO] Bad: Logging credentials
logger.debug("Login attempt", extra={"username": "user@example.com", "password": "secret123"})
```

### External Service Calls

```python
# [YES] Good: Log request, response, and timing
logger.info("Payment service called", extra={
    "service": "stripe",
    "method": "charge",
    "amount": 99.99,
    "request_id": "req_123abc"
})

logger.warning("Payment service slow", extra={
    "service": "stripe",
    "latency_ms": 3500,
    "timeout_ms": 5000
})

logger.error("Payment service error", extra={
    "service": "stripe",
    "status_code": 500,
    "error_message": "Internal Server Error",
    "request_id": "req_123abc"
})
```

### Database Operations

```python
# [YES] Good: Log queries that matter
logger.info("Order created in database", extra={
    "order_id": "ORD-999",
    "customer_id": 456,
    "items_count": 3
})

logger.warning("Slow database query", extra={
    "query": "SELECT * FROM orders ...",
    "duration_ms": 2000,
    "rows_returned": 50000
})

# [NO] Bad: Logging every SELECT (creates noise)
logger.debug("SELECT user WHERE id = 123")
logger.debug("SELECT orders WHERE customer_id = 456")
```

### Job/Task Processing

```python
# [YES] Good: Log job lifecycle
logger.info("Background job started", extra={
    "job_id": 999,
    "job_type": "send_email",
    "user_id": 456
})

logger.info("Background job completed", extra={
    "job_id": 999,
    "duration_ms": 5000,
    "status": "success"
})

logger.error("Background job failed", extra={
    "job_id": 999,
    "error": "SMTP connection timeout",
    "retries_remaining": 2,
    "retry_after_sec": 60
})
```

---

## Structured Logging Best Practices

### Consistent Format

```python
# [YES] Good: JSON structured logging
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            **record.extra if hasattr(record, 'extra') else {}
        })

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Usage:
logger.info("User registered", extra={
    "user_id": 123,
    "email": "user@example.com"
})
```

### Include Correlation IDs (Microservices)

```python
import uuid
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')

def log_with_correlation(message, level, **context):
    """Log with automatic correlation ID for request tracing."""
    context['correlation_id'] = correlation_id_var.get()
    logger.log(level, message, extra=context)

# Middleware to set correlation ID
def correlation_id_middleware(request):
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    correlation_id_var.set(correlation_id)
    return request
```

### Context and Exception Handling

```python
# [YES] Good: Include exception context
try:
    process_payment(order)
except PaymentError as e:
    logger.error("Payment processing failed", extra={
        "order_id": order.id,
        "error_code": e.code,
        "error_message": str(e),
        "exception": type(e).__name__
    })
    raise
```

---

## Log Level Configuration by Environment

### Development
```
DEBUG: All levels enabled (catch all issues early)
```

### Staging
```
INFO: Business events only (monitor production-like behavior)
WARNING: Unusual patterns
ERROR: Failed operations
CRITICAL: System failures
```

### Production
```
INFO: Business events (user actions, transactions)
WARNING: Unexpected conditions (slow requests, retries)
ERROR: Failed operations (requires investigation)
CRITICAL: System outages (page on-call)

DEBUG: Disabled (logs to /dev/null)
```

**Configuration Example (Python):**
```python
import os
import logging

log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))

# Specific module log levels
logging.getLogger('vendor_library').setLevel(logging.WARNING)  # Less verbose for 3rd party
logging.getLogger('myapp.payment').setLevel(logging.DEBUG)      # More verbose for critical
```

---

## Common Issues & Fixes

### Problem: "Log Bombing" - Too Many Logs

**[NO] Example:**
```python
for user_id in user_ids:
    logger.info(f"Processing user {user_id}")  # Logs 1000 times!
    logger.info(f"Fetched data for user {user_id}")
    logger.info(f"Updated database for user {user_id}")
```

**[YES] Fix:**
```python
logger.info("Starting bulk user processing", extra={"total_users": len(user_ids)})
for user_id in user_ids:
    # Only log errors, not normal flow
    try:
        process_user(user_id)
    except Exception as e:
        logger.error("Failed to process user", extra={
            "user_id": user_id,
            "error": str(e)
        })
logger.info("Bulk user processing completed", extra={
    "total_users": len(user_ids),
    "duration_sec": elapsed_time
})
```

---

### Problem: Missing Context

**[NO] Bad:**
```python
logger.error("Connection failed")  # Which connection? Which service?
logger.warning("Request timed out")  # Which request? What timeout?
```

**[YES] Good:**
```python
logger.error("Database connection failed", extra={
    "host": "db.prod.example.com",
    "port": 5432,
    "error": "connection refused",
    "timeout_ms": 5000
})
logger.warning("API request timed out", extra={
    "service": "payment_provider",
    "endpoint": "/api/charges",
    "timeout_ms": 5000,
    "attempt": 2
})
```

---

### Problem: Logging Sensitive Data

**[NO] Bad:**
```python
logger.info("User login", extra={
    "email": user.email,
    "password": user.password,  # NEVER log this!
    "ssn": user.ssn              # NEVER log this!
})
```

**[YES] Good:**
```python
logger.info("User login successful", extra={
    "user_id": user.id,
    "email_hash": hash(user.email),  # Hash for verification
    "ip_address": request.remote_addr
})
```

---

## Logging Checklist

Before deploying, verify:

- [ ] **No sensitive data**: No passwords, API keys, PII in logs
- [ ] **Appropriate levels**: DEBUG/INFO in right places
- [ ] **Unique identifiers**: Include IDs (user_id, order_id, request_id)
- [ ] **Correlation IDs**: All related requests traceable (microservices)
- [ ] **Error context**: Errors include error codes and context
- [ ] **Not redundant**: Same information not logged twice
- [ ] **Not noisy**: Not logging every normal operation
- [ ] **Parsing-friendly**: JSON structured logging (not raw strings)
- [ ] **Performance impact**: Logging overhead acceptable in hot paths

---

## Integration with Playbook

**Related to logging:**
- `/pb-security` — Logging sensitive data safely
- `/pb-observability` — Logging as part of observability
- `/pb-incident` — Using logs during incident investigation
- `/pb-guide` — Implementing logging in development
- `/pb-testing` — Testing logging behavior

**Tools to consider:**
- **Local**: Python `logging`, Node.js `winston`, Go `zap`
- **Cloud**: AWS CloudWatch, GCP Cloud Logging, Azure Monitor
- **Aggregation**: ELK Stack, Splunk, Datadog, New Relic

---

*Created: 2026-01-11 | Category: Code Review | Tier: M*
