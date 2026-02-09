# Evolution System Operational Guide

**For:** Playbook maintainers running quarterly (or on-demand) evolution cycles
**Date:** 2026-02-09
**Version:** 1.0

This guide walks through the complete evolution process with all safety mechanisms in place.

---

## Overview: The Evolution Workflow

```
┌─────────────────────────────────────────────────────────┐
│ PREPARE                                                 │
│ ├─ Ensure clean git state                              │
│ ├─ Create snapshot (enable rollback)                   │
│ └─ Record evolution cycle (structured log)             │
├─────────────────────────────────────────────────────────┤
│ ANALYZE                                                 │
│ ├─ Review capability changes since last cycle          │
│ ├─ Audit playbooks against new capabilities            │
│ └─ Propose changes with rationale                      │
├─────────────────────────────────────────────────────────┤
│ VALIDATE & TEST                                         │
│ ├─ Generate diff (what will change?)                   │
│ ├─ Run execution tests (do evolved playbooks work?)    │
│ └─ Verify metadata consistency                         │
├─────────────────────────────────────────────────────────┤
│ APPROVE                                                 │
│ ├─ Create PR with proposed changes                     │
│ ├─ Request peer review                                 │
│ └─ Merge only after approval                           │
├─────────────────────────────────────────────────────────┤
│ APPLY                                                   │
│ ├─ Update playbooks with approved changes              │
│ ├─ Regenerate indices and documentation                │
│ └─ Final validation                                    │
├─────────────────────────────────────────────────────────┤
│ COMPLETE                                                │
│ ├─ Tag release                                         │
│ ├─ Record cycle completion                             │
│ └─ Document outcomes and metrics                       │
└─────────────────────────────────────────────────────────┘
```

---

## Part 1: PREPARE Phase

### 1.1: Ensure Clean Git State

Before starting, verify your working tree is clean:

```bash
# Check git status
git status

# Must show:
# On branch main
# nothing to commit, working tree clean

# If dirty, commit or stash changes
git add .
git commit -m "checkpoint: save work before evolution"
```

### 1.2: Create Evolution Snapshot

**This is critical.** A snapshot is your insurance policy.

```bash
# Create snapshot with descriptive message
python3 scripts/evolution-snapshot.py \
  --create "Before Q1 2026 evolution: Sonnet 4.6 analysis"

# Output will look like:
# 📸 Creating snapshot: evolution-20260209-143022
#   ✅ Git tag created: evolution-20260209-143022
#   ✅ Metadata saved
# ✅ Snapshot created: evolution-20260209-143022
```

The snapshot:
- Creates a git tag (cloud backup)
- Records metadata (creation time, message)
- Enables rollback if needed

### 1.3: Record Evolution Cycle

Log the cycle in the structured audit log:

```bash
# Record the cycle
python3 scripts/evolution-log.py \
  --record-cycle "2026-Q1" \
  --trigger quarterly \
  --capability-changes "Sonnet 4.6: +30% speed, same cost. Parallelization now viable."

# Output:
# ✅ Evolution cycle recorded: 2026-Q1
```

**Trigger types:**
- `quarterly` — Scheduled quarterly evolution (Feb/May/Aug/Nov)
- `version_upgrade` — New Claude model release
- `user_feedback` — User-reported issue or pattern
- `manual` — Ad-hoc evolution (e.g., testing)

---

## Part 2: ANALYZE Phase

### 2.1: Document Capability Changes

Understand what's changed since last evolution:

```bash
# Check Claude version
# Use: announcements, release notes, or testing directly

# Document findings
cat > /tmp/capability-changes.md << 'EOF'
# Claude Capability Changes (Since 2025-11-01)

## Model Versions
- Sonnet 4.5 → 4.6: 30% faster at same cost
- Opus 4.5 → 4.6: 15% faster, slightly better reasoning
- Haiku unchanged

## Speed Implications
- Sonnet now competitive with Opus on some reasoning tasks
- Parallelization more efficient (faster total time)
- Model routing can be more aggressive

## Limitations Unchanged
- Context window still 200K (Sonnet, Opus)
- Haiku still 100K
- Cost per token unchanged

## What To Test
1. Can Sonnet handle what Opus used to do?
2. Is parallelization worth the token cost?
3. Do old playbooks need simplification?
EOF

# Review your findings
cat /tmp/capability-changes.md
```

### 2.2: Audit Playbooks by Category

Systematically review each playbook category:

**DEVELOPMENT playbooks** (pb-start, pb-cycle, pb-commit, pb-pr, pb-debug)
- Question: Can Sonnet 4.6 handle all development tasks?
- Action: Test complex refactoring with Sonnet
- Possible change: Move some from Opus → Sonnet

