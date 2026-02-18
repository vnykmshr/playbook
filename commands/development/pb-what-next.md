---
name: "pb-what-next"
title: "Recommend Next Playbook Command"
category: "development"
difficulty: "advanced"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-cycle', 'pb-commit', 'pb-pr', 'pb-release']
last_reviewed: "2026-02-18"
last_evolved: "2026-02-18"
version: "2.0.0"
version_notes: "v2.13.1: Clarified title from 'What's Next?' to emphasize command recommendation based on git state"
breaking_changes: []
---
# Recommend Next Playbook Command

Get context-aware playbook command recommendations based on your current work state.

**Mindset:** This tool assumes both `/pb-preamble` thinking (challenge recommendations, don't follow blindly) and `/pb-design-rules` thinking (verify design decisions at each stage).

The recommendations are starting points, not rules. Question them. Challenge the suggestion if you think a different path makes more sense. Use this as a thinking tool, not an oracle.

**Resource Hint:** haiku — git state analysis and command recommendation

---

## When to Use

Run this command when you're unsure which playbook command to use next. The command analyzes:
- **Git state**: Current branch, modified files, commit history
- **File types**: What you're working on (code, docs, tests, etc.)
- **Work phase**: Early stage, mid-work, ready for review, etc.

---

## Status

✅ **Available Now** (Phase 3+)

The `/pb-what-next` command is fully implemented and ready to use. It analyzes your git state and recommends the next playbook commands automatically.

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

## Real-World Examples

### Example 1: Starting a Feature

**Your Situation:**
- Branch: `feature/user-auth`
- Commits: 0
- Changes: None

**Recommendation Output:**
```
Recommended Next Steps
━━━━━━━━━━━━━━━━━━━

1. `/pb-start` — Start Development Work
   - Begin iterative development
   - Time: 5 min
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

1. `/pb-cycle` — Development Cycle
   - Self-review + peer review
   - Confidence: 90% | Time: 45 min

2. `/pb-testing` — Advanced Testing
   - Verify test coverage
   - Confidence: 85% | Time: 5 min

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

1. `/pb-commit` — Atomic Commits
   - Organize into logical commits
   - Confidence: 90% | Time: 10 min

2. `/pb-pr` — Quick PR Creation
   - Create pull request
   - Confidence: 90% | Time: varies

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

1. `/pb-release` — Release Preparation
   - Prepare for production
   - Time: 45 min

2. `/pb-deployment` — Deployment Strategies
   - Plan deployment
   - Time: 5 min

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
- **Phase**: Detected workflow phase (START, DEVELOP, FINALIZE, REVIEW, RELEASE)
- **Changes**: Number of modified files and their types

### Recommended Next Steps
Each recommendation includes:
- **Command name**: Which `/pb-*` command to run next
- **Purpose**: Brief description of what the command does
- **Confidence**: 0.6-1.0 score indicating how certain the recommendation is
- **Time**: Estimated duration (5 min to 2 hours)

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
- Branch name matters: use `feature/*`, `fix/*`, `refactor/*` naming for best results

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

4. **Use with feature/fix/refactor branch naming**
   - `feature/new-feature` → Development workflow
   - `fix/bug-name` → Bug fix workflow
   - `refactor/cleanup` → Refactor workflow
   - Naming helps the tool detect your intent

5. **Combine with `/pb-standup` for tracking**
   - Run `/pb-what-next` to see what's next
   - Complete that step
   - Run `/pb-standup` to track progress
   - Repeat until work is ready to merge

---

## How It Works

The command analyzes your current situation and recommends relevant commands:

### Branch Analysis
- **feature/*** branch? → Development workflow
- **fix/*** branch? → Bug fix workflow
- **refactor/*** branch? → Refactor workflow
- Just merged to main? → Release workflow

### File Analysis
- Changed **tests/**? → Run `/pb-testing`
- Changed **docs/**? → Use `/pb-documentation`
- Changed **src/** + **tests/**? → Full cycle needed
- No tests changed? → Add test coverage with `/pb-testing`

### Time-Based Recommendations
- Early in feature? → `/pb-start`, `/pb-cycle`, `/pb-standards`
- Mid-feature? → `/pb-cycle`, `/pb-testing`
- Ready to finalize? → `/pb-commit`, `/pb-pr`
- Code review? → `/pb-review-hygiene`, `/pb-review-tests`, `/pb-security`
- Release time? → `/pb-release`, `/pb-deployment`

---

## Example Output

```
📊 Current Work State
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Branch:    feature/v1.3.0-user-auth
Files:     3 changed (src/, tests/)
Status:    Mid-feature, tests need updating

✅ RECOMMENDED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔄 /pb-cycle  →  Self-review + peer feedback
   "Self-review your changes and get peer feedback on approach"
   Time: 30-60 minutes

2. ✅ /pb-testing  →  Verify test coverage
   "Ensure your tests match your changes"
   Time: 10 minutes

3. 🎯 /pb-commit  →  Craft atomic commits
   "Organize your work into logical commits"
   Time: 5 minutes

4. 🔗 /pb-pr  →  Create pull request
   "Submit your work for integration"
   Time: 10 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 WHY THESE COMMANDS?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Both src/ and tests/ changed  → You're doing TDD (good!)
• Tests modified recently       → Run /pb-testing to verify coverage
• Feature branch active         → You're in development mode
• No commits yet                → Time to wrap up and PR
```

---

## Related Commands

- `/pb-start` — Begin feature work (creates branch)
- `/pb-cycle` — Self-review + peer review loop
- `/pb-commit` — Craft atomic commits
- `/pb-pr` — Create pull request
- `/pb-release` — Release preparation

---

## How It Differs from Other Commands

| Command | Purpose | When |
|---------|---------|------|
| `/pb-what-next` | Recommend next action | Unsure, need guidance |
| `/pb-start` | Create branch, establish rhythm | Starting feature |
| `/pb-cycle` | Self-review + peer review | After coding a unit |
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
git log --oneline -10        # Recent commits
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
Maps your situation to one of 5 phases:
- **START** (0 commits, fresh branch)
- **DEVELOP** (1-4 commits, active changes)
- **FINALIZE** (5+ commits, ready to wrap up)
- **REVIEW** (PR created, in review)
- **RELEASE** (on main branch, deployment time)

### 4. Recommendation Generation
Uses your phase + file types to suggest commands:
- Phase-based: Different commands for each workflow phase
- File-type-based: Test changes trigger `/pb-testing`, doc changes trigger `/pb-documentation`
- Confidence scoring: Each recommendation gets 0.6-1.0 confidence based on match strength

### 5. Metadata-Driven
Uses `.playbook-metadata.json` for:
- Command titles, purposes, tiers
- Time estimates per command
- Related commands and integrations

---

## Recommended Workflow

Typical development session:

```
1. START
   └─ /pb-start       Create branch
                      Time: 5 min

2. DEVELOP
   └─ /pb-cycle       Iterate (repeat 3-5x)
      /pb-testing     Verify tests
                      Time: 30-60 min per iteration

3. FINALIZE
   └─ /pb-commit      Organize commits
      /pb-pr          Create PR
                      Time: 15 min

4. REVIEW
   └─ /pb-review-hygiene Code review
      /pb-review-tests Test review
      /pb-security     Security check
                       Time: 30-60 min

5. MERGE & DEPLOY
   └─ /pb-release     Release checklist
      /pb-deployment   Deploy strategy
                       Time: 1-2 hours
```

At any point, run `/pb-what-next` to confirm you're on the right path.

---

## Tips

- **Stuck?** Run `/pb-what-next --verbose` for detailed explanations
- **Learning?** Check "Related Commands" to understand the full workflow
- **Customizing?** Edit command recommendations by improving command metadata
- **Tracking?** Use `/pb-standup` to record daily progress
- **Templates?** Use `/pb-templates` for starting code templates

---

## Next Steps

After getting recommendations:
1. Run the suggested command
2. Complete that step
3. Come back and run `/pb-what-next` again
4. Repeat until your work is ready to merge

Tip: Each command should take 5-60 minutes. If a step takes longer, you may need to break it into smaller pieces.

---

*Auto-generated recommendations based on git state, file changes, and command metadata.*
*Last updated: 2026-01-12*
