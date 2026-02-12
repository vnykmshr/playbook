---
name: "pb-review"
title: "Comprehensive Project Review"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "reference"
related_commands: ['pb-review-code', 'pb-review-hygiene', 'pb-review-tests', 'pb-security', 'pb-cycle']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Comprehensive Project Review

**Purpose:** Orchestrate multi-perspective reviews by coordinating specialized review commands. Consolidate findings into actionable priorities.

**Recommended Frequency:** Monthly or before major releases

**Mindset:** This review embodies `/pb-preamble` thinking (challenge assumptions, surface risks) and `/pb-design-rules` thinking (verify Clarity, Simplicity, Robustness across the codebase).

**Resource Hint:** opus — orchestrates multiple review perspectives requiring deep cross-cutting analysis

---

## When to Use

- Pre-release comprehensive audit
- Monthly project health check
- After major architectural changes
- Post-incident review
- New team member onboarding (codebase assessment)

---

## Multi-Perspective Reviews (v2.11.0+)

For deeper, more contextualized reviews by complementary personas:

| Review Type | Purpose | Use When |
|-------------|---------|----------|
| `/pb-review-backend` | Systems reliability & testing | Backend code, APIs, data layer |
| `/pb-review-frontend` | User experience & clarity | Frontend code, UI, documentation |
| `/pb-review-infrastructure` | Security & resilience | Infrastructure, deployments, hardening |

**Persona Deep Dives:**
- `/pb-linus-agent` — Security pragmatism and threat modeling
- `/pb-alex-infra` — Systems thinking and resilience design
- `/pb-maya-product` — User impact and scope discipline
- `/pb-sam-documentation` — Clarity and knowledge transfer
- `/pb-jordan-testing` — Test coverage and reliability

See `/pb-preamble` for the team thinking philosophy that enables these perspectives to complement rather than conflict.

---

## Review Tiers

Choose based on available time and review depth needed.

### Quick Review (30 min - 1 hour)

For rapid health check or time-constrained situations.

**Run in parallel:**

| Command | Focus |
|---------|-------|
| `/pb-review-code` | Recent changes quality |
| `/pb-security quick` | Critical security issues |
| `/pb-review-tests` | Test suite health |

**Consolidate:** Top 3 critical issues, immediate next actions.

### Standard Review (2-3 hours)

For monthly reviews or pre-feature-release checks.

**Run in parallel (add to Quick Review):**

| Command | Focus |
|---------|-------|
| `/pb-review-hygiene` | Code quality + operational readiness |
| `/pb-review-docs` | Documentation currency |
| `/pb-logging` | Logging standards |

**Consolidate:** Prioritized issue list with effort estimates.

### Deep Review (Half day)

For major releases, quarterly reviews, or comprehensive audits.

**Run in parallel (add to Standard Review):**

| Command | Focus |
|---------|-------|
| `/pb-review-product` | Engineering + product alignment |
| `/pb-review-microservice` | Architecture (if applicable) |
| `/pb-security deep` | Full security audit |
| `/pb-a11y` | Accessibility compliance |
| `/pb-performance` | Performance review |

**Consolidate:** Full report with executive summary.

---

## Orchestration Process

### Step 1: Scope the Review

Before starting, clarify:

```
- Review tier: Quick / Standard / Deep
- Focus areas: Any specific concerns?
- Scope: Full codebase or changes since [commit/date]?
- Time budget: For review and for fixes?
- Pre-release? If yes, what version?
```

### Step 2: Launch Parallel Reviews

Run the appropriate review commands concurrently:

```
For Quick Review:
  - Launch /pb-review-code for recent changes
  - Launch /pb-security quick
  - Launch /pb-review-tests

For Standard Review (add):
  - Launch /pb-review-hygiene
  - Launch /pb-review-docs
  - Launch /pb-logging

For Deep Review (add):
  - Launch /pb-review-product
  - Launch /pb-review-microservice (if applicable)
  - Launch /pb-security deep
  - Launch /pb-a11y
```

### Step 3: Consolidate Findings

After all reviews complete, synthesize into unified report:

```markdown
## Executive Summary

**Overall Health:** [Good / Needs Attention / At Risk]
**Production Readiness:** [Ready / Conditional / Not Ready]

### Top 5 Priorities
1. [Issue] - [Severity] - [Source review]
2. ...

---

## Issue Tracker

| # | Issue | Severity | Source | Location | Effort |
|---|-------|----------|--------|----------|--------|
| 1 | [Issue description] | CRITICAL | Security | [file:line] | S |
| 2 | [Issue description] | HIGH | Code Quality | [file:line] | M |
...

---

## Quick Wins (< 15 min each)
- [ ] [Action item]
- [ ] [Action item]

## Technical Debt (Track for later)
- [ ] [Item with rationale]

## Deferred (Intentionally not addressing)
- [ ] [Item] - Rationale: [why]
```

### Step 4: Create Action Plan

Prioritize findings into:

1. **CRITICAL** — Must fix before production/release
2. **HIGH** — Should fix soon (this sprint)
3. **MEDIUM** — Address when convenient
4. **LOW** — Nice to have

### Step 5: Track Progress

Create/update review document:

```
todos/project-review-YYYY-MM-DD.md
```

Include:
- Review tier and duration
- Issues found per category
- Items completed
- Remaining items with status
- Commits created for fixes

---

## Specialized Review Commands

| Command | Focus | Use When |
|---------|-------|----------|
| `/pb-review-code` | PR/code change review | Reviewing specific changes |
| `/pb-review-hygiene` | Code quality + operational readiness | Periodic maintenance |
| `/pb-review-tests` | Test suite health | Test coverage concerns |
| `/pb-review-docs` | Documentation quality | Docs need updating |
| `/pb-review-product` | Engineering + product alignment | Strategy alignment |
| `/pb-review-microservice` | Architecture review | Distributed systems |
| `/pb-security` | Security audit | Security-focused review |
| `/pb-logging` | Logging standards | Observability concerns |
| `/pb-a11y` | Accessibility audit | Accessibility compliance |
| `/pb-performance` | Performance review | Performance concerns |
| `/pb-review-playbook` | Playbook meta-review | Reviewing playbook commands |

---

## Review Cadence Recommendations

| Cadence | Tier | Focus |
|---------|------|-------|
| Weekly | Quick | Recent changes, CI health |
| Monthly | Standard | Hygiene, docs, test coverage |
| Quarterly | Deep | Full audit, architecture, security |
| Pre-release | Standard/Deep | Based on release scope |
| Post-incident | Targeted | Affected areas only |

---

## Example Invocation

```
Conduct a Standard Review of this codebase.

Context:
- Pre-release review for v2.0.0
- Changes since commit abc1234
- Time budget: 2 hours review, 4 hours fixes

Priorities:
1. Security (adding user auth features)
2. Test coverage (new payment module)
3. Documentation (API changes)

Create review document at todos/project-review-2026-01-21.md
```

---

## Tips for Effective Reviews

1. **Parallelize** — Run independent reviews concurrently
2. **Focus scope** — Use `git diff` to limit to changed files
3. **Time-box** — Set review duration upfront
4. **Prioritize ruthlessly** — Not every finding needs immediate action
5. **Track progress** — Use the review document across sessions
6. **Follow up** — Schedule remediation session after review

---

## Related Commands

- `/pb-review-code` — Code change review
- `/pb-review-hygiene` — Code quality and operational readiness
- `/pb-review-tests` — Test suite health
- `/pb-security` — Security audit
- `/pb-cycle` — Self-review + peer review iteration

---

**Last Updated:** 2026-01-21
**Version:** 2.0.0