**PLANNING playbooks** (pb-plan, pb-adr, pb-think, pb-patterns-*)
- Question: Do planning decisions still need Opus reasoning?
- Action: Test strategy proposals with Sonnet
- Possible change: Parallel ideation (fan-out) now viable

**REVIEW playbooks** (pb-review-code, pb-security, pb-voice)
- Question: Can parallel reviews work with faster Sonnet?
- Action: Test 3-way review (multiple agents) on same code
- Possible change: Parallel review pattern

**UTILITIES** (pb-doctor, pb-git-hygiene, pb-ports, etc.)
- Question: Can more tasks use Haiku instead of Sonnet?
- Action: Test each utility with Haiku
- Possible change: Expand Haiku-suitable tasks

### 2.3: Propose Changes

For each opportunity, document:

```markdown
### Opportunity: Parallel Code Review

**Status quo:**
- Code review runs sequentially: one agent reviews, time=T

**Capability change:**
- Sonnet 4.6 is 30% faster
- Context windows still 200K (sufficient for reviews)

**Proposal:**
- Run 3-way parallel review (code style, logic, security)
- Each agent gets same code + different focus
- Merge results

**Why now:**
- Sonnet fast enough that parallel doesn't double cost
- Users want faster reviews

**Risk:**
- Three agents might have redundant observations
- Could result in longer report

**Test plan:**
- Run parallel review on 3 open PRs
- Compare: time saved vs report size
- If time saves > 30% and quality maintained, implement

**Expected impact:**
- Code review time: 25 min → 15 min (-40%)
- Cost per review: same (3 agents × faster speed ≈ sequential)
```

Record proposed changes:

```bash
# For each significant change, record it
python3 scripts/evolution-log.py \
  --record-change pb-review-code \
  --field execution_pattern \
  --before sequential \
  --after parallel \
  --rationale "Sonnet 4.6 fast enough for concurrent review agents" \
  --cycle "2026-Q1"
```

---

## Part 3: VALIDATE & TEST Phase

### 3.1: Generate Diff Preview

See exactly what will change:

```bash
# Generate diff report (compares current vs proposed)
python3 scripts/evolution-diff.py \
  --detailed main HEAD

# This shows:
# - Which commands change
# - What fields change
# - Old → new values
```

**Example output:**
```
### pb-review-code

**execution_pattern:**
- Before: `sequential`
- After: `parallel`

**related_commands:**
- Before: `['pb-review-docs', 'pb-security', 'pb-cycle']`
- After: `['pb-review-docs', 'pb-security', 'pb-cycle', 'pb-voice']`
```

### 3.2: Run Execution Tests

Validate that evolved playbooks still work:

```bash
# Run all evolution tests
pytest tests/test_evolution_execution.py -v

# Key tests:
# ✓ Metadata is consistent (Resource Hint ↔ model_hint)
# ✓ Related commands still exist
# ✓ Model hints make sense
# ✓ No orphaned metadata fields
# ✓ Categories are valid
# ✓ Execution patterns are valid

# If any test fails, fix before proceeding!
```

### 3.3: Verify Metadata Consistency

```bash
# Check that all metadata is still valid
python3 scripts/evolve.py --validate

# Should output:
# All metadata valid
# 86 commands parsed successfully
```

### 3.4: Run Convention Checks

```bash
# Ensure playbooks still follow conventions
python3 scripts/validate-conventions.py

# Should output:
# Passed: 253
# Warnings: 0-10 (pre-existing are OK)
# Errors: 0
```

---

## Part 4: APPROVE Phase

### 4.1: Create PR for Review

**Don't apply changes directly.** Create a PR and get peer review.

```bash
# Create feature branch (don't commit to main yet)
git checkout -b evolution/2026-q1
git add commands/
git commit -m "evolution: propose Q1 2026 changes"

# Generate markdown diff report for reviewers
python3 scripts/evolution-diff.py \
  --report main HEAD

# Create PR
gh pr create \
  --title "evolution(quarterly): Q1 2026 — Sonnet 4.6 analysis" \
  --body "$(cat <<'EOF'
## Summary

Quarterly evolution for Claude Sonnet 4.6 improvements.

## Changes
- Parallel review patterns now viable
- Model routing optimized (Sonnet handles more)
- No breaking changes

See `todos/evolution-diff-report.md` for detailed diff.

## Testing
- ✅ Execution tests: PASS
- ✅ Metadata consistency: PASS
- ✅ Convention validation: PASS
- ✅ All tests: PASS

## Review Checklist
- [ ] Capability changes make sense
- [ ] Proposed changes align with capabilities
- [ ] No unintended side effects
- [ ] Metadata is consistent
- [ ] Tests pass
EOF
)"

# Example output:
# ✓ https://github.com/vnykmshr/playbook/pull/10
```

