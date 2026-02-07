# Glossary

Common terms and abbreviations used in the Engineering Playbook.

---

## Playbook-Specific Terms

### Atomic Commit
A single commit that addresses one logical change and is always deployable. See `/pb-commit`.

### Code Review Cycle
The process of developing code, reviewing it (self and peer), and getting approval before committing. See `/pb-cycle`.

### Decision Framework
The Engineering Playbook itself—a set of structured processes for making engineering decisions.

### Integration Guide
Comprehensive documentation showing how all commands work together. See `/docs/integration-guide.md`.

### Quality Gate
A checkpoint that must pass before code moves forward. Examples: linting, testing, security review.

### Self-Review
Review by the code author before requesting peer review. Catches obvious issues and respects reviewers' time.

### Peer Review
Review by another engineer (usually senior) checking architecture, correctness, security, and maintainability.

---

## Development Process Terms

### Branch
A copy of the codebase where you work on a feature without affecting main code. See `/pb-start`.

### Commit
A logical unit of work saved to git with a message explaining what changed and why. See `/pb-commit`.

### Pull Request (PR)
A formal request to merge your branch into main. Includes code, description, and rationale. See `/pb-pr`.

### Feature
A new capability or user-facing improvement.

### Hotfix
An emergency fix for production issues, using expedited process. See `/pb-incident`.

### Refactor
Code change that doesn't change behavior, just improves structure/readability.

### Release
Publishing code to production. Includes pre-release checks and deployment. See `/pb-release`.

### Rollback
Reverting to previous code version if release breaks something.

---

## Architecture & Design Terms

### ADR
Architecture Decision Record. Documents major decisions with context, options, and rationale. See `/pb-adr`.

### Pattern
A proven solution to a recurring design problem. See `/pb-patterns-*`.

### Microservice
A small, independent service focused on one business capability.

### SOA
Service-Oriented Architecture. Breaking system into independent services.

### Event-Driven
Architecture where components communicate via events rather than direct calls.

### CQRS
Command Query Responsibility Segregation. Separating read and write models.

### Saga
Pattern for distributed transactions across multiple services.

### Circuit Breaker
Pattern for preventing cascading failures by stopping requests to failing services.

### Retry
Pattern for automatically retrying failed operations with backoff.

---

## Code Quality Terms

### Linting
Automatic code style checking. Catches style violations and common mistakes.

### Type Checking
Verifying code types match (especially in typed languages like TypeScript, Go).

### Test Coverage
Percentage of code executed by tests. Target: 70%+ for critical paths.

### Edge Case
Unusual or boundary condition that code must handle correctly.

### Flaky Test
Test that sometimes passes and sometimes fails (usually due to timing or randomness).

### Technical Debt
Code shortcuts taken for speed that require later rework. Accumulates if not managed.

---

## Security Terms

### Authentication
Verifying who the user is (login). See `/pb-security`.

### Authorization
Checking if authenticated user has permission for an action.

### Injection Attack
Attack where attacker inserts code through input fields (SQL injection, command injection).

### Rate Limiting
Restricting requests from single user/IP to prevent abuse.

### Secret
Sensitive data like passwords, tokens, API keys. Must never be in code.

### Input Validation
Checking user input is valid before processing.

---

## Operations Terms

### CI/CD
Continuous Integration / Continuous Deployment. Automated build, test, and deployment.

### Observability
System's ability to be understood from outside. Includes logging, metrics, tracing.

### Monitoring
Continuous observation of system health and performance.

### Alerting
Automatic notifications when metrics exceed thresholds.

### Runbook
Step-by-step guide for handling operational issues.

### SLA
Service Level Agreement. Commitment to availability/performance.

### P0/P1/P2/P3
Incident severity levels. P0=all users affected, P1=major impact, P2=limited, P3=minor.

### Deployment
Moving code from development to production.

### Rollout
Gradual deployment to percentage of users (canary deployment).

### Downtime
System is unavailable or significantly degraded.

---

## Team & Process Terms

### Standup
Daily status update (synchronous or async). See `/pb-standup`.

### Retrospective
Team reflection on what went well and what could improve.

### Onboarding
Process of bringing new team member up to speed. See `/pb-onboarding`.

### Knowledge Transfer
Sharing knowledge between team members or with new joiners. See `/pb-knowledge-transfer`.

### Tech Lead
Senior engineer responsible for technical decisions and code quality.

### Code Owner
Engineer responsible for specific code area. Should review changes to that area.

### Pair Programming
Two developers working on same code simultaneously.

### Code Review Feedback
Comments and suggestions on PR from reviewer.

---

## Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| CQRS | Command Query Responsibility Segregation |
| CI/CD | Continuous Integration / Continuous Deployment |
| DB/DB | Database |
| DRY | Don't Repeat Yourself |
| E2E | End-to-End |
| HTTP | HyperText Transfer Protocol |
| JSON | JavaScript Object Notation |
| ORM | Object-Relational Mapping |
| PR | Pull Request |
| QA | Quality Assurance |
| REST | Representational State Transfer |
| SLA | Service Level Agreement |
| SOA | Service-Oriented Architecture |
| SQL | Structured Query Language |
| SSH | Secure Shell |
| TDD | Test-Driven Development |
| TTL | Time To Live |
| UI/UX | User Interface / User Experience |
| UTC | Coordinated Universal Time |
| YAML | YAML Ain't Markup Language |

---

## Command Reference

Shorthand for commands used throughout documentation:

| Shorthand | Full Command | Purpose |
|-----------|--------------|---------|
| `/pb-adr` | Architecture Decision Record | Document major decisions |
| `/pb-commit` | Craft Atomic Commits | Create logical, well-formatted commits |
| `/pb-cycle` | Development Cycle | Self-review and peer review iteration |
| `/pb-guide` | SDLC Guide | Full development framework |
| `/pb-incident` | Incident Response | Handle production issues |
| `/pb-logging` | Logging Standards | Structured logging audit |
| `/pb-observability` | Observability Setup | Monitor, log, trace systems |
| `/pb-patterns` | Pattern Overview | Architecture patterns |
| `/pb-patterns-async` | Async Patterns | Async/concurrent patterns |
| `/pb-patterns-core` | Core Patterns | SOA, events, repository, DTO |
| `/pb-patterns-resilience` | Resilience Patterns | Retry, circuit breaker, rate limiting |
| `/pb-patterns-db` | Database Patterns | Pooling, optimization, sharding |
| `/pb-patterns-distributed` | Distributed Patterns | Saga, CQRS, eventual consistency |
| `/pb-performance` | Performance Optimization | Profiling and optimization |
| `/pb-pr` | Pull Request Creation | Create PR with context |
| `/pb-release` | Release Checklist | Pre-release verification |
| `/pb-review` | Comprehensive Review | Multi-perspective code audit |
| `/pb-security` | Security Checklist | Input validation, auth, secrets |
| `/pb-start` | Start Feature Branch | Create branch and set rhythm |
| `/pb-standup` | Daily Standup | Async status update |
| `/pb-standards` | Team Standards | Coding standards and norms |
| `/pb-templates` | Reusable Templates | Commit, PR, review templates |
| `/pb-testing` | Testing Patterns | Unit, integration, E2E tests |

---

## See Also

- **[Decision Guide](decision-guide.md)** — Which command to use?
- **[Command Reference](command-index.md)** — All commands
- **[Getting Started](getting-started.md)** — Quick start
- **[FAQ](faq.md)** — Common questions
