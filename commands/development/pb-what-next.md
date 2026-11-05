---
name: "pb-what-next"
title: "Recommend Next Playbook Command"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-forge', 'pb-commit', 'pb-pr', 'pb-release']
last_reviewed: "2026-11-05"
version: "2.1.0"
version_notes: "v2.1.0: Example Output is a real run of the script; the other examples are labelled illustrative and carry no times. Four phases are detected, as the script does; branch names other than main or master change nothing; the commit count is the branch's own commits since the default branch. Recommended Workflow is the daily ritual, with hygiene and test reviews periodic; /pb-review replaces /pb-cycle in the comparison table; /pb-templates is SDLC and quality templates."
breaking_changes: []
---
# Recommend Next Playbook Command

Get context-aware playbook command recommendations based on your current work state.

**Mindset:** This tool assumes both `/pb-preamble` thinking (challenge recommendations, don't follow blindly) and `/pb-design-rules` thinking (verify design decisions at each stage).

The recommendations are starting points, not rules. Question them. Challenge the suggestion if you think a different path makes more sense. Use this as a thinking tool, not an oracle.

**Resource Hint:** sonnet - Git state analysis and context-aware command recommendation.

---

## When to Use

Run this command when you're unsure which playbook command to use next. The command analyzes:
- **Git state**: Current branch, modified files, commit history
- **File types**: What you're working on (code, docs, tests, etc.)
- **Work phase**: Early stage, mid-work, ready for review, etc.

---

## Status

It analyzes your git state and recommends the next playbook commands. It needs a playbook clone: it runs `scripts/analyze-playbook-context.py`, which `install.sh` does not link.

## Usage

```bash
# Get recommendations for your current state
python scripts/analyze-playbook-context.py

# Get detailed analysis with reasoning
python scripts/analyze-playbook-context.py --verbose

# Use custom metadata file
python scripts/analyze-playbook-context.py --metadata /path/to/metadata.json
```

This command analyzes:
- Git branch and changed files
- Commit count and work phase
- File types (source, tests, docs, config, CI)
- Related commands from metadata
- Workflow patterns

---

## Examples (Illustrative)

Abridged sketches of what each phase recommends; Example Output below is a real run.

### Example 1: Starting a Feature

**Your Situation:**
- Branch: `feature/user-auth`
- Commits: 0
- Changes: None

**Recommendation Output:**
```
Recommended Next Steps
━━━━━━━━━━━━━━━━━━━

1. `/pb-start` - Start Development Work
   - Begin iterative development
```

**Why:** You've just created the branch. `/pb-start` helps establish the rhythm for your work.

### Example 2: Mid-Feature Development

**Your Situation:**
- Branch: `feature/user-auth`
- Commits: 3
- Changes: Both `src/auth.py` and `tests/test_auth.py` modified

**Recommendation Output:**
```
Recommended Next Steps
━━━━━━━━━━━━━━━━━━━

1. `/pb-cycle` - Development Cycle
   - Self-review + peer review
   - Confidence: 90%

2. `/pb-testing` - Advanced Testing
   - Verify test coverage
   - Confidence: 85%

Why These Commands?
━━━━━━━━━━━━━━━━━━━

• Both source and test files changed → Full development cycle
• 3 commits → Time to iterate on feedback
• Active feature branch → In development mode
```

**Why:** You're actively coding. `/pb-cycle` helps with self-review and peer feedback, while `/pb-testing` ensures your tests match your code.

### Example 3: Ready to Submit

**Your Situation:**
- Branch: `feature/user-auth`
- Commits: 5
- Changes: All staged

**Recommendation Output:**
```
Recommended Next Steps
━━━━━━━━━━━━━━━━━━━

1. `/pb-commit` - Atomic Commits
   - Organize into logical commits
   - Confidence: 90%

2. `/pb-pr` - Quick PR Creation
   - Create pull request
   - Confidence: 90%

Why These Commands?
━━━━━━━━━━━━━━━━━━━

• 5+ commits → Time to organize with /pb-commit
• All changes staged → Ready for PR
• Feature branch → Ready to integrate
```

**Why:** Your work is ready to submit. `/pb-commit` helps organize into clean commits, then `/pb-pr` creates the pull request.

### Example 4: On Main Branch (Release Time)

**Your Situation:**
- Branch: `main`
- Commits: 10+
- Changes: None

**Recommendation Output:**
```
Recommended Next Steps
━━━━━━━━━━━━━━━━━━━

1. `/pb-release` - Release Preparation
   - Prepare for production

2. `/pb-deployment` - Deployment Strategies
   - Plan deployment

Why These Commands?
━━━━━━━━━━━━━━━━━━━

• On main branch → Release mode detected
• Multiple commits → Ready for release checklist
• Clean working directory → All changes are committed
```

**Why:** You're on main. It's time to prepare the release and plan deployment.

---

## Output Interpretation Guide

### Current Work State
- **Branch**: The git branch you're on (feature/*, fix/*, main, etc.)
- **Phase**: Detected workflow phase (START, DEVELOP, FINALIZE, RELEASE)
- **Changes**: Number of modified files and their types

### Recommended Next Steps
Each recommendation includes:
- **Command name**: Which `/pb-*` command to run next
- **Purpose**: Brief description of what the command does
- **Confidence**: A percentage indicating how certain the recommendation is
- **Time**: From the command's tier in metadata: 5, 10, 25 or 45 min, or varies

### Confidence Levels
- **0.90-1.0** (Very High): Direct match to your situation
- **0.80-0.90** (High): Strong pattern match from context
- **0.70-0.80** (Moderate): Inferred from related changes
- **0.60-0.70** (Low): Suggested based on workflow

### Why These Commands?
Explains the reasoning:
- File types changed (source, tests, docs, config, CI)
- Commit count and phase detection
- Detected work patterns

---

## Troubleshooting

### "Metadata file not found"
**Problem:** The command can't find `.playbook-metadata.json`

**Solution:** Run the metadata extraction command:
```bash
python scripts/extract-playbook-metadata.py
```

This generates the metadata that `/pb-what-next` uses for command details.

### "No recommendations"
**Problem:** You get an empty recommendations list

**Solution:**
1. Verify you're in a git repository: `git status`
2. Create or modify files to establish context
3. Run with `--verbose` to see detailed analysis: `python scripts/analyze-playbook-context.py --verbose`

### "Unexpected recommendations"
**Problem:** Recommendations don't match your expectations

**Solution:**
- Run with `--verbose` to see how the phase was detected
- Check your git state: `git status`, `git log --oneline -5`
- Only `main` and `master` change the phase (RELEASE); other branch names do not

### "Can't analyze git state"
**Problem:** Git analysis fails

**Solution:**
- Ensure you're in a git repository: `git init` if needed
- Ensure git is installed: `git --version`
- Check git permissions: `ls -la .git`

---

## Tips & Best Practices

1. **Run after each unit of work**
   - After coding a feature, run `/pb-what-next`
   - After code review feedback, run `/pb-what-next`
   - At any point when you're unsure what to do next

2. **Use verbose mode to understand decisions**
   ```bash
   python scripts/analyze-playbook-context.py --verbose
   ```
   See detailed traces of how phases were detected and why

3. **Follow recommendations in order**
   - First recommendation is the highest priority
   - Each command builds on the previous one
   - Complete each step before returning for new recommendations

4. **Combine with `/pb-standup` for tracking**
   - Run `/pb-what-next` to see what's next
   - Complete that step
   - Run `/pb-standup` to track progress
   - Repeat until work is ready to merge

---

## How It Works

The command analyzes your current situation and recommends relevant commands:

### Phase Recommendations
- START (no commits, clean tree) → `/pb-start`
- DEVELOP → `/pb-cycle`, `/pb-testing`
- FINALIZE → `/pb-commit`, `/pb-pr`
- RELEASE (on `main` or `master`) → `/pb-release`, `/pb-deployment`

DEVELOP and FINALIZE name the manual path. In the ritual, `/pb-review` commits and `/pb-pr` follows. The script also holds a REVIEW set (`/pb-review-code`, `/pb-review-tests`, `/pb-security`) that no git state reaches.

### File Analysis
- Changed **tests/**? → `/pb-testing`
- Changed **docs/** or Markdown? → `/pb-documentation`
- Changed **.github/workflows/**? → `/pb-deployment`

---

## Example Output

A real run on a branch of this repo (`python3 scripts/analyze-playbook-context.py`):

```text
# Current Work State
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Branch**: `stabilize`
**Phase**: FINALIZE
**Changes**: 22 files changed (docs/)
**Commits**: 10 recent commits

# Recommended Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **`/pb-pr`** — Quick PR Creation
   - Create pull request for integration
   - Confidence: 90% | Time: 5 min

2. **`/pb-documentation`** — Writing Great Engineering Documentation
   - Documentation changed, ensure clarity
   - Confidence: 75% | Time: 5 min

3. **`/pb-commit`** — Commit (Usually Automatic)
   - Organize work into logical commits
   - Confidence: 90% | Time: 45 min

# Why These Commands?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Multiple commits → Time to organize and prepare for integration
• Documentation updated → Ensure clarity and completeness

# Tips
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Run `/pb-what-next --verbose` for detailed analysis
- Each command should take 5-60 minutes
- Return here after each step for updated recommendations
```

---

## Related Commands

- `/pb-start` - Begin feature work (creates branch)
- `/pb-forge` - Drive a deliverable through its arc (the executing twin of this command)
- `/pb-commit` - Craft atomic commits
- `/pb-pr` - Create pull request
- `/pb-release` - Release preparation

---

## How It Differs from Other Commands

| Command | Purpose | When |
|---------|---------|------|
| `/pb-what-next` | Recommend next action | Unsure, need guidance |
| `/pb-start` | Create branch, establish rhythm | Starting feature |
| `/pb-review` | Quality gate; commits on pass | After coding a unit |
| `/pb-release` | Release checklist | Preparing for production |

Use `/pb-what-next` when in doubt. It analyzes your situation and points you to the right command.

---

## How the Implementation Works

The `/pb-what-next` command analyzes your situation through these steps:

### 1. Git State Analysis
Runs these git commands to understand your work:
```bash
git branch --show-current    # Current branch
git status --porcelain       # Modified files
git log --oneline main..HEAD # This branch's commits
git diff --name-only         # Files changed
```

Returns: branch name, changed files, commit count, unstaged/staged changes

### 2. File Type Detection
Categorizes changes by type:
- **Tests**: Files matching `*test*.py`, `*.spec.ts`, etc.
- **Docs**: Markdown files, documentation directories
- **Source**: Code files (`.py`, `.ts`, `.js`, `.go`, `.rs`)
- **Config**: Docker, package.json, pyproject.toml, etc.
- **CI**: GitHub Actions workflows, CI config files

### 3. Workflow Phase Detection
Maps your situation to one of 4 phases:
- **START** (0 commits, clean tree)
- **DEVELOP** (1-4 commits, active changes)
- **FINALIZE** (5+ commits, or committed and clean)
- **RELEASE** (on `main` or `master`)

The commit count is the branch's own commits since it left the default branch (`origin/HEAD`, else `main`, else `master`).

### 4. Recommendation Generation
Uses your phase + file types to suggest commands:
- Phase-based: Different commands for each workflow phase
- File-type-based: Test changes trigger `/pb-testing`, doc changes trigger `/pb-documentation`
- Confidence scoring: Each recommendation gets a confidence based on match strength

### 5. Metadata-Driven
Uses `.playbook-metadata.json` for:
- Command titles, purposes, tiers
- Time estimates per command
- Related commands and integrations

---

## Recommended Workflow

The daily ritual, by phase:

```text
1. START      /pb-start           Scope and branch
2. DEVELOP    code → /pb-review   Gate; commits on pass (repeat)
3. FINALIZE   /pb-pr              Open the PR
4. REVIEW     /pb-review-code     Peer review of the PR
5. RELEASE    /pb-release         Readiness gate, tag, deploy
```

`/pb-review-hygiene` and `/pb-review-tests` are periodic checks, not steps of each PR. At any point, run `/pb-what-next` to confirm you're on the right path.

---

## Tips

- **Stuck?** Run `/pb-what-next --verbose` for detailed explanations
- **Learning?** Check "Related Commands" to understand the full workflow
- **Customizing?** Edit command recommendations by improving command metadata
- **Tracking?** Use `/pb-standup` to record daily progress
- **Templates?** Use `/pb-templates` for SDLC and quality templates

---

## Next Steps

After getting recommendations:
1. Run the suggested command
2. Complete that step
3. Come back and run `/pb-what-next` again
4. Repeat until your work is ready to merge

---

*Auto-generated recommendations based on git state, file changes, and command metadata.*