### 4.2: Peer Review Checklist

**Reviewer, use this checklist:**

- [ ] **Capability alignment** — Do proposed changes match new Claude capabilities?
- [ ] **No regressions** — Will evolved playbooks still work as intended?
- [ ] **Metadata consistency** — Do all field changes make sense together?
- [ ] **Impact scope** — Are side effects acceptable?
- [ ] **Test coverage** — Do execution tests pass?
- [ ] **Documentation** — Is rationale clear?
- [ ] **Risk assessment** — Are there gotchas?

**If review finds issues:**
- Return PR for fixes
- Don't approve until all concerns resolved

### 4.3: Merge After Approval

```bash
# Only after approval:
git push origin evolution/2026-q1

# Merge via GitHub or CLI
gh pr merge 10 --squash

# Pull latest main
git checkout main
git pull origin main
```

---

## Part 5: APPLY Phase

### 5.1: Apply Approved Changes

Now that changes are approved and merged, make them active:

```bash
# Update playbook content
# Example: if you proposed parallel reviews, implement it in pb-review-code

# 1. Edit commands/reviews/pb-review-code.md
#    - Add "Parallel Review Pattern" section
#    - Update execution_pattern in metadata: sequential → parallel
#    - Update examples to show parallel execution

# 2. Regenerate auto-generated files
python3 scripts/evolve.py --generate

# 3. Regenerate CLAUDE.md
/pb-claude-project

# 4. Validate everything still works
python3 scripts/evolve.py --validate
pytest tests/test_evolution_execution.py -v
```

### 5.2: Final Validation

```bash
# Ensure nothing broke
python3 scripts/validate-conventions.py
mkdocs build --strict
npx markdownlint-cli --config .markdownlint.json 'commands/**/*.md'

# All must pass!
```

---

## Part 6: COMPLETE Phase

### 6.1: Commit Changes

```bash
# Stage all changes
git add commands/ docs/ scripts/ .claude/ CHANGELOG.md

# Commit with clear message
git commit -m "$(cat <<'EOF'
evolution(q1-2026): apply Sonnet 4.6 optimizations

Implemented parallel review patterns and model routing optimizations
based on Sonnet 4.6 capability improvements.

Changes:
- Parallel code review now standard (execution_pattern: parallel)
- Model routing: Sonnet handles 5 additional task types
- Updated context efficiency in pb-claude-orchestration

Metrics:
- Expected time savings: 15% per review cycle
- Expected cost savings: minimal (parallel increases token use slightly)
- Risk: low (tested on live PRs)

Cycle snapshot: evolution-20260209-143022
EOF
)"
```

### 6.2: Tag Release

```bash
# Create version tag
git tag -a v2.11.0 -m "v2.11.0: Q1 2026 Evolution (Sonnet 4.6 Optimizations)"

# Push tag
git push origin v2.11.0
```

### 6.3: Record Cycle Completion

```bash
# Record that cycle is complete
python3 scripts/evolution-log.py \
  --complete "2026-Q1" \
  --pr 10

# Export timeline for metrics
python3 scripts/evolution-log.py --analyze
```

### 6.4: Update CHANGELOG

```markdown
# CHANGELOG.md

## v2.11.0 (2026-05-15) — Q1 2026 Evolution

### Improvements
- **Parallel Review Patterns** — Code reviews now run 3-way parallel (style, logic, security)
- **Model Routing Optimization** — Sonnet 4.6 now handles architecture decisions previously requiring Opus
- **Context Efficiency** — Improved compression techniques; context use -8%

### Metrics
- Review time: -40% (25 min → 15 min)
- Session cost: same (parallelization offsets speed gains)
- User satisfaction: +12% (faster turnaround)

### Testing
- Parallel review patterns tested on 50+ real PRs
- Model routing changes validated on 100+ sessions
- Backward compatible: old playbooks still work

### Upgrade Path
- No breaking changes
- Automatic via system update
- Recommended for all users
```

---

## Handling Problems: Rollback

### If Something Breaks After Release

**Scenario:** You released evolution changes, but they cause issues in production.

**Response:**

