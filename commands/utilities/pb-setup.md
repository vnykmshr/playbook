---
name: "pb-setup"
title: "Bootstrap Dev Machine"
category: "utilities"
difficulty: "advanced"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-doctor', 'pb-update', 'pb-storage', 'pb-start']
tags: ['design', 'security', 'workflow', 'review', 'documentation']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Bootstrap Dev Machine

Set up a new Mac for development from scratch. Opinionated defaults with escape hatches for customization.

**Platform:** macOS
**Use Case:** New machine, nuke-and-pave, or standardizing team setups

**Mindset:** Design Rules emphasize "simple by default" — install only what's needed, configure minimally.

**Resource Hint:** haiku — installation commands and configuration are mechanical and well-defined.

## When to Use

- Setting up a brand new Mac for development
- Reinstalling after an OS wipe or nuke-and-pave
- Standardizing team dev environments with a shared Brewfile
- Onboarding a new team member who needs a working setup quickly

---

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. PREFLIGHT    Verify macOS, accept Xcode license        │
│         ↓                                                   │
│  2. FOUNDATION   Homebrew, git, shell setup                 │
│         ↓                                                   │
│  3. LANGUAGES    Node, Python, Go, Rust (as needed)         │
│         ↓                                                   │
│  4. TOOLS        Docker, editors, CLI utilities             │
│         ↓                                                   │
│  5. CONFIG       Dotfiles, SSH keys, git config             │
│         ↓                                                   │
│  6. VERIFY       Run health check                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Preflight

### Accept Xcode License

```bash
# Install command line tools (if not present)
xcode-select --install 2>/dev/null || true

# Accept Xcode license
sudo xcodebuild -license accept 2>/dev/null || true
```

### Verify macOS Version

```bash
sw_vers

# Recommended: macOS 13+ (Ventura or later)
```

---

## Phase 2: Foundation

### Install Homebrew

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (Apple Silicon)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Verify
brew --version
```

### Core CLI Tools

```bash
brew install \
  git \
  gh \
  jq \
  ripgrep \
  fd \
  fzf \
  tree \
  htop \
  wget \
  curl
```

### Shell Setup (zsh)

```bash
# Oh My Zsh (optional but common)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Or keep vanilla zsh with just essentials
touch ~/.zshrc
```

---

## Phase 3: Languages

### Node.js (via nvm)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell
source ~/.zshrc

# Install Node LTS
nvm install --lts
nvm alias default lts/*

# Verify
node --version
npm --version
```

### Python (via pyenv)

```bash
# Install pyenv
brew install pyenv

# Add to shell
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# Install Python
pyenv install 3.12
pyenv global 3.12

# Verify
python3 --version
pip3 --version
```

### Go

```bash
# Install Go
brew install go

# Set up GOPATH
echo 'export GOPATH=$HOME/go' >> ~/.zshrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc

# Verify
go version
```

### Rust

```bash
# Install Rust via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Reload shell
source ~/.cargo/env

# Verify
rustc --version
cargo --version
```

---

## Phase 4: Development Tools

### Docker

```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop manually, then verify
docker --version
docker compose version
```

### Editors

```bash
# VS Code
brew install --cask visual-studio-code

# Or your preferred editor
# brew install --cask cursor
# brew install --cask zed
# brew install neovim
```

### Database Tools (as needed)

```bash
# PostgreSQL client
brew install libpq
brew link --force libpq

# Or full PostgreSQL
# brew install postgresql@16

# Redis
# brew install redis

# MongoDB tools
# brew tap mongodb/brew
# brew install mongodb-database-tools
```

### Additional CLI Tools

```bash
brew install \
  lazygit \
  bat \
  eza \
  delta \
  tldr
```

---

## Phase 5: Configuration

### Git Configuration

```bash
# Identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Defaults
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true

# Better diffs (if delta installed)
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"

# Aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
```

### SSH Key

