---
name: "pb-threat-hunt"
title: "Security Threat Hunt: Deep Audit Methodology"
category: "reviews"
difficulty: "expert"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-security', 'pb-secrets', 'pb-hardening', 'pb-incident', 'pb-debug']
last_reviewed: "2026-07-02"
last_evolved: "2026-07-02"
version: "1.0.0"
version_notes: "v1.0.0: 12-step executable deep audit with adversarial payload catalog, severity rubric, and terminal DoD gate. Multi-language: Go default + Python/Node appendices."
breaking_changes: []
---
# Security Threat Hunt: Deep Audit Methodology

A 12-step executable security audit that treats every auth shortcut, redirect, token source, cookie, forwarded header, parser, cache, and cryptographic decision as a security boundary until proven otherwise. The default answer to "is this safe?" is "prove it." Not a checklist — a hunt.

**Mindset:** Apply `/pb-preamble` thinking (challenge every safety assumption) and `/pb-design-rules` thinking (fail noisily, distrust "one true way," recovery-oriented errors). The hunt is adversarial by design.

**Resource Hint:** opus — deep audit requires tracing decision paths end-to-end, evaluating cryptographic boundaries, and validating findings against exploit scenarios.

**Language:** This methodology targets **Go** projects by default. For Python equivalents, see **Appendix A**. For Node, see **Appendix B**. Language-agnostic steps (canonicalization, header trust, reporting) apply to all. Steps marked with `[Go]` need appendix translation.

---

## When to Use This Command

- **Deep security audit** — full methodology, every step executed
- **Pre-release security gate** — for L-tier changes touching auth, crypto, or input parsing
- **Post-incident review** — hunt the vulnerability class that caused the incident across the codebase
- **Dependency boundary audit** — when integrating a new auth provider, payment processor, or identity system

For quick pre-release checks, use `/pb-security`. This command is the deep pass.

---


## Severity Rubric

| Level | Criteria |
|-------|----------|
| **Critical** | Remote code execution, authentication bypass, credential exfiltration, privilege escalation to admin |
| **High** | Data exfiltration (non-credential), token forgery, SSRF to internal services, broken access control on sensitive data |
| **Medium** | Information disclosure (non-sensitive), open redirect, DoS with restart requirement, debug info leak |
| **Low** | Configuration weakness (no direct exploit), missing security headers (defense-in-depth), verbose error messages |
| **Info** | Hardening opportunity (no vulnerability), code pattern that could become exploitable with future changes |

---

## The Hunt

### Step 1: Scope the Hunt

Define what you are hunting and what is out of bounds.

**Run:**
- Identify the target: a codebase, a subsystem, a set of endpoints, or a dependency boundary
- List every external input point: HTTP parameters, headers, cookies, file uploads, API inputs, webhook payloads, environment variables
- Mark what is OUT of scope explicitly

**Exit:** Is the scope concrete enough that two independent hunters would search the same surface? Fails when scope is "the whole codebase" with no focus.

### Step 2: Map the Decision Path

For each critical input from Step 1, trace the decision path end-to-end. Do not stop at `grep`.

**Run:**
- For each input: trace input → validation → processing → decision → output
- Flag every point where a decision is made without explicit validation
- Document: what happens when validation fails? Does the code fail open or closed?

**Exit:** For every critical input, can you name the last function that makes a trust decision based on it? Fails when you have inputs with no traced path.

### Step 3: Targeted Search Passes `[Go]`

Run structured searches across the codebase. Each pattern targets a specific vulnerability class. Run all passes; skip none.

**Run — URL/Path:**
```bash
rg -n 'url\.Parse|path\.Join|filepath\.Join|path\.Clean|fmt\.Sprintf.*/%s|http\.Redirect'
```

**Run — Token/Cookie/Session:**
```bash
rg -n 'ParseWithClaims|jwt\.Sign|jwt\.NewWithClaims|jwt\.Parse|SetCookie|cookie\.Set|http\.Cookie'
```

**Run — Parsing/Deserialization:**
```bash
rg -n 'json\.Unmarshal|xml\.Unmarshal|gob\.NewDecoder|\.\(\w+\)|fmt\.Sscanf|strconv\.Atoi|strconv\.Parse|template\.Must'
```

**Run — Crypto:**
```bash
rg -n 'md5\.Sum|md5\.New|sha1\.Sum|sha1\.New|crypto/aes|crypto/rsa|ecdsa\.|hmac\.|rand\.Read|crypto/rand'
```

**Run — Concurrency/Race:**
```bash
rg -n 'go func|sync\.Mutex|sync\.RWMutex|sync\.Map|chan\b|sync\.Once|sync\.WaitGroup'
```

