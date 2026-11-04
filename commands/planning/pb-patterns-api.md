---
name: "pb-patterns-api"
title: "API Design Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-frontend', 'pb-security', 'pb-patterns-resilience', 'pb-patterns-async', 'pb-testing']
last_reviewed: "2026-11-04"
version: "2.0.0"
version_notes: "v2.0.0: Cut from 865 to 332 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. PATCH is not idempotent in general (RFC 5789); the breaking-change list names type, error-format and endpoint removals."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# API Design Patterns

Patterns for designing APIs that are consistent, intuitive, and maintainable. Covers REST, GraphQL, and RPC styles.

**Trade-offs exist:** API design is permanent once clients depend on it. Use `/pb-preamble` thinking (challenge assumptions about what clients need) and `/pb-design-rules` thinking (especially Clarity in naming, Least Surprise in behavior, and Extensibility for evolution).

Design for the consumer, not the implementation.

**Resource Hint:** sonnet - API pattern reference; implementation-level interface design decisions.

---

## API Style Decision

### When to Use Each Style

| Style | Best For | Avoid When |
|-------|----------|------------|
| **REST** | CRUD operations, resource-oriented systems, public APIs | Complex queries, real-time, tight coupling acceptable |
| **GraphQL** | Complex data requirements, multiple clients with different needs | Simple CRUD, strict caching needs, small team |
| **gRPC** | Service-to-service, high performance, streaming | Browser clients, public APIs, simple requests |

### Decision Framework

```
Is this a public API consumed by third parties?
├─ Yes → REST (widest compatibility, simplest tooling)
└─ No → Is performance critical (service-to-service)?
    ├─ Yes → gRPC (binary protocol, streaming)
    └─ No → Do clients have varied data needs?
        ├─ Yes → GraphQL (client-driven queries)
        └─ No → REST (simplest option)
```

---

## REST Patterns

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No* | No |
| DELETE | Remove resource | Yes | No |

*PATCH is not idempotent in general (RFC 5789); it is only when the patch document is (set a field, not increment one).

**Idempotent means:** Calling multiple times produces the same result as calling once.

### Status Codes

| Code | Meaning | Use When |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates resource |
| 204 | No Content | Successful DELETE, or PUT with no body |
| 400 | Bad Request | Invalid input, validation error |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource, version conflict |
| 422 | Unprocessable Entity | Validation failed (alternative to 400) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side failure |
| 503 | Service Unavailable | Temporary outage, maintenance |

### Response Design

API responses are contracts. What you return defines what consumers depend on. Returning your internal model directly is the "SELECT *" of API design - easy now, costly forever.

**The core discipline:** Separate your data layer from your API contract. Return what consumers need, not what the database has.

**Why this matters:**

| Concern | Risk of Returning Everything |
|---------|------------------------------|
| **Performance** | Large text fields, blobs, nested objects add latency and bandwidth cost - multiplied by every request, every user |
| **Security** | Internal attributes leak implementation details: workflow states, generation prompts, internal IDs, admin flags |
| **Coupling** | Consumers depend on your database schema shape; renaming a column breaks the API |
| **Clarity** | Consumer can't tell which fields are for them vs. internal bookkeeping |

#### Pattern: Response DTOs

Never serialize your data model directly. Define explicit response shapes per consumer need.

#### Field Selection Guidance

Ask these questions for every field in a response:

1. **Does the consumer need this?** If no, don't return it.
2. **Is this an internal implementation detail?** Workflow states, processing flags, internal IDs, embeddings - keep these server-side.
3. **Is this large?** Text blobs, HTML content, base64 data - return only in detail endpoints, not in list endpoints.
4. **Is this sensitive?** Even non-secret data can be sensitive in aggregate (usage patterns, internal scores, admin metadata).

#### List vs. Detail Responses

A common and effective pattern: return lean summaries in lists, full detail on individual fetch.

Don't return `description` and `lyrics` for 50 tracks in a list response when the UI shows titles and cover art.

#### Large Fields

For fields that are legitimately large (content bodies, transcripts, generated text):

- **Exclude from list endpoints** - Always
- **Consider lazy loading** - Separate endpoint or query parameter (`?fields=lyrics`)
- **Set size expectations** - Document max sizes in API docs
- **Compress** - Use gzip/brotli for text-heavy responses

#### When NOT to Optimize

This is not about premature optimization. It's about informed decisions:

- **Internal tools with 3 users** - Returning the full model is fine; don't build DTO layers for admin dashboards
- **Prototyping** - Ship fast, shape later. But track the debt.
- **Single consumer, small payloads** - If the response is 200 bytes, field selection adds complexity without benefit

The question isn't "always optimize" - it's "know what you're sending and why."

#### Design Rules Applied

- **Rule of Separation** - API contract is separate from data model
- **Rule of Clarity** - Response shape communicates what consumers should use
- **Rule of Repair** - Large unintended payloads should be noticed, not silently tolerated
- **Rule of Simplicity** - Don't build DTO layers where they aren't needed, but don't skip them where they are

### Input Binding Discipline

The inbound counterpart to Response Design: don't bind request bodies directly into your data model.

**Discipline:**
- **Allowlist writable fields per operation** - Create and update may accept different fields
- **Readonly fields are never writable** - `id`, `createdAt`, `role`, `internalScore` cannot be set via API
- **Validate types and constraints** - Don't just filter fields; validate values (use Pydantic, Zod, Go struct validation)

