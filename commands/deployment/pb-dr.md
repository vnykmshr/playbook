# Disaster Recovery

Plan, test, and execute recovery from major system failures. When everything goes wrong, have a plan that works.

**Mindset:** Disaster recovery embodies `/pb-design-rules` thinking: Repair (fail noisily, recover quickly), Robustness (design for failure), and Least Surprise (recovery should work as documented). Use `/pb-preamble` thinking to challenge assumptions about what disasters are "unlikely."

The best time to plan for disaster is before it happens. The second best time is now.

---

## Quick Reference

| Term | Definition |
|------|------------|
| **RTO** | Recovery Time Objective — max acceptable downtime |
| **RPO** | Recovery Point Objective — max acceptable data loss |
| **Failover** | Switching to backup system |
| **Failback** | Returning to primary system |

---

## RTO/RPO Definitions

### Recovery Time Objective (RTO)

**RTO = How long can you be down?**

| RTO Target | Meaning | Example |
|------------|---------|---------|
| 0 (zero) | No downtime acceptable | Payment processing |
| < 1 hour | Critical system | Core API |
| < 4 hours | Important system | Admin dashboard |
| < 24 hours | Standard system | Reporting |
| < 1 week | Low priority | Development tools |

**Setting RTO:**
```
Questions to ask:
- What is the business impact per hour of downtime?
- Do we have SLA commitments?
- What is our reputation risk?
- What can we realistically achieve?
```

### Recovery Point Objective (RPO)

**RPO = How much data can you lose?**

| RPO Target | Meaning | Backup Strategy |
|------------|---------|-----------------|
| 0 (zero) | No data loss | Synchronous replication |
| < 1 minute | Near-zero | Streaming replication |
| < 1 hour | Minimal | Frequent snapshots |
| < 24 hours | Standard | Daily backups |
| < 1 week | Acceptable | Weekly backups |

**Setting RPO:**
```
Questions to ask:
- How much work would users lose?
- Can data be reconstructed from other sources?
- What is the regulatory requirement?
- What can we afford to backup?
```

### RTO/RPO Trade-offs

Lower RTO/RPO = Higher cost and complexity

```
Zero RTO + Zero RPO:
  - Active-active multi-region
  - Synchronous replication
  - Expensive, complex

1 hour RTO + 1 hour RPO:
  - Warm standby
  - Frequent async replication
  - Moderate cost

24 hour RTO + 24 hour RPO:
  - Cold standby
  - Daily backups
  - Low cost
```

**Document your targets:**
```markdown
## Service: Payment Processing
- RTO: 15 minutes
- RPO: 0 (zero data loss)
- Justification: Revenue impact, regulatory requirement
- Strategy: Active-passive with synchronous replication

## Service: Admin Dashboard
- RTO: 4 hours
- RPO: 1 hour
- Justification: Internal tool, can reconstruct recent changes
- Strategy: Backup restore from hourly snapshots
```

---

## Backup Strategies

### The 3-2-1 Rule

- **3** copies of data
- **2** different storage types
- **1** offsite location

```
Example:
  Copy 1: Production database (primary)
  Copy 2: Local replica (different disk)
  Copy 3: Cloud storage backup (different region/provider)
```

### Immutable Backups

Protect against ransomware and accidental deletion.

```bash
# AWS S3 with Object Lock
aws s3api put-object-lock-configuration \
  --bucket my-backups \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "GOVERNANCE",
        "Days": 30
      }
    }
  }'

# Objects cannot be deleted for 30 days
```

**Immutability options:**
- AWS S3 Object Lock
- Azure Immutable Blob Storage
- GCP Bucket Lock
- Air-gapped offline backups

### Backup Verification

**Backups that haven't been tested are not backups.**

