---
name: "pb-review-frontend"
title: "Frontend Review: Maya + Sam"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "parallel"
related_commands: ['pb-maya-product', 'pb-sam-documentation', 'pb-review-code', 'pb-standards', 'pb-a11y']
last_reviewed: "2026-02-12"
last_evolved: ""
---

# Frontend Review: Product & User Experience Focus

Multi-perspective code review combining **Maya Sharma** (Product & User Strategy) and **Sam Rivera** (Documentation & Clarity) expertise.

**When to use:** Frontend features, UI components, user-facing changes, design systems, API consumers.

**Resource Hint:** opus — User-centric thinking + clarity. Parallel execution of both agents recommended.

---

## How This Works

Two expert perspectives review in parallel, then synthesize:

1. **Maya's Review** — Product lens
   - Does this solve a real user problem?
   - Is scope bounded? Can we ship an MVP?
   - Is the solution clear to users?
   - Does this distract from higher priorities?

2. **Sam's Review** — Clarity lens
   - Can users understand this?
   - Is the interface self-evident?
   - Does documentation explain the "why"?
   - Will new team members understand this code?

3. **Synthesize** — Combined perspective
   - User-facing clarity + developer clarity
   - Are UI/UX changes aligned with product goals?
   - Is the implementation clear enough for maintenance?

---

## Maya's Product Review

**What Maya Examines:**

### 1. Problem Clarity
- [ ] Is the user problem clearly stated?
- [ ] Is it a real problem users face?
- [ ] Is it a common problem or edge case?
- [ ] Do we have data backing this up?

**Bad:** "Users might want dark mode." No evidence. Trendy.
**Good:** "40% of users use app at night. 63% requested dark mode in survey."

### 2. Solution Fit
- [ ] Does the proposed solution actually solve the problem?
- [ ] Are simpler alternatives considered?
- [ ] Could this be solved without building?

**Bad:** Problem: "Users need better reporting" → Solution: "50 visualization dashboard"
**Good:** Problem: "Users want to export data" → Solution: "CSV export button (1 day)" → Escalate to dashboard if >20% use

### 3. User Impact
- [ ] Will users notice this feature?
- [ ] Does it improve their lives or add complexity?
- [ ] How many users benefit?
- [ ] How much time does it save?

**Bad:** "Power users will appreciate this." Adds complexity for 5% of users.
**Good:** "30% of active users need this. 2 min task becomes 10 seconds."

