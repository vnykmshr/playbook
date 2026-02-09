---
name: "pb-security"
title: "Security Review & Checklist"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review', 'pb-review-hygiene', 'pb-hardening', 'pb-secrets', 'pb-patterns-security']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Security Review & Checklist

Comprehensive security guidance for code review, design assessment, and pre-release validation. Use the checklist appropriate to your context: quick review, standard audit, or deep dive.

**Mindset:** Security review embodies `/pb-preamble` thinking (find what was missed, challenge safety assumptions) and `/pb-design-rules` thinking (especially Robustness and Transparency: systems should fail safely and be observable).

Your job is to surface risks and vulnerabilities. Reviewers should ask hard questions. Authors should welcome this scrutiny.

**Resource Hint:** opus — security review demands thorough analysis of attack surfaces, threat models, and vulnerability patterns

---

## When to Use This Command

- **Code review** — Checking PRs for security issues
- **Pre-release** — Security validation before shipping
- **Security audit** — Periodic comprehensive review
- **New authentication/authorization** — Changes to access control
- **Handling sensitive data** — PII, payments, credentials

---

## Overview

Security is not an afterthought. Integrate these checks into:
- **Code review** — Before merging to main
- **Design phase** — Architecture decisions
- **Pre-release** — Before shipping to production

Choose the checklist that fits your context:
- **Quick Checklist** — 5-10 minutes, S tier changes
- **Standard Checklist** — 20 minutes, M tier changes
- **Deep Dive** — 1+ hour, L tier changes, security-critical features

---

## Quick Security Checklist (5 minutes)

Use for small changes, bug fixes, single-file updates.

### Input & Validation
- [ ] All user inputs validated (never trust user input)
- [ ] No SQL injection (use parameterized queries)
- [ ] No XSS (output encoded, Content-Security-Policy set)
- [ ] No command injection (no shell eval, use APIs instead)

### Secrets & Configuration
- [ ] No secrets in code (no hardcoded passwords, API keys, tokens)
- [ ] Secrets in environment variables or secrets manager
- [ ] No secrets in git history (use git-secrets or similar)

### Authentication & Authorization
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks present (not just auth, but correct permissions)
- [ ] Session/token management secure

### Dependency Security
- [ ] No new dependencies with known vulnerabilities
- [ ] Dependencies from trusted sources (not random npm packages)

### Logging
- [ ] No sensitive data logged (no PII, passwords, tokens)
- [ ] Error messages don't leak information

---

## Standard Security Checklist (20 minutes)

Use for feature development, API changes, multi-file changes.

### Input Validation & Data Processing
- [ ] All user inputs validated and sanitized
- [ ] Input size limits enforced (prevent buffer overflow, DoS)
- [ ] File uploads restricted: extension allowlist, magic byte verification, content validation, size limits per type
- [ ] File upload bypasses considered: double extensions (`shell.jpg.php`), null bytes, MIME spoofing, polyglot files, SVG with JS, XXE via DOCX/XLSX, ZIP slip (`../` in archive paths)
- [ ] Uploaded files renamed (UUID), stored outside webroot, served with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`
- [ ] Data type validation (not just format, but values)
- [ ] Null/empty input handling
- [ ] SQL injection prevention (parameterized queries, ORMs)
- [ ] SQL edge cases: ORDER BY and table/column names cannot be parameterized — use allowlist
- [ ] NoSQL injection prevention (use proper query builders)
- [ ] Command injection prevention (no shell execution)
- [ ] Path traversal prevention (canonicalize path, validate against base directory, reject `..` and absolute paths)
- [ ] Deserialization safety (validate JSON/XML structure)
- [ ] XXE prevention: disable DTD processing, external entity resolution, and XInclude in all XML parsers

### Output Encoding & XSS Prevention
- [ ] HTML output properly encoded
- [ ] JavaScript output properly escaped
- [ ] URL parameters encoded
- [ ] CSS escaping where needed
- [ ] Content-Security-Policy headers configured
- [ ] No `innerHTML` with user input (use `textContent` or sanitize)
- [ ] Indirect input sources sanitized (URL fragments, WebSocket messages, postMessage, localStorage/sessionStorage values rendered in DOM)
- [ ] Often-overlooked vectors checked (error messages reflecting input, PDF/email generators with user data, SVG uploads, markdown rendering allowing HTML, admin log viewers)

### CSRF Prevention
- [ ] All state-changing endpoints protected (POST, PUT, PATCH, DELETE)
- [ ] CSRF tokens cryptographically random and tied to user session
- [ ] Missing token = rejected request (never skip validation when token is absent)
- [ ] SameSite cookie attribute set (`Strict` or `Lax`)
- [ ] Session cookies use `Secure` and `HttpOnly` flags
- [ ] JSON APIs also protected (Content-Type header alone does not prevent CSRF; validate Origin/Referer AND use tokens)
- [ ] Pre-auth endpoints covered (login, signup, password reset)
- [ ] Note: APIs using Authorization header with bearer tokens (not cookies) are inherently CSRF-immune — the browser does not attach the header automatically. CSRF tokens are unnecessary in this case.

### Open Redirect Prevention
- [ ] Redirect URLs validated against allowlist of trusted domains
- [ ] Or: only relative paths accepted (starts with `/`, no `//`)
- [ ] Common bypasses blocked: `@` symbol (`https://legit.com@evil.com`), protocol-relative (`//evil.com`), `javascript:` protocol, double URL encoding, backslash normalization
- [ ] For sensitive redirects: consider blocking non-ASCII domains (IDN homograph attacks)

