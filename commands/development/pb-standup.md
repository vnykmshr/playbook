# Async Standup & Status Updates

Keep team aligned on progress without synchronous meetings. Use this template for async standups, progress updates, or team check-ins during distributed work.

---

## Purpose

Async standups provide visibility into:
- What work got done and what's in progress
- Blockers or help needed
- Team rhythm and cadence
- Historical record of progress

**When to use:**
- Daily async standups (instead of sync meetings)
- Multi-day/week feature progress updates
- Milestone check-ins during long-running work
- Handoff documentation when someone takes over work
- End-of-week team status summarization

---

## Quick Template (5 min to write)

```markdown
## Standup: [Your Name] - [Date]

### Yesterday ✅
- [Task completed with link/PR/commit]
- [Task completed]

### Today 🔄
- [Current focus]
- [Planned task]

### Blockers 🚧
- [What's blocking progress, if anything]

### Help Needed ❓
- [Specific ask, if any]

### Notes (optional)
[Anything else useful for team context]
```

**Example:**
```markdown
## Standup: Sarah - 2026-01-13

### Yesterday ✅
- Implemented user authentication endpoint (PR #234)
- Added unit tests for auth logic
- Fixed bug in password validation

### Today 🔄
- Refactoring database queries for performance
- Adding integration tests for auth flow
- Pairing with James on API contract

### Blockers 🚧
- None currently

### Help Needed ❓
- Review for PR #234 when you get a chance

### Notes
- Performance improvements showing good results
- Database indexes now properly configured
```

---

## Detailed Template (Comprehensive)

Use when you need to provide more context or detailed progress update.

### Section 1: Yesterday (What Got Done)

List completed work from the previous working day:
- ✅ **Task description** — Brief outcome
  - Where to find it: PR link, commit, test results, screenshot

**Guidelines:**
- One line per task (keep it scannable)
- Link to artifacts (PRs, commits, deployments)
- Focus on outcome, not effort ("Fixed login bug" not "Spent 3 hours debugging")
- Include both code and non-code work (reviews, meetings, docs)

**Example:**
```
### Yesterday ✅
- Created payment webhook endpoint (PR #445)
- Added webhook signature validation tests
- Reviewed team's database design PR #440
- Updated API documentation
```

### Section 2: Today (Current Focus & Plans)

What you're working on right now and what's planned:
- 🔄 **Current task** — What you're actively coding on
- 📋 **Planned task** — What comes next
- ⏸️ **Waiting on** — Things you're waiting for (feedback, approval, dependency)

