# Frequently Asked Questions

Common questions about the Engineering Playbook.

---

## Getting Started

### Q: What is the Engineering Playbook?
**A:** The Engineering Playbook is a decision framework—a set of 45 commands and guides that codify how to approach development work. It covers planning, development, code review, release, and team operations. It's not a tool, but a structured process that reduces friction and maintains quality at every step.

### Q: Do I have to use all 45 commands?
**A:** No. Start with the commands that address your current challenges. Most teams begin with `/pb-plan`, `/pb-cycle`, and `/pb-release`. You can adopt others gradually as you need them.

### Q: How long does it take to learn the playbook?
**A:** You can start using key commands (like `/pb-start`, `/pb-cycle`, `/pb-commit`) in a few hours. Mastering the full system takes a few weeks of regular use. The playbook is designed to be adopted incrementally.

### Q: Can I use the playbook with my existing tools?
**A:** Yes. The playbook works with any tech stack, version control system, and CI/CD platform. It's tool-agnostic by design.

### Q: Does the playbook require Claude Code?
**A:** The playbook is designed to work with Claude Code, but the concepts and processes work in any development environment. The commands are formatted as Claude Code prompts, but you can adapt them for other AI assistants or human reviewers.

---

## Installation & Setup

### Q: How do I install the playbook?
**A:** Clone the repository and run the install script:
```bash
git clone https://github.com/vnykmshr/playbook.git
cd playbook
./scripts/install.sh
```
This creates symlinks in `~/.claude/commands/` making all 45 commands available in Claude Code.

### Q: I ran the install script but commands aren't showing up. What do I do?
**A:** Check that `~/.claude/commands/` exists and has the symlinks:
```bash
ls -la ~/.claude/commands/ | grep pb-
```
If the directory doesn't exist, create it and re-run the install script. If symlinks are broken, check that the source files exist in your cloned playbook repository.

### Q: How do I uninstall the playbook?
**A:** Run the uninstall script:
```bash
./scripts/uninstall.sh
```
This removes all symlinks from `~/.claude/commands/`.

### Q: Can I install the playbook in multiple locations?
**A:** Yes. Each playbook installation is independent. You can have different playbook versions in different directories.

---

## Workflows

### Q: What's the difference between `/pb-cycle` and `/pb-pr`?
**A:**
- `/pb-cycle` is for iterative development and review before committing
- `/pb-pr` is for creating the pull request after your code is approved and committed

**Sequence**: Develop → `/pb-cycle` (self-review + peer review) → Approve → `/pb-commit` → `/pb-pr`

### Q: Do I have to use `/pb-todo-implement`?
**A:** No. `/pb-todo-implement` is for structured implementation with checkpoint-based review if you want extra feedback during development. Use `/pb-cycle` if you prefer simpler iteration without checkpoints.

### Q: How often should I commit?
**A:** Commit after each meaningful unit of work. Guidelines:
- New feature → `feat:` commit
- Bug fix → `fix:` commit
- Refactor → `refactor:` commit
- Tests → `test:` commit
- Config/build → `chore:` commit

Don't commit every 5 lines; don't wait until end-of-day. Commit logically.

### Q: What if I need to skip a step (like testing)?
**A:** Don't. Quality gates exist to catch problems early. If a step feels unnecessary, discuss with your team about removing it, but don't skip it unilaterally. If you're in a crisis (incident), use `/pb-incident` for the emergency workflow.

### Q: How do I handle urgent hotfixes?
**A:** Use `/pb-incident` which has a streamlined workflow for emergency fixes. It covers fast mitigation (rollback, hotfix, disable feature) without the normal review burden.

---

## Code Review

### Q: Who should do code review?
**A:** A senior engineer perspective is ideal for `/pb-cycle` peer review. They should understand:
- System architecture and patterns
- Correctness and edge cases
- Maintainability and naming
- Security implications
- Test quality

### Q: What if a reviewer requests changes I disagree with?
**A:** In the playbook process, you iterate:
1. Request review
2. Reviewer identifies issues
3. You fix or discuss
4. If unresolved, escalate to tech lead or discuss as a team

The key principle: **Fix the issue, don't argue.** If you believe the reviewer is wrong, fix it their way, get approval, then propose a different approach next time.

### Q: How long should code review take?
**A:** Target: 24 hours max. Aim for:
- Small PRs reviewed in 2-4 hours
- Medium PRs reviewed in 4-8 hours
- Large PRs reviewed next business day

If reviews are taking longer, consider smaller, more frequent PRs.

### Q: Can I review my own code?
**A:** You do `/pb-cycle` self-review before requesting peer review. Self-review catches obvious issues, but a peer review from another engineer is always required before merging.

---

## Testing & Quality

### Q: How much test coverage should I aim for?
**A:** The playbook targets:
- Unit tests: Core business logic (aim for 80%+)
- Integration tests: Critical workflows
- E2E tests: User-facing features
- Don't aim for 100%—aim for meaningful coverage

