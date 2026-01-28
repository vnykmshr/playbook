# Production Maintenance

Establish systematic maintenance patterns to prevent production incidents. This playbook provides thinking triggers for database maintenance, backup verification, health monitoring, and alerting strategy.

**Mindset:** Maintenance embodies `/pb-design-rules` thinking: Robustness (systems fail gracefully when maintenance lapses) and Transparency (make system health visible). Apply `/pb-preamble` thinking to challenge assumptions about what's "good enough" maintenance.

---

## When to Use This Command

- **New production deployment** — Establish maintenance patterns from day one
- **After incidents** — Add maintenance tasks that would have prevented the incident
- **Quarterly reviews** — Audit and update maintenance schedules
- **Capacity planning** — Maintenance is part of resource planning
- **Onboarding** — Help new team members understand operational patterns

---

## Quick Reference

| Tier | Frequency | Focus |
|------|-----------|-------|
| Daily | Every day | Logs, backups, health checks |
| Weekly | Once/week | Database stats, security updates, reports |
| Monthly | Once/month | Deep cleans, cert audits, DR tests |

---

## Philosophy

Production systems accumulate entropy:
- Databases bloat with dead data
- Disks fill with logs and artifacts
- Certificates expire silently
- Dependencies develop vulnerabilities
- Backups rot without verification

**This playbook provides thinking triggers, not prescriptions.** Every project has different needs — use these patterns to ask the right questions about your system.

---

## Core Questions

Before implementing maintenance, answer:

1. **What accumulates?** (logs, dead tuples, orphan records, temp files)
2. **What expires?** (certificates, tokens, cache entries, sessions)
3. **What drifts?** (config, dependencies, schema, data integrity)
4. **What breaks silently?** (backups, health checks, alerting itself)

---

## Maintenance Tiers

| Tier | Frequency | Purpose | Questions to Ask |
|------|-----------|---------|------------------|
| **Daily** | Every day | Prevent accumulation | What grows unbounded? What needs rotation? |
| **Weekly** | Once/week | Catch drift | What statistics go stale? What reports matter? |
| **Monthly** | Once/month | Deep clean | What requires downtime? What needs verification? |

**Principle:** Automate aggressively, monitor passively, intervene rarely.

---

## Database Maintenance

### Questions to Ask

- Does your database have automatic maintenance (autovacuum, etc.)?
- Is automatic maintenance sufficient, or does your write pattern need manual intervention?
- How do you detect bloat before it causes problems?
- What's your index maintenance strategy?

### PostgreSQL Patterns

| Task | Purpose | When to Consider |
|------|---------|------------------|
| `VACUUM ANALYZE` | Mark dead tuples reusable, update stats | High-write tables, weekly minimum |
| `VACUUM FULL` | Reclaim disk space (requires lock) | Significant bloat, monthly or less |
| `REINDEX` | Rebuild bloated indexes | After bulk deletes, schema changes |

**Bloat detection trigger:**
```sql
-- Adapt this query to your tables
SELECT relname, n_dead_tup, n_live_tup,
       round(100.0 * n_dead_tup / NULLIF(n_live_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

**Ask:** Which tables in your system have the highest write churn?

### Other Databases

- **MySQL:** `OPTIMIZE TABLE`, `ANALYZE TABLE`, binary log purging
- **MongoDB:** `compact`, index rebuilds, oplog sizing
- **Redis:** Memory monitoring, key expiration policies
- **SQLite:** `VACUUM`, `ANALYZE`

**Ask:** What's the equivalent maintenance for your database?

---

## Backup Strategy

### Questions to Ask

- When did you last verify a backup by restoring it?
- How long would recovery take?
- What's not in your backup? (uploads, generated files, external services)
- Do you have off-site copies?

### 3-2-1 Principle

- **3** copies of data
- **2** different storage types
- **1** offsite

### Verification Trigger

Backups are worthless until tested. Schedule periodic restore tests:

```bash
# Pattern: verify backup is not empty/corrupted
# Adapt to your backup format
# Note: stat flags differ by platform (-c%s on Linux, -f%z on macOS)
BACKUP_SIZE=$(stat -c%s "$BACKUP_FILE" 2>/dev/null || stat -f%z "$BACKUP_FILE")
if [[ "$BACKUP_SIZE" -lt 1000 ]]; then
    echo "ALERT: Backup suspiciously small: $BACKUP_FILE ($BACKUP_SIZE bytes)"
    # Send to your alerting system (Slack, PagerDuty, etc.)
