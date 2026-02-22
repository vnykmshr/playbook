---
name: "pb-zero-stack"
title: "Zero-Stack App Initiation ($0/month Architecture)"
category: "repo"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "interactive"
related_commands: ['pb-repo-init', 'pb-start', 'pb-patterns-cloud', 'pb-design-language', 'pb-calm-design']
last_reviewed: "2026-02-22"
last_evolved: ""
version: "2.0.0"
version_notes: "Tidepool identity, calm-by-default DNA, product brief in Step 1, content decisions, go-live readiness, framework-specific guidance"
breaking_changes: []
---
# Zero-Stack App Initiation ($0/month Architecture)

A thinking tool for building **Tidepools** — small, self-contained apps fed by external data on a natural cycle. You visit when you're curious. They cost nothing to exist. They're calm by design.

The topology: static site, edge API proxy, CI pipeline. Two vendor accounts. Zero servers. Zero monthly cost. Only fixed cost: domain registration (~$10-15/year) if you want a custom domain — the `*.pages.dev` default is free.

A structured conversation that takes an idea (or PRD) and walks through the product, data, design, and content decisions that produce a tailored project scaffold — not a generic template you fork and gut.

**Mindset:** Apply `/pb-preamble` thinking — challenge whether the idea fits this topology before committing to it. Apply `/pb-design-rules` thinking — the topology is simple by default, modular, and fails noisily. Apply `/pb-calm-design` thinking — Tidepools respect user attention by default.

**Resource Hint:** sonnet — scaffolding follows established patterns; architecture decisions are guided, not open-ended

---

## When to Use

- Building a read-heavy, API-backed app with public data
- Side project that should cost $0/month to run
- Want production architecture without production ops burden
- Starting from an idea, not a template

## When NOT to Use

- User-generated content, file uploads, or auth required — use `/pb-repo-init`
- Real-time collaboration or WebSocket-heavy — use `/pb-repo-init` + `/pb-patterns-async`
- Relational data or complex queries — use `/pb-repo-init` + `/pb-patterns-db`
- SSR required — this topology serves static files at the edge

If the idea doesn't fit, redirect early. Don't force the topology.

---

## The Non-Negotiable Topology

Every zero-stack app has the same shape:

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

This is what makes it a pattern, not a collection of choices. The topology is fixed. Choices within it are flexible. A Tidepool is any app that fits this topology.

### Calm by Default

The topology enforces calm design (see `/pb-calm-design`). No auth means no login wall. No write path means no input validation. Read-heavy means information display, not task management. Data refreshes on its own schedule — users check when they want to, not when the app demands it.

These defaults are non-negotiable for a Tidepool:

- **Silence during normal operation** — data appears or shows a stale timestamp. No "refreshing..." banners. Live proxy path may have a brief initial load; use stale-first rendering (show cached data, update in place).
- **Stale over empty** — if the cache is old, show it with a timestamp. Never show an empty page when you have cached data.
- **Status in the periphery** — "Last updated 3 hours ago" in the footer, not a toast notification.
- **Works on first visit** — no onboarding, no configuration, no "sign up to see data."
- **Graceful offline** — PWA serves cached data with clear staleness indicator. No error walls.

---

## Phase A: Shape (One Session)

Goal: idea to working local dev with mock data. No accounts needed.

### Step 1: Product Brief & Fit

Start with the product, not the technology. If the user has a PRD, extract these answers from it. If they have an idea, ask:

```
What are you building? (one sentence)
> ___

Who checks this?     (developers, commuters, parents, traders?)
> ___

What do they learn in 5 seconds?  (AQI is 42, BTC is $68K, next bus in 3 min)
> ___

Where does the data come from?  (public API, RSS feed, government data portal?)
> ___

When do they come back?  (daily habit, event-driven, seasonal?)
> ___
```

These four answers — audience, headline value, data source, return pattern — drive every subsequent decision: data freshness, display type, active window, content layout, and calm design choices. Pin them before moving on.

**Fit checklist:**

Now validate that the idea fits the Tidepool topology:

```
Fit checklist:
  ✓ Read-heavy? (users consume data, not create it)
  ✓ Public data? (no user auth required)
  ✓ API-backed? (data comes from an external API)
  ✓ Low write frequency? (updates hourly or less, not per-request)
```

**All four checked:** proceed to Step 2.
**Three of four?** Describe the exception. Some near-misses work with minor adaptations — a contact form can POST to a Worker that writes to KV, optional auth can use CF Access, static data sources just skip the proxy. If the adaptation is small, proceed. If it reshapes the architecture, redirect.
**Two or fewer:** redirect to `/pb-repo-init` or `/pb-plan`. Don't force the topology.

### Step 2: Data Architecture