### 4. Scope Creep Detection
- [ ] Is scope bounded (what's in/out)?
- [ ] Can we ship an MVP in 2 weeks or less?
- [ ] Are nice-to-haves separated from essentials?
- [ ] Is escalation trigger defined?

**Bad:** Search feature expands 7x over time. Never ships.
**Good:** MVP: "Basic text search". Launch → Gather data → Decide on filters.

### 5. Prioritization & Trade-offs
- [ ] Is this more important than next backlog item?
- [ ] Does this align with product strategy?
- [ ] What gets deprioritized?
- [ ] Is this a one-off request or strategic?

**Bad:** Build for every customer request → scattered product.
**Good:** Prioritize by user count + strategy alignment + effort.

**Maya's Checklist:**
- [ ] Real user problem identified (not assumed)
- [ ] Problem severity understood (how many users? how often?)
- [ ] Current workaround documented
- [ ] Simpler alternatives considered
- [ ] User benefit quantified
- [ ] Scope bounded (MVP-able in 2 weeks)
- [ ] Strategy alignment clear

**Maya's Automatic Rejection Criteria:**
- 🚫 Solving unvalidated problem
- 🚫 Proposing solution before understanding problem
- 🚫 Expanding scope without validation
- 🚫 Building one-off requests that distract from strategy
- 🚫 Treating nice-to-haves as essentials

---

## Sam's Clarity Review

**What Sam Examines:**

### 1. Audience Clarity
- [ ] Is the intended user clear?
- [ ] Are prerequisites stated?
- [ ] Does the UI assume prior knowledge?
- [ ] Can users self-serve (without asking for help)?

**Bad:** Complex interface. No explanation. Users confused.
**Good:** Clear onboarding. Tooltips explain why things matter.

### 2. Explicitness & Assumptions
- [ ] Are labels clear?
- [ ] Are implicit assumptions stated?
- [ ] Does the UI explain "why" (not just "what")?
- [ ] Can users understand without external docs?

**Bad:** Button labeled "Run Reconciliation". What does that do?
**Good:** Button labeled "Sync with Bank". Tooltip: "Compares our records with your bank statement and flags mismatches."

### 3. Completeness Without Bloat
- [ ] Are common questions answered (in UI or nearby docs)?
- [ ] Are examples provided for complex operations?
- [ ] Is there help for when things fail?
- [ ] Does it tell users where to go next?

**Bad:** Error message: "Connection failed". Nothing else.
**Good:** Error message: "Can't reach payment service. Retrying in 10 seconds. [Learn more] [Try now]"

### 4. Maintainability & Code Clarity
- [ ] Is component purpose clear from name?
- [ ] Are complex functions documented?
- [ ] Can new developer understand this code?
- [ ] Are architecture assumptions stated?

**Bad:** Component named "DataProcessor". Does what?
**Good:** Component named "PaymentReconciliationReport". Purpose obvious.

### 5. Accessibility & Structure
- [ ] Can keyboard users navigate?
- [ ] Are focus states visible?
- [ ] Do screen readers understand content?
- [ ] Can this be read at 200% zoom?

**Bad:** Icon-only buttons. No alt text.
**Good:** Icon + text. ARIA labels. Keyboard shortcuts.

**Sam's Checklist:**
- [ ] Intended user/audience is clear
- [ ] Prerequisites stated (or none)
- [ ] UI labels are explicit (not assuming knowledge)
- [ ] Common tasks discoverable
- [ ] Error messages helpful
- [ ] Code is readable by new developer
- [ ] Accessibility standards met (WCAG 2.1 AA)

**Sam's Automatic Rejection Criteria:**
- 🚫 Unclear intended audience
- 🚫 No examples for complex operations
- 🚫 Error messages assume prior knowledge
- 🚫 Code lacks clarity (unreadable without external docs)
- 🚫 Accessibility barriers (keyboard inaccessible, no alt text, poor contrast)

---

## Combined Perspective: Frontend Review Synthesis

**When Maya & Sam Agree:**
- ✅ Solves a real user problem AND is clearly communicated
- ✅ Approve for merging

**When They Disagree:**
Common disagreement: "Should we add this advanced feature?"
- Maya says: "Only 5% of users need this. Not worth the maintenance burden."
- Sam says: "If we add it, it needs clear documentation or it confuses everyone."
- Resolution: Either build and document well, or defer. Sam's documentation burden informs Maya's priority decision.

**Trade-offs to Surface:**
1. **Feature Simplicity vs User Capability**
   - Simpler UI = fewer options
   - More options = more documentation needed
   - Find the sweet spot

2. **Visual Simplicity vs Information**
   - Minimal design looks good but might hide features
   - Cluttered design shows everything but confuses users
   - Design hierarchy solves both

3. **Immediate Launch vs Documentation**
   - Launch fast with minimal docs → users confused
   - Document before launch → delays but prevents confusion
   - Balance based on audience (power users vs general users)

---

## Review Checklist

### Before Review Starts
- [ ] Self-review already completed (author did `/pb-cycle` step 1-2)
- [ ] Quality gates passed (lint, type check, tests all pass)
- [ ] UI/UX changes are visible (screenshots or demo)
- [ ] PR description explains what and why

### During Maya's Review
- [ ] User problem is validated
- [ ] Solution is appropriate
- [ ] Scope is bounded
- [ ] User benefit is quantified
- [ ] Strategic alignment is clear

### During Sam's Review
- [ ] UI is self-evident (doesn't require external docs)
- [ ] Code is readable by new developers
- [ ] Error messages are helpful
- [ ] Accessibility standards met
- [ ] Documentation (if needed) is clear

### After Both Reviews
- [ ] Feedback synthesized
- [ ] Trade-offs explained
- [ ] User value is clear
- [ ] Approval given (or revisions requested)

---

## Review Decision Tree

```
1. Does the feature solve a real user problem (Maya)?
   NO → Ask to validate problem first
   YES → Continue

2. Is the solution clearly communicated (Sam)?
   NO → Ask to clarify UI/code/docs
   YES → Continue

3. Is there a scope/priority disagreement?
   YES → Discuss (often about maintenance burden)
   NO → Continue

4. Is the code ready to merge?
   YES → Approve
   NO → Request specific revisions
```

---

## Example: Dark Mode Review

**Code Being Reviewed:** Dark mode theme toggle

### Maya's Review:
**Product Check:**
- ✅ Problem validated: 40% of users use app at night
- ✅ User survey: 63% requested dark mode
- ❌ Issue: Scope includes both light and dark + auto-detection
- ✅ MVP: Just dark toggle (no auto-detection)
- ✅ Aligned with product: Competitive parity

**Maya's Recommendation:** Approve toggle only. Defer auto-detection to v2.

### Sam's Review:
**Clarity Check:**
- ❌ Problem: Toggle is icon-only, unclear what it does
- ✅ Good: Theme applies to all pages consistently
- ❌ Problem: Component code is complex (no comments)
- ❌ Problem: No accessibility label on toggle
- ✅ Good: Colors have sufficient contrast

**Sam's Recommendation:** Add label to toggle. Add comments to theme logic. Add ARIA labels.

### Synthesis:
**Trade-off Identified:** Auto-detection adds complexity. Neither Maya nor Sam wants it in MVP.
- Maya: "Too many features initially"
- Sam: "Auto-detection is complex to document"

**Approval:** Conditional on Sam's clarity fixes (labels, comments, accessibility).

---

## Related Commands

- **Maya's Deep Dive:** `/pb-maya-product` — Problem validation, scope discipline, user impact
- **Sam's Deep Dive:** `/pb-sam-documentation` — Reader-centric thinking, clarity, accessibility
- **Code Review:** `/pb-review-code` — General code review (both agents apply)
- **Accessibility:** `/pb-a11y` — Detailed accessibility review (reference standard)
- **Standards:** `/pb-standards` — Coding principles both agents apply

---

## When to Escalate

**Escalate to Linus (Security)** if:
- Code handles authentication, PII, or sensitive data
- Client-side security matters
- API integration has security implications

**Escalate to Alex (Infrastructure)** if:
- Feature impacts performance (client or server)
- Scaling implications (large data sets)
- Infrastructure dependencies

**Escalate to Jordan (Testing)** if:
- Complex interactions need testing strategy
- Edge cases are unclear
- Concurrency matters

---

*Frontend review: Solves a real problem + clearly communicated*