### Authentication
- [ ] Authentication mechanism appropriate (basic auth not over HTTP, etc.)
- [ ] Passwords never logged or stored in plain text
- [ ] Password requirements reasonable (length, complexity)
- [ ] Failed login attempts rate-limited
- [ ] Multi-factor authentication available for sensitive operations
- [ ] Session timeout configured (15-30 min recommended)
- [ ] Session tokens invalidated on logout
- [ ] Token/session storage secure (secure HttpOnly cookies preferred)
- [ ] JWT-specific: algorithm validated server-side (`alg: none` rejected), secret/key appropriate for algorithm (HMAC vs RSA), tokens not stored in localStorage for web apps

### Authorization & Access Control
- [ ] Authorization checks at correct layer (server-side, not client)
- [ ] Principle of least privilege (minimum required permissions)
- [ ] All restricted endpoints protected
- [ ] Cross-tenant data isolation (if multi-tenant)
- [ ] Admin functions only accessible to admins
- [ ] API endpoints check user ownership before returning data (IDOR: verify requesting user has access to the specific resource ID)
- [ ] Mass assignment prevented: filter writable fields per operation, don't bind request body directly to models
- [ ] API responses don't expose internal model attributes (workflow states, processing flags, internal scores, admin metadata)
- [ ] Data layer models not serialized directly to API responses (use explicit response shapes)

### Secrets Management
- [ ] No hardcoded secrets (API keys, tokens, passwords)
- [ ] Secrets stored in secure location (AWS Secrets Manager, HashiCorp Vault, etc.)
- [ ] Secrets rotated regularly
- [ ] Service-to-service authentication uses temporary credentials
- [ ] Database credentials use principle of least privilege
- [ ] API keys scoped to minimum required permissions

### Cryptography
- [ ] Sensitive data encrypted in transit (HTTPS/TLS)
- [ ] Sensitive data encrypted at rest (database encryption, file encryption)
- [ ] Use strong algorithms (AES-256, SHA-256 minimum)
- [ ] No custom cryptography (use established libraries)
- [ ] Random values use cryptographically secure random (not Math.random())

### Error Handling
- [ ] Error messages don't leak sensitive information
- [ ] Stack traces not exposed to users
- [ ] Generic error message to user ("An error occurred") with code for logging
- [ ] Logging includes full error details for debugging
- [ ] Don't reveal information about the system (versions, paths, etc.)

### Logging & Monitoring
- [ ] No PII logged (names, emails, passwords, credit cards, etc.)
- [ ] Authentication/authorization events logged
- [ ] Failed login attempts logged and alerted
- [ ] Data access logged (who accessed what data)
- [ ] API key/token usage logged
- [ ] Suspicious activities logged (unusual patterns, rapid requests, etc.)

### Dependencies
- [ ] No known vulnerabilities in dependencies (`npm audit`, `safety check`)
- [ ] Dependencies from trusted sources
- [ ] Dependency versions locked (lock file committed)
- [ ] Dependency update process regular and tested
- [ ] Unused dependencies removed