Walk through these decisions. Each one shapes the scaffold.

**Data source:**

- What API(s) are you pulling from?
- Free tier limits? (daily request cap, rate limits)
- Auth method? API key is fine. OAuth means this probably isn't zero-stack.

**Update frequency:**

- How often does the data change? (real-time, hourly, daily)
- What freshness do users expect?
- This determines which data paths to use:

| Freshness Need | Data Path | Implementation |
|---------------|-----------|----------------|
| Minutes | Live Worker proxy | Worker fetches on request, caches in KV |
| Hours | Cron + Worker | GitHub Actions cron writes to KV, Worker serves from KV on request |
| Daily | Cron + rebuild | GitHub Actions cron fetches data and triggers a Pages rebuild with data baked into static HTML |

**Active window:**

- Usage pattern: global (24h) or regional (e.g., 14h active window)?
- This drives budget math — fewer active hours = fewer API hits

**Budget math** (calculate for the user):

```
API hits/day = (active_hours * 60 / kv_ttl_minutes) + cron_runs
```

Show the result against free tier headroom:

| Resource | Free Tier | This App | Headroom |
|----------|-----------|----------|----------|
| Workers requests | 100K/day | [calculated] | [remaining] |
| KV reads | 100K/day | [calculated] | [remaining] |
| KV writes | 1K/day | [calculated] | [remaining] |
| Pages builds | 500/month | [calculated] | [remaining] |
| GH Actions | 2K min/month | [calculated] | [remaining] |

> **Sharing a CF account across apps?** KV writes (1K/day) are shared across all apps on the account. Divide the limit by your app count.

**What happens when you exceed free tier:** Workers requests beyond 100K/day return 1015 errors (visible). KV reads beyond 100K/day return errors (visible). KV writes beyond 1K/day return 429 errors — but if your Worker doesn't check the KV put response, stale data keeps being served and you won't know your cron updates stopped landing. Always check KV write responses. Pages builds beyond 500/month queue and may time out.

**Production lessons to surface in this step:**

- Two-tier cache (edge response cache + KV storage) prevents thundering herd across Cloudflare's 200+ PoPs. Set edge TTL shorter than KV TTL — edge serves stale while one PoP refreshes from KV.
- Set `expirationTtl` on every KV put. Without it, stale entries live forever if your cron stops or your key format changes.
- Cloudflare WAF rate limiting is a paid feature. Don't investigate it — the built-in cache layers are sufficient for read-heavy patterns.
- Validate API response shape before caching. If the upstream API changes its schema, you want to fail at write time, not serve corrupt cached data.

### Step 3: Project Shape

**Basics:**

- Project name (lowercase, hyphenated)
- Single page or multi-page? (default: single, grow later)
- Primary display: dashboard, ticker, list, map, or other?
- PWA with service worker? (default: yes — offline shows stale data with timestamp)

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
| Description | \[one sentence from Step 1\] | Reuse fit description |
| Language | en / es / fr / ... | en |

These feed into `<title>`, `<meta name="description">`, `<html lang>`, manifest, and OG tags. Set once, used everywhere.

**Creative assets** (generate or provide):

| Asset | Format | Dimensions | Notes |
|-------|--------|------------|-------|
| Logo mark | SVG preferred | — | Simple mark, works at 16px. Used as favicon source |
| Favicon set | .ico + .svg + apple-touch-icon.png | 16/32/180/512 | Derive from logo SVG |
| OG image | PNG or JPG | 1200×630 | Social sharing preview. Static file or build-time generated |

Don't block on assets — the scaffold includes placeholders. Replace before go-live.

If using an AI image tool or design tool, provide the project name and description from above as the brief. A simple geometric mark at high contrast works better than a detailed illustration at favicon sizes.

**Content decisions** (what goes on the page):

| Element | Source | Notes |
|---------|--------|-------|
| Headline metric/status | From API response | The 5-second answer from Step 1 |
| Supporting context | Derived or static | What explains the headline (trend, range, comparison) |
| Data attribution | Static | "Data from \[API name\]" — users deserve to know the source |
| Freshness indicator | Cache timestamp | "Updated 2 hours ago" — peripheral, not prominent (calm default) |
| Empty state | Static copy | What shows before first data load or if API is unreachable |
| Error state | Static copy + stale data | Show last known data with explanation, not an error wall |
| Footer | Static + cache timestamp | Data attribution, freshness indicator, API link — calm design lives here |

Empty and error states are product decisions, not afterthoughts. A Tidepool that shows "Error fetching data" on first visit is a broken window. Show a meaningful placeholder or explain what the user will see once data flows.

### Step 4: Stack Confirmation

Show the default stack with rationale. Allow substitutions but warn about cascading effects.

