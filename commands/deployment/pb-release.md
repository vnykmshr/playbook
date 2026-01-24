# Release to Production

Orchestrate a production release: readiness gate, version management, deployment trigger, and verification. This is the central command for shipping releases.

**Mindset:** This command embodies `/pb-preamble` thinking (challenge readiness assumptions, surface risks directly) and `/pb-design-rules` thinking (verify Robustness, verify Clarity, ensure systems fail loudly not silently).

Don't hide issues to seem "ready." Surface risks directly. A delayed release beats a broken release.

---

## When to Use This Command

- Shipping a versioned release (vX.Y.Z)
- After `/pb-ship` completes review phases
- Production deployment with full ceremony
- Hotfix releases (streamlined path available)

---

## Release Flow Overview

```
Phase 1: READINESS GATE          Phase 2: VERSION & TAG         Phase 3: DEPLOY & VERIFY
│                                │                              │
├─ Code quality verified         ├─ Version bumped              ├─ /pb-deployment
│  (via /pb-review-hygiene)      │                              │  (execute deployment)
│                                ├─ CHANGELOG updated           │
├─ CI passing                    │                              ├─ Health check
│                                ├─ Git tag created             │
├─ Security reviewed             │                              ├─ Smoke tests
│  (via /pb-security)            ├─ GitHub release created      │
│                                │                              ├─ Monitor metrics
├─ Tests adequate                │                              │
│  (via /pb-review-tests)        │                              └─ Release summary
│                                │
├─ Docs accurate                 │
│  (via /pb-review-docs)         │
│                                │
└─ Senior sign-off               │
   (final gate)                  │
```

---

## Phase 1: Readiness Gate

Verify the codebase is release-ready. This absorbs what was previously `/pb-review-prerelease`.

### Step 1.1: Quality Gates

```bash
# Run all quality checks
make lint        # Linting passes
make typecheck   # Type checking passes
make test        # All tests pass
```

**All gates must pass. No exceptions.**

### Step 1.2: CI Verification

```bash
# Check CI status on main/release branch
gh run list --limit 3
gh run view [RUN_ID]

# All checks must be green
gh pr checks [PR_NUMBER]  # If PR-based release
```

**Checklist:**
- [ ] CI pipeline passing
- [ ] All required checks green
- [ ] No flaky test failures (investigate if any)

### Step 1.3: Release Readiness Checklist

Review with senior engineer perspective:

**Code Quality:**
- [ ] No debug code (console.log, print statements)
- [ ] No commented-out code
- [ ] No hardcoded secrets or credentials
- [ ] No TODO/FIXME for critical items
- [ ] Code patterns consistent
- [ ] No unnecessary complexity

**Security:**
- [ ] No secrets in code (environment variables used)
- [ ] Input validation at system boundaries
- [ ] SQL queries parameterized
- [ ] Dependencies scanned for vulnerabilities
- [ ] Auth/authz properly implemented

**Testing:**
- [ ] Critical paths have test coverage
- [ ] Edge cases tested
- [ ] No flaky tests
- [ ] Integration tests for key flows

**Documentation:**
- [ ] README accurate (installation, usage)
- [ ] API docs updated (if applicable)
- [ ] Migration guide updated (if breaking changes)

**Infrastructure:**
- [ ] Docker images use specific versions (not `latest`)
- [ ] Health checks configured
- [ ] Rollback plan documented and tested

### Step 1.4: Final Sign-off

```markdown
## Release Readiness Sign-off

**Version:** vX.Y.Z
**Date:** YYYY-MM-DD
**Engineer:** [name]

### Verification
- [ ] Quality gates pass
- [ ] CI green
- [ ] Code quality reviewed
- [ ] Security reviewed
- [ ] Tests adequate
- [ ] Docs accurate
- [ ] Rollback plan ready

### Known Issues (if any)
- [Issue description] — [Severity] — [Mitigation]

### Decision: GO / NO-GO

Signed: _______________
```

**If NO-GO:** Document blockers, return to development, re-run `/pb-cycle`.

---

## Phase 2: Version & Tag

### Step 2.1: Verify CHANGELOG

```bash
# Check CHANGELOG has entry for this version
grep -E "## \[v?X\.Y\.Z\]" CHANGELOG.md

# Verify entry has required sections
# - Added, Changed, Fixed, Removed (as applicable)
# - Date
# - Version links at bottom
```

**CHANGELOG checklist:**
- [ ] Version entry exists with date
- [ ] All changes documented
- [ ] Version links added at bottom
- [ ] Format follows Keep a Changelog

### Step 2.2: Bump Version (If Not Already)

```bash
# Update version in package files
# Node.js
npm version X.Y.Z --no-git-tag-version

# Python (pyproject.toml)
# Edit version = "X.Y.Z"

# Go (typically no version file)
# Update in relevant constants if needed
```

### Step 2.3: Create Git Tag

```bash
# Ensure on main branch with latest
git checkout main
git pull origin main

# Verify clean state
git status  # Should be clean

# Create annotated tag
git tag -a vX.Y.Z -m "vX.Y.Z - Brief description"

# Push tag
git push origin vX.Y.Z
```

