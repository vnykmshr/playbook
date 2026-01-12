# What's Next?

Get context-aware playbook command recommendations based on your current work state.

---

## When to Use

Run this command when you're unsure which playbook command to use next. The command analyzes:
- **Git state**: Current branch, modified files, commit history
- **File types**: What you're working on (code, docs, tests, etc.)
- **Work phase**: Early stage, mid-work, ready for review, etc.

---

## Status

⚠️ **This command is documented for Phase 2, implementation comes in Phase 3 (with CI/CD automation).**

Currently, this guide helps you understand how context-aware discovery works. The actual `/pb-what-next` implementation will analyze your git state and recommend commands automatically.

## Planned Usage (Phase 3)

```bash
# See recommendations for your current state (implementation in Phase 3)
/pb-what-next

# This command will analyze:
# - Git branch and changed files
# - Work phase (early, mid-feature, ready for review)
# - Related commands from metadata
# - Workflow suggestions
```

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
- Code review? → `/pb-review-code`, `/pb-review-tests`, `/pb-security`
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
- `/pb-testing` — Verify test coverage
- `/pb-commit` — Craft atomic commits
- `/pb-pr` — Create pull request
- `/pb-review-code` — Code review
- `/pb-security` — Security review
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

## How the Implementation Will Work (Phase 3)

The `/pb-what-next` command will use intelligent analysis:

1. **Git State Analysis**
   ```bash
   git branch --show-current
   git status --porcelain
   git log --oneline -10
   git diff --name-only
   ```

2. **File Type Detection**
   - Patterns: `tests/**`, `docs/**`, `src/**`, `.github/workflows/**`
   - Language: `.go`, `.py`, `.ts`, `.js`, `.md`
   - Config: `Dockerfile`, `docker-compose.yml`, `package.json`, etc.

3. **Workflow Matching**
   - Maps current state to one of the 5 key workflows
   - Shows commands in recommended order
   - Estimates time per step

4. **Metadata-Driven**
   - Uses `.playbook-metadata.json` for command details
   - Shows purpose, tier, related commands
   - Pulls decision_context for conditional logic

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
   └─ /pb-review-code Code review
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
