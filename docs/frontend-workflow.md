# Frontend Development Workflow

Complete guide to frontend development using the Engineering Playbook. Covers the full lifecycle from design to deployment.

**Philosophy:** Mobile-first, theme-aware, accessible by default. Build the simple version first, then enhance.

---

## Quick Start

**New frontend project?**
```
/pb-repo-init → /pb-design-language → /pb-patterns-frontend → /pb-start
```

**Adding frontend feature?**
```
/pb-start → /pb-patterns-frontend → /pb-a11y → /pb-cycle → /pb-ship
```

**Frontend code review?**
```
/pb-cycle (self-review) → /pb-a11y checklist → /pb-review-cleanup
```

---

## The Frontend Command Stack

| Phase | Command | Purpose |
|-------|---------|---------|
| **Foundation** | `/pb-design-language` | Establish design tokens, vocabulary, constraints |
| **Architecture** | `/pb-patterns-frontend` | Component patterns, state management, performance |
| **Accessibility** | `/pb-a11y` | Semantic HTML, keyboard navigation, screen readers |
| **API Integration** | `/pb-patterns-api` | Backend communication patterns |
| **Development** | `/pb-cycle` | Iterate: code → self-review → test |
| **Quality** | `/pb-ship` | Full review workflow before merge |

---

## Phase 1: Foundation — Design Language

Before writing component code, establish the design language.

### New Projects

```
/pb-design-language
```

This command guides you through creating:
- **Design tokens** (colors, typography, spacing, motion)
- **Component vocabulary** (naming conventions)
- **Constraints** (what you don't do)
- **Asset requirements** (logos, icons, images)

**Output:** `docs/design-language.md` — living document that evolves with the project.

### Existing Projects

If joining an existing project:
1. Read existing `docs/design-language.md` (or equivalent)
2. Understand the token system
3. Follow established vocabulary

### Key Decisions at This Phase

| Decision | Options | Guidance |
|----------|---------|----------|
| CSS approach | CSS Modules, Tailwind, CSS-in-JS | Team familiarity, bundle size |
| Token format | CSS variables, Tailwind config, theme object | Framework alignment |
| Dark mode | CSS variables swap, class toggle, media query | User control preference |
| Icon system | SVG sprites, icon font, inline SVG | Bundle size, flexibility |

---

## Phase 2: Architecture — Component Patterns

Plan component structure before implementation.

```
/pb-patterns-frontend
```

### Key Decisions

**Component Organization:**
```
components/
├── atoms/          # Button, Input, Icon
├── molecules/      # SearchField, UserAvatar
├── organisms/      # Header, ProductCard
├── templates/      # PageLayout, DashboardLayout
└── pages/          # Actual route pages
```

**State Management:**
```
State type?
├─ Single component → useState
├─ Parent-child sharing → Lift state up
├─ Deep nesting → Context
├─ Server data → React Query / SWR
├─ Complex client state → Zustand / Redux
└─ URL state → useSearchParams
```

**Mobile-First Checklist:**
- [ ] Base styles are for mobile (smallest viewport)
- [ ] `min-width` media queries (not `max-width`)
- [ ] Touch targets 44x44px minimum
- [ ] Layouts work at 320px width

---

## Phase 3: Accessibility — Built In, Not Bolted On

Accessibility is part of development, not a separate phase.

```
/pb-a11y
```

### During Component Development

For EVERY component, verify:

- [ ] **Semantic HTML** — Using correct elements (`<button>`, `<nav>`, `<main>`)
- [ ] **Keyboard accessible** — Tab, Enter, Escape work
- [ ] **Focus visible** — Focus ring shows in all themes
- [ ] **Labels present** — All inputs have labels (visible or `aria-label`)
- [ ] **Alt text** — All informative images have alt text

### Quick Semantic HTML Reference

| Need | Use | Not |
|------|-----|-----|
| Clickable action | `<button>` | `<div onClick>` |
| Navigation link | `<a href>` | `<span onClick>` |
| Form field | `<input>` with `<label>` | Unlabeled input |
| Section heading | `<h1>`-`<h6>` in order | `<div class="heading">` |
| List of items | `<ul>` / `<ol>` | Multiple `<div>` |

### Testing Accessibility

**Manual (every feature):**
1. Tab through — logical order?
2. Enter/Space — activates buttons?
3. Escape — closes modals?
4. Screen reader — announces correctly?

**Automated (in CI):**
```bash
# axe-core in tests
npm install @axe-core/playwright
```

---

## Phase 4: API Integration

When frontend needs backend data.

```
/pb-patterns-api
```

### Data Fetching Pattern

```typescript
// Server state with React Query
const { data, isLoading, error } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

// Optimistic updates for mutations
const mutation = useMutation({
  mutationFn: updateUser,
  onMutate: async (newData) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries(['user', userId]);
    // Snapshot previous value
    const previous = queryClient.getQueryData(['user', userId]);
    // Optimistically update
    queryClient.setQueryData(['user', userId], newData);
    return { previous };
  },
  onError: (err, newData, context) => {
    // Rollback on error
    queryClient.setQueryData(['user', userId], context.previous);
  },
});
```

### Error Handling Pattern

```typescript
// Consistent error boundary
<ErrorBoundary fallback={<ErrorFallback />}>
  <Suspense fallback={<Loading />}>
    <UserProfile />
  </Suspense>
</ErrorBoundary>
```

---

## Phase 5: Development Iteration

The core development loop.

```
/pb-cycle
```

### Frontend Self-Review Checklist

Before requesting peer review:

**Functionality:**
- [ ] Feature works on mobile viewport
- [ ] Feature works on desktop viewport
- [ ] Feature works in light mode
- [ ] Feature works in dark mode
- [ ] Loading states handled
- [ ] Error states handled
- [ ] Empty states handled

**Accessibility:**
- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] Focus management correct (modals, drawers)
- [ ] Color contrast sufficient

