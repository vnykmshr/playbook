---
name: "pb-repo-enhance"
title: "Repository Enhancement Suite"
category: "repo"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-repo-init', 'pb-repo-organize', 'pb-repo-readme', 'pb-repo-about', 'pb-repo-docsite']
tags: ['design', 'testing', 'workflow', 'review', 'deployment']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Repository Enhancement Suite

Comprehensive repository polish: organize, document, and present.

**Meta-perspective:** Enhancing a repository is about making it easy for others to understand it and challenge it. Use `/pb-preamble` thinking (organize for scrutiny, document for error-detection) and `/pb-design-rules` thinking (Clarity, Modularity, Representation: repository should be obviously organized).

Organize for scrutiny. Document clearly. Present honestly. Let others understand and challenge your work.

**Resource Hint:** sonnet — repository enhancement orchestrates structured tasks across organization, docs, and presentation

---

## When to Use

- Preparing a repository for public release or open source
- Periodic repository polish after a development milestone
- When the repo looks unprofessional or is hard to navigate
- Before onboarding new team members

---

## Objective

Transform a working repository into a polished, professional, discoverable project. Combines organization, documentation, and presentation tasks.

---

## Tasks

### 1. Repository Organization
**Reference:** `/pb-repo-organize`

- Clean up project root
- Move files to logical folders (`/docs`, `/scripts`, `/examples`)
- Keep only essential files at root
- Preserve `/todos` directory (gitignored)
- Ensure GitHub special files are in correct locations

### 2. GitHub About & Tags
**Reference:** `/pb-repo-about`

- Write concise About section (≤160 chars)
- Describe what, who, and key trait
- Include main tech stack
- Select 6-10 relevant, discoverable tags

### 3. README Enhancement
**Reference:** `/pb-repo-readme`

- Clear, professional structure
- Quick start example that works
- Installation instructions
- API reference or usage guide
- Badges for build status, coverage, version

### 4. Technical Blog Post
**Reference:** `/pb-repo-blog`

Create `docs/TECHNICAL_BLOG.md`:
- Introduction and rationale
- Architecture with Mermaid diagram(s)
- Code examples
- Design decisions
- Real-world applications
- Practical conclusion

### 5. Documentation Site (Optional)
**Reference:** `/pb-repo-docsite`

Transform docs into professional static site:
- Choose SSG based on project language (Hugo/MkDocs/Docusaurus)
- Set up CI/CD for GitHub Pages
- Migrate existing markdown docs
- Add Mermaid diagram support

---

## Process

### Phase 1: Audit
```bash
# Current state
ls -la
tree -L 2 -d  # or: find . -type d -maxdepth 2

# File count at root
find . -maxdepth 1 -type f | wc -l
```

### Phase 2: Organize
1. Create target directories
2. Move files to appropriate locations
3. Update any hardcoded paths
4. Verify build and tests pass

### Phase 3: Document
1. Write or update README
2. Create technical blog post
3. Ensure CHANGELOG exists
4. Add/update CONTRIBUTING.md if needed

### Phase 4: Present
1. Craft GitHub About section
2. Select topic tags
3. Add badges to README
4. Verify GitHub renders correctly

### Phase 5: Verify
```bash
# Build passes
make build

# Tests pass
make test

# No broken links in docs
# README renders correctly
# About section displays properly
```

---

## Output Checklist

After enhancement, verify:

**Structure:**
- [ ] Clean root with only essential files
- [ ] Logical folder organization
- [ ] GitHub special files in correct locations
- [ ] `/todos` preserved and gitignored

**Documentation:**
- [ ] README is clear and complete
- [ ] Technical blog post created
- [ ] CHANGELOG exists
- [ ] LICENSE present

**Presentation:**
- [ ] About section is compelling
- [ ] Tags are relevant and discoverable
- [ ] Badges display correctly
- [ ] Repository looks professional

---

## Quality Standards

**Tone:**
- Professional, not salesy
- Technical, not condescending
- Concise, not verbose

**Content:**
- Examples that work
- Accurate technical details
- No placeholder text
- No AI-sounding phrases

**Structure:**
- Consistent formatting
- Proper Markdown
- Working links
- Rendered correctly on GitHub

---

## Anti-Patterns to Avoid

| Problem | Solution |
|---------|----------|
| Cluttered root | Organize into folders |
| Vague README | Add examples and specifics |
| Missing About | Write compelling description |
| No tags | Add 6-10 relevant tags |
| Broken badges | Fix URLs or remove |
| Stale docs | Update or remove |

---

## Related Commands

- `/pb-repo-init` — Initialize new project structure
- `/pb-repo-organize` — Clean up repository structure
- `/pb-repo-readme` — Generate comprehensive README
- `/pb-repo-about` — Generate GitHub About section
- `/pb-repo-docsite` — Set up documentation site

---

*Professional repository, professional impression.*
