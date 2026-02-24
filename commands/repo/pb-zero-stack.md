---
name: "pb-zero-stack"
title: "Zero-Stack App Initiation ($0/month Architecture)"
category: "repo"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "interactive"
related_commands: ['pb-repo-init', 'pb-start', 'pb-patterns-cloud', 'pb-design-language', 'pb-calm-design']
last_reviewed: "2026-02-24"
last_evolved: "2026-02-24"
version: "3.0.0"
version_notes: "Expanded scope beyond read-heavy: user-content paths, complexity tiers, trust boundaries, CSP per-variant, UX states, implementation order with checkpoints, pre-ship checklist, agent guidance, persona awareness. Fixed contradictions (vanilla CSS/JS default). Preserved production lessons and calm design DNA."
breaking_changes: ["Scope expanded from read-heavy-only to all zero-cost topologies", "Default stack changed: vanilla CSS/JS default, Preact/Tailwind as options", "CSP delivery via meta tag (not Worker header)", "Data freshness mapping corrected", "Fit checklist replaced with broader data source taxonomy"]
---
# Zero-Stack App Initiation ($0/month Architecture)

A thinking tool for building **Gists** — small, calm apps that give you the essential point. You visit, get the gist, move on. Zero cost. Zero servers. Zero monthly bills.

A Gist is any app that fits the zero-stack topology: static site, optional edge proxy, CI pipeline. Two vendor accounts. The only fixed cost: domain registration (~$10-15/year) if you want a custom domain — the `*.pages.dev` default is free.

**What fits:** API dashboards, personal tools, form-based collectors, note-taking apps, display-only pages, data visualizers — anything that runs on static hosting with optional edge compute. Read-heavy, write-light, or user-content. The topology is the constraint, not the content type.

A structured conversation that takes an idea (or PRD) and walks through the product, data, design, and content decisions that produce a tailored project scaffold — not a generic template you fork and gut.

**Mindset:** Apply `/pb-preamble` thinking — challenge whether the idea fits this topology before committing to it. Apply `/pb-design-rules` thinking — the topology is simple by default, modular, and fails noisily. Apply `/pb-calm-design` thinking — Gists respect user attention by default.

**Resource Hint:** sonnet — scaffolding follows established patterns; architecture decisions are guided, not open-ended

---

## When to Use

- Building a small app that should cost $0/month to run
- API-backed dashboard or data display (public data, no auth)
- Personal tool — notes, trackers, calculators, generators
- Simple form submission (contact form, feedback widget, survey)
- Display-only content (portfolio, landing page, static info)
- Side project where production architecture shouldn't mean production ops burden
- Starting from an idea, not a template

## When NOT to Use

- Real-time collaboration or WebSocket-heavy — use `/pb-repo-init` + `/pb-patterns-async`
- Complex relational data or SQL queries — use `/pb-repo-init` + `/pb-patterns-db`
- OAuth flows, user accounts, or session management — use `/pb-repo-init`
- File uploads or media processing — use `/pb-repo-init`
- SSR required — this topology serves static files at the edge

If the idea doesn't fit, redirect early. Don't force the topology.

**Near-misses that still fit:** A contact form can POST to a Worker or external handler (Formspree, Netlify Forms). localStorage persistence works for personal tools. Optional auth via Cloudflare Access is fine for admin pages. Static data sources skip the proxy entirely. If the adaptation is small, proceed. If it reshapes the architecture, redirect.

---

## The Topology

Every zero-stack app has the same base shape. The complexity tier determines which pieces are active:

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│  Static Site │    │  Edge API Proxy   │    │  CI Pipeline │
│  (CF Pages)  │◄──►│  (CF Worker + KV) │    │  (GH Actions)│
└──────────────┘    └──────────────────┘    └──────────────┘
       │                     │                      │
       └─────────────────────┴──────────────────────┘
                    Two vendor accounts
                  (Cloudflare + GitHub)
