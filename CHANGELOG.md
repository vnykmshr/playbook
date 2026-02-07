# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **pb-server-hygiene** — Periodic server health and hygiene review
  - 5-phase ritual: snapshot, health signals, drift detection, cleanup, future readiness
  - Weekly/monthly/quarterly cadence with phase mapping
  - Safe cleanup patterns with dry-run-first discipline
  - Drift and bloat detection checklists (disk, service, config, security)
  - Server manifest template for living documentation
  - Red flags section for recognizing neglected servers

### Changed

- **pb-maintenance** — Updated Related Commands (swapped pb-hardening for pb-server-hygiene)
- **pb-hardening** — Added pb-server-hygiene back-link to Related Commands

### Stats

- **Total commands**: 83 (was 82)
- **Files modified**: 4
- **Theme**: Server operations, periodic hygiene ritual

---

## [v2.7.0] - 2026-02-07

### Added

- **pb-claude-orchestration** — New orchestration guide for Claude Code
  - Three model tiers: Architect (opus), Engineer (sonnet), Scout (haiku)
  - Task-to-model mapping with decision criteria
  - Task delegation patterns (parallel vs sequential, when to delegate)
  - Context budget management and efficiency principles
  - Playbook-to-model mapping by classification
  - Self-healing behaviors and auto-memory feedback loops
  - Continuous improvement: observe outcomes, record learnings, surface gaps
  - Anti-patterns table for common orchestration mistakes

- **pb-review-playbook** — Quick Review Mode
  - Abbreviated 4-perspective review for 1-3 changed commands
  - Escalation criteria for full review
  - Model delegation hints per review phase (haiku/opus/opus)
  - Self-improvement trigger for systemic patterns

### Changed

- **pb-review-playbook** — Fixed stale category counts
  - Replaced hardcoded counts with dynamic shell command
  - Removed stale "Release (1)" category (merged into deployment in v2.3.0)
  - Added missing "Utilities" category

- **pb-new-playbook** — Resource awareness (v1.0.0 → v1.1.0)
  - Added Resource Hint field to scaffold template
  - Added classification-to-model table
  - Added quality validation: resource hint, context budget
  - Added integration validation: CLAUDE.md regeneration, quick review

- **pb-claude-global** — Template trimmed and enriched
  - Replaced Context Management with Context & Resource Efficiency
  - Added model selection table and continuous improvement directive
  - Merged Commits + PRs into single concise section
  - Trimmed Quick Reference to 8 essential entries
  - Generated CLAUDE.md: 212 → 144 lines (under 150-line target)

### Stats

- **Total commands**: 82 (was 81)
- **Files modified**: 5
- **Themes**: Model orchestration, resource efficiency, operational self-improvement

---

## [v2.6.0] - 2026-02-03

### Added

- **pb-patterns-api** — Response Design section
  - DTO discipline: separate data layer from API contracts
  - Field selection guidance (4 questions per field)
  - List vs. detail response patterns
  - Large field handling (exclude from lists, lazy load, compress)
  - "When NOT to optimize" guardrails
  - TypeScript, Python, Go examples
  - 676 → 845 lines (+25%)

- **pb-patterns-api** — Input Binding Discipline section
  - Mass assignment prevention patterns
  - Allowlisted writable fields per operation
  - Mirror of Response Design: explicit about what goes in, not just out

- **pb-patterns-api** — GraphQL Security section
  - Query depth and complexity limiting
  - Introspection disabled in production
  - Batching attack prevention
  - Field-level authorization

- **pb-security** — Web application vulnerability depth
  - CSRF prevention checklist (7 items + SPA bearer-token note)
  - Open redirect prevention with bypass catalog
  - XXE prevention by language (Python, Node.js, Go)
  - File upload attack catalog (double extensions, polyglot, SVG XSS, ZIP slip)
  - SSRF bypass techniques table with DNS resolution pattern
  - Security headers reference with exact values
  - IDOR, mass assignment, JWT-specific attacks, race conditions (TOCTOU)
  - XSS indirect input sources (WebSocket, postMessage, localStorage)
  - 540 → 660 lines (+22%)

### Changed

- **pb-security** — Deep Dive consolidation
  - Security headers deduplicated (Advanced API Security now cross-references)
  - CSRF contradiction between tiers resolved
  - Go: replaced archived `gorilla/mux` with `net/http` and `go-chi/chi`
  - Added `defusedxml` to Python recommended packages

- **pb-review-code** — API payload awareness
  - Architecture Review: explicit response shapes check
  - Security Review: consolidated API exposure items to cross-reference `/pb-security`
  - Red Flags: oversized API payloads added

