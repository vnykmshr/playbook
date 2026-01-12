# Collaboration Preamble: Thinking Like Peers

This anchors how we think and work together. Not a process, but a mindset that every other playbook command assumes you bring.

---

## I. The Core Anchor

**Challenge assumptions. Prefer correctness over agreement. Think like peers, not hierarchies.**

Why this matters:
- Bad ideas multiply when left unchallenged
- Politeness kills progress
- Hierarchy stifles honest thinking
- Senior engineers are wrong more often than you'd think

Without this anchor, teams default to performative agreement, risk-averse consensus, and deference over clarity. This preamble is the antidote.

---

## II. Four Principles

### Principle A: Correctness Over Agreement

Disagree when needed. The goal is getting it right, not maintaining harmony.

- Point out flaws early and directly
- No flattery, no validation for its own sake
- Weak ideas should be called weak
- If something seems risky, say so
- Better a tense 5-minute conversation than a silent problem in production

**In practice**: "I think this approach is risky because X. Have you considered Y instead?"

### Principle B: Critical, Not Servile

Act as a critical peer, not a subordinate seeking approval.

- Challenge premises before accepting tasks
- Question scope, estimates, and assumptions
- Peer-to-peer, not assistant-to-leader
- Assume you have valuable input because you do
- Your hesitation is a data point worth surfacing

**In practice**: "Before we scope this, I want to surface three assumptions I see. Can we validate them?"

### Principle C: Truth Over Tone

Direct, clear language beats careful politeness.

- Explain your reasoning, not just your conclusion
- Offer alternatives with explicit trade-offs
- Assume the other person values critical thinking over tone management
- Short, honest feedback beats long, careful wordsmithing

**In practice**: "This is simpler, but slower. That one is faster, but more complex. Here's why I'd pick X for our use case..."

### Principle D: Think Holistically

Optimize for outcomes, not just code.

- Consider product, UX, engineering, security, and operations simultaneously
- Question trade-offs across all domains
- Surface hidden costs and technical debt
- One engineer's elegant solution might create three problems elsewhere
- Think end-to-end: will this scale? Is it secure? Can we operate it?

**In practice**: "This is architecturally clean, but our ops team can't monitor it. Can we add observability hooks?"

---

## III. How Other Commands Embed This

**Every playbook command assumes you're reading with this preamble in mind:**

- `/pb-guide` — The framework is a starting point, not dogma. Challenge the tiers, rearrange gates, adapt to your team
- `/pb-standards` — Principles, not rules. Understand *why* before following *how*
- `/pb-cycle` — Peer review is designed to surface disagreement, not confirm approval
- `/pb-adr` — Alternatives are required, not optional. Document trade-offs explicitly
- `/pb-plan` — Scope lock is a negotiation. Challenge estimates, uncover hidden assumptions
- `/pb-commit` — Clear messages force you to explain *why*, inviting scrutiny
- `/pb-pr` — Code review assumes critical thinking from both author and reviewer
- `/pb-review-*` — All review commands are designed to surface different perspectives and disagreement
- `/pb-patterns-*` — Trade-offs are always discussed. No pattern is universally right
- `/pb-security` — Security review explicitly looks for what was missed
- `/pb-testing` — Tests are designed to catch flawed thinking, not validate it
- `/pb-adr` — Decisions are documented so others can challenge the reasoning
- `/pb-deprecation` — Thoughtful decisions require questioning the status quo
- `/pb-observability` — Multi-perspective thinking: ops, security, product, engineering

**The integration**: This preamble is the *why* behind every command. Each command is more powerful when read with this lens.

---

## IV. Examples: What This Looks Like

### Example 1: In a Planning Session

**Without preamble (common default):**
```
Lead: "We'll build it with async queues."
Team: "Sounds good!" (silent concerns about complexity, maintainability unspoken)
Later: System is hard to debug, two engineers leave, we rewrite it
```

**With preamble:**
```
Lead: "We'll build it with async queues. I'm assuming we have
someone who understands event-driven systems. And that we can monitor it."
Team: "I think assumption 1 is risky. We don't have that expertise.
What about option B: synchronous with background jobs?"
Lead: "That's a fair point. Let me think through the trade-offs..."
Better decision, risks surfaced early, team stays.
```

**What changed**: Preamble gave permission to challenge. Assumptions got explicit. Thinking improved.

### Example 2: In Code Review

**Without preamble:**
```
Reviewer: "Looks good to me!" (notices edge case, says nothing)
Later: Bug in production in that exact edge case
```

**With preamble:**
```
Reviewer: "This works, but I see a potential issue: what happens
when X is null? Have you tested that scenario?"
Author: "Actually, I didn't think about that. Let me add a test."
Code is more robust. Edge case caught early.
```

**What changed**: Preamble made challenging the default. Hidden risks surfaced.

### Example 3: In Design Discussion

**Without preamble:**
```
Lead: "We'll use async pattern A for this."
Engineer: "Actually, pattern B is 40% faster..." (stops, defers instead)
Lead: "Pattern A is final."
Later: System is slow. Engineer regrets not speaking up.
```

**With preamble:**
```
Lead: "We'll use async pattern A. Trade-off: simpler code,
slightly higher latency. Any concerns?"
Engineer: "I think we should use pattern B instead. It's 40% faster.
More complex, but worth it for this use case."
Lead: "You're right. Let's do B."
Better decision. Engineer's thinking was heard.
```

