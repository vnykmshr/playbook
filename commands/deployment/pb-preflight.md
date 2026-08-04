---
name: "pb-preflight"
title: "Pre-Ship Readiness Gate"
category: "deployment"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-ship', 'pb-security', 'pb-hardening', 'pb-deployment', 'pb-release']
last_reviewed: "2026-08-04"
last_evolved: "2026-08-04"
version: "1.1.0"
version_notes: "v1.1.0: Step 0 Surface Assessment, and a third state. The 30 bullets describe a service you operate, which the command never said -- run against a static site or a docs corpus, 22 of 30 do not land, and a gate showing 22 irrelevant items is not filtered, it is abandoned. Step 0 picks a profile (Service = all 30; Static/Managed = a 9/12/9 partition of owned, delegated and out-of-surface) with a declare-and-justify escape hatch so the profile list never has to be exhaustive. Two profiles, not five orthogonal axes and not a 30-row tag matrix: the failure mode of a wrong tag is a gate that silently renders fewer items. The Static profile is transcribed from the v2.27.0 ship rather than invented. Binary becomes PASS / FAIL / DELEGATED(provider, verified-date), because a managed host terminating TLS is not the same fact as TLS not applying -- one has an owner you can name and a date you can check, the other stops the thinking. N/A is deleted as a writable outcome. Initial v1.0.0: 30-item gate for solo devs and small teams, distinct from /pb-security (depth audit) and /pb-ship (workflow orchestrator)."
breaking_changes: ['Bullets are numbered N.M and referenced by number', 'N/A is no longer a valid outcome -- a bullet is in your profile or it is not rendered']
---
# Pre-Ship Readiness Gate

The wiring check before you deploy to production: is the deploy path actually connected, not is the code good. Thirty bullets across six categories, **written for a service you operate**. Step 0 scopes them to what you are actually shipping. If you cannot rule on every bullet in your profile, you are not ready to ship.

**Resource Hint:** sonnet - Gate execution, not deep audit. Invoke `/pb-security` or `/pb-hardening` when a bullet fails and you need depth.

---

## Mindset

Apply `/pb-preamble` thinking: challenge every "it should be fine." Apply `/pb-design-rules` thinking: fail noisily, distrust the happy path, verify instead of assume.

This is the gate, not the audit. It exists because the patch after launch costs more than the fix before launch, and because the hour before deploy is when assumptions turn into incidents. Every check resolves to a fact you can point at: you verified it, you did not, or you can name who does it for you. There is no fourth answer, and "it does not apply here" is a Step 0 decision made once, not a per-bullet escape.

---

## When to Use

- Immediately before a production deploy (solo or small team)
- Before flipping a feature flag for real users
- Before a release candidate becomes a release
- Any time "should we ship?" comes up without a clear answer

## When NOT to Use

- Mid-feature development - use `/pb-review` and `/pb-cycle`
- Infrastructure hardening from scratch - use `/pb-hardening`
- Deep security audit - use `/pb-security`
- Post-incident recovery - use `/pb-incident`

This gate assumes your code already passed review. It checks the seams between code-complete and production-serving.

---

## Step 0: Surface Assessment

One question, asked once per project: **what are you shipping?**

| Profile | You are shipping | Gate |
|---|---|---|
| **Service** | A process you operate that serves requests -- API, web app, worker, anything with a runtime you restart | All 30 |
| **Static/Managed** | A build artifact served by a provider you do not operate -- static site, docs corpus, published pages | The partition below |

**Neither fits?** Do not force one. Write your deploy surface in a single sentence -- what runs, who operates it, what it touches -- then rule on all 30 against that sentence. Every out-of-surface call must name the clause that excludes it. A profile list that is not exhaustive is fine; a silent skip is not.

### The Static/Managed partition

Nine you own, twelve delegated, nine out of surface. Referenced by number against The Gate below, which is always printed in full.

