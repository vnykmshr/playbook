# Workflows: How Commands Work Together

The Engineering Playbook is organized around major workflows. This page shows how commands combine to solve real problems.

---

## Feature Development Workflow

From planning through production, here's how commands work together to deliver features:

```
PLANNING PHASE        DEVELOPMENT PHASE       CODE REVIEW PHASE     RELEASE PHASE
│                     │                       │                      │
├─ /pb-plan           ├─ /pb-start            ├─ /pb-cycle           ├─ /pb-release
│                     │                       │                      │
├─ /pb-adr            ├─ /pb-cycle (iterate)  ├─ /pb-testing         ├─ /pb-deployment
│                     │                       │                      │
├─ /pb-patterns-*     ├─ /pb-testing          ├─ /pb-security        └─ Verify in
│                     │                       │                         production
├─ /pb-observability  ├─ /pb-security         ├─ /pb-logging
│                     │                       │
└─ /pb-performance    ├─ /pb-standards        ├─ /pb-review-*
                      │
                      ├─ /pb-documentation
                      │
                      ├─ /pb-commit
                      │
                      └─ /pb-pr
```

### Step-by-Step Execution

1. **Plan Phase** (before coding)
   - `/pb-plan` — Lock scope, define success criteria, identify risks
   - `/pb-adr` — Document architectural decisions
   - `/pb-patterns-*` — Reference relevant patterns (core, async, database, distributed)
   - `/pb-observability` — Plan monitoring and observability requirements
   - `/pb-performance` — Identify performance targets and constraints

2. **Development Phase** (iterative)
   - `/pb-start` — Create feature branch, establish iteration rhythm
   - `/pb-cycle` — Develop feature:
     - Write code following `/pb-standards`
     - Include tests as you code (`/pb-testing`)
     - Review logging strategy (`/pb-logging`)
     - Update documentation (`/pb-documentation`)
     - Self-review changes
     - Request peer review (quality gates)
   - Repeat until feature is complete

3. **Code Review Phase** (before merging)
   - `/pb-cycle` — Iterate on feedback if needed
   - `/pb-testing` — Verify test coverage and quality
   - `/pb-security` — Security checklist during review
   - `/pb-logging` — Logging standards validation
   - `/pb-review-*` — Additional specialized reviews as needed:
     - `/pb-review-cleanup` — Code quality and patterns
     - `/pb-review-product` — Product alignment (if user-facing)
     - `/pb-review-tests` — Test suite depth and coverage
     - `/pb-review-prerelease` — Final senior engineer review

4. **Commit & PR Phase**
   - `/pb-commit` — Create atomic, well-formatted commit(s)
   - `/pb-pr` — Create pull request with context and rationale

5. **Release Phase** (after merge)
   - `/pb-release` — Pre-release checklist (security, performance, docs)
   - `/pb-deployment` — Choose deployment strategy (blue-green, canary, rolling)
   - Verify in production (monitor, observe)

---

## Incident Response Workflow

When production is down, this workflow guides rapid assessment and recovery:

```
INCIDENT DECLARED     ASSESSMENT               MITIGATION            RECOVERY           POST-INCIDENT
│                     │                        │                      │                  │
├─ PAGE ONCALL        ├─ /pb-incident          ├─ Rollback (fastest)  ├─ /pb-observability├─ /pb-incident
│                     │   (Severity: P0-P3)    │                      │                  │   (Root cause
├─ GATHER INFO        │                        ├─ Hotfix (targeted)   ├─ MONITOR          │    analysis)
│                     ├─ Identify root         │                      │                  │
└─ ESTABLISH          │   cause (quick)        └─ Feature disable     └─ Verify health  └─ /pb-adr
  COMMAND POST        │                           (safest)                                (Document
                      └─ Choose strategy                                                 decision)
```

### Step-by-Step Execution

1. **Incident Declaration** (0 minutes)
   - Page oncall engineer or incident lead
   - Establish command post (Slack channel, bridge, etc.)
   - Gather initial information (what's broken, who's affected, customer impact)

2. **Assessment Phase** (0-5 minutes)
   - `/pb-incident` — Run triage checklist:
     - What's the severity? (P0 = all users, P1 = major subset, P2 = feature, P3 = minor)
     - Quick root cause hypothesis?
     - What's the fastest mitigation? (rollback, hotfix, disable feature)
   - Decide: Rollback, Hotfix, or Feature Disable?

