# Ship Focus Area to Production

Complete a focus area through comprehensive review, PR creation, peer review, merge, release, and verification. This is the full journey from "code complete" to "in production."

**Mindset:** This command embodies `/pb-preamble` thinking (challenge readiness assumptions, surface risks directly) and `/pb-design-rules` thinking (verify Clarity, Robustness, Simplicity before shipping).

Ship when ready, not when tired. Every review step is an opportunity to find issues—embrace them.

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
├─ Quality gates     ├─ /pb-review-cleanup  ├─ /pb-review-    ├─ /pb-pr            ├─ Merge PR
│  (lint,test,type)  │  (code quality)      │  prerelease     │                    │
│                    │                      │  (senior gate)  ├─ Peer review       ├─ /pb-release
└─ /pb-cycle         ├─ /pb-review-hygiene  │                 │  (scoped to PR)    │
   (self-review)     │  (project health)    └─ Ship decision  │                    ├─ Verify
                     │                         (go/no-go)     ├─ Address feedback  │
                     ├─ /pb-review-tests                      │                    └─ Summarize
                     │  (coverage)                            └─ Approved sign-off
                     │
                     ├─ /pb-security
                     │  (vulnerabilities)
                     │
                     ├─ /pb-logging
                     │  (standards)
                     │
                     └─ /pb-review-docs
                        (accuracy)
```

---

## Phase 1: Foundation

Establish a clean baseline before specialized reviews.

### Step 1.1: Run Quality Gates

```bash
# Run all quality checks
make lint        # or: npm run lint / ruff check
make typecheck   # or: npm run typecheck / mypy
make test        # or: npm test / pytest

# Verify CI status
gh run list --limit 1
```

**Checkpoint:** All gates must pass before proceeding. Fix failures now, not later.

### Step 1.2: Basic Self-Review

Run `/pb-cycle` for a quick self-review:

- [ ] No debug code (console.log, print statements)
- [ ] No commented-out code
- [ ] No hardcoded secrets or credentials
- [ ] No TODO/FIXME for critical items
- [ ] Changes match the intended scope

---

## Phase 2: Specialized Reviews

Run each review sequentially. Track issues found and address them before moving to the next.

### Issue Tracking Template

Create or update `todos/ship-review-YYYY-MM-DD.md`:

```markdown
# Ship Review: [Feature/Focus Area]
**Date:** YYYY-MM-DD
**Branch:** [branch-name]

## Issues Found

### From pb-review-cleanup
| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | [description] | HIGH/MED/LOW | FIXED/DEFERRED |

### From pb-review-hygiene
| # | Issue | Severity | Status |
|---|-------|----------|--------|

### From pb-review-tests
| # | Issue | Severity | Status |
|---|-------|----------|--------|

### From pb-security
| # | Issue | Severity | Status |
|---|-------|----------|--------|

### From pb-logging
| # | Issue | Severity | Status |
|---|-------|----------|--------|

### From pb-review-docs
| # | Issue | Severity | Status |
|---|-------|----------|--------|

## Summary
- Total issues: X
- Critical: X (must fix)
- High: X (should fix)
- Medium: X (address if time)
- Low: X (defer)
- Fixed: X
- Deferred: X (with rationale)
```

### Step 2.1: Code Quality Review

Run `/pb-review-cleanup`:

- [ ] Code patterns are consistent
- [ ] No duplication (DRY)
- [ ] No AI-generated bloat
- [ ] Naming conventions followed
- [ ] Complexity is justified

**Address issues before proceeding.**

### Step 2.2: Project Hygiene Review

Run `/pb-review-hygiene`:

- [ ] Dependencies up to date
- [ ] No dead code or unused modules
- [ ] CI/CD pipeline healthy
- [ ] Configuration is clean
- [ ] No stale files

**Address issues before proceeding.**

### Step 2.3: Test Coverage Review

Run `/pb-review-tests`:

- [ ] Critical paths have coverage
- [ ] Edge cases tested
- [ ] No flaky tests
- [ ] Test quality is good (not just coverage %)
- [ ] Integration tests for key flows

**Address issues before proceeding.**

### Step 2.4: Security Review

Run `/pb-security`:

- [ ] No secrets in code
- [ ] Input validation at boundaries
- [ ] SQL injection prevention
- [ ] XSS/CSRF protection (if applicable)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Auth/authz properly implemented

**Address CRITICAL/HIGH issues before proceeding. Document deferred items.**

### Step 2.5: Logging Review (Optional)

Run `/pb-logging` if backend/API changes:

- [ ] Structured logging used
- [ ] No secrets in logs
- [ ] Appropriate log levels
- [ ] Request tracing in place
- [ ] Error context preserved

### Step 2.6: Documentation Review

Run `/pb-review-docs`:

- [ ] README accurate
- [ ] API docs updated (if applicable)
- [ ] Code comments meaningful (not obvious)
- [ ] Architecture docs current
- [ ] CHANGELOG updated

---

## Phase 3: Final Gate

### Step 3.1: Pre-Release Review

Run `/pb-review-prerelease`:

This is the senior engineer final gate. Review with fresh eyes:

- [ ] Release checklist complete
- [ ] Code is production-ready
- [ ] All CRITICAL/HIGH issues addressed
- [ ] Deferred items documented with rationale
- [ ] Rollback plan exists

### Step 3.2: Ship Decision

**Go/No-Go Checklist:**

- [ ] All quality gates pass
- [ ] All CRITICAL issues fixed
- [ ] All HIGH issues fixed (or explicitly deferred with approval)
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
- CI passes on final commit

```bash
# Check PR status
gh pr checks [PR-NUMBER]
gh pr status
```

**Approval comment template:**

```markdown
## Approved

