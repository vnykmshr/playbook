---
name: "pb-usability"
title: "Webapp Usability Audit"
category: "reviews"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "parallel"
related_commands: ['pb-review-frontend', 'pb-a11y', 'pb-calm-design', 'pb-security', 'pb-performance']
last_reviewed: "2026-03-27"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial release: post-deploy usability audit orchestrator"
breaking_changes: []
---

# Webapp Usability Audit

Post-deploy audit of the live product from a user's perspective. Not a code review — a product audit. Run this against a staging URL or production site to surface usability gaps, trust issues, and readiness for AI-era expectations.

**Mindset:** Apply `/pb-preamble` thinking — challenge "works for me" assumptions by auditing as if you're a first-time visitor. Apply `/pb-design-rules` thinking — clarity (is it obvious?), simplicity (is it minimal?), resilience (does it recover?).

**Resource Hint:** opus - Multi-section audit requiring judgment across product, accessibility, trust, and technical dimensions.

---

## When to Use

- Before launching a new product or major feature
- Periodic health check on an existing product (quarterly)
- After redesign or migration to verify nothing regressed
- Evaluating a competitor or third-party product

---

## How This Works

This command orchestrates existing playbooks alongside its own native audit sections. Run the sections that matter for your context, or run all for a comprehensive audit.

```
pb-usability execution:

  ┌─ [native] First Impressions        ── Value prop, CTA, visual hierarchy
  ├─ [native] Navigation & Discovery    ── Consistency, search, mobile nav
  ├─ [native] Forms & Input UX          ── Errors, flexibility, preservation
  ├─ [native] Content & Readability     ── Scannability, microcopy, freshness
  ├─ [native] System Feedback           ── Loading states, error resilience
  │
  ├─ /pb-a11y                           ── Accessibility (keyboard, contrast, screen reader)
  ├─ /pb-calm-design Section E          ── Dark patterns, consent, engagement
  ├─ /pb-security Trust section         ── Privacy, cookies, trust indicators
  ├─ /pb-performance SEO section        ── Discoverability, LLM readiness
  │
  ├─ [native] AI Readiness              ── Agent access, decision appeals, transparency
  ├─ [native] User Rights               ── Deletion, cross-device, high-stakes friction
  │
  └─ Synthesis                          ── Severity tiers, unified report
```

---

## Quick Audit (15 minutes)

Top 15 highest-signal items. One from each concern. If any fail, run the full section.

| # | Check | Section |
|---|-------|---------|
| 1 | Can you tell what this site does in 5 seconds from the homepage? | First Impressions |
| 2 | Can you complete the top user task in 3 clicks or fewer? | Navigation |
| 3 | Do form errors explain what went wrong and how to fix it? | Forms |
| 4 | Does partially filling a form, navigating away, and returning preserve your input? | Forms |
| 5 | Can you scan-read any page and get the main points in 10 seconds? | Content |
| 6 | Are button labels, empty states, and confirmations written in user language (not system language)? | Content |
| 7 | Does every user action get immediate visible feedback? | System Feedback |
| 8 | Can every modal, flow, and overlay be dismissed or undone? | System Feedback |
| 9 | Can you navigate the entire site with only a keyboard? | Accessibility |
| 10 | Is the site free of dark patterns (hidden costs, confirmshaming, forced continuity)? | Ethical Calm |
| 11 | Is the privacy policy readable by a non-lawyer? | Trust |
| 12 | Do pages load in under 2.5 seconds (LCP)? | Performance |
| 13 | Can an AI agent navigate the DOM without executing complex JS? | AI Readiness |
| 14 | Can a user delete their account within 2 clicks of account settings? | User Rights |
| 15 | Are high-stakes actions (purchases, deletions) confirmed before execution? | User Rights |

**Scoring:** 13-15 pass: strong. 9-12: address gaps before launch. <9: significant usability debt.

---

## Comprehensive Audit

### Section 1: First Impressions

Audit the homepage and landing pages as a first-time visitor.

**1.1 Clear value proposition**
- View only above-the-fold content. Can you determine in under 5 seconds: what this site does, who it's for, and what the primary action is?
- If any are unclear, note exactly what's missing.

**1.2 Visual hierarchy**
- Identify the primary, secondary, and tertiary focal points. Are they correctly ordered by visual weight (size, contrast, color, position)?
- Flag competing elements that create visual noise or CTAs that are visually subordinate to less important content.

**1.3 Clear call to action**
- Identify every CTA on the homepage. Is there a clear primary CTA that dominates?
- Do labels communicate a benefit ("Start free trial") rather than a mechanic ("Submit")?
- Are there too many competing CTAs diluting focus?

**1.4 Above-the-fold content**
- On desktop (1440x900) and mobile (375x667): does the visible area contain site identity, headline, and primary CTA?
- Flag anything critical pushed below the fold or non-essential content displacing important content.

**1.5 Contact information visible**
- Can users find contact information (email, phone, chat, address) within two clicks from the homepage?
- Does the footer include basic contact details?

