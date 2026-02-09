---
name: "pb-a11y"
title: "Accessibility Deep-Dive"
category: "reviews"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-frontend', 'pb-design-language', 'pb-review-hygiene', 'pb-testing', 'pb-security']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Accessibility Deep-Dive

Comprehensive accessibility guidance for web applications. Semantic HTML first, ARIA as enhancement, keyboard-first interaction model.

**Accessibility is not optional.** It's not a feature. It's not "nice to have." It's a requirement for professional software.

**Mindset:** Use `/pb-preamble` thinking to challenge "works for me" assumptions. Use `/pb-design-rules` thinking — especially Clarity (is the interface obvious to ALL users?), Robustness (does it work with assistive technology?), and Repair (fail accessibly when things break).

**Resource Hint:** sonnet — accessibility audit follows structured WCAG checklists and component patterns

---

## When to Use

- Building new UI components or pages
- Pre-release accessibility compliance check
- After receiving accessibility-related bug reports or user feedback
- Periodic audit of existing web application

---

## Philosophy

### Semantic HTML First

ARIA is a repair tool, not a feature. If you need ARIA, ask first: "Can I use semantic HTML instead?"

```html
<!-- [NO] div with ARIA (repairing bad markup) -->
<div role="button" tabindex="0" aria-pressed="false" onclick="toggle()">
  Toggle
</div>

<!-- [YES] Semantic HTML (needs no repair) -->
<button type="button" aria-pressed="false" onclick="toggle()">
  Toggle
</button>
```

**The first rule of ARIA:** Don't use ARIA if you can use semantic HTML.

**The second rule of ARIA:** If you must use ARIA, use it correctly.

### Keyboard-First Interaction

Every interaction must work without a mouse:

- **Tab** navigates between focusable elements
- **Enter/Space** activates buttons and links
- **Arrow keys** navigate within widgets (tabs, menus, sliders)
- **Escape** closes modals and dismisses overlays
- **Focus** is always visible

If an interaction only works on hover or click, it's broken.

### Progressive Enhancement

Build the accessible version first, then enhance:

```html
<!-- Base: Works without JavaScript -->
<a href="/products">View Products</a>

<!-- Enhanced: Better UX with JavaScript -->
<a href="/products" onclick="openModal(event)">View Products</a>
```

If JavaScript fails, the link still works.

---

## Semantic Structure

### Document Landmarks

Use HTML5 landmarks for page structure:

```html
<body>
  <header role="banner">
    <!-- Site header, logo, primary nav -->
  </header>

  <nav role="navigation" aria-label="Main">
    <!-- Primary navigation -->
  </nav>

  <main role="main">
    <!-- Primary content -->
  </main>

  <aside role="complementary">
    <!-- Related content, sidebar -->
  </aside>

  <footer role="contentinfo">
    <!-- Site footer -->
  </footer>
</body>
```

**Note:** Modern browsers understand `<header>`, `<main>`, etc. The `role` attributes are for older assistive technology.

### Heading Hierarchy

Headings create an outline. Don't skip levels.

```html
<!-- [NO] Skipped levels, style-driven -->
<h1>Page Title</h1>
<h4>Section Title</h4>  <!-- Skipped h2, h3 -->
<h2>Another Section</h2>

<!-- [YES] Logical hierarchy -->
<h1>Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>
<h2>Another Section</h2>
```

**Use CSS for styling, headings for structure.**

### Lists

Use lists for groups of related items:

```html
<!-- Navigation is a list of links -->
<nav aria-label="Main">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Steps are an ordered list -->
<ol>
  <li>Add items to cart</li>
  <li>Enter shipping address</li>
  <li>Complete payment</li>
</ol>
```

Screen readers announce "list of 3 items" — helpful context.

### Tables

Use tables for tabular data, not layout:

```html
<table>
  <caption>Monthly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
      <td>+5%</td>
    </tr>
  </tbody>
</table>
```

- `<caption>` describes the table
- `scope="col"` and `scope="row"` associate headers with cells

---

## Interactive Elements

### Buttons vs Links

**Links** navigate to a new location:

```html
<!-- Goes somewhere -->
<a href="/products">View Products</a>
<a href="#section">Jump to Section</a>
```

**Buttons** perform an action:

```html
<!-- Does something -->
<button type="button" onclick="openModal()">Open Modal</button>
<button type="submit">Submit Form</button>
```

```html
<!-- [NO] Link that acts like a button -->
<a href="#" onclick="doSomething(); return false;">Do Something</a>

<!-- [YES] Button for actions -->
<button type="button" onclick="doSomething()">Do Something</button>
```

### Form Controls

Proper form markup:

