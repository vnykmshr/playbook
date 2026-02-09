---
name: "pb-design-language"
title: "Project Design Language"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-patterns-frontend', 'pb-a11y', 'pb-adr', 'pb-repo-init', 'pb-documentation']
tags: ['design', 'testing', 'workflow', 'review', 'documentation']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Project Design Language

Create and evolve a project-specific design specification. A living document that captures the "why" of design decisions and grows with your project.

**This is NOT a generic style guide.** It's YOUR project's design language — the vocabulary, constraints, and decisions that make your interface coherent.

**Mindset:** Use `/pb-preamble` thinking to challenge aesthetic assumptions. Use `/pb-design-rules` thinking — especially Clarity (is the intent obvious?), Simplicity (are we over-designing?), and Representation (fold design knowledge into data/tokens).

**Resource Hint:** sonnet — Design language creation follows structured process; implementation-level guidance.

---

## What is a Design Language?

A design language is:
- **Vocabulary** — Names for components, patterns, and states
- **Constraints** — What we DON'T do (as important as what we do)
- **Tokens** — Design decisions encoded as variables
- **Rationale** — WHY we made these choices

A design language is NOT:
- A component library (that implements the language)
- A style guide (that describes the result)
- A Figma file (that's a different representation)

The design language is the **source of truth** that all artifacts derive from.

---

## When to Create One

**Start a design language when:**
- Beginning a new project (even a simple one)
- Inheriting a project with inconsistent UI
- Multiple developers touching the frontend
- Preparing for theming or white-labeling
- Design decisions keep being re-debated

**Keep it simple initially.** A 20-line design language is better than none.

---

## Bootstrap Template

Start here. Copy to `docs/design-language.md` or similar.

```markdown
# [Project Name] Design Language

**Version:** 0.1.0
**Last Updated:** YYYY-MM-DD

## Overview

[One paragraph: What is this project? What feeling should the UI evoke?]

---

## Users & Context

**Primary users:** [Who uses this most?]
**Secondary users:** [Who else uses this?]
**Context of use:** [Where/when/how do they use it?]

| User | Goal | Key Constraint |
|------|------|----------------|
| [User type] | [What they want] | [Device, time, ability] |

**Design implications:**
- [e.g., "Mobile-first because users are on-the-go"]
- [e.g., "High contrast because used in bright environments"]

---

## Voice & Tone

### Writing Principles

| Principle | Do | Don't |
|-----------|-----|-------|
| Clear | "Save changes" | "Persist modifications" |
| Helpful | "Enter your email to continue" | "Email required" |
| Human | "Something went wrong" | "Error 500" |
| Concise | "Delete" | "Click here to delete this item" |

### Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| Success | Encouraging | "You're all set!" |
| Error | Helpful, not blaming | "We couldn't save. Try again?" |
| Empty state | Guiding | "No projects yet. Create your first one." |
| Loading | Reassuring | "Loading your data..." |

### Terminology

| Use | Instead of |
|-----|------------|
| [Project term] | [Avoided term] |

---

## Principles

Our design follows these priorities (in order):

1. **[Principle 1]** — [Why it matters]
2. **[Principle 2]** — [Why it matters]
3. **[Principle 3]** — [Why it matters]

Example principles:
- Clarity over cleverness
- Mobile-first, always
- Accessible by default
- Fast perceived performance
- Minimal visual noise

---

## Color Tokens

### Semantic Colors

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--color-surface` | #ffffff | #1f2937 | Background surfaces |
| `--color-on-surface` | #1f2937 | #f9fafb | Text on surfaces |
| `--color-primary` | #3b82f6 | #60a5fa | Primary actions, links |
| `--color-on-primary` | #ffffff | #000000 | Text on primary |
| `--color-error` | #ef4444 | #f87171 | Error states |
| `--color-success` | #10b981 | #34d399 | Success states |

### Brand Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-brand` | #[hex] | Logo, key accents |
| `--color-brand-alt` | #[hex] | Secondary brand |

---

## Typography

### Font Stack

```css
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### Type Scale

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `--text-xs` | 0.75rem | 1rem | Captions, labels |
| `--text-sm` | 0.875rem | 1.25rem | Secondary text |
| `--text-base` | 1rem | 1.5rem | Body text |
| `--text-lg` | 1.125rem | 1.75rem | Subheadings |
| `--text-xl` | 1.25rem | 1.75rem | Section headings |
| `--text-2xl` | 1.5rem | 2rem | Page headings |

### Font Weights

| Token | Weight | Usage |
|-------|--------|-------|
| `--font-normal` | 400 | Body text |
| `--font-medium` | 500 | Emphasis, buttons |
| `--font-semibold` | 600 | Headings |
| `--font-bold` | 700 | Strong emphasis (rare) |

---

## Spacing

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 0.25rem | Tight gaps |
| `--space-2` | 0.5rem | Related elements |
| `--space-3` | 0.75rem | Form elements |
| `--space-4` | 1rem | Standard gaps |
| `--space-6` | 1.5rem | Section padding |
| `--space-8` | 2rem | Large gaps |
| `--space-12` | 3rem | Section separation |

### Layout Containers

| Token | Max Width | Usage |
|-------|-----------|-------|
| `--container-sm` | 640px | Forms, narrow content |
| `--container-md` | 768px | Article content |
| `--container-lg` | 1024px | Standard layouts |
| `--container-xl` | 1280px | Wide layouts |

---

## Motion

### Duration

| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` | 150ms | Micro-interactions |
| `--duration-normal` | 300ms | Standard transitions |
| `--duration-slow` | 500ms | Complex animations |

### Easing

| Token | Value | Usage |
|-------|-------|-------|
| `--ease-default` | cubic-bezier(0.4, 0, 0.2, 1) | General |
| `--ease-in` | cubic-bezier(0.4, 0, 1, 1) | Exit animations |
| `--ease-out` | cubic-bezier(0, 0, 0.2, 1) | Enter animations |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Component Vocabulary

### Naming Conventions

| Pattern | Name | NOT |
|---------|------|-----|
| Primary action button | Button (variant: primary) | CTAButton, MainButton |
| Container with padding | Card | Box, Panel, Container |
| Navigation list | Nav | Menu, Sidebar |
| Form input | Input (type: text/email/etc) | TextField, TextInput |
| User feedback | Toast | Notification, Alert, Snackbar |

### State Names

| State | Name | CSS Class |
|-------|------|-----------|
| Default | default | (none) |
| Focused | focus | .is-focused |
| Hovered | hover | .is-hovered |
| Active/Pressed | active | .is-active |
| Disabled | disabled | .is-disabled |
| Loading | loading | .is-loading |
| Error | error | .has-error |
| Success | success | .has-success |

---

## Constraints (What We Don't Do)

- No custom scrollbars
- No parallax effects
- No auto-playing video
- No animations > 500ms
- No font sizes below 14px (accessibility)
- No colors below 4.5:1 contrast ratio
- No hover-only interactions (mobile)
- [Add your constraints]

---

## Assets & Creatives

### Required Assets Checklist

- [ ] **Logo**: SVG format, both light and dark variants
- [ ] **Favicon**: Multiple sizes (16, 32, 180, 192, 512)
- [ ] **Open Graph image**: 1200x630px
- [ ] **App icons** (if applicable): iOS and Android sizes
- [ ] **Primary illustrations** (if used): Consistent style
- [ ] **Icon set**: Chosen library or custom set

### Asset Naming Convention

```
[type]-[name]-[variant].[ext]

logo-primary-light.svg
logo-primary-dark.svg
icon-search-24.svg
illustration-empty-state.svg
og-image-default.png
```

### Placeholder Strategy

During development, use:
- Placeholder.com for images: `https://via.placeholder.com/300x200`
- Heroicons or Lucide for icons (temporary)
- System fonts until brand fonts loaded

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| YYYY-MM-DD | Chose Inter as primary font | Open source, excellent legibility, variable font support |
| YYYY-MM-DD | 4px spacing base | Aligns with 8px grid when doubled |
| YYYY-MM-DD | No custom scrollbars | Cross-browser inconsistency, accessibility concerns |

---

## Evolution Protocol

When to update this document:

1. **Adding a new component** — Define its vocabulary first
2. **Changing a token** — Document why in decision log
3. **Adding a constraint** — Explain what problem it prevents
4. **Major version** — Review all sections for accuracy
```

---

## Evolution Protocol (Detailed)

### When to Update

**Mandatory updates:**
- New component type added to the system
- Color or typography change
- New constraint discovered
- Breaking change to existing pattern

**Optional updates:**
- New variant of existing component
- Performance optimization
- Documentation improvement

### How to Update

1. **Propose change** — Describe what and why
2. **Check constraints** — Does this violate existing rules?
3. **Update tokens** — If values change, update CSS variables
4. **Update decision log** — Document the rationale
5. **Increment version** — Patch for additions, minor for changes

### Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (renamed tokens, removed components)
MINOR: New features (new components, new tokens)
PATCH: Fixes and clarifications
```

---

## Requesting Assets & Creatives

When working with designers or creating assets yourself:

### Creative Brief Template

```markdown
## Asset Request: [Name]

**Type:** [Logo / Icon / Illustration / Photo / Animation]
**Purpose:** [Where and how it will be used]
**Dimensions:** [Required sizes]
**Format:** [SVG / PNG / WebP / etc.]
**Variants:** [Light/dark, sizes, states]

**Context:**
[Screenshot or description of where it appears]

**Constraints:**
- Must work on both light and dark backgrounds
- Must be recognizable at 16x16px (if icon)
- Must not use [specific colors/styles to avoid]

**Examples of similar:**
[Links to reference images]

**Deadline:** [Date needed]
```

### Self-Service Guidelines

If creating assets yourself:

**Icons:**
- Use existing icon library first (Heroicons, Lucide, Phosphor)
- Maintain consistent stroke width across custom icons
- Export at multiple sizes or use SVG

**Images:**
- Optimize with squoosh.app or similar
- Use WebP with PNG fallback
- Provide 2x versions for retina

**Illustrations:**
- Match existing illustration style (if any)
- Use brand colors from tokens
- Keep file size under 50KB

---

## Integration Points

### With Code

Design tokens should be:
1. Defined in CSS custom properties (source of truth)
2. Imported into Tailwind/other frameworks
3. Available in JavaScript for dynamic styling

```css
/* tokens.css - Source of truth */
:root {
  --color-primary: #3b82f6;
  /* ... */
}
```

```javascript
// tailwind.config.js - Consuming tokens
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
      },
    },
  },
};
```

### With Designers

**Principle: The design language document is the source of truth. Design tools derive from it, not vice versa.**

- Share the design language document, not just Figma
- Designers update Figma to match the document, not vice versa
- Export tokens to design tools; don't maintain separately
- Decision log prevents repeated debates
- When Figma and code disagree, the design language document decides

### With CI

Consider automated checks:
- Token usage validation (no hardcoded colors)
- Contrast ratio verification
- Unused token detection

---

## Starting a New Project

When initializing a project with `/pb-repo-init`:

1. Copy the bootstrap template to `docs/design-language.md`
2. Fill in project overview and principles
3. Define initial color tokens (even if just placeholder)
4. Check the assets checklist
5. Commit as initial design language

Then evolve as the project matures.

---

## Related Commands

- `/pb-patterns-frontend` — Implementation patterns using design tokens
- `/pb-a11y` — Accessibility requirements that constrain design
- `/pb-adr` — For significant design decisions
- `/pb-repo-init` — Bootstrap includes design language
- `/pb-documentation` — Documentation standards

---

## Design Rules Applied

| Rule | Application |
|------|-------------|
| **Clarity** | Explicit vocabulary prevents ambiguity |
| **Representation** | Fold design knowledge into tokens (data), not scattered CSS |
| **Simplicity** | Constraints prevent over-design |
| **Extensibility** | Tokens enable theming without code changes |
| **Transparency** | Decision log explains reasoning |

---

**Last Updated:** 2026-01-19
**Version:** 1.0
