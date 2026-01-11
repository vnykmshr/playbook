# SDLC Templates & Quality Standards

Reusable templates for consistent implementation across all focus areas.

---

## Commit Strategy

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring (no functional change)
- `docs`: Documentation only
- `test`: Adding/updating tests
- `chore`: Build, config, tooling changes
- `perf`: Performance improvement

**Scope**: Service or component name (e.g., `identity`, `wallet`, `shared`, `user-app`)

**Examples**:
```
feat(identity): add user-admin paired account creation

- Create user_admin_pairs table migration
- Modify registration to create paired accounts
- Add pairing validation middleware

Closes #123
```

```
fix(wallet): handle NULL rejection_reason in KYC query

Use sql.NullString for nullable columns to prevent
silent scan failures.
```

### Commit Frequency

- **One logical change per commit**
- **Commit after each subtask** (not at end of phase)
- **Never commit broken code** to main branch
- **Squash WIP commits** before merge

---

## Self-Review Checklist

**See `/docs/checklists.md`** for comprehensive checklist with all sections.

Quick reference before requesting peer review:
- **Code Quality**: No hardcoded values, no dead code, naming, DRY, error messages
- **Security**: No secrets, input validation, parameterized queries, auth/authz, no sensitive logging
- **Testing**: Unit tests, integration tests, edge cases, error paths, all passing
- **Documentation**: Doc comments, complex logic explained, README, API docs
- **Database**: Reversible migrations, indexes, constraints, no breaking changes
- **Performance**: No N+1, pagination, timeouts, no unbounded loops

---

## Peer Review Checklist

**See `/docs/checklists.md`** for comprehensive peer review checklist.

Quick reference when reviewing:
- **Architecture**: Aligns with patterns, no unnecessary complexity, separation of concerns
- **Correctness**: Requirements met, edge cases handled, error handling, race conditions
- **Maintainability**: Readable, single-purpose functions, clear naming
- **Security**: No injection vulnerabilities, proper authorization, no info leakage
- **Tests**: Tests verify behavior, clear names, appropriate mocks, no flaky tests

---

## Quality Gates

### Gate 1: Pre-Implementation
Before writing code:
- [ ] Requirements are clear and documented
- [ ] Database schema designed and reviewed
- [ ] API contracts defined
- [ ] Edge cases identified

### Gate 2: Pre-Commit
Before committing:
- [ ] Code compiles without warnings
- [ ] All tests pass
- [ ] Linter passes (`golangci-lint run` / `npm run lint`)
- [ ] Self-review checklist complete

### Gate 3: Pre-Merge
Before merging to main:
- [ ] Peer review approved
- [ ] CI pipeline passes
- [ ] No merge conflicts
- [ ] Documentation updated

### Gate 4: Post-Merge
After merging:
- [ ] Verify deployment (if applicable)
- [ ] Smoke test critical paths
- [ ] Monitor logs for errors
- [ ] Update task tracker

---

## Phase Document Template

```markdown
# Phase X: [Phase Name]

## Objective
[One-sentence description of what this phase accomplishes]

## Prerequisites
- [ ] [Previous phase/dependency]
- [ ] [Required tooling/access]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

---

## Tasks

### Task X.1: [Task Name]

**Objective**: [What this task accomplishes]

**Implementation**:
1. [Step 1]
2. [Step 2]

**Files Changed**:
- `path/to/file.go` - [description]

**Tests**:
- [ ] [Test case 1]
- [ ] [Test case 2]

**Commit**: `type(scope): message`

---

## Database Migrations

### Migration: [name]

```sql
-- UP
[SQL]

-- DOWN
[SQL]
```

---

## Self-Review
- [ ] [Checklist item from template]

## Peer Review Requested
- Reviewer: [Name/Handle]
- Focus areas: [What to look at]

## Quality Gate: [Gate Name]
- [ ] [Gate criteria]
```

---

## User Role Matrix

Reference for permission design across all user types.

| Capability | Regular User | User-Admin | Super Admin |
|------------|--------------|------------|-------------|
| **Own Profile** | View, Edit | View (paired user) | View all |
| **Own Wallet** | Full access | View (paired) | View all |
| **Transfers** | Send (with limits) | View (paired) | View all, reverse |
| **Beneficiaries** | CRUD own | View (paired) | View all |
| **Verification** | Request | Approve (paired) | Override any |
| **KYC** | Submit own | View (paired) | Approve/reject all |
| **Transactions** | View own | View (paired) | Search all |
| **Users** | - | - | Full CRUD |
| **System Config** | - | - | Full access |
| **Simulation** | - | - | Full control |
| **Audit Logs** | - | - | View all |

### Permission Naming Convention

```
{service}:{resource}:{action}

Examples:
- identity:user:read
- identity:user:update
- wallet:wallet:transfer
- transaction:transaction:search
- verification:request:approve
- admin:simulation:configure
```

---

## API Response Standards

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-06T12:00:00Z"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-06T12:00:00Z"
  }
}
```

### Pagination Response

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

---

## Code Reuse Patterns

### Shared Utilities Location

```
shared/
├── errors/      # Error types and handling
├── logger/      # Structured logging
├── middleware/  # HTTP middleware (auth, CORS, etc.)
├── response/    # Response formatting
├── validator/   # Input validation
├── crypto/      # Cryptographic utilities
└── testutil/    # Test helpers
```

### When to Extract to Shared

Extract when:
- Used by 2+ services
- Generic enough to be service-agnostic
- Stable API (unlikely to change per-service)

Don't extract when:
- Service-specific logic
- Only used once
- Evolving rapidly

---

## Testing Standards

### Unit Test Naming

```go
func TestFunctionName_Scenario_ExpectedBehavior(t *testing.T)

// Examples:
func TestCreateUser_ValidInput_ReturnsUser(t *testing.T)
func TestCreateUser_DuplicateEmail_ReturnsConflictError(t *testing.T)
func TestTransfer_InsufficientBalance_ReturnsError(t *testing.T)
```

### Test File Organization

```
service/
├── handler.go
├── handler_test.go      # Unit tests
├── service.go
├── service_test.go
└── integration_test.go  # Integration tests (separate file)
```

### Mock vs Real Dependencies

- **Mock**: External services, databases in unit tests
- **Real**: Database in integration tests (use test containers)
- **Never mock**: The code under test itself

---

## Cleanup Checklist

Run periodically to reduce technical debt.

- [ ] Remove unused imports
- [ ] Remove unused functions/variables
- [ ] Consolidate duplicate code
- [ ] Update outdated comments
- [ ] Remove TODO comments (convert to issues)
- [ ] Update dependencies to latest stable
- [ ] Archive completed phase documents
