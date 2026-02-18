---
name: "pb-review-hygiene"
title: "Codebase Hygiene Review (Periodic Health Check)"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review', 'pb-review-code', 'pb-review-tests', 'pb-security', 'pb-repo-organize']
last_reviewed: "2026-02-18"
last_evolved: "2026-02-18"
version: "2.0.0"
version_notes: "v2.13.1: Clarified purpose as periodic health check (not specific code review). Part of code review family decision tree."
breaking_changes: []
---
# Codebase Hygiene Review (Periodic Health Check)

**Purpose:** Periodic, codebase-wide review of code quality and operational readiness. Combines cleanup (code patterns, duplication, complexity) and hygiene (operational health, dependencies, documentation).

**Use when:** You want a **periodic audit** of your entire codebase (not a specific PR). Monthly or before starting new development.

**When NOT to use:** For reviewing specific code changes (use `/pb-review-code` instead) or focusing on test quality (use `/pb-review-tests` instead).

**Recommended Frequency:** Monthly or before starting new development

**Mindset:** This review embodies `/pb-preamble` thinking (surface flaws directly, challenge assumptions) and `/pb-design-rules` thinking (Clarity, Simplicity, Modularity, Robustness).

Challenge hidden assumptions about what "health" means. Surface risks directly. Focus on reducing complexity and tech debt. Don't soften findings to be diplomatic.

**Resource Hint:** opus — comprehensive hygiene review spans code quality, operations, security, and documentation across entire codebase

---

## Code Review Family Decision Tree

See `/pb-review-code` for the complete decision tree. Key distinction:

- **Use `/pb-review-code`** for reviewing a specific PR or commit
- **Use `/pb-review-hygiene`** for periodic (monthly) health checks of entire codebase
- **Use `/pb-review-tests`** for test suite quality and coverage focus

---

## When to Use

- **Monthly maintenance check** ← Primary use case (scheduled, periodic)
- **Before starting a fresh round of development** (cleanup mode)
- **Pre-release operational readiness assessment**
- **After major refactoring** (verify patterns still clean)
- **When codebase feels "heavy"** or hard to work with (signal that health check is needed)

---

## Review Perspectives

Act as these roles simultaneously:

1. **Senior Engineer** — Technical soundness, codebase cleanliness, dependency health
2. **Technical Architect** — System design, infrastructure readiness, scalability
3. **DevOps/Operations** — Automation, deployment, observability coverage
4. **Security Reviewer** — Security posture, compliance gaps

---

## Part 1: Code Quality (Cleanup Focus)

### 1.1 Repository Health Check

- [ ] Repo structure aligns with best practices (scripts, configs, docs clearly separated)
- [ ] Versioning, tags, and branches are clear and consistent
- [ ] README accurately describes purpose, setup, and usage
- [ ] LICENSE, CONTRIBUTING, and CHANGELOG are present and current

### 1.2 Code Review and Cleanup

- [ ] Remove duplication across scripts/modules (dedupe functions, configs)
- [ ] Consolidate constants, paths, config variables into single source of truth
- [ ] Strip unused code, comments, placeholders from prior iterations
- [ ] Refactor overly complex logic into simple, maintainable patterns

### 1.3 AI/Boilerplate Bloat Detection

Look for telltale signs of over-generation:

| Signal | Example | Action |
|--------|---------|--------|
| Generic error handling | `catch(e) { /* ignore */ }` | Add meaningful handling |
| Repeated boilerplate | Same setup in 10 test files | Extract to shared fixture |
| Over-commenting | Comments stating the obvious | Remove or rewrite |
| Verbose naming | `theUserWhoIsCurrentlyLoggedIn` | Simplify to `currentUser` |
| Copy-paste artifacts | Code from unrelated projects | Remove or adapt |

### 1.4 Telltale Signs Checklist

- [ ] No generic error handling that hides useful context
- [ ] No repeated boilerplate where a function/loop is better
- [ ] No over-commenting or comments stating the obvious
- [ ] No inconsistent variable names
- [ ] No copy-paste leftovers from unrelated projects

---

## Part 2: Operational Readiness (Hygiene Focus)

### 2.1 Codebase Health

- [ ] Clear, readable structure with no major dead code
- [ ] Dependencies up to date and pinned
- [ ] Build scripts and Makefiles functional and minimal
- [ ] Linting, formatting, and static checks passing
- [ ] Sensitive info (API keys, creds) properly excluded

