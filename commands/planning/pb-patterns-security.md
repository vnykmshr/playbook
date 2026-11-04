---
name: "pb-patterns-security"
title: "Security Patterns & Microservice Security"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-security', 'pb-hardening', 'pb-patterns-core', 'pb-patterns-distributed']
last_reviewed: "2026-11-04"
version: "2.0.0"
version_notes: "v2.0.0: Cut from 785 to 216 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. OAuth code flow uses PKCE with S256 (RFC 9700); JWT verification pins the algorithm and rejects none (RFC 8725)."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Security Patterns & Microservice Security

## Overview

Security in microservices requires a multi-layered approach: authentication proves *who* you are, authorization proves *what* you can do, and data protection ensures information stays safe. Rather than bolting security on at the end, effective architectures embed security patterns throughout design.

This guide covers proven security patterns for microservices, showing when to use each and real-world trade-offs.

**Caveat:** Security patterns can add significant complexity. Use `/pb-preamble` thinking (challenge assumptions, surface trade-offs) and `/pb-design-rules` thinking (does this pattern serve Simplicity while maintaining Robustness?).

Question threat models. Challenge assumed attack surfaces. Surface the real risk vs. implementation cost trade-off. Don't add complexity without understanding the actual risk.

**Resource Hint:** sonnet - Security pattern reference; implementation-level authentication and authorization decisions.

---

## Authentication Patterns

Authentication answers: "Are you who you claim to be?"

### Pattern 1: OAuth 2.0 with Authorization Code Flow

**When to use**: Third-party integrations, user-facing APIs, token-based access

**How it works**:
1. User requests access to their data
2. App redirects to authorization server with a PKCE code challenge (S256)
3. User grants permission
4. Authorization server returns authorization code
5. App exchanges code and PKCE code verifier for access token (backend-to-backend)
6. App uses access token to call APIs

PKCE with S256 is MUST for public clients (SPAs, mobile, CLI) and RECOMMENDED for confidential clients (RFC 9700).

**Trade-offs**:
- ✅ Industry standard, well-supported
- ✅ Doesn't expose user password to application
- ✅ Easy delegation to third-party identity providers
- ❌ More complex than basic authentication
- ❌ Requires redirect flow (not suitable for server-to-server)

**Antipatterns**:
- ❌ Storing authorization codes indefinitely
- ❌ Sending access tokens through unsecured channels
- ❌ Not validating state parameter (CSRF vulnerability)
- ❌ Skipping PKCE: an intercepted authorization code becomes a token
- ❌ Storing user password instead of using OAuth

---

### Pattern 2: JWT (JSON Web Tokens) for API Authentication

**When to use**: Stateless API authentication, microservice-to-microservice, mobile apps

**How it works**:
1. Client authenticates with credentials
2. Server creates JWT (Header.Payload.Signature)
3. Client includes JWT in Authorization header for each request
4. Server validates signature to verify authenticity

**Trade-offs**:
- ✅ Stateless (no server session needed)
- ✅ Scalable across multiple servers
- ✅ Works well for APIs and microservices
- ❌ Token size larger than session cookies
- ❌ Can't revoke tokens immediately (use token blacklists for logout)

**Antipatterns**:
- ❌ Storing sensitive data in JWT (it's base64-encoded, not encrypted)
- ❌ Using weak secret keys
- ❌ Not validating expiration
- ❌ Taking `alg` from the token header: pin the algorithm on verify and reject `none` (RFC 8725)
- ❌ Storing JWT in local storage (use httpOnly cookies for web apps)

---

### Pattern 3: mTLS (Mutual TLS) for Service-to-Service Authentication

**When to use**: Internal microservice communication, service mesh, high-security requirements

**How it works**:
1. Both client and server present certificates
2. Both verify each other's certificates
3. TLS handshake establishes encrypted connection
4. Communication is authenticated and encrypted

**Trade-offs**:
- ✅ Strongest authentication (mutual verification)
- ✅ Encrypted in transit
- ✅ No shared secrets
- ❌ Certificate management overhead
- ❌ More complex to set up than API keys
- ❌ Performance cost of TLS handshake

---

## Authorization Patterns

Authorization answers: "What are you allowed to do?"

### Pattern 1: RBAC (Role-Based Access Control)

**When to use**: Most common authorization, clear role definitions

**How it works**: Users have roles, roles have permissions. Check if user's role has required permission.

**Trade-offs**:
- ✅ Simple and understandable
- ✅ Easy to implement
- ❌ Inflexible for fine-grained control
- ❌ Doesn't account for context (time, location, resource)

---

### Pattern 2: ABAC (Attribute-Based Access Control)

**When to use**: Fine-grained control, context-dependent access, complex business rules

**How it works**: Access decisions based on attributes of user, resource, action, and environment.

**Trade-offs**:
- ✅ Highly flexible
- ✅ Handles complex business logic
- ❌ Hard to understand and maintain
- ❌ Performance overhead of evaluation

---

## Secret Management Patterns

### Pattern 1: Encrypted Secret Vault

**When to use**: Production applications, sensitive credentials (API keys, database passwords)

**Trade-offs**:
- ✅ Centralized secret management
- ✅ Audit trail of secret access
- ✅ Rotation without app restart
- ❌ Additional infrastructure
- ❌ Single point of failure

---

## Data Protection Patterns

### Pattern 1: Encryption at Rest

**When to use**: Sensitive data in databases, file systems, backups

**Trade-offs**:
- ✅ Protects data at rest (database breaches)
- ✅ Compliance requirement (PCI-DSS, HIPAA, GDPR)
- ❌ Key management complexity
- ❌ Performance overhead (encrypt/decrypt on every access)

---

## Input Validation Pattern

### Validate All External Input

**When to use**: Every entry point (APIs, forms, file uploads, external systems)

---

## Common Security Antipatterns

❌ **Storing passwords in plaintext** - Always hash with bcrypt/scrypt
❌ **Logging sensitive data** - Never log passwords, tokens, PII
❌ **Hardcoding secrets** - Use vault or environment variables
❌ **SQL injection** - Use parameterized queries, never string concatenation
❌ **XSS vulnerabilities** - Always encode/escape output
❌ **Trusting client-side validation** - Always validate server-side
❌ **Weak TLS versions** - Use TLS 1.2+ minimum
❌ **Ignoring certificate expiration** - Monitor and rotate regularly

---

## When to Use Security Patterns

**Use these patterns when**:
- Building APIs with external users
- Handling sensitive data (PII, payments, health)
- Meeting compliance requirements (HIPAA, GDPR, PCI-DSS, SOC 2)
- Building multi-tenant systems
- Microservices with inter-service communication

**Don't over-engineer**:
- Internal tools with limited users: simple auth is fine

---

## Related Commands

- `/pb-security` - Security review checklist for code and infrastructure
- `/pb-hardening` - Security hardening reference for deployment configs
- `/pb-patterns-core` - Core architectural patterns including OWASP overview
- `/pb-patterns-distributed` - Distributed system patterns and service-to-service concerns

---

**Use these patterns as building blocks. Security is layered, not single-solution.**