### API Security
- [ ] HTTPS enforced (no HTTP)
- [ ] CORS configured correctly (not `*` for sensitive APIs)
- [ ] Rate limiting enforced
- [ ] API versioning (clear deprecation path)
- [ ] Request size limits
- [ ] Timeout limits on API calls
- [ ] API authentication (OAuth2, JWT, or API keys)

---

## Deep Dive Security Review (1+ hour)

Use for security-critical features, payment processing, authentication systems, data handling.

### Threat Modeling
- [ ] Threat model created (STRIDE, PASTA, or similar)
- [ ] High-risk data flows identified
- [ ] Attack surfaces enumerated
- [ ] Mitigation strategies documented

### Advanced Input Validation
- [ ] Unicode handling correct (no bypass with special characters)
- [ ] Regex validation doesn't have ReDoS (Regular Expression Denial of Service) vulnerability
- [ ] Input length limits enforce min/max (not just max)
- [ ] Whitelist validation where possible (only allow known good input)
- [ ] Special characters handled correctly
- [ ] Format validation (email, phone, dates) uses libraries, not custom regex
- [ ] Batch input size limits (prevent bulk operations DoS)

### Advanced Authentication
- [ ] Password hashing uses strong algorithm (bcrypt, argon2, scrypt)
- [ ] Password salt used and unique per user
- [ ] Account lockout after failed attempts
- [ ] Password reset flow secure (token expiration, one-time use)
- [ ] Email verification before account activation
- [ ] Session fixation prevention
- [ ] Brute force protection
- [ ] CAPTCHA or similar for login forms (if public)
- [ ] Consider passwordless auth (passkeys, magic links) for UX improvement

### Advanced Authorization
- [ ] Role-based access control (RBAC) or attribute-based (ABAC)
- [ ] Permission model documented
- [ ] Admin actions require additional verification
- [ ] Sensitive operations (delete, transfer, etc.) require confirmation
- [ ] Delegation of permissions possible and auditable
- [ ] Temporary elevated privileges possible (not permanent admin accounts)

### Security-Relevant Race Conditions
- [ ] Financial/transactional operations are atomic (double-spend, double-enrollment, coupon reuse)
- [ ] Check-then-act sequences use proper locking or database constraints (TOCTOU)
- [ ] Rate limiting checks are atomic (not vulnerable to race between check and increment)

### Data Protection
- [ ] PII identification complete (name, email, phone, SSN, IP, etc.)
- [ ] PII storage justified (do we actually need to store this?)
- [ ] PII encrypted in database
- [ ] PII encrypted in transit
- [ ] Data retention policy defined
- [ ] Data deletion process defined (not just flag as deleted)
- [ ] Database backups encrypted
- [ ] Backup restoration tested and documented
- [ ] Cross-tenant data isolation verified

### Advanced Cryptography
- [ ] Key management process documented
- [ ] Key rotation schedule established
- [ ] Key derivation uses proper KDF (not custom)
- [ ] Encryption authenticated (not just encrypted, use AEAD)
- [ ] IV/nonce handling correct (random, not reused)
- [ ] TLS version recent (1.2 or 1.3, not 1.0 or 1.1)
- [ ] Cipher suites strong (no weak algorithms)
- [ ] Certificate pinning considered for mobile apps

### Advanced API Security
- [ ] OAuth2/OIDC implementation correct (not homemade auth)
- [ ] CSRF prevention verified per Standard Checklist above
- [ ] Security headers configured (see Security Headers section below)
- [ ] API rate limiting per user and IP
- [ ] API request timeout configured