This is the mirror of Response Design: be explicit about what goes in, not just what comes out.

---

## Error Handling

### Error Response Standard

**Components:**
- `code` - Machine-readable error type (for client logic)
- `message` - Human-readable description (for debugging/display)
- `details` - Additional context (varies by error type)
- `requestId` - For support/debugging correlation
- `documentation` - Link to error documentation (optional)

---

## Pagination

### Cursor-Based (Recommended)

Best for real-time data, no "page drift" when items are added/removed:

**Cursor is opaque:** Client doesn't decode it, just passes it back.

### Offset-Based (Simple)

Easier to implement, allows jumping to pages:

**Problem:** "Page drift" when items added/removed during pagination.

### Keyset-Based

For sorted data with unique keys:

**Most efficient** for large datasets (uses index).

---

## Versioning

### URL Versioning (Recommended for REST)

**Pros:** Explicit, easy to route, cacheable
**Cons:** URL pollution, can't version individual endpoints

### Header Versioning

**Pros:** Clean URLs, per-request versioning
**Cons:** Hidden, harder to test, caching complexity

### Query Parameter

**Pros:** Explicit, easy to test
**Cons:** Pollutes query string, caching issues

### Versioning Strategy

1. **Avoid breaking changes** - Add fields. Breaking: removing or renaming a field, changing a field's type, changing the error format, removing an endpoint
2. **Deprecation period** - Warn before removing (6-12 months)
3. **Version when necessary** - Not every release needs a version bump

---

## Authentication

### API Key (Simple)

**Use for:** Server-to-server, simple integrations
**Don't use for:** User authentication, browser apps

### OAuth 2.0 (Third-party)

For "Login with Google" etc. See OAuth 2.0 spec for flows.

---

## Rate Limiting

### Rate Limit Strategies

| Strategy | Description |
|----------|-------------|
| Fixed window | X requests per minute/hour |
| Sliding window | X requests in rolling window |
| Token bucket | Burst allowed, refills over time |

---

## GraphQL Patterns

### Mutation Patterns

**Pattern:** Return both success data AND errors in payload.

### GraphQL Pitfalls

Common issues to avoid:

- **N+1 queries** - Use DataLoader for batching
- **Over-fetching in resolvers** - Fetch only requested fields
- **Schema complexity** - Start simple, evolve carefully
- **Missing error handling** - Return errors in payload, not HTTP errors

### GraphQL Security

- **Query depth limiting** - Without limits, nested queries (`{ user { friends { friends { ... } } } }`) exhaust the server. Set max depth (typically 7-10 levels).
- **Query complexity/cost analysis** - Assign cost to fields and reject queries exceeding a budget. Prevents expensive queries even within depth limits.
- **Disable introspection in production** - Introspection exposes every type, field, and relation. Enable only in development.
- **Batching limits** - GraphQL allows multiple operations per request. Without limits, an attacker sends thousands of mutations in one HTTP call, bypassing per-request rate limiting.
- **Field-level authorization** - In REST you protect endpoints; in GraphQL you must protect individual fields and nested resolvers. Authorization middleware must run per-field, not just per-query.

---

## Documentation

### Documentation Checklist

- [ ] All endpoints documented
- [ ] Request/response examples for each endpoint
- [ ] Error responses documented
- [ ] Authentication explained
- [ ] Rate limits documented
- [ ] Changelog maintained

---

## API Design Checklist

### Before Building

- [ ] Who are the consumers? (Frontend, mobile, third-party)
- [ ] What style fits? (REST, GraphQL, gRPC)
- [ ] What's the versioning strategy?
- [ ] What's the authentication method?
- [ ] What are the rate limits?

### During Design

- [ ] Resource names are nouns, plural
- [ ] HTTP methods used correctly
- [ ] Status codes are appropriate
- [ ] Error format is consistent
- [ ] Pagination strategy chosen
- [ ] Fields are named consistently (camelCase or snake_case, pick one)
- [ ] Response shapes are explicit (not serialized data models)
- [ ] No internal/backend-only attributes in responses (workflow states, embeddings, processing flags)
- [ ] List endpoints return lean summaries; detail endpoints return full data
- [ ] Large text fields excluded from collection responses

### Before Release

- [ ] Documentation complete
- [ ] Examples for all endpoints
- [ ] Error codes documented
- [ ] Rate limits communicated
- [ ] Breaking changes identified

---

## Related Commands

- `/pb-patterns-frontend` - Frontend data fetching patterns (client-side API consumption)
- `/pb-security` - API security patterns
- `/pb-patterns-resilience` - Resilience patterns (Circuit Breaker, Retry, Rate Limiting)
- `/pb-patterns-async` - Async API patterns
- `/pb-testing` - API contract testing

---

## Design Rules Applied

| Rule | Application |
|------|-------------|
| **Clarity** | Consistent naming, predictable behavior, response shapes communicate intent |
| **Least Surprise** | Standard HTTP methods and status codes |
| **Simplicity** | REST for simple needs, complexity only when justified |
| **Separation** | API contract decoupled from data layer; explicit DTOs over model serialization |
| **Extensibility** | Add fields without breaking, versioning strategy |
| **Robustness** | Clear error handling, rate limiting |