3. **Mitigation Phase** (5-30 minutes, depending on strategy)
   - **Rollback** (fastest, 5-10 min) — Revert last deployment
   - **Hotfix** (targeted, 15-30 min) — Emergency fix, test, deploy
   - **Feature Disable** (safest, 5-15 min) — Kill feature flag, keep code

4. **Recovery & Monitoring** (30+ minutes)
   - `/pb-observability` — Monitor key metrics during recovery:
     - Error rates returning to baseline?
     - Latency normalized?
     - User-visible impact resolved?
   - Maintain open communication with stakeholders

5. **Post-Incident** (within 24 hours)
   - `/pb-incident` — Comprehensive incident review:
     - What was the root cause?
     - How did we miss it pre-deployment?
     - What's the permanent fix?
   - `/pb-adr` — Document decision to prevent recurrence
   - Schedule permanent fix into sprint

---

## Team Onboarding Workflow

Bringing new team members up to speed systematically:

```
PREPARATION           FIRST DAY               FIRST WEEK             RAMP-UP             GROWTH & GROWTH
│                     │                       │                      │                  │
├─ /pb-onboarding     ├─ /pb-start            ├─ /pb-knowledge-      ├─ /pb-cycle        ├─ /pb-team
│   (Setup access)    │   (orientation)       │   transfer           │   (first feature)  │   (feedback)
│                     │                       │                      │                  │
├─ SETUP DEV ENV      ├─ INTRO TO CODEBASE    ├─ /pb-guide           ├─ /pb-pr           ├─ RETROSPECTIVE
│                     │                       │   (SDLC framework)   │                  │
├─ ASSIGN MENTOR      ├─ ROLE CLARIFICATION   ├─ /pb-standards       └─ Peer review     └─ CAREER
│                     │                       │   (working principles)    feedback        DEVELOPMENT
└─ DOCS ACCESS        └─ CALENDAR INVITES     └─ /pb-context
                                              (decisions, roadmap)
```

### Step-by-Step Execution

1. **Preparation Phase** (before hire starts)
   - `/pb-onboarding` — Prepare:
     - Set up development environment
     - Create accounts and access
     - Assign mentor/buddy
     - Gather documentation

2. **First Day**
   - `/pb-start` — Orientation:
     - Welcome, team introductions
     - Development environment walkthrough
     - Assign initial tasks
   - Set up calendar invites for regular syncs

3. **First Week**
   - `/pb-knowledge-transfer` — Transfer knowledge:
     - System architecture overview
     - Key decision history
     - Code organization tour
   - `/pb-guide` — Learn SDLC framework:
     - 11 phases of development
     - Quality gates
     - Review process
   - `/pb-standards` — Learn working principles:
     - Coding standards
     - Communication norms
     - Collaboration expectations
   - `/pb-context` — Understand project:
     - Current roadmap
     - Major decisions
     - Team priorities

4. **Ramp-Up Phase** (weeks 2-4)
   - `/pb-cycle` — Contribute first feature:
     - Pick small feature or bug fix
     - Follow full cycle (plan → develop → review → commit → PR)
     - Get peer feedback
   - Request review, fix feedback, merge PR
   - Build confidence in workflow

5. **Growth Phase** (ongoing)
   - `/pb-team` — Team feedback:
     - Retrospectives
     - 1-on-1s
     - Career development
   - Increase ownership and autonomy
   - Mentor future team members

---

## Periodic Quality Reviews Workflow

Regular check-ins on different aspects of code and team health:

```
MONTHLY CADENCE       QUARTERLY CADENCE       AS-NEEDED
│                     │                       │
├─ /pb-review-cleanup    ├─ /pb-review-hygiene  ├─ /pb-review (comprehensive)
│   (Quality)         │   (Tech debt)        │
│                     │                       ├─ /pb-performance
├─ /pb-review-tests   ├─ /pb-review-product  │   (Bottlenecks)
│   (Coverage)        │   (Fit & vision)     │
│                     │                       ├─ /pb-review-docs
└─ /pb-logging        └─ Team retrospective   │   (Accuracy)
   (Standards)                               └─ /pb-review-prerelease
                                                (Before release)
```

### Recommended Schedule

