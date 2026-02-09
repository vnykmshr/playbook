---
name: "pb-patterns-api"
title: "API Design Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-patterns-frontend', 'pb-security', 'pb-patterns-resilience', 'pb-patterns-async', 'pb-testing']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# API Design Patterns

Patterns for designing APIs that are consistent, intuitive, and maintainable. Covers REST, GraphQL, and RPC styles.

**Trade-offs exist:** API design is permanent once clients depend on it. Use `/pb-preamble` thinking (challenge assumptions about what clients need) and `/pb-design-rules` thinking (especially Clarity in naming, Least Surprise in behavior, and Extensibility for evolution).

Design for the consumer, not the implementation.

**Resource Hint:** sonnet — API pattern reference; implementation-level interface design decisions.

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

### Resource Naming

Resources are nouns, not verbs:

```
# [YES] Nouns
GET    /users
GET    /users/{id}
POST   /users
PUT    /users/{id}
DELETE /users/{id}

# [NO] Verbs
GET    /getUsers
POST   /createUser
POST   /deleteUser/{id}
```

**Plurals for collections:**

```
# [YES] Plural
/users
/users/{id}/orders

# [NO] Singular (inconsistent)
/user
/user/{id}/order
```

**Hierarchical relationships:**

```
# [YES] Nested resources
GET /users/{userId}/orders
GET /users/{userId}/orders/{orderId}

# [NO] Flat with query params for relationships
GET /orders?userId=123  (OK for filtering, not for hierarchy)
```

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | Yes* | No |
| DELETE | Remove resource | Yes | No |

*PATCH is idempotent if the same patch produces the same result.

**Idempotent means:** Calling multiple times produces the same result as calling once.

```
# Idempotent (safe to retry)
PUT /users/123 { "name": "Alice" }  # Always results in name = Alice

# Not idempotent (retry creates duplicates)
POST /users { "name": "Alice" }  # Creates new user each time
```

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

### Request/Response Format

**Consistent envelope:**

```json
// Success response
{
  "data": { /* resource or array */ },
  "meta": {
    "page": 1,
    "totalPages": 10,
    "totalCount": 100
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email"
      }
    ]
  }
}
```

**Alternatively, no envelope (simpler):**

```json
// Success: Just the data
{ "id": 1, "name": "Alice" }

// Success: Array
[{ "id": 1 }, { "id": 2 }]

// Error: Standard error object
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid email address"
}
```

Pick one style and be consistent.

### Response Design

API responses are contracts. What you return defines what consumers depend on. Returning your internal model directly is the "SELECT *" of API design — easy now, costly forever.

**The core discipline:** Separate your data layer from your API contract. Return what consumers need, not what the database has.

**Why this matters:**

| Concern | Risk of Returning Everything |
|---------|------------------------------|
| **Performance** | Large text fields, blobs, nested objects add latency and bandwidth cost — multiplied by every request, every user |
| **Security** | Internal attributes leak implementation details: workflow states, generation prompts, internal IDs, admin flags |
| **Coupling** | Consumers depend on your database schema shape; renaming a column breaks the API |
| **Clarity** | Consumer can't tell which fields are for them vs. internal bookkeeping |

#### Pattern: Response DTOs

Never serialize your data model directly. Define explicit response shapes per consumer need.

```python
# [NO] Data layer leaking through API
@app.get("/api/tracks/{id}")
def get_track(id):
    track = db.query(Track).get(id)
    return jsonify(track.to_dict())  # Everything: embeddings, prompts, workflow_state

# [YES] Explicit response shape
@app.get("/api/tracks/{id}")
def get_track(id):
    track = db.query(Track).get(id)
    return jsonify({
        "id": track.id,
        "title": track.title,
        "artist": track.artist,
        "duration": track.duration,
        "coverUrl": track.cover_url,
    })
```

