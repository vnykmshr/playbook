# Command Index

Quick reference for all playbook commands.

**For detailed integration guide showing how commands work together, see [`/docs/integration-guide.md`](integration-guide.md)**

---

## 🚀 Read First: The Preamble

**→ `/pb-preamble`** — Foundational mindset for all collaboration. Read this before any other command. It establishes the assumptions all playbook commands build on.

---

## Development Workflow

| Command | When to Use |
|---------|-------------|
| `/pb-start` | Starting work on a feature branch |
| `/pb-todo-implement` | Structured implementation of individual todos with checkpoint-based review |
| `/pb-cycle` | Each iteration (develop → review → commit) |
| `/pb-resume` | Resuming after a break |
| `/pb-pause` | Pausing work, preserving context for later |
| `/pb-ship` | Ready to ship: full reviews → PR → merge → release |
| `/pb-pr` | Creating a pull request (standalone) |
| `/pb-knowledge-transfer` | Preparing KT session for new developer or team handoff |
| `/pb-debug` | Systematic debugging methodology (reproduce, isolate, hypothesize, test, fix) |
| `/pb-design-language` | Create and evolve project-specific design specification (tokens, vocabulary, constraints) |

## Patterns & Architecture

| Command | When to Use |
|---------|-------------|
| `/pb-patterns` | Overview & quick reference for all patterns |
| `/pb-patterns-core` | Core architectural & design patterns (SOA, Event-Driven, Retry, Circuit Breaker, etc.) |
| `/pb-patterns-async` | Async/concurrent patterns (callbacks, promises, async/await, reactive, workers, job queues) |
| `/pb-patterns-db` | Database patterns (pooling, optimization, replication, sharding) |
| `/pb-patterns-distributed` | Distributed patterns (saga, CQRS, eventual consistency, 2PC) |
| `/pb-patterns-security` | Security patterns for microservices (OAuth, JWT, mTLS, RBAC, ABAC, encryption, audit trails) |
| `/pb-patterns-cloud` | Cloud deployment patterns (AWS EC2/RDS, ECS, Lambda; GCP Cloud Run, GKE; Azure App Service, Functions) |
| `/pb-patterns-frontend` | Frontend architecture patterns (mobile-first, theme-aware, component patterns, state management) |
| `/pb-patterns-api` | API design patterns (REST, GraphQL, gRPC, versioning, error handling, pagination) |

## Planning

| Command | When to Use |
|---------|-------------|
| `/pb-plan` | Planning a new feature/release |
| `/pb-adr` | Documenting architectural decisions |
| `/pb-deprecation` | Planning deprecations, breaking changes, migration paths |
| `/pb-observability` | Planning monitoring, observability, and alerting strategy |
| `/pb-performance` | Performance optimization and profiling strategy |

## Release & Operations

| Command | When to Use |
|---------|-------------|
| `/pb-release` | Pre-release checks and deployment |
| `/pb-incident` | P0/P1 production incidents |

## Repository Management

| Command | When to Use |
|---------|-------------|
| `/pb-repo-init` | Initialize new greenfield project |
| `/pb-repo-organize` | Clean up project root structure |
| `/pb-repo-about` | Generate GitHub About section + tags |
| `/pb-repo-readme` | Write or rewrite project README |
| `/pb-repo-blog` | Create technical blog post |
| `/pb-repo-enhance` | Full repository polish (combines above) |

## Reviews

| Command | When to Use | Frequency |
|---------|-------------|-----------|
| `/pb-review` | Comprehensive multi-perspective | Monthly or pre-release |
| `/pb-review-cleanup` | Code cleanup, repo health | Before new dev cycle |
| `/pb-review-prerelease` | Pre-release code review | Before each release |
| `/pb-review-tests` | Test suite quality | Monthly |
| `/pb-review-docs` | Documentation accuracy | Quarterly |
| `/pb-review-hygiene` | Multi-role health check | Quarterly |
| `/pb-review-product` | Technical + product review | Monthly |
| `/pb-review-microservice` | Microservice architecture design review | Before microservice deployment |
| `/pb-logging` | Logging strategy & standards audit | During code review, pre-release |
| `/pb-a11y` | Accessibility deep-dive (semantic HTML, keyboard, ARIA, screen readers) | During frontend development, every PR |

## Thinking Partner

Self-sufficient thinking partner methodology for expert-quality collaboration.

| Command | When to Use |
|---------|-------------|
| `/pb-query` | Need polished, expert-quality answer (multi-pass refinement) |
| `/pb-ideate` | Need to explore options, generate possibilities (divergent thinking) |
| `/pb-synthesize` | Need to combine multiple inputs into coherent insight (integration) |

**Thinking Partner Stack:**
```
/pb-ideate      → Explore options (divergent)
/pb-synthesize  → Combine insights (integration)
/pb-preamble    → Challenge assumptions (adversarial)
/pb-plan        → Structure approach (convergent)
/pb-adr         → Document decision (convergent)
/pb-query       → Refine output (refinement)
```

## Reference Documents

| Command | Purpose |
|---------|---------|
| `/pb-guide` | Full SDLC guide with tiers, gates, checklists |
| `/pb-guide-go` | Go-specific SDLC guide with concurrency patterns and tooling |
| `/pb-guide-python` | Python-specific SDLC guide with async/await and testing |
| `/pb-templates` | Templates for commits, phases, reviews |
| `/pb-standards` | Coding standards, quality principles |
| `/pb-context` | Project onboarding context template |

## Example Projects

Real-world implementations of the playbook in action:

| Project | Stack | Purpose | Location |
|---------|-------|---------|----------|
| **Go Backend API** | Go 1.22 + PostgreSQL | REST API with graceful shutdown, connection pooling | `examples/go-backend-api/` |
| **Python Pipeline** | Python 3.11 + SQLAlchemy | Async data pipeline with event aggregation | `examples/python-data-pipeline/` |
| **Node.js REST API** | Node.js 20 + TypeScript + Express | Type-safe REST API with request tracing | `examples/node-api/` |

**See [`docs/playbook-in-action.md`](playbook-in-action.md) for detailed walkthrough showing:**
- How to use `/pb-start`, `/pb-cycle`, and `/pb-pr` with real examples
- Complete development workflows for each stack
- Testing, code quality, and deployment patterns
- Common scenarios with step-by-step commands

## Typical Workflows

### Feature Development (with Checkpoint Review)
```
/pb-plan              → Lock scope, define phases
/pb-start             → Create branch, set rhythm
/pb-todo-implement    → Implement todos with checkpoint-based approval
/pb-cycle             → Self-review → Peer review iteration
/pb-pause             → End of day: preserve context
/pb-resume            → Next day: recover context
/pb-ship              → Full reviews → PR → merge → release → verify
```

### Feature Development (Traditional)
```
/pb-plan     → Lock scope, define phases
/pb-start    → Create branch, set rhythm
/pb-cycle    → Develop → Review → Commit (repeat)
/pb-pause    → End of session: preserve context
/pb-resume   → Resume: recover context
/pb-ship     → Full reviews → PR → merge → release → verify
```

### New Project Setup
```
/pb-repo-init      → Plan project structure
/pb-repo-organize  → Clean folder layout
/pb-repo-readme    → Write documentation
/pb-repo-about     → GitHub presentation
```

### Repository Polish
```
/pb-repo-enhance   → Full suite (organize + docs + presentation)
```

### Periodic Maintenance
```
/pb-review-*       → Various reviews as scheduled
```

## Browse All Commands

For a comprehensive list of all available commands organized by category, see the command files in `/commands/` directory or consult the [integration guide](integration-guide.md) for workflow-based command references.
