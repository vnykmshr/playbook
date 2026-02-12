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
version: "1.1.0"
version_notes: "Initial v2.11.0 (Phase 1-4 enhancements)"
breaking_changes: []
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

See `/pb-maya-product` for the comprehensive product strategy framework and checklist.

**For frontend-specific review, focus on:**
- **Problem Validation:** Is this a real user problem (data-backed) or assumed?
- **User Impact:** How many users benefit? How much does it improve their experience?
- **Scope Discipline:** Is the MVP shippable in 2 weeks? Are nice-to-haves separated?
- **UX Consequences:** Does this add complexity? Could users misuse it?
- **Trade-offs:** Is this feature worth the ongoing maintenance burden?

**Maya's Red Flags for Frontend:**
- Building without user research or validation
- Scope undefined or expanding over time
- Feature benefits only 5% of users but adds UI complexity
- Nice-to-have features presented as essentials

---

## Sam's Clarity Review

See `/pb-sam-documentation` for the comprehensive clarity framework and checklist.

**For frontend-specific review, focus on:**
- **UI Clarity:** Are labels explicit? Do users understand without needing help?
- **Accessibility:** Can keyboard users navigate? Is focus visible? WCAG 2.1 AA compliant?
- **Error Messages:** Do errors explain what happened AND how to fix it?
- **Code Readability:** Can a new developer understand component purpose from the code?
- **Documentation:** Are complex interactions explained? Are assumptions stated?

**Sam's Red Flags for Frontend:**
- Icon-only buttons without text or ARIA labels
- Error messages assume prior knowledge ("Connection failed")
- Component names unclear (e.g., "DataProcessor" vs. "PaymentReconciliationReport")
- No focus states or keyboard navigation support

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

