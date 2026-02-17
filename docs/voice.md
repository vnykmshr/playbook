# Command Voice & Communication Style

How playbook commands talk to you.

---

## Philosophy

Commands are peers, not procedures. We communicate dev-to-dev: direct, authentic, reasoning-forward. You get the *why*, not a checklist.

**This means:**

- **Prose over templates** — Explanation embedded in narrative, not bullet-pointed
- **Specific reasoning** — "This N+1 will scale poorly (20ms now → 2s at 100K records)" vs "consider performance"
- **Context-aware** — Small changes get conversational prose; architecture changes get structured reasoning
- **No artificial formality** — We skip the bot-speak ("it is recommended that...") and talk like peers

---

## What You'll See

### Code Review Feedback (`/pb-review`)

**Instead of:**
```
## Issues Found
- Type: Performance
  - Location: queries.py:45
  - Severity: High
  - Recommendation: Add index
```

**You get:**
```
Your query loop hits the database on every iteration. With 100K records, this goes from 20ms to 2 seconds. Add an index or batch the queries—either takes about 15 minutes.
```

Why? Because you need to know *what matters* (scale impact) and *how hard* (effort), not just a structured diagnosis.

### Scope Capture (`/pb-start`)

**Instead of:**
```
Q1: Feature type? (greenfield/existing)
Q2: Risk level? (low/medium/high)
Q3: Timeline? (flexible/fixed)
```

**You get:**
A conversation: "Tell me what you're building—is this greenfield or adding to existing services? What's the riskiest part?" Questions emerge from what you describe.

### Commit Messages

**Why:** They explain *reasoning*, not just what changed.

```
fix(auth): extract oauth service

Tighter boundaries make this reusable in other services and
easier to test. Prep for microservice migration.
```

Not just: "Extract oauth service."

---

## When Structure Appears

**Small changes** (< 50 LOC): Prose, minimal structure.

**Medium changes** (50–150 LOC): Narrative with light headers where needed.

**Large changes** (150+ LOC, multiple concerns): Structured, but still authentic voice.

**Architecture decisions**: Detailed reasoning with explicit tradeoffs.

**Multi-stakeholder communication** (release notes, migration guides): Scannable structure because clarity requires it.

**Why this matters:** Structure earns its place. It's not applied by default.

---

## Anti-Patterns You Won't See

| Don't | We Don't Do |
|------|-----------|
| Hedging | "It may be helpful to consider..." |
| Filler | "Let's dive into...", "Here's the thing..." |
| Passive voice | "Changes should be made to..." |
| Third-person reporting | "The code exhibits tight coupling" |
| Vague metrics | "This could be faster" |
| False politeness | "Thank you for considering..." |

We assume you're sharp and direct. Peer to peer.

---

## Matching Project Conventions

Commands adapt to your project's style. If your repo uses:
- Structured ADRs → We respect that format
- Detailed checklists → We follow that convention
- Markdown with frontmatter → We honor it

The voice stays authentic; the *structure* matches context.

---

## Key Principle

**Clarity through focus, not format.**

One idea per sentence. Specific examples. Concrete thresholds. Active voice. Direct address. The point comes first; the reasoning follows.

---

## Related

- **Global guidelines:** Developers working on the playbook use `/pb-voice` and internal voice guidelines to maintain consistency
- **Each command:** Documents its own communication style in the command description
- **Your workflow:** Commands adapt this voice to your preferences via `/pb-preferences`

---

*v1.0 | Updated 2026-02-17*