Use `/pb-testing` for detailed guidance.

### Q: Should I write tests before or after code?
**A:** Either approach works:
- **TDD (Test-First)**: Write tests, then code to pass them
- **Test-Alongside**: Write code and tests together
- **Test-After**: Code first, then comprehensive tests

The playbook requires tests before `/pb-cycle` peer review. Choose the approach that works for your team.

### Q: How do I handle flaky tests?
**A:** Flaky tests are technical debt. If you encounter a flaky test:
1. Fix it before merging your change
2. Document why it was flaky
3. Add it to your team's "flaky tests" tracking

Use `/pb-review-tests` to identify flaky test patterns across the codebase.

---

## Documentation & Communication

### Q: Should I document everything?
**A:** No. Document:
- **Why** decisions were made (not just the what)
- **Non-obvious** code logic
- **Public APIs** and contracts
- **Architectural decisions** (via `/pb-adr`)
- **Operational runbooks** for production systems

Skip documentation for self-explanatory code.

### Q: How do I stay on top of architecture documentation?
**A:** Use `/pb-adr` to record decisions as you make them, not after. This prevents "documentation debt" where decisions are undocumented.

### Q: Should I write standups if I'm co-located?
**A:** Yes. Async standups (via `/pb-standup`) help:
- Maintain clear documentation of progress
- Enable async team members
- Create a searchable record

Even co-located teams benefit from written standups.

---

## Patterns & Architecture

### Q: How do I choose between `/pb-patterns-core`, `/pb-patterns-async`, etc.?
**A:** Use the decision guide:
1. Start with `/pb-patterns-core` for fundamental patterns
2. If you need async/concurrent behavior, check `/pb-patterns-async`
3. If you need database concerns, check `/pb-patterns-db`
4. If you're building distributed systems, check `/pb-patterns-distributed`

All patterns can be combined; they're not mutually exclusive.

### Q: Can I use multiple patterns together?
**A:** Yes. Most real systems use multiple patterns. Example:
- **Core pattern**: Event-Driven (from `/pb-patterns-core`)
- **Async pattern**: Job Queues (from `/pb-patterns-async`)
- **Database pattern**: Connection Pooling (from `/pb-patterns-db`)

Document the combination in your `/pb-adr`.

### Q: What if I don't like a suggested pattern?
**A:** The patterns are recommendations, not requirements. If a pattern doesn't fit your constraints:
1. Understand why it was suggested
2. Identify alternative patterns
3. Document your choice in `/pb-adr` with rationale

---

## Performance & Optimization

### Q: When should I optimize?
**A:** Follow this sequence:
1. **Build it correctly first** (readable, maintainable)
2. **Measure** (use `/pb-performance` profiling)
3. **Optimize bottlenecks** (not guesses)
4. **Verify** (re-measure after optimization)

Don't optimize prematurely.

### Q: How do I know if my system is performant?
**A:** Use `/pb-performance` to:
- Define performance targets
- Profile your system
- Identify bottlenecks
- Optimize iteratively
- Verify improvements

---

## Incident Response

### Q: What's the difference between P0, P1, P2, P3?
**A:** Severity levels from `/pb-incident`:
- **P0**: All users affected, complete service outage
- **P1**: Major user subset affected, significant degradation
- **P2**: Limited users affected, feature broken
- **P3**: Minor impact, cosmetic issues

Severity determines mitigation speed and strategy.

### Q: Should I do a post-mortem for every incident?
**A:** Guidelines:
- **P0/P1**: Post-mortem required (24 hours)
- **P2**: Post-mortem recommended (if recurring)
- **P3**: Post-mortem optional

Use `/pb-incident` for comprehensive analysis.

### Q: How do I prevent the same incident twice?
**A:** Three steps:
1. Post-mortem via `/pb-incident` (root cause)
2. Document via `/pb-adr` (decision to prevent recurrence)
3. Implementation (preventative fix in next sprint)

---

## Team & Growth

### Q: How do I onboard a new team member quickly?
**A:** Use `/pb-onboarding` for structured approach:
- Preparation phase (before they start)
- First day (orientation)
- First week (knowledge transfer, frameworks)
- Ramp-up (contribute first feature)
- Growth (ongoing development)

### Q: What should I do in a retrospective?
**A:** Use `/pb-team` for structured retrospective:
- What went well? (celebrate)
- What could improve? (action items)
- How do we implement? (next steps)

Monthly retrospectives maintain team health.

### Q: How do I handle conflict on my team?
**A:** Use `/pb-standards` to define team working principles:
- Clear communication norms
- Decision-making process
- Conflict resolution approach

Most conflicts stem from unclear expectations; standards clarify them.

---

## Release & Operations

