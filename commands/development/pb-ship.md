---
name: "pb-ship"
title: "Ship Focus Area to Production"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-cycle', 'pb-pr', 'pb-release', 'pb-review-hygiene', 'pb-deployment']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Ship Focus Area to Production

Complete a focus area through comprehensive review, PR creation, peer review, merge, release, and verification. This is the full journey from "code complete" to "in production."

**Mindset:** This command embodies `/pb-preamble` thinking (challenge readiness assumptions, surface risks directly) and `/pb-design-rules` thinking (verify Clarity, Robustness, Simplicity before shipping).

Ship when ready, not when tired. Every review step is an opportunity to find issues—embrace them.

**Resource Hint:** sonnet — review orchestration and release coordination

---

## When to Use This Command

- **Focus area complete** — Feature/fix is code-complete, ready for final review
- **Release candidate** — Preparing a version for production
- **End of sprint** — Shipping accumulated work
- **Milestone delivery** — Completing a planned deliverable

---

## The Ship Workflow

```
PHASE 1              PHASE 2                PHASE 3           PHASE 4              PHASE 5
FOUNDATION           SPECIALIZED REVIEWS    FINAL GATE        PR & PEER REVIEW     MERGE & RELEASE
│                    │                      │                 │                    │
├─ Quality gates     ├─ /pb-review-docs     ├─ /pb-release    ├─ /pb-pr            ├─ Merge PR
│  (lint,test,type)  │  (REQUIRED)          │  Phase 1        │                    │
│                    │                      │  (readiness)    ├─ Peer review       ├─ /pb-release
├─ /pb-cycle         ├─ /pb-review-hygiene  │                 │  (scoped to PR)    │  Phase 2-3
│  (self-review)     │  (code quality)      └─ Ship decision  │                    │  (tag, deploy)
│                    │                         (go/no-go)     ├─ Address feedback  │
└─ Release artifacts ├─ /pb-review-hygiene                    │                    ├─ /pb-deployment
   (CHANGELOG etc)   │  (project health)                      └─ Approved sign-off │
                     │                                                             └─ Summarize
                     ├─ /pb-review-tests
                     │  (coverage)
                     │
                     ├─ /pb-security
                     │  (vulnerabilities)
                     │
                     └─ /pb-logging
                        (standards)
```

---

## Release Type Quick Reference

| Release Type | Phase 1 | Phase 2 | Phase 3 | Phase 4-5 |
|--------------|---------|---------|---------|-----------|
| Versioned (vX.Y.Z) | Full + Artifacts | At least `/pb-review-docs` | Required | Required |
| S-tier versioned | Full + Artifacts | `/pb-review-docs` only | Quick check | Required |
| Hotfix (no tag) | Quality gates | Optional | Skip | Streamlined |
| Trivial (typo) | Lint only | Skip | Skip | Quick merge |

**Key rule:** Any release that will be tagged (vX.Y.Z) requires CHANGELOG verification.

---

## Phase 1: Foundation

Establish a clean baseline before specialized reviews.

### Step 1.1: Run Quality Gates

```bash
# Run all quality checks
make lint        # or: npm run lint / ruff check
make typecheck   # or: npm run typecheck / mypy
make test        # or: npm test / pytest
```

**Checkpoint:** All gates must pass before proceeding. Fix failures now, not later.

### Step 1.2: Verify CI Status (If Configured)

If the project has CI configured, verify it passes before proceeding:

```bash
# Check latest CI run status
gh run list --limit 3

# View details of a specific run
gh run view [RUN_ID]

# Wait for CI to complete if running
gh run watch

# Check PR-specific CI status (if PR already exists)
gh pr checks [PR-NUMBER]
```

**CI Verification Checklist:**
- [ ] Latest CI run on current branch is passing
- [ ] No flaky test failures (if failures, investigate root cause)
- [ ] All required checks are green

**Non-negotiable:** If CI is configured for the project, it MUST pass before shipping. Do not proceed with "it was passing yesterday" or "it's just a flaky test." Fix the CI first.

