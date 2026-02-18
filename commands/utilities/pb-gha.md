---
name: "pb-gha"
title: "GitHub Actions Failure Analysis"
category: "utilities"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-doctor', 'pb-debug', 'pb-review-hygiene', 'pb-release']
last_reviewed: "2026-02-18"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial release — structured CI failure investigation"
breaking_changes: []
---
# GitHub Actions Failure Analysis

Structured investigation of GitHub Actions failures. Follows a 6-step methodology: identify what failed, assess flakiness, find the breaking commit, analyze root cause, check for existing fixes, and report.

Works with any GitHub Actions workflow. Requires `gh` CLI authenticated.

**Mindset:** Apply `/pb-debug` thinking — reproduce before theorizing. Apply `/pb-preamble` thinking — challenge the obvious explanation. A "flaky test" might be a real race condition. A "random failure" might be a dependency change.

**Resource Hint:** sonnet — log analysis, pattern matching, and structured investigation

---

## When to Use

- CI pipeline fails and you need to understand why
- Recurring failures that might be flaky vs. genuinely broken
- Pre-release when CI must be green and something is red
- After merging a PR that broke CI on main

---

## Usage

```
/pb-gha [URL or context]
```

**Examples:**
- `/pb-gha https://github.com/org/repo/actions/runs/12345`
- `/pb-gha` (analyzes the current repo's latest failed run)
- `/pb-gha the lint job keeps failing on main`

---

## Step 1: Identify the Failure

Figure out exactly what failed. Not the workflow — the specific job and step.

```bash
# Get the latest failed run (or use provided URL)
gh run list --status failure --limit 5

# View the specific run
gh run view <run-id>

# Get the logs for the failed job
gh run view <run-id> --log-failed
```

**What to look for:**
- The exit code 1 trigger — not warnings, the actual failure
- Error messages vs. noise (deprecation warnings aren't failures)
- Which step in the job failed (build, test, lint, deploy)
- The commit that triggered this run

---

## Step 2: Assess Flakiness

Check whether this is a one-off or a pattern. The key is checking the *specific failing job*, not just the workflow.

```bash
# List recent runs of the workflow
gh run list --workflow <workflow-name> --limit 20

# For each run, check if the specific job passed or failed
# Look for patterns: always fails? fails on certain branches? intermittent?
```

**Flakiness indicators:**
- Same job fails intermittently on the same branch → likely flaky
- Job fails consistently after a specific date → likely a real breakage
- Job fails only on certain branches → likely a code issue
- Job fails at random intervals → timing issue, race condition, or external dependency

**Calculate:**
- Success rate over last 20 runs
- When it last passed
- When it first started failing

---

## Step 3: Find the Breaking Commit

If the failure is consistent (not flaky), pinpoint when it started.

```bash
# Find the last passing run
gh run list --workflow <workflow-name> --status success --limit 1

# Find the first failing run
# Compare: what commits landed between the last success and first failure?

# View the commit that introduced the failure
gh run view <first-failing-run-id> --json headSha
git log --oneline <last-good-sha>..<first-bad-sha>
```

**Verification:** The job should pass consistently before the breaking commit and fail consistently after it. If it's intermittent on both sides, it's not a clean break — look for a flakiness trigger instead.

---

## Step 4: Analyze Root Cause

With the logs, history, and breaking commit (if found), determine what's actually going wrong.

**Common root causes:**

| Category | Examples |
|----------|---------|
| Code change | Test assertion broken, API contract changed, import error |
| Dependency | Package version bumped with breaking change, lockfile drift |
| Environment | Runner image updated, tool version changed, disk space |
| Timing | Race condition, timeout too short, external service slow |
| Configuration | Workflow syntax, permissions, secrets expired |

**Root cause checklist:**
- Read the actual error message (not just the job name)
- Check if the failing code was recently modified
- Check if dependencies were updated (lockfile diff)
- Check if the runner environment changed (ubuntu-latest vs pinned)
- Check for external service dependencies (APIs, registries)

---

## Step 5: Check for Existing Fixes

Before writing a fix, check if someone already has one.

```bash
# Search open PRs for the error message or affected file
gh pr list --state open --search "<error keyword>"

# Check if there's a related issue
gh issue list --search "<error keyword>"

# Check if main has moved ahead with a fix
git log origin/main --oneline --since="yesterday" -- <affected-file>
```

---

## Step 6: Report

Synthesize findings into a clear report.

```markdown
## GHA Failure Report

**Workflow:** [name]
**Job:** [name]
**Step:** [name]
**Run:** [URL]

### Failure
[What specifically failed — the actual error, not the job name]

### Flakiness
[One-off / Intermittent (N/20 failures) / Consistent since [date]]

### Breaking Commit
[SHA and summary, or "N/A — flaky" if intermittent]

### Root Cause
[What's actually wrong and why]

### Existing Fix
[PR link if found, or "None found"]

### Recommendation
[What to do — fix, retry, pin version, skip, etc.]
```

---

## Quick Mode

For simple "CI is red, what happened?" situations:

```bash
# One-liner: show the latest failure's logs
gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId' \
  | xargs gh run view --log-failed
```

Then follow up with the full methodology if the cause isn't obvious.

---

## Integration with Other Commands

| Situation | Follow Up |
|-----------|-----------|
| Root cause is a code bug | `/pb-debug` for systematic fix |
| Root cause is test flakiness | `/pb-review-tests` for reliability audit |
| Root cause is infra/config | `/pb-review-infrastructure` for resilience check |
| Blocking a release | `/pb-release` once green |
| Recurring problem | `/pb-review-hygiene` for systemic health |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Re-run without investigating | Understand the failure first |
| Blame "flaky tests" without data | Check the last 20 runs for actual flakiness rate |
| Fix the symptom (skip test) | Fix the root cause |
| Assume the obvious explanation | Verify with logs and history |
| Ignore intermittent failures | Intermittent = real bug with a timing component |

---

## Related Commands

- `/pb-debug` — Systematic debugging methodology
- `/pb-doctor` — Local system health check
- `/pb-review-hygiene` — Codebase operational health
- `/pb-release` — Release orchestration (needs green CI)

---

**Last Updated:** 2026-02-18
**Version:** 1.0.0
