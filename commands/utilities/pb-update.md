---
name: "pb-update"
title: "Update All Tools"
category: "utilities"
difficulty: "advanced"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-doctor', 'pb-storage', 'pb-setup', 'pb-security']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Update All Tools

Update all package managers, development tools, and system software with appropriate safety tiers. Keep your dev environment current without breaking things.

**Platform:** macOS (primary), Linux (alternatives noted)
**Risk Model:** Safe updates first, major version bumps require confirmation

**Mindset:** Design Rules say "distrust one true way" — update selectively, verify after each tool.

**Resource Hint:** haiku — detecting outdated packages and running update commands.

## When to Use

- Weekly routine to apply safe patch updates
- Monthly full maintenance cycle (safe + moderate tiers)
- After a security advisory requiring immediate tool updates
- Setting up a recently bootstrapped dev machine

---

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. SCAN         Detect installed package managers/tools    │
│         ↓                                                   │
│  2. CHECK        List what's outdated in each               │
│         ↓                                                   │
│  3. TIER SELECT  User chooses: safe / all / selective       │
│         ↓                                                   │
│  4. EXECUTE      Run updates with progress output           │
│         ↓                                                   │
│  5. VERIFY       Confirm tools still work                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Update (Safe Tier Only)

Run this for routine maintenance:

```bash
# Homebrew (most common)
brew update && brew upgrade

# npm global packages
npm update -g

# macOS software updates (safe ones only)
softwareupdate -l
```

---

## Step 1: Detect Installed Tools

```bash
echo "=== Package Managers ==="
command -v brew && echo "Homebrew: $(brew --version | head -1)"
command -v npm && echo "npm: $(npm --version)"
command -v pip3 && echo "pip: $(pip3 --version)"
command -v cargo && echo "Cargo: $(cargo --version)"
command -v gem && echo "RubyGems: $(gem --version)"
command -v go && echo "Go: $(go version)"

echo -e "\n=== Version Managers ==="
command -v nvm && echo "nvm: installed"
command -v pyenv && echo "pyenv: installed"
command -v rbenv && echo "rbenv: installed"
command -v rustup && echo "rustup: installed"
```

---

## Step 2: Check What's Outdated

### Homebrew

```bash
# Update formula list first
brew update

# Show outdated packages
brew outdated

# Show outdated casks (apps)
brew outdated --cask
```

### npm (Global Packages)

```bash
# List outdated globals
npm outdated -g

# Or with details
npm outdated -g --depth=0
```

### pip (Python)

```bash
# List outdated packages
pip3 list --outdated

# Or just count
pip3 list --outdated | wc -l
```

### Rust (rustup + cargo)

```bash
# Check for Rust updates
rustup check

# Check cargo-installed binaries (if cargo-update installed)
cargo install-update -l 2>/dev/null || echo "Install cargo-update for this"
```

### Go

```bash
# Go modules in current project
go list -m -u all 2>/dev/null | grep '\[' | head -10
```

### macOS System

```bash
# List available system updates
softwareupdate -l
```

---

## Tier Definitions

### Tier 1: SAFE (Patch updates, no breaking changes)

| Tool | Command | Notes |
|------|---------|-------|
| Homebrew | `brew upgrade` | All formulae |
| npm | `npm update -g` | Respects semver |
| pip | `pip3 install --upgrade pip` | pip itself only |
| Rust | `rustup update` | Stable toolchain |

**Commands:**
```bash
# Safe tier - run all
brew update && brew upgrade
npm update -g
pip3 install --upgrade pip
rustup update stable 2>/dev/null
```

**Risk:** Minimal. Patch updates follow semver.

---

### Tier 2: MODERATE (Minor version updates)

| Tool | Command | Notes |
|------|---------|-------|
| Homebrew casks | `brew upgrade --cask` | App updates |
| npm major | `npm install -g <pkg>@latest` | Specific packages |
| pip packages | `pip3 install --upgrade <pkg>` | Specific packages |
| Node.js | `nvm install --lts` | New LTS version |

**Commands:**
```bash
# Homebrew casks (GUI apps)
brew upgrade --cask

# Node LTS (if using nvm)
nvm install --lts
nvm alias default lts/*
```

**Risk:** Low-moderate. May require config changes.

---

### Tier 3: MAJOR (Major version updates, potential breaking changes)

