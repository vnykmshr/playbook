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
| `/pb-commit` | Crafting atomic, meaningful commits |
| `/pb-resume` | Resuming after a break |
| `/pb-pause` | Pausing work, preserving context for later |
| `/pb-ship` | Ready to ship: full reviews → PR → merge → release |
| `/pb-pr` | Creating a pull request (standalone) |
| `/pb-testing` | Testing philosophy (unit, integration, E2E strategies) |
| `/pb-jordan-testing` | Testing & reliability review (gap detection, edge case coverage, failure mode analysis) |
| `/pb-standup` | Daily async status updates for distributed teams |
| `/pb-knowledge-transfer` | Preparing KT session for new developer or team handoff |
| `/pb-what-next` | Context-aware command recommendations based on git state |
| `/pb-debug` | Systematic debugging methodology (reproduce, isolate, hypothesize, test, fix) |
| `/pb-learn` | Capture reusable patterns from sessions (errors, debugging, workarounds) |
| `/pb-design-language` | Create and evolve project-specific design specification (tokens, vocabulary, constraints) |

## Patterns & Architecture

| Command | When to Use |
|---------|-------------|
| `/pb-patterns` | Overview & quick reference for all patterns |
| `/pb-patterns-core` | Core architectural & structural patterns (SOA, Event-Driven, Repository, DTO, Strangler Fig) |
| `/pb-patterns-resilience` | Resilience patterns (Retry, Circuit Breaker, Rate Limiting, Cache-Aside, Bulkhead) |
| `/pb-patterns-async` | Async/concurrent patterns (callbacks, promises, async/await, reactive, workers, job queues) |
| `/pb-patterns-db` | Database patterns (pooling, optimization, replication, sharding) |
| `/pb-patterns-distributed` | Distributed patterns (saga, CQRS, eventual consistency, 2PC) |
| `/pb-patterns-security` | Security patterns for microservices (OAuth, JWT, mTLS, RBAC, ABAC, encryption, audit trails) |
| `/pb-patterns-cloud` | Cloud deployment patterns (AWS EC2/RDS, ECS, Lambda; GCP Cloud Run, GKE; Azure App Service, Functions) |
| `/pb-patterns-frontend` | Frontend architecture patterns (mobile-first, theme-aware, component patterns, state management) |
| `/pb-patterns-api` | API design patterns (REST, GraphQL, gRPC, versioning, error handling, pagination) |
| `/pb-patterns-deployment` | Deployment strategies (blue-green, canary, rolling, feature flags, rollback) |

## Planning

| Command | When to Use |
|---------|-------------|
| `/pb-plan` | Planning a new feature/release |
| `/pb-adr` | Documenting architectural decisions |
| `/pb-maya-product` | Product & user strategy review (features as expenses, scope discipline) |
| `/pb-deprecation` | Planning deprecations, breaking changes, migration paths |
| `/pb-observability` | Planning monitoring, observability, and alerting strategy |
| `/pb-performance` | Performance optimization and profiling strategy |

## Release & Operations

| Command | When to Use |
|---------|-------------|
| `/pb-release` | Release orchestrator: readiness gate, version/tag, trigger deployment |
| `/pb-deployment` | Execute deployment: discovery, pre-flight, execute, verify, rollback |
| `/pb-alex-infra` | Infrastructure & resilience review (systems thinking, failure modes, recovery) |
| `/pb-incident` | P0/P1 production incidents |
| `/pb-maintenance` | Production maintenance patterns — database, backups, health monitoring |
| `/pb-sre-practices` | Toil reduction, error budgets, on-call health, blameless culture |
| `/pb-dr` | Disaster recovery planning, RTO/RPO, backup strategies, game days |
| `/pb-server-hygiene` | Periodic server health and hygiene review (drift, bloat, cleanup) |
| `/pb-database-ops` | Database migrations, backups, performance, connection pooling |

## Security & Hardening

| Command | When to Use |
|---------|-------------|
| `/pb-security` | Application security review |
| `/pb-hardening` | Server, container, and network security hardening |
| `/pb-secrets` | Secrets management (SOPS, Vault, rotation, incident response) |

## Repository Management

| Command | When to Use |
|---------|-------------|
| `/pb-repo-init` | Initialize new greenfield project |
| `/pb-repo-organize` | Clean up project root structure |
| `/pb-repo-about` | Generate GitHub About section + tags |
| `/pb-repo-readme` | Write or rewrite project README |
| `/pb-repo-blog` | Create technical blog post |
| `/pb-repo-docsite` | Transform docs into professional static site |
| `/pb-repo-enhance` | Full repository polish (combines above) |
| `/pb-zero-stack` | Scaffold $0/month app (static + edge proxy + CI) |

## Reviews

