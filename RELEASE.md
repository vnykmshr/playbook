# Release Process

This document describes how to release a new version of the Engineering Playbook.

---

## Prerequisites

- Git and Bash installed
- All changes committed to main branch
- Changelog entries prepared for new version

---

## Release Steps

### 1. Prepare Changelog

Add new section to `CHANGELOG.md`:

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Added
- [New features/commands]

### Fixed
- [Bug fixes]

### Changed
- [Modifications]
```

Commit changes:

```bash
git add CHANGELOG.md
git commit -m "docs: release notes for vX.Y.Z"
```

### 2. Create Release Tag

Run the release script:

```bash
./scripts/release.sh
```

The script will:
- Verify git state (no uncommitted changes)
- Prompt for new version (format: X.Y.Z)
- Create annotated git tag with release message
- Show next steps

### 3. Push Tag to Remote

```bash
git push origin vX.Y.Z
```

GitHub will automatically create a Release page from the tag.

### 4. Verify Release

- Check https://github.com/vnykmshr/playbook/releases
- Verify tag appears with correct commit
- Verify docs deployed to https://vnykmshr.github.io/playbook/

---

## Version Numbering

Uses semantic versioning: **vX.Y.Z**

- **X** (Major): Breaking changes to commands or workflow
- **Y** (Minor): New commands, features, or non-breaking enhancements
- **Z** (Patch): Bug fixes, docs updates, cleanup

---

## Example: Release v1.2.1

### Step 1: Update Changelog

```bash
# Add new release section to CHANGELOG.md
cat >> CHANGELOG.md <<EOF

## [v1.2.1] - 2026-01-12

### Fixed
- Fixed broken link in pb-review-hygiene command
- Corrected indentation in CONTRIBUTING.md examples

EOF

git add CHANGELOG.md
git commit -m "docs: release notes for v1.2.1"
```

### Step 2: Create Tag

```bash
./scripts/release.sh
# When prompted:
# Enter new version (e.g., 1.2.1): 1.2.1
# Proceed with release? (y/n) y
```

### Step 3: Push Tag

```bash
git push origin v1.2.1
```

The release is complete. GitHub will create the Release page automatically.

---

## Troubleshooting

### Tag Already Exists

If you try to create a tag that already exists:

```bash
git tag -d vX.Y.Z         # Delete local tag
git push origin --delete vX.Y.Z  # Delete remote tag
# Then try again: ./scripts/release.sh
```

### Need to Amend Release

If you need to update the release message:

```bash
git tag -d vX.Y.Z
git tag -a vX.Y.Z -m "Updated release notes..."
git push origin --force vX.Y.Z
```

### Rollback Release

If release was problematic:

```bash
git tag -d vX.Y.Z                      # Delete local tag
git push origin --delete vX.Y.Z        # Delete remote tag
git reset --soft HEAD~1                # Undo CHANGELOG commit if needed
# Fix the issue and try again
```

### Script Exits Without Creating Tag

Common reasons:

1. **Uncommitted changes**: Commit or stash changes first
   ```bash
   git status  # Check for changes
   git add .   # Stage changes
   git commit -m "message"
   ```

2. **Tag already exists**: Use troubleshooting section above

3. **Not in repo root**: Run from the playbook directory
   ```bash
   cd /path/to/playbook
   ./scripts/release.sh
   ```

---

## Automation

Future enhancements (not yet implemented):

- [ ] Auto-update version in README badge
- [ ] Generate changelog from commit messages
- [ ] Create GitHub Release with formatted notes
- [ ] Trigger additional CI/CD steps

---

## Quick Reference

```bash
# Normal release process
./scripts/release.sh
git push origin v[version]

# Check latest tag
git tag -l | sort -V | tail -1

# See tag details
git show v1.2.0

# View all tags
git tag -l
```

---

## Related Documentation

- **CHANGELOG.md** — Version history and release notes
- **scripts/release.sh** — Automated release script
- **.github/CONTRIBUTING.md** — Contribution guidelines
- **README.md** — Project overview