```

This is what makes it a pattern, not a collection of choices. The topology is fixed. Choices within it are flexible. A Gist is any app that fits this topology.

### Complexity Tiers

Not every Gist needs every piece. The data source, update frequency, and scale determine the tier:

| Tier | When | What's Active | Framework |
|------|------|---------------|-----------|
| **Minimal** | No external data, personal use, display-only | Static site + CI only | Plain HTML/CSS/JS — no framework, no build tools |
| **Standard** | External API (keyless) or user-content with persistence | Static site + optional Worker | Astro (file-based routing, zero JS default) |
| **Full** | API with key, hourly+ freshness, or public scale | Static site + Worker + KV + cron | Astro + Workers + KV + GitHub Actions cron |

**The tier emerges from the conversation.** Don't ask "what tier do you want?" — determine it from the product decisions. Personal tool with no API? Minimal. Weather dashboard with public API? Standard. News aggregator with hourly updates? Full.

**Tier escalation signals:**
- API key required → needs Worker proxy (standard → full)
- Hourly or real-time freshness → needs cron + KV (full)
- Public scale with external data → needs Worker proxy (standard → full)
- Multi-page with routing → standard minimum (Astro file-based routing)
- User-saves-data with multi-user → standard minimum (needs storage backend)

### Calm by Default

The topology enforces calm design (see `/pb-calm-design`). These defaults are non-negotiable for a Gist:

- **Silence during normal operation** — data appears or shows a stale timestamp. No "refreshing..." banners. Live proxy path may have a brief initial load; use stale-first rendering (show cached data, update in place).
- **Stale over empty** — if the cache is old, show it with a timestamp. Never show an empty page when you have cached data.
- **Status in the periphery** — "Last updated 3 hours ago" in the footer, not a toast notification.
- **Works on first visit** — no onboarding, no configuration, no "sign up to see data."
- **Graceful offline** — PWA serves cached data with clear staleness indicator. No error walls.

### Trust Boundaries

Every Gist has clear trust boundaries. Name them explicitly in the scaffold:

| Boundary | Trust Level | Enforcement |
|----------|-------------|-------------|
| User input (forms, URL params) | Untrusted | Validate at entry, sanitize for display |
| External API responses | Semi-trusted | Validate shape before caching, sanitize before rendering |
| KV cache reads | Trusted (we wrote it) | Still validate shape (schema may have changed between deploys) |
| Worker ↔ Pages | Trusted (same origin) | CORS same-origin, no extra auth needed |
| sessionStorage/localStorage | Semi-trusted | Try-catch all access (private browsing, storage disabled) |

**DOM safety:** Never use `innerHTML` with dynamic content. Use `textContent` or DOM APIs (`createElement`, `setAttribute`). This is a hard rule, not a suggestion.

---

## Phase A: Shape (One Session)

Goal: idea to working local dev with mock data. No accounts needed.

### Step 1: Product Brief & Fit

Start with the product, not the technology. If the user has a PRD, extract these answers from it. If they have an idea, ask:

```
What are you building? (one sentence)
> ___

Who is this for?  (just me, friends/team, public?)
> ___

What's the headline value in 5 seconds?  (AQI is 42, next bus in 3 min, my notes organized)
> ___

Where does the data come from?
  □ External API (public, no key needed)
  □ External API (requires API key)
  □ User creates content (forms, notes, entries)
  □ Display-only (static content, portfolio, landing page)
  □ Mixed (API data + user input)
> ___

How often does the data change?  (real-time, hourly, daily, rarely, user-driven)
> ___