**No CI configured?** Skip this step, but consider adding CI as a follow-up task (`/pb-review-hygiene`).

### Step 1.3: Basic Self-Review

Run `/pb-cycle` for a quick self-review:

- [ ] No debug code (console.log, print statements)
- [ ] No commented-out code
- [ ] No hardcoded secrets or credentials
- [ ] No TODO/FIXME for critical items
- [ ] Changes match the intended scope

### Step 1.4: Release Artifacts Check

**Required for any versioned release (vX.Y.Z):**

```bash
# Verify CHANGELOG has entry for this version
grep -E "## \[v?X\.Y\.Z\]" CHANGELOG.md docs/CHANGELOG.md 2>/dev/null

# Verify version tag doesn't already exist
git tag -l "vX.Y.Z"

# Check version in package files (if applicable)
# For Go: no version file typically
# For Node: grep version package.json
# For Python: grep version pyproject.toml
```

**Release Artifacts Checklist:**
- [ ] CHANGELOG.md has entry for this version with date
- [ ] All changes documented in CHANGELOG (Added, Changed, Fixed, Removed)
- [ ] Version links added at bottom of CHANGELOG
- [ ] Version number updated in package files (if applicable)
- [ ] Release notes drafted (can use CHANGELOG entry)

**This check is NOT optional for versioned releases. No exceptions.**

---

## Phase 2: Specialized Reviews

Run reviews based on release type. Track issues found and address them before moving to the next.

### Minimum Required (ALL versioned releases)

**Step 2.1: Documentation Review (REQUIRED)**

Run `/pb-review-docs`:

- [ ] CHANGELOG.md updated with this version's entry
- [ ] README accurate (installation, usage examples)
- [ ] API docs updated (if applicable)
- [ ] Code comments meaningful (not obvious)
- [ ] Migration guide updated (if breaking changes)

**Do not proceed without completing this review for versioned releases.**

### Full Suite (M/L tier releases, recommended for all)

**Step 2.2: Code Quality Review**

Run `/pb-review-hygiene`:

- [ ] Code patterns are consistent
- [ ] No duplication (DRY)
- [ ] No AI-generated bloat
- [ ] Naming conventions followed
- [ ] Complexity is justified

**Address issues before proceeding.**

**Step 2.3: Project Hygiene Review**

Run `/pb-review-hygiene`:

- [ ] Dependencies up to date
- [ ] No dead code or unused modules
- [ ] CI/CD pipeline healthy
- [ ] Configuration is clean
- [ ] No stale files

**Address issues before proceeding.**

**Step 2.4: Test Coverage Review**

Run `/pb-review-tests`:

- [ ] Critical paths have coverage
- [ ] Edge cases tested
- [ ] No flaky tests
- [ ] Test quality is good (not just coverage %)
- [ ] Integration tests for key flows

**Address issues before proceeding.**

**Step 2.5: Security Review**

Run `/pb-security`:

- [ ] No secrets in code
- [ ] Input validation at boundaries
- [ ] SQL injection prevention
- [ ] XSS/CSRF protection (if applicable)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Auth/authz properly implemented

**Address CRITICAL/HIGH issues before proceeding. Document deferred items.**

**Step 2.6: Logging Review (Optional)**

Run `/pb-logging` if backend/API changes:

- [ ] Structured logging used
- [ ] No secrets in logs
- [ ] Appropriate log levels
- [ ] Request tracing in place
- [ ] Error context preserved

### Issue Tracking Template

Create or update `todos/ship-review-YYYY-MM-DD.md`:

```markdown
# Ship Review: [Feature/Focus Area]
**Date:** YYYY-MM-DD
**Branch:** [branch-name]
**Version:** vX.Y.Z

## Release Artifacts
- [ ] CHANGELOG.md updated
- [ ] Version links added
- [ ] Release notes drafted

## Issues Found

### From pb-review-docs (REQUIRED)
| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | [description] | HIGH/MED/LOW | FIXED/DEFERRED |

### From pb-review-hygiene
| # | Issue | Severity | Status |
|---|-------|----------|--------|

[... other sections ...]

## Summary
- Total issues: X
- Critical: X (must fix)
- High: X (should fix)
- Medium: X (address if time)
- Low: X (defer)
- Fixed: X
- Deferred: X (with rationale)
```

---

## Phase 3: Final Gate

### Step 3.1: Release Readiness Review

Run `/pb-release` Phase 1 (Readiness Gate):

This is the senior engineer final gate. Review with fresh eyes:

- [ ] Release checklist complete
- [ ] Code is production-ready
- [ ] All CRITICAL/HIGH issues addressed
- [ ] Deferred items documented with rationale
- [ ] Rollback plan exists

### Step 3.2: Ship Decision

**Go/No-Go Checklist:**

- [ ] All quality gates pass
- [ ] **CI passes** (if configured) ← REQUIRED
- [ ] All CRITICAL issues fixed
- [ ] All HIGH issues fixed (or explicitly deferred with approval)
- [ ] **CHANGELOG.md updated with this version's entry** ← REQUIRED
- [ ] **Version links added to CHANGELOG** ← REQUIRED
- [ ] Documentation is accurate
- [ ] Team is aware of the release
- [ ] Rollback plan tested

**Decision:** GO / NO-GO

If NO-GO, document blockers and return to appropriate phase.

---

## Phase 4: PR & Peer Review

### Step 4.1: Create Pull Request

Run `/pb-pr`:

```bash
# Create PR with comprehensive context
gh pr create --title "[type]: brief description" --body "$(cat <<'EOF'
## Summary
[1-3 bullet points: what and why]

## Changes
[Key changes, grouped logically]

## Review Focus
[What reviewers should pay attention to]

## Test Plan
[How to verify this works]

## Ship Review
- Release artifacts: PASS (CHANGELOG updated)
- Code quality: PASS
- Hygiene: PASS
- Tests: PASS
- Security: PASS
- Docs: PASS
- Pre-release: PASS

Issues addressed: X | Deferred: X (see todos/ship-review-*.md)
EOF
)"
```

### Step 4.2: Request Peer Review

Run `/code-review:code-review` or `/pb-review` scoped to PR changes:

```bash
# Get the diff for context
gh pr diff [PR-NUMBER]

# Or review specific files
gh pr view [PR-NUMBER] --json files
```

**Review scope:** Focus reviewer attention on:
1. Logic correctness
2. Edge cases
3. Security implications
4. Performance concerns
5. Maintainability

### Step 4.3: Submit Feedback

Add review findings as PR comments:

```markdown
## Review Feedback

### Must Address (Blocking)
- [ ] [Issue 1 with file:line reference]
- [ ] [Issue 2 with file:line reference]

### Should Address (Non-blocking)
- [ ] [Suggestion 1]
- [ ] [Suggestion 2]

### Notes
- [Observation or question]
```

### Step 4.4: Address Feedback & Iterate

For each feedback item:

1. **Address** — Fix the issue
2. **Respond** — Comment explaining the fix or decision
3. **Re-request** — Ask for re-review

```bash
# After addressing feedback
git add -A && git commit -m "fix: address review feedback"
git push

# Re-request review
gh pr ready [PR-NUMBER]
```

### Step 4.5: Get Approved Sign-Off

**Approval criteria:**
- All blocking items addressed
- Reviewer explicitly approves
- **CI passes on final commit** (non-negotiable if CI is configured)

```bash
# Check PR status and CI checks
gh pr checks [PR-NUMBER]
gh pr status

# Ensure all checks pass - DO NOT merge with failing CI
gh pr checks [PR-NUMBER] --required
```