```html
<form>
  <!-- Text input with visible label -->
  <div>
    <label for="email">Email address</label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-describedby="email-hint email-error"
    />
    <p id="email-hint">We'll never share your email.</p>
    <p id="email-error" role="alert" hidden>Please enter a valid email.</p>
  </div>

  <!-- Checkbox -->
  <div>
    <input type="checkbox" id="terms" name="terms" required />
    <label for="terms">I agree to the terms and conditions</label>
  </div>

  <!-- Radio group -->
  <fieldset>
    <legend>Preferred contact method</legend>
    <div>
      <input type="radio" id="contact-email" name="contact" value="email" />
      <label for="contact-email">Email</label>
    </div>
    <div>
      <input type="radio" id="contact-phone" name="contact" value="phone" />
      <label for="contact-phone">Phone</label>
    </div>
  </fieldset>

  <button type="submit">Subscribe</button>
</form>
```

**Key patterns:**
- Every input has a `<label>` with matching `for`/`id`
- Related inputs grouped in `<fieldset>` with `<legend>`
- Error messages linked via `aria-describedby`
- Errors announced via `role="alert"`

### Custom Widgets

When semantic HTML isn't enough, build accessible widgets:

**Tabs:**

```html
<div class="tabs">
  <div role="tablist" aria-label="Product information">
    <button
      role="tab"
      id="tab-1"
      aria-selected="true"
      aria-controls="panel-1"
    >
      Description
    </button>
    <button
      role="tab"
      id="tab-2"
      aria-selected="false"
      aria-controls="panel-2"
      tabindex="-1"
    >
      Reviews
    </button>
  </div>

  <div
    role="tabpanel"
    id="panel-1"
    aria-labelledby="tab-1"
  >
    <!-- Description content -->
  </div>

  <div
    role="tabpanel"
    id="panel-2"
    aria-labelledby="tab-2"
    hidden
  >
    <!-- Reviews content -->
  </div>
</div>
```

**Keyboard behavior:**
- Tab to tablist, then arrow keys between tabs
- Selected tab has `tabindex="0"`, others have `tabindex="-1"`
- Enter/Space activates tab

**Modal Dialog:**

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
>
  <h2 id="modal-title">Confirm Delete</h2>
  <p id="modal-desc">Are you sure you want to delete this item?</p>

  <div>
    <button type="button" onclick="closeModal()">Cancel</button>
    <button type="button" onclick="confirmDelete()">Delete</button>
  </div>
</div>
```

**Requirements:**
- Focus trapped inside modal while open
- Escape closes modal
- Focus returns to trigger element on close
- Background content has `aria-hidden="true"` and `inert`

---

## Focus Management

### Focus Order

Focus order should follow visual order (usually left-to-right, top-to-bottom in LTR languages).

```html
<!-- [NO] tabindex messing with order -->
<button tabindex="3">Third</button>
<button tabindex="1">First</button>
<button tabindex="2">Second</button>

<!-- [YES] Natural DOM order -->
<button>First</button>
<button>Second</button>
<button>Third</button>
```

**Only use tabindex:**
- `tabindex="0"` — Add to focus order (for custom focusable elements)
- `tabindex="-1"` — Remove from focus order (but focusable via JavaScript)

**Never use** `tabindex > 0`.

### Focus Visibility

Focus must ALWAYS be visible:

```css
/* [NO] Removing focus indicator */
*:focus {
  outline: none;
}

/* [YES] Custom focus indicator */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Works in both light and dark modes */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--color-surface);
}
```

### Focus Trapping

For modals and dialogs, trap focus inside:

```javascript
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === firstFocusable) {
        lastFocusable.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastFocusable) {
        firstFocusable.focus();
        e.preventDefault();
      }
    }
  });
}
```

### Skip Links

Allow keyboard users to skip repetitive navigation:

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header><!-- Navigation --></header>

  <main id="main-content" tabindex="-1">
    <!-- Main content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: var(--color-primary);
  color: var(--color-on-primary);
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

---

## Screen Reader Support

### Labels and Descriptions

Every interactive element needs a label:

```html
<!-- Visible label (preferred) -->
<label for="search">Search</label>
<input type="search" id="search" />

<!-- Hidden label (when visual label exists elsewhere) -->
<input type="search" aria-label="Search products" />

<!-- Icon-only button -->
<button type="button" aria-label="Close">
  <svg aria-hidden="true"><!-- X icon --></svg>
</button>

<!-- Additional description -->
<input
  type="password"
  aria-label="Password"
  aria-describedby="password-requirements"