- **pb-patterns-api** — Design Rules Applied table
  - Added Separation rule (API contract decoupled from data layer)
  - Updated Clarity rule (response shapes communicate intent)

### Stats

- **Files modified**: 3
- **Net change**: +327 lines across security and API design coverage
- **Commits**: 3

---

## [v2.5.0] - 2026-01-29

### Changed

- **pb-guide** — Removed 847 lines of duplicate async/distributed pattern examples
  - Content now cross-references `/pb-patterns-async` and `/pb-patterns-distributed`
  - Removed Appendix B (redundant with Quick Reference)
  - 1475 → 628 lines (-57%)

- **pb-incident** — Moved on-call scheduling content to pb-sre-practices
  - Now focuses purely on incident response
  - Cross-references `/pb-sre-practices` for on-call setup
  - 893 → 681 lines (-24%)

- **pb-sre-practices** — Received on-call scheduling and setup content
  - On-call rotation structure, tools, expectations
  - Mock incident training guidance
  - 593 → 646 lines (+9%)

- **pb-patterns-core** — Removed duplicate TypeScript/JavaScript examples
  - Kept Python as canonical language per pattern
  - 1306 → 1231 lines (-6%)

- **pb-patterns-distributed** — Condensed duplicate language examples
  - Removed Python Saga Idempotency (kept JS)
  - Condensed JS Outbox to outline (kept Python)
  - 1266 → 1124 lines (-11%)

- **pb-patterns-db** — Removed duplicate JavaScript examples
  - Kept Python connection pooling and denormalization
  - 1113 → 1022 lines (-8%)

- **pb-patterns-security** — Condensed Go OAuth/JWT examples to outlines
  - Kept Python as full examples
  - 929 → 769 lines (-17%)

- **pb-patterns-async** — Condensed Python examples to brief outlines
  - JavaScript is canonical for async patterns
  - Kept unique Python patterns (multiprocessing, Celery)
  - 802 → 705 lines (-12%)

- **Related Commands standardized** — Trimmed to ≤5 items across all commands
  - pb-cycle: 10 → 5
  - pb-what-next: 11 → 5
  - pb-review: 11 → 5
  - pb-review-microservice: 6 → 5
  - pb-repo-docsite: 7 → 5

- **Integration sections trimmed** — Removed verbose workflow diagrams
  - pb-resume: Removed redundant workflow diagram
  - pb-standup: Removed verbose command list

### Stats

- **Total lines**: 44,251 → 42,605 (-1,646 lines, -3.7%)
- **Files modified**: 15
- **Commits**: 8

---

## [v2.4.0] - 2026-01-29

### Added

- **pb-maintenance** — New command for production maintenance patterns
  - Question-driven maintenance philosophy
  - Tier-based scheduling (daily/weekly/monthly)
  - Database maintenance patterns (PostgreSQL focus)
  - Backup verification strategy (3-2-1 principle)
  - Health monitoring dimensions
  - Alerting quality checklist

- **pb-hardening** — SSL certificate and certbot patterns for Docker
  - SSL certificate access for containers with fixed GID
  - Certbot renewal hooks for Docker service coordination
  - Additional auditd rules (Docker config, sudoers)
  - Troubleshooting table for common issues

- **pb-sre-practices** — Server migration checklist
  - Full database dump/restore patterns
  - Post-migration verification queries
  - New server security verification table
  - Rollback plan guidance

- **pb-cycle** — Context checkpoint step (Step 7)
  - Signs of context filling up with concrete thresholds
  - Natural breakpoints guidance
  - Updated Quick Cycle Summary

- **pb-plan** — Context-efficient plan structure
  - Principles for resumability without full reload
  - Directory structure with done/ folder for archives
  - Updated master tracker template with Current Status section

- **pb-claude-global** — Context management section
  - Subagent usage for exploration
  - Context exhaustion recovery patterns
  - Updated output checklist with 2K token target

- **pb-claude-project** — Conciseness guidelines
  - 2K token / 150 line target
  - Keep vs move to docs/ guidance
  - Aggressive trimming examples

### Changed

- **pb-observability** — Added cross-reference to pb-maintenance
- **pb-dr** — Added cross-reference to pb-maintenance
- **pb-incident** — Added cross-reference to pb-maintenance (prevention)
- **pb-resume** — Added context efficiency guidance
- **pb-pause** — Added context state preservation guidance

### Stats

- Total commands: 81 (was 80)
- Files modified: 12
- Themes: Operations lifecycle, Context efficiency

---

## [v2.3.0] - 2026-01-24

### Changed

**Documentation Hygiene & Consistency**

Addresses periodic review findings to improve maintainability and reduce drift.