When do they come back?  (daily habit, event-driven, seasonal, one-time)
> ___
```

These answers — audience, headline value, data source, freshness, return pattern — drive every subsequent decision. Pin them before moving on.

**Data source taxonomy:**

| Data Source | Description | Typical Tier | Data Path |
|-------------|-------------|--------------|-----------|
| `public-api` | External API, no key | Standard | Browser fetches directly (CORS-friendly) |
| `keyed-api` | External API, key required | Full | Worker proxy hides key, caches in KV |
| `rss-feed` | RSS/Atom feed (news, blogs) | Standard | Fetch XML, parse to JSON at build or via Worker |
| `user-content:simple-form` | Contact form, feedback widget | Minimal–Standard | Form submits to handler (Formspree, Worker, etc.) |
| `user-content:user-saves-data` | Notes app, tracker, personal data | Standard | Client persistence (localStorage MVP, or database) |
| `user-content:display-only` | Portfolio, landing page, static info | Minimal | Content pre-loaded in HTML or fetched at build time |
| `mixed` | API data + user input | Standard–Full | Combination of above paths |

**Fit validation:**

Does this idea fit the zero-stack topology?

- **Fits cleanly:** Read-heavy, public data, no auth, low write frequency
- **Fits with adaptation:** Simple forms (POST to handler), personal storage (localStorage), optional admin auth (CF Access)
- **Doesn't fit:** User accounts, OAuth, file uploads, real-time collaboration, complex queries, SSR

If the adaptation is small, proceed. If it reshapes the architecture, redirect to `/pb-repo-init`.

**Persona awareness:**

Who is building this?

- **Developer** — comfortable with technical decisions, wants precise control
- **New builder** — may be using an AI coding assistant, needs jargon-free guidance

If new builder: the scaffold and spec should include reassuring hints. Technical sections are for the AI assistant; the builder needs to understand what their app will include without understanding every implementation detail.

### Step 2: Data Architecture

Now dig into the data source from Step 1. The path depends on which data source type was chosen.

#### Path A: External API (public-api or keyed-api)

- What API(s) are you pulling from?
- Free tier limits? (daily request cap, rate limits)
- Auth method? API key is fine. OAuth means this probably isn't zero-stack.
- Response format? (JSON, XML, RSS)

**Update frequency → data path mapping:**

| Freshness Need | Data Path | Implementation |
|---------------|-----------|----------------|
| Real-time (< 5 min) | Live Worker proxy | Worker fetches on request, caches in KV with short TTL |
| Hourly | Cron + KV | GitHub Actions cron writes to KV, Worker serves from KV |
| Daily | Cron + rebuild | GitHub Actions cron triggers Pages rebuild with data baked into HTML |
| Rarely / static | Build-time only | Data fetched at build, baked into static HTML |

**Active window:**

- Usage pattern: global (24h) or regional (e.g., 14h active window)?
- This drives budget math — fewer active hours = fewer API hits

#### Path B: User Content

- What does the user create? (form submissions, notes, entries, settings)
- Where does it persist?

| User Content Type | Persistence | Complexity |
|-------------------|-------------|------------|
| Simple form (contact, feedback) | External handler (Formspree, Netlify Forms) or Worker endpoint | Low — fire and forget |
| User saves data (personal) | localStorage (MVP) | Low — single user, client-side only |
| User saves data (multi-user) | Database (D1, Supabase, Firebase) | Medium — needs storage backend |
| Display-only | None — content in HTML | Lowest |

**For user-saves-data apps:** This adds real complexity. The user needs CRUD operations, data validation, empty states, and error handling. Surface this early:

> **Complexity note:** Apps where users create and save data require a storage backend, form validation, empty states, and error recovery. This is meaningfully more complex than a display-only or API-read app. Budget extra time for the data round-trip (create → read → update → delete).

#### Path C: Display-Only

- Content is pre-loaded in HTML or fetched at build time
- No runtime data fetching needed
- Simplest path — minimal tier

#### Path D: Mixed

- Combine paths as needed
- Each data source follows its own path above
- The most complex path determines the tier

### Step 3: UX States

Every Gist has states beyond "data loaded successfully." Define these early — they're product decisions, not afterthoughts.

**Core states (all Gists):**

| State | What the User Sees | Design Notes |
|-------|-------------------|--------------|
| **Loading** | Skeleton or spinner | Brief. If data is cached, show stale data immediately (stale-first rendering). |
| **Loaded** | The headline value from Step 1 | The normal state. This is what the app exists to show. |
| **Error (Network)** | Last known data + explanation | Never show a raw error. Show stale data with "Couldn't refresh — showing data from [timestamp]." |
| **Empty / First Use** | Clear call to action | For API apps: "Data loading..." then timeout message. For user-content: "No [items] yet — create your first one." |
| **Offline** | Cached data + staleness indicator | PWA shows cached version. "You're offline — showing data from [timestamp]." |

**Additional states by data source:**

| Data Source | Extra States |
|-------------|-------------|
| External API | **Error (API)** — upstream is down. Show stale data, not error wall. |
| User content (simple-form) | **Success** — form submitted confirmation. **Error (Submit)** — submission failed, keep form populated. |
| User content (user-saves-data) | **Empty / First Use** — no saved data, clear CTA. **Error (Storage)** — save failed, inline error with retry, never lose user input. |

Empty and error states are product decisions, not afterthoughts. A Gist that shows "Error fetching data" on first visit is a broken window.

### Step 4: Project Shape

**Basics:**

- Project name (lowercase, hyphenated)
- Single page or multi-page? (default: single for minimal, file-based routing for standard+)
- Primary display: dashboard, ticker, list, form, editor, map, or other?
- PWA with service worker? (default: yes for daily-use apps — offline shows stale data with timestamp)

**Design choices** (two decisions, not a design system):

| Choice | Options | Default |
|--------|---------|---------|
| Palette direction | warm / cool / mono | mono |
| Font vibe | system / geometric / humanist | system |

These produce a `design-tokens.css` in the scaffold. For deeper design work, run `/pb-design-language` after scaffolding.

**Web identity** (three decisions):

| Choice | Options | Default |
|--------|---------|---------|
| Site title | \[from project name\] | Capitalize project name |
| Description | \[one sentence from Step 1\] | Reuse headline value |
| Language | en / es / fr / ... | en |

These feed into `<title>`, `<meta name="description">`, `<html lang>`, manifest, and OG tags. Set once, used everywhere.

**Creative assets** (generate or provide):

| Asset | Format | Dimensions | Notes |
|-------|--------|------------|-------|
| Logo mark | SVG preferred | — | Simple mark, works at 16px. Used as favicon source |
| Favicon set | .ico + .svg + apple-touch-icon.png | 16/32/180/512 | Derive from logo SVG |
| OG image | PNG or JPG | 1200×630 | Social sharing preview. Static file or build-time generated |

Don't block on assets — the scaffold includes placeholders. Replace before go-live.

**Content decisions** (what goes on the page):

| Element | Source | Notes |
|---------|--------|-------|
| Headline metric/status | From data source | The 5-second answer from Step 1 |
| Supporting context | Derived or static | What explains the headline (trend, range, comparison) |
| Data attribution | Static | "Data from \[source\]" — users deserve to know the source |
| Freshness indicator | Cache timestamp | "Updated 2 hours ago" — peripheral, not prominent (calm default) |
| Empty state | Static copy | What shows before first data load or on first use |
| Error state | Static copy + stale data | Show last known data with explanation, not an error wall |
| Footer | Static + cache timestamp | Data attribution, freshness indicator, source link — calm design lives here |

### Step 5: Stack Confirmation

Show the default stack with rationale. The default adapts to the complexity tier.

**Minimal tier:**

| Layer | Default | Why |
|-------|---------|-----|
| Framework | None (plain HTML/CSS/JS) | No build tools, no dependencies, maximum simplicity |
| CSS | Vanilla CSS with custom properties | Design tokens in `:root`, responsive, dark mode via `prefers-color-scheme` |
| JS | Vanilla TypeScript (or JS) | No framework overhead for simple interactions |
| Host | CF Pages | Free, atomic deploys, edge network |
| CI | GitHub Actions | Lint + deploy on push |

> **Minimal means minimal.** No frameworks, no build tools, no server-side components. If you're reaching for a framework, you're probably standard tier.

**Standard tier:**

| Layer | Default | Why |
|-------|---------|-----|
| SSG | Astro | Islands architecture, zero JS by default, file-based routing |
| CSS | Vanilla CSS with custom properties | Design tokens in `:root`, responsive, dark mode via `prefers-color-scheme` |
| JS | Vanilla TypeScript in Astro components + `src/lib/` modules | No framework overhead unless islands are needed |
| Islands | Preact (optional) | 3KB, React-compatible API. Only add if you need client-side interactivity beyond what vanilla JS provides |
| Host | CF Pages | Free, atomic deploys, edge network |
| Proxy | CF Worker (if needed) | Same vendor as Pages, KV built-in |
| CI | GitHub Actions | Lint + type check + test + deploy |

**Full tier:**

| Layer | Default | Why |
|-------|---------|-----|
| SSG | Astro | Islands architecture, zero JS by default |
| CSS | Vanilla CSS with custom properties | Same as standard |
| JS | Vanilla TypeScript + Astro components | Same as standard |
| Islands | Preact (optional) | Same as standard |
| Host | CF Pages | Same vendor for hosting + proxy + cache |
| Proxy | CF Worker | API key hiding, response caching, health endpoint |
| Cache | CF KV | Global, free 100K reads/day |
| CI | GitHub Actions | Lint + test + deploy + cron for data refresh |

**Substitution notes:**

The default stack is chosen as a unit — single vendor for hosting means one API token, one dashboard, one set of docs.

| Substitution | Cascading Effect |
|-------------|------------------|
| Astro → Hugo | No JS islands, different template syntax, built-in sitemap |
| Astro → Vanilla HTML | No routing, no components, no build step. Fine for minimal tier. |
| Preact → Svelte | Different island syntax, slightly larger bundle |
| Preact → None | Vanilla JS for interactivity. Preferred unless you have complex reactive state. |
| Vanilla CSS → Tailwind v4 | Zero-config Vite plugin. Fine if team prefers. Not the default. |
| CF Pages → Vercel | Changes proxy (Vercel Edge), cache (Upstash), and deployment story |
| CF Pages → Netlify | Changes proxy, cache, and forms handling |

> Changing the host from CF Pages also changes the proxy, cache, and deployment story. That's fine if you're already on another platform — just know it's a package deal.

Confirm or adjust, then proceed.

### Step 6: Content Security Policy

Generate a CSP tailored to the data source and stack decisions. CSP is delivered via `<meta>` tag in the HTML `<head>` (not via Worker header — avoids coupling static site security to Worker availability).

**CSP per variant:**

| Data Source | `connect-src` | Notes |
|-------------|---------------|-------|
| No external data (minimal) | `'self'` | Tightest policy |
| External API via Worker proxy | `'self'` | Worker is same-origin |
| External API (keyless, direct) | `'self' https:` | Browser calls API directly |
| User content (simple-form) | `'self' https:` | May submit to external handler |
| User content (user-saves-data) | `'self' https:` | May call cloud database (Supabase, Firebase) |
| Display-only | `'self'` | No runtime fetching |

**Base policy (adapt per variant):**

```
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self';
connect-src [per variant above];
frame-ancestors 'none';
base-uri 'self';
form-action 'self' [add external handler domain if simple-form];
```

> If using an external form handler (Formspree, Netlify Forms), tighten `connect-src` and `form-action` to its specific domain rather than blanket `https:`.

> If using Cloudflare Web Analytics, add `static.cloudflareinsights.com` to `script-src` and `cloudflareinsights.com` to `connect-src`.

### Step 7: Implementation Order

Generate a step-by-step build order. The order matters — each step builds on the previous one. An AI coding assistant should be able to follow this top-to-bottom without jumping between sections.

**Base order (all tiers):**

```
1. Scaffold — project structure, config files, design tokens, base layout
   (Web standards files: robots.txt, sitemap, manifest, favicon — created here)