| Command | When to Use | Frequency |
|---------|-------------|-----------|
| `/pb-review` | Orchestrate comprehensive multi-perspective review | Monthly or pre-release |
| `/pb-review-code` | Dedicated code review for reviewers (peer review checklist) | Every PR review |
| `/pb-linus-agent` | Direct, unfiltered technical feedback grounded in pragmatism | Security-critical code, architecture decisions |
| `/pb-review-backend` | Backend review (Alex infrastructure + Jordan testing) | Backend PRs |
| `/pb-review-frontend` | Frontend review (Maya product + Sam documentation) | Frontend PRs |
| `/pb-review-infrastructure` | Infrastructure review (Alex resilience + Linus security) | Infrastructure PRs |
| `/pb-review-hygiene` | Code quality + operational readiness | Before new dev cycle, monthly |
| `/pb-review-tests` | Test suite quality | Monthly |
| `/pb-review-docs` | Documentation accuracy | Quarterly |
| `/pb-review-product` | Technical + product review | Monthly |
| `/pb-review-microservice` | Microservice architecture design review | Before microservice deployment |
| `/pb-logging` | Logging strategy & standards audit | During code review, pre-release |
| `/pb-a11y` | Accessibility deep-dive (semantic HTML, keyboard, ARIA, screen readers) | During frontend development, every PR |
| `/pb-review-playbook` | Review playbook commands for quality, consistency, and completeness | Every PR, monthly |
| `/pb-review-context` | Audit CLAUDE.md files against conversation history (violated rules, missing patterns, stale content) | Quarterly, before `/pb-evolve` |
| `/pb-voice` | Detect and remove AI tells from prose (two-stage: detect → rewrite) | After AI-assisted drafting, before publishing |

## Thinking Partner

Self-sufficient thinking partner methodology for expert-quality collaboration.

| Command | When to Use |
|---------|-------------|
| `/pb-think` | Complete thinking toolkit with modes: ideate, synthesize, refine |
| `/pb-think mode=ideate` | Divergent exploration - generate options and possibilities |
| `/pb-think mode=synthesize` | Integration - combine multiple inputs into coherent insight |
| `/pb-think mode=refine` | Convergent refinement - polish to expert-quality |

**Thinking Partner Stack:**
```
/pb-think mode=ideate     → Explore options (divergent)
/pb-think mode=synthesize → Combine insights (integration)
/pb-preamble              → Challenge assumptions (adversarial)
/pb-plan                  → Structure approach (convergent)
/pb-adr                   → Document decision (convergent)
/pb-think mode=refine     → Refine output (refinement)
```

## Reference Documents

| Command | Purpose |
|---------|---------|
| `/pb-guide` | Full SDLC guide with tiers, gates, checklists |
| `/pb-guide-go` | Go-specific SDLC guide with concurrency patterns and tooling |
| `/pb-guide-python` | Python-specific SDLC guide with async/await and testing |
| `/pb-templates` | Templates for commits, phases, reviews |
| `/pb-standards` | Coding standards, quality principles |
| `/pb-documentation` | Writing technical docs at 5 levels |
| `/pb-sam-documentation` | Documentation & clarity review (reader-centric, assumption surfacing, structural clarity) |
| `/pb-design-rules` | 17 classical design principles (Clarity, Simplicity, Resilience, Extensibility) |
| `/pb-preamble-async` | Async/distributed team collaboration patterns |
| `/pb-preamble-power` | Power dynamics and psychological safety |
| `/pb-preamble-decisions` | Decision-making and constructive dissent |
| `/pb-new-playbook` | Meta-playbook for creating new playbook commands (classification, scaffold, validation) |

## Team & People

| Command | When to Use |
|---------|-------------|
| `/pb-onboarding` | Structured team member onboarding |
| `/pb-team` | Team dynamics, feedback, and retrospectives |
| `/pb-knowledge-transfer` | Team knowledge sharing and KT sessions |

## System Utilities

Developer machine health and maintenance.

| Command | When to Use |
|---------|-------------|
| `/pb-doctor` | System health check (disk, memory, CPU, processes) |
| `/pb-storage` | Tiered disk cleanup (caches, packages, Docker) |
| `/pb-update` | Update all package managers and tools |
| `/pb-ports` | Find/kill processes on ports |
| `/pb-setup` | Bootstrap new dev machine |
| `/pb-gha` | Investigate GitHub Actions failures (flakiness, breaking commits, root cause) |
| `/pb-git-hygiene` | Periodic git repo audit (tracked files, stale branches, large objects, secrets) |

## Context & Templates

| Command | When to Use |
|---------|-------------|
| `/pb-context` | Project onboarding context template |
| `/pb-claude-global` | Generate global ~/.claude/CLAUDE.md from playbooks |
| `/pb-claude-project` | Generate project .claude/CLAUDE.md by analyzing codebase |
| `/pb-claude-orchestration` | Model selection, task delegation, and resource efficiency guide |
| `/pb-context-review` | Audit and maintain all context layers — quarterly or after releases |

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
/pb-repo-init      → Plan project structure (generic)
/pb-zero-stack     → Scaffold $0/month app (static + edge + CI)
/pb-repo-organize  → Clean folder layout
/pb-repo-readme    → Write documentation
/pb-repo-about     → GitHub presentation
```

### Repository Polish
```
/pb-repo-enhance   → Full suite (organize + docs + presentation)
```

### Documentation Site Setup
```
/pb-repo-docsite   → Transform existing docs into professional static site
                   → Includes CI/CD, GitHub Pages, Mermaid support
```

### Periodic Maintenance
```
/pb-review-*       → Various reviews as scheduled
/pb-git-hygiene    → Monthly git repo audit (branches, large files, secrets)
```

### System Maintenance
```
/pb-doctor         → Diagnose system health
/pb-storage        → Clean up disk space
/pb-update         → Update tools and packages
/pb-ports          → Resolve port conflicts
```

### New Machine Setup
```
/pb-setup          → Bootstrap dev environment
/pb-doctor         → Verify system health
```

## Browse All Commands

For a comprehensive list of all available commands organized by category, see the command files in `/commands/` directory or consult the [integration guide](integration-guide.md) for workflow-based command references.