```typescript
// [NO] Returning the database entity
app.get("/api/tracks/:id", async (req, res) => {
  const track = await db.track.findUnique({ where: { id: req.params.id } });
  res.json(track);  // Includes embeddingVector, generationPrompt, workflowState
});

// [YES] Explicit response type
interface TrackResponse {
  id: string;
  title: string;
  artist: string;
  duration: number;
  coverUrl: string;
}

app.get("/api/tracks/:id", async (req, res) => {
  const track = await db.track.findUnique({ where: { id: req.params.id } });
  const response: TrackResponse = {
    id: track.id,
    title: track.title,
    artist: track.artist,
    duration: track.duration,
    coverUrl: track.coverUrl,
  };
  res.json(response);
});
```

```go
// [NO] Struct tags expose everything
type Track struct {
    ID                 string `json:"id"`
    Title              string `json:"title"`
    EmbeddingVector    []float64 `json:"embedding_vector"`    // Internal
    GenerationPrompt   string    `json:"generation_prompt"`   // Internal
    WorkflowState      string    `json:"workflow_state"`      // Internal
}

// [YES] Separate response type
type TrackResponse struct {
    ID       string `json:"id"`
    Title    string `json:"title"`
    Artist   string `json:"artist"`
    Duration int    `json:"duration"`
    CoverURL string `json:"coverUrl"`
}
```

#### Field Selection Guidance

Ask these questions for every field in a response:

1. **Does the consumer need this?** If no, don't return it.
2. **Is this an internal implementation detail?** Workflow states, processing flags, internal IDs, embeddings — keep these server-side.
3. **Is this large?** Text blobs, HTML content, base64 data — return only in detail endpoints, not in list endpoints.
4. **Is this sensitive?** Even non-secret data can be sensitive in aggregate (usage patterns, internal scores, admin metadata).

#### List vs. Detail Responses

A common and effective pattern: return lean summaries in lists, full detail on individual fetch.

```
GET /api/tracks          → id, title, artist, duration, coverUrl
GET /api/tracks/{id}     → id, title, artist, duration, coverUrl, description, lyrics
```

Don't return `description` and `lyrics` for 50 tracks in a list response when the UI shows titles and cover art.

#### Large Fields

For fields that are legitimately large (content bodies, transcripts, generated text):

- **Exclude from list endpoints** — Always
- **Consider lazy loading** — Separate endpoint or query parameter (`?fields=lyrics`)
- **Set size expectations** — Document max sizes in API docs
- **Compress** — Use gzip/brotli for text-heavy responses

#### When NOT to Optimize

This is not about premature optimization. It's about informed decisions:

- **Internal tools with 3 users** — Returning the full model is fine; don't build DTO layers for admin dashboards
- **Prototyping** — Ship fast, shape later. But track the debt.
- **Single consumer, small payloads** — If the response is 200 bytes, field selection adds complexity without benefit

The question isn't "always optimize" — it's "know what you're sending and why."

#### Design Rules Applied

- **Rule of Separation** — API contract is separate from data model
- **Rule of Clarity** — Response shape communicates what consumers should use
- **Rule of Repair** — Large unintended payloads should be noticed, not silently tolerated
- **Rule of Simplicity** — Don't build DTO layers where they aren't needed, but don't skip them where they are

### Input Binding Discipline

The inbound counterpart to Response Design: don't bind request bodies directly into your data model.

**The problem:**

```python
# [NO] Mass assignment — attacker sends {"role": "admin", "name": "Alice"}
@app.put("/api/users/{id}")
def update_user(id):
    user = db.query(User).get(id)
    user.update(**request.json)  # Binds ALL fields, including role
    db.commit()

# [YES] Allowlisted fields per operation
UPDATABLE_FIELDS = {'name', 'email', 'bio'}

@app.put("/api/users/{id}")
def update_user(id):
    user = db.query(User).get(id)
    data = {k: v for k, v in request.json.items() if k in UPDATABLE_FIELDS}
    user.update(**data)
    db.commit()
```

**Discipline:**
- **Allowlist writable fields per operation** — Create and update may accept different fields
- **Readonly fields are never writable** — `id`, `createdAt`, `role`, `internalScore` cannot be set via API
- **Validate types and constraints** — Don't just filter fields; validate values (use Pydantic, Zod, Go struct validation)