**Performance:**
- [ ] No unnecessary re-renders (React DevTools)
- [ ] Images optimized
- [ ] Bundle size reasonable

**Code Quality:**
- [ ] Component is focused (single responsibility)
- [ ] Props are minimal and clear
- [ ] No hardcoded colors (use tokens)
- [ ] No hardcoded breakpoints (use tokens)

### Commit Pattern

```bash
# Component commits
feat(Button): add loading state variant
feat(Header): implement responsive navigation

# Style commits
style(tokens): add dark mode color variants
style(Button): adjust hover state for accessibility

# Accessibility commits
a11y(Modal): add focus trap and escape handling
a11y(Form): add aria-describedby for error messages
```

---

## Phase 6: Quality — Ship Workflow

When feature is code-complete.

```
/pb-ship
```

### Frontend-Specific Review Focus

**Phase 2 reviews for frontend:**

| Review | Frontend Focus |
|--------|---------------|
| `/pb-review-cleanup` | Component structure, prop design, dead code |
| `/pb-a11y` | Full accessibility checklist |
| `/pb-security` | XSS prevention, CSP compliance |
| `/pb-review-tests` | Component test coverage |

**Performance audit (add to Phase 2):**
```bash
# Bundle analysis
npm run build -- --analyze

# Lighthouse audit
npx lighthouse http://localhost:3000 --view
```

### Pre-Merge Checklist

- [ ] All self-review items verified
- [ ] Accessibility audit passed
- [ ] Cross-browser tested (Chrome, Firefox, Safari)
- [ ] Mobile tested (real device or emulator)
- [ ] Performance acceptable (bundle size, load time)
- [ ] No console errors or warnings

---

## Common Frontend Recipes

### Recipe: New Component

```
1. /pb-design-language
   └─ Check: Does vocabulary exist for this component?
   └─ If not: Define name, variants, states

2. /pb-patterns-frontend
   └─ Choose pattern: Atomic level, composition approach

3. Build component
   └─ Start mobile-first
   └─ Use design tokens
   └─ Add keyboard support

4. /pb-a11y checklist
   └─ Semantic HTML
   └─ ARIA if needed
   └─ Focus management

5. /pb-cycle
   └─ Self-review → Test → Commit
```

### Recipe: Design System Update

```
1. /pb-design-language
   └─ Update tokens or vocabulary
   └─ Document in decision log

2. /pb-adr (if significant)
   └─ Document alternatives, trade-offs

3. Update components
   └─ One component per commit

4. /pb-ship
   └─ Visual regression check
```

### Recipe: Accessibility Remediation

```
1. /pb-a11y
   └─ Audit existing component
   └─ Create issue list

2. /pb-start
   └─ Create a11y/component-name branch

3. Fix issues
   └─ One issue per commit
   └─ Test with screen reader

4. /pb-cycle → /pb-ship
```

---

## Tools Quick Reference

| Purpose | Tool |
|---------|------|
| Component dev | Storybook |
| Accessibility audit | axe DevTools, WAVE |
| Performance | Lighthouse, WebPageTest |
| Bundle analysis | webpack-bundle-analyzer, Vite bundle visualizer |
| Cross-browser | BrowserStack, Sauce Labs |
| Screen reader | VoiceOver (Mac), NVDA (Windows) |

---

## Related Commands

- `/pb-design-language` — Design token and vocabulary system
- `/pb-patterns-frontend` — Component and state patterns
- `/pb-a11y` — Accessibility deep-dive
- `/pb-patterns-api` — API integration patterns
- `/pb-debug` — Frontend debugging techniques
- `/pb-testing` — Component testing patterns

---

## Quick Decision Tree

```
What are you doing?

├─ Starting new frontend project
│   └─ /pb-design-language → /pb-patterns-frontend → /pb-start
│
├─ Building a component
│   └─ Check /pb-design-language → Build → /pb-a11y check → /pb-cycle
│
├─ Connecting to API
│   └─ /pb-patterns-api → /pb-patterns-frontend (state section)
│
├─ Reviewing frontend code
│   └─ /pb-a11y checklist → /pb-review-cleanup
│
├─ Fixing accessibility issue
│   └─ /pb-a11y → Fix → Test with screen reader
│
└─ Shipping frontend feature
    └─ /pb-ship (include /pb-a11y in Phase 2)
```

---

**Last Updated:** 2026-01-19
**Version:** 1.0