---

### Section 2: Navigation & Discovery

**2.1 Navigation consistency**
- Visit at least 5 different pages including homepage, a deep content page, and a transactional page.
- Primary navigation appears in the same position, uses identical labels, and indicates the current location on all pages.
- On mobile: navigation is reachable within one interaction.

**2.2 Search quality**
- Test with: an exact term, a misspelled version, a synonym, and a natural language query.
- Does search handle misspellings? Are results relevant? Does autocomplete aid discovery?
- Do zero-result pages offer helpful next steps?

**2.3 Mobile navigation**
- At 375px viewport: is the menu trigger clearly recognizable and tappable (minimum 48x48px)?
- Does the expanded menu work without layout conflicts? Are dropdowns accessible via tap (not hover)?
- Is there a visible way to close the menu?

**2.4 Content findability**
- Select the 5 most important user tasks. For each, count minimum clicks to reach the goal from the homepage.
- Flag any task requiring more than 3 interactions.
- Check for: breadcrumbs on interior pages, related content links, clear signposting.

**2.5 Descriptive links**
- Flag any links with generic text ("click here", "read more", "learn more") that don't describe their destination.
- All links should be visually distinguishable from non-link text.
- Links that open external sites or downloads should indicate this.

---

### Section 3: Forms & Input UX

**3.1 Helpful error messages**
- Deliberately trigger every possible validation error. For each: does it appear next to the relevant field?
- Does it explain what went wrong specifically ("Email must include @" not "Invalid input")?
- Does it use both color AND text/icon (not color alone)? Does focus move to the first error?

**3.2 Autofill support**
- Do name, email, phone, address, and payment fields have correct HTML `autocomplete` attributes?
- Is the correct `input type` used (`email`, `tel`, `url`) to trigger appropriate mobile keyboards?
- Are any fields blocking autofill with `autocomplete="off"` when they shouldn't?

**3.3 Required fields marked**
- Are required fields clearly indicated (asterisk, "required" label, or similar)?
- Is the marking convention explained? Can users identify required fields before interacting?

**3.4 Flexible input formats**
- Test every input expecting formatted data (phone, date, credit card, postal code) with different valid formats.
- Does the form accept variations? Strip or format automatically? Provide format hints?

**3.5 Progress preservation**
- Partially fill every multi-field form, navigate away, return. Is form data preserved?
- For multi-step forms: can users go back without losing data?
- After a failed submission: is previously valid input preserved?

**3.6 Long forms broken into steps**
- Identify every form with more than 6 fields. Is each broken into logical steps with a progress indicator?
- Are conditionally relevant fields hidden until triggered? Can users review entries before final submission?

---

### Section 4: Content & Readability

**4.1 Text is scannable**
- Are paragraphs short (3-4 sentences max)? Subheadings every 2-3 paragraphs?
- Key terms bolded? Lists used where appropriate?
- Line height at least 1.5x font size? Content width between 45-75 characters per line?

**4.2 Reading level is appropriate**
- Flag: sentences over 25 words, paragraphs over 4 lines, jargon without explanation, passive voice, double negatives.
- Can a general audience understand the main content without domain expertise?

**4.3 Microcopy is thoughtful**
- Audit button labels, form placeholders, tooltips, empty states, loading messages, success/error confirmations.
- Flag generic text ("Submit", "Error", "OK"), system language instead of user language, unhelpful empty states.

**4.4 Content is current**
- Identify: pages missing publication or last-updated dates, broken links (404s, wrong redirects), references to past events or expired promotions, outdated statistics.
- Copyright year in footer — is it current?

---

### Section 5: System Feedback

**5.1 Immediate feedback**
- Identify every user action (clicks, form submissions, loading states, transitions) that lacks immediate visible feedback.
- For each: recommend a specific feedback mechanism (spinner, progress bar, confirmation, animation).
- Flag any point where users might feel uncertain whether the system received their input.

**5.2 Undo, cancel, and escape**
- Map every multi-step flow, modal, overlay, and state change. For each: is there a clearly visible way to undo, cancel, go back, or dismiss?
- Test every destructive action (delete, unsubscribe, remove). Are they confirmed before execution? Can they be undone within a grace period?
- Flag any flow where the user could feel trapped — no back button, no cancel, no escape key support.

**5.3 Error resilience**
- Visit non-existent URLs: does the 404 page offer navigation, search, and helpful suggestions?
- Disable JavaScript: is critical content still accessible?
- Simulate a slow network: do loading states appear?
- Force an API failure: does the UI show a helpful error or break silently?

---

### Section 6: Delegated Audits

Run these existing playbooks as part of the comprehensive audit:

**Accessibility** — Run `/pb-a11y` or its manual testing checklist:
- Keyboard navigation, focus indicators, color contrast, alt text, heading hierarchy, screen reader experience, motion preferences

**Ethical Calm** — Run `/pb-calm-design` Section E:
- Dark patterns detection, meaningful consent, engagement well-being