```bash
# Monthly backup verification script
#!/bin/bash

echo "=== Backup Verification $(date) ==="

# 1. Download latest backup
aws s3 cp s3://backups/latest/db.sql.gz /tmp/restore-test/

# 2. Restore to test database
gunzip /tmp/restore-test/db.sql.gz
psql -h test-db -U admin -d restore_test < /tmp/restore-test/db.sql

# 3. Verify data integrity
EXPECTED_ROWS=1000000  # Known approximate count
ACTUAL_ROWS=$(psql -h test-db -U admin -d restore_test -t -A -c "SELECT COUNT(*) FROM users")

if [ "$ACTUAL_ROWS" -lt "$EXPECTED_ROWS" ]; then
  echo "ERROR: Row count mismatch. Expected ~$EXPECTED_ROWS, got $ACTUAL_ROWS"
  exit 1
fi

# 4. Verify application can connect
curl -f http://test-app/health || exit 1

echo "=== Backup verification PASSED ==="
```

**Verification schedule:**
- Daily: Automated integrity checks
- Weekly: Restore to test environment
- Monthly: Full recovery drill
- Quarterly: DR test (see below)

### Retention Policies

| Backup Type | Retention | Purpose |
|-------------|-----------|---------|
| Hourly | 24 hours | Point-in-time recovery |
| Daily | 30 days | Short-term recovery |
| Weekly | 3 months | Medium-term recovery |
| Monthly | 1 year | Long-term/compliance |
| Yearly | 7 years | Regulatory (varies) |

---

## Failover Procedures

### Manual Failover Steps

When automated failover isn't possible or appropriate:

```markdown
## Database Failover Runbook

### Pre-Conditions
- Primary database is unresponsive or corrupted
- Replica has current data (check replication lag)
- You have authority to initiate failover

### Steps

1. **Verify the problem (2 min)**
   - Is primary truly down? (not network issue)
   - What is replica lag? (acceptable data loss?)
   - Notify team in #incidents

2. **Stop writes to primary (1 min)**
   - Update application config to reject writes
   - Or: Block primary at network level

3. **Promote replica (5 min)**
   ```bash
   # PostgreSQL
   pg_ctl promote -D /var/lib/postgresql/data

   # Verify promotion
   psql -c "SELECT pg_is_in_recovery();"  # Should return 'f'
   ```

4. **Update application config (2 min)**
   - Point DATABASE_URL to new primary
   - Deploy config change

5. **Verify application (2 min)**
   - Check health endpoints
   - Verify writes working
   - Monitor error rates

6. **Communicate (ongoing)**
   - Update status page
   - Notify stakeholders

### Post-Failover
- [ ] Document what happened
- [ ] Schedule postmortem
- [ ] Plan failback (when original primary is repaired)
```

### Automated Failover

For zero/low RTO requirements:

```yaml
# Example: PostgreSQL with Patroni (automated failover)
# patroni.yml
scope: my-cluster
name: node1

restapi:
  listen: 0.0.0.0:8008

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # 1MB max lag for failover

postgresql:
  listen: 0.0.0.0:5432
  data_dir: /var/lib/postgresql/data
  parameters:
    synchronous_commit: "on"  # For zero data loss
```

**Automated failover considerations:**
- Test failover regularly (it will fail when you need it otherwise)
- Set appropriate lag thresholds
- Have manual override procedures
- Monitor failover events

### DNS-Based Failover

For simple active-passive setups:

```bash
# Health check fails → update DNS
# Using AWS Route 53 health checks

aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456 \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "db.example.com",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "10.0.2.100"}]
      }
    }]
  }'
```

**DNS failover considerations:**
- TTL affects failover time (lower TTL = faster failover, more DNS traffic)
- Clients may cache DNS beyond TTL
- Not suitable for zero-RTO requirements

---

## Recovery Testing

### Game Day Exercises

Controlled failure injection to test recovery.

**Game day template:**

```markdown
## Game Day: Database Failover Test

### Date: 2026-02-15
### Duration: 2 hours (10am - 12pm)
### Participants: SRE team, Database team, On-call engineer

### Objectives
- Verify automated failover works as documented
- Measure actual RTO
- Identify documentation gaps

### Scenario
Simulate primary database failure during normal traffic.

### Pre-Conditions
- Staging environment configured identically to production
- All participants briefed
- Rollback plan ready
- Status page prepared

### Steps
1. (T+0) Announce game day start
2. (T+5) Inject failure: Stop primary database
3. (T+5) Observe: Does automated failover trigger?
4. (T+10) Measure: Time to full recovery
5. (T+20) Verify: Application functioning correctly
6. (T+30) Restore: Bring original primary back
7. (T+45) Failback: Return to original configuration
8. (T+60) Debrief: What worked, what didn't

### Success Criteria
- RTO < 5 minutes (target: 2 minutes)
- RPO = 0 (synchronous replication)
- No customer-visible errors

### Actual Results
[Fill in after exercise]
- RTO achieved: ___
- RPO achieved: ___
- Issues discovered: ___
- Action items: ___
```

