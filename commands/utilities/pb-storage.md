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
version: "1.2.0"
version_notes: "v1.2.0: dry run before every tier, and a tier audit against the membership test ~/.cache failed -- can this be deleted without a human deciding anything? Five more rows failed it: ~/.Trash and Safari LocalStorage leave Tier 1, docker --volumes and Xcode Archives leave the sweep entirely, ~/.pub-cache gains its executables caveat. Tier 1's Caches glob is documented as subsuming two Tier 2 rows. v1.1.0: ~/.cache moves to Tier 2 and is enumerated, never globbed -- it holds model weights and VM images that do not regenerate, so it cannot sit in a tier labelled always-reversible. Measure the APFS Data volume, not `/`. One zsh-safe deletion idiom throughout. Full Disk Access documented for ~/.Trash."
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

**The membership test for this tier:** *can it be deleted without a human deciding anything?*
If the answer needs a look first, it is not Tier 1. Two paths that used to live here failed
that test and moved -- see the tier notes below.

| Target | Path | Notes |
|--------|------|-------|
| Library Caches | `~/Library/Caches/*` | Apps regenerate on demand. This glob **subsumes** the `pip` and `CocoaPods` rows in Tier 2 -- running Tier 1 alone already clears them |
| System Logs | `~/Library/Logs/*` | Old log files |

Three paths that look like they belong here and do not: `~/.cache` (Tier 2 -- holds things that
never come back), `~/.Trash` (Tier 2 -- irreversible, and *you* put those files there),
`~/Library/Safari/LocalStorage` (not cleaned at all -- it is site data, not cache).

**Commands:**
```bash
# Preview sizes first
du -sh ~/Library/Caches ~/Library/Logs 2>/dev/null

# 1. DRY RUN -- always. Same command, `echo` in place of `rm -rf`. Read the list.
find ~/Library/Caches ~/Library/Logs -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +

# 2. Execute. One idiom, no globs: in zsh a glob that matches nothing -- an empty directory --
#    aborts the whole `rm` before it deletes any of its OTHER arguments and exits 1, which the
#    `2>/dev/null` these lines used to carry turned into silence. Pointing `find` at the
#    directory has no such failure mode: nothing to match is nothing to do.
find ~/Library/Caches -mindepth 1 -maxdepth 1 -exec rm -rf {} +
find ~/Library/Logs   -mindepth 1 -maxdepth 1 -exec rm -rf {} +
```

**Risk:** None for the listed paths.

**Apps holding files open** (Chrome especially) will produce `Directory not empty` as they recreate
what `rm` removes. Harmless; check the size afterwards rather than trusting the error.

---

### Tier 2: MODERATE (Rebuilds on next use)

| Target | Path | Notes |
|--------|------|-------|
| User Cache | `~/.cache/*` | **Enumerate first -- see below.** Not everything here rebuilds |
| Trash | `~/.Trash/*` | **Irreversible, and not a cache** -- you put these here and have not confirmed deletion. Look before emptying |
| npm cache | `~/.npm/_cacache` | `npm install` rebuilds |
| Gradle caches | `~/.gradle/caches/*` | Next build downloads |
| pip cache | `~/Library/Caches/pip` | `pip install` rebuilds |
| Homebrew cache | `brew cleanup` | Old versions removed |
| pub-cache | `~/.pub-cache/*` | Flutter/Dart packages -- also holds `dart pub global activate` executables, which need reinstalling, not just re-downloading |
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
# 1. DRY RUN -- sizes, then exactly what would go.
du -sh ~/.npm ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache ~/.Trash 2>/dev/null
brew cleanup --dry-run 2>/dev/null
find ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache ~/.Trash -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +

# 2. Execute (after reading the list above).
npm cache clean --force
brew cleanup
find ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# ~/.Trash is deliberately separate -- emptying it is irreversible. Empty it only after
# reading the dry run, and note it needs Full Disk Access (see Troubleshooting).
find ~/.Trash -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# ~/.cache: use the enumerate-then-exclude form above, never a blanket sweep.
```

**Risk:** Low for the package caches -- next build/install takes longer. `~/.Trash` is the
exception in this tier: it does not rebuild, it is gone.

---

### Tier 3: AGGRESSIVE (May require reinstall/reconfiguration)

| Target | Path | Notes |
|--------|------|-------|
| Docker images | `docker system prune -a` | Removes all unused images. Re-pull to recover |
| Android AVDs | `~/.android/avd/*.avd` | Must recreate emulators; installed apps and state inside them are lost |
| Android system-images | `~/Library/Android/sdk/system-images/*` | Must re-download |
| iOS Simulators | `xcrun simctl delete unavailable` | Only removes runtimes you no longer have |
| Xcode DerivedData | `~/Library/Developer/Xcode/DerivedData/*` | Rebuilds on compile |
| Old Rust toolchains | `rustup toolchain uninstall` | Keeps default only |
| Node global modules | `/usr/local/lib/node_modules/*` | Must reinstall globals |

**Two things this tier deliberately does not sweep**, because "reinstall or reconfigure" undersells
what they cost:

- **`docker system prune --volumes`.** Named volumes are *data* -- your local Postgres, the seeded
  test database, whatever a compose file mounted. That is not reconfiguration, it is data loss, and
  no amount of re-pulling brings it back. Run `docker volume ls` first, and add `--volumes` only once
  you have looked at that list.
- **`~/Library/Developer/Xcode/Archives`.** Archives carry the dSYMs for builds you shipped. Without
  them you cannot symbolicate a crash report from a release already in users' hands. Delete archives
  for builds that never shipped; keep the rest, however old they look.

**Commands:**
```bash
# Preview sizes first
docker system df 2>/dev/null
du -sh ~/.android/avd ~/Library/Android/sdk/system-images 2>/dev/null
du -sh ~/Library/Developer/Xcode/DerivedData ~/Library/Developer/Xcode/Archives 2>/dev/null

# DRY RUN first -- this tier is the one where a mistake costs an afternoon.
docker system prune -a --dry-run 2>/dev/null || docker system df
docker volume ls                                   # volumes are NOT pruned below; look anyway
find ~/.android/avd ~/Library/Android/sdk/system-images \
     ~/Library/Developer/Xcode/DerivedData -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +
rustup toolchain list 2>/dev/null

# Execute (after reading the above)
docker system prune -a -f                          # NO --volumes; see the note above
find ~/.android/avd -mindepth 1 -maxdepth 1 \( -name '*.avd' -o -name '*.ini' \) -exec rm -rf {} +
find ~/Library/Android/sdk/system-images -mindepth 1 -maxdepth 1 -exec rm -rf {} +
xcrun simctl delete unavailable
find ~/Library/Developer/Xcode/DerivedData -mindepth 1 -maxdepth 1 -exec rm -rf {} +
rustup toolchain list 2>/dev/null | grep -v default | xargs -I {} rustup toolchain uninstall {}
# Xcode Archives: not swept. Delete per-archive, only for builds you never shipped.
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

Expert mode is the *dry run* run first, every time. Swap `echo "WOULD DELETE"` for `rm -rf` once
you have read the list -- that substitution is the whole ritual.

```bash
# Dry run, any tier: same paths, harmless verb.
find <paths> -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +

# Safe tier. ~/.cache and ~/.Trash are OMITTED on purpose -- both need a human first.
find ~/Library/Caches ~/Library/Logs -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# Full moderate tier (minus ~/.cache and ~/.Trash, same reason)
npm cache clean --force && brew cleanup
find ~/.gradle/caches ~/.pub-cache ~/Library/Caches/pip ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# Nuclear (all tiers, no prompts). "Nuclear" means accepting re-downloads -- NOT destroying
# data. So it still excludes ~/.cache, ~/.Trash, docker volumes and Xcode Archives; each of
# those is unrecoverable and needs you to look first. There is no flag for that.
find ~/Library/Caches ~/Library/Logs -mindepth 1 -maxdepth 1 -exec rm -rf {} +
npm cache clean --force && brew cleanup
find ~/.gradle/caches ~/.pub-cache ~/Library/Caches/pip ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache -mindepth 1 -maxdepth 1 -exec rm -rf {} +
docker system prune -a -f
find ~/.android/avd ~/Library/Android/sdk/system-images \
     ~/Library/Developer/Xcode/DerivedData -mindepth 1 -maxdepth 1 -exec rm -rf {} +
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
| `~/Library/Safari/LocalStorage` | **Site data, not cache** -- web apps persist drafts, offline data and signed-in state here. It does not regenerate. Safari's actual cache is `~/Library/Caches/com.apple.Safari` |
| Docker named volumes | Databases and seeded test data. `docker volume ls` first; `--volumes` is opt-in |
| `~/Library/Developer/Xcode/Archives` | dSYMs for shipped builds -- needed to symbolicate crash reports from releases already in users' hands |

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
