---
name: "pb-calm-design"
title: "Calm Design: Attention-Respecting Features & Systems"
category: "reviews"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "checklist"
related_commands: ['pb-design-rules', 'pb-standards', 'pb-security', 'pb-review-product', 'pb-review-frontend']
last_reviewed: "2026-02-18"
last_evolved: "2026-02-18"
version: "1.1.0"
version_notes: "v2.13.1: Added pb-security backward reference (Calm Design includes secure-by-default principles)"
breaking_changes: []
---

# Calm Design: Attention-Respecting Features & Systems

**Technology should recede into the background until genuinely needed.** Calm design applies attention-efficiency principles to every feature, system, and interface you build.

**Resource Hint:** sonnet — Design and code review with attention as a resource lens.

## When to Use

- Before shipping a feature: Does this respect user attention?
- During code review: Is this feature calm or demanding?
- During design feedback: Would you use this daily without frustration?
- Planning notifications or alerts: Is this necessary or just noise?

---

## Philosophy: Attention as a Finite Resource

From Amber Case's *Calm Technology*: "Our world is made of information that competes for our attention." Most systems lose this lens and compete for attention constantly.

**Compare:**
- **Demanding system**: Notifications every 5 minutes, unclear alerts, requires constant vigilance
- **Calm system**: Works silently, alerts only when critical, provides status without demanding focus

**The shift**: Attention isn't infinite. Design systems that respect this.

See `/pb-design-rules` for clarity and simplicity principles. Calm design extends those: *the same clarity that makes code readable makes interfaces calm*.

---

## The 10-Question Calm Design Checklist

Use this to evaluate features, systems, or interfaces for attention-efficiency.

### Section A: Minimal Attention (User-Facing)

**1. Does this work without the user thinking about it?**

- Can the system operate automatically without constant user input?
- Or does it demand attention at every step?
- Example: Auto-save works silently ✅ vs. Manual save button everywhere ❌

**2. What happens during normal operation—silence or chatter?**

- Does the system only communicate when something's wrong?
- Or does it provide constant status updates?
- Example: Background sync with no status ✅ vs. Progress bar on every operation ❌

**3. Can secondary information move to the periphery?**

- Is all information front-and-center demanding focus?
- Or can less urgent info be subtle (icon, indicator, optional detail)?
- Example: Status dot shows sync complete ✅ vs. Modal dialog: "Sync complete! Click OK" ❌

**4. Have we eliminated notifications that aren't critical?**

- Which alerts are truly urgent vs. "nice to know"?
- Can "nice to know" be optional or on-demand?
- Example: Slack notification on mention only ✅ vs. Notification for every message ❌

### Section B: Graceful Degradation (System Failures)

**5. What happens when this system fails—alarm or adaptation?**

- Does failure break everything, or does the system gracefully degrade?
- Can users continue with partial functionality?
- Example: Form saves draft locally if network fails ✅ vs. "Error: Save failed" with no recovery ❌

**6. Do error messages explain the problem and path forward?**