| Layer | Default | Why | Substitution Notes |
|-------|---------|-----|--------------------|
| SSG | Astro | Islands architecture, zero JS by default | Hugo if no JS needed at all |
| Islands | Preact | 3KB, React-compatible API | Svelte if team prefers; vanilla JS if minimal |
| CSS | Tailwind v4 | Zero-config Vite plugin | Vanilla CSS if app is small |
| Host | CF Pages | Free, atomic deploys, edge network | Vercel if already invested (changes proxy layer too) |
| Proxy | CF Worker | Same vendor as Pages, KV built-in | Vercel Edge if Pages moved to Vercel |
| Cache | CF KV | Global, free 100K reads/day | Upstash if on different host |
| CI | GitHub Actions | Native git integration, cron support | GitLab CI if repo lives there |

The default stack is chosen as a unit — single vendor for hosting means one API token, one dashboard, one set of docs. Substituting one piece may cascade. Flag this clearly:

> Changing the host from CF Pages also changes the proxy, cache, and deployment story. That's fine if you're already on Vercel — just know it's a package deal.

Confirm or adjust, then proceed.

### Step 5: Scaffold

Generate project files with the decisions from Steps 2-4 baked in. The scaffold must work immediately with mock data — no Cloudflare account needed.

The structure below is representative — the actual scaffold adapts to the conversation. No `normalizer.ts` if the API has a stable schema. No `data-cron.yml` if the data path is live-only. The command shapes the files, not the other way around.

**Representative structure:**

```
project-name/
├── public/
│   ├── favicon.ico           # Placeholder, replace before go-live
│   ├── favicon.svg           # SVG favicon (modern browsers)
│   ├── apple-touch-icon.png  # 180×180 (iOS)
│   ├── og-image.png          # 1200×630 (social sharing)
│   ├── robots.txt            # Crawler directives
│   ├── humans.txt            # Attribution
│   └── site.webmanifest      # PWA metadata (ties to Step 3 choices)
├── src/
│   ├── pages/              # Astro pages
│   │   └── 404.astro       # or 404.html / 404.md depending on framework
│   ├── components/         # Preact islands
│   ├── styles/
│   │   └── design-tokens.css  # From Step 3 choices
│   └── lib/
│       └── api.ts          # Data fetching (uses mock in dev)
├── worker/
│   ├── index.ts            # Edge proxy
│   ├── cache.ts            # KV cache with TTLs from Step 2
│   └── normalizer.ts       # Response shape validation
├── .github/
│   └── workflows/
│       ├── ci.yml          # Lint + type check + test
│       ├── deploy.yml      # Pages + Worker deploy
│       └── data-cron.yml   # (if cron path chosen in Step 2)
├── docs/
│   └── setup.md            # Bootstrap checklist (Phase B)
├── mock/
│   └── data.json           # Mock API response for local dev
├── wrangler.toml           # Worker config with TTLs, bindings
├── astro.config.mjs
├── package.json
├── tsconfig.json
└── README.md
```

**Production lessons baked into the scaffold:**

- `wrangler.toml`: no `[env.dev.vars]` section — it causes interactive prompts in CI. Use `.dev.vars` file locally instead.
- `deploy.yml`: content-hash comparison to skip no-change deploys. Never deploy locally with dev config — CI is the only deploy path.
- `worker/index.ts`: accepts both GET and HEAD requests. Uptime monitors send HEAD; returning 405 looks like downtime.
- `ci.yml` and `deploy.yml` are separate workflows. Push doesn't automatically deploy — release-gated deploys mean push != ship.
- `public/` directory includes go-live files (robots.txt, humans.txt, manifest, favicon placeholders). Replace creative asset placeholders before first deploy. Discovery files work as-is.

**First run:**

```bash
npm install && npm run dev
```

Pages render with mock data. Islands hydrate. In dev mode, `api.ts` detects no Worker and loads from `mock/data.json` directly — same component code, different data source. Ready for real API integration.

---

## Go-Live Readiness

The scaffold produces correct HTML structure, meta tags, and discovery files from your Step 3 decisions. This gate verifies you've customized the placeholders and confirms the Tidepool is ready for real visitors.

### Verify the scaffold got it right

The base layout should already include these from your Step 3 choices. Confirm, don't re-implement:

- `<html lang="...">` matches your language choice
- `<title>` and `<meta name="description">` match your web identity
- `<meta name="theme-color">` matches your palette
- `<link rel="canonical">` points to your production URL
- Semantic landmarks (`<header>`, `<main>`, `<footer>`) structure the page
- Skip-to-content link present for keyboard users
- One `<h1>` per page, proper heading hierarchy

Most SSGs (Astro, Hugo) handle charset, viewport, and lang in their base layout. If vanilla HTML, verify these are in your `<head>` manually.