fi
```

**Ask:** What would you do at 2 AM if you needed to restore?

---

## Health Monitoring

### Questions to Ask

- What's the minimum check that proves the system works end-to-end?
- What dependencies can fail silently?
- How do you know if monitoring itself is broken?

### Health Check Dimensions

| Dimension | What to Check |
|-----------|---------------|
| Service health | HTTP endpoints, process status |
| Dependencies | Database connections, cache, queues |
| Resources | Disk, memory, connections, file descriptors |
| Certificates | SSL expiry, API key rotation |
| Data integrity | Expected counts, orphan records |

**Pattern:** Health checks should be cheap, fast, and actionable.

**Ask:** If this health check fails, what would you do about it?

---

## Resource Monitoring

### Questions to Ask

- What resources can be exhausted?
- What are the warning thresholds vs. critical thresholds?
- Who gets alerted, and can they act on it?

### Common Resources

| Resource | Warning Sign | Question |
|----------|--------------|----------|
| Disk | >70% full | What's growing? Logs? Data? Uploads? |
| Memory | Sustained >85% | Memory leak? Undersized? Cache unbounded? |
| Connections | >70% of pool | Connection leak? Pool too small? |
| File descriptors | Approaching limit | Too many open files? Socket leak? |

**Ask:** What's the first resource that will run out in your system?

---

## Security Hygiene

### Questions to Ask

- When was the last security update applied?
- What's your certificate renewal process?
- How do you detect unauthorized access attempts?
- What secrets need rotation, and when?

### Maintenance Dimensions

| Frequency | Focus |
|-----------|-------|
| Daily | Failed login monitoring, intrusion detection |
| Weekly | Security update check, audit log review |
| Monthly | Dependency vulnerability scan, certificate audit |
| Quarterly | Access review, secret rotation |

**Ask:** What would an attacker target first in your system?

---

## Post-Migration Verification

**Critical pattern:** After any migration, verify that:

1. **Database records match reality** — Rows exist, counts are correct
2. **Generated artifacts exist** — Files tracked in DB actually exist on disk
3. **Volumes are mounted correctly** — Containers can access expected paths
4. **External dependencies are reachable** — APIs, services, storage
5. **Background jobs can run** — Workers have access to everything they need

**Common trap:** Database migrated, but files/volumes weren't. System looks healthy until something tries to access the missing files.

**Ask:** What in your system exists both in the database AND on the filesystem? Are both migrated?

---

## Alerting Strategy

### Questions to Ask

- Is this alert actionable at 3 AM?
- What's the difference between "needs attention" and "wake someone up"?
- How do you prevent alert fatigue?
- How do you know if alerting is broken?

### Alert Quality Checklist

- [ ] Alert has clear remediation steps
- [ ] Alert fires only when action is needed
- [ ] Alert includes enough context to diagnose
- [ ] Someone is responsible for responding

**Pattern:** If an alert fires and you snooze it, the alert is wrong.

**Ask:** How many alerts fired last week that required no action?

---

## Reporting

### Questions to Ask

- What trends matter for capacity planning?
- What would you want to know before a Monday morning?
- What metrics indicate system health vs. business health?

### Weekly Report Triggers

Consider including:
- Resource utilization trends (not just current values)
- Backup status and age
- Security summary (failed attempts, updates pending)
- Anything that changed unexpectedly

**Ask:** What would have prevented your last incident if you'd known it sooner?

---

## Automation Principles

### Script Structure Pattern

```bash
#!/bin/bash
set -e

# Configuration
APP_DIR="/opt/myapp"
LOG_FILE="/var/log/maintenance.log"

# Utility functions
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
alert() { log "ALERT: $1"; curl -X POST "$WEBHOOK_URL" -d "text=$1" 2>/dev/null || true; }

# Task functions (idempotent, can run multiple times safely)
task_backup() { log "Running backup"; pg_dump ... }
task_health_check() { log "Health check"; curl -sf "$HEALTH_URL" || alert "Health check failed"; }
task_vacuum() { log "Running vacuum"; psql -c "VACUUM ANALYZE;" ... }
task_report() { log "Generating report"; ... }

# Main dispatch
case "${1:-daily}" in
    daily)  task_backup; task_health_check ;;
    weekly) task_vacuum; task_report ;;
esac
```

### Principles

- **Idempotent:** Safe to run multiple times
- **Logged:** Know when it ran and what happened
- **Alerting:** Fail loudly, not silently
- **Documented:** Future you will forget why

**Ask:** Can you run this script twice safely?

---

## Cron Scheduling

### Pattern

| Time | Task | Rationale |
|------|------|-----------|
| Low traffic window | Daily maintenance | Minimize impact |
| After daily completes | Weekly maintenance | Build on daily |
| After weekly pattern | Monthly maintenance | Least frequent last |

### Checklist

- [ ] Absolute paths (cron has minimal PATH)
- [ ] Output redirected to logs
- [ ] Wrapper scripts for complex jobs
- [ ] Tested manually before scheduling

**Ask:** What happens if the cron job fails silently?

---

## Getting Started Checklist

Use this to audit your current maintenance:

- [ ] **Database:** Do you have scheduled maintenance? Is it sufficient?
- [ ] **Backups:** When did you last test a restore?
- [ ] **Health:** What's your minimum end-to-end health check?
- [ ] **Resources:** What will run out first? How will you know?
- [ ] **Security:** When was the last security update?
- [ ] **Certificates:** When do they expire? Who gets notified?
- [ ] **Alerts:** Are they actionable? Is there fatigue?
- [ ] **Reports:** What trends should you be watching?

---

## Red Flags

Signs your maintenance needs attention:

- "We'll deal with it when it becomes a problem"
- "The backup runs, but we've never tested restore"
- "Alerts fire so often we ignore them"
- "Disk filled up and we had to emergency clean"
- "We found out the certificate expired from users"
- "After migration, we discovered files were missing"

---

## Summary

**Maintenance is prevention.** The goal isn't to have impressive automation — it's to avoid 3 AM incidents.

Ask yourself:
1. What can fail silently in my system?
2. What would I want to know before it becomes urgent?
3. What did the last incident teach me about what to maintain?

Then automate the answers.

---

## Related Commands

- `/pb-observability` — Monitoring detects; maintenance prevents
- `/pb-sre-practices` — Toil reduction and operational health
- `/pb-incident` — Good maintenance reduces incident frequency
- `/pb-dr` — Disaster recovery (backups are foundation)
- `/pb-hardening` — Security hardening before deployment

---

*Good maintenance is invisible. You only notice its absence.*