### 2.2 Tests and Quality Gates

- [ ] Unit/integration tests running in CI
- [ ] Coverage reports available and meaningful
- [ ] Flaky tests identified and tracked
- [ ] Test data sane and isolated

### 2.3 Documentation and Metadata

- [ ] README covers setup, run, and contribution steps
- [ ] Architecture overview updated with recent changes
- [ ] Owner/maintainer info available
- [ ] CHANGELOG reflects recent changes

### 2.4 CI/CD and Infrastructure

- [ ] Pipelines consistent, reproducible, and passing
- [ ] Deployments versioned and auditable
- [ ] Monitoring, alerting, and rollback procedures exist
- [ ] Environment variables and secrets documented

### 2.5 Security and Compliance

- [ ] Dependencies scanned for vulnerabilities
- [ ] Secrets properly stored (Vault, Secret Manager, etc.)
- [ ] Logging and access controls verified
- [ ] No unpatched services or public exposure risks

### 2.6 Operational Readiness

- [ ] New engineer can onboard easily
- [ ] Recovery/runbooks available for production issues
- [ ] Resource usage (CPU, memory, DB) monitored
- [ ] Error budgets or SLAs tracked

---

## Human-Level Sanity Check

Ask these questions:

| Question | Target |
|----------|--------|
| **Readability** | Can another engineer grasp intent at a glance? |
| **Minimalism** | Does each line have a purpose? |
| **Maintainability** | Can future contributors extend it easily? |
| **Consistency** | Does the repo feel like it was written by one person? |

---

## Quick Wins Identification

List small improvements (< 2 hours each) that yield immediate benefits:

Examples:
- Update README section with current setup steps
- Remove unused Docker image from CI
- Add missing env var documentation
- Enable Dependabot for dependency updates
- Refresh lock file to remove vulnerabilities
- Delete dead code module

---

## Deliverables

### 1. Executive Summary

3-5 bullet overview of overall health:
- **Good** — Minor issues, ready for development
- **Needs Attention** — Notable issues, address before heavy development
- **At Risk** — Critical issues, stop and fix first

### 2. Key Findings

Grouped by category with severity tags:

| Category | Finding | Severity | Location |
|----------|---------|----------|----------|
| Codebase | Dead code in utils/ | Medium | utils/legacy.ts |
| Security | Hardcoded API key | Critical | config.ts:45 |
| Docs | README setup outdated | Minor | README.md |

### 3. Quick Wins List

Practical actions sorted by effort:
1. [15 min] Remove unused imports in 5 files
2. [30 min] Update README quickstart
3. [1 hour] Add missing error handling in API client

### 4. Next Review Focus

Areas that need deeper follow-up next cycle.

---

## Example Output

```markdown
## Executive Summary

**Overall Health:** Needs Attention

- Codebase is generally clean but has accumulated dead code in utils/
- Security posture is good, no critical vulnerabilities found
- Documentation is stale, README doesn't match current setup
- Test coverage is adequate but 3 flaky tests need attention
- Dependencies are 6 months old, recommend update cycle

## Key Findings

| Category | Finding | Severity | Location |
|----------|---------|----------|----------|
| Codebase | 200+ lines of dead code | Medium | utils/legacy.ts |
| Codebase | Duplicate config loading | Low | config/*.ts |
| Tests | 3 flaky tests | Medium | tests/api.test.ts |
| Docs | Outdated quickstart | Medium | README.md |
| Deps | 12 outdated packages | Low | package.json |

## Quick Wins

1. [15 min] Delete utils/legacy.ts (confirmed unused)
2. [30 min] Fix README quickstart section
3. [1 hour] Update 12 outdated dependencies
4. [2 hours] Investigate and fix flaky tests

## Next Review Focus

- Deep security audit before v2.0 release
- Performance review after new caching layer
```

---

## Related Commands

- `/pb-review` — Orchestrate comprehensive multi-perspective review
- `/pb-review-code` — Code change review for PRs
- `/pb-review-tests` — Test suite health review
- `/pb-security` — Security audit
- `/pb-repo-organize` — Clean up repository structure

---

**Last Updated:** 2026-01-21
**Version:** 2.0.0