**Guidelines:**
- Realistic scope (what you'll actually complete today)
- In priority order (what matters most first)
- Include dependencies ("Can't start integration tests until #450 merges")
- Flag if you're jumping contexts

**Example:**
```
### Today 🔄
- Debugging rate limiter edge case (in progress, hoping to complete by noon)
- Adding caching layer to user queries (if rate limiter done)
- Waiting on QA sign-off from yesterday's changes before deploying
```

### Section 3: Blockers (What's Stuck)

What's preventing progress and needs intervention:
- 🚧 **Blocker description** — What's stuck and why
  - Impact: How much does this affect you?
  - Needed: What's required to unblock?

**Example:**
```
### Blockers 🚧
- Database migration script timing out (testing on staging)
  - Impacting: Can't ship auth refactor until migration works
  - Need: DBA to review migration strategy or provide alternative approach
```

### Section 4: Help Needed (Explicit Requests)

What you explicitly need from others:
- ❓ **Specific ask** — Exactly what you need
  - Who: Who should help (name or team)
  - By when: Urgency (ASAP, this week, next week)

**Example:**
```
### Help Needed ❓
- Code review on PR #456 (auth refactor)
  - Who: Tech lead or senior engineer
  - Urgency: Need feedback this afternoon to stay on schedule
- Clarification on payment reconciliation logic
  - Who: Product/finance team
  - Urgency: Next 2 days is fine
```

### Section 5: Notes & Context (Optional)

Anything else useful for team understanding:
- Metrics or measurements (performance improvements, test coverage)
- Architecture decisions made
- Risks or concerns noticed
- Positive progress or momentum
- Learning or interesting findings
- Upcoming changes that affect the team

**Example:**
```
### Notes
- Performance improvements: Query time down 40% with new indexing
- Upcoming: Payment vendor API deprecates v1 next month, starting migration planning
- Pairing tomorrow with frontend team on integration testing
- All tests passing, no blockers beyond those noted above
```

---

## By Work Type

### Feature Development Standup

Focus on:
- Feature completion percentage
- Design decisions made
- Integration points with other systems
- Timeline status (on track, at risk, etc.)

### Bug Fix Standup

Focus on:
- Root cause found/confirmed
- Solution approach
- Testing coverage
- Deployment plan

### Refactoring Standup

Focus on:
- Refactoring scope
- Testing strategy
- Risk assessment
- Performance impact

### Multi-Week Project Standup

Expand to include:
- Phase progress (which phase, % complete)
- Dependency status (are we blocked on other teams?)
- Team capacity (any changes to resource availability?)
- Risks or mitigation actions taken

---

## Best Practices

### Writing Effective Standups

✅ **DO:**
- Be specific ("Added validation for email input" not "Worked on form")
- Include links (PR, commit, dashboard, screenshot)
- Be honest about blockers and concerns
- Keep it scannable (bullet points, one thought per line)
- Write for someone who doesn't know the project

❌ **DON'T:**
- Over-explain ("Spent 2 hours debugging" — just say "Fixed bug X")
- Use jargon without context
- Make excuses ("Lots of meetings" — just note if it affected progress)
- Go too long (standup should take 5 min to write, 2 min to read)

### Frequency & Timing

**Daily standups** (async):
- Post at start of your day (before you start coding)
- Team reads async throughout the day
- No meeting needed
- Updates morale and transparency

**Weekly standups** (for M/L tier work):
- Friday EOD or Monday morning
- Summarize week's progress
- Highlight risks or blockers
- Great for distributed teams

**Milestone standups** (for long-running work):
- After significant milestone
- Broader audience (stakeholders, product)
- More formal tone
- Includes metrics and outcomes

### Using Standups for Async Alignment

Standups create a paper trail of:
- What was built and why
- Decisions made and rationale
- Blockers and how they were resolved
- Team coordination without meetings

**Read standups before:**
- Meetings (know what's already happened)
- Code reviews (understand context)
- Planning (understand where we are)

---

## Integration with Playbook

**Part of workflow:**
- `/pb-start` → Creates feature branch, work begins
- `/pb-standup` → Daily async visibility (YOU ARE HERE)
- `/pb-cycle` → Iteration with reviews
- `/pb-pr` → Merge to main
- `/pb-release` → Deploy

**Related Commands:**
- `/pb-start` — Starting a feature (pre-standup)
- `/pb-cycle` — Iteration & reviews (happens during standups)
- `/pb-pr` — Opening PR (post-standup when ready)
- `/pb-resume` — Resuming after break (first thing, write standup)

---

## Template to Copy

```markdown
## Standup: [Your Name] - [Date: YYYY-MM-DD]

### Yesterday ✅
- [ ] Task 1
- [ ] Task 2

### Today 🔄
- [ ] Current work
- [ ] Next task

### Blockers 🚧
- None (or describe)

### Help Needed ❓
- None (or describe)

### Notes
- (optional: metrics, risks, context)
```

---

## FAQ

**Q: How detailed should standups be?**
A: Detailed enough that someone unfamiliar with the task understands progress. Link to PRs/commits for details.

**Q: What if I'm blocked and can't make progress?**
A: Explicitly state the blocker in the "Blockers" section. Be specific about what's needed to unblock.

**Q: Can I skip a standup if nothing changed?**
A: No, write it anyway. Even "No progress (waiting on external API response)" is useful for team visibility.

**Q: Should I include meetings/interruptions?**
A: Only if they significantly affected work. "Lots of meetings" is context but not as useful as "Pairing on auth design with team lead".

**Q: How long should a standup take?**
A: 5 minutes to write, 2 minutes to read. If it's longer, you're over-explaining.

---

*Created: 2026-01-11 | Category: Development | Updated: When first shipped*