### Q: When should I release?
**A:** Release when:
- Feature is complete and tested
- Code reviewed and approved
- Pre-release checks pass (via `/pb-release`)
- Team agrees on timing

Don't release on Friday unless it's critical.

### Q: What deployment strategy should I use?
**A:** Use `/pb-deployment` to choose:
- **Blue-Green**: Zero downtime, instant rollback (safest)
- **Canary**: Gradual rollout to subset (recommended)
- **Rolling**: Progressive replacement (traditional)
- **Feature Flag**: Dark deploy, enable on command (most control)

Blue-Green and Feature Flag are safest for production.

### Q: How do I monitor my system after release?
**A:** Use `/pb-observability` to:
- Set up key metrics (errors, latency, throughput)
- Configure alerting thresholds
- Create runbooks for common issues
- Establish on-call rotation

Monitor for at least 30 minutes after release.

---

## Integration & Customization

### Q: Can I customize the playbook for my team?
**A:** Yes. The playbook is a framework, not dogma:
- Adapt commands to your workflow
- Add team-specific checklists
- Modify processes based on learnings
- Document your customizations

Keep core principles; customize implementation.

### Q: How do I integrate with existing tools (CI/CD, GitHub, Slack)?
**A:** The playbook works with any tools:
- Embed commands in CI/CD pipelines
- Reference commands in GitHub templates
- Post command results to Slack
- Use commands in documentation

Examples: Use `/pb-testing` output in CI, `/pb-security` checks in PRs, `/pb-incident` timeline in Slack.

### Q: Can I use the playbook with other frameworks?
**A:** Yes. The playbook complements:
- Agile/Scrum (use `/pb-plan` for sprints)
- Kanban (use `/pb-cycle` for continuous flow)
- SAFe (use `/pb-adr` for enterprise decisions)
- Anything (it's process-agnostic)

---

## Getting Help

### Q: Where do I find a specific command?
**A:** Use the [Decision Guide](decision-guide.md) or [Command Reference](command-index.md).

### Q: I found a bug or have a feature request. What do I do?
**A:** [Open an issue on GitHub](https://github.com/vnykmshr/playbook/issues).

### Q: How do I contribute to the playbook?
**A:** See [CONTRIBUTING.md](https://github.com/vnykmshr/playbook/blob/main/CONTRIBUTING.md) for guidelines.

### Q: I'm still confused about something. Where do I ask?
**A:** Options:
1. Check the [Getting Started](getting-started.md) guide
2. Read the [Integration Guide](integration-guide.md)
3. Check this FAQ
4. [Ask in GitHub Discussions](https://github.com/vnykmshr/playbook/discussions)
5. [Open an issue](https://github.com/vnykmshr/playbook/issues) describing your situation

---

## Version & Updates

### Q: How often is the playbook updated?
**A:** The playbook follows semantic versioning:
- **Patch** (v1.2.1): Bug fixes, clarifications
- **Minor** (v1.3.0): New commands, workflow improvements
- **Major** (v2.0.0): Breaking changes to existing commands

See [version history in README](https://github.com/vnykmshr/playbook/blob/main/README.md#version-history).

### Q: How do I update to a new version?
**A:**
```bash
cd playbook
git pull origin main
./scripts/install.sh    # Reinstall symlinks for new commands
```

### Q: Will updates break my existing workflows?
**A:** No. The playbook maintains backward compatibility within major versions. If breaking changes are needed, they happen in major version releases with clear migration paths.

---

## Troubleshooting

### Q: I cloned the playbook but commands aren't working. What do I do?
**A:**
1. Verify installation: `ls ~/.claude/commands/ | grep pb-`
2. Check symlinks exist: `ls -la ~/.claude/commands/pb-*`
3. Verify original files exist: `ls commands/*/*.md` in playbook directory
4. Re-run install script: `./scripts/install.sh`

### Q: A command isn't doing what I expected. How do I fix it?
**A:**
1. Re-read the command documentation carefully
2. Check [Decision Guide](decision-guide.md) to ensure it's the right command
3. Look at examples in the command
4. [Open an issue on GitHub](https://github.com/vnykmshr/playbook/issues)

### Q: My team doesn't want to use the playbook. What do I do?
**A:**
1. Start with a single command that solves your team's biggest pain point
2. Show the value (time saved, quality improved)
3. Gradually introduce more commands as adoption increases
4. Customize processes to fit your team's culture

The playbook is a tool to help, not a mandate.

---

## Still Have Questions?

- **[Decision Guide](decision-guide.md)** — Find commands by situation
- **[Command Reference](command-index.md)** — Browse all 45 commands
- **[Getting Started](getting-started.md)** — Quick start guide
- **[Integration Guide](integration-guide.md)** — How commands work together
- **[GitHub Issues](https://github.com/vnykmshr/playbook/issues)** — Report problems
- **[GitHub Discussions](https://github.com/vnykmshr/playbook/discussions)** — Ask questions