- **Removed hardcoded counts** — README and docs no longer reference specific command counts
  - Prevents maintenance burden when adding/removing commands
  - Uses generic language ("comprehensive set" instead of "78 commands")

- **Fixed broken mkdocs links** — 3 links in technical-blog.md corrected
  - Now point to quick-ref pages instead of non-existent command files

- **H1 title consistency** — Fixed bold formatting in pb-guide.md
  - Standard: `# Title` (no bold, no special formatting)

- **Standardized Related Commands** — Renamed "See Also" to "Related Commands" in 4 files
  - pb-design-rules, pb-preamble-async, pb-preamble-decisions, pb-preamble-power

- **Category consolidation** — Merged release/ into deployment/
  - pb-release.md moved to commands/deployment/
  - 9 categories reduced to 9 (release was single-file category)

- **Trimmed verbose pattern files** — 876 lines removed (21% reduction)
  - pb-patterns-distributed: 1521 → 1266 lines (-17%)
  - pb-patterns-db: 1452 → 1113 lines (-23%)
  - pb-patterns-async: 1070 → 802 lines (-25%)
  - Removed redundant Go Examples sections, kept representative examples

### Added

- **"When to Use" sections** — Added to 15 commands for better discoverability
  - development: pb-commit, pb-cycle, pb-debug, pb-pr
  - deployment: pb-incident, pb-database-ops, pb-dr, pb-hardening, pb-sre-practices
  - core: pb-documentation
  - reviews: pb-security
  - people: pb-onboarding, pb-knowledge-transfer
  - repo: pb-repo-init, pb-repo-organize

### Command Count

- Commands: 78 (unchanged)
- Categories: 9 (release/ merged into deployment/)

---

## [v2.2.0] - 2026-01-24

### Added

**Playbook Philosophy Evolution**

Integrates three foundational concepts into the playbook DNA:

- **Guardrails section** — Added to `/pb-claude-global` and `/pb-claude-project` templates
  - 4 universal rules for global (verify before done, preserve functionality, plan multi-file changes, git safety)
  - 5 project-specific constraints template (infrastructure, dependencies, ports, design system, data safety)

- **MLP Quality Bar** — Added Section VII to `/pb-standards`
  - 3 criteria: daily use without frustration, recommend without apology, smallest complete thing
  - Mindset shift table: MVP thinking vs MLP thinking
  - "Build less. Care more." discipline

- **Genesis & Hierarchy** — Added to README.md
  - Why this playbook exists (genesis statement)
  - Document hierarchy: Project > Global > Playbook precedence

### Changed

- `/pb-claude-global` template streamlined, target reduced from 300 to 150 lines
- `/pb-standards` section numbering updated (VII → VIII for SDLC Discipline)
- Global CLAUDE.md: removed Technology Guidelines (project-level concern)

### Philosophy

This release elevates the playbook DNA from:
- Preamble + Design Rules

