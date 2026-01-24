# Git Hygiene

**Purpose:** Periodic audit of git repository health. Identify tracked files that shouldn't be, clean stale branches, detect large objects, scan for secret exposure, and remediate with options from safe amendments to full history rewrites.

**Recommended Frequency:** Monthly, before major releases, or when repo feels slow

**Mindset:** Apply `/pb-preamble` thinking (surface problems directly, don't minimize findings) and `/pb-design-rules` thinking (Clarity, Simplicity: repository should contain only what's needed, history should be clean).

A healthy git repo is fast to clone, safe from leaked secrets, and free of accumulated cruft. This audit surfaces issues; you decide what to fix.

---

## When to Use

- **Monthly maintenance** — Routine hygiene check
- **Before major release** — Clean up feature branches, verify no secrets
- **After onboarding developers** — Catch accidental commits of secrets or large files
- **When clone feels slow** — Diagnose repo bloat
- **Before open-sourcing** — Audit history for sensitive data
- **After security incident** — Scan for leaked credentials in history

---

## Phase 1: Discovery (Read-Only Audit)

Run these checks to understand current state. No changes made.

### 1.1 Tracked Files That Shouldn't Be

Check for files that should be gitignored:

```bash
# Environment and secrets
git ls-files | grep -E '\.env$|\.env\.|credentials|secrets|\.pem$|\.key$|id_rsa'

# Generated artifacts
git ls-files | grep -E 'node_modules/|vendor/|dist/|build/|__pycache__|\.pyc$|\.class$'

# IDE and OS files
git ls-files | grep -E '\.idea/|\.vscode/|\.DS_Store|Thumbs\.db|\.swp$'

# Lock files — NOTE: Most projects SHOULD commit these for reproducible builds
# Only flag if your project intentionally excludes them
# git ls-files | grep -E 'package-lock\.json|yarn\.lock|Gemfile\.lock|poetry\.lock'
```

### 1.2 .gitignore Coverage Gaps

Compare what's ignored vs what should be:

```bash
# Show files that would be ignored if .gitignore were applied fresh
git ls-files --ignored --exclude-standard

# Check if common patterns are in .gitignore
for pattern in ".env" "node_modules" ".DS_Store" "*.pyc" ".idea" "dist"; do
  grep -q "$pattern" .gitignore 2>/dev/null || echo "Missing: $pattern"
done
```

### 1.3 Large Files in Current Tree

```bash
# Find files larger than 1MB
find . -type f -size +1M -not -path "./.git/*" -exec ls -lh {} \;

# Top 20 largest files
git ls-files | xargs -I{} du -h "{}" 2>/dev/null | sort -rh | head -20
```

### 1.4 Large Objects in History

```bash
# Find largest objects in entire history (requires git-filter-repo or manual)
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print $3, $4}' | \
  sort -rn | head -20

# Simpler: check pack size
du -sh .git/objects/pack/
```

### 1.5 Branch Inventory

```bash
# List all local branches with last commit date
git for-each-ref --sort=-committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)'

# List merged branches (safe to delete)
git branch --merged main | grep -v "main\|master\|\*"

# List remote branches merged to main
git branch -r --merged origin/main | grep -v "main\|master\|HEAD"

# Stale branches (no commits in 90 days)
git for-each-ref --sort=committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)' | \
  awk -v cutoff=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d '90 days ago' +%Y-%m-%d) \
  '$1 < cutoff {print}'
```

### 1.6 Secret Scanning

**Current files:**
```bash
# Quick pattern scan (basic, not comprehensive)
git ls-files | xargs grep -l -E \
  'AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35}|sk-[a-zA-Z0-9]{48}|ghp_[a-zA-Z0-9]{36}' \
  2>/dev/null

# API key patterns
git ls-files | xargs grep -l -E \
  'api[_-]?key|apikey|secret[_-]?key|password\s*=' 2>/dev/null
```

**History scan (use dedicated tools):**
```bash
# gitleaks (recommended)
gitleaks detect --source . --verbose

# trufflehog
trufflehog git file://. --only-verified

# git-secrets (AWS-focused)
git secrets --scan-history
```

### 1.7 Repository Size and Health

```bash
# Total repo size
du -sh .git

# Object count and size
git count-objects -vH

# Check for corruption
git fsck --full

# Dangling objects (orphaned commits/blobs)
git fsck --unreachable | head -20
```

---

## Phase 2: Triage Findings

Categorize discoveries by severity:

| Severity | Examples | Action Timeline |
|----------|----------|-----------------|
| **Critical** | Secrets in current files, credentials in history | Immediate (rotate + remove) |
| **High** | Large binaries in history, secrets in old commits | This session |
| **Medium** | Stale branches, unnecessary tracked files | Soon |
| **Low** | .gitignore improvements, minor cleanup | When convenient |

### Triage Template

```markdown
## Git Hygiene Findings: [Date]

### Critical (Immediate)
- [ ] [Finding]

### High (This Session)
- [ ] [Finding]

### Medium (Soon)
- [ ] [Finding]

### Low (When Convenient)
- [ ] [Finding]
```

---

## Phase 3: Remediation

Choose remediation level based on severity and whether changes have been pushed.

### Level 1: Safe (No History Rewrite)

**Use when:** Recent unpushed commits, or changes that don't require history modification.

#### Delete merged branches