This is the mirror of Response Design: be explicit about what goes in, not just what comes out.

---

## Error Handling

### Error Response Standard

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "details": {
      "resourceType": "user",
      "resourceId": "123"
    },
    "requestId": "req_abc123",
    "documentation": "https://api.example.com/docs/errors#RESOURCE_NOT_FOUND"
  }
}
```

**Components:**
- `code` — Machine-readable error type (for client logic)
- `message` — Human-readable description (for debugging/display)
- `details` — Additional context (varies by error type)
- `requestId` — For support/debugging correlation
- `documentation` — Link to error documentation (optional)

### Error Codes

Define a consistent error taxonomy:

```
# Authentication/Authorization
UNAUTHORIZED           # Not authenticated
FORBIDDEN              # Authenticated but not allowed
TOKEN_EXPIRED          # Auth token needs refresh

# Validation
VALIDATION_ERROR       # Input validation failed
MISSING_FIELD          # Required field not provided
INVALID_FORMAT         # Field format wrong

# Resources
RESOURCE_NOT_FOUND     # Requested resource doesn't exist
RESOURCE_CONFLICT      # Duplicate or version conflict
RESOURCE_GONE          # Resource was deleted

# Rate Limiting
RATE_LIMITED           # Too many requests
QUOTA_EXCEEDED         # Usage quota exceeded

# Server Errors
INTERNAL_ERROR         # Generic server error
SERVICE_UNAVAILABLE    # Temporary outage
```

### Client Error Handling

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);

  if (!response.ok) {
    const error = await response.json();

    switch (error.error.code) {
      case 'RESOURCE_NOT_FOUND':
        throw new UserNotFoundError(id);
      case 'UNAUTHORIZED':
        throw new AuthenticationError();
      case 'RATE_LIMITED':
        // Retry after delay
        await sleep(error.error.details.retryAfter);
        return fetchUser(id);
      default:
        throw new ApiError(error.error.message);
    }
  }

  return response.json();
}
```

---

## Pagination

### Cursor-Based (Recommended)

Best for real-time data, no "page drift" when items are added/removed:

```
GET /users?cursor=abc123&limit=20

Response:
{
  "data": [ ... ],
  "pagination": {
    "nextCursor": "def456",
    "prevCursor": "xyz789",
    "hasMore": true
  }
}
```

**Cursor is opaque:** Client doesn't decode it, just passes it back.

### Offset-Based (Simple)

Easier to implement, allows jumping to pages:

```
GET /users?page=2&limit=20
GET /users?offset=20&limit=20

Response:
{
  "data": [ ... ],
  "pagination": {
    "page": 2,
    "limit": 20,
    "totalPages": 10,
    "totalCount": 200
  }
}
```

**Problem:** "Page drift" when items added/removed during pagination.

### Keyset-Based

For sorted data with unique keys:

```
GET /users?after_id=123&limit=20

Response:
{
  "data": [ ... ],
  "pagination": {
    "lastId": 143
  }
}
```

**Most efficient** for large datasets (uses index).

---

## Versioning

### URL Versioning (Recommended for REST)

```
/v1/users
/v2/users
```

**Pros:** Explicit, easy to route, cacheable
**Cons:** URL pollution, can't version individual endpoints

### Header Versioning

```
GET /users
Accept: application/vnd.api+json; version=2
```

**Pros:** Clean URLs, per-request versioning
**Cons:** Hidden, harder to test, caching complexity

### Query Parameter

```
GET /users?version=2
```

**Pros:** Explicit, easy to test
**Cons:** Pollutes query string, caching issues

### Versioning Strategy

1. **Avoid breaking changes** — Add fields, don't remove or rename
2. **Deprecation period** — Warn before removing (6-12 months)
3. **Version when necessary** — Not every release needs a version bump

```
# Non-breaking (no version needed)
- Adding new optional field
- Adding new endpoint
- Adding new optional query param

# Breaking (needs version)
- Removing field
- Renaming field
- Changing field type
- Changing error format
- Removing endpoint
```

