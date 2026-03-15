---
name: "pb-zero-stack"
title: "Zero-Stack App Initiation ($0/month Architecture)"
category: "repo"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-repo-init', 'pb-start', 'pb-patterns-cloud', 'pb-design-language', 'pb-calm-design']
last_reviewed: "2026-02-25"
last_evolved: "2026-02-25"
version: "3.2.0"
version_notes: "Friction reduction pass: cut bloat from Step 4 (creative assets, web identity table, content decisions table), removed substitutions table, moved active window to Budget Math. Added missing dev-phase decisions: data transformation prompt, error copy prompt, loading skeleton nudge, responsive/dark-mode/animation/URL questions, validation rules, testing strategy, retry default."
breaking_changes: []
---
# Zero-Stack App Initiation ($0/month Architecture)

A thinking tool for building **Gists** - small, calm apps that give you the essential point. You visit, get the gist, move on. Zero cost. Zero servers. Zero monthly bills.

A Gist is any app that fits the zero-stack topology: static site, optional edge proxy, CI pipeline. Two vendor accounts. The only fixed cost: domain registration (~$10-15/year) if you want a custom domain - the `*.pages.dev` default is free.

**What fits:** API dashboards, personal tools, form-based collectors, note-taking apps, display-only pages, data visualizers - anything that runs on static hosting with optional edge compute. Read-heavy, write-light, or user-content. The topology is the constraint, not the content type.

> Not every Gist fits the "visit, get the point, leave" pattern - a personal notes app fits the topology but is a tool you return to. That's fine. "Gist" describes the deployment shape, not the interaction pattern.

A structured conversation that takes an idea (or PRD) and walks through the product, data, design, and content decisions that produce a tailored project scaffold - not a generic template you fork and gut.

**Mindset:** Apply `/pb-preamble` thinking - challenge whether the idea fits this topology before committing to it. Apply `/pb-design-rules` thinking - the topology is simple by default, modular, and fails noisily. Apply `/pb-calm-design` thinking - Gists respect user attention by default.

**Resource Hint:** opus - the conversation makes product architecture decisions (fit, tier, data paths, trust, CSP). Scaffold generation is pattern application.

---

## When to Use

- Building a small app that should cost $0/month to run
- API-backed dashboard or data display (public data, no auth)
- Personal tool - notes, trackers, calculators, generators
- Simple form submission (contact form, feedback widget, survey)
- Display-only content (portfolio, landing page, static info)
- Side project where production architecture shouldn't mean production ops burden
- Starting from an idea, not a template

## When NOT to Use

- Real-time collaboration or WebSocket-heavy - use `/pb-repo-init` + `/pb-patterns-async`
- Complex relational data or SQL queries - use `/pb-repo-init` + `/pb-patterns-db`
- OAuth flows, user accounts, or session management - use `/pb-repo-init`
- Dynamic file uploads from users or media processing - use `/pb-repo-init`
- SSR required - this topology serves static files at the edge

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
| **Minimal** | No external data, personal use, display-only | Static site + CI only | Plain HTML/CSS/JS - no framework, no build tools |
| **Standard** | External API (keyless) or user-content with persistence | Static site + optional Worker | Astro (file-based routing, zero JS default) |
| **Full** | API with key, hourly+ freshness, or public scale | Static site + Worker + KV + cron | Astro + Workers + KV + GitHub Actions cron |

**The tier emerges from the conversation.** Don't ask "what tier do you want?" - determine it from the product decisions. Personal tool with no API? Minimal. Weather dashboard with public API? Standard. News aggregator with hourly updates? Full.

**Tier escalation signals:**
- API key required → needs Worker proxy (standard → full)
- Hourly or real-time freshness → needs cron + KV (full)
- Public scale with external data → needs Worker proxy (standard → full)
- Multi-page with routing → standard minimum (Astro file-based routing)
- User-saves-data with multi-user → standard minimum (needs storage backend)

### Calm by Default

The topology enforces calm design (see `/pb-calm-design`). Non-negotiable defaults:

- **Silence during normal operation** - data appears or shows a stale timestamp. No "refreshing..." banners. Live proxy path: stale-first rendering (show cached, update in place).
- **Stale over empty** - if the cache is old, show it with a timestamp. Never show an empty page when you have cached data.
- **Status in the periphery** - "Last updated 3 hours ago" in the footer, not a toast notification.
- **Works on first visit** - no onboarding, no configuration, no "sign up to see data."
- **Graceful offline** - PWA serves cached data with clear staleness indicator. No error walls.
- **Transitions are opt-in** - if used: subtle (150-200ms), functional (communicates state change), and disabled under `prefers-reduced-motion`.