```bash
# Generate SSH key (if not restoring from backup)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add to keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Copy public key
pbcopy < ~/.ssh/id_ed25519.pub
echo "SSH public key copied to clipboard. Add to GitHub/GitLab."
```

### GitHub CLI Authentication

```bash
# Authenticate with GitHub
gh auth login

# Verify
gh auth status
```

### Dotfiles (if you have them)

```bash
# Clone your dotfiles repo
git clone git@github.com:YOUR_USERNAME/dotfiles.git ~/.dotfiles

# Run your install script
cd ~/.dotfiles && ./install.sh
```

---

## Phase 6: Verification

Run the health check:

```bash
echo "=== Verification ==="
echo "Homebrew: $(brew --version | head -1)"
echo "Git: $(git --version)"
echo "Node: $(node --version)"
echo "npm: $(npm --version)"
echo "Python: $(python3 --version)"
echo "Go: $(go version 2>/dev/null || echo 'Not installed')"
echo "Rust: $(rustc --version 2>/dev/null || echo 'Not installed')"
echo "Docker: $(docker --version 2>/dev/null || echo 'Not running')"

# Run full doctor check
# /pb-doctor
```

---

## Brewfile (Declarative Setup)

For repeatable setups, use a Brewfile:

```bash
# Create Brewfile
cat > ~/Brewfile << 'EOF'
# Taps
tap "homebrew/bundle"
tap "homebrew/cask"

# CLI Tools
brew "git"
brew "gh"
brew "jq"
brew "ripgrep"
brew "fd"
brew "fzf"
brew "tree"
brew "htop"
brew "bat"
brew "eza"
brew "lazygit"

# Languages
brew "pyenv"
brew "go"

# Apps
cask "docker"
cask "visual-studio-code"
cask "rectangle"
cask "1password"
EOF

# Install everything
brew bundle --file=~/Brewfile
```

---

## User Interaction Flow

When executing this playbook:

1. **Preflight** — Check macOS version, Xcode status
2. **Select stack** — Ask what languages/tools needed
3. **Execute phases** — Run with progress updates
4. **Configure** — Walk through git config, SSH setup
5. **Verify** — Run health check

### AskUserQuestion Structure

**Stack Selection:**
```
Question: "What development stack do you need?"
Options:
  - Full stack web (Node, Python, Docker)
  - Frontend (Node only)
  - Backend (Python, Go, Docker)
  - Systems (Rust, Go)
MultiSelect: false
```

**Additional Tools:**
```
Question: "Which additional tools?"
Options:
  - Docker Desktop
  - VS Code
  - PostgreSQL
  - Redis
MultiSelect: true
```

---

## Quick Setup Script

One-liner for the brave (installs essentials):

```bash
# WARNING: Review before running
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
eval "$(/opt/homebrew/bin/brew shellenv)" && \
brew install git gh jq ripgrep fd fzf && \
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
source ~/.zshrc && nvm install --lts
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Homebrew permission denied | `sudo chown -R $(whoami) /opt/homebrew` |
| Xcode license not accepted | `sudo xcodebuild -license accept` |
| nvm: command not found | Add nvm init to shell profile, restart terminal |
| pyenv: python not found | `eval "$(pyenv init -)"` in profile |
| Docker won't start | Open Docker Desktop app first, accept terms |
| SSH key not working | Check `ssh-add -l`, ensure key added |

---

## Post-Setup Checklist

- [ ] Homebrew installed and working
- [ ] Git configured with name and email
- [ ] SSH key generated and added to GitHub/GitLab
- [ ] Primary language runtime installed
- [ ] Docker running (if needed)
- [ ] Editor installed and configured
- [ ] Clone essential repos
- [ ] Run `/pb-doctor` to verify health

---

## Related Commands

- `/pb-doctor` — Verify system health after setup
- `/pb-update` — Keep tools current
- `/pb-storage` — Clean up if disk gets full
- `/pb-start` — Begin development work

---

*Run on new machines or after OS reinstall. Keep Brewfile in dotfiles for repeatability.*