2. Mock data — hardcode representative data, build all UI states
   > Checkpoint: Show the user the UI with mock data. Get design approval before
   > connecting real data.
3. [Data connection step — varies by data source, see below]
   > Checkpoint: Confirm data flows correctly end-to-end before proceeding.
4. Polish — Lighthouse 90+, accessibility audit, mobile testing, verify all UX
   states work. Complete the Pre-Ship Checklist before declaring done.
```

**Data connection step by source:**

| Data Source | Step 3 |
|-------------|--------|
| External API (keyless) | **Connect API** — Wire fetch calls to real API endpoint, handle errors, implement stale-first rendering |
| External API (keyed) | **Deploy Worker proxy** — API key in Worker secrets, KV cache with TTL, health endpoint |
| User content (simple-form) | **Form handler** — Connect form to submission endpoint (Formspree, Netlify Forms, or Worker) |
| User content (user-saves-data) | **Storage backend** — Set up persistence (localStorage for MVP, or D1/Supabase/Firebase for multi-user). Define schema and read/write operations. Then: **Connect storage** — Wire forms to storage, confirm data round-trips (create → read → update → delete) |
| Display-only | No step 3 needed — content is already in HTML from step 2 |
| Mixed | Combine relevant steps above |

**Full tier additions** (insert between steps 2 and 3):

```
2.5. Worker proxy — deploy Worker with KV bindings, health endpoint
2.6. Cron job — GitHub Actions schedule, data fetch script, KV writes
```

**Agent guidance:**

> **For AI assistants:** Follow the Implementation Order step by step. If any requirement is ambiguous, ask the user — do not assume. Verify the design with the user after rendering mock data before connecting real data.

This guidance should be included in any spec or scaffold produced by this command. It prevents AI assistants from making assumptions about data formats, design preferences, or architecture decisions.

### Step 8: Scaffold

Generate project files with the decisions from Steps 1-7 baked in. The scaffold must work immediately with mock data — no Cloudflare account needed.

The structure below is representative — the actual scaffold adapts to the conversation. No `normalizer.ts` if the API has a stable schema. No `data-cron.yml` if the data path is live-only. No `worker/` directory if minimal tier. The command shapes the files, not the other way around.

**Standard tier structure (representative):**

```
project-name/
├── public/
│   ├── favicon.ico           # Placeholder, replace before go-live
│   ├── favicon.svg           # SVG favicon (modern browsers)
│   ├── apple-touch-icon.png  # 180×180 (iOS)
│   ├── og-image.png          # 1200×630 (social sharing)
│   ├── robots.txt            # Crawler directives
│   ├── humans.txt            # Attribution
│   ├── sw.js                 # Service worker (if PWA)
│   └── site.webmanifest      # PWA metadata
├── src/
│   ├── pages/                # Astro pages (index, 404, etc.)
│   ├── components/           # Astro components (.astro files)
│   ├── styles/
│   │   └── design-tokens.css # From Step 4 choices
│   └── lib/
│       ├── types.ts          # TypeScript types
│       └── api.ts            # Data fetching (uses mock in dev)
├── worker/                   # (standard/full tier only)
│   ├── src/
│   │   └── index.ts          # Edge proxy
│   └── wrangler.toml         # Worker config
├── .github/
│   └── workflows/
│       ├── ci.yml            # Lint + type check + test
│       ├── deploy.yml        # Pages + Worker deploy
│       └── data-cron.yml     # (full tier only, if cron path)
├── mock/
│   └── data.json             # Mock API response for local dev
├── package.json
├── tsconfig.json
├── CHANGELOG.md              # Keep a Changelog format from day one
└── README.md
```

**Minimal tier structure:**

```
project-name/
├── index.html
├── 404.html
├── styles/
│   └── main.css              # Design tokens + styles
├── scripts/
│   └── main.js               # Vanilla JS (if any)
├── public/
│   ├── favicon.ico
│   ├── favicon.svg
│   ├── og-image.png
│   ├── robots.txt
│   └── site.webmanifest
├── .github/
│   └── workflows/
│       └── deploy.yml
├── CHANGELOG.md
└── README.md
```

**Production lessons baked into the scaffold:**

- `wrangler.toml`: no `[env.dev.vars]` section — it causes interactive prompts in CI. Use `.dev.vars` file locally instead.
- `deploy.yml`: content-hash comparison to skip no-change deploys. Never deploy locally with dev config — CI is the only deploy path.
- `deploy.yml`: actions pinned to commit SHAs (supply chain security), not version tags.
- `worker/src/index.ts`: accepts both GET and HEAD requests. Uptime monitors send HEAD; returning 405 looks like downtime.
- `ci.yml` and `deploy.yml` are separate workflows. Push doesn't automatically deploy — release-gated deploys mean push != ship.
- `public/` directory includes go-live files (robots.txt, humans.txt, manifest, favicon placeholders). Replace creative asset placeholders before first deploy.
- Service worker: network-first for HTML pages (get latest deploy), cache-first for static assets (fonts, CSS, JS). Bump cache version on every release.
- sessionStorage/localStorage: always wrapped in try-catch (private browsing, storage disabled).

**First run:**

```bash
npm install && npm run dev    # Standard/full tier
# or just open index.html     # Minimal tier
```

Pages render with mock data. No Cloudflare account needed. Ready for real data integration after design approval.

---

## Go-Live Readiness (Phase A exit gate)

The scaffold produces correct HTML structure, meta tags, and discovery files from your decisions. This gate verifies you've customized the placeholders and confirms the Gist is ready for real visitors.

### Verify the scaffold got it right

The base layout should already include these from your choices. Confirm, don't re-implement:

- `<html lang="...">` matches your language choice
- `<title>` and `<meta name="description">` match your web identity
- `<meta name="theme-color">` matches your palette
- `<link rel="canonical">` points to your production URL
- CSP `<meta>` tag matches your variant from Step 6
- Semantic landmarks (`<header>`, `<main>`, `<footer>`) structure the page
- Skip-to-content link present for keyboard users
- One `<h1>` per page, proper heading hierarchy

### Replace creative asset placeholders

These are the placeholders the scaffold created. Replace all before first deploy:

- Logo mark (SVG) — the favicon and manifest icons derive from this
- Favicon set (ico + svg + apple-touch-icon) — derived from logo
- OG image (1200×630) — what people see when your URL is shared
- App icons for manifest (192×192 + 512×512 PNG)

### Verify social sharing

- `og:title`, `og:description`, `og:image`, `og:url` populated from web identity
- `twitter:card` set to `summary_large_image`
- Test with a social sharing debugger before announcing

### Verify discovery files

- **robots.txt** — allows crawling, references sitemap
- **sitemap.xml** — generated by framework (Astro: `@astrojs/sitemap`, Hugo: built-in) or static file
- **humans.txt** — project name, tech stack, last updated
- **site.webmanifest** — name, icons, theme_color, background_color from design choices

### Framework reference

| Concern | Astro | Hugo | Vanilla HTML |
|---------|-------|------|--------------|
| Sitemap | `@astrojs/sitemap` | Built-in | Static file |
| Meta tags | In layout `<head>` | In `baseof.html` | In `<head>` |
| 404 page | `src/pages/404.astro` | `layouts/404.html` | `404.html` |
| Manifest | `public/site.webmanifest` | `static/site.webmanifest` | `site.webmanifest` |
| Favicon | `public/` directory | `static/` directory | Root directory |
| Routing | File-based (`src/pages/`) | File-based (`content/`) | Manual links |

---

## Pre-Ship Checklist

Before declaring done, verify these. This is the exit gate for the Implementation Order's "Polish" step.

### Security (6 items)

- [ ] No secrets in frontend code (API keys in Worker secrets only)
- [ ] CSP meta tag present and correct for your variant
- [ ] No `innerHTML` with dynamic content (use `textContent` or DOM APIs)
- [ ] Form inputs validated at boundaries
- [ ] External data sanitized before rendering
- [ ] Dependencies audited (`npm audit`)

### Web Standards (verify scaffold produced these)

- [ ] `<html lang>` set correctly
- [ ] `<meta charset="utf-8">` present
- [ ] `<meta name="viewport">` present
- [ ] `<title>` and `<meta name="description">` set
- [ ] `<link rel="canonical">` points to production URL
- [ ] `<meta name="theme-color">` matches palette
- [ ] OG tags populated (title, description, image, url)
- [ ] Semantic HTML landmarks (header, main, footer)
- [ ] One `<h1>` per page, proper heading hierarchy
- [ ] Skip-to-content link present
- [ ] robots.txt, sitemap.xml, humans.txt, site.webmanifest present
- [ ] Favicon set (ico + svg + apple-touch-icon) replaced from placeholders
- [ ] OG image (1200×630) replaced from placeholder
- [ ] All images have `alt` text
- [ ] Touch targets 44px minimum
- [ ] WCAG AA contrast ratios met

### Accessibility

- [ ] Keyboard navigation works for all interactive elements
- [ ] Focus indicators visible
- [ ] `aria-label` or `aria-describedby` on controls without visible text
- [ ] `prefers-reduced-motion` respected (no animation for users who opt out)
- [ ] `prefers-color-scheme` dark mode works correctly

### Release Readiness

- [ ] Lighthouse score 90+ (Performance, Accessibility, Best Practices, SEO)
- [ ] All UX states verified (loading, loaded, error, empty, offline)
- [ ] Mobile tested (responsive, touch targets, no horizontal scroll)
- [ ] CHANGELOG.md created ([Keep a Changelog](https://keepachangelog.com/) format)

---

## Phase B: Deploy (When Ready)

Goal: scaffold to production. Human-paced, no rush.

### Step 9: Bootstrap Checklist

Generate `docs/setup.md` with paste-able commands. Each step is one command with expected output.

```markdown
## One-Time Setup (~30 minutes)