### Trust Boundaries

Every Gist has clear trust boundaries. Name them explicitly in the scaffold:

| Boundary | Trust Level | Enforcement |
|----------|-------------|-------------|
| User input (forms, URL params) | Untrusted | Validate at entry, sanitize for display |
| External API responses | Semi-trusted | Validate shape before caching, sanitize before rendering |
| KV cache reads | Trusted (we wrote it) | Still validate shape (schema may have changed between deploys) |
| Worker ↔ Pages | Trusted (same origin) | CORS same-origin, no extra auth needed |
| sessionStorage/localStorage | Semi-trusted | Try-catch all access (private browsing, storage disabled) |

**DOM safety:** Never use `innerHTML` with dynamic content. Use `textContent` or DOM APIs (`createElement`, `setAttribute`). Hard rule - referenced in Ship Gate and Anti-Patterns.

---

## Phase A: Shape (One Session)

Goal: idea to working local dev with mock data. No accounts needed.

**Persona hint:** If the builder is new to development (using an AI coding assistant), keep product sections jargon-free. Technical detail lives in the scaffold spec where the assistant consumes it. Thread this awareness through each step - the builder needs to understand *what* their app will include; the assistant handles *how*.

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

These answers - audience, headline value, data source, freshness, return pattern - drive every subsequent decision. Pin them before moving on.

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

**Data transformation:** Does the raw API response need shaping before display? Identify: which fields you display, what you rename, what you derive (e.g., AQI category from numeric value). Pin the types now - they go into `types.ts` and prevent the assistant from guessing the data shape.

**On API failure:** Default: serve stale data, no automatic client retry. If the Worker proxy is involved, it serves from KV cache on upstream failure. Surface this decision now - different retry strategies produce different user experiences.

#### Path B: User Content

- What does the user create? (form submissions, notes, entries, settings)
- Where does it persist?

| User Content Type | Persistence | Complexity |
|-------------------|-------------|------------|
| Simple form (contact, feedback) | External handler (Formspree, Netlify Forms) or Worker endpoint | Low - fire and forget |
| User saves data (personal) | localStorage (MVP) | Low - single user, client-side only |
| User saves data (multi-user) | Database (D1, Supabase, Firebase) | Medium - needs storage backend |
| Display-only | None - content in HTML | Lowest |

**For user-saves-data apps:** Surface complexity early - CRUD operations, data validation, empty states, and error recovery are meaningfully more work than read-only apps. Budget extra time for the data round-trip.

**Validation rules:** Define per field - required, type, limits. Validation fires inline on blur for required fields, on submit for the rest (default). Pin these now; the assistant will implement whatever the spec says, and changing validation UX mid-build is expensive.

#### Path C: Display-Only

Content is pre-loaded in HTML or fetched at build time. No runtime data fetching. Simplest path - minimal tier.

#### Path D: Mixed

Combine paths as needed. Each data source follows its own path above. The most complex path determines the tier.

### Step 3: UX States

Every Gist has states beyond "data loaded successfully." Define these early - they're product decisions, not afterthoughts.

**Core states (all Gists):**

| State | What the User Sees | Design Notes |
|-------|-------------------|--------------|
| **Loading** | Skeleton placeholder matching layout shape | Prefer skeletons over spinners - they preview the loaded layout. Describe the shape (e.g., "three cards with pulsing blocks"). Spinners only for brief operations (< 1s). |
| **Loaded** | The headline value from Step 1 | The normal state. This is what the app exists to show. |
| **Error (Network)** | Last known data + explanation | Show stale data with "Couldn't refresh - showing data from [timestamp]." |
| **Empty / First Use** | Clear call to action | API apps: timeout message. User-content: "No [items] yet - create your first one." |
| **Offline** | Cached data + staleness indicator | PWA shows cached version with timestamp. |

**Additional states by data source:**

| Data Source | Extra States |
|-------------|-------------|
| External API | **Error (API)** - upstream is down. Show stale data, not error wall. |
| User content (simple-form) | **Success** - confirmation. **Error (Submit)** - keep form populated. |
| User content (user-saves-data) | **Empty / First Use** - clear CTA. **Error (Storage)** - inline error with retry, never lose user input. |