To:
- Preamble (how we think) + Design Rules (what we build) + Guardrails (what we protect) + Quality Bar (when we're done)

---

## [v2.1.0] - 2026-01-21

### Added

**Operational Automation Patterns**

Selective imports from `everything-claude-code` analysis to add automation capabilities while preserving philosophy-first approach.

- **`/pb-learn`** — New command for capturing reusable patterns from sessions
  - Error resolutions, debugging techniques, workarounds, project conventions
  - Project-local storage (`.claude/patterns/`) by default
  - Global storage (`~/.claude/learned/`) with `--global` flag
  - Comprehensive template and real-world examples

- **`hooks/` directory** — Hook patterns documentation
  - README explaining Claude Code hook lifecycles (PreToolUse, PostToolUse, PreCompact, SessionStart, Stop)
  - Example patterns for console.log detection, tmux reminders, session state preservation
  - Copy-and-adapt approach (not auto-installed)

### Changed

- **`/pb-review-code`** — Added approval decision matrix and review verdicts
  - Severity mapping: Critical (MUST) → Warning (SHOULD) → Suggestion (CONSIDER/NIT)
  - Explicit verdicts: APPROVED, CONDITIONAL, BLOCKED
  - Example verdict format for consistent reviews

- **`/pb-resume`** — Added session state preservation guidance
  - What to preserve before compaction (state, decisions, blockers, next steps)
  - Strategic compaction timing (good vs bad transition points)
  - Session notes template
  - Cross-reference to hooks for automation

- **`/pb-debug`** — Added cross-reference to `/pb-learn` for pattern capture
- **`/pb-cycle`** — Added cross-reference to `/pb-learn` for pattern capture

### Command Count

- Before: 72 commands
- After: 73 commands (+1 new command)

---

## [v2.0.0] - 2026-01-21

### Breaking Changes

#### Thinking Partner Consolidation
- **REMOVED**: `/pb-query`, `/pb-ideate`, `/pb-synthesize`
- **ADDED**: `/pb-think` — Unified thinking command with modes
  - `/pb-think` (default) — Full cycle: ideate → synthesize → refine
  - `/pb-think mode=ideate` — Divergent exploration
  - `/pb-think mode=synthesize` — Integration and combination
  - `/pb-think mode=refine` — Convergent refinement

#### Review Command Hierarchy
- **REMOVED**: `/pb-review-cleanup` (merged into pb-review-hygiene)
- **CHANGED**: `/pb-review` now acts as orchestrator, guiding users to specialized review commands
- **CHANGED**: `/pb-review-hygiene` now covers both code quality and operational readiness

#### Category Reorganization
- **MOVED**: `/pb-knowledge-transfer` from development → people
- **MOVED**: `/pb-design-language` from development → planning

### Improvements

- All review commands now have Related Commands sections
- Removed emojis from titles for consistent text-only style
- Fixed cross-reference issues in pb-hardening and pb-sre-practices
- Added Related Commands to all repo commands
- Added Related Commands to pb-context
- Fixed structure consistency in pb-review-docs, pb-review-tests, pb-review-product

### Command Count

- Before: 75 commands
- After: 72 commands (-3 due to consolidation)

---

## [v1.9.0] - 2026-01-20

### Added

**Production Readiness & Operational Excellence**
- Added 5 new commands for production operations and security:
  - `/pb-hardening` — Server, container, and network security hardening
  - `/pb-secrets` — Secrets management lifecycle (SOPS, Vault, rotation, incident response)
  - `/pb-sre-practices` — SRE operational practices (toil, error budgets, on-call health)
  - `/pb-dr` — Disaster recovery planning (RTO/RPO, backups, game days)
  - `/pb-database-ops` — Database operations (migrations, backups, performance, failover)

**`/pb-hardening` (Security Hardening)**
- Server setup: SSH hardening, UFW firewall, fail2ban, auditd
- Docker container security: cap_drop ALL, no-new-privileges, non-root users, read-only fs
- Network isolation: internal Docker networks, service authentication, port exposure rules
- Host hardening: kernel parameters, automatic security updates
- Pre-deployment and post-deployment security checklists
- Defense-in-depth philosophy

**`/pb-secrets` (Secrets Management)**
- Secrets hierarchy: local dev → CI/CD → staging → production
- SOPS + age encryption workflow with detailed setup guide
- HashiCorp Vault patterns for dynamic secrets
- Cloud secrets managers comparison (AWS, GCP, Azure)
- Rotation strategies: manual checklist, automated, zero-downtime
- Incident response: immediate rotation, investigation, prevention tools

**`/pb-sre-practices` (SRE Practices)**
- Toil identification and reduction with tracking templates
- Error budget policies: healthy, concerning, critical, exhausted
- Capacity planning with forecasting and quarterly review templates
- Service ownership model with handoff protocol
- Blameless culture and psychological safety
- On-call health: rotation patterns, load metrics, burnout prevention
- Operational review cadence: weekly, monthly, quarterly, annually

**`/pb-dr` (Disaster Recovery)**
- RTO/RPO definitions with business alignment guidance
- Backup strategies: 3-2-1 rule, immutable backups, verification
- Failover procedures: manual runbook, automated, DNS-based
- Recovery testing: game day exercises, chaos engineering, tabletop exercises
- Data recovery workflows: point-in-time, file system, application state
- Communication templates: status page, stakeholder, customer email
- DR plan template for critical services

**`/pb-database-ops` (Database Operations)**
- Migration patterns: expand/contract for zero-downtime schema changes
- Backup operations: automated scripts, verification, retention policies
- Performance baselines and query optimization guidelines
- Connection pooling with PgBouncer configuration patterns
- Common runbooks: slow queries, connection exhaustion, replication lag
- Failover procedures for high availability
- Production checklist for database deployments

### Documentation

- Updated command-index: Added Security & Hardening section, expanded Release & Operations
- Created new command category structure for operations-focused commands

### Status

- 73 commands across 10 categories
- Complete production readiness workflow
- Defense-in-depth security approach integrated

---

## [v1.8.0] - 2026-01-20

### Added

**Repository Documentation Infrastructure**
- Added `/pb-repo-docsite` — Transform project documentation into professional static sites
  - Tech stack selection: Hugo (Go), MkDocs (Python), Docusaurus (Node.js)
  - Phase workflow: Infrastructure → Migration → Content → Hygiene → Release
  - CI/CD templates for GitHub Pages deployment
  - Mermaid diagram support across all SSGs
  - Editorial guidelines aligned with `/pb-documentation` standards

**`/pb-repo-docsite` Features**
- Transformation workflow for existing markdown docs
- Greenfield setup for new projects
- Tech-specific appendices (setup, config, workflows)
- Content migration map (ALLCAPS → lowercase-hyphenated)
- Standard 10-12 page documentation structure
- Anti-patterns and troubleshooting sections
- Integration with `/pb-repo-enhance` suite

### Status

- 68 commands across 10 categories
- Complete repository documentation workflow
- Standardized docsite transformation across projects

---

## [v1.7.0] - 2026-01-19

### Added

**Frontend & Fullstack Quality**
- Added 5 new commands for frontend development and debugging:
  - `/pb-patterns-frontend` — Mobile-first, theme-aware frontend architecture patterns
  - `/pb-design-language` — Project-specific design specification template
  - `/pb-a11y` — WCAG 2.1 AA accessibility guidance and testing
  - `/pb-patterns-api` — REST, GraphQL, gRPC design patterns
  - `/pb-debug` — Systematic debugging methodology

**`/pb-patterns-frontend` (Frontend Architecture)**
- Component patterns: atomic design, compound components, container/presentational
- State management: location decision tree, server vs client state, URL state
- UI states: loading, error, empty states with code examples
- Form patterns: layout, validation, multi-step forms
- Performance: code splitting, lazy loading, memoization
- Theming: design tokens, dark mode, skinnable interfaces
- Responsive: mobile-first breakpoints, fluid typography, container queries

**`/pb-design-language` (Design Specification)**
- Bootstrap template for new projects
- Voice & tone guidelines
- Color, typography, spacing, motion tokens
- Component vocabulary standardization
- Constraints documentation (what we don't do)
- Decision log for rationale

**`/pb-a11y` (Accessibility)**
- Philosophy: semantic HTML first, ARIA as enhancement, keyboard-first
- WCAG 2.1 AA baseline with 2.2 recommended enhancements
- Semantic structure, interactive elements, focus management
- Screen reader support, color/contrast, motion considerations
- Tiered testing tools and manual testing checklist

**`/pb-patterns-api` (API Design)**
- Decision framework: REST vs GraphQL vs gRPC
- REST patterns: resource naming, HTTP methods, status codes
- Error handling, pagination, versioning strategies
- Authentication: API keys, JWT, OAuth 2.0
- Rate limiting and GraphQL patterns

**`/pb-debug` (Debugging Methodology)**
- 6-step process: reproduce, isolate, hypothesize, test, fix, prevent
- Techniques: print, debugger, network, database, performance
- Frontend debugging: DevTools, network waterfall, React/Vue DevTools
- Common bug patterns and production debugging

### Documentation

- Added `docs/recipes.md`: Pre-built command sequences for common scenarios
- Added `docs/frontend-workflow.md`: Complete frontend development guide
- Updated command-index: Added all 5 new commands
- Updated pb-patterns: Added pb-patterns-frontend and pb-patterns-api
- Updated pb-what-next: Added frontend development recommendations
- Updated pb-testing: Added pb-a11y for accessibility testing
- Updated pb-guide: Added v1.7.0 commands to phase integrations

### Maintenance

- Removed hardcoded version references and command counts for maintainability

### Status

- 67 commands across 10 categories
- Complete frontend development workflow
- Accessibility-first approach integrated

---

## [v1.6.0] - 2026-01-19

### Added

**Session Management & Shipping Workflow**
- Added 2 new commands for development lifecycle management:
  - `/pb-pause` — Gracefully pause work, preserve context for later sessions
  - `/pb-ship` — Complete shipping workflow from code-complete to production

**`/pb-pause` (Session Management)**
- 7-step pause checklist: preserve state, update trackers, review docs, update context, update CLAUDE.md, document handoff, cleanup
- Standardized pause notes location (`todos/pause-notes.md`)
- Quick pause flow for short breaks
- Extended pause checklist for vacations/handoffs
- Integrates with `/pb-resume` as session boundary bookends

**`/pb-ship` (Complete Shipping Workflow)**
- Phase 1: Foundation — Quality gates + basic self-review
- Phase 2: Specialized Reviews (optimally ordered):
  - `/pb-review-cleanup` (code quality first)
  - `/pb-review-hygiene` (project health)
  - `/pb-review-tests` (coverage)
  - `/pb-security` (vulnerabilities)
  - `/pb-logging` (standards, optional)
  - `/pb-review-docs` (accuracy)
- Phase 3: Final Gate — `/pb-review-prerelease` + go/no-go decision
- Phase 4: PR & Peer Review — Create PR, peer review, iterate, get approval
- Phase 5: Merge & Release — Merge, deploy, verify, summarize
- Issue tracking template for review findings
- Escape hatch for trivial changes (typos, comments)
- Philosophy: "review does not harm, better safe than sorry"

### Documentation

- Updated README: Development commands 11→12
- Updated command-index: Added pb-pause, pb-ship to workflow tables
- Updated integration-guide: Command count 60→62, updated development flow
- Updated workflows: Daily workflow now shows pb-pause/pb-ship
- Updated pb-resume: Added pause notes reading, references pb-ship

### Status

- 62 commands across 10 categories
- Complete session management (pause ↔ resume)
- Complete shipping workflow (reviews → PR → release)
- All quality gates passing

---

## [v1.5.1] - 2026-01-17

### Added

**Thinking Partner Commands**
- Added 3 new commands establishing Claude as a self-sufficient thinking partner:
  - `/pb-query` — Multi-pass query processing (draft → critique → refine) for expert-quality answers
  - `/pb-ideate` — Divergent exploration with 6 lenses for option generation (10+ options before evaluating)
  - `/pb-synthesize` — Integration mode for combining multiple inputs into coherent, actionable insight

**Thinking Partner Stack**
- Complete cognitive mode framework:
  - Divergent: `/pb-ideate` (explore options)
  - Integration: `/pb-synthesize` (combine insights)
  - Adversarial: `/pb-preamble` (challenge assumptions)
  - Convergent: `/pb-plan`, `/pb-adr` (decide and structure)
  - Refinement: `/pb-query` (polish output)

### Documentation

- Updated README: Added thinking partner commands to Core Foundation (now 7 commands)
- Updated command-index: Added Thinking Partner section with stack diagram
- Updated integration-guide: Command count 55→60, added Cluster 9 (Thinking Partner)

### Status

- 60 commands across 10 categories
- Complete thinking partner methodology
- All quality gates passing

---

## [v1.5.0] - 2026-01-12

### Added

**Design Rules Framework Integration**
- Integrated 17 classical design rules as foundational technical framework alongside Preamble
- Created `/pb-design-rules.md` (23KB) with complete design rules philosophy
  - 4 clusters organizing 17 rules: Clarity, Simplicity, Resilience, Extensibility
  - Decision framework for rule trade-offs
  - 5 real-world implementation examples
- Created `/docs/design-rules-quick-ref.md` for daily reference lookup
  - Quick table of all 17 rules
  - Decision tree for which rules apply when
  - Trade-off matrix for conflicting rules
  - Failure mode diagnosis

**Framework Integration Across 50+ Commands**
- Updated all 51 command files to reference Design Rules
- Every command now explicitly shows which design rules apply to its domain
- Integration across all command categories:
  - Core commands (4): Added design rules context
  - Planning commands (10): Show design rules for architectural decisions
  - Development commands (9): Design rules checks in iteration cycle
  - Deployment commands (2): Simplicity vs Robustness trade-offs
  - Release commands (1): Robustness and clarity in release process
  - Review commands (10): Design rules language for code review
  - Repository commands (6): Clarity and representation rules
  - People commands (3): Technical excellence + psychological safety
  - Templates (1): Design rules in onboarding context

**Documentation Enhancement**
- Enhanced README.md to prominently feature both Preamble and Design Rules
  - Reframed overview to present two complementary frameworks
  - Updated key capabilities to show which framework enables each one
  - Restructured principles section to show integration
  - New principle: Preamble + Design Rules enable autonomy + soundness
- Enhanced docs/index.md as documentation site home
  - Dual framework introduction with equal prominence
  - New section: "The Two Frameworks Enable Each Other"
  - Detailed explanation of how frameworks complement each other
  - Updated all 5 key principles to show both framework perspectives
  - New 6th principle: Integration as one system
- Updated mkdocs.yml site description to reference both frameworks
- Enhanced working context (todos/1-working-context.md) development guide

### Documentation

- Added comprehensive design rules reference guide for daily use
- Enhanced project README to show complete philosophy (Preamble + Design Rules)
- Updated documentation site home to feature both frameworks
- All command documentation now reference applicable design rules

### Mission Alignment

- Clarified core mission: "Complete framework for development workflows, anchored in peer collaboration (Preamble) and technical design principles (Design Rules)"
- Verified every command embodies both frameworks
- Both frameworks now visibly foundational across all entry points (README, docs, mkdocs)

### Status

- 50+ commands across 9 categories
- Complete Preamble + Design Rules integration
- Production-ready documentation
- All quality gates passing

---

## [v1.4.1] - 2026-01-12

### Fixed

**CI/CD & Automation**
- Updated GitHub Actions artifact actions from v3 to v4 for compatibility
- Made CI/CD workflow more resilient to metadata extraction warnings
- Disabled redundant `validate-metadata` workflow, consolidated to `deploy-docs` only
- Added `scripts/` directory to deployment workflow trigger paths
- Enhanced `deploy-docs` triggers to include README.md and script changes

**Scripts & Quality**
- Resolved f-string syntax error in `generate-quick-ref.py` script
- Improved metadata extraction robustness to handle field errors gracefully
- Corrected markdown linting error in `/pb-what-next.md` command

**Documentation**
- Updated mkdocs site description from 45 to 47 commands
- Improved documentation formatting to fit YAML line length requirements

### Status

- All v1.4.0 features stable and production-ready
- CI/CD pipeline optimized and resilient
- No breaking changes; patch-level fixes only

---

## [v1.4.0] - 2026-01-12

### Added

**Context-Aware Command Discovery**
- `/pb-what-next` command for intelligent playbook recommendations
  - Analyzes git state (branch, changed files, commits)
  - Detects workflow phase (START, DEVELOP, FINALIZE, REVIEW, RELEASE)
  - Generates ranked recommendations with confidence scores (0.6-1.0)
  - Provides time estimates and reasoning for each recommendation
  - Support for verbose mode showing detailed analysis traces

**Metadata Extraction & Validation Pipeline** (Phases 1-2)
- Automated metadata extraction from command markdown files
- Confidence scoring system (89% average) for extraction quality
- Validation rules with quality gates (0.80 minimum threshold)
- Quick-reference generator for workflows and decision trees
- JSON metadata structure driving all discovery tools

**CI/CD Automation Workflow**
- `.github/workflows/validate-metadata.yml` for automated quality gates
- Multi-stage pipeline: Extract → Validate → Generate → Report
- Quality metrics reporting with per-field confidence breakdown
- Automatic quick-reference generation on every push to main
- Failure blocking for deployments when quality gates not met

**Production Quality Enhancements**
- Comprehensive unit tests (`tests/test_analyze_context.py`): 17 test classes, 80%+ coverage
  - Git state analysis, workflow phase detection, file type categorization
  - Recommendation generation, confidence scoring, output formatting
  - Error handling for edge cases (missing files, invalid JSON, git failures)
- Enhanced documentation for `/pb-what-next` with real-world examples
  - 4 workflow scenarios (START/DEVELOP/FINALIZE/RELEASE phases)
  - Output interpretation guide, troubleshooting section, tips & best practices
  - Expanded from 217 to 451 lines (+234 lines)
- Code consolidation and cleanup
  - Created `scripts/playbook_utils.py` for shared utilities
  - Eliminated 519+ lines of code duplication across 4 scripts
  - Unified logging, metadata loading, and constants management
  - Reduced maintenance burden and improved consistency

### Documentation

- Enhanced `/commands/development/pb-what-next.md` with comprehensive usage guide
- Added `.playbook-metadata.json` for command metadata reference
- Added `.playbook-quick-ref.md` auto-generated quick reference guide
- Added `/docs/metadata-extraction.md` for metadata extraction and authoring guide
- Phase review documents: `todos/PHASE3-REVIEW.md`, `todos/PHASE4-REVIEW.md`
- Pre-release cleanup review: `todos/PRE-RELEASE-CLEANUP.md`

### Fixed

- Updated `.gitignore` with Python cache patterns (`__pycache__/`, `*.py[cod]`, `.pytest_cache/`, etc.)
- Consolidated error handling across all Python scripts
- Fixed incomplete command references in pattern guides
- Corrected script imports for consistency
- Removed temporary build artifacts from repository

### Testing

- 17 test classes covering all `/pb-what-next` functionality
- 40+ test methods with parametrized test scenarios
- Mock-based testing for git commands (no repository dependencies)
- Edge case coverage: missing files, invalid JSON, git failures, timeouts
- Syntax validation: All tests compile and ready for pytest execution
- Target: 80%+ pragmatic coverage (critical paths + workflows + error handling)

### Performance & Quality

- All scripts tested and working correctly
- Metadata extraction completes in <1 second
- Validation reports generated with detailed confidence metrics
- No security issues found (no hardcoded credentials or secrets)
- No duplication remaining (consolidation reduced by 379 lines)
- Repository ready for production use

## [v1.3.0] - 2026-01-12

### Added
- **Example Projects**: Three complete, production-ready examples demonstrating playbook patterns:
  - Go Backend API (Go 1.22 + PostgreSQL): REST API with connection pooling, graceful shutdown, table-driven tests
  - Python Data Pipeline (Python 3.11 + SQLAlchemy): Async event processing pipeline with aggregation
  - Node.js REST API (Node.js 20 + TypeScript): Type-safe Express API with request tracing and structured logging
- **Playbook in Action Guide**: Comprehensive walkthrough (`docs/playbook-in-action.md`) showing:
  - Real-world workflows using `/pb-start`, `/pb-cycle`, `/pb-pr` with three example projects
  - Step-by-step development scenarios and common patterns
  - Testing, code quality, and deployment strategies for each stack
- **Example Integration**: Updated command-index with references to example projects
- **Project Templates**: Complete Dockerfile, docker-compose, Makefile, and documentation templates

### Documentation
- Added `docs/playbook-in-action.md`: Real-world playbook usage guide with complete examples
- Updated `docs/command-index.md`: Added Example Projects section with links and quick reference
- Each example project includes comprehensive README and DEVELOPMENT.md guides

### Fixed
- Go Backend API: Updated to Go 1.22 for PathValue support in HTTP routing
- Node.js API: Added missing TypeScript type definitions (@types/pg, @types/uuid, @types/supertest)
- Node.js API: Updated npm ci syntax to --omit=dev for production builds
- All examples: Validated with docker-compose, endpoints tested and working

### Validation
- All 3 example projects tested with docker-compose
- Go Backend API: Health check and CRUD endpoints verified
- Node.js API: TypeScript compilation and test suite passing
- Python Pipeline: Async pipeline execution validated
- Total: 5375+ lines of code and documentation across 28 new files

### Deferred to v1.3.1
- GitHub Discussions community infrastructure
- Community contribution guidelines (`/docs/community.md`)
- Case study templates and community project showcase
- Additional documentation and integration examples

## [v1.2.1] - 2026-01-11

### Added
- **Release Automation**: `scripts/release.sh` for automated version management and git tagging
- **Git Configuration**: `.gitattributes` for consistent line ending normalization (LF)
- **Command Structure Guidelines**: Enhanced `CONTRIBUTING.md` with detailed command creation standards

### Documentation
- Added command structure requirements: title, overview, sections, examples, checklists
- Added linting standards and formatting guidelines for command files
- Added pre-submission checklist for contributors
- Added example command template

### Changed
- Extended CI/CD pipeline (`.github/workflows/deploy-docs.yml`) to validate both `docs/` and `commands/` directories
- Enhanced contributor documentation with command structure expectations

### Fixed
- Established line ending normalization via `.gitattributes` to prevent CRLF issues across platforms

## [v1.2.0] - 2026-01-11

### Added
- **Pattern Library**: 4 pattern family commands (async, core, database, distributed)
- **Structured Implementation**: `pb-todo-implement` with checkpoint-based review
- **Knowledge Transfer**: `pb-knowledge-transfer` for team handoff
- **Logging Standards**: `pb-logging` for audit and compliance
- **Documentation Pipeline**: Mkdocs + GitHub Pages deployment
- **CI/CD Integration**: Automated lint, build, and deploy workflow

### Fixed
- Resolved duplicate `/pb-incident.md` (kept deployment version, deleted release version)
- Recategorized `/pb-knowledge-transfer` from Team & Growth to Development
- Removed broken INTEGRATION-SUMMARY.md reference

### Changed
- Removed emojis from all playbook commands for text-only style
- Updated command count references for dynamic flexibility

### Documentation
- Created `.github/CONTRIBUTING.md` with contribution guidelines
- Published docs site at https://vnykmshr.github.io/playbook/
- Added command-index, integration-guide, decision-guide, workflows, faq, best-practices, checklists, glossary

## [v1.1.0] - Earlier

- Initial release with 25 core commands

---

## How to Update This File

When releasing a new version:

1. Add new section at top: `## [vX.Y.Z] - YYYY-MM-DD`
2. Use these categories as needed:
   - **Added**: New features/commands
   - **Changed**: Modifications to existing commands
   - **Fixed**: Bug fixes and corrections
   - **Removed**: Deleted commands or features
   - **Deprecated**: Commands marked for removal in future versions
   - **Documentation**: Docs-only changes
   - **Security**: Security-related fixes

3. Keep "Unreleased" section at top for in-progress work (remove when releasing)

4. Link versions at bottom: `[vX.Y.Z]: https://github.com/vnykmshr/playbook/releases/tag/vX.Y.Z`

---

[v2.7.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.7.0
[v2.6.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.6.0
[v2.5.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.5.0
[v2.4.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.4.0
[v2.3.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.3.0
[v2.2.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.2.0
[v2.1.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.1.0
[v2.0.0]: https://github.com/vnykmshr/playbook/releases/tag/v2.0.0
[v1.8.0]: https://github.com/vnykmshr/playbook/releases/tag/v1.8.0
[v1.7.0]: https://github.com/vnykmshr/playbook/releases/tag/v1.7.0
