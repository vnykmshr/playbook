# Contributing to Engineering Playbook

## How to Report Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/vnykmshr/playbook/issues) with:
- Clear title describing the problem
- Steps to reproduce (if applicable)
- Expected vs. actual behavior

## How to Suggest Improvements

Have an idea for a new command or enhancement? [Start a discussion](https://github.com/vnykmshr/playbook/discussions) to:
- Describe the use case
- Explain why it's needed
- Discuss the approach before implementing

## Dependency Management

This project uses [Dependabot](https://dependabot.com) to manage dependencies. Updates are created for npm, pip, Go, and GitHub Actions.

### Handling Dependabot PRs

**Review Policy:**
- **Patch updates** (1.2.3 → 1.2.4) — Approve and merge after CI passes
- **Minor updates** (1.2.0 → 1.3.0) — Review release notes, consider impact
- **Major updates** (1.0.0 → 2.0.0) — Detailed review and testing required
- **Security patches** — Always prioritize and merge immediately

**Labels:** `dependencies`, plus ecosystem labels (`npm`, `python`, `go`, `github-actions`)

**Security Issues:** Check [Security Advisories](../../security/dependabot) for vulnerabilities

## How to Contribute Code

### Commands

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-command-name`
3. Create command file in appropriate `commands/` subdirectory
4. Follow existing command structure and documentation format
5. Test locally: verify the command works as documented
6. Submit a pull request with:
  - Clear description of what the command does
  - When to use it
  - How it integrates with other commands

#### Command Structure Guidelines

All commands must follow this structure to ensure consistency and usability:

**Required Elements:**

1. **Title** (H1 heading)
  - Clear, action-oriented description (e.g., "Start Development Work", "Deploy with Blue-Green Strategy")
  - Format: `# [Verb] [What]` or `# [What] Guide`

2. **Overview** (introductory paragraph)
  - One sentence describing when to use this command
  - One sentence describing what it does
  - Reference related commands using `/pb-command-name` format

3. **Sections** (H2 headings with `---` dividers)
  - Use at least 3 major sections (e.g., "Preconditions", "Steps", "Verification")
  - Separate sections with `---` for visual clarity
  - Order sections logically (setup → execution → verification → rollback)

4. **Code Examples**
  - Include at least one runnable example
  - Use appropriate syntax highlighting (markdown, bash, etc.)
  - Real code examples, not pseudocode
  - Examples should be directly copy-pasteable

5. **Checklists** (where appropriate)
  - Use `[ ]` format for verification steps
  - Include acceptance criteria
  - Help users verify work is complete

6. **Cross-references**
  - Reference related commands using `/pb-command-name`
  - Format: `See [description](/pb-command-name)`
  - Keep references minimal (avoid link pollution)

**Optional Elements:**

- **Examples** section for multiple use cases
- **Troubleshooting** section for common issues
- **FAQ** section for questions
- **Rollback** section for destructive operations

**Linting Standards:**

- **Line length**: Soft limit 100 chars (warning at 120)
- **Heading style**: Consistent (all ATX style `# Heading`)
- **List indentation**: 2 spaces
- **No hard tabs**: Use spaces only
- **No trailing whitespace**
- **One blank line between sections**

**Before Submitting:**

- [ ] Title is clear and action-oriented
- [ ] Overview describes when and why to use
- [ ] At least 3 major sections with `---` dividers
- [ ] At least one runnable code example
- [ ] All `/pb-command` references are valid
- [ ] Markdown linting passes: `markdownlint --config .markdownlint.json commands/category/pb-command.md`
- [ ] No trailing whitespace or hard tabs
- [ ] Tone consistent with existing commands (professional, concise, no fluff)

**Example Command Structure:**

```
# [Title]

[Overview paragraph]

---

## [Section 1]

[Content]

### Subsection

[Details]

---

## [Section 2]

[Content with examples]

\`\`\`bash
# Example code
\`\`\`

---

## [Section 3]

[Content]

- [ ] Verification step 1
- [ ] Verification step 2
```

### Documentation

1. Follow the same branch/PR process
2. Keep changes focused and atomic
3. Run local checks: `markdownlint docs/` (if linting tools are set up)
4. Verify all links work

### Process

- All PRs require review
- Keep changes focused (one feature/fix per PR)
- Reference any related issues
- Be responsive to feedback

## Code of Conduct

Be respectful and constructive. This is a collaborative project for teams to improve their development practices.

## Questions?

- Check [docs/](/docs/) for existing documentation
- See [docs/command-index.md](/docs/command-index.md) for command reference
- Open a [discussion](https://github.com/vnykmshr/playbook/discussions) for questions
