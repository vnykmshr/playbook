# Incident Response & Recovery

Respond to production incidents quickly and professionally. Clear process, clear communication, minimal impact.

---

## Purpose

Incidents are inevitable. What matters:
- **Speed**: Detect and respond quickly
- **Clarity**: Know exactly what's happening
- **Communication**: Keep stakeholders informed
- **Recovery**: Get back to normal fast
- **Learning**: Prevent repeats through post-incident review

---

## Incident Severity Levels

Classify incidents to determine response urgency and escalation.

### SEV-1 (Critical, Immediate Page)
- User-facing service completely down
- Data loss or data integrity risk
- Security breach active
- Major revenue impact

**Response time:** Immediate (< 5 minutes)
**Escalation:** Page on-call, VP, customers
**Communication:** Every 15 minutes
**Resolution target:** 1-2 hours

**Examples:**
- API servers offline, users can't access service
- Database corrupted, data cannot be retrieved
- Payment processing broken, no transactions processing
- Authentication system down, users locked out

### SEV-2 (High, Urgent Page)
- User-facing service degraded (slow, errors)
- Partial functionality broken
- Workaround exists but poor user experience

**Response time:** 15 minutes
**Escalation:** Page on-call + relevant team lead
**Communication:** Every 30 minutes
**Resolution target:** 4 hours

**Examples:**
- API responses 10x slower than normal
- Search feature broken (but users can browse)
- Emails not sending (but users can still order)
- Mobile app crashes on one action (desktop works)

### SEV-3 (Medium, No Page)
- Internal system degraded
- Non-critical feature broken
- User workaround available
- Limited customer impact

**Response time:** Next business day acceptable
**Escalation:** Slack to team, create ticket
**Communication:** Daily update
**Resolution target:** 1-2 days

**Examples:**
- Admin dashboard slow
- Reporting system down (business can continue)
- Non-critical background job failing
- One endpoint timeout (alternate exists)

### SEV-4 (Low, Future Fix)
- Documentation issue
- Minor UI bug
- Development environment broken
- No user-facing impact

**Response time:** Next sprint
**Escalation:** Create ticket, no escalation
**Communication:** Team awareness
**Resolution target:** When convenient

**Examples:**
- Typo in UI text
- Help docs incorrect
- Dev script broken
- Console warning (no functional impact)

---

## Incident Declaration

### Who declares incidents?

- **Anyone** can declare an incident (no permission needed)
- Don't wait for managers to approve
- Better to declare and cancel than miss critical issue
- When in doubt, declare

### How to declare

**For SEV-1/2:** Declare immediately
```
Slack: #incidents channel
Message: "@incident-commander SEV-1: Users report 503 errors on checkout"
Include: Service affected, symptoms, your name
```

**For SEV-3/4:** Create ticket
```
Jira/GitHub issue with label: incident
Title: [SEV-3] Admin dashboard slow
Include: What's broken, user impact, symptoms
```

### Incident Commander Role

Once incident declared:
1. **Incident Commander** assigned (first responder or on-call)
2. IC decides severity
3. IC starts bridge call for SEV-1/2
4. IC starts Slack thread tracking
5. IC coordinates investigation and communication

---

## On-Call Scheduling & Rotations

### Setting Up On-Call

Before incidents happen, establish clear on-call coverage.

**On-Call Rotation Structure:**

```
Primary On-Call: Responds immediately (paged on SEV-1/2)
  - Works day job normally
  - Paged within minutes of alert
  - Expected to join call within 5 minutes
  - High interrupt cost, use 1 week rotations

Secondary On-Call: Called if primary unavailable
  - Called if primary doesn't respond in 5 minutes
  - Escalation person for major incidents

Weekly Rotation:
  Monday-Friday: Primary + Secondary
  Weekends/Holidays: Same rotation or coverage plan
  Handoff: Friday 5pm (or end of week)
  Ramp-up: New person shadows for 1 week first
```

**Coverage Calculation:**

```
If incident rate is 2 per month:
  Average incident every 2 weeks
  Per person: ~1 incident per 12 weeks (manageable)

If incident rate is 2 per week:
  Per person: ~1 incident per 6 weeks (getting heavy)
  Need more people or reduce incident rate

If incident rate is 2 per day:
  Need dedicated on-call team (not part-time)
```

