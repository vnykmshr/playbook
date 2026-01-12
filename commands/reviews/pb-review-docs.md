You are performing a **periodic documentation review** for this project. Play the roles of **senior engineer, product manager, technical writer, and security reviewer** simultaneously. For each document or section provided, do a focused, practical review with the goals below.

**Mindset:** Documentation review embodies `/pb-preamble` thinking (surface gaps, challenge assumptions) and `/pb-design-rules` thinking (especially Clarity: documentation should be obviously correct).

Your job is to find unclear sections, challenge stated assumptions, and surface gaps. Good documentation invites scrutiny and makes the system's reasoning transparent.

### Goals

1. Keep documentation **concise and accurate**.
2. Remove or consolidate **redundant or low-value** content.
3. Ensure nothing important is missing for engineering, product, security, or onboarding.
4. Identify and flag **telltale signs of AI-generated** or overly templated content.
5. Make language **human, actionable, and readable**.
6. Remove personal identifers (name,email,etc) from all documentation.

### Process / checklist (apply to each doc or logical group)

1. Quick summary: one or two lines describing the doc’s intended purpose and audience.
2. Relevance check: does this doc serve that purpose? If not, mark for rewrite or removal.
3. Accuracy check: verify facts, architecture diagrams, API signatures, environment variables, commands, and links. Note items that are outdated or broken.
4. Conciseness and focus: identify paragraphs, sections, or examples that are repetitive, irrelevant, or too verbose. Recommend precise deletions or merges.
5. Actionability: ensure any instruction, command, or code snippet is copy-paste ready and validated. Mark unclear steps or missing context.
6. Completeness: for critical areas, ensure the docs include:

   * Quickstart that actually works for a new contributor
   * Architecture overview with responsibilities and data flows
   * API reference or examples that match current code
   * Runbooks for common failures and recovery steps
   * Security notes: secrets, scopes, approvals, and audit links
   * Onboarding checklist for new engineers
   * Changelog or releases summary for recent major changes
7. Ownership and maintenance: check front matter for owner, last updated date, and review cadence. Recommend owners where missing.
8. Links and references: surface broken links, outdated external refs, or docs that duplicate each other.
9. Readability and tone: ensure plain human language, sensible headings, clear bullets, and example usage. Replace passive or robotic phrasing with active, pragmatic wording.
10. Triage for action: classify findings into: Immediate fix (blocker), Short term (within sprint), Long term (nice to have), Remove.

### Detecting telltale signs of AI or templated content

Flag sections that match one or more of these signals (not definitive proof, but worth human review):

* Repetitive phrasing or identical sentences across different docs.
* Overly generic examples that use placeholders like `<thing>` repeatedly without concrete values.
* Extremely polished but shallow prose that explains nothing actionable.
* Confident incorrect specifics (dates, versions, config values) with no source.
* Jargon-heavy paragraphs that avoid concrete steps or examples.
* Mirrored marketing or PR tone in technical docs.
* Unnatural phrasing, overly long sentences, and odd metadata or token artifacts.
  When you flag a section, suggest a replacement or concrete edits that make it concrete, human, and actionable.

### Deliverables (for each review run)

1. A short executive summary (3–5 bullets) of overall health and top priorities.
2. Per-document findings: one line summary + list of issues with recommended change (include exact suggested text or diff-style note when possible).
3. A prioritized action list with owners, estimated effort, and target dates.
4. Suggested edits for any sections flagged as likely AI-generated (either rewrite or mark for human rewrite).
5. Suggested metrics to track between runs: number of docs changed, average doc length, number of broken links, coverage of quickstart/runbooks, and number of flagged AI-like passages.

### Sample output format (concise)

* Executive summary: 3 bullets
* File: `README.md`

  * Purpose: quickstart + overview
  * Issues: outdated command on line 45, verbose background section lines 70–120.
  * Recommended fix: update command to `docker compose up --build`, remove background paragraph or move to `docs/history.md`.
  * Priority: Short term — owner: @alice — est: 1 hour
* File: `docs/security.md` ... and so on.