/>
<p id="password-requirements">Must be at least 8 characters.</p>
```

### Live Regions

Announce dynamic content changes:

```html
<!-- Polite: Announced after current speech -->
<div aria-live="polite" aria-atomic="true">
  3 items in cart
</div>

<!-- Assertive: Interrupts current speech (use sparingly) -->
<div role="alert">
  Error: Payment failed. Please try again.
</div>

<!-- Status: For status messages -->
<div role="status">
  Saving...
</div>
```

### Hiding Content

**Hide from everyone:**

```html
<div hidden>Not rendered at all</div>
<div style="display: none;">Not rendered at all</div>
```

**Hide visually but keep accessible:**

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

```html
<button>
  <svg aria-hidden="true"><!-- icon --></svg>
  <span class="visually-hidden">Close menu</span>
</button>
```

**Hide from screen readers only:**

```html
<span aria-hidden="true">★★★☆☆</span>
<span class="visually-hidden">3 out of 5 stars</span>
```

---

## Standards

### WCAG 2.1 AA Baseline

This playbook targets **WCAG 2.1 Level AA** as the baseline. All guidance assumes AA compliance unless noted otherwise.

**Why 2.1 AA:**
- Industry standard for most organizations
- Legal requirement in many jurisdictions (ADA, Section 508, EN 301 549)
- Achievable without significant design constraints
- Covers vast majority of accessibility needs

**WCAG 2.2 Enhancements (Recommended):**

| Criterion | What | When to Implement |
|-----------|------|-------------------|
| 2.4.11 Focus Not Obscured | Focused element not hidden | New projects |
| 2.5.7 Dragging Movements | Alternative to drag operations | Touch interfaces |
| 2.5.8 Target Size (Minimum) | 24x24px targets | All projects |
| 3.2.6 Consistent Help | Help in consistent location | Complex apps |
| 3.3.7 Redundant Entry | Don't re-request same info | Multi-step forms |
| 3.3.8 Accessible Authentication | No cognitive tests for auth | All auth flows |

Implement 2.2 criteria in new projects. Retrofit existing projects during major updates.

---

## Color and Contrast

### WCAG Contrast Requirements

| Element | Ratio Required | Level |
|---------|---------------|-------|
| Normal text | 4.5:1 | AA |
| Large text (18px+ bold, 24px+) | 3:1 | AA |
| UI components, graphics | 3:1 | AA |
| Normal text | 7:1 | AAA |

**Tools:**
- WebAIM Contrast Checker
- Chrome DevTools (inspect > color picker shows ratio)
- Figma plugins (Stark, A11y)

### Color Not Sole Indicator

Don't rely on color alone:

```html
<!-- [NO] Only color indicates error -->
<input type="email" class="error" />  <!-- Red border -->

<!-- [YES] Color + icon + text -->
<input type="email" class="error" aria-invalid="true" aria-describedby="email-error" />
<p id="email-error">
  <svg aria-hidden="true"><!-- Error icon --></svg>
  Please enter a valid email address.
</p>
```

---

## Motion and Animation

### Reduced Motion

Respect user preference for reduced motion:

```css
/* Default: Animations enabled */
.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}

/* Reduced motion: Disable or minimize */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }

  .card:hover {
    transform: none;
  }
}
```

**In JavaScript:**

```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (!prefersReducedMotion) {
  // Run animation
}
```

### Safe Animation Guidelines

- No flashing more than 3 times per second
- Provide pause/stop controls for auto-playing content
- Keep animations under 5 seconds or provide controls
- Avoid animations that fill the entire screen

---

## Touch and Mobile

### Touch Target Size

Minimum 44x44 CSS pixels for touch targets:

```css
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 16px;
}