### On-Call Tools

**PagerDuty / Opsgenie (Recommended):**
```
1. Set up escalation policy
   - Primary on-call: page immediately
   - 5 min: if no ack, page secondary
   - 5 min: if no ack, page manager

2. Configure alert routing
   - SEV-1: Page on-call immediately
   - SEV-2: Page on-call immediately
   - SEV-3: Create ticket, no page

3. On-call calendar
   - Shows who's on-call
   - Enables time-off swaps
   - Mobile app for easy acknowledgment
```

**Simple Alternative (Google Calendar + Slack):**
```
1. Create calendar "On-Call"
   - Add weekly shifts (e.g., "John - Week of Jan 15")
   - Share with team

2. Set up Slack bot
   - "/whois-oncall" → Returns current on-call person
   - Bot pages person for SEV-1/2 (via SMS if needed)
   - Cheaper but less robust than PagerDuty
```

### On-Call Handoff

**Friday at 5pm (or end of shift):**
```
Outgoing on-call (John):
  - "Handing off to Sarah"
  - Update calendar/PagerDuty
  - Brief incoming on-call about ongoing work
  - Point to dashboard
  - Ensure Sarah has phone number
  - Confirm Sarah logged into monitoring

Incoming on-call (Sarah):
  - Acknowledge handoff
  - Check dashboard (no active incidents?)
  - Review logs from past week (recent issues?)
  - Ask John about recent incidents
  - Confirm phone is charged and alerts enabled
```

### On-Call Expectations

**What on-call should do:**

✅ **During on-call week:**
- Check phone for messages/alerts every 10 minutes
- Respond to SEV-1/2 pages within 5 minutes
- Acknowledge page (even if investigating)
- Work from location where you can join calls (home, not hiking)
- Sleep with phone nearby but on vibrate (not silent)

❌ **During on-call week (avoid):**
- Don't travel to areas without cell service
- Don't go to venues with restricted phones (movies, concerts)
- Don't drink heavily (need clear mind if paged)
- Don't schedule major meetings/presentations
- Don't ignore pages "just because it's Friday night"

**What the company should do:**

✅ **For on-call engineers:**
- Pay on-call stipend (e.g., $500/week extra)
- Give Friday afternoon flexible time off (if paged Thursday night)
- Limit to 1 week on-call per month if possible
- Provide on-call fatigue recovery (day off after heavy on-call)
- Recognize/thank on-call people (they trade social life)

