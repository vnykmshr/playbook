---
name: "pb-storage"
title: "macOS Storage Cleanup"
category: "utilities"
difficulty: "advanced"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-debug', 'pb-start']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# macOS Storage Cleanup

Tiered storage cleanup for developer machines. Reclaim disk space safely with user confirmation at each tier.

**Platform:** macOS only
**Risk Model:** Safe → Moderate → Aggressive (each tier requires explicit confirmation)

**Mindset:** Design Rules say "measure before optimizing" — check what's using space before cleaning.

**Resource Hint:** haiku — scanning directories and executing cleanup commands.

## When to Use

- Disk usage exceeds 80% (run `/pb-doctor` first to confirm)
- Build tools failing due to insufficient disk space
- Quarterly maintenance to prevent space issues from accumulating

---

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. SCAN         Detect installed toolchains, measure sizes │
│         ↓                                                   │
│  2. REPORT       Show current usage by category             │
│         ↓                                                   │
│  3. TIER SELECT  User chooses tier(s) to execute            │
│         ↓                                                   │
│  4. CONFIRM      Show items + sizes, require confirmation   │
│         ↓                                                   │
│  5. EXECUTE      Run cleanup with progress output           │
│         ↓                                                   │
│  6. VERIFY       Show before/after disk usage comparison    │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Scan Current State

Run these commands to assess storage:

```bash
# Overall disk usage
df -h /

# Scan major cleanup targets (run all, report sizes)
du -sh ~/Library/Caches 2>/dev/null || echo "Library/Caches: N/A"
du -sh ~/.cache 2>/dev/null || echo ".cache: N/A"
du -sh ~/.npm 2>/dev/null || echo ".npm: N/A"
du -sh ~/.gradle/caches 2>/dev/null || echo ".gradle: N/A"
du -sh ~/.pub-cache 2>/dev/null || echo ".pub-cache: N/A"
du -sh ~/Library/Android/sdk/system-images 2>/dev/null || echo "Android images: N/A"
du -sh ~/.android/avd 2>/dev/null || echo "Android AVDs: N/A"

# Docker (if installed)
docker system df 2>/dev/null || echo "Docker: not running"

# Homebrew
brew cleanup --dry-run 2>/dev/null | tail -3 || echo "Homebrew: N/A"
```

---

## Step 2: Tier Definitions

### Tier 1: SAFE (Always reversible, no side effects)

| Target | Path | Notes |
|--------|------|-------|
| Library Caches | `~/Library/Caches/*` | Apps regenerate on demand |
| User Cache | `~/.cache/*` | General cache directory |
| System Logs | `~/Library/Logs/*` | Old log files |
| Trash | `~/.Trash/*` | Already "deleted" items |
| Safari Cache | `~/Library/Safari/LocalStorage/*` | Browser regenerates |

**Commands:**
```bash
# Preview sizes first
du -sh ~/Library/Caches ~/.cache ~/Library/Logs ~/.Trash 2>/dev/null

# Execute (after confirmation)
rm -rf ~/Library/Caches/* 2>/dev/null
rm -rf ~/.cache/* 2>/dev/null
rm -rf ~/Library/Logs/* 2>/dev/null
rm -rf ~/.Trash/* 2>/dev/null
```

**Risk:** None. All items regenerate automatically.

---

### Tier 2: MODERATE (Rebuilds on next use)

| Target | Path | Notes |
|--------|------|-------|
| npm cache | `~/.npm/_cacache` | `npm install` rebuilds |
| Gradle caches | `~/.gradle/caches/*` | Next build downloads |
| pip cache | `~/Library/Caches/pip` | `pip install` rebuilds |
| Homebrew cache | `brew cleanup` | Old versions removed |
| pub-cache | `~/.pub-cache/*` | Flutter/Dart packages |
| CocoaPods | `~/Library/Caches/CocoaPods` | `pod install` rebuilds |
| Cargo cache | `~/.cargo/registry/cache` | Rust crates |

**Commands:**
```bash
# Preview sizes first
du -sh ~/.npm ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache 2>/dev/null

# Execute (after confirmation)
npm cache clean --force 2>/dev/null
rm -rf ~/.gradle/caches/* 2>/dev/null
rm -rf ~/Library/Caches/pip/* 2>/dev/null
brew cleanup 2>/dev/null
rm -rf ~/.pub-cache/* 2>/dev/null
rm -rf ~/Library/Caches/CocoaPods/* 2>/dev/null
rm -rf ~/.cargo/registry/cache/* 2>/dev/null
```

**Risk:** Low. Next build/install takes longer (re-downloads packages).

---

### Tier 3: AGGRESSIVE (May require reinstall/reconfiguration)