### Security Headers
- [ ] `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- [ ] `Content-Security-Policy` configured (avoid `unsafe-inline` and `unsafe-eval` for scripts)
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`)
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Cache-Control: no-store` on sensitive pages

### Infrastructure Security
- [ ] Network isolation (not all services accessible from everywhere)
- [ ] Firewall rules minimal (default deny)
- [ ] Database not directly accessible from internet
- [ ] Secrets not in environment (consider Secrets Manager)
- [ ] Container image scanning for vulnerabilities
- [ ] Container running as non-root
- [ ] Secret scanning in CI/CD pipeline

### Incident Response
- [ ] Logging sufficient for investigation
- [ ] Alerting on suspicious activities
- [ ] Incident response plan documented
- [ ] Communication plan for security incidents
- [ ] Forensics capability (log retention, audit trail)

### OWASP Top 10 (Application Security)

1. **Broken Access Control** — Verified authorization checks
2. **Cryptographic Failures** — Verified encryption and key management
3. **Injection** — Verified input validation and parameterized queries
4. **Insecure Design** — Threat modeling done, secure defaults
5. **Security Misconfiguration** — Production config reviewed, defaults changed
6. **Vulnerable Components** — Dependencies checked for vulnerabilities
7. **Authentication Failures** — Authentication mechanism secure
8. **Software & Data Integrity** — Dependencies from trusted sources, no tampering
9. **Logging & Monitoring Failures** — Logging sufficient and alerting configured
10. **SSRF** — Internal service discovery protected, not accessible from untrusted sources

---

## Language-Specific Guidance

### JavaScript/Node.js

**Common vulnerabilities:**
- `eval()`, `Function()` constructor — NEVER use with user input
- `innerHTML` with user input → Use DOMPurify or `textContent`
- Prototype pollution — Validate object keys
- Regex DoS — Use safe-regex or library validation

**Best practices:**
```javascript
// [NO] DANGEROUS
const result = eval(userInput);
element.innerHTML = userInput;
const obj = JSON.parse(userInput); // Trust JSON.parse, not the input

// [YES] SAFE
// Use libraries for evaluation
const safe = DOMPurify.sanitize(userInput);
element.textContent = userInput;  // Text is safe
const obj = JSON.parse(userInput); // Safe to parse
// Validate object keys
if (!allowedKeys.includes(key)) throw new Error('Invalid key');
```

**XXE**: If parsing XML, use libraries that disable DTD by default. With `libxmljs`: `{ noent: false, dtdload: false }`.

**Recommended packages:**
- `helmet` — Security headers middleware
- `express-rate-limit` — Rate limiting
- `bcryptjs` — Password hashing
- `jsonwebtoken` — JWT handling
- `dompurify` — HTML sanitization

### Python

**Common vulnerabilities:**
- `pickle.loads(userInput)` → Use JSON instead
- SQL string formatting — Use parameterized queries (SQLAlchemy)
- `exec()`, `eval()` with user input — NEVER
- File path concatenation → Use `pathlib`, not string concat

**Best practices:**
```python
# [NO] DANGEROUS
user_data = pickle.loads(request.data)  # Arbitrary code execution
query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection
exec(user_input)  # Arbitrary code execution

# [YES] SAFE
user_data = json.loads(request.data)  # Safe parsing
query = db.session.query(User).filter_by(id=user_id)  # SQLAlchemy ORM
# Execute only trusted code, not user input
```

**XXE**: Use `defusedxml` instead of stdlib `xml.etree`. With `lxml`: `etree.XMLParser(resolve_entities=False, no_network=True)`.

**Recommended packages:**
- `flask` — Web framework with security features
- `sqlalchemy` — ORM with parameterized queries
- `cryptography` — Encryption library
- `bcrypt` — Password hashing
- `pydantic` — Input validation and serialization
- `defusedxml` — Safe XML parsing

### Go

**Common vulnerabilities:**
- `sql.Query` with string concatenation → Use parameterized queries
- `exec.Command` with user input → Use array args, not shell
- Insecure deserialization → Validate before unmarshaling

**Best practices:**
```go
// [NO] DANGEROUS
query := fmt.Sprintf("SELECT * FROM users WHERE id = %d", userID)
cmd := exec.Command("sh", "-c", userInput)  // Shell injection
json.Unmarshal(data, &obj)  // No validation

// [YES] SAFE
db.QueryRow("SELECT * FROM users WHERE id = ?", userID)
cmd := exec.Command("program", args...)  // No shell
// Validate before unmarshaling
json.Unmarshal(data, &obj)
validator.Validate(obj)
```

**XXE**: Go's `encoding/xml` is safe by default (no external entity resolution). Verify third-party XML parsers disable DTD processing.

**Recommended packages:**
- `database/sql` — Parameterized queries
- `net/http` — Standard library routing (Go 1.22+ supports path parameters)
- `go-chi/chi` — Lightweight router (actively maintained)
- `golang-jwt/jwt` — JWT handling
- `golang.org/x/crypto` — Cryptography
- `github.com/asaskevich/govalidator` — Input validation

---

## Common Vulnerability Examples

### Example 1: SQL Injection

```python
# [NO] VULNERABLE
user_id = request.args.get('id')
query = f"SELECT * FROM users WHERE id = {user_id}"
results = db.execute(query)

