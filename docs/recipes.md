# Workflow Recipes

Pre-built command sequences for common development scenarios. Each recipe links commands into a coherent workflow, showing exactly when to use which command.

**Philosophy:** Commands are precision tools. Recipes show how to combine them effectively. Think of recipes as "playbooks within the playbook."

---

## Quick Reference

| Recipe | Scenario | Tier | Time |
|--------|----------|------|------|
| [recipe-bug-fix](#recipe-bug-fix) | Fixing bugs (simple to complex) | S/M | 1-4 hours |
| [recipe-feature](#recipe-feature) | Building new features | M/L | Days-weeks |
| [recipe-frontend](#recipe-frontend) | Frontend/UI development | M/L | Days-weeks |
| [recipe-api](#recipe-api) | API development | M | Days |
| [recipe-incident](#recipe-incident) | Production emergencies | Emergency | Hours |
| [recipe-context-switch](#recipe-context-switch) | Pausing and resuming work | N/A | 5-15 min |
| [recipe-onboarding](#recipe-onboarding) | New team member integration | N/A | Weeks |
| [recipe-release](#recipe-release) | Pre-release preparation | L | Hours-days |

**Discovery tip:** All recipes use the `recipe-` prefix for easy search and tab completion.

---

## recipe-bug-fix

**Scenario:** Fixing bugs, from simple typos to complex investigations
**Tier:** S (simple) or M (complex)

### Workflow

```
1. /pb-start
   └─ Create fix/issue-123 branch

2. /pb-debug (if cause unclear)
   └─ Reproduce → Isolate → Hypothesize → Test

3. /pb-cycle
   └─ Fix → Self-review → Test
   └─ Repeat until fix is solid

4. /pb-commit
   └─ fix(scope): description
   └─ Fixes #123

5. /pb-pr
   └─ Summary: What was broken, how it's fixed
   └─ Test plan: How to verify

→ Merge after approval
```

### Checklist

- [ ] Bug reproduced before fixing
- [ ] Root cause addressed (not just symptom)
- [ ] Regression test added
- [ ] No unrelated changes included

---

## recipe-feature

**Scenario:** Building new features end-to-end
**Tier:** M or L

### Workflow

```
1. /pb-plan
   └─ Discovery: What problem? What boundaries?
   └─ Scope lock: In/out of scope, success criteria

2. /pb-adr (if architectural decisions needed)
   └─ Document alternatives, trade-offs, decision

3. /pb-start
   └─ Create feature/feature-name branch

4. /pb-cycle (repeat)
   └─ Implement → Self-review → Test
   └─ /pb-commit for each logical chunk

5. /pb-ship
   └─ Phase 1: Quality gates
   └─ Phase 2: Specialized reviews
   └─ Phase 3: Final gate
   └─ Phase 4: PR & peer review
   └─ Phase 5: Merge & release

6. /pb-release (if production deployment)
   └─ Deploy → Verify → Monitor
```

### Checklist

- [ ] Scope locked before implementation
- [ ] Changes are atomic (one concern per commit)
- [ ] Tests cover happy path and key edge cases
- [ ] Documentation updated
- [ ] No scope creep

---

## recipe-frontend

**Scenario:** Frontend/UI feature development with design language and accessibility
**Tier:** M or L

### Workflow

```
1. /pb-plan
   └─ What problem? Who benefits?
   └─ Scope lock

2. /pb-design-language (if new project or new patterns)
   └─ Define tokens, vocabulary, constraints
   └─ Request/create required assets

3. /pb-patterns-frontend
   └─ Choose component patterns
   └─ Plan state management approach
   └─ Consider performance implications

4. /pb-start
   └─ Create feature/feature-name branch

5. /pb-cycle (repeat)
   └─ Build components (mobile-first)
   └─ /pb-a11y checks during development
   └─ Self-review → Test → Commit

6. /pb-ship
   └─ Include /pb-a11y checklist in reviews
   └─ Performance audit (bundle size, load time)

7. /pb-release
   └─ Deploy → Cross-browser testing → Monitor
```

### Frontend-Specific Checklist

- [ ] Mobile-first implemented (styles build up, not down)
- [ ] Theme-aware (uses design tokens, supports dark mode)
- [ ] Semantic HTML used (not div soup)
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Screen reader tested
- [ ] Assets optimized (images, fonts)
- [ ] Bundle size acceptable

---

## recipe-api

**Scenario:** API design and implementation
**Tier:** M

### Workflow

```
1. /pb-plan
   └─ Who consumes this API?
   └─ What operations needed?

2. /pb-patterns-api
   └─ Choose style (REST, GraphQL, gRPC)
   └─ Design resources/schema
   └─ Define error handling

3. /pb-adr (if significant decisions)
   └─ Document API style choice, versioning strategy

4. /pb-start
   └─ Create feature/api-name branch

5. /pb-cycle (repeat)
   └─ Implement endpoint
   └─ Write API tests
   └─ Update documentation (OpenAPI)
   └─ Commit

6. /pb-security
   └─ Authentication/authorization review
   └─ Input validation
   └─ Rate limiting

7. /pb-ship → /pb-release
```

### API-Specific Checklist

- [ ] OpenAPI/GraphQL schema documented
- [ ] Error responses consistent
- [ ] Authentication implemented
- [ ] Rate limiting configured
- [ ] Backward compatible (or version bumped)

---

## recipe-incident

**Scenario:** Production incident response and recovery
**Tier:** Emergency

### Workflow

```
1. /pb-incident
   └─ ASSESS: What's broken? Who's affected?
   └─ MITIGATE: Rollback, disable, scale (stop bleeding)
   └─ COMMUNICATE: Status to stakeholders

2. /pb-debug (after bleeding stopped)
   └─ Reproduce → Isolate → Hypothesize
   └─ Find root cause

3. /pb-start (expedited)
   └─ Create hotfix/incident-123 branch

4. /pb-cycle (minimal)
   └─ Fix → Quick self-review → Test critical path

5. /pb-commit
   └─ fix(scope): hotfix for incident-123

6. /pb-pr (expedited review)
   └─ Sync review, not async

7. Deploy immediately
   └─ Verify fix in production
   └─ Monitor closely

8. Post-incident (within 24-48 hours)
   └─ Document timeline
   └─ Root cause analysis
   └─ Action items to prevent recurrence
```

### Incident Checklist

- [ ] Mitigation applied (bleeding stopped)
- [ ] Stakeholders notified
- [ ] Fix verified in production
- [ ] Post-incident review scheduled

---

## recipe-context-switch

**Scenario:** Pausing and resuming work across sessions
**Tier:** N/A (operational)

### Pausing Work

```
1. /pb-pause
   └─ Commit or stash current work
   └─ Push to remote
   └─ Update tracker (if applicable)
   └─ Write pause notes (todos/pause-notes.md)
```

### Resuming Work

```
1. /pb-resume
   └─ git status, git log (current state)
   └─ Read pause notes
   └─ Sync with main (git fetch, rebase)
   └─ Verify environment (make dev, make test)

2. /pb-what-next (if unsure)
   └─ Context-aware recommendations
```

### Context Switch Checklist

**Before switching:**
- [ ] Work committed or stashed
- [ ] Pushed to remote
- [ ] Pause notes written

**When returning:**
- [ ] Pause notes read
- [ ] Branch up to date
- [ ] Tests passing

---

## recipe-onboarding

**Scenario:** New team member integration
**Tier:** N/A (operational)

### New Team Member Workflow

```
Week 1:
1. /pb-preamble
   └─ Understand collaboration philosophy
   └─ Challenge assumptions, peer thinking

2. /pb-design-rules
   └─ Understand technical principles
   └─ Clarity, Simplicity, Resilience, Extensibility

3. /pb-guide
   └─ Understand SDLC framework
   └─ Change tiers, checkpoints

4. /pb-standards
   └─ Code quality expectations
   └─ Commit and PR standards

Week 2:
5. /pb-onboarding (formal)
   └─ Codebase walkthrough
   └─ Architecture overview
   └─ Key contacts

6. First task (XS or S tier)
   └─ /pb-start → /pb-cycle → /pb-commit → /pb-pr
   └─ Experience the workflow

Week 3+:
7. /pb-knowledge-transfer
   └─ Deep dive into specific areas
   └─ Pair with senior engineer
```

### Onboarding Checklist

- [ ] Preamble philosophy understood
- [ ] Development environment working
- [ ] Access to all required systems
- [ ] First PR merged
- [ ] Key architecture understood

---

## recipe-release

**Scenario:** Pre-release preparation and deployment
**Tier:** L

### Pre-Release Workflow

```
1. /pb-review (comprehensive)
   └─ Security audit
   └─ Performance review
   └─ Test coverage analysis
   └─ Code quality review

2. /pb-release (final gate)
   └─ Senior engineer sign-off
   └─ Go/no-go decision

3. /pb-release
   └─ Version bump
   └─ Changelog update
   └─ Tag release
   └─ Deploy to production
   └─ Smoke test
   └─ Monitor for 1-24 hours

4. Post-release
   └─ Announce release
   └─ Monitor metrics
   └─ Be ready for hotfix if needed
```

### Release Checklist

- [ ] All planned features complete
- [ ] All tests passing
- [ ] Security review complete
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Rollback plan ready
- [ ] Team available for monitoring

---

## Recipe Selection Guide

```
What are you doing?

├─ Fixing a bug
│   └─ Simple bug? → Bug Fix recipe
│   └─ Complex investigation? → Add /pb-debug first
│
├─ Building something new
│   └─ Backend/API? → API Development recipe
│   └─ Frontend/UI? → Frontend Feature recipe
│   └─ Full stack? → Feature Development recipe
│
├─ Handling emergency
│   └─ Production down? → Incident Response recipe
│
├─ Switching context
│   └─ Leaving? → /pb-pause
│   └─ Returning? → /pb-resume
│
├─ Preparing release
│   └─ Release Preparation recipe
│
└─ Joining team
    └─ Onboarding recipe
```

---

## Creating Custom Recipes

For project-specific workflows, create recipes in `todos/recipes/` or `docs/team-recipes.md`:

```markdown
## Recipe: [Name]

**When to use:** [Scenario]
**Tier:** [XS/S/M/L]

### Workflow

1. Command 1
   └─ What to do

2. Command 2
   └─ What to do

### Checklist

- [ ] Item 1
- [ ] Item 2
```

---

## Related Commands

- `/pb-what-next` — Intelligent command recommendations
- `/pb-guide` — Full SDLC framework
- `/pb-ship` — Complete shipping workflow

---

**Last Updated:** 2026-01-19
**Version:** 1.0