---

## Authentication

### API Key (Simple)

```
GET /api/users
Authorization: Bearer api_key_abc123

# Or header
X-API-Key: api_key_abc123
```

**Use for:** Server-to-server, simple integrations
**Don't use for:** User authentication, browser apps

### JWT (Token-based)

```
POST /auth/login
{ "email": "...", "password": "..." }

Response:
{
  "accessToken": "eyJ...",
  "refreshToken": "...",
  "expiresIn": 3600
}

# Subsequent requests
GET /api/users
Authorization: Bearer eyJ...
```

**Token refresh:**

```
POST /auth/refresh
{ "refreshToken": "..." }

Response:
{
  "accessToken": "eyJ...(new)...",
  "expiresIn": 3600
}
```

### OAuth 2.0 (Third-party)

For "Login with Google" etc. See OAuth 2.0 spec for flows.

---

## Rate Limiting

### Response Headers

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

### Rate Limited Response

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 100,
      "window": "1 minute",
      "retryAfter": 60
    }
  }
}
```

### Rate Limit Strategies

| Strategy | Description |
|----------|-------------|
| Fixed window | X requests per minute/hour |
| Sliding window | X requests in rolling window |
| Token bucket | Burst allowed, refills over time |

---

## GraphQL Patterns

### Schema Design

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  orders(first: Int, after: String): OrderConnection!
}

type Order {
  id: ID!
  total: Money!
  status: OrderStatus!
  items: [OrderItem!]!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

### Query Patterns

```graphql
# Good: Specific fields
query GetUserOrders($userId: ID!) {
  user(id: $userId) {
    name
    orders(first: 10) {
      edges {
        node {
          id
          total
        }
      }
    }
  }
}

# Bad: Over-fetching
query GetEverything($userId: ID!) {
  user(id: $userId) {
    ...AllUserFields
    orders {
      ...AllOrderFields
      items {
        ...AllItemFields
      }
    }
  }
}
```

### Mutation Patterns

```graphql
type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
  updateOrder(input: UpdateOrderInput!): UpdateOrderPayload!
  deleteOrder(id: ID!): DeleteOrderPayload!
}

input CreateOrderInput {
  userId: ID!
  items: [OrderItemInput!]!
}

type CreateOrderPayload {
  order: Order
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
}
```

**Pattern:** Return both success data AND errors in payload.

### GraphQL Pitfalls

Common issues to avoid:

- **N+1 queries** — Use DataLoader for batching
- **Over-fetching in resolvers** — Fetch only requested fields
- **Schema complexity** — Start simple, evolve carefully
- **Missing error handling** — Return errors in payload, not HTTP errors

### GraphQL Security

- **Query depth limiting** — Without limits, nested queries (`{ user { friends { friends { ... } } } }`) exhaust the server. Set max depth (typically 7-10 levels).
- **Query complexity/cost analysis** — Assign cost to fields and reject queries exceeding a budget. Prevents expensive queries even within depth limits.
- **Disable introspection in production** — Introspection exposes every type, field, and relation. Enable only in development.
- **Batching limits** — GraphQL allows multiple operations per request. Without limits, an attacker sends thousands of mutations in one HTTP call, bypassing per-request rate limiting.
- **Field-level authorization** — In REST you protect endpoints; in GraphQL you must protect individual fields and nested resolvers. Authorization middleware must run per-field, not just per-query.

**Future consideration:** For comprehensive GraphQL guidance (subscriptions, federation, caching, tooling), see `/pb-patterns-graphql` when available.

---

## Documentation

### OpenAPI (REST)

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        name:
          type: string
      required:
        - id
        - email
```

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

- `/pb-patterns-frontend` — Frontend data fetching patterns (client-side API consumption)
- `/pb-security` — API security patterns
- `/pb-patterns-resilience` — Resilience patterns (Circuit Breaker, Retry, Rate Limiting)
- `/pb-patterns-async` — Async API patterns
- `/pb-testing` — API contract testing

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

---

**Last Updated:** 2026-02-03
**Version:** 1.1