# Attacker can pass: id=1 OR 1=1 (returns all users)

# [YES] SAFE
user_id = request.args.get('id')
results = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Or with ORM
results = User.query.filter_by(id=user_id).all()
```

### Example 2: XSS (Cross-Site Scripting)

```javascript
// [NO] VULNERABLE
const comment = getUserComment();
document.getElementById('comments').innerHTML = comment;
// If comment = "<img src=x onerror='alert(\"hacked\")'>"
// The script will execute

// [YES] SAFE
document.getElementById('comments').textContent = comment;
// Or sanitize
const clean = DOMPurify.sanitize(comment);
document.getElementById('comments').innerHTML = clean;
```

### Example 3: Hardcoded Secrets

```python
# [NO] VULNERABLE
API_KEY = "sk_live_abc123def456"  # In code, in git history

# [YES] SAFE
import os
API_KEY = os.environ.get('API_KEY')

# Or with secrets manager
import boto3
secrets = boto3.client('secretsmanager')
response = secrets.get_secret_value(SecretId='api-key')
API_KEY = response['SecretString']
```

### Example 4: Weak Password Hashing

```python
# [NO] VULNERABLE
import hashlib
password_hash = hashlib.sha256(password.encode()).hexdigest()

# [YES] SAFE
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Verification
bcrypt.checkpw(password.encode(), password_hash)
```

### Example 5: Command Injection

```bash
# [NO] VULNERABLE (Shell Injection)
filename = request.args.get('file')
os.system(f"cat {filename}")  # If filename = "file.txt; rm -rf /", disaster

# [YES] SAFE (No Shell Expansion)
import subprocess
filename = request.args.get('file')
result = subprocess.run(['cat', filename], capture_output=True)
# Args as list, no shell expansion
```

**Why**: Shell expands special characters (`|`, `;`, `$()`, etc.). Always use APIs that don't invoke shell.

### Example 6: Server-Side Request Forgery (SSRF)

```python
# [NO] VULNERABLE (No URL validation)
import requests
user_url = request.args.get('url')
data = requests.get(user_url).text  # Could fetch internal services
# Attacker passes: http://internal-api:8080/admin or http://localhost:6379

# [YES] SAFE (Allowlist + DNS validation)
import requests
import ipaddress
import socket
from urllib.parse import urlparse

user_url = request.args.get('url')
parsed = urlparse(user_url)

# Step 1: Scheme must be http/https
if parsed.scheme not in ('http', 'https'):
    raise ValueError("Invalid scheme")

# Step 2: Allowlist safe domains
ALLOWED_DOMAINS = ['example.com', 'api.example.com']
if parsed.hostname not in ALLOWED_DOMAINS:
    raise ValueError("Domain not allowed")

# Step 3: Resolve DNS and validate IP is not private
resolved_ip = socket.getaddrinfo(parsed.hostname, None)[0][4][0]
ip = ipaddress.ip_address(resolved_ip)
if ip.is_private or ip.is_loopback or ip.is_link_local:
    raise ValueError("Private/internal IPs not allowed")

# Step 4: Request using resolved IP (pin it, don't re-resolve)
data = requests.get(user_url, timeout=5).text
```

**Why**: Without validation, attacker can access internal services, cloud metadata APIs (AWS, GCP credentials), or local services.

**Common SSRF bypasses to block:**

| Bypass | Example |
|--------|---------|
| Decimal/octal/hex IP | `http://2130706433`, `http://0177.0.0.1`, `http://0x7f.0.0.1` |
| IPv6 localhost | `http://[::1]`, `http://[::ffff:127.0.0.1]` |
| Shortened IP | `http://127.1` |
| DNS rebinding | Attacker DNS returns internal IP on second resolution |
| Redirect chains | External URL 302s to internal address |

