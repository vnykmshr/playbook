# Preamble Quick Reference Guide

**One-page guide to preamble thinking. For detailed guidance, see `/pb-preamble` and its parts (async, power, decisions).**

---

## The Core Anchor

**Challenge assumptions. Prefer correctness over agreement. Think like peers, not hierarchies.**

---

## Four Principles

| Principle | Means | In Practice | Not |
|-----------|-------|-------------|-----|
| **Correctness Over Agreement** | Get it right, not harmony | "I think this is risky because X. Have you considered Y?" | Flattery or false consensus |
| **Critical, Not Servile** | Think as peer, not subordinate | "Before we scope this, let me surface three assumptions" | Deferring just because they're senior |
| **Truth Over Tone** | Direct, clear language | "This is simpler but slower. That's faster but complex. I'd choose X for us." | Careful politeness that obscures meaning |
| **Think Holistically** | Optimize outcomes, not just code | "This is architecturally clean, but can ops monitor it?" | Siloed thinking that creates problems elsewhere |

---

## Quick Decision: When to Challenge vs. Trust

### CHALLENGE WHEN:
- ✓ Assumptions are unstated ("We need X" — why?)
- ✓ Trade-offs are hidden ("Simple solution" — at what cost?)
- ✓ Risk is glossed over ("Production-ready" — tested failure modes?)
- ✓ Scope is unclear ("Add this feature" — what's done?)
- ✓ Process is unfamiliar (first time, don't understand why)
- ✓ Context has changed ("We always do X" — still true?)
- ✓ Your expertise applies (you have info they don't)

### TRUST WHEN:
- ✓ Expert explained reasoning (you understand their thinking)
- ✓ You lack context (outside your domain, they have info you don't)
- ✓ Time cost exceeds benefit (challenging button color wastes time)
- ✓ Decision is made, executing now (stop re-litigating, align)
- ✓ Pattern is proven ("20 times this way, it works")
- ✓ You're learning from them (understand their reasoning instead)

---

## The Challenge Framework

### How to Challenge Effectively

```
1. Understand their perspective first
   "I understand you're deciding X because [reason], right?"

2. Name your concern directly
   "I have a concern: [specific issue]"

3. Show your reasoning
   "Why: [evidence, experience, logic]"

4. Ask what you're missing
   "What am I missing about this?"
```

### Challenge Rules

| Rule | Do This | Don't Do This |
|------|---------|---------------|
| **What to challenge** | Ideas, decisions, assumptions | People, character, competence |
| **With what** | Evidence and reasoning | Feelings and vibes |
| **Where** | Public for ideas, private for character | Never publicly attack someone |
| **How often** | 2-3 things per month (not meeting) | Challenge everything (become noise) |

---

## Async Quick Rules

| Situation | What to Do |
|-----------|-----------|
| **Writing challenge** | Write as if explaining to team. Name concern directly. Show reasoning. |
| **Missing context** | Quote relevant context. Explain your frame. State assumptions. |
| **Decision taking too long** | Set decision clock: "We'll decide Friday EOD. I'll announce Monday." |
| **Feeling unclear** | Ask clarifying questions, don't assume. Reference specific earlier statements. |
| **Disagreement in PR** | Direct but specific: "I see value here. Concern: [specific]. Trade-off: [reason]" |

---

## Hierarchy Quick Rules

| Situation | What to Do | What NOT to Do |
|-----------|-----------|---|
| **Junior challenging senior** | Use evidence. Build credibility first. Ask what you're missing. | Defer just because they're senior. |
| **Senior person challenged** | Actually listen. Explain your reasoning. Sometimes change your mind. | Dismiss. Defend. Punish disagreement. |
| **Decision you disagree with** | Execute well. Document concern if serious. Watch if it fails. | Sabotage. Hope it fails. Go silent. |
| **Escalating disagreement** | Only if: safety, ethics, or legality violated. Document it. | Use escalation as disagreement override. |

---

## Decision Clocks

### When You Need to Decide

**Announce before discussion:**
```
Timeline: Now to [DATE EOD] — discuss
Decision: [DATE MORNING] — I decide
Options: [List with trade-offs]
Input needed: [What matters]
Revisit: In [TIMEFRAME] if [CONDITIONS]
```

**After decision:**
- Explain your reasoning (why you chose this)
- Acknowledge concerns (even ones you didn't address)
- Be clear about revisit conditions
- Document it (future reference)

---

## Loyalty After Disagreement

| Level | Your Stance | Example |
|-------|-----------|---------|
| **1: Alignment** | "I disagree but I understand. Let's execute." | Normal path for most disagreements |
| **2: Documented** | "I want this recorded: I flagged risk X." | For serious concerns you want noted |
| **3: Escalate** | "I can't execute this. Violates [safety/ethics/law]." | Very rare. Career-affecting. |
| **4: Leave** | "This represents fundamental mismatch." | Extremely rare. Only if core values conflict. |

**Key:** Loyalty ≠ Agreement. You disagree AND execute well.

---

## Failure Modes: Quick Diagnosis

**Your team might be in trouble if:**

| Symptom | What's Wrong | Fix |
|---------|-------------|-----|
| Everyone agrees with senior person | **Pseudo-safety** — challenge is punished subtly | Leaders must visibly change mind when challenged |
| Meetings never end, decisions keep reopening | **Perpetual debate** — no decision clock | Set specific decision dates and stick to them |
| Person who challenged is now quiet | **Punishment recognized** — challenge got consequences | Check in 1-on-1. Show next challenge is safe. |
| Half the team stops speaking | **Argumentative culture** — everything challenged | Distinguish: strategic decisions debate more, tactical decide faster |
| Senior person asserts without reasoning | **Authority over correctness** — hierarchy winning | Require: "Here's why" before decisions. Invite challenge. |
| People complain in hallways not meetings | **Lost faith in process** — challenges feel pointless | Make one example where challenge changed outcome |

---

## Post-Decision Learning

**When something fails:**

| Wrong Approach | Right Approach |
|---|---|
| "That decision was stupid. Jane should have known." | "We assumed X. It turned out false. What does that teach us?" |
| "Why didn't we see that coming?" | "With information we had then, this was reasonable. New info changed outcome." |
| "Never do that again" | "For next time: test this assumption earlier, have reversal plan" |

**Good post-mortem:**
1. Acknowledge outcome (not judgment)
2. Review assumptions (what was wrong)
3. Understand why (what changed/what we missed)
4. Extract learning ("For next time...")
5. Document it (so history teaches)

---

## Quick Checklist: Am I Using Preamble Thinking?

- [ ] I challenge decisions I disagree with, not just comply
- [ ] My challenges include reasoning, not just feelings
- [ ] I distinguish between when to challenge and when to trust
- [ ] I execute decisions well even when I disagreed
- [ ] I ask clarifying questions instead of assuming
- [ ] I can name concerns directly without being harsh
- [ ] I see failed decisions as learning, not failure
- [ ] I change my mind when challenged with good reasoning
- [ ] I document why I decided, not just what
- [ ] The best ideas win, not the senior person's ideas

**Yes to most?** You're using preamble thinking.
**No to many?** Read the full guidance: `/pb-preamble` + relevant parts.

---

## Quick Navigation

**I need guidance on...**

| Question | Read |
|----------|------|
| Core mindset | `/pb-preamble` — sections I-V |
| When to challenge | `/pb-preamble` — section II.5 |
| Failure modes | `/pb-preamble` — section VIII |
| Async communication | `/pb-preamble-async` |
| Challenging my boss | `/pb-preamble-power` — section VI |
| Building team safety | `/pb-preamble-power` — section VII |
| Decision clocks | `/pb-preamble-decisions` — section II |
| After I lose an argument | `/pb-preamble-decisions` — section III |
| Learning from failures | `/pb-preamble-decisions` — section VI |

---

## The Test

**Is your team using preamble thinking?**

Look for these signals:

✅ **Good signs:**
- People disagree in meetings without fear
- Leaders sometimes change their minds
- Problems surface in discussion, not production
- New people feel safe asking questions
- Senior person's idea gets challenged
- Mistakes become learning opportunities
- Execution is strong because alignment happened

❌ **Warning signs:**
- Everyone agrees with the senior person
- Meetings get longer, not shorter
- People check out mentally after decisions
- Hallway complaints instead of meeting challenges
- New people quickly learn to stay quiet
- Same mistakes happen twice

---

## Remember

**Preamble thinking is:**
- About how you think together
- A foundation for all other playbook commands
- Progressive (build over time)
- Scalable (works small to large)
- Hard initially, natural eventually

**It's not:**
- Being rude
- Constant debate
- Ignoring hierarchy
- Free-for-all disagreement
- Never making decisions

**The goal:** Better thinking wins. Better decisions happen. Better execution follows.

---

*For complete guidance, read `/pb-preamble` and parts 2-4. This is the quick version.*
