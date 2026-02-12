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
- **Removed sections** — Command has fewer sections than before (requires user adaptation)
- **Changed scope/purpose** — Command does something fundamentally different
- **Breaking API** — Command's structure or inputs/outputs change significantly
- **Replaced** — Command is replaced by another (migration path required)

Examples triggering major bump:
- Remove "Outcome Clarification" from pb-start → 2.0.0
- Merge pb-security and pb-hardening into single command → 2.0.0
- Change pb-cycle from sequential to parallel-only execution → 2.0.0

### MINOR Version (new features, non-breaking)

Bump MINOR when:
- **Added sections** — New section added to command
- **Enhanced guidance** — Existing section rewritten with more depth
- **New examples** — Added concrete examples or code snippets
- **Related commands updated** — New cross-references added
- **Reorganization** — Content reorganized for clarity (same content, different structure)

Examples triggering minor bump:
- Add "Philosophy" section to design rules → 1.1.0
- Add "Step 0: Outcome Verification" to pb-cycle → 1.1.0
- Add new example to pb-testing → 1.1.0

### PATCH Version (cosmetic fixes, non-breaking)

Bump PATCH when:
- **Typo fix** — Grammar, spelling, or formatting corrections
- **Clarification** — Rewrote unclear sentence (same meaning, clearer expression)
- **Date update** — Updated reference date or timestamp
- **Link fix** — Fixed broken or outdated link

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
version_notes: "Initial v2.11.0 (Phase 1-4 enhancements)"
breaking_changes: []           # List of breaking changes (if any)
---
```

### `version`
Current semantic version of this command.

### `version_notes`
Human-readable note about what version changed:
- First release: "v2.10.0 baseline" or "Initial v2.11.0"
- Enhancement: "Phase 3: Added Outcome Clarification"
- Fix: "Fixed typo in Step 2"

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

**In the command index:**
View `/docs/command-changelog.md` for version history of all commands.

**In the help text:**
When viewing a command's help, the version is displayed.

---

## Migration Guide for Breaking Changes

When a command has a MAJOR version bump (breaking change):

### Step 1: Read the breaking_changes list
Check what changed and how it affects you.

### Step 2: Follow the migration path
The command will include a "Migration" section explaining:
- What changed
- Why it changed
- How to adapt your usage
- Alternative commands (if any)

### Step 3: Update your workflows
Adapt your processes to the new version.

### Example: Hypothetical pb-cycle v2.0.0

```
## Migration Guide

**What changed:** pb-cycle now requires parallel execution pattern (no sequential mode)

**Why:** Testing infrastructure improved; serial execution no longer needed

**How to adapt:**
- Remove `sequential` mode from your workflows
- All cycles now run: code → [parallel-review + parallel-test] → commit
- Review results synthesized before approval

**Alternative:** Use `/pb-cycle-sequential` for legacy serial workflows (deprecated, use sparingly)
```

---

## Version Stability Guarantees

### v1.x.x (1.0.0 - 1.9.9)
**Stable API.** Features may be added (MINOR), bugs fixed (PATCH), but core structure is stable. Safe to depend on.

### v2.x.x (2.0.0+)
**Breaking changes possible.** Core has changed. Review breaking_changes list before upgrading.

### v0.x.x (if ever used)
**Unstable.** Not yet stable. Breaking changes expected. Use with caution.

---

## When Commands Are Versioned

Commands are versioned:
1. **At creation** → v1.0.0 (initial baseline)
2. **When enhanced** → v1.1.0 (added sections)
3. **When fixed** → v1.0.1 (bug fixes, typos)
4. **When substantially changed** → v2.0.0 (breaking changes)

Commands are NOT versioned on every single edit. Only meaningful changes (additions, removals, significant rewrites) warrant version bumps.

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
- Bookmark `/docs/command-changelog.md` for reference

### For Maintainers (Playbook Authors)
- Bump version ONLY when making changes
- Use clear version_notes describing what changed
- Document breaking_changes for MAJOR bumps with migration paths
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

- **Command Changelog:** [command-changelog.md](command-changelog.md) — Version history of all commands
- **Command Index:** [command-index.md](command-index.md) — Full list of commands
- **Individual Commands:** Each command has version metadata in its YAML front-matter

---

*This guide applies to v1.1.0+ commands. Older baseline commands (v1.0.0) use the same scheme.*