**Always**: resolve DNS before requesting, validate resolved IP is not private, pin resolved IP (don't re-resolve), block cloud metadata IPs (`169.254.169.254`) explicitly.

### Example 7: Unsafe Deserialization

```python
# [NO] VULNERABLE (Arbitrary code execution)
import pickle
user_data = pickle.loads(request.data)  # pickle can execute code during deserialization

# [NO] ALSO VULNERABLE (eval)
config_str = request.args.get('config')
config = eval(config_str)  # Arbitrary code execution

# [YES] SAFE (Use JSON only)
import json
user_data = json.loads(request.data)  # Safe parsing, no code execution
```

**Why**: `pickle` and `eval` can execute arbitrary code. JSON is data-only format, safe to deserialize untrusted input.

### Example 8: XXE (XML External Entity)

```xml
<!-- Malicious XML payload -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

**Prevention by language:**

```python
# Python — use defusedxml
from defusedxml import ElementTree
tree = ElementTree.parse(xml_file)  # Safe: external entities disabled

# Or with lxml
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)
```

```javascript
// Node.js — disable DTD in your XML library
// If using libxmljs: { noent: false, dtdload: false }
// Prefer libraries that disable DTD by default
```

```go
// Go — xml.Decoder is safe by default (no external entity resolution)
// If using third-party parsers, verify DTD processing is disabled
```

**Why**: XML parsers that resolve external entities can read local files, make network requests, or cause DoS. Disable DTD processing entirely when possible.

### Example 9: Open Redirect

```python
# [NO] VULNERABLE (no validation)
redirect_url = request.args.get('next')
return redirect(redirect_url)
# Attacker: ?next=https://evil.com (phishing via your domain)

# [YES] SAFE (allowlist)
from urllib.parse import urlparse

redirect_url = request.args.get('next', '/')
parsed = urlparse(redirect_url)

# Only allow relative paths
if parsed.netloc or parsed.scheme:
    redirect_url = '/'  # Fall back to safe default

return redirect(redirect_url)
```

**Why**: Open redirects enable phishing (victim trusts your domain in the URL) and can chain with SSRF or OAuth token theft.

---

## Compliance Framework Guidance

If you need to meet security compliance frameworks, here's what maps to this guide:

### PCI-DSS (Payment Card Data)
Focus on: Secrets management, encryption in transit/at rest, access control
Relevant sections: Cryptography, Secrets Management, Authorization & Access Control, API Security
Additional: Audit logging, data retention policies

### HIPAA (Healthcare Data)
Focus on: Encryption, access logs, data minimization
Relevant sections: Data Protection, Cryptography, Logging & Monitoring, Secrets Management
Additional: Audit controls, breach notification procedures

### SOC 2 (Service Organization Control)
Focus on: Security controls, access management, incident response
Relevant sections: All checklist sections apply
Additional: Evidence collection (audit logs, access reviews), incident response testing

### GDPR (Data Privacy - Europe)
Focus on: Consent, data minimization, user rights
Relevant sections: Data Protection, Input Validation, Error Handling
Additional: Privacy by design, user data export/deletion

**Action**: Use checklists above. For compliance frameworks, consult your legal/security team and audit frameworks for specific requirements.

---

## Resources

- **OWASP Top 10** — https://owasp.org/www-project-top-ten/
- **CWE Top 25** — https://cwe.mitre.org/top25/
- **NIST Cybersecurity Framework** — https://www.nist.gov/cyberframework/
- **Snyk Vulnerability Database** — https://snyk.io/vuln/
- **PortSwigger Web Security Academy** — https://portswigger.net/web-security/

---

## Integration with Playbook

**Part of review workflow:**
- `/pb-cycle` Step 1 — Self-review security checklist
- `/pb-review-hygiene` — Security section in code review
- `/pb-guide` §4.5 — Security design during planning
- `/pb-release` — Pre-release security checklist

---

## Related Commands

- `/pb-review` — Comprehensive multi-perspective review orchestrator
- `/pb-review-hygiene` — Code quality including security
- `/pb-hardening` — Infrastructure security (servers, containers, networks)
- `/pb-secrets` — Secrets management lifecycle
- `/pb-patterns-security` — Security patterns for microservices

---

*Created: 2026-01-11 | Category: Reviews | Last updated: 2026-02-03*