**Draft the actual copy now.** Write the 3-5 strings users will see: network error message, API/upstream error, empty state CTA, form success (if applicable), form error (if applicable). Keep it calm - the user doesn't need to know what broke, just what they're seeing and how fresh it is. Deciding copy now saves 2-3 rounds of "make it friendlier" during development.

### Step 4: Project Shape

**Basics:**

- Project name (lowercase, hyphenated)
- Single page or multi-page? (default: single for minimal, file-based routing for standard+)
- Primary display: dashboard, ticker, list, form, editor, map, or other?
- PWA with service worker? (default: yes for daily-use apps)
- URL state: can users share a link to a specific view or filter? (default: no for single-page, query params for filtered views)

**Design choices:**

| Choice | Options | Default |
|--------|---------|---------|
| Palette direction | warm / cool / mono | mono |
| Font vibe | system / geometric / humanist | system |
| Dark mode | system-preference / toggle / light-only | system-preference (auto-derived dark palette) |
| Responsive priority | mobile-first / desktop-first | mobile-first single-column stack; responsive grid for standard+ |

These produce a `design-tokens.css` (including dark mode variants) in the scaffold. For deeper design work, run `/pb-design-language` after scaffolding.

**Web identity:** Site title (from project name), description (reuse headline value from Step 1), language (default: en). These feed into `<title>`, `<meta description>`, `<html lang>`, manifest, and OG tags. Override if needed.

### Step 5: Stack Confirmation

Show the default stack with rationale. The default adapts to the complexity tier.

**Why these defaults as a unit:** Single vendor (Cloudflare) means one auth flow, one dashboard, one billing page. Astro ships zero JS by default. Vanilla CSS with custom properties provides design tokens without build tooling. GitHub Actions gives native cron on the same platform as the repo.

**Minimal tier:**

| Layer | Default | Why |
|-------|---------|-----|
| Framework | None (plain HTML/CSS/JS) | No build tools, no dependencies, maximum simplicity |
| CSS | Vanilla CSS with custom properties | Design tokens in `:root`, responsive, dark mode via `prefers-color-scheme` |
| JS | Vanilla TypeScript (or JS) | No framework overhead for simple interactions |
| Host | CF Pages | Free, atomic deploys, edge network |
| CI | GitHub Actions | Lint + deploy on push |

> **Minimal means minimal.** No frameworks, no build tools. If you're reaching for a framework, you're probably standard tier.

**Standard tier:**

| Layer | Default | Why |
|-------|---------|-----|
| SSG | Astro | Islands architecture, zero JS default, file-based routing |
| CSS | Vanilla CSS with custom properties | Same pattern, same tokens |
| JS | Vanilla TypeScript in Astro components + `src/lib/` modules | No framework overhead unless islands needed |
| Islands | Preact (optional, 3KB) | Only add for client-side interactivity beyond vanilla JS |
| Host | CF Pages | Free, atomic deploys, edge network |
| Proxy | CF Worker (if needed) | Same vendor as Pages, KV built-in |
| CI | GitHub Actions | Lint + type check + test + deploy |

**Full tier:**

| Layer | Default | Why |
|-------|---------|-----|
| SSG | Astro | Islands architecture, zero JS default |
| Host | CF Pages | Same vendor for hosting + proxy + cache |
| Proxy | CF Worker | API key hiding, response caching, health endpoint |
| Cache | CF KV | Global, free 100K reads/day |
| CI | GitHub Actions | Lint + test + deploy + cron for data refresh |

> Full tier uses the same CSS/JS/Islands defaults as standard. The additions are Worker, KV, and cron.
> **Substitutions:** The stack is chosen as a unit. Swapping one piece (e.g., CF Pages → Vercel) changes the proxy, cache, and deployment story - it's a package deal. If you need different defaults, say so now; the scaffold adapts.

Confirm or adjust, then proceed.

### Step 6: Content Security Policy

Generate a CSP tailored to the data source and stack. Delivered via `<meta>` tag in HTML `<head>` (not Worker header - decouples security from Worker availability).

**CSP per variant:**