| Frequency | Review | Purpose |
|-----------|--------|---------|
| Monthly | `/pb-review-cleanup` | Code quality, patterns, maintainability |
| Monthly | `/pb-review-tests` | Test coverage, quality, edge cases |
| Monthly | `/pb-logging` | Logging strategy, standards, compliance |
| Quarterly | `/pb-review-hygiene` | Technical debt, cleanup opportunities |
| Quarterly | `/pb-review-product` | Feature fit, user feedback, roadmap alignment |
| Quarterly | Team retrospective | Team health, communication, growth |
| As-needed | `/pb-review-prerelease` | Final gate before production release |
| As-needed | `/pb-review` | Comprehensive multi-perspective audit |

---

## Pattern Selection Workflow

When designing a new feature or system, follow this workflow to select and combine patterns:

```
UNDERSTAND PROBLEM    SELECT CORE PATTERN     IDENTIFY ASYNC NEEDS  COMPLETE DESIGN
│                     │                       │                      │
├─ Define constraints ├─ /pb-patterns-core    ├─ /pb-patterns-async  ├─ /pb-adr
│                     │   (SOA, events, etc.) │   (callbacks,         │   (Record decision)
├─ Identify goals     │                       │    promises, etc.)   │
│                     ├─ Check for conflicts/ ├─ /pb-patterns-db     ├─ /pb-observability
├─ Consider scale     │   composition         │   (pooling, etc.)     │   (Monitoring plan)
│                     │                       │                      │
└─ Review constraints └─ Validate trade-offs  ├─ /pb-patterns-       └─ /pb-performance
                                             │   distributed         (Perf targets)
                                             │   (saga, CQRS, etc.)
                                             │
                                             └─ Plan combinations
```

### Step-by-Step Execution

1. **Understand Problem**
   - Define requirements and constraints
   - Identify scalability goals
   - List non-functional requirements (latency, throughput, consistency)

2. **Select Core Pattern** (`/pb-patterns-core`)
   - SOA, Event-Driven, Request-Reply, Retry, Circuit Breaker, etc.
   - Match pattern to problem
   - Check for conflicts with existing architecture

3. **Identify Async Needs** (`/pb-patterns-async`)
   - Do you need callbacks, promises, async/await, reactive streams?
   - Worker threads or job queues?
   - Real-time vs. eventual consistency?

4. **Database Considerations** (`/pb-patterns-db`)
   - Connection pooling strategy?
   - Query optimization needed?
   - Replication or sharding?

5. **Distributed System Patterns** (`/pb-patterns-distributed`)
   - Multiple services / microservices?
   - Need saga or distributed transactions?
   - CQRS for read/write separation?

6. **Document Decision** (`/pb-adr`)
   - Record pattern choices
   - Explain trade-offs
   - Document alternative considered

7. **Plan Observability** (`/pb-observability`)
   - How will you monitor?
   - Key metrics to track?
   - Alerting strategy?

8. **Set Performance Targets** (`/pb-performance`)
   - Latency requirements?
   - Throughput targets?
   - Resource limits?

---

## Daily Workflow

A typical day for an engineer using the playbook:

```
MORNING               MIDDAY                AFTERNOON               END OF DAY
│                     │                      │                      │
├─ /pb-resume         ├─ /pb-context         ├─ /pb-cycle            ├─ /pb-pause
│ (Get context)       │ (Big picture)        │ (Final self-review)   │ (Preserve context)
│                     │                      │                      │
├─ /pb-standup        ├─ /pb-patterns        ├─ Ready to ship?       └─ Update trackers,
│ (Write standup)     │ (Plan next work)     │  → /pb-ship             document state
│                     │                      │
└─ /pb-cycle          └─ /pb-cycle           └─ Code review feedback
  (Self-review)         (Develop feature)        (Address if needed)
  (Peer review if ready)
```

**Session boundaries:** `/pb-pause` and `/pb-resume` work as bookends—pause preserves context at end of session, resume recovers it at start of next.

**Shipping:** When focus area is code-complete, use `/pb-ship` for the full journey: specialized reviews → PR → peer review → merge → release → verify.

---

## Next Steps

- **[Decision Guide](decision-guide.md)** — Find the right command for any situation
- **[Command Reference](command-index.md)** — Browse all commands
- **[Integration Guide](integration-guide.md)** — Deep dive on command relationships