```bash
# Delete local merged branches
git branch --merged main | grep -v "main\|master\|\*" | xargs -r git branch -d

# Delete remote merged branches (careful!)
git branch -r --merged origin/main | grep -v "main\|master\|HEAD" | \
  sed 's/origin\///' | xargs -I{} git push origin --delete {}
```

#### Remove file from index (keep in .gitignore)

```bash
# Stop tracking file but keep locally
git rm --cached path/to/file
echo "path/to/file" >> .gitignore
git add .gitignore
git commit -m "chore: stop tracking [file], add to .gitignore"
```

#### Amend recent unpushed commit

```bash
# Remove file from last commit (not pushed)
git reset HEAD~1
git add [files-to-keep]
git commit -m "original message"
```

---

### Level 2: Careful (History Rewrite, Team Coordination)

**Use when:** Need to remove from history, but repo is shared. **Requires team coordination.**

**Before starting:**
1. Notify all team members
2. Ensure everyone has pushed their work
3. Plan re-clone or rebase for all developers

#### git filter-repo (Recommended)

```bash
# Install if needed
pip install git-filter-repo

# Remove file from entire history
git filter-repo --path path/to/secret/file --invert-paths

# Remove directory from history
git filter-repo --path secrets/ --invert-paths

# Remove files matching pattern
git filter-repo --path-glob '*.pem' --invert-paths
```

#### After history rewrite

```bash
# Force push (coordinate with team first!)
git push origin --force --all
git push origin --force --tags

# Team members must:
git fetch origin
git reset --hard origin/main
# OR fresh clone
```

---

### Level 3: Nuclear (Full History Rewrite or Migration)

**Use when:** Severe contamination, open-sourcing private repo, or history is unsalvageable.

**Warning:** These options destroy git history. For regulated industries (finance, healthcare, government), git history may be required for audit trails. Consult compliance before proceeding. Consider archiving the original repo before any destructive action.

#### BFG Repo-Cleaner

Faster than filter-repo for large repos:

```bash
# Download BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# Remove files larger than 100MB from history
java -jar bfg.jar --strip-blobs-bigger-than 100M

# Remove specific files
java -jar bfg.jar --delete-files "*.pem"

# Remove secrets
java -jar bfg.jar --replace-text passwords.txt

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

#### Fresh Start Migration

When history is too contaminated:

```bash
# Archive old repo
mv .git .git-old

# Initialize fresh
git init
git add .
git commit -m "chore: fresh start (history archived)"

# Push to new remote (or same with force)
git remote add origin <url>
git push -u origin main --force
```

---

## Phase 4: Prevention

Stop issues from recurring.

### Update .gitignore

Add missing patterns:

```gitignore
# Secrets
.env
.env.*
*.pem
*.key
credentials.json
secrets/

# Generated
node_modules/
vendor/
dist/
build/
__pycache__/
*.pyc

# IDE
.idea/
.vscode/settings.json
*.swp

# OS
.DS_Store
Thumbs.db
```

### Pre-Commit Hooks

Install hooks to catch issues before commit:

```bash
# Using pre-commit framework
pip install pre-commit

# .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
EOF

pre-commit install
```

### CI Integration

Add to CI pipeline:

```yaml
# GitHub Actions example
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

- name: Check file sizes
  run: |
    find . -type f -size +5M -not -path "./.git/*" && exit 1 || exit 0
```

---

## Output: Hygiene Report Template

```markdown
# Git Hygiene Report: [Repo Name]
**Date:** [Date]
**Auditor:** [Name]

## Summary
- **Overall Health:** [Good | Needs Attention | At Risk]
- **Repo Size:** [X MB/GB]
- **Branch Count:** [X local, Y remote]
- **Critical Issues:** [X]

## Findings

### Critical
| Issue | Location | Remediation |
|-------|----------|-------------|
| [Issue] | [Path/Ref] | [Action taken] |

### High
| Issue | Location | Remediation |
|-------|----------|-------------|

### Medium
| Issue | Location | Remediation |
|-------|----------|-------------|

### Low
| Issue | Location | Recommended Action |
|-------|----------|-------------------|

## Actions Taken
1. [Action]
2. [Action]

## Prevention Measures Added
- [ ] Updated .gitignore
- [ ] Installed pre-commit hooks
- [ ] Added CI checks

## Next Review
Scheduled: [Date]
Focus areas: [Areas to watch]
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Find tracked secrets | `git ls-files \| grep -E '\.env\|credentials'` |
| Find large files | `find . -type f -size +1M -not -path "./.git/*"` |
| List merged branches | `git branch --merged main` |
| Delete merged branches | `git branch --merged main \| grep -v main \| xargs git branch -d` |
| Remove file from history | `git filter-repo --path FILE --invert-paths` |
| Scan for secrets | `gitleaks detect --source .` |
| Check repo size | `du -sh .git` |
| Prune dangling objects | `git gc --prune=now` |

---

## Verification

After completing hygiene audit:

- [ ] All 7 discovery checks executed
- [ ] Findings triaged by severity
- [ ] Critical issues addressed immediately
- [ ] High-priority issues have remediation plan
- [ ] Prevention measures implemented (pre-commit hooks, CI checks)
- [ ] Hygiene report documented
- [ ] Next review date scheduled

---

## Related Commands

- `/pb-review-hygiene` — Code quality and operational readiness review
- `/pb-security` — Security audit (broader than git-specific)
- `/pb-repo-organize` — Repository structure cleanup
- `/pb-repo-enhance` — Repository polish suite
- `/pb-doctor` — System health check

---

**Last Updated:** 2026-01-24
**Version:** 1.0.0
