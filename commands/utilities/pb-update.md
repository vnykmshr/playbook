---
name: "pb-update"
title: "Update All Tools"
category: "utilities"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-doctor', 'pb-storage', 'pb-setup', 'pb-security']
last_reviewed: "2026-11-06"
version: "1.1.0"
version_notes: "v1.1.0: Tiers re-cut by mechanism (tracked, named, platform) with no semver claims; pip goes through venv or pipx, `--break-system-packages` last; nvm is sourced before use; the update script survives `brew doctor` warnings; Platform is macOS; the script sources nvm and shows pipx and rustup failures."
breaking_changes: []
---
# Update All Tools

Update all package managers, development tools, and system software with appropriate safety tiers. Keep your dev environment current without breaking things.

**Platform:** macOS
**Risk Model:** Tracked updates first; named packages and platform updates require confirmation

**Mindset:** Apply `/pb-design-rules` thinking: distrust one true way. Update selectively, verify after each tool.

**Resource Hint:** sonnet - Detecting outdated packages and running update commands with correct version handling.

## When to Use

- Weekly routine to apply tracked updates
- Monthly full maintenance cycle (tracked + named tiers)
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
│  3. TIER SELECT  User chooses: tracked / all / selective    │
│         ↓                                                   │
│  4. EXECUTE      Run updates with progress output           │
│         ↓                                                   │
│  5. VERIFY       Confirm tools still work                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Update (Tracked Tier Only)

Run this for routine maintenance:

```bash
# Homebrew (most common)
brew update && brew upgrade

# npm global packages
npm update -g

# macOS software updates (list only)
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
[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ] && echo "nvm: installed"   # a sourced function; command -v misses it
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

### Tier 1: TRACKED (what each manager already tracks)

| Tool | Command | Notes |
|------|---------|-------|
| Homebrew | `brew upgrade` | Outdated, unpinned formulae; can cross majors |
| npm | `npm update -g` | Installed globals |
| pipx | `pipx upgrade-all` | Python CLI tools, each in its own venv |
| Rust | `rustup update` | Stable toolchain |

**Commands:**
```bash
# Tracked tier - run all
brew update && brew outdated     # read what moves; `brew pin <formula>` holds one
brew upgrade
npm update -g
command -v pipx >/dev/null && pipx upgrade-all
rustup update stable 2>/dev/null
```

**Risk:** Low, not zero. Nothing here is bounded by semver; `brew outdated` shows the jumps first.

---

### Tier 2: NAMED (packages and apps you pick)

| Tool | Command | Notes |
|------|---------|-------|
| Homebrew casks | `brew upgrade --cask` | App updates |
| npm package | `npm install -g <pkg>@latest` | Moves to latest, majors included |
| pip packages | `pip install --upgrade <pkg>` | Inside the project's venv |

**Commands:**
```bash
# Homebrew casks (GUI apps)
brew upgrade --cask
```

**Risk:** Low-moderate. May require config changes.

---

### Tier 3: PLATFORM (OS, toolchains, runtimes)

| Tool | Command | Notes |
|------|---------|-------|
| macOS | `softwareupdate -ia` | Full system update |
| Xcode | App Store | May break builds |
| Python | `pyenv install X.Y` | New Python version |
| Node.js | `nvm install --lts` | New LTS line |
| Docker | Cask upgrade | Container compat |

**Commands:**
```bash
# macOS system updates
sudo softwareupdate -ia

# New Python version (pyenv)
pyenv install 3.12  # or latest
pyenv global 3.12

# Node LTS (nvm is a shell function: source it first)
. "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
nvm install --lts
nvm alias default 'lts/*'

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
# Homebrew's Python is externally managed (PEP 668): upgrade inside a venv, never globally
source .venv/bin/activate
pip install --upgrade pip

# Upgrade all packages in the venv (use with caution)
pip list --outdated --format=json | \
  python3 -c "import json,sys;print('\n'.join([p['name'] for p in json.load(sys.stdin)]))" | \
  xargs -n1 pip install -U

# CLI tools installed with pipx
pipx upgrade-all
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

1. **Detect** - Show all installed package managers
2. **Scan** - List outdated packages per manager
3. **Present tiers** - Let user choose update scope
4. **Execute** - Run updates with progress
5. **Verify** - Run quick health checks

### AskUserQuestion Structure

**Tier Selection:**
```
Question: "What update level should I run?"
Options:
  - Tracked only (brew, npm globals, pipx, rustup) - Low risk
  - Include named packages and casks - Some risk
  - Full update (including OS and runtimes) - Higher risk, review first
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
[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ] && . "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
npm update -g

echo -e "\n=== pipx ==="
if command -v pipx >/dev/null; then pipx upgrade-all; fi

echo -e "\n=== Rust ==="
if command -v rustup >/dev/null; then rustup update; fi

echo -e "\n=== Verification ==="
brew doctor || true   # exits 1 on any warning
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
| pip externally-managed | Use a venv, or `pipx install <tool>` for CLIs. `--break-system-packages` last: it can break the system Python |
| Xcode update breaks tools | `xcode-select --install` |
| Rust won't update | `rustup self update` first |
| Node version mismatch | Check nvm: `nvm current` vs `node --version` |

---

## Update Schedule

| Frequency | What to Update |
|-----------|----------------|
| Weekly | Tracked tier |
| Monthly | Tracked + named tiers |
| Quarterly | Platform tier (with testing) |
| As needed | Security patches immediately |

---

## Related Commands

- `/pb-doctor` - Check system health before/after updates
- `/pb-storage` - Clean up after updates (old versions)
- `/pb-setup` - Full environment setup
- `/pb-security` - Check for security updates

---

*Run weekly for tracked updates, monthly for full maintenance. Always verify after platform updates.*