❌ **Don't:**
- Expect on-call to work extra (they're on-call instead of coding)
- Schedule meetings during on-call week
- Ignore on-call fatigue (leads to burnout)
- Force people to be on-call against their will

### On-Call Rotation Schedule

**Example 4-person team (12 weeks per year on-call = 1 week/month):**

```
Jan:  John, Sarah, Mike, Lisa
      Week 1-4: John
      Week 5-8: Sarah
      Week 9-12: Mike
      Week 13-13: Lisa
      Week 1-52: Repeat

No person on-call twice in a row (unfair)
Everyone gets same amount (fair)
Predictable (plan vacation around it)
```

**Smaller team (2-3 people):**

```
Each person on-call 2 weeks per month (rotating)
More burden, but covers gaps
Pay higher on-call stipend

OR

Hire dedicated on-call person (if company large enough)
Dedicated role just responds to incidents
Reduces burden on engineers with day jobs
```

---

## Immediate Response (First 5 Minutes)

### IC Quick Triage

1. **Is it real?** (5 seconds)
   - Check monitoring: Is P99 latency actually up?
   - Check logs: Are errors really happening?
   - Avoid: Chasing false alarms from bad metrics

2. **What's affected?** (30 seconds)
   - Which services? endpoints? regions?
   - How many users impacted? percentage?
   - Is it spreading or stable?

3. **What changed recently?** (1 minute)
   - Was there a deployment? (check git log)
   - Configuration change? (check configs)
   - Traffic spike? (check metrics)
   - External dependency failure? (check upstreamhealth)

4. **Initial action** (2 minutes)
   - **If recent deployment:** Consider rollback immediately
   - **If configuration change:** Revert change
   - **If dependency down:** Switch to failover/degraded mode
   - **Otherwise:** Page relevant team for investigation

### Initial Communication (SEV-1/2)

Send to Slack #incidents:
```
@channel SEV-1: Checkout failing (503 errors)

Status: Investigating
Symptoms: POST /checkout returning 503 since 14:32 UTC
Affected: ~5% of transactions
Potential causes: Database slow? Payment API down? Recent deploy?

Updates every 15 minutes in thread.
```

---

## Investigation (5-30 Minutes)

### Investigation Team

- **Incident Commander:** Coordinates, owns timeline, communicates
- **Oncall Engineer:** Investigates service, runs commands
- **Subject Matter Expert:** Called if needed (database expert, payments, etc)

### Diagnostic Checklist

```
☐ Check recent deployments (git log --since="10 minutes ago")
☐ Check monitoring: latency, errors, resource usage
☐ Check logs: error messages, stack traces
☐ Check external dependencies: Are they healthy?
☐ Check database: Is it responsive? Any locks?
☐ Check traffic: Is there a sudden spike?
☐ Check configuration: Any recent changes?
☐ Check disk space: Are we full? Out of inodes?
```

### Root Cause Patterns

**Deployment-related (50% of incidents)**
- New code has bug
- Migration script failed
- Configuration not deployed
- Infrastructure change

Action: Rollback or hotfix

**Database-related (20% of incidents)**
- Slow query locking table
- Connection pool exhausted
- Disk full
- Replication lag

Action: Kill slow query, scale connections, free space

**Resource exhaustion (15% of incidents)**
- CPU 100%
- Memory full
- Disk full
- Network bandwidth full

Action: Identify process consuming, kill or scale

**External dependency (10% of incidents)**
- API provider down
- CDN down
- Payment processor down
- DNS down

Action: Use fallback, degrade gracefully, wait for recovery

**Configuration (5% of incidents)**
- Wrong environment variables
- SSL certificate expired
- Feature flag stuck on/off
- Rate limiting too aggressive

Action: Fix configuration, restart service

---

## Resolution (Immediate Actions)

### Recovery Strategies (In Order of Speed)

**1. Rollback (Fastest, if recent deploy)**
```bash
# If incident started after recent deployment
git log --oneline -5  # See recent deploys
git revert <commit-hash>  # Create revert commit
make deploy  # Deploy revert

# Rollback clears issue in minutes
# Then investigate what went wrong later
```

**2. Kill Slow Queries (If database slow)**
```sql
-- MySQL
SHOW PROCESSLIST;  -- See running queries
-- Find query taking > 30 seconds
KILL <process-id>;  -- Stop it

-- PostgreSQL
SELECT pid, query, state FROM pg_stat_activity WHERE state != 'idle';
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid != pg_backend_pid() AND query_start < now() - interval '30 seconds';
```

**3. Scale Horizontally (If resource maxed)**
```bash
# If CPU/memory at 100%
kubectl scale deployment api --replicas=10  # Add more instances
# or
aws autoscaling set-desired-capacity --desired-capacity 20

# Service recovers in 30-60 seconds as new instances start
```

**4. Degrade Gracefully (If dependency down)**
```
If payment processor down:
- Return 503 for checkout
- Queue orders for manual processing
- Users can try again in 5 minutes

If search service down:
- Disable search feature
- Show "Search temporarily unavailable"
- Users can browse without search

If cache down:
- Route around cache
- Use slower database directly
- Accept higher latency, avoid errors
```

**5. Feature Flag (If specific feature broken)**
```
If checkout broken but other features OK:
- Kill checkout feature flag
- Users see "Checkout under maintenance"
- Other site functions normally
- Buy time to fix checkout
```

**6. Configuration Fix (If config issue)**
```bash
# If environment variable wrong
kubectl set env deployment api ENV_VAR=correct_value
kubectl rollout restart deployment api

# or if config file
git commit -am "fix: correct environment variable"
make deploy
```

---

## Communication During Incident

### Rules for Communication

- **Honesty:** Tell truth about what's happening
- **Frequency:** Update every 15 min (SEV-1), 30 min (SEV-2)
- **Specificity:** Not "we're investigating" but "database queries slow, killing long-running query"
- **Clarity:** Avoid technical jargon, explain impact
- **No blame:** Never blame person, focus on recovery

### Communication Template

**Initial (First 2 min):**
```
SEV-1: Checkout down - 503 errors

What: POST /checkout returning 503 errors
When: Started 14:32 UTC (5 minutes ago)
Impact: ~5% of transactions failing (~$10k/hour)
Status: Investigating root cause
ETA: 15 minutes
```

**Update (Every 15 min during incident):**
```
UPDATE: Found root cause

Root cause: Payment API provider rate limiting us
Evidence: Logs show 429 responses from payment processor
Action: Increasing rate limit quota with provider
ETA: 10 minutes for fix, may need 5 min for orders to catch up
```

**Resolution (When fixed):**
```
RESOLVED: Checkout fully functional again

Root cause: Payment processor temporary rate limiting
Fix applied: Increased our rate limit quota
Time to fix: 27 minutes (14:32 to 14:59)
Impact: ~120 failed transactions (manual processing queued)
Action: Post-incident review scheduled for tomorrow 10am
```

### Notify Stakeholders

**Immediately (if SEV-1):**
- #incidents Slack channel
- @oncall
- VP Engineering
- Customer Success team

**Every 15 minutes:**
- Post update in #incidents thread
- If still ongoing, email major customers

**After 1 hour (if still ongoing):**
- Public status page update
- Email all customers
- If critical, call major customers

---

## Post-Incident Review

### Timing

- **SEV-1:** Review within 24 hours
- **SEV-2:** Review within 3 days
- **SEV-3/4:** Review optional, log lessons

### Review Participants

- Incident Commander
- Responders (who worked on incident)
- Service owner
- One person taking notes

### Review Structure (30 min meeting)

**1. Timeline (5 min)**
```
14:32 - Incident starts (checkout returns 503)
14:33 - Alert fires, IC pages on-call
14:35 - IC declares SEV-1
14:38 - Team identifies payment processor rate limiting
14:42 - Team increases rate limit quota
14:59 - Incident resolved, checkout working
```

**2. What Went Well (5 min)**
- Fast detection (1 minute)
- Clear communication
- Quick escalation
- Good teamwork

**3. What Could Improve (10 min)**
- Didn't have payment processor limits in runbook (add it)
- Took 7 minutes to investigate (could have suspected API faster)
- Didn't have direct contact for payment processor (get it)

**4. Action Items (10 min)**
```
☐ Add payment processor limits to runbook
☐ Get direct contact info for payment processor
☐ Add payment processor rate limits to monitoring alerts
☐ Consider circuit breaker for payment API
☐ Test failover to backup payment processor
```

---

## Common Incident Runbooks

### Incident: Database Slow

**Quick diagnosis (2 min):**
```sql
-- Show slow running queries
SHOW PROCESSLIST;  -- MySQL
-- or
SELECT pid, query, query_start FROM pg_stat_activity WHERE state != 'idle' ORDER BY query_start;  -- PostgreSQL

-- Show table locks
SHOW OPEN TABLES WHERE In_use > 0;  -- MySQL
```

**Immediate action:**
1. Identify query taking > 30 seconds
2. `KILL <process-id>` to stop it
3. Service recovers immediately

**Investigation:**
1. What query was slow? (check logs)
2. Is it a known slow query?
3. Missing index?
4. N+1 query pattern?
5. Should cache this result?

**Resolution:**
- Add index if missing
- Optimize query
- Add caching
- Scale database vertically

---

### Incident: API Server CPU 100%

**Quick diagnosis (1 min):**
```bash
# What process consuming CPU?
top -b -n 1 | head -20

# If Node/Python/Java process:
ps aux | grep node  # See how many processes

# Which endpoint consuming CPU?
curl http://localhost:9000/debug/cpu-profile  # if available
```

**Immediate action:**
1. Scale horizontally: Add more instances
2. Traffic redistributes to new instances
3. CPU returns to normal within 1 minute

**Investigation:**
1. What changed recently? (deployment?)
2. Is CPU spike legitimate?
3. Is there a memory leak? (check memory growing over time)
4. Is there a bad query? (database slow too?)
5. Is there infinite loop in code?

**Resolution:**
- Optimize code (cache, fewer DB queries)
- Increase instance size
- Scale more instances permanently
- Add monitoring for CPU spike

---

### Incident: Payment Processor Down

**Detection:**
- Checkout returns errors
- Logs show "Connection refused" to payment processor

**Immediate action:**
```
// Pseudo-code for graceful degradation
if (paymentProcessor.unavailable) {
  queueOrderForManualProcessing(order);
  return { success: false, reason: "Processing temporarily unavailable, please try again" };
}
```

**Communication:**
- Tell customers: "Orders temporarily queued, will process shortly"
- Give ETA (usually 30-60 minutes for processor recovery)

**Recovery:**
- If payment processor expected to recover soon (< 1 hour): Wait and communicate
- If expected long outage (> 1 hour): Activate backup processor if available

---

### Incident: Disk Full

**Quick diagnosis (1 min):**
```bash
df -h  # Show disk usage
# Look for 100% usage

du -sh /*  # Show which directory consuming space
# Usually /var/log if log files not rotated
```

**Immediate action:**
1. Find large log files: `ls -lh /var/log/*.log`
2. Compress old logs: `gzip /var/log/old.log`
3. Or delete if safe: `rm /var/log/debug.log*`
4. Restart service to free memory
5. Disk space now available

**Prevention:**
- Enable log rotation (logrotate)
- Monitor disk space
- Set alerts at 80% full
- Clean up old files regularly

---

## Incident Command Bridge Setup

### Before Incident: Prepare

- Slack #incidents channel exists
- On-call schedule configured (PagerDuty/etc)
- Runbooks documented (like above)
- Stakeholders know to watch #incidents
- Phone bridge number available if needed

### During Incident: IC Opens Bridge

```
1. IC posts to #incidents: "Starting investigation bridge"
2. IC starts Slack thread in #incidents
3. If SEV-1: Post phone bridge link
4. IC posts updates every 15 minutes
5. IC tracks timeline (start time, diagnosis, actions, resolution time)
```

### Bridge Rules

- One person talking at a time (IC manages)
- IC asks questions, delegates tasks
- Investigators report findings
- No blame, focus on recovery
- Keep bridge to 5 people max (core team)
- Post findings in Slack thread for others to see

---

## Escalation Paths

### Who to escalate to (and when)

**For database issues:**
- Page database on-call
- 5 min: If still investigating

**For infrastructure issues:**
- Page infrastructure on-call
- 5 min: If still investigating

**For unknown cause after 10 minutes:**
- Page service owner
- Call VP Engineering
- This means we're stumped, need leadership

**For external dependency issues:**
- If known contact: Call them
- Otherwise: Wait or use fallback
- Post-incident: Get direct contact numbers

---

## Integration with Playbook

**Part of deployment and reliability:**
- `/pb-guide` — Section 7 references incident readiness
- `/pb-observability` — Monitoring enables incident detection
- `/pb-release` — Release runbook includes incident contacts
- `/pb-adr` — Architecture decisions affect failure modes

**Related Commands:**
- `/pb-observability` — Set up monitoring to detect incidents
- `/pb-guide` — Section 8.2 (rollback plan)
- `/pb-release` — On-call contacts and escalation

---

## Incident Response Checklist

### Before Incidents Happen

- [ ] On-call schedule set up and published
- [ ] Incident commander role defined
- [ ] #incidents Slack channel created
- [ ] Runbooks written (database, CPU, payment, disk)
- [ ] Phone bridge number documented
- [ ] Customer support knows how to handle incident-related inquiries
- [ ] Post-incident review process defined
- [ ] Monitoring configured (see /pb-observability)

### During Incident

- [ ] Incident declared in #incidents within 2 minutes
- [ ] Severity level assigned (SEV-1/2/3/4)
- [ ] IC assigned and acknowledged
- [ ] Investigation started
- [ ] Communications every 15 minutes
- [ ] Root cause identified
- [ ] Action taken to recover
- [ ] Resolution time tracked

### After Incident

- [ ] Post-incident review scheduled (within 24 hours)
- [ ] Action items identified and assigned
- [ ] Runbook updated with new learnings
- [ ] Monitoring improved to detect earlier
- [ ] Prevention implemented if applicable
- [ ] All participants thanked

---

*Created: 2026-01-11 | Category: Deployment | Tier: S/M/L*