**Trust & Privacy** — Run `/pb-security` User-Facing Trust section:
- Privacy policy readability, cookie audit, trust indicators, third-party disclosure, data proportionality, AI transparency

**Performance & Discoverability** — Run `/pb-performance` with SEO section:
- Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1), image optimization, JS audit, SEO meta tags, LLM discoverability

---

### Section 7: AI Readiness

Systems increasingly interact with AI agents on behalf of users. Audit whether the product is ready for this reality.

**7.1 Site works for AI agents**
- If a personal AI agent visited this site to perform a task (e.g., "buy the cheapest red toaster"), could it navigate the DOM without executing complex JS?
- Are buttons and form actions semantically labeled in HTML?
- Are key actions exposed via clear semantic HTML rather than hidden behind JavaScript event handlers?
- Flag agent-traps: non-standard captchas, invisible overlays, actions that require hover states to reveal.

**7.2 AI decisions can be appealed**
- Identify every place where AI makes or influences decisions: content moderation, dynamic pricing, eligibility, recommendations, search ranking, fraud detection, account restrictions.
- For each: is the user informed that AI is involved? Can they see why the decision was made?
- Is there a clear, accessible process to appeal to a human reviewer?

**7.3 Media transparency**
- Are any "photos" of products or people actually synthetic? If so, is this disclosed?
- Are user-generated sections (reviews, comments) verified as coming from real humans?
- Do images contain Content Credentials metadata identifying source and edit history?

**7.4 AI assistant quality** (if present)
- Does the chatbot or AI assistant auto-open and block content? Can users dismiss it permanently?
- Does it provide accurate, helpful responses? Does it clearly identify itself as AI?
- Can users reach a human? Does it respect conversation history? Can users delete chat history?

---

### Section 8: User Rights

**8.1 Account deletion is effortless**
- Attempt to delete an account. Is the option findable within 2 clicks of account settings?
- Can users export their data before deletion?
- Is the process instant, or does it require emailing support or calling a phone number?
- Compare the number of steps to sign up vs. delete. They should be comparable.

**8.2 Cross-device handoff works**
- Start a multi-step task on mobile (add items to cart, begin a form, start a chat). Switch to desktop on the same account.
- Check: cart contents, partially completed forms, chat history, reading position, saved preferences.
- List every piece of state that fails to sync.

**8.3 High-stakes actions have friction**
- Identify every high-consequence action: large transfers, permanent deletion, public posts, account changes, subscription commitments.
- Does the site provide enough positive friction to ensure the user isn't acting on impulse?
- Are there confirmations, cooling-off periods, or summary screens before irreversible actions?
- Flag any high-stakes action completable in a single click without review.

---

## Synthesis: Scoring & Report

After completing audit sections, synthesize findings into a severity-tiered report.

### Severity Tiers

| Tier | Definition | Action |
|------|-----------|--------|
| **Critical** | Users cannot complete core tasks, or are actively harmed (dark patterns, data leaks, trapped flows) | Fix before launch / immediately |
| **Major** | Significant friction on common tasks, accessibility failures, trust gaps | Fix within current cycle |
| **Minor** | Polish issues, edge cases, nice-to-haves | Backlog for next cycle |

### Report Template

```
# Usability Audit Report
**Site:** [URL]
**Date:** [Date]
**Auditor:** [Name/Team]
**Scope:** [Quick / Comprehensive / Specific sections]

## Summary
- Critical: [count]
- Major: [count]
- Minor: [count]

## Critical Findings
[List with section reference, specific issue, and recommended fix]

## Major Findings
[List with section reference, specific issue, and recommended fix]

## Minor Findings
[List with section reference, specific issue, and recommended fix]

## Strengths
[What the site does well — important for morale and context]

## Delegated Audit Results
- Accessibility (/pb-a11y): [summary]
- Ethical Calm (/pb-calm-design): [summary]
- Trust & Privacy (/pb-security): [summary]
- Performance (/pb-performance): [summary]
```

---

## Tips for Better Audits

- **Audit on a device you don't normally use.** Desktop person? Audit on mobile. Mobile person? Audit on desktop.
- **Clear cookies and cache first.** Experience the site as a new visitor.
- **Use incognito/private mode.** Removes personalization bias.
- **Test with real tasks, not abstract browsing.** "Buy the cheapest X" is better than "look around."
- **Include someone outside the team.** Fresh eyes catch what familiarity hides.

---

## Related Commands

- `/pb-review-frontend` — Code-level frontend review (Maya + Sam). Use during PR review.
- `/pb-a11y` — Deep accessibility audit. Delegated by this command.
- `/pb-calm-design` — Attention-respecting design including dark patterns. Delegated by this command.
- `/pb-security` — Security review including user-facing trust. Delegated by this command.
- `/pb-performance` — Performance optimization including SEO/LLM discoverability. Delegated by this command.

---

*Usability audit: Would a stranger trust this site, find what they need, and leave satisfied? If not, keep refining.*