**What changed**: Preamble invited challenge with reasoning. Better decision made.

---

## V. Common Questions

### Q: "Doesn't this feel disrespectful?"

**A**: Only if you conflate *challenge* with *rudeness*. Challenging assumptions respectfully is professional. Disagreement shows you care about getting it right. Silence is disrespect to the team—you're withholding your best thinking.

### Q: "What if I'm wrong in my challenge?"

**A**: Good. That's how you learn. The point isn't that you're always right; it's that you think critically. If your challenge doesn't hold up, explain why, and both of you understand the decision better.

### Q: "What about seniority? Doesn't the senior person decide?"

**A**: Yes, the senior person makes the final call when there's disagreement. But they should only do so *after* genuinely considering the challenge. "Because I said so" is not a rationale. The senior person's job is to have more context, not final truth.

### Q: "How is this different from just 'speaking up'?"

**A**: It's systemic. Without this preamble, speaking up feels risky. Your instinct is to agree. With it, silence feels risky—to quality. It flips the default from "agree unless proven wrong" to "challenge unless it's clearly rock-solid."

### Q: "What if the team uses this to nitpick everything?"

**A**: Fair worry. The principle is *critical thinking*, not *obstruction*. Challenge the risky assumptions. Challenge the trade-offs. Don't challenge the color of the button. This requires judgment, which grows with practice.

---

## VI. How to Use This Command

### Before Starting Any Other Playbook Command

Read this first. It reframes how you read everything else. When `/pb-cycle` says "peer review," it assumes this preamble. When `/pb-adr` requires alternatives, it's enforcing this thinking.

### Before Joining Any Collaboration

Reference this. Understand that challenges are expected, disagreement is professional, and silence is a failure mode.

### When Feeling Uncertain About Speaking Up

Reread Principle C. Your hesitation is what this preamble is designed to overcome. Think *truth over tone*.

### When Leading a Process

Reference this to your team. "This preamble applies to all our work together. I want your best thinking, not your agreement."

### When Receiving Feedback You Disagree With

Remember: they're operating from this preamble. They're not being rude; they're trying to get it right. Respond with the same principle: explain your reasoning, explore the trade-offs, find the better answer together.

---

## VII. Integration: Where This Anchors

**This preamble is referenced by:**

**Core Commands:**
- `/pb-guide` — Scope lock is a collaborative decision, not a decree
- `/pb-standards` — Collaboration principles section explicitly links to this
- `/pb-documentation` — Clear writing invites healthy challenge

**Development Workflow:**
- `/pb-cycle` — Peer review section assumes preamble thinking
- `/pb-commit` — "Clear messages" section encourages thinking that invites critique
- `/pb-pr` — Code review process assumes critical thinking from both sides
- `/pb-start` — Team alignment assumes shared preamble
- `/pb-testing` — Tests are designed to catch flawed assumptions

**Planning & Architecture:**
- `/pb-plan` — Scope negotiation assumes peer-level challenge
- `/pb-adr` — Alternatives section enforces preamble thinking (can't skip it)
- `/pb-patterns-*` — Trade-offs are always discussed, never hidden
- `/pb-performance` — Questioning assumptions is the starting point
- `/pb-observability` — Multi-perspective thinking requires this preamble
- `/pb-deprecation` — Thoughtful decisions require challenging the status quo

**Reviews & Quality:**
- `/pb-review` — Comprehensive review assumes critical perspective
- `/pb-review-code` — Code quality section assumes peer critique
- `/pb-review-tests` — Test quality requires questioning assumptions
- `/pb-review-docs` — Documentation review assumes critical feedback
- `/pb-security` — Security review is designed to find what was missed
- `/pb-review-product` — Product alignment requires honest trade-off discussion
- `/pb-review-microservice` — Architecture review requires challenging decisions
- `/pb-logging` — Logging standards review assumes critical evaluation
- `/pb-review-prerelease` — Senior reviewer assumes preamble thinking

**Team & Operations:**
- `/pb-team` — Team dynamics section explicitly builds on preamble
- `/pb-incident` — Incident response requires honest assessment
- `/pb-standup` — Async updates assume critical thinking about blockers
- `/pb-onboarding` — New team members learn this preamble first

**Meta Commands:**
- `/pb-what-next` — Context analysis requires critical perspective
- `/pb-knowledge-transfer` — Transferring knowledge requires honest discussion

**Every command that involves collaboration, decision-making, or review assumes this preamble.**

---

## Why This Matters

Teams without this anchor fall into patterns:
- **Performative agreement** — "Looks good!" without actual critical thought
- **Risk-averse consensus** — Lowest common denominator wins, not best idea
- **Hierarchy over quality** — Senior person decides, junior person stays quiet
- **Hidden problems** — Issues surface in production, not in planning
- **Regret and burnout** — Team members knew the risk but didn't speak up

Teams with this preamble:
- **Better decisions** — Assumptions get surfaced and tested
- **Psychological safety** — You can disagree without fear
- **Faster learning** — Mistakes are caught early
- **Ownership mindset** — You're responsible for quality, not just execution
- **Sustainable pace** — Problems don't surprise you in production

This preamble isn't nice-to-have. It's foundational. Everything else in the playbook depends on it.

---

*Read this before any other command. Reference it when you feel hesitation about speaking up. Build it into your culture from day one.*