**CI Gate:** If CI is configured, all required checks must be green before merge. No exceptions. If CI is red:
1. Investigate the failure
2. Fix the issue (don't dismiss as flaky)
3. Push the fix
4. Wait for CI to pass
5. Then proceed with approval

**Approval comment template:**

```markdown
## Approved

- [x] Code quality verified
- [x] Security considerations reviewed
- [x] Test coverage adequate
- [x] Documentation accurate
- [x] CHANGELOG updated
- [x] Ready for production

LGTM - Ship it!
```

---

## Phase 5: Merge & Release

### Step 5.1: Final CI Check & Merge PR

**Before merging, verify CI one final time:**

```bash
# Verify all checks pass
gh pr checks [PR-NUMBER]

# If any checks are failing, DO NOT proceed
# Fix the issue first, then return here
```

**Only when all checks are green:**

```bash
# Squash merge (recommended for clean history)
gh pr merge [PR-NUMBER] --squash --delete-branch

# Or merge commit if preserving history matters
gh pr merge [PR-NUMBER] --merge --delete-branch
```

**Note:** If your repository has branch protection rules requiring CI to pass, the merge will be blocked automatically. If not, enforce this discipline manually.

### Step 5.2: Release

Run `/pb-release`:

```bash
# Verify main is updated
git checkout main && git pull

# Tag the release
git tag -a vX.Y.Z -m "vX.Y.Z - Brief description"
git push origin vX.Y.Z

# Create GitHub release (use CHANGELOG entry for notes)
gh release create vX.Y.Z --title "vX.Y.Z - Title" --notes "..."

# Deploy
make deploy  # or your deployment command
```

### Step 5.3: Verify Release

```bash
# Health check
curl -s [PROD_URL]/api/health | jq

# Smoke test critical flows
# [Project-specific verification commands]

# Monitor for errors
# [Check logs, dashboards, alerts]
```

**Verification checklist:**
- [ ] Health endpoint returns OK
- [ ] Critical user flows work
- [ ] No new errors in logs
- [ ] Metrics look normal
- [ ] Alerts are quiet

### Step 5.4: Release Summary

Update `todos/ship-review-YYYY-MM-DD.md`:

```markdown
## Release Summary

**Version:** vX.Y.Z
**Released:** YYYY-MM-DD HH:MM
**PR:** #[number]
**Commit:** [hash]

### What Shipped
- [Feature/fix 1]
- [Feature/fix 2]

### Review Stats
- Reviews completed: 6
- Issues found: X
- Issues fixed: X
- Issues deferred: X

### Verification
- Health check: PASS
- Smoke tests: PASS
- Monitoring: NOMINAL

### Notes
- [Any observations, learnings, or follow-ups]

### Next Steps
- [ ] Monitor for 24h
- [ ] [Any follow-up tasks]
```

---

## Escape Hatch: Trivial Changes Only

For genuinely trivial changes (typo fix, comment update, README tweak):

```bash
# Phase 1: Foundation (still required)
make lint && make test
gh run list --limit 1  # Verify CI passes (if configured)

# Phase 2: Pick ONE relevant review
# /pb-review-hygiene (if code touched)
# /pb-review-docs (if docs touched)

# Phase 3: Skip

# Phase 4: PR (streamlined)
/pb-pr
# Quick peer review
# Get approval

# Phase 5: Ship
gh pr merge --squash --delete-branch
git checkout main && git pull
make deploy
```

**IMPORTANT: This escape hatch is NOT for versioned releases.**

Any release that will be tagged (vX.Y.Z) requires:
1. Phase 1 **including Release Artifacts Check**
2. `/pb-review-docs` from Phase 2 (CHANGELOG verification) — **MANDATORY**
3. Phase 3 Go/No-Go checklist
4. Full Phase 4-5

The escape hatch is for:
- Fixing a typo in documentation
- Updating a comment
- Minor config tweaks
- Hotfixes that don't warrant a version bump

**NOT for:**
- Any logic change
- Any new functionality
- Any test changes
- Any configuration changes
- Anything touching security, auth, or data
- **Any versioned release (vX.Y.Z)**

---

## Parallel Reviews (Advanced)

For faster shipping, some reviews can run in parallel:

```
Sequential (dependencies):
  pb-review-docs (REQUIRED FIRST) → pb-review-hygiene

Parallel (independent):
  ├─ pb-review-tests
  ├─ pb-security
  └─ pb-logging

Sequential (needs stable code):
  All above → pb-release (Phase 1: Readiness Gate)
```

---

## Troubleshooting

### Review found too many issues

- **Prioritize:** CRITICAL > HIGH > MEDIUM > LOW
- **Timebox:** Set a limit for fixes this session
- **Defer wisely:** Document deferred items with rationale
- **Don't ship debt:** If CRITICAL issues remain, don't ship

### PR feedback cycle taking too long

- **Scope PRs smaller:** Break into multiple PRs
- **Front-load reviews:** Self-review thoroughly before PR
- **Communicate:** Align on expectations with reviewer

### Release verification failed

- **Rollback immediately:** If critical
- **Investigate:** Check logs, recent changes
- **Hotfix or disable:** Choose based on severity
- **Run /pb-incident:** If production impact

### Forgot to update CHANGELOG

If discovered after merge but before tag:
```bash
# Update CHANGELOG on main
git checkout main && git pull
# Edit CHANGELOG.md
git add CHANGELOG.md && git commit -m "docs: add vX.Y.Z changelog entry"
git push
# Then proceed with tagging
```

If discovered after tag:
```bash
# Update CHANGELOG and create patch release or amend release notes
gh release edit vX.Y.Z --notes "..."
```

---

## Integration with Playbook

**Part of development workflow:**
```
/pb-start → /pb-cycle (iterate) → /pb-pause/resume → /pb-ship
                                                        │
                                    ┌───────────────────┘
                                    ↓
                              Foundation
                              + Release Artifacts ← NEW
                                    ↓
                           Specialized Reviews
                           (docs REQUIRED)      ← CLARIFIED
                                    ↓
                              Final Gate
                              (CHANGELOG check) ← ADDED
                                    ↓
                            PR & Peer Review
                                    ↓
                            Merge & Release
                                    ↓
                                Verify
```

## Related Commands

- `/pb-cycle` — Self-review and peer review before shipping
- `/pb-pr` — Create pull request for review
- `/pb-release` — Detailed release tagging and notes
- `/pb-review-hygiene` — Code and project health review
- `/pb-deployment` — Deployment strategies and verification

---

## Checklist Summary

```
PHASE 1: FOUNDATION
[ ] Quality gates pass (lint, typecheck, test)
[ ] CI passes (if configured) ← REQUIRED
[ ] Basic self-review complete (/pb-cycle)
[ ] Release artifacts verified (CHANGELOG, version)

PHASE 2: SPECIALIZED REVIEWS
[ ] /pb-review-docs — REQUIRED for versioned releases ← CLARIFIED
[ ] /pb-review-hygiene — code quality (recommended)
[ ] /pb-review-hygiene — project health (recommended)
[ ] /pb-review-tests — test coverage (recommended)
[ ] /pb-security — vulnerabilities (recommended)
[ ] /pb-logging — logging standards (optional)

PHASE 3: FINAL GATE
[ ] /pb-release Phase 1 — readiness gate (senior sign-off)
[ ] CHANGELOG.md verified
[ ] Ship decision: GO

PHASE 4: PR & PEER REVIEW
[ ] PR created (/pb-pr)
[ ] Peer review complete
[ ] Feedback addressed
[ ] Approved sign-off received
[ ] CI passes on final commit ← REQUIRED

PHASE 5: MERGE & RELEASE
[ ] Final CI verification (all checks green)
[ ] PR merged
[ ] /pb-release Phase 2-3 — version, tag, GitHub release
[ ] /pb-deployment — execute deployment, verify
[ ] Summary documented
```

---

*Ship with confidence. Every review is a gift. Never skip CHANGELOG. Never merge with red CI.*