- **You own (execute these):** 1.1 secrets in history · 2.3 a clean checkout rebuilds and redeploys the live site (this is the restore test) · 3.1 build and CI config match the expected schema · 3.5 rollback rehearsed · 4.3 the real public URL serves the new content · 4.5 dependency audit · 6.1 smoke test on a real page and a real link · 6.2 watched after the flip · 6.5 read like an attacker -- for a published corpus, what did you publish that you did not mean to
- **Delegated (name the provider and the date you last verified):** 1.2 · 3.2 · 3.3 · 3.4 · 4.1 · 4.2 · 4.4 · 5.1-5.5
- **Out of surface (no database, no sessions, no uploads):** 1.3 · 1.4 · 1.5 · 2.1 · 2.2 · 2.4 · 2.5 · 6.3 · 6.4

**Delegated is not a pass and it is not a skip.** A managed host terminating TLS is a different fact from TLS not applying: one has an owner you can name and a date you can check, the other stops the thinking. The day a provider changes a default is the day that distinction is the only thing standing between you and an outage nobody owns. A delegated bullet with **no named provider** is a FAIL.

---

## How to Run

1. Run Step 0 once. Record the profile in your deploy notes so the next run does not re-litigate it.
2. Read every bullet in the gate. Rule on each one in your profile.
3. Three outcomes, no fourth: **PASS** (paste evidence -- command output, link, one sentence), **FAIL**, or **DELEGATED** (name the provider and the date you last verified it). "Probably fine" is a FAIL. **N/A is not an outcome** -- a bullet is in your profile or it is not rendered.
4. Any FAIL stops the deploy until resolved or explicitly accepted in writing by a named human.
5. Total time: 5-10 minutes once you know your stack. First run will take longer while you wire up the missing pieces.

---

## The Gate

### [1] Secrets & Authentication

- [ ] **1.1 No secrets in client bundles or git history.** Run a scanner (gitleaks, trufflehog, or equivalent) against the last 100 commits and the production build artifact. Zero findings or all findings triaged to false-positive.
- [ ] **1.2 HTTPS enforced, HTTP redirected, HSTS header set.** Test: `curl -I http://your-domain` returns 301 to https; `curl -I https://your-domain` shows `Strict-Transport-Security`.
- [ ] **1.3 CORS restricted to known origins.** Not `*`. Not reflected from the `Origin` header. Allow-list only.
- [ ] **1.4 Every private route checks authn AND authz.** Not just "user is logged in." Resource ownership verified per request. Tested with a second user account against a first user's resource ID.
- [ ] **1.5 Passwords hashed with bcrypt/argon2/scrypt.** Tokens expire. Logout invalidates server-side session (confirmed: logged-out token rejected on next request).

### [2] Data Integrity & Validation

- [ ] **2.1 Parameterized queries everywhere.** No string concatenation or template interpolation into SQL. ORM usage does not bypass via raw escapes.
- [ ] **2.2 App connects as a non-root DB user with least privilege.** Prod and dev databases fully separated: different hosts or different credentials, never a shared connection string.
- [ ] **2.3 Backups configured AND restore-tested within the last 30 days.** "Backups run nightly" is not a check. "I restored the Feb 14 snapshot into a scratch DB and queried it" is.
- [ ] **2.4 Migrations in version control.** Forward path tested on a copy of prod data. Reversible, or the irreversibility is documented and accepted.
- [ ] **2.5 Server-side input validation at every boundary.** Client validation is UX, not security. Validation runs even when the request comes from curl.

### [3] Infrastructure & Deployment

- [ ] **3.1 Prod env vars match the expected schema.** Not "present" -- matching. Diff against a checked-in template or schema. Missing optional vars flagged; typo'd keys caught.
- [ ] **3.2 SSL cert valid and auto-renewal proven.** Scheduled is not proven. The last renewal actually happened and the new cert is live.
- [ ] **3.3 Firewall exposes only required ports.** Internal services (DB, cache, queue) unreachable from the public internet -- verified from an external host, not assumed.
- [ ] **3.4 Process/container auto-restart verified.** Kill the main process; service returns in under 10 seconds. If this has never been tested, it does not work.
- [ ] **3.5 Rollback rehearsed end-to-end.** One person executed it once, start to finish, in under 5 minutes. Documented trigger criteria and the exact command.

### [4] Observability & Feedback