/* Icon buttons need explicit sizing */
.icon-button {
  width: 44px;
  height: 44px;
  padding: 10px;
}
```

### Spacing Between Targets

Leave at least 8px between touch targets:

```css
.button-group {
  display: flex;
  gap: 8px;  /* Minimum spacing */
}
```

---

## Testing

### Manual Testing Checklist

**Keyboard:**
- [ ] Can Tab through all interactive elements
- [ ] Tab order is logical (follows visual flow)
- [ ] Focus is always visible
- [ ] Can activate all buttons/links with Enter/Space
- [ ] Can close modals with Escape
- [ ] No keyboard traps (can always Tab out)

**Screen Reader:**
- [ ] All images have alt text (or are decorative and hidden)
- [ ] All form inputs have labels
- [ ] Headings create logical outline
- [ ] Links and buttons have descriptive text
- [ ] Dynamic changes are announced

**Visual:**
- [ ] Contrast ratios meet WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Color is not sole indicator
- [ ] Focus indicators visible in all themes
- [ ] Text resizable to 200% without loss

**Mobile:**
- [ ] Touch targets at least 44x44px
- [ ] Works in portrait and landscape
- [ ] No horizontal scrolling at 320px width

### Tiered Automated Testing

Layer accessibility checks at different stages of development:

| Tier | Tool | When | Catches |
|------|------|------|---------|
| Development | axe-core (React/browser) | During coding | Immediate feedback |
| Commit | axe-core (Playwright/Cypress) | Pre-commit/CI | Regressions |
| Quality Gate | Lighthouse CI | PR/merge | Performance + a11y score |
| Manual | WAVE, axe DevTools | Code review | Context-sensitive issues |
| Audit | pa11y-ci | Periodic | Site-wide compliance |

**Tier 1: Development (Immediate Feedback)**

```javascript
// React axe (dev only)
if (process.env.NODE_ENV === 'development') {
  import('@axe-core/react').then((axe) => {
    axe.default(React, ReactDOM, 1000);
  });
}
```

**Tier 2: Commit (CI Integration)**

```bash
# axe-core via playwright
npm install @axe-core/playwright
```

```typescript
// In test:
import AxeBuilder from '@axe-core/playwright';

test('page should be accessible', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

**Tier 3: Quality Gate (Lighthouse CI)**

```yaml
# lighthouserc.js
module.exports = {
  ci: {
    assert: {
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.9 }],
      },
    },
  },
};
```

```bash
# In CI pipeline
npx lhci autorun
```

**Tier 4: Manual Review**

Browser extensions for code review:
- axe DevTools — Comprehensive issue detection
- WAVE — Visual overlay of issues
- Accessibility Insights — Step-by-step assessment

**Tier 5: Periodic Audit (pa11y-ci)**

```bash
# .pa11yci.json
{
  "urls": ["/", "/products", "/checkout"],
  "standard": "WCAG2AA"
}

# Run audit
npx pa11y-ci
```

Use pa11y-ci for periodic site-wide audits, especially before major releases.

### Screen Reader Testing

Test with real screen readers:

| Platform | Screen Reader | Browser |
|----------|--------------|---------|
| macOS | VoiceOver | Safari |
| Windows | NVDA | Firefox |
| Windows | JAWS | Chrome |
| iOS | VoiceOver | Safari |
| Android | TalkBack | Chrome |

**At minimum:** Test with VoiceOver (macOS) or NVDA (Windows).

---

## Quick Reference by Component

### Button

```html
<button type="button" aria-pressed="false">
  Toggle Feature
</button>
```

- Use `<button>`, not `<div>` or `<a>`
- `type="button"` prevents form submission
- `aria-pressed` for toggle buttons
- Descriptive text (not "Click here")

### Link

```html
<a href="/products">View all products</a>
```

- Use `<a>` with `href`, not `<span onclick>`
- Descriptive text (not "Learn more")
- Opens new tab? Add `target="_blank" rel="noopener"` and indicate visually

### Image

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 20% in Q4" />

<!-- Decorative image -->
<img src="decoration.svg" alt="" role="presentation" />

<!-- Complex image with long description -->
<figure>
  <img src="complex-chart.png" alt="Annual revenue chart" aria-describedby="chart-desc" />
  <figcaption id="chart-desc">
    Revenue grew from $1M in 2020 to $5M in 2024, with the largest growth in 2023.
  </figcaption>
</figure>
```

### Input

```html
<div>
  <label for="username">Username</label>
  <input
    type="text"
    id="username"
    name="username"
    required
    aria-invalid="false"
    aria-describedby="username-hint"
  />
  <p id="username-hint">3-20 characters, letters and numbers only.</p>
</div>
```

### Modal

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Dialog Title</h2>
  <!-- Content -->
  <button type="button" onclick="closeModal()">Close</button>
</div>
```

- Focus trapped inside
- Escape closes
- Focus returns to trigger on close

---

## Related Commands

- `/pb-patterns-frontend` — Accessible component patterns
- `/pb-design-language` — Accessibility constraints in design tokens
- `/pb-review-hygiene` — Include accessibility in code review
- `/pb-testing` — Accessibility testing integration
- `/pb-security` — CSP and CORS (overlap with a11y testing tools)

---

## Design Rules Applied

| Rule | Application |
|------|-------------|
| **Clarity** | Semantic HTML makes intent obvious to all users |
| **Robustness** | Works with assistive technology, degrades gracefully |
| **Repair** | Error states are announced, not just visual |
| **Simplicity** | Native HTML before ARIA complexity |

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [Inclusive Components](https://inclusive-components.design/)

---

**Last Updated:** 2026-01-19
**Version:** 1.0