**Run — Dangerous Standard Library:**
```bash
rg -n 'exec\.Command|os/exec|net/http\.Get|reflect\.|unsafe\.'
```

**Exit:** Every search pass executed; every hit reviewed. Fails when a pass is skipped because "that won't find anything here."

### Step 4: URL/Path Canonicalization

Test every URL and path input with adversarial payloads. Path traversal and open redirect share a root cause: trust in canonical form.

**Run:** For each URL/path input, test with these payloads:

| # | Payload | Targets |
|---|---------|---------|
| 1 | `../../../etc/passwd` | Path traversal (dot-dot-slash) |
| 2 | `....//....//....//etc/passwd` | Path traversal (dot-dot encoding bypass) |
| 3 | `..%2f..%2f..%2fetc%2fpasswd` | Path traversal (URL-encoded) |
| 4 | `..%252f..%252f..%252f` | Path traversal (double URL-encoded) |
| 5 | `/etc/passwd` (absolute path) | Direct absolute path access |
| 6 | `file:///etc/passwd` | File scheme injection |
| 7 | `http://evil.com` (full URL) | Open redirect |
| 8 | `//evil.com` (protocol-relative) | Open redirect (protocol-relative) |
| 9 | `https:evil.com` (no slashes) | Open redirect (browser quirk) |
| 10 | `\/\/evil.com` (backslash variant) | Open redirect (backslash bypass) |
| 11 | `http://user:pass@evil.com` | Open redirect with credentials |
| 12 | `http://legit.com@evil.com` | Open redirect (userinfo confusion) |
| 13 | `http://localhost:6379` | SSRF to local services |
| 14 | `http://169.254.169.254/latest/meta-data/` | SSRF to cloud metadata |
| 15 | `http://[::1]:8080/admin` | SSRF via IPv6 localhost |

**Exit:** Every URL/path input tested against all 15 payloads. Fails when only `../` variants are tested (the first payload catches only the simplest cases).

### Step 5: Redirect and Header Trust

Verify that user-controlled headers and redirect targets are not trusted.

**Run:**
```bash
rg -n 'X-Forwarded-For|X-Real-IP|X-Forwarded-Host|X-Forwarded-Proto|Location.*http|Referer|Origin'
```

For each hit:
- Is the header value used in a security decision (IP allowlisting, rate limiting, auth check)?
- Is a user-controlled `Location` header or `redirect_uri` used without allowlist validation?
- Is `Referer` used for CSRF protection (it can be spoofed)?

**Exit:** Every header hit reviewed; every redirect target validated. Fails when forwarded headers are used for auth without explicit documentation of the trust boundary.

### Step 6: Token, Cookie, and Session Security

Audit token handling end-to-end: creation, storage, transmission, validation, revocation.

**Run:**
```bash
rg -n 'jwt\.Sign|jwt\.NewWithClaims|jwt\.Parse|jwt\.ParseWithClaims|SetCookie|cookie\.Set|session\.|csrf|SameSite'
```

For each hit:
- JWT: Is the algorithm pinned (`jwt.SigningMethodHS256`) or left to the token header? (Header-controlled algorithm enables algorithm confusion.)
- Cookie: Is `HttpOnly` set? `Secure`? `SameSite`?
- Session: Is the session ID cryptographically random? Is it regenerated on login?
- CSRF tokens: Are they per-session or per-request?

**Exit:** Every token/cookie hit reviewed. Fails when JWTs accept the algorithm from the token header rather than pinning it server-side.

### Step 7: Parser, DoS, and Panic Boundaries

Find parsing paths that can crash, hang, or leak.

**Run:**
```bash
rg -n 'io\.ReadAll|ioutil\.ReadAll|json\.NewDecoder.*Decode|xml\.NewDecoder.*Decode|template\.Execute|template\.Must|panic\(|recover\('
```

For each hit:
- Is there a body size limit before `io.ReadAll`? (No limit = memory exhaustion.)
- Is `json.NewDecoder(r).Decode(&v)` called without `http.MaxBytesReader`?
- Is `template.Execute` processing user-controlled template strings? (Server-side template injection.)
- Is `panic` used for expected errors? (Should be error returns, not panics.)
- In test/benchmark files only — safe to skip.

**Run (race detector):**
```bash
go test -race ./...
```

**Exit:** Every unbounded read flagged; every user-controlled template string verified. Fails when `io.ReadAll` is used without a size limit at a network boundary.

### Step 8: Provider and Crypto Boundaries

Audit cryptographic decisions at integration boundaries.