```bash
# 1. List available snapshots
python3 scripts/evolution-snapshot.py --list

# 2. Choose the one from before evolution
#    Example: evolution-20260209-143022

# 3. Rollback (interactive confirmation)
python3 scripts/evolution-snapshot.py --rollback evolution-20260209-143022

# 4. Record the revert
python3 scripts/evolution-log.py \
  --revert "2026-Q1" \
  --reason "Parallel reviews increased false positives; needs refinement"

# 5. Push rollback commit
git push origin main

# 6. Post-mortem: What went wrong?
# - Was the assumption wrong? (Sonnet not ready for this?)
# - Was the implementation wrong? (Bad parallelization strategy?)
# - What would you do differently next time?
```

---

## Tools Reference

### Snapshot Management

```bash
# Create snapshot
python3 scripts/evolution-snapshot.py --create "Message"

# List snapshots
python3 scripts/evolution-snapshot.py --list

# Show snapshot details
python3 scripts/evolution-snapshot.py --show evolution-20260209-143022

# Rollback to snapshot
python3 scripts/evolution-snapshot.py --rollback evolution-20260209-143022

# Cleanup old snapshots (keep 5 most recent)
python3 scripts/evolution-snapshot.py --cleanup 5
```

### Evolution Log

```bash
# Record new cycle
python3 scripts/evolution-log.py \
  --record-cycle "2026-Q1" \
  --trigger quarterly \
  --capability-changes "Sonnet 4.6: +30% speed"

# Record change within cycle
python3 scripts/evolution-log.py \
  --record-change pb-review-code \
  --field execution_pattern \
  --before sequential \
  --after parallel \
  --rationale "Sonnet 4.6 enables parallelization" \
  --cycle "2026-Q1"

# View history
python3 scripts/evolution-log.py --show

# Analyze patterns
python3 scripts/evolution-log.py --analyze

# Complete cycle
python3 scripts/evolution-log.py --complete "2026-Q1" --pr 10

# Revert cycle
python3 scripts/evolution-log.py --revert "2026-Q1" --reason "Issues found"
```

### Diff and Testing

```bash
# Generate diff
python3 scripts/evolution-diff.py --detailed main HEAD

# Generate report
python3 scripts/evolution-diff.py --report main HEAD

# Run execution tests
pytest tests/test_evolution_execution.py -v

# Validate metadata
python3 scripts/evolve.py --validate

# Check conventions
python3 scripts/validate-conventions.py
```

---

## Troubleshooting

### "Working tree is dirty" error

```bash
# Stage and commit changes
git add .
git commit -m "checkpoint: save progress"

# Then retry evolution commands
```

### Snapshot creation fails

```bash
# Ensure git is configured
git config user.name "Your Name"
git config user.email "your@email.com"

# Retry snapshot
python3 scripts/evolution-snapshot.py --create "Message"
```

### Diff tool shows huge changes

```bash
# Normal if metadata changed significantly
# Review carefully in PR

# If concerned, start with smaller change
# Revert proposed changes and try again
```

### Tests fail after evolution

```bash
# Run tests locally first
pytest tests/test_evolution_execution.py -v

# Fix issues before creating PR
# Examples:
# - Update Resource Hints if model hints changed
# - Add new related commands if topology changed
# - Verify metadata consistency

# Re-run tests
pytest tests/test_evolution_execution.py -v

# Only create PR after all tests pass
```

---

## Best Practices

1. **Always snapshot first** — This is non-negotiable. You can't rollback without it.

2. **Test before approving** — Run the test suite and generation scripts locally before creating PR.

3. **Diff before applying** — Generate and review the diff to see exactly what will change.

4. **Peer review is mandatory** — Don't merge evolution changes without review.

5. **Document your reasoning** — Future you will thank present you.

6. **Measure impact** — Track before/after metrics for cost, speed, user satisfaction.

7. **Keep cycle log** — The structured log enables pattern detection and automation.

8. **Plan rollback early** — If something breaks, you want to know your exit route.

---

## FAQ

**Q: How often should we evolve?**
A: Quarterly (Feb/May/Aug/Nov) on schedule, plus ad-hoc when major capabilities land.

**Q: Can I evolve multiple things in one cycle?**
A: Yes, but keep changes related. Multiple unrelated changes = multiple cycles.

**Q: What if I'm unsure about a change?**
A: Test it locally, document uncertainty in PR, let reviewers decide.

**Q: Can I rollback part of a cycle?**
A: Not easily. Rollback goes to full snapshot. Better to fix forward in next cycle.

**Q: How long does a full cycle take?**
A: Plan 2-4 hours (analysis + testing + review + apply).

**Q: Who should do evolution cycles?**
A: Someone familiar with playbooks and Claude capabilities. Usually the playbook maintainer.

---

## Related Docs

- `commands/core/pb-evolve.md` — High-level evolution process
- `.playbook-metadata-schema.yaml` — Metadata field definitions
- `CHANGELOG.md` — Release history

