# Node.js API - Development Guide

This guide walks through the development workflow for the Node.js User Management API using the Engineering Playbook commands and best practices.

## Setup

### Option 1: Docker (Recommended)

```bash
cd examples/node-api

# Start API and PostgreSQL together
make docker-up

# API runs on http://localhost:3000
# Database on localhost:5432

# Verify health
curl http://localhost:3000/health

# Stop when done
make docker-down
```

### Option 2: Local Development

```bash
# Install Node 20+
node --version  # Should be v20.x or higher

# Install dependencies
make install

# Start development server (with hot reload)
make dev

# API runs on http://localhost:3000
```

For local development, you'll need PostgreSQL running separately:
```bash
# Option A: Use Docker Compose with only PostgreSQL
docker-compose up postgres

# Option B: PostgreSQL installed locally
psql postgres://postgres:postgres@localhost:5432/playbook_db
```

## Development Workflow

This project follows the `/pb-cycle` pattern: **Develop → Test → Commit → Repeat**

### 1. Create Feature Branch

```bash
git checkout -b feature/user-profiles-endpoint main
# Or use /pb-start
```

### 2. Make Changes

```bash
# Edit src/main.ts or tests/api.test.ts
vim src/main.ts

# Run development server with auto-reload
make dev

# Test in another terminal
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
```

### 3. Run Tests

```bash
# Run all tests
make test

# Run in watch mode (re-run on file changes)
make test-watch

# Generate coverage report
make test-coverage
```

### 4. Code Quality

```bash
# Check for issues
make lint

# Fix automatically where possible
make lint-fix

# Format code
make format

# Type check
make typecheck

# All at once
make lint-fix && make format && make typecheck
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: add user profiles endpoint

- Add GET /users/:id/posts endpoint
- Fetch user posts from database
- Add error handling for missing users"

# Or use /pb-commit for guided commit
```

### 6. Repeat

Push and create PR:
```bash
git push origin feature/user-profiles-endpoint
# Then use /pb-pr
```

## Common Tasks

### Add a New Endpoint

1. **Define the route handler in `src/main.ts`:**

```typescript
// GET /users/:id/posts
app.get('/users/:id/posts', async (req, res, next) => {
  try {
    const { id } = req.params;
    const result = await pool.query(
      'SELECT * FROM posts WHERE user_id = $1',
      [id]
    );
    res.json(result.rows);
  } catch (err) {
    next(err);
  }
});
```

2. **Add tests in `tests/api.test.ts`:**

```typescript
describe('GET /users/:id/posts', () => {
  it('should return user posts', async () => {
    const response = await request(app)
      .get('/users/1/posts');

    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);
  });

  it('should return 404 for non-existent user', async () => {
    const response = await request(app)
      .get('/users/999/posts');

    expect(response.status).toBe(404);
  });
});
```

3. **Test locally:**

```bash
make dev          # Terminal 1
make test-watch   # Terminal 2
```

### Modify Database Schema

1. **Update the schema in `src/main.ts`:**

```typescript
// In the init() function
const schema = `
  CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
  );

  CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
  );
`;
```

2. **Restart the development server:**

```bash
# Ctrl+C to stop
# make dev to restart
```

The schema is created on startup with `CREATE TABLE IF NOT EXISTS`, so it's safe to restart multiple times.

### Run Specific Tests

```bash
# Run a single test file
npm test tests/api.test.ts

# Run tests matching a pattern
npm test -- --testNamePattern="POST /users"

# Run in watch mode
make test-watch
```

### Debug Issues

**TypeScript Errors:**
```bash
# Full type check with detailed errors
make typecheck

# Or during development
npm run typecheck
```

**Lint Errors:**
```bash
# See all issues
make lint

# Fix automatically
make lint-fix
```

**Database Errors:**
```bash
# Check database is running (Docker)
docker-compose ps

# View database logs
docker-compose logs postgres

# Connect to database
docker exec -it playbook_node_db psql -U postgres -d playbook_db

# Common queries
SELECT * FROM users;
SELECT * FROM users WHERE email = 'alice@example.com';
DROP TABLE users;  -- Reset if needed
```

**Port Already in Use:**
```bash
# Use different port
PORT=3001 make dev

# Or kill the process
lsof -ti:3000 | xargs kill -9
```

## Code Quality Gates

### Before Committing

```bash
# 1. Run tests
make test

# 2. Type check
make typecheck

# 3. Lint
make lint-fix

# 4. Format
make format

# 5. Coverage check
make test-coverage

# Shortcut: Run everything
make test && make typecheck && make lint-fix && make format
```

### In Pull Request

The CI/CD pipeline runs:
```bash
make test
make typecheck
make lint
```

If these fail locally, they'll fail in the PR.

## Key TypeScript Patterns

### Type-Safe Database Queries

```typescript
// Define result type
interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

// Type-safe query
const result = await pool.query<User>(
  'SELECT * FROM users WHERE id = $1',
  [id]
);

const user: User = result.rows[0];
```

### Error Handling