| Data Source | `connect-src` |
|-------------|---------------|
| No external data (minimal) | `'self'` |
| External API via Worker proxy | `'self'` (Worker is same-origin) |
| External API (keyless, direct) | `'self' https:` |
| User content / display-only | `'self'` or `'self' https:` (depends on external handlers) |

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
form-action 'self' [add external handler domain if needed];
```

> Tighten `connect-src` and `form-action` to specific domains rather than blanket `https:` when possible. Add analytics domains (e.g., `cloudflareinsights.com`) if using CF Web Analytics.

### Step 7: Implementation Order

Generate a step-by-step build order. Each step builds on the previous. An AI coding assistant should follow this top-to-bottom without jumping between sections.

**Base order (all tiers):**

```
1. Scaffold - project structure, config files, design tokens, base layout, web standards files
2. Mock data - hardcode representative data, build all UI states
   > Checkpoint: Show the user the UI with mock data. Get design approval before
   > connecting real data.
3. [Data connection step - varies by data source, see below]
   > Checkpoint: Confirm data flows correctly end-to-end before proceeding.
4. Polish - Lighthouse 90+, accessibility audit, mobile testing, verify all UX states.
   Complete the Ship Gate before declaring done.
```

**Data connection step by source:**

| Data Source | Step 3 |
|-------------|--------|
| External API (keyless) | **Connect API** - Wire fetch calls, handle errors, implement stale-first rendering |
| External API (keyed) | **Deploy Worker proxy** - API key in Worker secrets, KV cache with TTL, health endpoint |
| User content (simple-form) | **Form handler** - Connect to submission endpoint |
| User content (user-saves-data) | **Storage backend** - Set up persistence, define schema, wire CRUD, confirm data round-trips |
| Display-only | No step 3 - content is already in HTML |
| Mixed | Combine relevant steps above |

**Full tier additions** (insert between steps 2 and 3):

```
2.5. Worker proxy - deploy Worker with KV bindings, health endpoint
2.6. Cron job - GitHub Actions schedule, data fetch script, KV writes
```

> **For AI assistants:** Follow the Implementation Order step by step. If any requirement is ambiguous, ask the user - do not assume. Verify design with mock data before connecting real data. Include this guidance in any spec or scaffold produced by this command.

**Testing strategy:** Test the data path (fetch → transform → render), not the component tree. For full tier: test that Worker proxy serves cached data on upstream failure. For user-saves-data: test the CRUD round-trip. For all tiers: verify each UX state from Step 3 renders correctly.

### Step 8: Scaffold

Generate project files with the decisions from Steps 1-7 baked in. The scaffold must work immediately with mock data - no Cloudflare account needed.

The structure adapts to the conversation. No `worker/` if minimal tier. No `data-cron.yml` if live-only. The command shapes the files, not the other way around.

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
│   ├── sitemap.xml           # Generated or static (multi-page)
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
├── CHANGELOG.md
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

- `wrangler.toml`: no `[env.dev.vars]` section - causes interactive prompts in CI. Use `.dev.vars` locally.
- `deploy.yml`: content-hash comparison to skip no-change deploys. Actions pinned to commit SHAs (supply chain security).
- `worker/src/index.ts`: accept both GET and HEAD requests (uptime monitors send HEAD).
- `ci.yml` and `deploy.yml` are separate workflows - push ≠ ship.
- Service worker: network-first for HTML (get latest deploy), cache-first for static assets. Bump cache version on release.
- sessionStorage/localStorage: always try-catch (private browsing, storage disabled).

**First run:**

```bash
npm install && npm run dev    # Standard/full tier
# or just open index.html     # Minimal tier
```

Pages render with mock data. No Cloudflare account needed.

---

## Ship Gate

Single exit gate for Phase A. The scaffold produces correct structure from your decisions - this gate verifies you've customized placeholders and the Gist is ready for visitors.

**Verify scaffold output:**

- [ ] `<html lang>`, `<title>`, `<meta description>`, canonical, theme-color match your choices
- [ ] CSP `<meta>` tag matches your variant from Step 6
- [ ] Semantic landmarks, one `<h1>` per page, skip-to-content link
- [ ] OG tags populated (title, description, image, url)

**Replace placeholders:**

- [ ] Favicon set (ico + svg + apple-touch-icon) - derived from logo
- [ ] OG image (1200×630)
- [ ] App icons for manifest (192×192 + 512×512 PNG)

**Quality:**

- [ ] Lighthouse 90+ (Performance, Accessibility, Best Practices, SEO)
- [ ] All UX states verified (loading, loaded, error, empty, offline)
- [ ] Mobile tested (responsive, touch targets 44px+, no horizontal scroll)
- [ ] Keyboard navigation works, focus indicators visible
- [ ] `prefers-reduced-motion` and `prefers-color-scheme` respected
- [ ] WCAG AA contrast ratios met

**Security:**

- [ ] No secrets in frontend code (API keys in Worker secrets only)
- [ ] DOM safety enforced (see Trust Boundaries)
- [ ] External data sanitized before rendering
- [ ] Dependencies audited (`npm audit`)

**Discovery files present:** robots.txt, sitemap.xml, humans.txt, site.webmanifest

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

### 2. KV Namespace (standard/full tier only)
- Create: `wrangler kv namespace create "CACHE"`
- Create preview: `wrangler kv namespace create "CACHE" --preview`
- Update wrangler.toml with both IDs

### 3. API Secrets (if keyed-api)
- Set secret: `wrangler secret put API_KEY`
- GitHub: repo Settings → Secrets → `CF_API_TOKEN`

### 4. GitHub Actions
- Enable Actions in repo Settings
- Add secrets: `CF_API_TOKEN`, `CF_ACCOUNT_ID`

### 5. DNS (optional - skip for *.pages.dev)
- Custom domain: Pages → Custom domains → Add
```