**Run (check for weak primitives):**
```bash
rg -n 'md5\.|sha1\.|DES|3DES|RC4|ECB|crypto/md5|golang\.org/x/crypto/md5'
```

**Per-protocol checklist:**

| Protocol | Check |
|----------|-------|
| OAuth 2.0 / OIDC | State parameter used and verified? PKCE for public clients? `redirect_uri` validated against allowlist? |
| SAML | Signature validation enforced? Assertion expiry checked? XML signature wrapping considered? |
| LDAP | Connection uses TLS? Bind credentials not hardcoded? Input sanitized for LDAP injection (`*`, `(`, `)`, `\`)? |
| KMS / Vault | Token stored in memory only? Rotation handled? Authentication at boundary, not deep in call chain? |
| Database | TLS for connections? Parameterized queries (not string formatting)? Connection string not hardcoded? |

**Exit:** Every protocol boundary checked. Fails when a provider integration is skipped because "that's a third-party library."

### Step 9: Concurrency and Cache Safety

Find data races, cache poisoning, and goroutine leaks.

**Run:**
```bash
rg -n 'sync\.Map\.|sync\.Mutex|sync\.RWMutex|\.Lock\(\)|\.Unlock\(\)|\.RLock\(\)|go func|chan\b|context\.WithCancel|context\.WithTimeout'
```

For each hit:
- Mutex: Is the unlock in a `defer`? (Early return without unlock = deadlock.)
- RWMutex: Are writes happening under `RLock`? (Read lock doesn't protect against concurrent writes.)
- Goroutine: Is there a cancel/context to stop it? (Goroutine without lifecycle = leak.)
- Channel: Is there a reader for every writer? (Unread channel send = goroutine leak.)
- Cache: Are cache keys derived from user input? (Cache poisoning.)

**Exit:** Every lock checked for defer-unlock; every goroutine checked for lifecycle. Fails when goroutines lack cancellation paths.

### Step 10: Validate Findings

Not every hit from Steps 3-9 is a vulnerability. Validate before reporting.

**6-state outcome:**

| Outcome | Criteria |
|---------|----------|
| **Confirmed** | Exploit path demonstrated end-to-end |
| **Likely** | Exploit path partially demonstrated; missing link plausible |
| **Possible** | Exploit path not demonstrated; evidence suggests risk |
| **Needs investigation** | Suspicious pattern; cannot confirm or rule out |
| **False positive** | Pattern is safe; verified by code-path analysis |
| **Unknown** | Insufficient information; requires domain expertise |

**Run:**
- For every Confirmed and Likely finding: write a one-sentence exploit scenario
- For every Possible and Needs Investigation: document what additional evidence would confirm or refute
- Downgrade or discard False Positives explicitly

**Exit:** Every finding classified into one of the 6 outcomes. Fails when "Confirmation" is just "I read the code and it looks suspicious."

### Step 11: Report Clearly

Structure each finding so a reviewer can understand the risk without redoing the hunt.

**Per-finding template:**

```
### [Severity] — [One-line title]

**Location:** [file:line]
**Input:** [what attacker controls]
**Decision path:** [input → validation → processing → sink]
**Exploit scenario:** [concrete inputs → wrong output/crash]
**Current mitigation:** [if any — why it's insufficient]
**Recommended fix:** [specific, at the nearest boundary]
```

**Exit:** Every Confirmed/Likely finding has all 7 fields. Fails when exploit scenarios are vague ("could lead to RCE").

### Step 12: Fix Conservatively

How you fix matters as much as what you find.

**Rules:**
- Normalize at the validation boundary, not deep in processing
- Fail closed — deny by default, allow explicitly
- Keep the patch near the boundary where the input enters
- Add a regression test that reproduces the exploit scenario before fixing
- Verify the fix passes the test AND the existing suite

**Exit:** Every fix has a regression test. Fails when the fix is "added validation" without a test that proves the old code was exploitable.

---

## Definition of Done

The hunt is not complete until ALL boxes are checked:

- [ ] Scope documented (what was hunted, what was out of bounds)
- [ ] All 6 search passes from Step 3 executed (no skipped passes)
- [ ] URL/path inputs tested against all 15 adversarial payloads from Step 4
- [ ] Every finding classified into one of 6 validation outcomes (Step 10)
- [ ] Every Confirmed and Likely finding has a concrete exploit scenario
- [ ] Every Confirmed finding has a fix with a regression test
- [ ] Report written with all 7 fields per finding for Confirmed/Likely
- [ ] Provider boundaries checked (each present in this project — OAuth, SAML, LDAP, KMS, DB)
- [ ] `go test -race ./...` passes (or explained if not run)

---

## Key Judgment Calls

- **Govulncheck stdlib findings** — report as release/toolchain notes. Do not recommend raising the `go` directive to clear scanner warnings.
- **Forwarded-IP trust** — this is a deployment assumption, not a library vulnerability. Flag if the code silently trusts it without documentation.
- **OAuth debug logging** — intentional admin diagnostics unless the data escapes outside debug level. Flag only if production log level exposes tokens or codes.
- **Test/benchmark panic patterns** — `panic` in `_test.go` or benchmark files is normal. Skip.
- **`unsafe` usage** — flag for review but do not auto-classify as a vulnerability. `unsafe` has legitimate uses (FFI, performance-critical paths). The question is whether it's exploitable from outside.

---

## Appendix A: Python Search Pass Equivalents

When hunting Python codebases, replace the Step 3 Go search passes with these:

**URL/Path:**
```bash
rg -n 'urllib\.parse|urlparse|urljoin|os\.path\.join|open\(.*user|redirect\(|flask\.redirect|django\.shortcuts\.redirect'
```

**Token/Cookie/Session:**
```bash
rg -n 'PyJWT\.|jwt\.encode|jwt\.decode|itsdangerous\.|flask\.session|django\.contrib\.sessions|set_cookie|response\.set_cookie'
```

**Parsing/Deserialization:**
```bash
rg -n 'pickle\.|\.loads\(|json\.loads|yaml\.load\b|yaml\.load_all|xml\.etree\.|defusedxml|lxml\.etree|eval\(|exec\('
```

**Crypto:**
```bash
rg -n 'hashlib\.md5|hashlib\.sha1|hashlib\.sha256|cryptography\.fernet|\.encrypt\(|\.decrypt\(|secrets\.|os\.urandom|random\.randint'
```

**Concurrency:**
```bash
rg -n 'asyncio\.create_task|asyncio\.gather|threading\.Thread|multiprocessing\.|concurrent\.futures|async def|await'
```

**Dangerous Standard Library:**
```bash
rg -n 'subprocess\.call|subprocess\.run|subprocess\.Popen|os\.system|os\.popen|exec\(|eval\(|compile\('
```

**Additional Python-specific passes:**

```bash
# Django ORM injection
rg -n '\.extra\(|RawSQL|\.raw\(|cursor\.execute.*%'

# Flask/Jinja2 template injection
rg -n 'render_template_string|Markup\(|\.from_string'
```

---

## Appendix B: Node.js/TypeScript Search Pass Equivalents

When hunting Node/TypeScript codebases, replace the Step 3 Go search passes with these:

**URL/Path:**
```bash
rg -n 'url\.parse|path\.join|path\.resolve|fs\.readFile|fs\.createReadStream|res\.redirect|\.sendFile'
```

**Token/Cookie/Session:**
```bash
rg -n 'jsonwebtoken|jwt\.sign|jwt\.verify|express-session|cookie-parser|res\.cookie|req\.cookies|csrf|csurf'
```

**Parsing/Deserialization:**
```bash
rg -n 'JSON\.parse|xml2js|fast-xml-parser|\.parse\(|eval\(|new Function\(|vm\.runInNewContext|vm\.Script'
```

**Crypto:**
```bash
rg -n 'crypto\.createHash|crypto\.createHmac|crypto\.randomBytes|crypto\.pbkdf2|bcrypt|argon2|md5|sha1'
```

**Concurrency/Promises:**
```bash
rg -n 'new Promise|Promise\.all|async function|await|process\.nextTick|setImmediate|worker_threads|cluster\.fork'
```

**Dangerous Standard Library:**
```bash
rg -n 'child_process\.exec|child_process\.spawn|child_process\.fork|exec\(|execSync.*user'
```

**Additional Node-specific passes:**

```bash
# Prototype pollution
rg -n '\.__proto__|\.constructor\.prototype|Object\.assign.*req\.body|merge\(.*req\.body|\.extend.*req\.body'

# NoSQL injection (MongoDB)
rg -n '\$where|\$regex.*req\.|\.find\({.*req\.'
```

---

## Report Path

Write findings to `todos/security/reports/{target}/threat-hunt-{YYYY-MM-DD}.md`.

---

## Related Commands

- `/pb-security` — Quick pre-release security checklist (run first; use this for deep follow-up)
- `/pb-secrets` — Secrets management lifecycle
- `/pb-hardening` — Infrastructure hardening (servers, containers, networks)
- `/pb-incident` — Incident response when a finding becomes an active threat
- `/pb-debug` — Tracing exploit paths through code

---

*12-step executable methodology. The hunt is not complete until all 9 DoD boxes are checked.*
