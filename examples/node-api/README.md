# Node.js User Management API

A minimal but realistic Express.js API with TypeScript demonstrating how to use the Engineering Playbook (`/pb-*` commands) in a modern JavaScript project.

---

## What This Project Does

REST API for managing users with TypeScript:
- **GET /users** — List all users
- **GET /users/{id}** — Get single user
- **POST /users** — Create user with validation
- **DELETE /users/{id}** — Delete user

Features:
- TypeScript for type safety
- Express.js web framework
- PostgreSQL with connection pooling
- Request ID tracking for tracing
- Structured logging with Pino
- Graceful shutdown

---

## How This Project Uses the Playbook

### Development
- **`/pb-start`** — Create feature branch
- **`/pb-cycle`** — Each feature: develop → test → commit
- **`/pb-guide-python`** — JavaScript/TypeScript patterns (async, testing)

### Testing
- **`/pb-testing`** — Unit tests with Jest and supertest
- Run: `make test`

### Code Quality
- **`/pb-standards`** — ESLint, Prettier, TypeScript
- Run: `make lint && make format && make typecheck`

### Security
- **`/pb-patterns-security`** — Input validation, parameterized queries
- **`/pb-security`** — Security checklist

### Release
- **`/pb-release`** — Pre-release checks
- **`/pb-deployment`** — Container deployment

---

## Quick Start

### 1. Run with Docker Compose

```bash
cd examples/node-api

# Start API and PostgreSQL
docker-compose up

# Test in another terminal
curl http://localhost:3000/health
curl http://localhost:3000/users
```

### 2. Develop Locally

```bash
# Install Node 20+
# Install dependencies
make install

# Run tests
make test

# Start development server
make dev

# API runs on http://localhost:3000
```

### 3. Build and Run

```bash
make build
make run
```

---

## Project Structure

```
node-api/
├── src/
│   └── main.ts              # Express app + handlers
├── tests/
│   └── api.test.ts          # Jest tests + supertest
├── docs/
│   ├── DEVELOPMENT.md       # Dev workflow
│   └── ARCHITECTURE.md      # System design
├── Dockerfile               # Container image
├── docker-compose.yml       # Local dev stack
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
├── Makefile                 # Build targets
└── README.md                # This file
```

---

## Key Patterns from Playbook

### 1. Type Safety (`/pb-guide-python` - JavaScript section)
```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

async function getUser(id: number): Promise<User | null> {
  // Type checked at compile time
}
```

### 2. Error Handling (`/pb-patterns-core`)
```typescript
try {
  const user = await getUserFromDB(id);
  if (!user) {
    const error = new Error('User not found') as ApiError;
    error.status = 404;
    throw error;
  }
} catch (err) {
  // Structured error response
  next(err);
}
```

### 3. Request Tracing (`/pb-observability`)
```typescript
// Request ID middleware
const requestId = req.headers['x-request-id'] || uuidv4();
res.setHeader('x-request-id', requestId);
```

### 4. Graceful Shutdown
```typescript
process.on('SIGTERM', () => {
  server.close(() => {
    pool.end();
  });
});
```

### 5. Testing (`/pb-testing`)
```typescript
describe('POST /users', () => {
  it('should create user with valid input', async () => {
    const response = await request(app)
      .post('/users')
      .send({ name: 'Alice', email: 'alice@example.com' });

    expect(response.status).toBe(201);
  });
});
```

---

## Common Tasks

### Add a New Endpoint

```typescript
// In src/main.ts
app.get('/users/:id/posts', async (req, res, next) => {
  try {
    const posts = await getPosts(req.params.id);
    res.json(posts);
  } catch (err) {
    next(err);
  }
});
```

### Run Tests

```bash
make test           # Run all tests
make test-watch     # Watch mode
make test-coverage  # Coverage report
```

### Quality Checks

```bash
make lint           # Check for issues
make lint-fix       # Fix automatically
make format         # Format code
make typecheck      # Type checking
```

---

## Development Workflow

```bash
# 1. Start feature
git checkout -b feature/v1.0.0-new-endpoint main

# 2. Each iteration
make dev            # Run locally
make test           # Test
make lint-fix       # Fix issues
git commit -m "feat: add new endpoint"

# 3. Final checks
make typecheck
make test-coverage

# 4. Create PR
git push origin feature/v1.0.0-new-endpoint
# Use /pb-pr command
```

---

## Docker & Deployment

### Build

```bash
make docker-build
```

### Run

```bash
make docker-up
# API on http://localhost:3000
# Database on localhost:5432
```

### Stop

```bash
make docker-down
```

---

## Related Playbook Commands

- `/pb-guide` — General SDLC process
- `/pb-testing` — Testing strategy
- `/pb-patterns-core` — Error handling, patterns
- `/pb-patterns-security` — Security patterns
- `/pb-security` — Security checklist
- `/pb-deployment` — Container deployment

---

## Troubleshooting

### Port already in use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 make dev
```

### Database connection failed

```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### Tests fail

```bash
# Check Node version
node --version  # Should be 20+

# Reinstall dependencies
rm -rf node_modules
make install
make test
```

---

*This example is part of the Engineering Playbook project.*
*Last updated: 2026-01-12*