### Step 10: First Deploy

```bash
git push origin main
```

CI runs. Pages deploy. Worker deploy (if applicable). Verify:

- Pages serve at `project-name.pages.dev`
- Worker proxies at `project-name.workers.dev/api/...` (if applicable)
- `/health` returns 200 on both GET and HEAD (if Worker deployed)
- Cron runs on schedule (if applicable)

**Post-deploy:** Enable CF Web Analytics (free, privacy-first). Pin API versions if available. Tag first release (`git tag -a v1.0.0 -m "Initial release"`). For Worker observability, the CF Workers dashboard shows request counts, errors, and latency.

---

## Budget Math

Calculate during Step 2. Exceeding free tier limits is the #1 failure mode.

**Formula:**

```
API hits/day = (active_hours * 60 / kv_ttl_minutes) + cron_runs
```

**Free tier headroom:**

| Resource | Free Tier | Notes |
|----------|-----------|-------|
| Workers requests | 100K/day | Exceeding returns 1015 errors (visible to users) |
| KV reads | 100K/day | Exceeding returns errors (visible) |
| KV writes | 1K/day | **Exceeding fails silently** - always check put() response |
| KV storage | 1 GB | |
| Pages builds | 500/month | |
| GH Actions | 2K min/month | |
| D1 rows (if user-saves-data) | 5M read, 100K written/day | |
| Supabase (if user-saves-data) | 500MB storage, 2GB bandwidth/month | |

> Sharing a CF account across apps? KV writes (1K/day) are shared. Divide by app count.

**Active window refinement:** Usage pattern global (24h) or regional (e.g., 14h)? Fewer active hours = fewer API hits. Factor this into the formula.

**Cache guidance:** Two-tier cache (edge response + KV) prevents thundering herd. Set edge TTL shorter than KV TTL. Always set `expirationTtl` on KV puts - without it, stale entries live forever if your cron stops. Validate API response shape before caching - fail at write time, not when serving corrupt data.

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Force-fit an idea that needs auth/accounts | Redirect to `/pb-repo-init` in Step 1 |
| Skip budget math | Calculate it - free tier surprise is the #1 failure mode |
| Deploy before local dev works | Phase A must complete before Phase B |
| Use `[env.dev.vars]` in wrangler.toml | Use `.dev.vars` file (not committed) |
| Deploy from local machine | CI is the only deploy path |
| Set up CF account before writing code | Scaffold works with mocks - deploy when ready |
| Ship with placeholder favicon and OG image | Replace before go-live |
| Connect real data before design approval | Mock data first → visual sign-off → wire up real data |
| Assume the AI assistant knows your preferences | Be explicit in specs - design vibe, error copy, UX states |
| Use `innerHTML` with dynamic content | Use `textContent` or DOM APIs (see Trust Boundaries) |
| Default to Tailwind/Preact for simple apps | Start vanilla. Add tools when vanilla isn't enough. |

---

## Related Commands

- `/pb-repo-init` - Generic greenfield initiation (when the Gist topology doesn't fit)
- `/pb-start` - Begin feature work after scaffolding
- `/pb-patterns-cloud` - Cloud deployment patterns reference
- `/pb-design-language` - Deeper design system work (optional, after scaffold)
- `/pb-calm-design` - Calm design principles (Gists embody these by default)

---

*Opinionated about topology. Flexible about content. Calm by default. $0/month is a feature, not a constraint.*