- Error: "Database error" (user can't do anything with this)
- Better: "Your changes couldn't save. Retry or save as draft?" (clear action)
- Example: Clear, actionable errors ✅ vs. Technical jargon ❌

### Section C: Design Minimalism (Feature Scope)

**7. Have we stripped this to the minimum that solves the problem?**

- What's the smallest version that delivers value?
- Are we adding features "just in case"?
- Example: One clear action ✅ vs. Ten options for different use cases ❌

**8. Is the interface the least surprising thing users would expect?**

- Would a person using this for the first time know what to do?
- Or do they need to learn unique conventions?
- Example: Standard button labels and placement ✅ vs. Custom UI with novel interactions ❌

### Section D: Operational Calm (Behind the Scenes)

**9. Have we designed this to be maintainable and debuggable?**

- Can ops teams understand what the system is doing?
- Or is state hidden and behavior opaque?
- Example: Clear logs + metrics ✅ vs. Silent processing with no visibility ❌

**10. Does this scale peacefully, or will it demand constant babysitting?**

- Can this grow without frequent manual intervention?
- Or does growth require constant tuning and monitoring?
- Example: Self-tuning retry logic ✅ vs. Manual threshold adjustments ❌

---

## How to Use This Checklist

### During Design (Before Building)

- Read questions 1-4 (user-facing attention)
- Ask the team: "Which of these could fail?"
- Identify where calm design could prevent problems

### During Code Review

- Run through questions 5-6 (failure modes)
- Ask: "Does this fail quietly or loudly?"
- Calm doesn't mean no errors—it means kind errors

### Before Shipping

- Full checklist: all 10 questions
- Score: How many are you fully confident about?
- "7-10: Ship. 5-6: Address gaps. <5: Revisit design."

---

## Calm Tech Principles Applied

| Calm Tech Principle | In Practice | Link |
|-------------------|-------------|------|
| **Minimal Attention** | Does it work in the background? | Questions 1-2 |
| **Use the Periphery** | Can secondary info move to edges? | Question 3 |
| **Alternative Communication** | Not just alerts—use status, light, subtle indicators | Question 4 |
| **Graceful Failure** | Does it fail gently or catastrophically? | Questions 5-6 |
| **Minimum Viable Design** | Have we cut to the core? | Question 7 |
| **Least Surprise** | Would a first-time user understand? | Question 8 |
| **Observability** | Can ops see what's happening? | Questions 9-10 |

---

## Key Integration: Calm Tech + Design Rules

**Tension Example:**

Design Rules say: *Fail noisily and early* (Rule 10: Repair)
Calm Tech says: *Don't overwhelm users with alerts* (Alternative Communication)

**Resolution:**

- **In code/dev:** Fail noisily. Log everything. Crash on invariant violations. Engineers need to know.
- **In UX:** Fail calmly. Users get clear error + recovery path. No unnecessary alarms.

**Same principle, different layers:**
- Engineers need loud failures to catch bugs fast
- Users need calm failures with clear paths forward

---

## Examples: Calm vs. Demanding

### Example 1: Notification System

**Demanding:**
- Email notification for every action
- Slack alert for every mention
- In-app modal for every status change
- Result: User disables all notifications

**Calm:**
- Email digest once daily (15 items summarized)
- Slack only for mentions (@specific person)
- Status visible in sidebar (user checks when curious)
- Result: User stays informed without interruption

### Example 2: Form Validation

**Demanding:**
- Real-time validation with red underlines
- Shows every validation error before user finishes typing
- Modal alert if any field is invalid
- Result: User frustrated by constant feedback

**Calm:**
- Validation only on blur (after user finishes entering)
- Shows one clear error message per field
- Submit button disabled with explanation tooltip
- Result: User doesn't feel judged, knows what to fix

### Example 3: Background Sync

**Demanding:**
- Progress bar visible at all times
- Notification each time sync completes
- Modal dialog if sync fails
- User must click "OK" to continue

**Calm:**
- Small status dot: gray (idle), blue (syncing), green (complete)
- Optional toast notification (auto-dismisses)
- Syncs automatically; doesn't interrupt user
- If failure: saves draft locally, shows clear recovery option

### Example 4: API Rate Limiting

**Demanding:**
- 429 error with no explanation
- User has to guess they've exceeded a limit
- No indication of when they can retry

**Calm:**
- Error message: "Too many requests. Retry after 2 minutes."
- Client auto-retries with exponential backoff (silent)
- User doesn't notice the limit was hit
- System behaves patiently, not punitively

### Example 5: Configuration

**Demanding:**
- 50 configuration options on first launch
- Defaults that work for nobody
- User must configure before doing anything

**Calm:**
- Smart defaults (works for 80% of users)
- Advanced settings in collapsed section (user never sees them)
- Configuration optional, inline guidance
- User gets value immediately

---

## Mindset: Calm Design as Respect

Read `/pb-design-rules` for technical principles (clarity, simplicity, modularity).

**The mindset extension:** If you respect engineers through clarity and simplicity, respect users the same way.

- **Clarity to engineers**: "Here's what this code does"
- **Clarity to users**: "Here's what happens when you click this"
- **Simplicity for engineers**: "Minimal code, maximum understanding"
- **Simplicity for users**: "Minimal options, obvious action"
- **Respect for engineers**: "Your time is valuable; I made this readable"
- **Respect for users**: "Your attention is valuable; I made this calm"

---

## When NOT to Be Calm

Calm design doesn't mean hiding problems. Some systems NEED to be noisy:

**Be loud when:**
- **Safety is at risk** — Security breach, data loss, financial error: alert loudly
- **User explicitly asks** — User enabled notifications: notify them
- **Time is critical** — Deadline in 1 hour, meeting starting now: alert
- **User attention is already focused** — During an active operation (form submission, upload)

**Remain calm when:**
- **It's background work** — Sync, backup, index rebuild: silent
- **The user will notice anyway** — Feature works, they'll see it
- **It's optional or secondary** — Nice-to-know info: make it available, don't push it

---

## Checklist for Code Review

When reviewing code, ask:

- [ ] **Attention**: Does this demand user focus when it doesn't have to?
- [ ] **Failure**: If this breaks, does the user know what to do?
- [ ] **Scope**: Could we ship less and still deliver value?
- [ ] **Clarity**: Would a first-time user understand this?
- [ ] **Silence**: Does normal operation produce unnecessary output?
- [ ] **Observability**: Can we (ops) see what's happening?
- [ ] **Degradation**: Does this fail gracefully?

If you check all 7: Ship. If you check 5-6: Address gaps. If <5: Request redesign.

---

## Integration with Playbook

### Related to Design Rules

See `/pb-design-rules`:
- **Rule 1 (Clarity)**: Calm design is clarity extended to users
- **Rule 3 (Silence)**: "When there's nothing to say, say nothing"
- **Rule 5 (Simplicity)**: Minimum feature set respects user attention
- **Rule 8 (Composition)**: Systems work together without demanding attention

### Related to Standards

See `/pb-standards`:
- **Quality Bar (MLP)**: "Would you use this daily?" includes calm design
- **Test Standards**: Test that errors are clear and recoverable
- **Accessibility**: Keyboard-first and focus management are calm design

### Related to Security & Operations

See `/pb-security`, `/pb-observability`:
- Calm systems are more observable (clear logs, metrics)
- Calm failures are easier to debug (not hidden)
- Graceful degradation is more secure (no cascading failures)

---

## Checkpoint: Am I Building Calm?

Before shipping, ask yourself:

```
✅ This works in the background without demanding focus
✅ Error messages are clear; user knows what to do
✅ Failed gracefully; user can work around it
✅ I would use this daily without frustration
✅ Someone new could use this without training
```

If all 5: Calm. If 3-4: Good start; refine. If <3: Revisit design.

---

## Related Commands

- `/pb-design-rules` — Technical principles (clarity, simplicity, modularity)
- `/pb-standards` — Quality bar and MLP criteria
- `/pb-review-product` — Product-focused review including user experience
- `/pb-review-frontend` — Frontend review; applies calm principles to UI
- `/pb-a11y` — Accessibility review; overlaps with calm design

---

*Calm design: Features that work for users, not against them. Respect attention like you respect code clarity.*
