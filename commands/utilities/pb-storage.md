---
name: "pb-storage"
title: "macOS Storage Cleanup"
category: "utilities"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-debug', 'pb-start']
last_reviewed: "2026-07-28"
last_evolved: "2026-07-28"
version: "1.1.0"
version_notes: "v1.1.0: ~/.cache moves to Tier 2 and is enumerated, never globbed -- it holds model weights and VM images that do not regenerate, so it cannot sit in a tier labelled always-reversible. Measure the APFS Data volume, not `/`. One zsh-safe deletion idiom throughout. Full Disk Access documented for ~/.Trash."
breaking_changes: []
---
# macOS Storage Cleanup

Tiered storage cleanup for developer machines. Reclaim disk space safely with user confirmation at each tier.

**Platform:** macOS only
**Risk Model:** Safe → Moderate → Aggressive (each tier requires explicit confirmation)

**Mindset:** Design Rules say "measure before optimizing" - check what's using space before cleaning.

**Resource Hint:** sonnet - Storage analysis and safe cleanup with careful file operations.

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
# Overall disk usage. On APFS, `/` is the read-only signed SYSTEM volume and its capacity
# percentage is effectively constant -- measured on a real machine, `df -h /` said 24%
# while the Data volume holding everything was at 84%. Measure the Data volume.
VOL=$([ -d /System/Volumes/Data ] && echo /System/Volumes/Data || echo /)
df -h "$VOL"

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
| System Logs | `~/Library/Logs/*` | Old log files |
| Trash | `~/.Trash/*` | Already "deleted" items |
| Safari Cache | `~/Library/Safari/LocalStorage/*` | Browser regenerates |

`~/.cache` is **not** in this tier -- see Tier 2, it holds things that do not come back.

**Commands:**
```bash
# Preview sizes first
du -sh ~/Library/Caches ~/Library/Logs ~/.Trash 2>/dev/null

# Execute (after confirmation). One idiom, no globs: in zsh a glob that matches nothing --
# an empty ~/.Trash -- aborts the whole `rm` before it deletes any of its OTHER arguments
# and exits 1, which the `2>/dev/null` these lines used to carry turned into silence.
# Pointing `find` at the directory has no such failure mode: nothing to match is nothing to do.
find ~/Library/Caches -mindepth 1 -maxdepth 1 -exec rm -rf {} +
find ~/Library/Logs   -mindepth 1 -maxdepth 1 -exec rm -rf {} +
find ~/.Trash         -mindepth 1 -maxdepth 1 -exec rm -rf {} +
```

**Risk:** None for the listed paths.

**`~/.Trash` needs Full Disk Access.** Without it macOS returns `Operation not permitted` and deletes
nothing. Grant it under System Settings -> Privacy & Security -> Full Disk Access, or empty the Trash
from Finder instead.

**Apps holding files open** (Chrome especially) will produce `Directory not empty` as they recreate
what `rm` removes. Harmless; check the size afterwards rather than trusting the error.

---

### Tier 2: MODERATE (Rebuilds on next use)

| Target | Path | Notes |
|--------|------|-------|
| User Cache | `~/.cache/*` | **Enumerate first -- see below.** Not everything here rebuilds |
| npm cache | `~/.npm/_cacache` | `npm install` rebuilds |
| Gradle caches | `~/.gradle/caches/*` | Next build downloads |
| pip cache | `~/Library/Caches/pip` | `pip install` rebuilds |
| Homebrew cache | `brew cleanup` | Old versions removed |
| pub-cache | `~/.pub-cache/*` | Flutter/Dart packages |
| CocoaPods | `~/Library/Caches/CocoaPods` | `pod install` rebuilds |
| Cargo cache | `~/.cargo/registry/cache` | Rust crates |

**`~/.cache` is a convention, not a guarantee** -- which is why it sits here and not in Tier 1. Tools
park things there that no amount of waiting brings back: downloaded model weights, provisioned VM
images, vendored toolchains. One real case: a hand-downloaded speech model under `~/.cache`, which a
project depended on for its verification stage. A blanket `rm -rf ~/.cache/*` would have broken that
pipeline silently, and "the cache regenerates" would have been the reason nobody looked there.

**Enumerate before deleting, and exclude by name:**

```bash
# 1. LOOK. One line per entry, largest first. Decide what is genuinely a cache.
du -sh ~/.cache/* 2>/dev/null | sort -rh

# 2. Delete everything EXCEPT what you just decided to keep. The exclusions are YOURS --
#    they come from step 1 on THIS machine. There is no correct default list.
find ~/.cache -mindepth 1 -maxdepth 1 ! -name <keep-this> ! -name <and-this> -exec rm -rf {} +
```

This step needs a human. That is the reason `~/.cache` never appears in the unattended blocks below.

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

1. **Run scan** - Show current disk usage and detected toolchains
2. **Present tiers** - Use multi-select to let user choose which tier(s)
3. **Within each tier** - Show individual items with sizes
4. **Confirm before execute** - Require explicit "yes" before each tier runs
5. **Report results** - Show space reclaimed per tier

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
# Show new disk usage (the Data volume, same as the scan)
df -h "$([ -d /System/Volumes/Data ] && echo /System/Volumes/Data || echo /)"

# Compare before/after
echo "Cleanup complete. Verify freed space above."
```

---

## Quick Commands (Expert Mode)

For users who know what they want:

```bash
# Safe tier only. ~/.cache is OMITTED on purpose -- it needs the enumerate step, which needs you.
find ~/Library/Caches ~/Library/Logs ~/.Trash -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# Full moderate tier
npm cache clean --force && rm -rf ~/.gradle/caches/* ~/.pub-cache/* && brew cleanup

# Nuclear option (all tiers, no prompts)
# WARNING: Only run if you understand all consequences. ~/.cache is STILL absent here --
# "nuclear" means you accept re-downloading caches, not silently destroying a model file
# that never comes back.
find ~/Library/Caches ~/Library/Logs ~/.Trash -mindepth 1 -maxdepth 1 -exec rm -rf {} +
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
# Run safe tier weekly (Sunday 3am). Same idiom as everywhere else -- cron runs /bin/sh, where an
# unmatched glob passes through literally rather than aborting, which is its own quiet way to be wrong.
# ~/.Trash is omitted (cron has no Full Disk Access) and so is ~/.cache (it needs a human).
0 3 * * 0 find ~/Library/Caches ~/Library/Logs -mindepth 1 -maxdepth 1 -exec rm -rf {} +
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" | Some caches locked by running apps. Quit apps first. |
| "Operation not permitted" on `~/.Trash` | Terminal lacks Full Disk Access. Grant it in System Settings -> Privacy & Security, or empty Trash from Finder. |
| Docker won't prune | Start Docker Desktop first |
| Space not freed immediately | macOS may delay reporting. Run `sudo purge` to update |
| Xcode paths not found | Xcode not installed, skip those items |

---

## Related Commands

- `/pb-debug` - Troubleshoot issues after aggressive cleanup
- `/pb-start` - Resume development after cleanup

---

*Run quarterly or when disk usage exceeds 80%.*
