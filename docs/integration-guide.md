# Playbook Integration Guide

Complete reference for how all playbook commands work together to form a unified SDLC framework.

**Last Updated**: 2026-01-24 | **Categories**: 9

---

## Table of Contents

1. [Quick Start: Command Selection](#quick-start)
2. [Command Inventory](#command-inventory-all-55)
3. [Workflow Maps](#workflow-maps)
4. [Command Clusters](#command-clusters-groups-that-work-together)
5. [Reference Matrix](#reference-matrix-which-commands-work-together)
6. [Integration Patterns](#integration-patterns)
7. [Common Workflows](#common-workflows-step-by-step)

---

## Quick Start: Command Selection

### By Situation

**Starting a new project?**
→ `/pb-plan` (planning) → `/pb-adr` (architecture) → `/pb-patterns-*` (select patterns) → `/pb-repo-init` (setup)

**Implementing a feature?**
→ `/pb-start` (begin) → `/pb-cycle` (iterate) → `/pb-commit` (atomic commits) → `/pb-pr` (merge)

**Implementing a specific todo?**
→ `/pb-todo-implement` (structured checkpoint-based implementation)

**Reviewing code before merge?**
→ `/pb-cycle` (self-review) → `/pb-review-hygiene` (peer review) → `/pb-security` (security review)

**Reviewing quality periodically?**
→ `/pb-review-tests` (monthly) → `/pb-review-hygiene` (quarterly) → `/pb-review-product` (product alignment)

**Deploying to production?**
→ `/pb-release` (pre-release checks) → `/pb-deployment` (strategy selection) → `/pb-observability` (monitoring)

**Incident response?**
→ `/pb-incident` (assessment + mitigation) → `/pb-observability` (monitoring) → Post-incident `/pb-incident` (deep review)

**Onboarding new team member?**
→ `/pb-onboarding` (structured plan) → `/pb-knowledge-transfer` (KT session) → `/pb-guide` (SDLC overview)

**Quick context recovery?**
→ `/pb-resume` (get back in context) → `/pb-context` (refresh decision log)

---

## Command Inventory

### CORE FOUNDATION & PHILOSOPHY
These establish baseline understanding and guiding philosophy. **Every engineer should know these.**

| # | Command | Purpose | Key Sections | When to Use | Tier |
|---|---------|---------|--------------|------------|------|
| 1 | **pb-guide** | Master SDLC framework | 11 phases from intake through post-release | Reference for all other commands | All |
| 2 | **pb-preamble** | Peer collaboration philosophy | Correctness, critical thinking, truth, holistic perspective | Foundation for all team interactions | All |
| 3 | **pb-design-rules** | Technical design principles | 17 rules in 4 clusters (Clarity, Simplicity, Resilience, Extensibility) | When making architectural decisions | M/L |
| 4 | **pb-standards** | Working principles and collaboration | Decision-making, scope discipline, quality standards | Before starting any work | All |
| 5 | **pb-documentation** | Technical documentation at 5 levels | Code comments, APIs, system design, process docs, FAQ | When writing docs (inline with code per /pb-cycle) | M/L |
| 6 | **pb-templates** | Reusable SDLC templates | Commit strategy, checklists, testing standards | When creating commits, PRs, tests | All |
| 7 | **pb-preamble-async** | Preamble for distributed teams | Async decision-making, communication patterns | For teams working across time zones | M |
| 8 | **pb-preamble-power** | Power dynamics and challenge | Psychological safety, healthy disagreement, authority | For building stronger team dynamics | M |
| 9 | **pb-preamble-decisions** | Decision discipline through preamble | Decision frameworks, tradeoff analysis | When making complex technical decisions | M |
| 10 | **pb-context** | Project context and decision log | Current focus, recent decisions, architecture notes | Quick context refresh, decision tracking | All |
| 11 | **pb-think** | Unified thinking partner | Complete toolkit: ideate, synthesize, refine modes | Complex questions, research, multi-perspective | All |

**How they work together**:
- Read `/pb-preamble` and `/pb-standards` to understand philosophy and principles
- Reference `/pb-guide` for framework (11 phases)
- Use `/pb-design-rules` for technical design guidance
- Use `/pb-templates` for format/structure
- Use `/pb-documentation` for content quality
- Use preamble expansions for specific team contexts
- Use `/pb-think` for expert-quality collaboration (modes: ideate, synthesize, refine)

---

### DEVELOPMENT WORKFLOW
Daily iterative development. **Use these multiple times per week.**

| # | Command | Purpose | Flow | When to Use | Tier |
|---|---------|---------|------|------------|------|
| 5 | **pb-start** | Begin feature development | Create branch, set iteration rhythm | Start of feature/bug | All |
| 6 | **pb-resume** | Get back in context after break | Restore working state, read pause notes | After context switch or day break | All |
| 7 | **pb-pause** | Gracefully pause work | Preserve state, update trackers, document handoff | End of day/session, before break | All |
| 8 | **pb-cycle** | Self-review + peer review iteration | Self-review → peer review → refine → commit | Multiple times per feature | All |
| 9 | **pb-commit** | Craft atomic, meaningful commits | One concern per commit, good messages | Before merging to main | S/M/L |
| 10 | **pb-ship** | Complete ship workflow | Reviews → PR → peer review → merge → release → verify | When focus area is code-complete | All |
| 11 | **pb-pr** | Streamlined pull request creation | PR title, description template, merge strategy | When ready for code review (standalone) | All |
| 12 | **pb-testing** | Testing philosophy and patterns | Unit/integration/E2E, test data, CI/CD | Alongside code in /pb-cycle | S/M/L |
| 13 | **pb-knowledge-transfer** | KT session preparation | 12-section guide for knowledge sharing | Team transitions, onboarding | M |
| 14 | **pb-todo-implement** | Guided implementation with checkpoints | 5 phases: INIT → SELECT → REFINE → IMPLEMENT → COMMIT | After /pb-plan, before /pb-cycle (for major work) | All |

**Development flow**:
```
/pb-start
  ↓
ITERATION LOOP (repeat per task):
  /pb-cycle
    ├─ Self-review
    ├─ /pb-testing (write tests)
    ├─ /pb-standards (check principles)
    └─ Peer review
  /pb-commit (atomic commit)
  ↓
SESSION BOUNDARY (if needed):
  ├─ /pb-pause (end of session: preserve context)
  └─ /pb-resume (next session: recover context)
  ↓
READY TO SHIP:
  /pb-ship (comprehensive workflow)
    ├─ Specialized reviews (cleanup, hygiene, tests, security, docs)
    ├─ Final gate (prerelease)
    ├─ PR creation and peer review
    ├─ Merge and release
    └─ Verification
```

**Key integration points**:
- `/pb-start` → `/pb-cycle` (iterative development)
- `/pb-cycle` includes `/pb-testing` and `/pb-standards`
- `/pb-cycle` → `/pb-commit` (after self-review)
- `/pb-pause` ↔ `/pb-resume` (session boundary bookends)
- `/pb-ship` orchestrates: reviews → PR → merge → release → verify
- `/pb-todo-implement` provides **structured checkpoint-based alternative** to direct `/pb-cycle` workflow

---

### PLANNING & ARCHITECTURE
Technical planning before implementation. **Use these once per release.**

| # | Command | Purpose | Phases | When to Use | Tier |
|---|---------|---------|--------|------------|------|
| 13 | **pb-plan** | New focus area planning | Discovery, analysis, scope lock, documentation | Before major feature/release | All |
| 14 | **pb-adr** | Architecture Decision Records | When/how/format, examples, review process | When documenting technical decisions | M |
| 15 | **pb-patterns** | Pattern family overview | Links to 4 specialized pattern commands | Quick reference, pattern selection | M/L |
| 16 | **pb-patterns-async** | Async/concurrent patterns | Async/await, job queues, concurrency models | Designing concurrent systems | M/L |
| 17 | **pb-patterns-core** | Core architectural patterns | SOA, event-driven, circuit breaker, etc. | Designing system architecture | M/L |
| 18 | **pb-patterns-db** | Database patterns | Queries, optimization, N+1, sharding | Designing database layer | M/L |
| 19 | **pb-patterns-distributed** | Distributed system patterns | Saga, CQRS, eventual consistency, 2PC | Designing distributed systems | M/L |
| 20 | **pb-performance** | Performance optimization | Profiling, optimization strategies, monitoring | When performance is requirement | M/L |
| 21 | **pb-observability** | Monitoring, logging, tracing, alerting | Dashboards, SLOs, distributed tracing | When designing production systems | M/L |
| 22 | **pb-deprecation** | Safe API deprecation | Deprecation phases, versioning, migration | When needing backwards-compatible changes | M |

**Planning flow**:
```
/pb-plan (clarify scope)
  ↓
/pb-adr (document decisions)
  ↓
/pb-patterns (select architectural patterns)
  ├─ /pb-patterns-async (if async work needed)
  ├─ /pb-patterns-db (if database changes)
  ├─ /pb-patterns-distributed (if microservices)
  └─ /pb-patterns-core (core architecture)
  ↓
/pb-observability (plan monitoring strategy)
/pb-performance (set performance targets)
  ↓
READY FOR IMPLEMENTATION
  ↓
/pb-todo-implement (implement individual todos)
  ↓
/pb-development workflow (pb-start → pb-cycle → pb-commit → pb-pr)
```

**Pattern selection guide**:
- **Async work?** Use `/pb-patterns-async` (goroutines, channels, job queues, etc.)
- **Database layer?** Use `/pb-patterns-db` (pooling, optimization, replication, sharding)
- **Core architecture?** Use `/pb-patterns-core` (SOA, event-driven, circuit breaker)
- **Microservices?** Use `/pb-patterns-distributed` (Saga, CQRS, eventual consistency)
- **Uncertain?** Start with `/pb-patterns` (overview, then jump to specialized)

---

### REVIEWS & QUALITY
Quality gates at multiple checkpoints. **Use these during development, before merge, and periodically.**

| # | Command | Purpose | Trigger | When to Use | Frequency |
|---|---------|---------|---------|------------|-----------|
| 23 | **pb-review** | Periodic project review overview | Feature/release boundaries | Quick reference to all review types | Monthly or pre-release |
| 24 | **pb-review-hygiene** | Code quality and best practices | Every PR | Before merging code | Every PR |
| 25 | **pb-review-product** | Product alignment + tech perspective | Feature completion | Before merging user-facing changes | Every user-facing PR |
| 26 | **pb-review-docs** | Documentation accuracy and completeness | Periodic audit | Quarterly documentation review | Quarterly |
| 27 | **pb-review-tests** | Test suite quality and coverage | Periodic audit | Monthly test health check | Monthly |
| 28 | **pb-review-hygiene** | Codebase cleanup (dead code, deps, etc.) | Periodic maintenance | Quarterly code cleanup | Quarterly |
| 29 | **pb-review-microservice** | Microservice architecture review | Microservice development | Before microservice deployment | Per microservice |
| 30 | **pb-security** | Security checklist (quick/standard/deep) | Code review, pre-release, incidents | Quick (5min), Standard (20min), Deep (1+ hr) | Every PR, pre-release |
| 31 | **pb-logging** | Logging strategy & standards | Code review, pre-release | Verify structured logging, no secrets | Every PR, pre-release |

**Code review flow** (per PR):
```
/pb-cycle (self-review)
  ↓
/pb-pr (create pull request)
  ↓
PEER REVIEW GATES:
  /pb-review-hygiene (code quality)
  /pb-security (security checklist)
  /pb-review-tests (test coverage)
  /pb-logging (logging standards)
  /pb-review-product (if user-facing)
  ↓
APPROVED
  ↓
/pb-commit (merge with atomic commit)
```

**Periodic review schedule**:
```
WEEKLY
  ├─ /pb-review-hygiene (spot check)
  └─ /pb-logging (log quality)

MONTHLY
  ├─ /pb-review-tests (test health)
  ├─ /pb-observability (dashboard/alert review)
  └─ /pb-review-product (alignment check)

QUARTERLY
  ├─ /pb-review-hygiene (code cleanup)
  ├─ /pb-review-docs (documentation audit)
  ├─ /pb-security (deep dive)
  └─ /pb-team (team retrospective)

RELEASE
  ├─ /pb-release (final gate)
  ├─ /pb-security (security review)
  └─ /pb-review-microservice (if applicable)
```

---

### DEPLOYMENT & OPERATIONS
Infrastructure, deployment, and incident response.

| # | Command | Purpose | When to Use | Tier |
|---|---------|---------|------------|------|
| 33 | **pb-deployment** | Deployment strategies and safety | Before production deployment | Blue-green, canary, rolling, feature flags | M/L |
| 34 | **pb-incident** | Incident response framework | During production incidents | Severity assessment, mitigation, escalation | S/M/L |

**Deployment flow**:
```
/pb-release (pre-release checks pass)
  ↓
/pb-deployment (select strategy: blue-green, canary, rolling)
  ↓
Deploy to production
  ↓
/pb-observability (monitor metrics, logs, alerts)
  ├─ All good? Declare victory
  └─ Issues? → /pb-incident (incident response)
```

**Incident flow**:
```
INCIDENT DETECTED
  ↓
/pb-incident (rapid assessment)
  ├─ Severity: P0/P1/P2/P3
  ├─ Choose mitigation:
  │  ├─ Rollback (quickest)
  │  ├─ Hotfix (if rollback not feasible)
  │  └─ Feature disable (safest for toggles)
  │
  ├─ /pb-deployment (if need detailed rollback strategy)
  ├─ /pb-observability (monitor recovery)
  │
  └─ POST-INCIDENT (within 24h)
     ├─ Comprehensive incident review
     ├─ Create /pb-adr if architectural change needed
     └─ Document in /pb-context (decision log)
```

---

### REPOSITORY MANAGEMENT
Professional repository structure and presentation.

| # | Command | Purpose | Use | Tier |
|---|---------|---------|-----|------|
| 35 | **pb-repo-init** | Initialize greenfield project | Project start | Directory structure, README template, CI/CD | Project start |
| 36 | **pb-repo-organize** | Organize repository structure | Cleanup/improvement | Root layout, folder org, GitHub special files | S/M |
| 37 | **pb-repo-readme** | Write high-quality README | Repository documentation | Clear, searchable, language-specific | S |
| 38 | **pb-repo-about** | Set GitHub About section + tags | GitHub presentation | Profile optimization, tag selection | S |
| 39 | **pb-repo-blog** | Write technical blog post | Showcase project | Medium post, dev.to, etc. | M |
| 40 | **pb-repo-enhance** | Complete repository enhancement suite | All of above at once | Combines all repo commands | M |

**Repository setup flow**:
```
NEW PROJECT:
  /pb-repo-init (initial setup)
    ↓
  /pb-repo-organize (structure directories)
    ↓
  /pb-repo-readme (create README)
    ↓
  /pb-repo-about (set GitHub About)
    ↓
  /pb-repo-blog (write showcase post)

ENHANCE EXISTING:
  /pb-repo-enhance (one command does all above)
```

---

### TEAM & CONTINUITY
Knowledge sharing and team development.

| # | Command | Purpose | When to Use | Tier |
|---|---------|---------|------------|------|
| 41 | **pb-onboarding** | Structured team onboarding | New team member joins | Preparation, first day, first week, ramp-up | M |
| 42 | **pb-team** | Team dynamics, feedback, growth | Team retrospectives and feedback | Team health, learning culture, feedback loops | M |

**Onboarding flow**:
```
NEW TEAM MEMBER JOINS
  ↓
/pb-onboarding (structured 4-phase plan)
  ├─ Phase 1: Preparation
  │  └─ Repo setup, access, dev environment
  ├─ Phase 2: First Day
  │  └─ Welcome, orientation, first task
  ├─ Phase 3: First Week
  │  └─ Pair programming, small tasks, KT sessions
  └─ Phase 4: Ramp-up
     └─ Increasing responsibility, independent work
  ↓
/pb-knowledge-transfer (actual KT session)
  ↓
/pb-guide (SDLC overview and reference)
  ↓
/pb-context (project context and decision log)
```

**Team health flow**:
```
MONTHLY/QUARTERLY
  ↓
/pb-team (team retrospective)
  ├─ Team health check
  ├─ Feedback loops
  ├─ Learning culture
  └─ Growth opportunities
  ↓
Create action items for improvement
```

---

### REFERENCE & CONTEXT

Project working context and decision log.

| # | Command | Purpose | When to Use | Tier |
|---|---------|---------|------------|------|
| 43 | **pb-context** | Project context and decision log | Quick context refresh | Current focus, recent decisions, architecture notes | All |

**Context usage**:
```
CONTEXT REFRESH
  ↓
/pb-context (read current focus, decisions, architecture)
  ↓
Then:
  ├─ Starting work → /pb-start
  ├─ Resuming work → /pb-resume
  ├─ Making decision → Document in /pb-context
  └─ Understanding architecture → /pb-adr
```

---

## Workflow Maps

### Workflow 1: Complete Feature Delivery

```
PRE-DEVELOPMENT
├─ /pb-plan               ← Clarify scope
├─ /pb-adr                ← Document architecture
├─ /pb-patterns-*         ← Select patterns
├─ /pb-observability      ← Plan monitoring
└─ /pb-performance        ← Set targets

IMPLEMENTATION (iterative daily)
├─ /pb-start              ← Create branch
│
├─ FOR EACH TASK:
│  └─ ITERATION LOOP
│     ├─ /pb-cycle        ← Self-review + peer review
│     │  ├─ /pb-testing   ← Write tests
│     │  ├─ /pb-standards ← Check principles
│     │  ├─ /pb-security  ← Security check
│     │  └─ Refine based feedback
│     │
│     └─ /pb-commit       ← Atomic commit
│
└─ Repeat for each task

CODE REVIEW
├─ /pb-pr                 ← Create pull request
├─ /pb-review-hygiene        ← Code quality
├─ /pb-review-tests       ← Test coverage
├─ /pb-logging            ← Logging standards
├─ /pb-security           ← Security review
├─ /pb-review-product     ← Product alignment (if user-facing)
└─ Approve / Request changes

PRE-RELEASE
├─ /pb-release            ← Release checklist
├─ /pb-release  ← Senior engineer final gate
├─ /pb-deployment         ← Choose deployment strategy
└─ /pb-observability      ← Verify monitoring ready

DEPLOYMENT
├─ Execute deployment (blue-green/canary/rolling)
├─ /pb-observability      ← Monitor metrics
└─ POST-DEPLOYMENT
   ├─ Verify in production
   └─ If issues → /pb-incident

END
```

### Workflow 2: Planning & Architecture

```
START (New Release/Feature)
├─ /pb-plan                  ← Lock scope
├─ /pb-adr                   ← Document decisions
├─ /pb-patterns              ← Overview of available patterns
│  ├─ /pb-patterns-async     ← If async/concurrency needed
│  ├─ /pb-patterns-db        ← If database changes
│  ├─ /pb-patterns-distributed ← If microservices
│  └─ /pb-patterns-core      ← If core architecture
├─ /pb-observability         ← Plan monitoring strategy
├─ /pb-performance           ← Set performance targets
└─ /pb-deprecation           ← If removing/deprecating existing

IMPLEMENTATION
└─ /pb-todo-implement        ← Structured implementation by todo
```

### Workflow 3: Incident Response

```
INCIDENT DETECTED
├─ /pb-incident              ← Rapid assessment
│  ├─ Assess severity (P0/P1/P2/P3)
│  ├─ Choose mitigation:
│  │  ├─ Rollback
│  │  ├─ Hotfix
│  │  └─ Feature disable
│  └─ Communicate status
│
├─ /pb-deployment            ← If need detailed rollback
├─ /pb-observability         ← Monitor recovery
│
└─ POST-INCIDENT (within 24h)
   ├─ Comprehensive review
   ├─ Root cause analysis
   ├─ /pb-adr                ← If architectural fix needed
   ├─ Create action items
   └─ Document in /pb-context

PREVENT REPEAT
├─ /pb-cycle                 ← Implement prevention fixes
├─ /pb-testing               ← Add regression tests
└─ /pb-observability         ← Improve alerting
```

### Workflow 4: Team Onboarding

```
NEW TEAM MEMBER JOINS
├─ /pb-onboarding            ← Structured 4-phase plan
│  ├─ Phase 1: Preparation   ← Setup, access, dev env
│  ├─ Phase 2: First Day     ← Welcome, orientation
│  ├─ Phase 3: First Week    ← Pair programming, KT
│  └─ Phase 4: Ramp-up       ← Independent work
│
├─ /pb-knowledge-transfer    ← KT session execution
├─ /pb-guide                 ← SDLC overview
├─ /pb-standards             ← Working principles
├─ /pb-context               ← Project context
├─ /pb-adr                   ← Architecture decisions
└─ /pb-patterns              ← Design patterns

CONTINUOUS DEVELOPMENT
├─ /pb-start                 ← Start feature work
├─ /pb-cycle                 ← Iterate with feedback
└─ /pb-team                  ← Ongoing feedback and growth
```

### Workflow 5: Periodic Quality Reviews

```
WEEKLY
├─ /pb-review-hygiene           ← Code quality spot check
└─ /pb-logging               ← Log quality check

MONTHLY
├─ /pb-review-tests          ← Test suite health
├─ /pb-observability         ← Dashboard and alert tuning
└─ /pb-review-product        ← Product alignment

QUARTERLY
├─ /pb-review-hygiene        ← Code cleanup and deps
├─ /pb-review-docs           ← Documentation audit
├─ /pb-security              ← Security deep dive
└─ /pb-team                  ← Team retrospective

RELEASE
├─ /pb-release     ← Final release gate
├─ /pb-security              ← Security review
└─ /pb-review-microservice   ← If applicable
```

---

## Command Clusters: Groups That Work Together

### Cluster 1: Core Foundation
**Commands**: pb-guide, pb-standards, pb-templates, pb-context
**Purpose**: Establish baseline understanding and discipline
**Frequency**: Reference constantly; update /pb-context periodically
**Who**: Every engineer

### Cluster 2: Daily Development
**Commands**: pb-start, pb-cycle, pb-pause, pb-resume, pb-commit, pb-ship, pb-pr, pb-testing
**Purpose**: Iterative feature development with quality gates, session management, and shipping
**Frequency**: Use multiple times per week per feature
**Who**: All developers

### Cluster 3: Planning & Architecture
**Commands**: pb-plan, pb-adr, pb-patterns (+ 4 specialized), pb-observability, pb-performance
**Purpose**: Design systems before implementation
**Frequency**: Once per release or major feature
**Who**: Tech leads, architects, senior engineers

### Cluster 4: Checkpoint-Based Implementation
**Commands**: pb-plan → pb-todo-implement → pb-cycle
**Purpose**: Structured implementation with checkpoints before full code review
**Frequency**: For major features or refactoring
**Who**: Developers with checkpoint-based approval preference

### Cluster 5: Code Review & Quality
**Commands**: pb-review-*, pb-security, pb-logging, pb-testing
**Purpose**: Multiple perspectives on quality
**Frequency**: Every PR, periodic reviews, pre-release
**Who**: All developers, leads, security team

### Cluster 6: Production Safety
**Commands**: pb-deployment, pb-incident, pb-observability, pb-release
**Purpose**: Safe production deployment and incident response
**Frequency**: Every release, during incidents
**Who**: SREs, DevOps, on-call engineers

### Cluster 7: Repository Management
**Commands**: pb-repo-init, pb-repo-organize, pb-repo-readme, pb-repo-about, pb-repo-blog, pb-repo-enhance
**Purpose**: Professional repository structure and presentation
**Frequency**: Project start, periodic enhancement
**Who**: Tech leads, project owners

### Cluster 8: Knowledge & Continuity
**Commands**: pb-knowledge-transfer, pb-onboarding, pb-team, pb-documentation
**Purpose**: Preserve and share knowledge
**Frequency**: Team transitions, regular intervals
**Who**: Mentors, managers, all engineers

### Cluster 9: Thinking Partner
**Commands**: pb-think
**Purpose**: Self-sufficient expert-quality collaboration
**Frequency**: Throughout development for complex questions, ideation, synthesis
**Who**: All engineers

**Thinking Partner Stack:**
```
/pb-think mode=ideate     → Explore options (divergent)
/pb-think mode=synthesize → Combine insights (integration)
/pb-preamble              → Challenge assumptions (adversarial)
/pb-plan                  → Structure approach (convergent)
/pb-adr                   → Document decision (convergent)
/pb-think mode=refine     → Refine output (refinement)
```

---

## Reference Matrix: Which Commands Work Together

### By Incoming References

**Most Referenced** (critical hub):
- pb-guide: 25+ references (master framework)
- pb-standards: 15+ references (working principles)
- pb-cycle: 10+ references (core development loop)
- pb-testing: 8+ references (quality verification)
- pb-security: 7+ references (quality gate)

**Well-Referenced** (important workflow nodes):
- pb-adr, pb-deployment, pb-incident, pb-observability, pb-review-hygiene (5-9 references each)

**Moderately Referenced** (specialized/optional):
- pb-documentation, pb-pr, pb-commit, pb-patterns-* (2-4 references each)

**Under-Referenced** (isolation issues):
- pb-resume: 0 references (should integrate with pb-start, pb-context)
- pb-standup: 0 references (should integrate with pb-standards, pb-context)

### By Category Connections

**Core → Everything**
- All 44 other commands reference pb-guide and/or pb-standards

**Development → Planning**
- pb-start → pb-plan (for major features)
- pb-cycle → pb-testing
- pb-cycle → pb-standards
- pb-cycle → pb-security

**Planning → Development**
- pb-plan → pb-todo-implement
- pb-adr → pb-start (architectural context)
- pb-patterns → pb-cycle (pattern selection)

**Development → Review**
- pb-cycle → pb-review-hygiene
- pb-commit → pb-review-tests
- pb-pr → pb-review-product

**Review → Deployment**
- pb-review-hygiene → pb-release (readiness gate)
- pb-security → pb-release
- pb-release → pb-deployment

**Deployment → Observability**
- pb-deployment → pb-observability
- pb-incident → pb-observability
- pb-observability → pb-incident (feedback loop)

---

## Integration Patterns

### Pattern 1: Tiered Complexity

Commands often provide **multiple depths**:

```
QUICK (5-15 min)
├─ /pb-security quick checklist (top issues)
├─ /pb-testing unit test patterns
└─ /pb-incident rapid response

STANDARD (20-30 min)
├─ /pb-security standard checklist (20 items)
├─ /pb-testing unit + integration
└─ /pb-incident with escalation

DEEP (1+ hour)
├─ /pb-security deep dive (threat modeling)
├─ /pb-testing E2E + load testing
└─ /pb-incident comprehensive review
```

**Choose based on feature tier** (see pb-guide for XS/S/M/L)

### Pattern 2: Workflow Sequences

Commands are **ordered for maximum clarity**:

```
/pb-plan → /pb-adr → /pb-patterns → /pb-todo-implement → /pb-cycle → /pb-pr → /pb-review-* → /pb-release
```

Each feeds into the next with clear handoffs.

### Pattern 3: "Related Commands" Sections

Most commands include this section showing:
- Prerequisites (what to do before)
- Complementary commands (what to use alongside)
- Next steps (what to do after)

**Use these sections for guidance.**

### Pattern 4: Categories Map to Workflow Phases

```
PLANNING PHASE → /pb-plan, /pb-adr, /pb-patterns, /pb-performance, /pb-observability
DEVELOPMENT PHASE → /pb-start, /pb-cycle, /pb-commit, /pb-pr, /pb-testing, /pb-todo-implement
REVIEW PHASE → /pb-review-*, /pb-security, /pb-logging
DEPLOYMENT PHASE → /pb-release, /pb-deployment
OPERATIONS PHASE → /pb-incident, /pb-observability
TEAM PHASE → /pb-onboarding, /pb-team, /pb-knowledge-transfer
REPO PHASE → /pb-repo-*, /pb-documentation
```

---

## Common Workflows: Step-by-Step

### Scenario 1: Feature Request from Product

```
STEP 1: Planning
├─ Read /pb-plan (lock scope)
├─ Read /pb-adr (document architecture)
├─ Choose from /pb-patterns-* (select patterns)
└─ Review /pb-observability (plan monitoring)

STEP 2: Implementation
├─ /pb-start (create feature branch)
├─ LOOP: /pb-cycle (iterate)
│  ├─ Code changes
│  ├─ /pb-testing (add tests)
│  ├─ Self-review
│  └─ Peer review feedback
├─ /pb-commit (atomic commits)
└─ /pb-pr (create pull request)

STEP 3: Code Review
├─ /pb-review-hygiene (code quality)
├─ /pb-review-product (product alignment)
├─ /pb-security (security review)
├─ /pb-review-tests (test coverage)
└─ Approve / Merge

STEP 4: Release Preparation
├─ /pb-release (pre-release checks)
├─ /pb-release (senior review)
├─ /pb-deployment (choose strategy)
└─ /pb-observability (verify monitoring)

STEP 5: Deployment
├─ Execute deployment
├─ Monitor with /pb-observability
└─ Verify in production
```

### Scenario 2: Bug Fix with Incident

```
STEP 1: Incident Response
├─ /pb-incident (assess severity)
├─ Choose mitigation (rollback/hotfix/disable)
├─ Execute mitigation
└─ Communicate status

STEP 2: Implement Fix
├─ /pb-start (create hotfix branch)
├─ Make minimal fix
├─ /pb-testing (add regression test)
└─ /pb-cycle (review)

STEP 3: Code Review
├─ /pb-cycle (fast-track review)
├─ /pb-security (safety check)
└─ Approve / Merge

STEP 4: Verification
├─ Deploy hotfix
├─ Monitor with /pb-observability
└─ Verify recovery

STEP 5: Post-Incident
├─ /pb-incident (comprehensive review)
├─ Root cause analysis
├─ /pb-adr (if architectural fix needed)
└─ Document in /pb-context
```

### Scenario 3: Refactoring Large Component

```
STEP 1: Planning
├─ /pb-plan (refactoring scope)
├─ /pb-adr (new architecture decision)
├─ /pb-patterns (design patterns)
└─ /pb-performance (performance targets)

STEP 2: Implementation Phases
├─ Phase 1:
│  └─ /pb-todo-implement (checkpoint-based)
│     ├─ REFINE: Analyze codebase
│     ├─ PLAN: Outline refactoring steps
│     └─ IMPLEMENT: Execute checkpoint-by-checkpoint
├─ Phase 2:
│  └─ /pb-todo-implement (next component)
└─ Continue for each component

STEP 3: Code Review
├─ /pb-review-hygiene (architecture alignment)
├─ /pb-review-tests (regression test coverage)
├─ /pb-security (if security implications)
└─ Approve / Merge

STEP 4: Quality Verification
├─ /pb-observability (performance metrics)
├─ /pb-review-tests (no regressions)
└─ /pb-team (document learnings)
```

### Scenario 4: New Team Member Joins

```
WEEK 0: Preparation (Before they arrive)
├─ /pb-onboarding (prepare environment)
├─ /pb-repo-organize (ensure clear structure)
└─ /pb-documentation (update docs)

DAY 1: First Day
├─ Follow /pb-onboarding Phase 2
├─ Dev environment setup
├─ Team introductions
└─ High-level project overview

WEEK 1: First Week
├─ /pb-knowledge-transfer (KT session)
├─ /pb-guide (SDLC overview)
├─ /pb-adr (architecture decisions)
├─ /pb-standards (working principles)
└─ Small task with pair programming

WEEK 2-4: Ramp-up
├─ Increasing task complexity
├─ Independent work with feedback
├─ /pb-cycle (code review feedback)
└─ /pb-team (feedback and support)

ONGOING: Growth
├─ /pb-cycle (iterate on features)
├─ /pb-standards (reinforce principles)
└─ /pb-team (regular feedback)
```

---

## Summary: Playbook as Unified System

### Core Principle

The commands form a **unified SDLC framework**. Use them **in combination**, not isolation:

```
ISOLATED:
[NO] /pb-cycle alone
[NO] /pb-security alone
[NO] /pb-testing alone
[NO] /pb-observability alone

POWERFUL:
[YES] /pb-cycle WITH /pb-testing, /pb-standards, /pb-security
[YES] /pb-plan WITH /pb-adr, /pb-patterns, /pb-observability
[YES] /pb-incident WITH /pb-observability, /pb-deployment, /pb-adr
[YES] /pb-onboarding WITH /pb-knowledge-transfer, /pb-guide, /pb-standards
```

### Key Relationships

1. **Foundation** → All work
   - pb-guide, pb-standards, pb-templates, pb-context

2. **Plan** → Implement
   - pb-plan → pb-adr → pb-patterns → pb-observability → pb-todo-implement

3. **Develop** → Review → Release
   - pb-start → pb-cycle → pb-commit → pb-pr → pb-review-* → pb-release

4. **Safety** → Observability → Incident
   - pb-deployment → pb-observability → pb-incident

5. **Knowledge** → Growth
   - pb-onboarding → pb-knowledge-transfer → pb-team → pb-documentation

### When to Use Each Command

**You'll know you need a command when:**
- `/pb-guide`: You're unsure how a phase works
- `/pb-standards`: You're making a decision on scope or quality
- `/pb-plan`: You're starting a major feature/release
- `/pb-adr`: You've made an architectural decision
- `/pb-patterns-*`: You're designing a system component
- `/pb-start`: You're beginning feature work
- `/pb-cycle`: You've coded something and need review
- `/pb-commit`: You're creating a commit message
- `/pb-pr`: You're merging code
- `/pb-testing`: You're writing tests
- `/pb-todo-implement`: You want checkpoint-based approval
- `/pb-review-*`: You need quality perspective
- `/pb-security`: You need to verify security
- `/pb-deployment`: You're preparing production deploy
- `/pb-incident`: Production is broken
- `/pb-observability`: You need to monitor/trace
- `/pb-onboarding`: Someone new is joining
- `/pb-team`: Team health needs attention
- `/pb-repo-*`: Repository structure needs improvement
- `/pb-context`: You need quick context refresh

---

**This guide is the map. Use it to navigate the playbook as an integrated system.**

*Last Updated: 2026-01-24 | Playbook Version: v2.2.0 | Integration Health: Excellent*
