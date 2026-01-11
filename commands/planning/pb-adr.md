# Architecture Decision Record (ADR)

Document significant architectural decisions to capture the context, alternatives considered, and rationale for future reference.

---

## When to Write an ADR

Write an ADR when:
- Choosing between multiple valid technical approaches
- Adopting a new technology, library, or pattern
- Making decisions that affect system architecture
- Changing existing architectural patterns
- Decisions that will be hard to reverse

Don't write an ADR for:
- Obvious implementation choices
- Temporary workarounds (document differently)
- Decisions that can easily be changed later

---

## ADR Template

Create ADR files at: `docs/adr/NNNN-title-with-dashes.md`

```markdown
# ADR-NNNN: [Title]

**Date:** YYYY-MM-DD
**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]
**Deciders:** [Names/roles involved]

## Context

[What is the issue we're addressing? What forces are at play?
Include technical constraints, business requirements, and team context.
Be specific about the problem, not the solution.]

## Decision

[What is the change we're proposing and/or doing?
State the decision clearly and directly.]

## Alternatives Considered

### Option A: [Name]
[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option B: [Name]
[Brief description]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

### Option C: [Name] (Selected)
[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]

## Rationale

[Why did we choose this option over the others?
What were the deciding factors?
What trade-offs are we accepting?]

## Consequences

**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative:**
- [Drawback 1]
- [Drawback 2]

**Neutral:**
- [Side effect that's neither good nor bad]

## Implementation Notes

[Any specific implementation guidance.
Things to watch out for.
Migration steps if applicable.]

## References

- [Link to relevant docs, issues, or discussions]
- [Related ADRs]
```

---

## ADR Numbering

Use sequential 4-digit numbers:
- `0001-initial-architecture.md`
- `0002-database-selection.md`
- `0003-authentication-strategy.md`

---

## Example ADR

```markdown
# ADR-0015: Self-Hosted Fonts Instead of Google Fonts

**Date:** 2026-01-04
**Status:** Accepted
**Deciders:** Engineering team

## Context

The application uses multiple custom fonts for different themes. Currently loading
from Google Fonts CDN, which introduces:
- External dependency and privacy concerns
- Render-blocking requests
- FOUT (Flash of Unstyled Text) on slow connections

Performance audits show font loading accounts for 400ms+ of blocking time.

## Decision

Self-host all fonts using @fontsource packages. Implement lazy loading for
theme-specific fonts.

## Alternatives Considered

### Option A: Keep Google Fonts
**Pros:** Zero maintenance, CDN caching
**Cons:** Privacy, render-blocking, external dependency

### Option B: Self-host with preload all
**Pros:** No external dependency, control over loading
**Cons:** Large initial payload, wasted bandwidth for unused themes

### Option C: Self-host with lazy loading (Selected)
**Pros:** Control over loading, minimal initial payload, load only what's needed
**Cons:** Slight complexity in implementation

## Rationale

Option C provides the best balance: eliminates external dependency while
minimizing payload through lazy loading of theme-specific fonts.

## Consequences

**Positive:**
- 87% reduction in render-blocking time
- No external dependencies
- Privacy-friendly (no Google tracking)

**Negative:**
- Slightly larger bundle (fonts in assets)
- Need to update fonts manually

## Implementation Notes

- Critical fonts (Inter, Noto Serif Devanagari) preloaded
- Theme fonts loaded on theme selection
- Font files in `/public/fonts/`
```

---

## ADR Lifecycle

```
Proposed → Accepted → [Active]
                   ↓
              Deprecated (no longer applies)
                   or
              Superseded (replaced by new ADR)
```

When superseding:
1. Create new ADR with updated decision
2. Update old ADR status to "Superseded by ADR-XXXX"
3. Reference old ADR in new ADR's context

---

## Directory Structure

```
docs/
└── adr/
    ├── 0001-initial-architecture.md
    ├── 0002-database-selection.md
    ├── 0003-authentication-strategy.md
    ├── ...
    └── README.md  # Index of all ADRs
```

### ADR Index Template

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-initial-architecture.md) | Initial Architecture | Accepted | 2025-01-01 |
| [0002](0002-database-selection.md) | PostgreSQL for Primary Database | Accepted | 2025-01-05 |
```

---

## Tips for Good ADRs

1. **Write in present tense** - "We decide" not "We decided"
2. **Be specific** - Vague context leads to vague decisions
3. **Include alternatives** - Shows you considered options
4. **State trade-offs** - No decision is perfect, acknowledge downsides
5. **Keep it concise** - 1-2 pages max
6. **Link to context** - Reference issues, PRs, discussions

---

*Decisions as code. Future you will thank present you.*
