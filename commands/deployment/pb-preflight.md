---
name: "pb-preflight"
title: "Pre-Ship Readiness Gate"
category: "deployment"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-ship', 'pb-security', 'pb-hardening', 'pb-deployment', 'pb-release']
last_reviewed: "2026-04-13"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial: 30-item pre-ship readiness gate for solo devs and small teams. Terse binary check, 5-10 min, distinct from /pb-security (depth audit) and /pb-ship (workflow orchestrator)."
breaking_changes: []
---
# Pre-Ship Readiness Gate

The 5-minute binary check before you deploy to production. Thirty bullets across six categories. If you cannot tick every box, you are not ready to ship.

**Resource Hint:** sonnet -- Gate execution, not deep audit. Invoke `/pb-security` or `/pb-hardening` when a bullet fails and you need depth.

---

## Mindset

Apply `/pb-preamble` thinking: challenge every "it should be fine." Apply `/pb-design-rules` thinking: fail noisily, distrust the happy path, verify instead of assume.

This is the gate, not the audit. It exists because the patch after launch costs more than the fix before launch, and because the hour before deploy is when assumptions turn into incidents. The checks are binary on purpose: either you verified it, or you did not.

---

## When to Use

- Immediately before a production deploy (solo or small team)
- Before flipping a feature flag for real users
- Before a release candidate becomes a release
- Any time "should we ship?" comes up without a clear answer

## When NOT to Use

- Mid-feature development -- use `/pb-review` and `/pb-cycle`
- Infrastructure hardening from scratch -- use `/pb-hardening`
- Deep security audit -- use `/pb-security`
- Post-incident recovery -- use `/pb-incident`

This gate assumes your code already passed review. It checks the seams between code-complete and production-serving.

---

## How to Run

1. Open this file. Read each bullet aloud.
2. For every bullet: either paste evidence (command output, link, screenshot, one sentence) or mark FAIL.
3. Do not skip. Do not mark "probably fine." Binary only: verified or not verified.
4. Any FAIL stops the deploy until resolved or explicitly accepted in writing by a named human.
5. Total time: 5-10 minutes once you know your stack. First run will take longer while you wire up the missing pieces.

---

## The Gate

### [1] Secrets & Authentication

- [ ] **No secrets in client bundles or git history.** Run a scanner (gitleaks, trufflehog, or equivalent) against the last 100 commits and the production build artifact. Zero findings or all findings triaged to false-positive.
- [ ] **HTTPS enforced, HTTP redirected, HSTS header set.** Test: `curl -I http://your-domain` returns 301 to https; `curl -I https://your-domain` shows `Strict-Transport-Security`.
- [ ] **CORS restricted to known origins.** Not `*`. Not reflected from the `Origin` header. Allow-list only.
- [ ] **Every private route checks authn AND authz.** Not just "user is logged in." Resource ownership verified per request. Tested with a second user account against a first user's resource ID.
- [ ] **Passwords hashed with bcrypt/argon2/scrypt.** Tokens expire. Logout invalidates server-side session (confirmed: logged-out token rejected on next request).

### [2] Data Integrity & Validation

- [ ] **Parameterized queries everywhere.** No string concatenation or template interpolation into SQL. ORM usage does not bypass via raw escapes.
- [ ] **App connects as a non-root DB user with least privilege.** Prod and dev databases fully separated: different hosts or different credentials, never a shared connection string.
- [ ] **Backups configured AND restore-tested within the last 30 days.** "Backups run nightly" is not a check. "I restored the Feb 14 snapshot into a scratch DB and queried it" is.
- [ ] **Migrations in version control.** Forward path tested on a copy of prod data. Reversible, or the irreversibility is documented and accepted.
- [ ] **Server-side input validation at every boundary.** Client validation is UX, not security. Validation runs even when the request comes from curl.

### [3] Infrastructure & Deployment

- [ ] **Prod env vars match the expected schema.** Not "present" -- matching. Diff against a checked-in template or schema. Missing optional vars flagged; typo'd keys caught.
- [ ] **SSL cert valid and auto-renewal proven.** Scheduled is not proven. The last renewal actually happened and the new cert is live.
- [ ] **Firewall exposes only required ports.** Internal services (DB, cache, queue) unreachable from the public internet -- verified from an external host, not assumed.
- [ ] **Process/container auto-restart verified.** Kill the main process; service returns in under 10 seconds. If this has never been tested, it does not work.
- [ ] **Rollback rehearsed end-to-end.** One person executed it once, start to finish, in under 5 minutes. Documented trigger criteria and the exact command.

### [4] Observability & Feedback