### Chaos Engineering (Lite)

Start simple before full chaos engineering:

**Level 1: Planned failures**
- Terminate a server during maintenance window
- Failover database on schedule
- Disconnect from external service

**Level 2: Automated small failures**
- Random pod termination (Kubernetes)
- Inject latency into service calls
- Simulate partial network failures

**Level 3: Full chaos engineering**
- Netflix Chaos Monkey style
- Production failures
- Requires mature observability and recovery

**Start with Level 1. Master each level before advancing.**

### Tabletop Exercises

Discussion-based DR testing without actual system changes.

```markdown
## Tabletop Exercise: Ransomware Attack

### Scenario
You arrive Monday morning. All production databases are encrypted.
Attackers demand 10 BTC. Last known good backup was Friday 6pm.

### Discussion Questions
1. Who do you notify first?
2. How do you verify backup integrity?
3. What is your recovery sequence?
4. How do you communicate with customers?
5. What is the estimated recovery time?
6. Do you pay the ransom? (Spoiler: No)

### Expected Outcomes
- Validate contact lists are current
- Identify gaps in backup strategy
- Practice decision-making under pressure
- Update runbooks based on discussion
```

---

## Data Recovery Workflows

### Database Point-in-Time Recovery

```bash
# PostgreSQL: Restore to specific timestamp
# Requires WAL archiving enabled

# 1. Stop application
sudo systemctl stop myapp

# 2. Create recovery configuration (PostgreSQL 12+)
# Note: recovery.conf was removed in PostgreSQL 12
cat >> /var/lib/postgresql/data/postgresql.conf << EOF
restore_command = 'cp /backup/wal/%f %p'
recovery_target_time = '2026-01-20 14:30:00'
recovery_target_action = 'promote'
EOF

# Create recovery signal file
touch /var/lib/postgresql/data/recovery.signal

# 3. Restore base backup
pg_basebackup -h backup-server -D /var/lib/postgresql/data-new

# 4. Start PostgreSQL (will replay WAL to target time)
sudo systemctl start postgresql

# 5. Verify data
psql -c "SELECT MAX(created_at) FROM transactions;"
```

### File System Recovery

```bash
# From snapshot (cloud provider)
aws ec2 create-volume \
  --snapshot-id snap-123456 \
  --availability-zone us-east-1a

# Mount and verify
sudo mount /dev/xvdf /mnt/recovery
ls -la /mnt/recovery/

# Or from backup
rsync -avz backup-server:/backups/2026-01-20/ /mnt/recovery/
```

### Application State Recovery

Some applications have state that needs recovery beyond database:

- **Session data**: May need to invalidate all sessions
- **Cache data**: Rebuild from source of truth
- **File uploads**: Restore from object storage backup
- **Search indexes**: Rebuild from database

**Recovery sequence matters:**
```
1. Database (source of truth)
2. File storage
3. Application servers
4. Cache/search indexes (rebuild)
5. CDN/edge cache (invalidate)
```

---

## Communication During Disaster

### Status Page Updates

**Update template:**

```markdown
## Incident: Database Outage

### [RESOLVED] 15:45 UTC
The database has been restored and all services are operational.
We are monitoring for any residual issues.

### [UPDATE] 15:30 UTC
Database restore in progress. Estimated completion: 15 minutes.

### [UPDATE] 15:00 UTC
We have identified the issue and are restoring from backup.
RTO estimate: 45 minutes.

### [INVESTIGATING] 14:30 UTC
We are experiencing database connectivity issues.
Some users may see errors. We are investigating.
```

**Communication cadence:**
- Initial: Within 10 minutes of detection
- Updates: Every 30 minutes (or on significant change)
- Resolution: When fully restored