- [x] Code quality verified
- [x] Security considerations reviewed
- [x] Test coverage adequate
- [x] Documentation accurate
- [x] Ready for production

LGTM - Ship it!
```

---

## Phase 5: Merge & Release

### Step 5.1: Merge PR

```bash
# Squash merge (recommended for clean history)
gh pr merge [PR-NUMBER] --squash --delete-branch

# Or merge commit if preserving history matters
gh pr merge [PR-NUMBER] --merge --delete-branch
```

### Step 5.2: Release

Run `/pb-release`:

```bash
# Verify main is updated
git checkout main && git pull

# Tag the release
git tag -a vX.Y.Z -m "vX.Y.Z - Brief description"
git push origin vX.Y.Z

# Create GitHub release
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

# Phase 2: Pick ONE relevant review
# /pb-review-cleanup (if code touched)
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

**Use full workflow by default. This escape hatch is for exceptions, not convenience.**

Examples of trivial changes:
- Fixing a typo in documentation
- Updating a comment
- Bumping a version number
- Adding a missing log message

Examples that are NOT trivial (use full workflow):
- Any logic change
- Any new functionality
- Any test changes
- Any configuration changes
- Anything touching security, auth, or data

---

## Parallel Reviews (Advanced)

For faster shipping, some reviews can run in parallel:

```
Sequential (dependencies):
  pb-review-cleanup → pb-review-hygiene

Parallel (independent):
  ├─ pb-review-tests
  ├─ pb-security
  └─ pb-logging

Sequential (needs stable code):
  pb-review-docs → pb-review-prerelease
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

---

## Integration with Playbook

**Part of development workflow:**
```
/pb-start → /pb-cycle (iterate) → /pb-pause/resume → /pb-ship
                                                        │
                                    ┌───────────────────┘
                                    ↓
                              Foundation
                                    ↓
                           Specialized Reviews
                                    ↓
                              Final Gate
                                    ↓
                            PR & Peer Review
                                    ↓
                            Merge & Release
                                    ↓
                                Verify
```

**Related commands:**
- `/pb-cycle` — Self-review before shipping
- `/pb-pause` — If shipping spans multiple sessions
- `/pb-release` — Detailed release process
- `/pb-incident` — If release causes issues

---

## Checklist Summary

```
PHASE 1: FOUNDATION
[ ] Quality gates pass (lint, typecheck, test)
[ ] Basic self-review complete (/pb-cycle)

PHASE 2: SPECIALIZED REVIEWS
[ ] /pb-review-cleanup — code quality
[ ] /pb-review-hygiene — project health
[ ] /pb-review-tests — test coverage
[ ] /pb-security — vulnerabilities
[ ] /pb-logging — logging standards (optional)
[ ] /pb-review-docs — documentation

PHASE 3: FINAL GATE
[ ] /pb-review-prerelease — senior engineer gate
[ ] Ship decision: GO

PHASE 4: PR & PEER REVIEW
[ ] PR created (/pb-pr)
[ ] Peer review complete
[ ] Feedback addressed
[ ] Approved sign-off received

PHASE 5: MERGE & RELEASE
[ ] PR merged
[ ] Release tagged and deployed (/pb-release)
[ ] Verification passed
[ ] Summary documented
```

---

*Ship with confidence. Every review is a gift.*