```typescript
interface ApiError extends Error {
  status: number;
}

// Create typed error
const error = new Error('User not found') as ApiError;
error.status = 404;
throw error;

// Or: typed handler
app.use((err: ApiError, req: Request, res: Response) => {
  const status = err.status || 500;
  res.status(status).json({ error: err.message });
});
```

### Request Tracing

```typescript
// Every response includes request ID
app.use((req: Request, res: Response, next: NextFunction) => {
  const requestId = req.headers['x-request-id'] || uuidv4();
  res.setHeader('x-request-id', requestId);

  // Pass to logger
  logger.info({ requestId }, 'Request started');

  next();
});

// In logs and responses:
{
  "x-request-id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "User created",
  "userId": 42
}
```

### Graceful Shutdown

```typescript
// Server stops accepting new connections
// Waits up to 30s for existing requests to finish
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');

  server.close(() => {
    pool.end();
    process.exit(0);
  });

  // Force exit after timeout
  setTimeout(() => {
    logger.error('Forced shutdown');
    process.exit(1);
  }, 30000);
});
```

## Testing Strategy

### Unit Tests (Jest)

```typescript
// Test a pure function or utility
describe('validateEmail', () => {
  it('should accept valid emails', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  it('should reject invalid emails', () => {
    expect(validateEmail('invalid')).toBe(false);
  });
});
```

### Integration Tests (Supertest)

```typescript
// Test full HTTP flow
describe('POST /users', () => {
  it('should create and retrieve user', async () => {
    const createResponse = await request(app)
      .post('/users')
      .send({ name: 'Bob', email: 'bob@example.com' });

    expect(createResponse.status).toBe(201);

    const getResponse = await request(app)
      .get(`/users/${createResponse.body.id}`);

    expect(getResponse.body.email).toBe('bob@example.com');
  });
});
```

### Test Coverage

```bash
# Generate coverage report
make test-coverage

# Open report in browser
open coverage/lcov-report/index.html
```

## Performance Considerations

### Connection Pooling

The API uses a connection pool (default: 20 connections):

```typescript
const pool = new Pool({
  max: 20,              // Max connections
  idleTimeoutMillis: 30000,  // Close idle after 30s
  connectionTimeoutMillis: 2000, // Connect timeout
});
```

For high throughput, adjust these values based on load testing.

### Query Performance

- Use parameterized queries (already done with `$1, $2` placeholders)
- Add database indexes for frequently queried fields
- Consider pagination for large result sets

```typescript
// With pagination
app.get('/users', async (req, res, next) => {
  const page = parseInt(req.query.page as string) || 1;
  const limit = 10;
  const offset = (page - 1) * limit;

  const result = await pool.query(
    'SELECT * FROM users LIMIT $1 OFFSET $2',
    [limit, offset]
  );

  res.json(result.rows);
});
```

## Monitoring & Observability

### Request Logging

Every request is logged with:
- Method and path
- Request ID (for tracing)
- Response time
- Status code

```typescript
// Access logs
2025-01-12T10:15:30.123Z POST /users 201 124ms req-id: 550e8400...
2025-01-12T10:15:31.456Z GET /users/1 200 45ms req-id: 660e8400...
```

### Health Check

```bash
curl http://localhost:3000/health
# Returns: {"status":"ok"}
```

Use for:
- Kubernetes liveness probes
- Load balancer health checks
- Container orchestration

### Error Logging

Errors are logged with full context:

```typescript
logger.error({
  requestId,
  error: err.message,
  stack: err.stack,
  userId,
  endpoint: '/users/1'
}, 'User fetch failed');
```

## Deployment

### Build Docker Image

```bash
make docker-build

# Or manually
docker build -t my-node-api:v1.0.0 .
```

### Run in Production

```bash
# Using Docker Compose (local demo)
make docker-up

# In Kubernetes or cloud platform:
# 1. Use the Dockerfile to build image
# 2. Push to registry
# 3. Deploy with environment variables:
#    - NODE_ENV=production
#    - DB_HOST, DB_USER, DB_PASSWORD
#    - DB_NAME, DB_PORT
#    - PORT

# The app handles graceful shutdown automatically
```

### Environment Variables

```bash
NODE_ENV=production      # production or development
PORT=3000                # Server port
DB_HOST=postgres         # Database hostname
DB_PORT=5432             # Database port
DB_USER=postgres         # Database user
DB_PASSWORD=postgres     # Database password
DB_NAME=playbook_db      # Database name
```

## Related Playbook Commands

- `/pb-start` — Create and track feature branches
- `/pb-cycle` — Feature develop → test → commit cycle
- `/pb-guide` — General SDLC process
- `/pb-testing` — Testing strategy and patterns
- `/pb-patterns-core` — Error handling, type safety, patterns
- `/pb-security` — Security checklist and validation patterns
- `/pb-deployment` — Container deployment strategies
- `/pb-observability` — Logging and monitoring design

## Getting Help

- Check logs: `docker-compose logs api`
- Inspect database: `docker exec -it playbook_node_db psql -U postgres`
- Read source: `src/main.ts` has inline comments
- Review tests: `tests/api.test.ts` shows usage examples

---

*Last updated: 2026-01-12*