### Stakeholder Communication

**Internal escalation:**
1. On-call engineer
2. Team lead
3. Engineering manager
4. VP Engineering (for major incidents)
5. CEO (for customer-facing outages > 1 hour)

**External communication:**
- Status page (all incidents)
- Email to affected customers (significant incidents)
- Social media (major outages)
- Press (if necessary)

### Communication Templates

**Customer email template:**

```
Subject: Service Disruption - [Service Name]

Dear Customer,

We experienced a service disruption affecting [specific impact]
between [start time] and [end time] UTC.

What happened:
[Brief, non-technical explanation]

What we're doing:
[Actions taken to prevent recurrence]

Impact to you:
[Specific impact, any data affected]

Next steps:
[Any action required from customer]

We apologize for the inconvenience and appreciate your patience.

[Your name]
[Company name]
```

---

## Post-Recovery Verification

After recovery, verify before declaring success:

### Verification Checklist

```markdown
## Post-Recovery Verification

### Data Integrity
- [ ] Row counts match expected values
- [ ] Recent transactions present
- [ ] No data corruption detected
- [ ] Referential integrity intact

### Application Function
- [ ] All health checks passing
- [ ] Authentication working
- [ ] Core user flows working
- [ ] Background jobs processing

### Performance
- [ ] Response times normal
- [ ] No error rate elevation
- [ ] Database query times normal
- [ ] No resource exhaustion

### Monitoring
- [ ] All alerts cleared
- [ ] Dashboards show normal
- [ ] Logs show no errors
- [ ] External monitors green

### Communication
- [ ] Status page updated
- [ ] Team notified
- [ ] Stakeholders updated
- [ ] Postmortem scheduled
```

---

## DR Plan Template

Every critical service needs a DR plan.

```markdown
# Disaster Recovery Plan: [Service Name]

## Overview
- Service: [Name]
- Owner: [Team]
- Last updated: [Date]
- Last tested: [Date]

## Recovery Objectives
- RTO: [X hours]
- RPO: [X hours]

## Backup Strategy
- Method: [Daily snapshot, continuous replication, etc.]
- Location: [Where backups stored]
- Retention: [How long kept]
- Verification: [How/when tested]

## Failure Scenarios

### Scenario 1: Database Failure
- Detection: [How we know]
- Response: [Steps to recover]
- Runbook: [Link]

### Scenario 2: Complete Region Failure
- Detection: [How we know]
- Response: [Steps to recover]
- Runbook: [Link]

### Scenario 3: Data Corruption
- Detection: [How we know]
- Response: [Steps to recover]
- Runbook: [Link]

## Recovery Procedures
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Contacts
- Primary: [Name, contact]
- Backup: [Name, contact]
- Escalation: [Name, contact]

## Dependencies
- [Service 1]: [Impact if unavailable]
- [Service 2]: [Impact if unavailable]

## Testing Schedule
- Monthly: Backup verification
- Quarterly: Failover test
- Annually: Full DR test
```

---

## Integration with Playbook

**Part of operational excellence:**
- `/pb-hardening` — Prevent disasters through security
- `/pb-secrets` — Protect credentials
- `/pb-sre-practices` — Sustainable operations
- `/pb-dr` — Recover when prevention fails (this command)
- `/pb-incident` — Respond during disasters

**DR testing cadence:**
```
Monthly: Backup verification
Quarterly: Failover testing (game day)
Annually: Full DR simulation
After changes: Verify DR still works
```

---

## Quick Reference

| Topic | Action |
|-------|--------|
| Set RTO/RPO | Document for each critical service |
| Verify backups | Monthly restore test |
| Test failover | Quarterly game day |
| Update DR plan | After any infrastructure change |
| Practice communication | Include in tabletop exercises |

---

## Related Commands

- `/pb-incident` — Respond to incidents during disaster scenarios
- `/pb-sre-practices` — Sustainable operations and toil reduction
- `/pb-database-ops` — Database backup and failover procedures
- `/pb-deployment` — Deploy recovery infrastructure

---

*Hope for the best, plan for the worst, test the plan.*
