---
name: "pb-patterns-frontend"
title: "Frontend Architecture Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-design-language', 'pb-a11y', 'pb-patterns-async', 'pb-patterns-api', 'pb-testing']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 943 to 264 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Frontend Architecture Patterns

Patterns for building scalable, maintainable user interfaces. Mobile-first and theme-aware by default.

**Trade-offs exist:** Frontend complexity compounds quickly. Use `/pb-preamble` thinking (challenge the need for each abstraction) and `/pb-design-rules` thinking (Clarity in component boundaries, Simplicity in state management, Resilience through graceful degradation).

Question whether that library is necessary. Challenge whether that abstraction earns its complexity. Understand the constraints before adding patterns.

**Resource Hint:** sonnet - Frontend pattern reference; implementation-level UI architecture decisions.

## When to Use

- Designing component architecture for a new frontend project
- Choosing state management, styling, or rendering patterns
- Reviewing frontend code against scalability and maintainability principles

---

## Philosophy

### Mobile-First is Not Optional

**Mobile-first means:**
- Start with the smallest viewport, enhance upward
- Simplest layout is the default; complexity is opt-in
- Touch targets before hover states
- Performance budget starts tight, not loose

### Theme-Aware is Foundational

Design systems that support theming from day one:

Theme-awareness enables:
- Dark/light mode without refactoring
- Brand customization for white-label
- Accessibility adjustments (high contrast)
- Future design evolution

See `/pb-design-language` for project-specific token systems.

---

## Component Patterns

### Atomic Design (Component Hierarchy)

**Key insight:** Components at lower levels should know NOTHING about higher levels.

### Compound Components

**Compound components:**
- Share state via Context internally
- Expose flexible composition externally
- Self-document their structure

**Use when:** Component has multiple related parts (Tabs, Accordion, Dropdown, Modal)

### Container/Presentational Split

Separate data fetching from rendering:

**Modern evolution:** Hooks blur this line. The principle (separate concerns) still applies even if the boundary is within a single component.

---

## State Management

### State Location Decision Tree

```
Is this state used by only ONE component?
├─ Yes → Local state (useState)
└─ No → Is it used by SIBLINGS or PARENT?
    ├─ Yes → Lift state to common ancestor
    └─ No → Is it DEEPLY nested (prop drilling)?
        ├─ Yes → Context or state library
        └─ No → Is it SERVER state (fetched data)?
            ├─ Yes → Data fetching library (React Query, SWR)
            └─ No → Is it URL state (search, filters)?
                ├─ Yes → URL parameters
                └─ No → Global state library (if truly global)
```

### Server State vs Client State

**Server state:** Data from backend (users, products, orders)
- Use: React Query, SWR, Apollo
- Characteristics: Async, cacheable, can be stale

**Client state:** UI state (modals, selections, form inputs)
- Use: useState, useReducer, Context, Zustand
- Characteristics: Sync, ephemeral, always fresh

### URL State

**URL state candidates:**
- Search queries
- Filters and sorting
- Pagination
- Selected items (for sharing)
- Modal/drawer open state (debatable)

---

## UI States

Every component that fetches data or performs async operations needs three states: loading, error, and empty. Handle all three explicitly.

### Loading States

**Loading patterns:**
- **Skeletons:** Match content shape, use for initial load
- **Spinners:** Use for actions (button click, form submit)
- **Progress bars:** Use for known-duration operations (uploads)
- **Optimistic UI:** Show expected result immediately, rollback on error

### Error States

**Error patterns:**
- **Inline errors:** For form fields, local failures
- **Error cards:** For section-level failures with retry
- **Error boundaries:** For unexpected crashes (React)
- **Toast notifications:** For background operation failures

### Empty States

**Empty state types:**
- **First-use:** No data yet, guide user to create
- **No results:** Search/filter returned nothing, suggest clearing filters
- **Filtered empty:** Data exists but filter excludes all, show "clear filters"
- **Error empty:** Failed to load, show retry option

---

## Form Patterns

Forms are where users interact most. Get the patterns right for validation, layout, and multi-step flows.

### Validation Patterns

**Validation timing:**
- **On blur:** Most fields (email, password, text)
- **On change (debounced):** Async validation (username check)
- **On submit:** Final validation, scroll to first error

### Multi-Step Forms

**Multi-step principles:**
- Show progress (step 2 of 3)
- Allow going back without losing data
- Validate each step before proceeding
- Show summary before final submit
- Save progress for long forms (localStorage or server)

---

## Performance Patterns

### Code Splitting

**Split on:**
- Routes (always)
- Heavy libraries (charts, editors, maps)
- Below-the-fold content
- Conditionally rendered features

### Memoization (Use Sparingly)

**Memoize when:**
- Component is expensive to render
- Component receives same props often
- Profiler shows it's a bottleneck

**Don't memoize when:**
- "Just in case"
- Component is simple
- Props change frequently anyway

### Bundle Analysis

**Budget guidance:**
- Main bundle: < 200KB gzipped
- Initial JS: < 100KB for fast Time to Interactive
- Largest chunk: < 100KB (for good caching)

---

## Theming Patterns

### Skinnable Interfaces

For white-label or heavily customizable products:

See `/pb-design-language` for creating project-specific token systems.

---

## Responsive Patterns

### Fluid Typography

Scale typography smoothly between breakpoints:

**clamp() formula:** `clamp(min, preferred, max)`
- `min`: Smallest size (mobile floor)
- `preferred`: Fluid calculation based on viewport
- `max`: Largest size (desktop ceiling)

### Container Queries

Style based on container size, not viewport:

**Use for:** Components that exist in different contexts (sidebar vs main content).

---

## Accessibility Integration

Frontend patterns MUST be accessible by default. See `/pb-a11y` for comprehensive guidance.

**Quick checklist for components:**

- [ ] Semantic HTML used (button not div, etc.)
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Focus visible and logical
- [ ] ARIA only when semantic HTML insufficient
- [ ] Color not sole indicator
- [ ] Touch targets 44x44px minimum

---

## Related Commands

- `/pb-design-language` - Project-specific design token systems
- `/pb-a11y` - Accessibility deep-dive
- `/pb-patterns-async` - Data fetching patterns
- `/pb-patterns-api` - API design patterns
- `/pb-testing` - Component testing patterns

---

## Design Rules Applied

| Rule | Application |
|------|-------------|
| **Clarity** | Component boundaries are explicit; no hidden state |
| **Simplicity** | Mobile-first forces prioritization; no premature abstraction |
| **Composition** | Compound components, composition over props explosion |
| **Resilience** | Error boundaries, graceful degradation, loading states |
| **Extensibility** | Design tokens enable theming without code changes |
