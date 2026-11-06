# Command Versioning Guide

This guide explains how playbook commands are versioned and how to interpret version numbers.

---

## Versioning Scheme

Commands use **semantic versioning**: MAJOR.MINOR.PATCH

```
MAJOR.MINOR.PATCH

Examples:
- 1.0.0 = Baseline (initial stable release)
- 1.1.0 = Enhanced with new sections (non-breaking)
- 1.0.1 = Typo fix (non-breaking)
- 2.0.0 = Breaking change (scope/purpose change)
```

### MAJOR Version (breaking changes)

Bump MAJOR when:
- **Removed invocation** - The command name, a flag or argument, or a step number or heading another command cites disappears (requires user adaptation)
- **Changed scope/purpose** - Command does something fundamentally different
- **Breaking API** - Command's structure or inputs/outputs change significantly
- **Replaced** - Command is replaced by another (migration path required)

Examples triggering major bump:
- Renumber a step that another command cites → 2.0.0
- Merge pb-security and pb-hardening into single command → 2.0.0
- Change pb-cycle from sequential to parallel-only execution → 2.0.0

### MINOR Version (new features, non-breaking)

Bump MINOR when:
- **Added sections** - New section added to command
- **Enhanced guidance** - Existing section rewritten with more depth
- **New examples** - Added concrete examples or code snippets
- **Related commands updated** - New cross-references added
- **Reorganization** - Content reorganized for clarity (same content, different structure)
- **Removed content** - Sections or examples nothing invokes or cites, however many

Examples triggering minor bump:
- Add "Philosophy" section to design rules → 1.1.0
- Add "Step 0: Outcome Verification" to pb-cycle → 1.1.0
- Add new example to pb-testing → 1.1.0

### PATCH Version (cosmetic fixes, non-breaking)

Bump PATCH when:
- **Typo fix** - Grammar, spelling, or formatting corrections
- **Clarification** - Rewrote unclear sentence (same meaning, clearer expression)
- **Date update** - Updated reference date or timestamp
- **Link fix** - Fixed broken or outdated link

Examples triggering patch bump:
- Fix typo in command description
- Clarify confusing example
- Update date reference

---

## Understanding Version Metadata

Each command has version metadata in its YAML front-matter:

```yaml
---
name: "pb-command"
version: "1.1.0"              # Current command version
version_notes: "v1.1.0: Added Outcome Clarification"
breaking_changes: []           # List of breaking changes (if any)
---
```

### `version`
Current semantic version of this command.

### `version_notes`
One line for the version being shipped, starting `v{version}:` and a space: what changed, and why where it is not obvious. A bump replaces the notes; earlier versions live in git and the CHANGELOG. `test_bumped_commands_name_one_version` checks every command bumped since the last tag, so notes written before the rule change at the command's next bump.

### `breaking_changes`
List of breaking changes (if MAJOR version):

```yaml
breaking_changes:
  - "Removed 'Legacy Mode' section; use /pb-new-alternative instead"
  - "Changed execution from sequential to parallel"
```

Empty if MINOR or PATCH version.

---

## How to Check a Command's Version

**In the command itself:**
Look at the YAML metadata at the top of the file:

```
---
name: "pb-start"
version: "1.1.0"
---
```

**In the CHANGELOG:**
[CHANGELOG.md](https://github.com/vnykmshr/playbook/blob/main/CHANGELOG.md) records each release's command version changes.

---

## Migration Guide for Breaking Changes

When a command has a MAJOR version bump (breaking change):

### Step 1: Read the breaking_changes list
Check what changed and how it affects you.

### Step 2: Read what changed
Each `breaking_changes` entry says what changed.

### Step 3: Update your workflows
Adapt your processes to the new version.

---

## Version Stability Guarantees

A MAJOR bump marks a breaking change (something invoked or cited disappears), and the command's `breaking_changes` lists it. MINOR and PATCH bumps never remove what a caller invokes or cites, whatever the major number. A MINOR bump can cut reference content.

---

## When Commands Are Versioned

Commands are versioned:
1. **At creation** → v1.0.0 (initial baseline)
2. **When enhanced** → v1.1.0 (added sections)
3. **When fixed** → v1.0.1 (bug fixes, typos)
4. **When substantially changed** → v2.0.0 (breaking changes)

A change to a command's body ships under a new version: PATCH for a fix, clarification or link change, the levels above otherwise. The body is everything after the front matter's closing `---`, blank lines aside. `test_body_change_carries_version_bump` checks every command against the last tag, working tree included.

**One bump per release.** A command's version moves at most once between two playbook tags. The first commit to touch a command after a tag sets the version it ships at; later commits before the next tag amend that version's `version_notes` and carry their own CHANGELOG line instead of minting another number. Plan the level at the first bump: a later change that needs a higher level waits for the next tag. `test_one_version_bump_per_command_per_window` enforces the count, and the changelog guard fires on a `version_notes` change as well as a bump.

---

## Playbook Version vs Command Versions

**Playbook version** (e.g., v2.11.0): Overall release of the playbook
**Command version** (e.g., 1.1.0): Version of an individual command within that playbook

They are independent:
- Playbook releases every quarter (v2.10.0, v2.11.0, v2.12.0...)
- Commands can update at any time (v1.0.0 → v1.1.0 can happen mid-quarter)
- A command at v1.0.0 in playbook v2.11.0 hasn't changed since v2.10.0

---

## Command Lifecycle

### Creation (v1.0.0)
New command created and released as v1.0.0 (baseline).

### Enhancement (v1.1.0, v1.2.0...)
Command gains new sections or improved guidance. Non-breaking, backward compatible.

### Stabilization (v1.x.x)
Command reaches maturity. Mostly typo fixes and clarifications. Rare new sections.

### Replacement (v2.0.0)
Command significantly changes OR is replaced by a newer command. Users must migrate.

### Deprecation (optional)
Command is marked for removal. Still works, but users encouraged to migrate.

### Removal (very rare)
Command deleted entirely (only after long deprecation period).

---

## Best Practices

### For Users
- Check command version when starting a new workflow
- Review `version_notes` to understand what's changed
- When upgrading playbooks, check breaking_changes for any MAJOR version bumps
- Read the [CHANGELOG](https://github.com/vnykmshr/playbook/blob/main/CHANGELOG.md) for each release's command changes

### For Maintainers (Playbook Authors)
- Bump version ONLY when making changes
- Use clear version_notes describing what changed
- Document breaking_changes for MAJOR bumps, saying what changed
- Announce deprecations 1-2 releases before removal
- Never bump version without updating version_notes

### Semantic Versioning Rules
- Start at 1.0.0 (not 0.1.0)
- Increment MAJOR for breaking changes
- Increment MINOR for backward-compatible features
- Increment PATCH for backward-compatible fixes
- Never have gaps (jump from 1.0.0 to 1.0.2 skipping 1.0.1 is wrong)

---

## Related Documentation

- **CHANGELOG:** [CHANGELOG.md](https://github.com/vnykmshr/playbook/blob/main/CHANGELOG.md) - Release history, including command version changes
- **Command Index:** [command-index.md](command-index.md) - Full list of commands
- **Individual Commands:** Each command has version metadata in its YAML front-matter

---

*This guide applies to v1.1.0+ commands. Older baseline commands (v1.0.0) use the same scheme.*
