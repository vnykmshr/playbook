---
name: "pb-standup"
title: "Async Standup & Status Updates"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-resume', 'pb-cycle']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Async Standup & Status Updates

Keep team aligned on progress without synchronous meetings. Use this template for async standups, progress updates, or team check-ins during distributed work.

**Mindset:** Standups are where you surface blockers and risks.

Use `/pb-preamble` thinking: be direct about problems, don't hide issues to seem productive. Use `/pb-design-rules` thinking in standups: highlight when code embodies good design (Clarity, Simplicity, Robustness) and flag design risks early.

**Resource Hint:** sonnet — status reporting and team communication

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

### Yesterday [YES]
- [Task completed with link/PR/commit]
- [Task completed]

### Today in progress
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

### Yesterday [YES]
- Implemented user authentication endpoint (PR #234)
- Added unit tests for auth logic
- Fixed bug in password validation

### Today in progress
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
- **Task description** — Brief outcome
  - Where to find it: PR link, commit, test results, screenshot

**Guidelines:**
- One line per task (keep it scannable)
- Link to artifacts (PRs, commits, deployments)
- Focus on outcome, not effort ("Fixed login bug" not "Spent 3 hours debugging")
- Include both code and non-code work (reviews, meetings, docs)

**Example:**
```
### Yesterday [YES]
- Created payment webhook endpoint (PR #445)
- Added webhook signature validation tests
- Reviewed team's database design PR #440
- Updated API documentation
```

### Section 2: Today (Current Focus & Plans)

What you're working on right now and what's planned:
- in progress **Current task** — What you're actively coding on
- task **Planned task** — What comes next
- ⏸️ **Waiting on** — Things you're waiting for (feedback, approval, dependency)

**Guidelines:**
- Realistic scope (what you'll actually complete today)
- In priority order (what matters most first)
- Include dependencies ("Can't start integration tests until #450 merges")
- Flag if you're jumping contexts

**Example:**
```
### Today in progress
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

[YES] **DO:**
- Be specific ("Added validation for email input" not "Worked on form")
- Include links (PR, commit, dashboard, screenshot)
- Be honest about blockers and concerns
- Keep it scannable (bullet points, one thought per line)
- Write for someone who doesn't know the project

[NO] **DON'T:**
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

## Related Commands

- `/pb-start` — Begin work on a new feature or fix
- `/pb-resume` — Get back into context after a break
- `/pb-cycle` — Self-review and peer review during development

---

## Template to Copy

```markdown
## Standup: [Your Name] - [Date: YYYY-MM-DD]

### Yesterday [YES]
- [ ] Task 1
- [ ] Task 2

### Today in progress
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

## Building Team Culture Around Standups

Standups are more than status updates—they're about building trust and psychological safety.

### Create Psychological Safety for Blockers

**Why it matters**: Teams that feel safe reporting blockers unblock faster and ship better.

**Practice:**
- Celebrate blockers being surfaced ("Thank you for flagging that early")
- Never punish for being stuck (ask how to help instead)
- Public blockers → team problem-solving (not individual failure)
- Model vulnerability (leaders share their own blockers first)

**Example:**
```
Bad: "Why is auth still blocked? That's been 3 days."
Good: "I see auth is blocked on API review. How can we unblock that? Can I help review?"
```

### Celebrating Progress in Distributed Teams

**Weekly wins ritual:**
- Highlight completed features (not just checklist items)
- Call out helpful peer reviews, knowledge sharing, or mentoring
- Recognize cross-team collaboration
- Share customer feedback or metrics

**Why**: Distributed teams lack hallway conversations. Standups are a moment to feel part of something.

### Handling Sensitive Situations

**Scope changes or deprioritization:**
- Acknowledge the shift explicitly
- Explain impact (avoid sudden plan changes)
- Provide new timeline/expectations
- Ask if team has concerns

**Extended blockers (1+ week):**
- Escalate explicitly (not buried in standup)
- Propose solutions, don't just report problem
- Schedule dedicated unblocking session

**Team dynamics or personal issues:**
- Normalize "personal circumstances affecting focus" (no details needed)
- Offer flexibility without requiring explanation
- Check in 1-on-1 separately if you notice patterns

### Remote-First Best Practices

**Written standups work best because:**
- Asynchronous (no meeting fatigue)
- Skimmable (busy people can scan quickly)
- Searchable (reference past decisions/blockers)
- Inclusive (no one talking over each other)

**Make them effective:**
- Post at consistent time (start of day recommended)
- Don't require immediate responses (async means async)
- Link to artifacts (PRs, docs, tickets) not raw prose
- Read others' standups regularly (builds team awareness)

**Video standups (avoid):**
- Same latency as meeting but less scannable
- Makes async harder
- Use for real-time discussions, not status

### Standup Etiquette

**For writers:**
- Be honest about blockers (don't minimize)
- Include "needs help" asks (don't suffer silently)
- Link everything (help readers find context)

**For readers:**
- Read daily (takes 5 min, huge impact on collaboration)
- Respond to help requests same day (or delegate)
- Ask thoughtful follow-up questions (shows you're paying attention)

---

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