- [ ] **Error tracker receiving events from the production build.** Fire a test exception. See it appear in the dashboard within 60 seconds. Not "the SDK is installed."
- [ ] **Structured, searchable logs.** Log level at info or below in prod (no debug flood, no stdout garbage). Can query by request ID end-to-end.
- [ ] **Health endpoint returns 200 from public DNS.** Not localhost. Not the internal network. The address a real user hits. Include one dependency check, not just `return "ok"`.
- [ ] **Alerts wired for real failure modes.** Error rate spike, p99 latency, downtime, disk/memory threshold. At least one reachable human on the receiving end right now. Test-fire one alert.
- [ ] **Dependency audit clean on criticals.** `npm audit` / `pip-audit` / `go list -m -u all` / equivalent run within the last 7 days. No critical or high vulns unacknowledged.

### [5] Resilience & Limits

- [ ] **Graceful shutdown on SIGTERM.** In-flight requests drained before exit. Deploy does not drop connections mid-response.
- [ ] **Upstream timeouts set on every external call.** No infinite waits. No default HTTP-client timeouts (most are unlimited or absurdly high).
- [ ] **Rate limiting on auth, write, and expensive endpoints.** Protects against abuse AND against cost runaway (LLM calls, paid APIs, egress).
- [ ] **Disk, memory, and queue headroom above 20%.** No unbounded growth paths. Log rotation configured. Cache has a max size, not "until the box OOMs."
- [ ] **Circuit breaker or explicit fallback for every external dependency.** When the payment processor / auth provider / email service goes down, your app degrades; it does not freeze.

### [6] Launch Sanity

- [ ] **Post-deploy smoke test runs one real user journey against prod DNS.** Sign in, do the primary action, sign out. Not a ping. A journey.
- [ ] **Error rate watched for 15 minutes after the flip.** Rollback trigger criteria stated in advance: "rollback if 5xx rate exceeds X% over 5 minutes."
- [ ] **Admin and internal routes audited manually.** Assume they are not hidden. Authenticated as a non-admin user, try every admin URL you know. None respond with data.
- [ ] **File uploads validated server-side for type, size, and content.** Uploading a `.php` named `.jpg` does not get stored or executed. Max size enforced at the server, not just the client.
- [ ] **Someone read the app like an attacker.** Not you, if possible. Basic abuse tried: SQLi on a visible form, IDOR on a visible resource ID, auth bypass by stripping tokens, a second user accessing a first user's data.

---

## If a Bullet Fails

You have three options, in order of preference:

1. **Fix it.** Most of these are cheap once you know what is missing. The hour you spend now is the hour you do not spend at 2am.
2. **Escalate to depth.** Jump to the playbook that owns that layer:
   - Secrets, authn/z, data validation, input handling -> `/pb-security`
   - Infra, SSH, firewall, container lockdown, kernel -> `/pb-hardening`
   - Secret storage and rotation -> `/pb-secrets`
   - Observability and logging design -> `/pb-observability`, `/pb-logging`
   - Resilience patterns (circuit breakers, timeouts, bulkheads) -> `/pb-patterns-resilience`
   - Post-incident response -> `/pb-incident`
3. **Explicitly accept the risk in writing.** A named human signs off, the reason is documented in the deploy ticket or commit message, and a follow-up task exists with a date. "It is fine for now" is not acceptance; "X accepts the risk because Y, follow-up by Z date" is.

Skipping a bullet silently is not an option. The point of a gate is that it is binary.

---

## After the Deploy

The gate is not done at "deploy succeeded." It is done at "the thing works for real users and the dashboards stayed green."

1. Run the smoke test against prod DNS immediately after the flip.
2. Watch error rate, latency, and at least one business metric (signups, orders, checkouts, whatever the app does) for 15 minutes.
3. If any of them move the wrong way past your stated threshold, execute the rehearsed rollback. Do not debug live.
4. After 15 clean minutes, log the deploy outcome somewhere durable: commit SHA, time, smoke result, incidents if any. The next person to ship needs this.

---

## Scope Guard

**Do during /pb-preflight:**
- Verify each bullet with evidence, not recollection
- Block the deploy on any FAIL unless explicitly accepted
- Escalate to depth commands when a category keeps failing
- Log the outcome so the next deploy starts from a known state

**Do NOT during /pb-preflight:**
- Use this as a substitute for `/pb-security` or `/pb-hardening`. It is the gate, not the depth.
- Ship with "probably fine." That is how incidents start.
- Skip the post-deploy watch because the build went green. CI passing is not production working.
- Turn this into a ceremony. It is 5-10 minutes. If it is taking longer every time, your stack has drift -- fix the drift, not the gate.

---

## Related Commands

- `/pb-ship` -- The ship workflow this gate slots into
- `/pb-security` -- Depth audit when the secrets/authn/data category keeps failing
- `/pb-hardening` -- Infra depth when infrastructure checks keep failing
- `/pb-deployment` -- The deployment step itself, downstream of this gate
- `/pb-release` -- Versioning and release orchestration

---

*Cannot tick every box? You are not ready to ship. The patch after launch costs more than the fix before launch -- always.*