- [ ] **4.1 Error tracker receiving events from the production build.** Fire a test exception. See it appear in the dashboard within 60 seconds. Not "the SDK is installed."
- [ ] **4.2 Structured, searchable logs.** Log level at info or below in prod (no debug flood, no stdout garbage). Can query by request ID end-to-end.
- [ ] **4.3 Health endpoint returns 200 from public DNS.** Not localhost. Not the internal network. The address a real user hits. Include one dependency check, not just `return "ok"`.
- [ ] **4.4 Alerts wired for real failure modes.** Error rate spike, p99 latency, downtime, disk/memory threshold. At least one reachable human on the receiving end right now. Test-fire one alert.
- [ ] **4.5 Dependency audit clean on criticals.** `npm audit` / `pip-audit` / `go list -m -u all` / equivalent run within the last 7 days. No critical or high vulns unacknowledged.

### [5] Resilience & Limits

- [ ] **5.1 Graceful shutdown on SIGTERM.** In-flight requests drained before exit. Deploy does not drop connections mid-response.
- [ ] **5.2 Upstream timeouts set on every external call.** No infinite waits. No default HTTP-client timeouts (most are unlimited or absurdly high).
- [ ] **5.3 Rate limiting on auth, write, and expensive endpoints.** Protects against abuse AND against cost runaway (LLM calls, paid APIs, egress).
- [ ] **5.4 Disk, memory, and queue headroom above 20%.** No unbounded growth paths. Log rotation configured. Cache has a max size, not "until the box OOMs."
- [ ] **5.5 Circuit breaker or explicit fallback for every external dependency.** When the payment processor / auth provider / email service goes down, your app degrades; it does not freeze.

### [6] Launch Sanity

- [ ] **6.1 Post-deploy smoke test runs one real user journey against prod DNS.** Sign in, do the primary action, sign out. Not a ping. A journey.
- [ ] **6.2 Error rate watched for 15 minutes after the flip.** Rollback trigger criteria stated in advance: "rollback if 5xx rate exceeds X% over 5 minutes."
- [ ] **6.3 Admin and internal routes audited manually.** Assume they are not hidden. Authenticated as a non-admin user, try every admin URL you know. None respond with data.
- [ ] **6.4 File uploads validated server-side for type, size, and content.** Uploading a `.php` named `.jpg` does not get stored or executed. Max size enforced at the server, not just the client.
- [ ] **6.5 Someone read the app like an attacker.** Not you, if possible. Basic abuse tried: SQLi on a visible form, IDOR on a visible resource ID, auth bypass by stripping tokens, a second user accessing a first user's data.

---

## If a Bullet Fails

First check you are not mislabelling a delegated bullet as a failure. If a provider owns it, name the provider and the date you last verified their behaviour -- that is a DELEGATED ruling, not a FAIL. If you cannot name the provider, it is a FAIL, and the fix is finding out who owns it.

For a real failure you have three options, in order of preference:

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
- Pick the profile once, in Step 0, and record it
- Verify each bullet with evidence, not recollection
- Name a provider and a date for every delegated bullet
- Block the deploy on any FAIL unless explicitly accepted
- Escalate to depth commands when a category keeps failing
- Log the outcome so the next deploy starts from a known state

**Do NOT during /pb-preflight:**
- Use this as a substitute for `/pb-security` or `/pb-hardening`. It is the gate, not the depth.
- Write N/A. It is not an outcome. Either Step 0 put the bullet out of surface, or you owe it a ruling.
- Treat delegated as done. A provider you cannot name is not a provider; it is an assumption with a logo.
- Ship with "probably fine." That is how incidents start.
- Skip the post-deploy watch because the build went green. CI passing is not production working.
- Turn this into a ceremony. It is 5-10 minutes. If it is taking longer every time, your stack has drift -- fix the drift, not the gate.
- Add a third profile speculatively. Two exist because two have been run; the escape hatch covers the rest until a real surface earns its own.

---

## Related Commands

- `/pb-ship` - The ship workflow this gate slots into
- `/pb-security` - Depth audit when the secrets/authn/data category keeps failing
- `/pb-hardening` - Infra depth when infrastructure checks keep failing
- `/pb-deployment` - The deployment step itself, downstream of this gate
- `/pb-release` - Versioning and release orchestration

---

*Cannot tick every box? You are not ready to ship. The patch after launch costs more than the fix before launch -- always.*
