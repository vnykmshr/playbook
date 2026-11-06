# Playbook Integration Guide

How playbook commands compose into workflows: which command to reach for, workflow maps, and step-by-step scenarios.

---

## Table of Contents

1. [Quick Start: Command Selection](#quick-start-command-selection)
2. [Workflow Maps](#workflow-maps)
3. [Integration Patterns](#integration-patterns)
4. [Common Workflows](#common-workflows-step-by-step)

---

## Quick Start: Command Selection

### By Situation

**Starting a new project?**
→ `/pb-plan` (planning) → `/pb-adr` (architecture) → `/pb-patterns-*` (select patterns) → `/pb-greenfield` (setup)

**Implementing a feature?**
→ `/pb-start` (begin) → code → `/pb-review` (quality gate, commits on pass) → `/pb-pr` (when peer review is needed)

**Implementing a specific todo?**
→ `/pb-todo-implement` (structured checkpoint-based implementation)

**Reviewing code before merge?**
→ `/pb-review` (self-review gate) → `/pb-review-code` (peer review) → `/pb-security` (security review)

**Deep multi-perspective review?**
→ `/pb-review-comprehensive` pairs the five core review personas by change type; `/pb-travis-security`, `/pb-elena-design` and `/pb-kai-reach` hold the security, design and reach lanes

**Reviewing quality periodically?**
→ `/pb-review-tests` (monthly) → `/pb-review-hygiene` (monthly) → `/pb-review-product` (product alignment)

**Deploying to production?**
→ `/pb-release` (pre-release checks) → `/pb-deployment` (strategy selection) → `/pb-observability` (monitoring)

**Incident response?**
→ `/pb-incident` (assessment + mitigation) → `/pb-observability` (monitoring) → Post-incident `/pb-incident` (deep review)

**Onboarding new team member?**
→ `/pb-onboarding` (structured plan) → `/pb-knowledge-transfer` (KT session) → `/pb-guide` (SDLC overview)

**Quick context recovery?**
→ `/pb-resume` (get back in context) → `/pb-context` (refresh decision log)

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
│  ├─ Code + tests (/pb-testing)
│  └─ /pb-review          ← Quality gate; commits on pass
│
└─ Repeat for each task

CODE REVIEW
├─ /pb-pr                 ← Create pull request
├─ /pb-review-code        ← Peer review
├─ /pb-review-tests       ← Test coverage
├─ /pb-logging            ← Logging standards
├─ /pb-security           ← Security review
├─ /pb-review-product     ← Product alignment (if user-facing)
└─ Approve / Request changes

PRE-RELEASE
├─ /pb-release            ← Phase 1 readiness gate
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
├─ /pb-start                 ← Implement prevention fixes
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
├─ /pb-review                ← Quality gate on each unit of work
└─ /pb-team                  ← Ongoing feedback and growth
```

### Workflow 5: Periodic Quality Reviews

```
WEEKLY
└─ /pb-logging               ← Log quality check

MONTHLY
├─ /pb-review-hygiene        ← Code quality and dependency health
├─ /pb-review-tests          ← Test suite health
├─ /pb-observability         ← Dashboard and alert tuning
└─ /pb-review-product        ← Product alignment

QUARTERLY
├─ /pb-review-docs           ← Documentation audit
├─ /pb-security              ← Security deep dive
└─ /pb-team                  ← Team retrospective

RELEASE
├─ /pb-release     ← Final release gate
├─ /pb-security              ← Security review
└─ /pb-review-microservice   ← If applicable
```

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
/pb-plan → /pb-adr → /pb-patterns → /pb-todo-implement → /pb-review → /pb-pr → /pb-release
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
DEVELOPMENT PHASE → /pb-start, /pb-review, /pb-pr, /pb-testing, /pb-todo-implement
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
├─ LOOP, per unit of work:
│  ├─ Code changes
│  ├─ /pb-testing (add tests)
│  └─ /pb-review (quality gate, commits on pass)
└─ /pb-pr (create pull request)

STEP 3: Code Review
├─ /pb-review-code (peer review)
├─ /pb-review-product (product alignment)
├─ /pb-security (security review)
├─ /pb-review-tests (test coverage)
└─ Approve / Merge

STEP 4: Release Preparation
├─ /pb-release (Phase 1 readiness gate)
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
└─ /pb-review (quality gate)

STEP 3: Code Review
├─ /pb-review-code (fast-track peer review)
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
├─ /pb-review-code (architecture alignment)
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
├─ /pb-review-code (code review feedback)
└─ /pb-team (feedback and support)

ONGOING: Growth
├─ /pb-review (each unit of work)
├─ /pb-standards (reinforce principles)
└─ /pb-team (regular feedback)
```

---

## Summary: Playbook as Unified System

### Key Relationships

1. **Foundation** → All work
   - pb-guide, pb-standards, pb-templates, pb-context

2. **Plan** → Implement
   - pb-plan → pb-adr → pb-patterns → pb-observability → pb-todo-implement

3. **Develop** → Review → Release
   - pb-start → pb-review → pb-pr → pb-release

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
- `/pb-review`: You've finished a unit of work
- `/pb-cycle`: You want the manual self-review and peer-review loop
- `/pb-commit`: You're committing by hand
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