### Step 2.4: Create GitHub Release

```bash
# Create release with notes from CHANGELOG
gh release create vX.Y.Z \
  --title "vX.Y.Z - Release Title" \
  --notes "$(cat <<'EOF'
## What's New

[Copy from CHANGELOG or write summary]

## Highlights
- [Key feature/fix 1]
- [Key feature/fix 2]

## Full Changelog
See [CHANGELOG.md](./CHANGELOG.md) for complete details.
EOF
)"
```

---

## Phase 3: Deploy & Verify

### Step 3.1: Execute Deployment

Run `/pb-deployment` for the full deployment workflow:

```bash
# Or if using make target
make deploy ENV=production

# Or trigger CI/CD deployment
# (push tag may auto-trigger in some setups)
```

**Follow `/pb-deployment` phases:**
1. Discovery (identify deployment method)
2. Pre-flight (verify readiness)
3. Execute (run deployment)
4. Verify (health checks, smoke tests)
5. Finalize or rollback

### Step 3.2: Post-Deployment Verification

```bash
# Health check
curl -s [PROD_URL]/health | jq

# Smoke test critical flows
# [Project-specific verification]

# Check error metrics
# [Monitoring dashboard]

# Review logs
# [Log aggregator]
```

**Verification checklist:**
- [ ] Health endpoint returns OK
- [ ] Critical user flows work
- [ ] No new errors in logs
- [ ] Metrics look normal
- [ ] Alerts are quiet

### Step 3.3: Monitor Period

**Stay alert for 30-60 minutes post-deploy:**
- Watch error rates
- Monitor latency
- Check resource usage
- Be ready to rollback

### Step 3.4: Release Summary

```markdown
## Release Summary

**Version:** vX.Y.Z
**Released:** YYYY-MM-DD HH:MM
**Tag:** [link to tag]
**Release:** [link to GitHub release]

### What Shipped
- [Feature/fix 1]
- [Feature/fix 2]

### Verification
- Health check: PASS
- Smoke tests: PASS
- Monitoring: NOMINAL

### Post-Release
- [ ] Monitor for 24h
- [ ] Close related issues
- [ ] Update project board
- [ ] Announce (if applicable)
```

---

## Hotfix Release (Streamlined)

For urgent fixes that don't warrant full ceremony:

```bash
# 1. Quick quality check
make lint && make test

# 2. Verify CI passes
gh run list --limit 1

# 3. Fast version bump
git tag -a vX.Y.Z -m "Hotfix: [description]"
git push origin vX.Y.Z

# 4. Deploy immediately
make deploy ENV=production

# 5. Verify
curl -s [PROD_URL]/health | jq

# 6. Document
echo "[$(date)] HOTFIX vX.Y.Z - [description]" >> CHANGELOG.md
```

**Hotfix rules:**
- Still requires passing tests
- Still requires CI green
- Streamlined review (skip full /pb-review-* suite)
- Must document in CHANGELOG after the fact
- Schedule full review for next regular release

---

## Rollback

If release verification fails:

```bash
# Immediate rollback via /pb-deployment
kubectl rollout undo deployment/[app-name]
# or
make rollback

# Verify rollback
curl -s [PROD_URL]/health | jq

# Notify team
echo "⚠️ Release vX.Y.Z rolled back - investigating"

# Document
# Add to incident log or CHANGELOG
```

**After rollback:**
1. Run `/pb-incident` if user impact
2. Investigate root cause
3. Fix issue
4. Re-run release process

---

## Release Checklist Summary

```
PHASE 1: READINESS GATE
[ ] Quality gates pass (lint, typecheck, test)
[ ] CI green
[ ] Code quality verified
[ ] Security reviewed
[ ] Tests adequate
[ ] Docs accurate
[ ] Senior sign-off: GO

PHASE 2: VERSION & TAG
[ ] CHANGELOG updated with version entry
[ ] Version bumped in package files
[ ] Git tag created (vX.Y.Z)
[ ] GitHub release created

PHASE 3: DEPLOY & VERIFY
[ ] Deployment executed (/pb-deployment)
[ ] Health check passing
[ ] Smoke tests passing
[ ] Metrics normal
[ ] Monitor period complete
[ ] Release summary documented
```

---

## Integration with Playbook

**Part of shipping workflow:**
```
/pb-start → /pb-cycle → /pb-ship → /pb-release → /pb-deployment
                                        │              │
                                   (orchestrator)  (executor)
```

**This command orchestrates:**
- Readiness verification (absorbs former pb-review-prerelease)
- Version management
- `/pb-deployment` trigger

## Related Commands

- `/pb-deployment` — Execute deployment to target environments
- `/pb-ship` — Full review workflow before release
- `/pb-pr` — Create pull requests for release branches
- `/pb-review-hygiene` — Comprehensive project health review

---

*Release with confidence. Verify thoroughly. Rollback without hesitation.*
