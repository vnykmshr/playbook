---
name: "pb-voice"
title: "Voice Review"
category: "reviews"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-think', 'pb-review-docs', 'pb-documentation', 'pb-design-rules', 'pb-preamble']
last_reviewed: "2026-04-26"
last_evolved: "2026-04-26"
version: "2.2.0"
version_notes: "v2.2.0: Reference global GitHub Artifact Register rule for review-comment register."
breaking_changes: ["Detection categories expanded from 11 to 12", "Step 0 (Register Calibration) added before Category 1", "Persona file now loaded in Step 0 (before detection) instead of Stage 2 (rewrite)"]
---
# Voice Review

**Purpose:** Detect and remove AI writing patterns from prose. Two roles, clearly separated: the tool removes tells, the author adds truth.

**Mindset:** Apply `/pb-preamble` thinking (honest, imperfect prose over polished output) and `/pb-design-rules` thinking (Clarity over cleverness. Silence when nothing to say. Fail noisily: if text reads generated, flag it, don't smooth it over).

**Resource Hint:** sonnet - Structured text analysis and surgical editing; pattern recognition, not architecture-level depth.

You are a detection system and a surgical editor. Find where AI shows through and fix only those spots, without introducing new mechanical patterns.

---

## When to Use

- **After persona-driven generation** - You wrote "create post on X as [author]-persona"; now run pb-voice as the quality gate to catch residual AI patterns the persona didn't suppress
- **Before publishing** - Final pass on blog posts, articles, social posts
- **When text "feels off"** - Too smooth, too balanced, too clean
- **Building a voice profile** - Extract patterns from your own writing samples

## Recommended Workflow

The best results come from persona + pb-voice together, not either alone:

```
1. Generate with persona:  "Write about X as [author]-persona"
   Or: /pb-voice persona=my-persona.md
   Persona drives voice, vocabulary, opinions during generation.

2. Quality gate with pb-voice:  "/pb-voice" on the output
   pb-voice catches residual AI patterns the persona didn't suppress.
```

**Why this order matters:** A persona embeds voice from the start (word choice, opinions, rhythm). pb-voice is the safety net that catches where the model slipped despite persona instructions. Using pb-voice *without* a persona can remove tells but can't add the author's actual voice. Using a persona *without* pb-voice lets subtle AI patterns through.

**Anti-pattern:** Don't generate generic content and then try to "humanize" it with pb-voice alone. That produces generic-minus-tells, not human writing.

---

## Pipeline Overview

```
Input  DETECT  annotated flags  REWRITE (flagged only)  VERIFY  output
```

### Modes

| Mode | What It Does | When to Use |
|------|-------------|-------------|
| `detect` | Flag AI patterns, score text, no changes | Quick audit, learning your tells |
| `fix` (default) | Detect + rewrite flagged sections only | Standard post-processing |
| `profile` | Analyze sample writing to build voice reference | One-time setup or periodic refresh |

**Usage:**

- `/pb-voice` - Full detect + fix on provided text or file
- `/pb-voice mode=detect` - Detection and scoring only
- `/pb-voice mode=profile` - Build voice profile from samples
- `/pb-voice persona=/path/to/persona.md` - Calibrate to author voice

Companion script: `scripts/voice-review.sh` (run `--help` for usage).

---

## Stage 1: Detect

Scan text for AI-generated patterns. Flag each occurrence with category and severity. Do not fix anything in this stage.

### Step 0: Register Calibration

Before running any detection category, determine what register the text should be in. The same phrase can be correct in one context and a tell in another.

**When persona is provided:** Read the persona file. Extract:
- **Target register:** conversational, technical, formal, or observational
- **Formality ceiling:** the most formal phrasing this persona would naturally use
- **Vocabulary anchors:** actual phrases from the persona's texture samples

**When context is provided (PR, issue, bug report, email, social post):** Infer register from the format:

| Format | Register | Formality ceiling |
|--------|----------|-------------------|
| Social post (LinkedIn, X, Bluesky) | conversational | spoken language |
| PR description / issue comment | dev-to-dev | how you'd explain it at a whiteboard |
| Bug report / security advisory | technical | precise but not academic |
| Blog post / article | depends on persona | check persona file |
| RFC / architecture doc | formal | technical writing norms apply |
| Email to maintainer | dev-to-dev | how you'd write to a colleague |

**When neither is provided:** Default to MEDIUM formality. Skip Category 12 (Register Mismatch).

**Output:** State the detected register at the top of your detection report: "Register: conversational (from persona)" or "Register: dev-to-dev (PR description)". This makes the calibration visible and challengeable. Each detection category documents its own register sensitivity where applicable.

**Voice Profile:** If a persona file is provided, load it now -- before detection, not after. The persona's vocabulary anchors and formality ceiling inform what counts as a tell across all categories. See "Voice Profile Integration" in Stage 2 for how the persona also calibrates rewrites.

### Category 1: Dead Giveaway Vocabulary (HIGH)

Words and phrases that almost never appear in natural writing but are statistically overrepresented in LLM output.

**Words:** delve, utilize, leverage, foster, robust, comprehensive, nuanced, streamline, facilitate, underscores, pivotal, multifaceted, holistic, synergy, paradigm, ecosystem (outside tech), landscape (metaphorical), tapestry, intricate, embark, unleash, realm, testament, cornerstone, spearhead, bolster, resonate, proliferate, aligns, crucial (outside technical context), garment, enduring, showcase, interplay, vibrant, vital

**Phrases:**

- "It's worth noting that..." / "It's important to note..."
- "In today's [X] landscape..."
- "Let's dive into..." / "Let me walk you through..."
- "This is a game-changer" / "Take it to the next level"
- "Stands as a testament to" / "Plays a crucial role"
- "In order to" (where "to" suffices)
- "Whether you're [X] or [Y]..." / "By doing [X], you can [Y]..."
- "In this article, we will..." / "Without further ado"
- "Moving forward" / "At the end of the day"

**Note:** Context can reduce severity. In technical writing (RFCs, architecture docs), "robust" and "leverage" may be legitimate (reduce to MEDIUM). Similarly, Category 3's "significance inflation" may be appropriate in historical writing, and Category 9's em-dashes may suit some style guides. When in doubt, check against the author's voice profile or project rules.

**Action:** Flag every occurrence. Replace or delete.

### Category 2: Structural Tells (HIGH)

Document-level organization patterns that reveal algorithmic generation. (For inline formatting tells, see Category 9.)

- **Uniform paragraph length** - Every paragraph 3-4 sentences. Real writing has 1-sentence paragraphs next to 6-sentence ones.
- **Topic-support-transition** - Each paragraph opens with topic sentence, supports it, transitions. Textbook structure. Real writing meanders.
- **Lists of exactly 3** - AI loves triplets. "Three key considerations..." Real lists are 2, or 4, or 7.
- **Symmetrical sections** - All H2s same length. All bullets identical grammar.
- **Colon introductions** - "Several factors to consider: X, Y, and Z."
- **Parallel openings** - Consecutive paragraphs starting the same way ("This approach...", "This method...", "This strategy...").

**Action:** Restructure. Make one paragraph a fragment. Make another twice as long. Break the template.

### Category 3: Content-Level Patterns (HIGH)

Sentence-construction habits and repetition patterns that go beyond individual words.

- **Copula avoidance** - "serves as" / "stands as" / "functions as" instead of "is." AI substitutes elaborate constructions for simple verbs. "Gallery 825 serves as the exhibition space"  "Gallery 825 is the exhibition space."
- **Significance inflation** - Puffing up importance with legacy/testament/pivotal framing. "Marking a pivotal moment in the evolution of..." The whole sentence construction inflates, not just the word.
- **Superficial -ing clauses** - Present participle phrases tacked on for fake depth: "highlighting the interplay," "underscoring the importance," "reflecting the community's values." The -ing clause adds no information; it just sounds analytical.
- **Synonym cycling** - Repetition-penalty-driven substitution. "The protagonist... The main character... The central figure... The hero..." all in one paragraph. Real writers repeat or use pronouns.
- **Negative parallelisms** - "Not only X but Y" / "It's not just about X; it's about Y." Overused construction that sounds profound but usually restates.
- **False ranges** - "from X to Y" where X and Y aren't on a meaningful scale. "From hobbyist experiments to enterprise-wide rollouts."
- **Explanatory completeness** - The model can't leave anything unexplained. If it mentions a concept, it defines it. A person writing to peers assumes shared context. "Claude's project files" is enough -- the model adds "which allow you to store persistent context for your projects." If the audience already knows, the explanation is a tell.
- **Clause-final summation** - Restating the point in abstract terms at the end of a sentence. "...which makes it ideal for teams that need both speed and reliability." "...providing a robust foundation for future development." The clause after "which" or the participial phrase adds no information. People end sentences on the specific, not the abstract.

**Action:** Simplify. Use "is"/"are." Delete -ing clauses that add no information. Let a word repeat rather than cycling synonyms. Replace false ranges with specifics. Delete explanations the audience doesn't need. Cut clause-final summations.

### Category 4: Hedging Density (MEDIUM)

AI hedges constantly to avoid being wrong. Humans hedge strategically, only when genuinely uncertain.

- More than 2 hedges per paragraph: "may," "might," "could potentially," "it's possible that"
- Qualifying needlessly: "This can be useful" vs "This is useful"
- Double hedges: "might potentially," "could possibly," "may help to some extent"
- Preemptive disclaimers: "While this isn't always the case..."

**Action:** Replace one hedge per paragraph with a direct statement. Keep hedges only where real uncertainty exists.

### Category 5: Transition Formality (MEDIUM)

Stock transitions humans rarely use in professional writing.

**Flag:** Moreover, Furthermore, Additionally, In conclusion, To summarize, That said, Having established, It is worth mentioning, Consequently, Subsequently, Notably, Importantly, Interestingly, Conversely, Nevertheless, Notwithstanding

**Action:** Delete most. If connection needed, use "But," "And," "So," "Still," or restructure.

### Category 6: Enthusiasm and Communication Artifacts (HIGH)

AI is trained helpful and positive. This creates distinctive filler. Also catches chat-generated text pasted as content.

- **Affirmations:** "Great question!", "Absolutely!", "That's a fantastic approach", "You're absolutely right!"
- **Preamble:** "I'd be happy to help with that," "Let me break this down"
- **Conclusion padding:** "I hope this helps!", "Feel free to ask", "Let me know if you'd like me to expand"
- **Excitement inflation:** "exciting," "powerful," "amazing," "groundbreaking" for mundane things
- **Sycophantic tone:** "That's an excellent point," "Great observation"
- **Knowledge disclaimers:** "As of my last update," "While specific details are limited"

**Action:** Delete entirely. Zero information content.

### Category 7: Rhythm and Cadence (MEDIUM)

AI produces unnaturally even rhythm.

- **Consistent sentence length** - Every sentence 15-25 words. No short punches. No long sprawls.
- **Clean clause structure** - Subject-verb-object, consistently. No interruptions or asides.
- **No fragments** - AI almost never writes incomplete sentences. Humans do it constantly.
- **No contractions** - "It is" instead of "it's." "Do not" instead of "don't."
- **Over-complete thoughts** - Every idea fully resolved in one sentence. No trailing thoughts.

**Action:** Vary length deliberately. Let a thought stand incomplete. Contract where natural. Let a thought trail off.

### Category 8: Abstraction Level (MEDIUM)

AI defaults to conceptual language. Humans anchor in specifics.

- **No concrete nouns** - Paragraph has no numbers, names, tools, dates, or places
- **Generic examples** - "For instance, in many organizations..." instead of naming one
- **Conceptual hand-waving** - "Improves efficiency" without saying how much or for whom
- **Category language** - "Various factors," "multiple considerations," "several approaches"
- **Precise-sounding vagueness** - Modifiers that sound specific but say nothing. "Significantly faster," "substantially improved," "considerably more efficient." The concrete nouns might be there, but the quantifiers are empty. How much faster? Compared to what?

**Action:** One concrete anchor per paragraph. A number, tool, date, name, or constraint from lived experience. Replace vague quantifiers with actual measurements or drop them.

### Category 9: Style and Formatting Tells (HIGH)

Formatting patterns that are quick to spot and high-signal.

- **Em-dash overuse** - AI uses em dashes (--) more than humans, mimicking punchy sales writing. Use commas, periods, parentheses, or restructure instead.
- **Boldface overuse** - Mechanical emphasis on key terms. "It blends **OKRs**, **KPIs**, and **BSC**." Remove most bold; let sentence structure do the emphasis.
- **Inline-header vertical lists** - Bullet points starting with bolded headers followed by colons. "- **Speed:** Significantly faster..." Restructure into prose or use plain bullets.
- **Title case in headings** - AI capitalizes all main words. "## Strategic Negotiations And Global Partnerships"  "## Strategic negotiations and global partnerships." Use sentence case.
- **Emoji decoration** - Emojis on headings or bullet points. Delete.
- **Curly quotation marks** - AI sometimes uses curly quotes instead of straight quotes. Normalize.

**Action:** Fix on sight. These are fast, high-confidence corrections.

**Note:** Some tells (em-dashes, title case) have legitimate uses in specific style guides. When a project style guide explicitly allows them, reduce severity to LOW. When voice-guidelines or project rules ban them outright, treat as HIGH regardless of context.

### Category 10: Summary Endings (HIGH)

The most reliable AI tell. LLMs almost always end with a summary paragraph restating what was already said.

- "In summary, ..."
- "To conclude, ..."
- "Overall, ..."
- Final paragraph adds no new information
- Restatement of the opening thesis
- Generic positive conclusion: "The future looks bright," "Exciting times lie ahead"

**Action:** Delete the summary paragraph. End on the last substantive point. Unresolved endings, open questions, abrupt stops are all fine.

### Category 11: Formulaic Sections (MEDIUM)

AI-generated articles include predictable section patterns.

- **"Challenges and Future Prospects"** - Formulaic challenges section followed by optimistic outlook. "Despite its... faces several challenges. Despite these challenges... continues to thrive."
- **"Broader Trends"** - Connecting a specific topic to vague broader significance. "This represents a broader shift in..."
- **Undue notability claims** - Listing media coverage or followers without context.

**Action:** Replace with specific facts. What challenges, specifically? What happened, specifically? If there's nothing specific to say, the section doesn't need to exist.

### Category 12: Register Mismatch (HIGH when register is set)

Phrases that are technically correct but wrong for the target register. This is the gap between "grammatically fine" and "sounds like a person wrote it." Only active when Step 0 has set a register. Category 1 flags words that are almost always AI tells regardless of register. Category 12 flags words that are fine in some registers but wrong in the target register. If a word is on the Category 1 list, flag it there, not here.

- **Compound nominal phrases** - Stacking nouns into noun phrases that nobody says out loud. "The personal agent ecosystem evaluation" instead of "testing personal agents." "A multi-channel messaging integration layer" instead of "a way to get messages from different apps." The longer the noun stack, the stronger the tell.
- **Nominalized verbs** - Turning verbs into abstract nouns. "The implementation of caching" instead of "implementing caching" or just "adding a cache." "Facilitation of communication" instead of "helping people talk." If the verb form is shorter and clearer, use it.
- **Category/framework language** - Imposing taxonomic structure where the author would just describe things. "The authentication subsystem" instead of "the login code." "A persistence layer" instead of "where we store things." "Requirements matrix" instead of "checklist." Technical categories are fine in RFCs and architecture docs. In a social post or PR description, they signal the model is organizing, not talking.
- **Register-inappropriate passive** - Passive voice that's correct in formal/technical registers but wrong for conversational. "The decision was made to sunset the feature" reads like a press release. "We dropped the feature" is dev-to-dev. "I killed it" is conversational. Passive is fine in RFCs and architecture docs. In a social post or PR, it distances the author from the action.
- **Textbook phrasing** - Correct terminology that nobody uses in the target register. "Persistent memory across interactions" instead of "remembering things between conversations." "Natively supports" instead of "works out of the box." "Mediocre at both tasks" instead of "okay at both and great at neither." The test: would you say this exact phrase to a colleague at a whiteboard? If not, it's textbook.

**How register affects severity:**
- Conversational (social posts, casual writing): HIGH. Every instance should be caught and rewritten.
- Dev-to-dev (PRs, issues, emails to maintainers): MEDIUM. Some technical shorthand is natural. Flag only when it reads more like a paper than a conversation.
- Technical (bug reports, security advisories): LOW. Precise terminology is expected. Flag only obvious over-formalization.
- Formal (RFCs, architecture docs): Skip. This category doesn't apply.

**Action:** Replace with the phrase the author would actually say. Read it out loud. If it sounds like a textbook, a slide deck, or a product brief, it's wrong for conversational register.

### Score Calibration

| Score | Category Flags | Description |
|-------|---------------|-------------|
| 1-2 | 6+ categories flagged, multiple HIGH | Dead giveaways in every paragraph, summary ending, no specifics, uniform structure |
| 3-4 | 4-5 categories flagged, 2+ HIGH | Structural tells dominate, giveaway vocab present, uniform hedging |
| 5-6 | 2-3 categories flagged, 0-1 HIGH | Reads okay on first pass, but pattern tells accumulate across paragraphs |
| 7-8 | 1-2 categories flagged, 0 HIGH | Individual tells only, most text is natural, voice present throughout |
| 9-10 | 0 categories flagged | No detectable patterns, distinct voice, could not be flagged by a reader |

**Target:** Score 7+ before publishing. Score 5-6 is acceptable for internal drafts. Below 5 needs another rewrite pass. A single HIGH flag caps the score at 6 regardless of other factors.

---

## Stage 2: Rewrite

Fix only flagged sections. Preserve everything else verbatim.

### Editing Rules

**Rule 0: Do not add ideas.** Subtraction and restructuring only. If the author didn't say it, don't introduce it.

**Rule 1: Cut first.** Most AI text is 20-40% longer than needed. Removing padding, filler transitions, and summary paragraphs is the highest-leverage edit. If cutting a sentence loses no meaning, cut it.

**Rule 2: Reclaim author phrasing.** If the original draft had a rougher but more genuine phrase, prefer it. The AI "improved" it by making it generic.

**Rule 3: Break structural patterns.** If three consecutive paragraphs follow the same shape, restructure one. Make a paragraph a single sentence. Let another run long.

**Rule 4: Flag missing anchors.** If a paragraph has no concrete detail (number, tool, date, name), flag it for the author to fix. Do not fabricate specifics, only the author has lived experience to draw from.

**Rule 5: Vary rhythm.** Short sentence. Then a longer one that takes its time. Fragment. Back to medium.

**Rule 6: Simplify verbs.** "Serves as" becomes "is." "Stands as" becomes "is." Use simple copulas.

**Rule 7: Contractions are natural.** "It's" not "It is." "Don't" not "Do not." Unless formality is specifically required.

**Rule 8: Kill the ending.** If the last paragraph is a summary, delete it. End on the last point that adds information.

### Voice Profile Integration

When a persona file is provided, calibrate rewrites to match the author's documented voice.

1. **Read the persona** - Extract sentence patterns, vocabulary, punctuation habits, tone markers
2. **Identify signatures** - What makes this author recognizable? Comma-connected thoughts? Programming metaphors? Trailing endings?
3. **Apply during rewrite** - Match the author's patterns, not generic "human" patterns
4. **Preserve looseness** - If the voice is informal and unpolished, don't tighten. The looseness is the voice.

If no persona provided, apply general human-voice heuristics without author-specific calibration.

### What the Author Brings

These are things no detection tool can supply - only the author has them:

- **Opinions** - React to facts. "I genuinely don't know how to feel about this" signals a real person thinking.
- **Lived-experience details** - Specific tools, dates, numbers, project names from memory. Not "many organizations" but "the team I was on in 2023."
- **Uncertainty acknowledged honestly** - "I can't verify this works at scale" beats false confidence.
- **Mixed feelings** - Real humans have them. "This is impressive but also kind of unsettling" beats simple praise or criticism.
- **Unresolved thoughts** - Not every paragraph needs a clean conclusion. Let a thought trail off if it's genuinely unresolved.

When flagging missing anchors (Rule 4), prompt the author for these. The rewrite can remove AI patterns, but only the author can inject the signal that makes prose recognizably theirs.

### What NOT to Do

| Don't | Why |
|-------|-----|
| Rewrite unflagged sections | Introduces new mechanical patterns |
| Add content | You're an editor, not a writer |
| Over-correct into "quirky" | Forced imperfection is as detectable as AI smoothness |
| Remove all structure | Break patterns, don't eliminate organization |
| Add slang unless voice is genuinely informal | Unnatural informality is a tell too |
| Touch technical content | Facts, code, specs: leave alone |

---

## Stage 3: Verify

After rewriting, validate the output.

### Checks

1. **Re-score** - Run detection on rewritten text. Score should improve by at least 2 points.
2. **Two-pass audit** - Ask: "What still makes this obviously AI-generated?" Answer honestly, then fix the remaining tells. This meta-cognitive step catches patterns that category-by-category detection misses.
3. **Read-aloud test** - The primary check for conversational registers. Read the text out loud (or simulate it). For each sentence, ask: "Would the author say this exact phrase to a colleague?" Not the idea -- the exact words. "Persistent memory across interactions" fails. "Remembering things between conversations" passes. If the register is conversational and a sentence sounds like a textbook, a slide deck, or a product brief, it's still a tell. For technical or formal registers, the bar is different: precision matters more than conversational flow.
4. **Meaning preservation** - Every claim in the original survives in the output.
5. **Length check** - Output should be shorter than input (typically 10-30% shorter). Longer means something went wrong.

---

## Examples

### Example 1: Blog Post Opening

**Input:**

```
In today's rapidly evolving tech landscape, developers are increasingly
leveraging AI tools to streamline their workflows. It's worth noting that
while these tools offer comprehensive capabilities, they may not always
align with individual coding styles. In this article, we'll delve into
practical strategies for maintaining your unique voice while utilizing
AI assistance effectively.
```

**Detection:** Score 2/10. Eight Category 1 flags (vocabulary), plus structural tells (colon pattern, hedging, no contractions).

**Output:**

```
I've been using AI tools for most of my writing this past year. They're
fast. They're also making everything sound the same. Grammar gets better,
sure, but my posts read like a committee wrote them.
```

Score: 2/10  8/10. Shorter. Specific. Has a voice.

### Example 2: Technical Paragraph

**Input:**

```
When implementing microservices architecture, it is essential to consider
several key factors. First, service boundaries should be carefully defined
to ensure proper separation of concerns. Second, inter-service communication
patterns must be robust and resilient. Third, monitoring and observability
should be comprehensive to facilitate troubleshooting.
```

**Detection:** Score 3/10. "Robust," "comprehensive," list-of-3 structure, no contractions, no concrete detail.

**Output (with persona):**

```
Microservices get messy at the boundaries. Where one service ends and
another begins, that's where most teams burn months. We got this wrong
twice before settling on domain events as the contract. Monitoring matters
too, but get the boundaries right first.
```

Score: 3/10  8/10. Concrete experience, opinionated, uneven structure.

### Example 3: Register Mismatch (Same Content, Different Registers)

The same AI-generated sentence rewritten for three registers. Category 12 fires differently in each.

**AI output:**

```
The framework natively supports persistent memory across interactions,
enabling seamless context retention for multi-session workflows.
```

**Conversational register (social post, casual writing):**

Category 12 flags: "natively supports" (textbook), "persistent memory across interactions" (compound nominal + textbook), "enabling seamless context retention" (nominalized verb + textbook), "multi-session workflows" (category language).

```
It remembers things between conversations out of the box, so you don't
start from scratch every time.
```

**Dev-to-dev register (PR description, issue comment):**

Category 12 flags: "enabling seamless context retention" (over-formal for a PR), "multi-session workflows" (category language). "Natively supports" and "persistent memory" are acceptable dev shorthand.

```
The framework supports persistent memory across sessions -- context
carries over without extra config.
```

**Technical register (architecture doc, RFC):**

Category 12: no flags. All terms are appropriate for the register.

```
The framework natively supports persistent memory across interactions,
enabling context retention for multi-session workflows.
```

Only "seamless" was cut -- it's Category 8 (precise-sounding vagueness), not register mismatch.

---

## Voice Profile: Building One

When running `mode=profile`, provide 5-10 samples of writing you're satisfied with. The system extracts:

| Dimension | What It Captures |
|-----------|-----------------|
| **Sentence patterns** | Average length, variance, fragment frequency |
| **Vocabulary** | Words you use naturally, words you never use |
| **Punctuation** | Comma habits, dash usage, parenthetical frequency |
| **Paragraph shape** | Length range, length variance |
| **Openings** | How you start paragraphs and pieces |
| **Closings** | How you end: trailing thoughts, abrupt stops, questions |
| **Tone markers** | Formality level, humor, directness |
| **Contractions** | Frequency and which ones |
| **Specificity** | How concrete your references are |

The profile becomes a calibration reference that detection and rewrite stages use to target *your* voice, not generic "human."

**Persona files vs voice profiles:** A persona file (e.g., `my-persona.md`) is an external document that describes how an author writes, used during *generation*. A voice profile is extracted *by this command* from writing samples, used during *detection and rewrite*. They complement each other: persona drives generation, profile calibrates the quality gate.

**Precedence:** Project style rules (voice-guidelines.md, CLAUDE.md) override voice profile defaults, which override generic heuristics. When conflicts arise, project rules win.

---

## Anti-Patterns

| Anti-Pattern | Problem | Do Instead |
|--------------|---------|------------|
| Humanizing without a persona | Generic-minus-tells, not human writing | Generate with persona first, then voice-review |
| Rewriting everything | New mechanical patterns | Fix only flagged sections |
| Forcing quirky fragments | Detectable as fake-casual | Imperfections only where natural |
| Removing all structure | Unreadable | Break patterns, keep organization |
| Single-pass detect+fix | No visibility into changes | Separate the stages |
| Ignoring author voice | Generic "human" isn't specific enough | Use persona when available |
| Over-shortening | Losing meaning | Cut padding, keep substance |
| Fixing subtle tells first | Low impact | Fix HIGH severity first |

---

## Comment Register

Findings posted as PR/issue comments follow `~/.claude/CLAUDE.md` § GitHub Artifact Register: one load-bearing observation per comment, one sentence per finding, no narration or severity adjectives.

---

## Related Commands

- `/pb-think` - General thinking toolkit; use `mode=refine` for output refinement
- `/pb-review-docs` - Documentation quality review (structural, not voice)
- `/pb-documentation` - Writing engineering documentation
- `/pb-design-rules` - Clarity over cleverness applies to prose
- `/pb-preamble` - Honest, direct communication philosophy

---

*The tool removes tells. The author adds truth. Persona drives voice. pb-voice is the safety net.*