| Target | Path | Notes |
|--------|------|-------|
| Docker all | `docker system prune -a --volumes` | Removes ALL images, volumes |
| Android AVDs | `~/.android/avd/*.avd` | Must recreate emulators |
| Android system-images | `~/Library/Android/sdk/system-images/*` | Must re-download |
| iOS Simulators | `xcrun simctl delete unavailable` | Removes old simulators |
| Xcode DerivedData | `~/Library/Developer/Xcode/DerivedData/*` | Rebuilds on compile |
| Xcode Archives | `~/Library/Developer/Xcode/Archives/*` | Old app archives |
| Old Rust toolchains | `rustup toolchain uninstall` | Keeps default only |
| Node global modules | `/usr/local/lib/node_modules/*` | Must reinstall globals |

**Commands:**
```bash
# Preview sizes first
docker system df 2>/dev/null
du -sh ~/.android/avd ~/Library/Android/sdk/system-images 2>/dev/null
du -sh ~/Library/Developer/Xcode/DerivedData ~/Library/Developer/Xcode/Archives 2>/dev/null

# Execute (after confirmation)
docker system prune -a --volumes -f 2>/dev/null
rm -rf ~/.android/avd/*.avd ~/.android/avd/*.ini 2>/dev/null
rm -rf ~/Library/Android/sdk/system-images/* 2>/dev/null
xcrun simctl delete unavailable 2>/dev/null
rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null
rm -rf ~/Library/Developer/Xcode/Archives/* 2>/dev/null
rustup toolchain list 2>/dev/null | grep -v default | xargs -I {} rustup toolchain uninstall {} 2>/dev/null
```

**Risk:** Medium. Requires re-downloading images, recreating emulators, or reinstalling tools.

---

## Step 3: User Interaction Flow

When executing this playbook:

1. **Run scan** — Show current disk usage and detected toolchains
2. **Present tiers** — Use multi-select to let user choose which tier(s)
3. **Within each tier** — Show individual items with sizes
4. **Confirm before execute** — Require explicit "yes" before each tier runs
5. **Report results** — Show space reclaimed per tier

### AskUserQuestion Structure

**Tier Selection:**
```
Question: "Which cleanup tiers should I run?"
Options:
  - Tier 1: SAFE (~X GB) - Caches, logs, trash
  - Tier 2: MODERATE (~X GB) - Package manager caches
  - Tier 3: AGGRESSIVE (~X GB) - Docker, SDKs, emulators
MultiSelect: true
```

**Within-Tier Confirmation (for Tier 2 and 3):**
```
Question: "Tier 2 will clean these items. Proceed?"
Options:
  - Yes, clean all selected
  - Let me pick specific items
  - Skip this tier
```

---

## Step 4: Verification

After cleanup completes:

```bash
# Show new disk usage
df -h /

# Compare before/after
echo "Cleanup complete. Verify freed space above."
```

---

## Quick Commands (Expert Mode)

For users who know what they want:

```bash
# Safe tier only (no confirmation needed)
rm -rf ~/Library/Caches/* ~/.cache/* ~/Library/Logs/* ~/.Trash/* 2>/dev/null

# Full moderate tier
npm cache clean --force && rm -rf ~/.gradle/caches/* ~/.pub-cache/* && brew cleanup

# Nuclear option (all tiers, no prompts)
# WARNING: Only run if you understand all consequences
rm -rf ~/Library/Caches/* ~/.cache/* ~/Library/Logs/* ~/.Trash/*
npm cache clean --force && rm -rf ~/.gradle/caches/* ~/.pub-cache/* && brew cleanup
docker system prune -a --volumes -f
rm -rf ~/.android/avd/*.avd ~/Library/Android/sdk/system-images/*
rm -rf ~/Library/Developer/Xcode/DerivedData/*
```

---

## What This Does NOT Clean

Items requiring manual decision (not automated):

| Item | Why Manual |
|------|------------|
| `~/Downloads` | May contain wanted files |
| `~/Documents` | User data |
| `node_modules` in projects | Breaks projects until reinstall |
| `.env` files | Contains secrets |
| Git repositories | User code |
| Application data | App-specific, may lose settings |

---

## Scheduling (Optional)

For automatic maintenance, add to crontab:

```bash
# Run safe tier weekly (Sunday 3am)
0 3 * * 0 rm -rf ~/Library/Caches/* ~/.cache/* ~/Library/Logs/* 2>/dev/null
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" | Some caches locked by running apps. Quit apps first. |
| Docker won't prune | Start Docker Desktop first |
| Space not freed immediately | macOS may delay reporting. Run `sudo purge` to update |
| Xcode paths not found | Xcode not installed, skip those items |

---

## Related Commands

- `/pb-debug` — Troubleshoot issues after aggressive cleanup
- `/pb-start` — Resume development after cleanup

---

*Run quarterly or when disk usage exceeds 80%.*