### 1. Cloudflare Account
- Sign up at dash.cloudflare.com (free plan)
- Install Wrangler: `npm install -g wrangler`
- Login: `wrangler login`
  Expected: browser opens, authorize, "Successfully logged in"

### 2. KV Namespace (standard/full tier only)
- Create: `wrangler kv namespace create "CACHE"`
  Expected: prints namespace ID
- Create preview: `wrangler kv namespace create "CACHE" --preview`
  Expected: prints preview namespace ID
- Update wrangler.toml with both IDs

### 3. API Secrets (if your data source needs an API key)
- Set secret: `wrangler secret put API_KEY`
  Expected: prompts for value, confirms "Success"
- Add to GitHub: repo Settings → Secrets → `CF_API_TOKEN`
  (Create token at dash.cloudflare.com/profile/api-tokens)

### 4. GitHub Actions
- Enable Actions in repo Settings → Actions → General
- Add secrets: `CF_API_TOKEN`, `CF_ACCOUNT_ID`

### 5. DNS (optional — skip for *.pages.dev default)
- Custom domain: Pages → Custom domains → Add
- CNAME subdomain (easy) or apex (needs registrar redirect)
```

### Step 10: First Deploy

```bash
git push origin main
```

CI runs. Pages deploy. Worker deploy (if applicable). Verify:

- Pages serve at `project-name.pages.dev`
- Worker proxies at `project-name.workers.dev/api/...` (if applicable)
- Cron runs on schedule (if applicable)
- `/health` returns 200 on both GET and HEAD (if Worker deployed)

### Post-Deployment

Verify after deploying, then establish ongoing practices:

- [ ] Live URL loads and core functionality works
- [ ] Analytics active (CF Web Analytics — free, built-in, privacy-first)
- [ ] Pin to API version if available — external APIs change without notice
- [ ] GitHub Actions cron runs successfully (if applicable) — failed crons mean stale data
- [ ] First release tagged with semver (`git tag -a v1.0.0 -m "Initial release"`)

---

## Budget Math

Calculate for the user during Step 2. This is the #1 failure mode — exceeding free tier limits.

### Formula

```
API hits/day = (active_hours * 60 / kv_ttl_minutes) + cron_runs
```

### Free tier headroom

| Resource | Free Tier | This App | Headroom |
|----------|-----------|----------|----------|
| Workers requests | 100K/day | [calculated] | [remaining] |
| KV reads | 100K/day | [calculated] | [remaining] |
| KV writes | 1K/day | [calculated] | [remaining] |
| KV storage | 1 GB | [estimated] | [remaining] |
| Pages builds | 500/month | [calculated] | [remaining] |
| GH Actions | 2K min/month | [calculated] | [remaining] |
| D1 rows (if user-saves-data) | 5M rows free | [estimated] | [remaining] |
| Supabase (if user-saves-data) | 500MB free | [estimated] | [remaining] |

> **Sharing a CF account across apps?** KV writes (1K/day) are shared across all apps on the account. Divide the limit by your app count.

### Free tier failure modes

Know what happens when you exceed limits:

| Resource | What Happens | Visibility |
|----------|-------------|------------|
| Workers requests (100K/day) | 1015 errors returned | Visible to users |
| KV reads (100K/day) | Errors returned | Visible to users |
| KV writes (1K/day) | 429 errors — **silent if you don't check put() response** | Invisible unless you check |
| Pages builds (500/month) | Builds queue and may time out | Visible in dashboard |
| GH Actions (2K min/month) | Workflows stop running | Visible in GitHub |

**Critical:** Always check KV write responses. If your Worker doesn't check the KV put response, stale data keeps being served and you won't know your cron updates stopped landing.

### Production cache lessons

- **Two-tier cache** (edge response cache + KV storage) prevents thundering herd across Cloudflare's 200+ PoPs. Set edge TTL shorter than KV TTL — edge serves stale while one PoP refreshes from KV.
- **Set `expirationTtl` on every KV put.** Without it, stale entries live forever if your cron stops or your key format changes.
- **Validate API response shape before caching.** If the upstream API changes its schema, you want to fail at write time, not serve corrupt cached data.
- **Cloudflare WAF rate limiting is a paid feature.** Don't investigate it — the built-in cache layers are sufficient for read-heavy patterns.

### Budget math for user-saves-data

If the app persists user data to a database, include database limits:

| Provider | Free Tier | Limit Type |
|----------|-----------|------------|
| Cloudflare D1 | 5M rows read, 100K rows written/day | Per day |
| Supabase | 500MB storage, 2GB bandwidth/month | Per month |
| Firebase (Firestore) | 50K reads, 20K writes/day | Per day |

---

## Observability

### Minimal / Standard tier (no Worker)

- Hosting provider analytics cover page views (CF Web Analytics: free, built-in, privacy-first)
- For funnel tracking (action → conversion), add custom events via `navigator.sendBeacon()` to an external endpoint
- Errors: `console.error()` with context. For production visibility, consider a free error tracker (Sentry free tier: 5K events/month)

### Full tier (with Worker)

All of the above, plus:

- **Health endpoint:** Add a `/health` route to your Worker returning `ok` (for uptime monitoring). Accept both GET and HEAD requests.
- **Worker analytics:** CF Workers dashboard shows request counts, errors, latency

---

## Stack Rationale (Reference)

Why these defaults as a unit:

**Cloudflare (Pages + Workers + KV):** Single vendor means one authentication flow, one dashboard, one billing page (free), and same-origin advantage between Pages and Workers. KV is globally replicated with no configuration.

**Astro (standard+ tier):** Islands architecture means zero JavaScript ships by default. Interactive components hydrate individually. Perfect for apps where most content is static. File-based routing eliminates manual route configuration.

**Vanilla CSS (all tiers):** Custom properties (`--color-primary`, `--space-md`) provide design tokens without build tooling. `prefers-color-scheme` handles dark mode. Mobile-first with minimal media queries. No Tailwind tax on bundle size or learning curve.

**Vanilla TypeScript (all tiers):** Strict mode, no `any`. Types in a single `types.ts` file. No framework runtime overhead for simple interactions. Astro components handle templating; vanilla TS handles logic.

**GitHub Actions:** Native cron for data refresh. Same platform as the repo. Free tier (2K minutes/month) is generous for CI + scheduled data fetches.

**The unit matters more than any piece.** Swapping one component is fine if you swap its dependencies too. The command warns about cascading changes in Step 5.

### Lightweight Libraries (when needed)

For minimal tier multi-page apps, consider:

- [tinyrouter.js](https://github.com/knadh/tinyrouter.js) (~950 B) — Frontend routing for multi-page navigation

For standard+ tier apps with external data that needs offline caching:

- [indexed-cache.js](https://oat.ink/other-libs/) — IndexedDB caching for offline-friendly data

> From [oat.ink/other-libs](https://oat.ink/other-libs/) — tiny, zero-dependency libraries. Only add if you genuinely need the capability.

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Force-fit an idea that needs auth/accounts | Redirect to `/pb-repo-init` in Step 1 |
| Skip budget math | Calculate it — free tier surprise is the #1 failure mode |
| Deploy before local dev works | Phase A must complete before Phase B |
| Use `[env.dev.vars]` in wrangler.toml | Use `.dev.vars` file (not committed) |
| Deploy from local machine | CI is the only deploy path |
| Set up CF account before writing code | Scaffold works with mocks — deploy when ready |
| Build a framework or CLI tool | This is a thinking tool that produces a scaffold |
| Ship with placeholder favicon and OG image | Replace before go-live — they're the first thing people see when sharing |
| Use `innerHTML` with dynamic content | Use `textContent` or DOM APIs — no exceptions |
| Skip the Pre-Ship Checklist | It's the exit gate. Complete it before declaring done. |
| Connect real data before design approval | Mock data first, get visual sign-off, then wire up real data |
| Assume the AI assistant knows your preferences | Be explicit in specs — design vibe, error copy, UX states |
| Default to Tailwind/Preact for simple apps | Start vanilla. Add tools when vanilla isn't enough. |
| Deliver CSP via Worker header | Use `<meta>` tag — decouples security from Worker availability |

---

## Related Commands

- `/pb-repo-init` — Generic greenfield initiation (when the Gist topology doesn't fit)
- `/pb-start` — Begin feature work after scaffolding
- `/pb-patterns-cloud` — Cloud deployment patterns reference
- `/pb-design-language` — Deeper design system work (optional, after scaffold)
- `/pb-calm-design` — Calm design principles (Gists embody these by default)
- `/pb-plan` — Focus area planning (for multi-phase work after scaffold)

---

*Opinionated about topology. Flexible about content. Calm by default. $0/month is a feature, not a constraint. The spec is the product — make it correct, coherent, and followable top-to-bottom.*