| Tool | Command | Notes |
|------|---------|-------|
| macOS | `softwareupdate -ia` | Full system update |
| Xcode | App Store | May break builds |
| Python | `pyenv install X.Y` | New Python version |
| Docker | Cask upgrade | Container compat |

**Commands:**
```bash
# macOS system updates
sudo softwareupdate -ia

# New Python version (pyenv)
pyenv install 3.12  # or latest
pyenv global 3.12

# Docker Desktop
brew upgrade --cask docker
```

**Risk:** Higher. Test builds after updating.

---

## Package-Specific Guides

### Homebrew

```bash
# Full update cycle
brew update          # Update formulae list
brew upgrade         # Upgrade all packages
brew cleanup         # Remove old versions
brew doctor          # Check for issues
```

### npm

```bash
# Update all globals to latest
npm outdated -g
npm update -g

# Update specific package to latest major
npm install -g typescript@latest

# Check what's installed globally
npm list -g --depth=0
```

### pip

```bash
# Upgrade pip itself
pip3 install --upgrade pip

# Upgrade all packages (use with caution)
pip3 list --outdated --format=json | \
  python3 -c "import json,sys;print('\n'.join([p['name'] for p in json.load(sys.stdin)]))" | \
  xargs -n1 pip3 install -U

# Better: use pip-review
pip3 install pip-review
pip-review --auto
```

### Rust

```bash
# Update Rust toolchain
rustup update

# Update cargo-installed tools
cargo install-update -a  # Requires cargo-update
```

### Ruby (rbenv)

```bash
# Update rbenv itself
brew upgrade rbenv ruby-build

# Install latest Ruby
rbenv install -l | grep -v - | tail -1  # Find latest
rbenv install X.Y.Z
rbenv global X.Y.Z
```

---

## User Interaction Flow

When executing this playbook:

1. **Detect** — Show all installed package managers
2. **Scan** — List outdated packages per manager
3. **Present tiers** — Let user choose update scope
4. **Execute** — Run updates with progress
5. **Verify** — Run quick health checks

### AskUserQuestion Structure

**Tier Selection:**
```
Question: "What update level should I run?"
Options:
  - Safe only (patch updates) - Low risk
  - Include minor versions - Some risk
  - Full update (including major) - Higher risk, review first
  - Let me pick specific tools
MultiSelect: false
```

**Tool Selection (if selective):**
```
Question: "Which tools should I update?"
Options:
  - Homebrew (X outdated)
  - npm globals (X outdated)
  - pip packages (X outdated)
  - System updates (X available)
MultiSelect: true
```

---

## Post-Update Verification

```bash
echo "=== Verification ==="

# Check critical tools still work
git --version
node --version
npm --version
python3 --version

# Run a quick test
echo 'console.log("Node OK")' | node
python3 -c "print('Python OK')"

# Check for broken Homebrew links
brew doctor
```

---

## Automated Update Script

Save as `~/bin/update-all.sh`:

```bash
#!/bin/bash

set -e

echo "=== Homebrew ==="
brew update && brew upgrade && brew cleanup

echo -e "\n=== npm globals ==="
npm update -g

echo -e "\n=== pip ==="
pip3 install --upgrade pip

echo -e "\n=== Rust ==="
rustup update 2>/dev/null || true

echo -e "\n=== Verification ==="
brew doctor
node --version
python3 --version

echo -e "\n=== Done ==="
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Homebrew permission errors | `sudo chown -R $(whoami) $(brew --prefix)/*` |
| npm EACCES errors | Fix npm permissions or use nvm |
| pip externally-managed | Use `pip3 install --break-system-packages` or venv |
| Xcode update breaks tools | `xcode-select --install` |
| Rust won't update | `rustup self update` first |
| Node version mismatch | Check nvm: `nvm current` vs `node --version` |

---

## Update Schedule

| Frequency | What to Update |
|-----------|----------------|
| Weekly | Homebrew (safe tier) |
| Monthly | All safe + moderate tiers |
| Quarterly | Major versions (with testing) |
| As needed | Security patches immediately |

---

## Related Commands

- `/pb-doctor` — Check system health before/after updates
- `/pb-storage` — Clean up after updates (old versions)
- `/pb-setup` — Full environment setup
- `/pb-security` — Check for security updates

---

*Run weekly for safe updates, monthly for full maintenance. Always verify after major updates.*