### Replace creative asset placeholders

These are the placeholders the scaffold created. Replace all before first deploy:

- Logo mark (SVG) — the favicon and manifest icons derive from this
- Favicon set (ico + svg + apple-touch-icon) — derived from logo
- OG image (1200×630) — what people see when your URL is shared
- App icons for manifest (192×192 + 512×512 PNG)

### Verify social sharing

- `og:title`, `og:description`, `og:image`, `og:url` populated from Step 3 web identity
- `twitter:card` set to `summary_large_image`
- Test with a social sharing debugger before announcing

### Verify discovery files

- **robots.txt** — allows crawling, references sitemap
- **sitemap.xml** — generated by framework (Astro: `@astrojs/sitemap`, Hugo: built-in) or static file
- **humans.txt** — project name, tech stack, last updated
- **site.webmanifest** — name, icons, theme\_color, background\_color from Step 3

### Edge security

The scaffold includes a CSP header in `worker/index.ts` tailored to your stack: `default-src 'self'`, plus `connect-src` for your API origin (from Step 2), and `style-src`/`script-src` directives matching your CSS and island choices. A bare `default-src 'self'` would break Preact islands and external API calls — the scaffold generates the correct policy from your Step 4 stack decisions.

### Performance

The main performance decision is already made: Astro ships zero JS by default. If you added Preact islands, they hydrate individually — verify the bundle is small. The scaffold also includes `<link rel="preconnect">` for your API origin (from Step 2) and `<link rel="dns-prefetch">` as fallback.

### Framework reference

| Concern | Astro | Hugo | Vanilla JS/HTML |
|---------|-------|------|-----------------|
| Sitemap | `@astrojs/sitemap` | Built-in | Static file |
| Meta tags | In layout `<head>` | In `baseof.html` | In `<head>` |
| 404 page | `src/pages/404.astro` | `layouts/404.html` | `public/404.html` |
| Manifest | `public/site.webmanifest` | `static/site.webmanifest` | `site.webmanifest` |
| Favicon | `public/` directory | `static/` directory | Root directory |

---

## Phase B: Deploy (When Ready)

Goal: scaffold to production. Human-paced, no rush.

### Step 6: Bootstrap Checklist

Generate `docs/setup.md` with paste-able commands. Each step is one command with expected output.

```markdown
## One-Time Setup (~30 minutes)

### 1. Cloudflare Account
- Sign up at dash.cloudflare.com (free plan)
- Install Wrangler: `npm install -g wrangler`
- Login: `wrangler login`
  Expected: browser opens, authorize, "Successfully logged in"

### 2. KV Namespace
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

### Step 7: First Deploy

```bash
git push origin main
```

CI runs. Pages deploy. Worker deploy. Verify:

- Pages serve at `project-name.pages.dev`
- Worker proxies at `project-name.workers.dev/api/...`
- Cron runs on schedule (if applicable)
- `/health` returns 200 on both GET and HEAD

---

## Stack Rationale (Reference)

Why these defaults as a unit:

**Cloudflare (Pages + Workers + KV):** Single vendor means one authentication flow, one dashboard, one billing page (free), and same-origin advantage between Pages and Workers. KV is globally replicated with no configuration.

**Astro:** Islands architecture means zero JavaScript ships by default. Interactive components hydrate individually. Perfect for read-heavy dashboards where most content is static.

**GitHub Actions:** Native cron for data refresh. Same platform as the repo. Free tier (2K minutes/month) is generous for CI + scheduled data fetches.

**The unit matters more than any piece.** Swapping one component is fine if you swap its dependencies too. The command warns about cascading changes.

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Force-fit an idea that needs auth | Redirect to `/pb-repo-init` in Step 1 |
| Skip budget math | Calculate it — free tier surprise is the #1 failure mode |
| Deploy before local dev works | Phase A must complete before Phase B |
| Use `[env.dev.vars]` in wrangler.toml | Use `.dev.vars` file (not committed) |
| Deploy from local machine | CI is the only deploy path |
| Set up CF account before writing code | Scaffold works with mocks — deploy when ready |
| Build a framework or CLI tool | This is a thinking tool that produces a scaffold |
| Ship with placeholder favicon and OG image | Replace before go-live — they're the first thing people see when sharing |

---

## Related Commands

- `/pb-repo-init` — Generic greenfield initiation (when the Tidepool topology doesn't fit)
- `/pb-start` — Begin feature work after scaffolding
- `/pb-patterns-cloud` — Cloud deployment patterns reference
- `/pb-design-language` — Deeper design system work (optional, after scaffold)
- `/pb-calm-design` — Calm design principles (Tidepools embody these by default)

---

*Opinionated about topology. Flexible about content. Calm by default. $0/month is a feature, not a constraint.*
