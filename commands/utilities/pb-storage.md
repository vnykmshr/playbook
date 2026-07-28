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
version: "2.0.0"
version_notes: "v2.0.0: tiers re-cut on time to recover -- SECONDS / A BUILD / A DOWNLOAD / NEVER -- replacing SAFE / MODERATE / AGGRESSIVE. The old scale described how a deletion felt; recovery time describes what it costs, and it exposes the offline question the old names could not ask: Tier 3 needs a network, so do not clear it before a flight. Tier 4 is not a tier you run. v1.2.0: dry run before every tier, and a tier audit against the membership test ~/.cache failed -- can this be deleted without a human deciding anything? Five more rows failed it. v1.1.0: ~/.cache out of the always-reversible tier and enumerated, never globbed. Measure the APFS Data volume, not `/`. One zsh-safe deletion idiom throughout. Full Disk Access documented for ~/.Trash."
breaking_changes: ['Tier names and membership changed: SAFE/MODERATE/AGGRESSIVE -> SECONDS/A BUILD/A DOWNLOAD/NEVER. A script or habit that ran "Tier 1" now sweeps less (~/.Trash left it) and "Tier 3" now means network-recoverable rather than most-destructive. Re-read the tier tables before reusing any saved invocation.']
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

Tiers are cut on **how long it takes to get the thing back**, because that is the question you
are actually answering at 2am with a full disk. "Safe" and "aggressive" describe how the deletion
feels; recovery time describes what it costs you, and only one of those is checkable.

| Tier | Recovery | Needs network? | Use when |
|------|----------|----------------|----------|
| 1 | **Seconds** -- regenerates on its own | No | Always. Start here |
| 2 | **A build** -- local compute, once | No | You can afford one slow compile |
| 3 | **A download** -- refetched over the network | **Yes** | You are online and staying online |
| 4 | **Never** -- gone | n/a | Never sweep. Decide per item, or not at all |

**The membership test, applied to every row:** *can this be deleted without a human deciding
anything, and if so, what does getting it back cost?* A path whose answer is "it depends what is
in it" belongs in Tier 4 no matter how cache-shaped its name is.

**Read Tier 3 before a flight.** Clearing a download-tier cache on Tuesday costs a coffee; clearing
it an hour before you board costs you the afternoon. This is the distinction the old
safe/moderate/aggressive scale could not express.

---

### Tier 1: SECONDS (regenerates on its own, offline)

| Target | Path | Recovery |
|--------|------|----------|
| Library Caches | `~/Library/Caches/*` | Apps repopulate on next launch. This glob **subsumes** the `pip` and `CocoaPods` rows in Tier 3 -- running Tier 1 alone already clears them, and those are downloads |
| System Logs | `~/Library/Logs/*` | Regenerate as apps run. Skip if you are mid-investigation: they are your evidence, and deleting them is the one way this tier costs you something |

**Commands:**
```bash
# 1. DRY RUN -- always. Same command, `echo` in place of `rm -rf`. Read the list.
find ~/Library/Caches ~/Library/Logs -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +

# 2. Execute. One idiom, no globs: in zsh a glob that matches nothing -- an empty directory --
#    aborts the whole `rm` before it deletes any of its OTHER arguments and exits 1, which a
#    `2>/dev/null` turns into silence. Pointing `find` at the directory has no such failure
#    mode: nothing to match is nothing to do.
find ~/Library/Caches -mindepth 1 -maxdepth 1 -exec rm -rf {} +
find ~/Library/Logs   -mindepth 1 -maxdepth 1 -exec rm -rf {} +
```

**Apps holding files open** (Chrome especially) will produce `Directory not empty` as they recreate
what `rm` removes. Harmless; check the size afterwards rather than trusting the error.

---

### Tier 2: A BUILD (local compute, offline-safe)

| Target | Path | Recovery |
|--------|------|----------|
| Xcode DerivedData | `~/Library/Developer/Xcode/DerivedData/*` | Next compile rebuilds it. Frequently the single largest reclaim on a Mac, and it costs you one slow build and no network |

**Commands:**
```bash
# DRY RUN
find ~/Library/Developer/Xcode/DerivedData -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +

# Execute
find ~/Library/Developer/Xcode/DerivedData -mindepth 1 -maxdepth 1 -exec rm -rf {} +
```

**Recovery:** one clean build per project you return to. Nothing is fetched.

---

### Tier 3: A DOWNLOAD (needs network -- check your connectivity first)

| Target | Path / Command | Recovery |
|--------|----------------|----------|
| npm cache | `~/.npm/_cacache` | `npm install` refetches |
| Gradle caches | `~/.gradle/caches/*` | Next build refetches |
| pip cache | `~/Library/Caches/pip` | `pip install` refetches |
| Homebrew | `brew cleanup` | Refetches on next install |
| CocoaPods | `~/Library/Caches/CocoaPods` | `pod install` refetches |
| Cargo registry | `~/.cargo/registry/cache` | `cargo build` refetches crates |
| pub-cache | `~/.pub-cache/*` | Refetches packages -- **also holds `dart pub global activate` executables**, which need reinstalling, not just refetching |
| Docker images | `docker system prune -a` | Re-pull. **No `--volumes`** -- see Tier 4 |
| Android system-images | `~/Library/Android/sdk/system-images/*` | Re-download, and these are large |
| iOS simulators | `xcrun simctl delete unavailable` | Only removes sims whose runtime is already gone; recreating needs a runtime download |
| Rust toolchains | `rustup toolchain uninstall` | Re-download; keeps default only |
| Node globals | `/usr/local/lib/node_modules/*` | `npm i -g` again |

**Commands:**
```bash
# 1. DRY RUN -- sizes, then exactly what would go.
du -sh ~/.npm ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache 2>/dev/null
brew cleanup --dry-run 2>/dev/null
docker system prune -a --dry-run 2>/dev/null || docker system df
docker volume ls                                   # volumes are NOT pruned below; look anyway
rustup toolchain list 2>/dev/null
find ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache ~/Library/Android/sdk/system-images \
     -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +

# 2. Execute (after reading the list, and while you still have bandwidth).
npm cache clean --force
brew cleanup
find ~/.gradle/caches ~/Library/Caches/pip ~/.pub-cache ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache ~/Library/Android/sdk/system-images \
     -mindepth 1 -maxdepth 1 -exec rm -rf {} +
docker system prune -a -f                          # NO --volumes; see Tier 4
xcrun simctl delete unavailable
rustup toolchain list 2>/dev/null | grep -v default | xargs -I {} rustup toolchain uninstall {}
```

**Recovery:** bandwidth and time. Do not run this tier on a tethered connection or before you
need to be productive offline.

---

### Tier 4: NEVER (unrecoverable -- decide per item, never sweep)

These look like cleanup targets. They are not. Nothing here is swept by any command on this page,
including the nuclear block, because no flag can make the decision for you.

| Target | Path | What you actually lose |
|--------|------|------------------------|
| User Cache | `~/.cache/*` | **Enumerate first.** A convention, not a guarantee -- it holds downloaded model weights, provisioned VM images, vendored toolchains |
| Trash | `~/.Trash/*` | Files *you* put there and have not confirmed deleting. "Already deleted" is the same reasoning that nearly cost a model file |
| Docker named volumes | `docker volume ls` | Databases. Your local Postgres, the seeded test data. Re-pulling an image does not bring data back |
| Xcode Archives | `~/Library/Developer/Xcode/Archives/*` | dSYMs for builds you shipped. Without them you cannot symbolicate a crash report from a release already in users' hands |
| Safari LocalStorage | `~/Library/Safari/LocalStorage/*` | Site data -- drafts, offline state, signed-in sessions. It does not regenerate. Safari's actual cache is `~/Library/Caches/com.apple.Safari` |
| Android AVDs | `~/.android/avd/*.avd` | The emulator is a download; the state inside it -- installed apps, configuration -- is not |

**`~/.cache`: enumerate, then exclude by name.**

```bash
# 1. LOOK. One line per entry, largest first. Decide what is genuinely a cache.
du -sh ~/.cache/* 2>/dev/null | sort -rh

# 2. Delete everything EXCEPT what you just decided to keep. The exclusions are YOURS --
#    they come from step 1 on THIS machine. There is no correct default list.
find ~/.cache -mindepth 1 -maxdepth 1 ! -name <keep-this> ! -name <and-this> -exec rm -rf {} +
```

**`~/.Trash`: empty it deliberately, from Finder or after reading a dry run.** It also needs Full
Disk Access; without it macOS returns `Operation not permitted` and deletes nothing.

```bash
find ~/.Trash -mindepth 1 -maxdepth 1 -exec echo "WOULD DELETE" {} +   # look first
find ~/.Trash -mindepth 1 -maxdepth 1 -exec rm -rf {} +                # then, if you mean it
```

**Recovery:** none. That is the whole tier.


---

## Step 3: User Interaction Flow

When executing this playbook:

1. **Run scan** - Show current disk usage and detected toolchains
2. **Present tiers** - Use multi-select to let user choose which tier(s)
3. **Within each tier** - Show individual items with sizes
4. **Confirm before execute** - Require explicit "yes" before each tier runs
5. **Report results** - Show space reclaimed per tier

### AskUserQuestion Structure

**Tier Selection** -- lead with recovery cost, since that is the choice being made:
```
Question: "Which cleanup tiers should I run?"
Options:
  - Tier 1: SECONDS (~X GB) - app caches and logs, regenerate on their own
  - Tier 2: A BUILD (~X GB) - Xcode DerivedData, costs one compile, no network
  - Tier 3: A DOWNLOAD (~X GB) - package caches, Docker images, SDKs. NEEDS NETWORK
MultiSelect: true
```

Tier 4 is never offered. It is not a tier you run.

**Before offering Tier 3, ask about connectivity** -- it is the only tier that can leave someone
stuck. If they are about to travel, tether, or demo, say so and let them decline:
```
Question: "Tier 3 refetches over the network. Are you staying online?"
Options:
  - Yes, run it
  - Skip Tier 3 - I need to work offline soon
```

**Within-Tier Confirmation (Tiers 2 and 3):**
```
Question: "Tier 3 will clean these items. Proceed?"
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

# Tier 1 -- SECONDS. Offline-safe.
find ~/Library/Caches ~/Library/Logs -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# Tier 2 -- A BUILD. Offline-safe; costs one compile.
find ~/Library/Developer/Xcode/DerivedData -mindepth 1 -maxdepth 1 -exec rm -rf {} +

# Tier 3 -- A DOWNLOAD. NEEDS NETWORK. Do not run this before going offline.
npm cache clean --force && brew cleanup
find ~/.gradle/caches ~/.pub-cache ~/Library/Caches/pip ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache ~/Library/Android/sdk/system-images \
     -mindepth 1 -maxdepth 1 -exec rm -rf {} +
docker system prune -a -f                          # NO --volumes
xcrun simctl delete unavailable
rustup toolchain list 2>/dev/null | grep -v default | xargs -I {} rustup toolchain uninstall {}

# Everything (Tiers 1-3, no prompts). "Everything" means accepting rebuilds and re-downloads --
# never destroying data. Tier 4 is absent by construction: ~/.cache, ~/.Trash, docker volumes,
# Xcode Archives, Safari LocalStorage and AVD state each need you to look first, and no flag
# can do that for you.
find ~/Library/Caches ~/Library/Logs ~/Library/Developer/Xcode/DerivedData \
     -mindepth 1 -maxdepth 1 -exec rm -rf {} +
npm cache clean --force && brew cleanup
find ~/.gradle/caches ~/.pub-cache ~/Library/Caches/pip ~/Library/Caches/CocoaPods \
     ~/.cargo/registry/cache ~/Library/Android/sdk/system-images \
     -mindepth 1 -maxdepth 1 -exec rm -rf {} +
docker system prune -a -f
```

---

## What This Does NOT Clean

Your data. These are not storage-cleanup candidates at any tier -- they are listed so nobody
scripts them by accident.

| Item | Why |
|------|-----|
| `~/Downloads` | May contain wanted files |
| `~/Documents` | User data |
| `node_modules` in projects | Breaks projects until reinstall |
| `.env` files | Contains secrets |
| Git repositories | User code |
| Application data | App-specific, may lose settings |

Distinct from **Tier 4**, which lists paths that *do* look like cleanup targets -- `~/.cache`,
`~/.Trash`, docker volumes, Xcode Archives, Safari LocalStorage, AVD state -- and are unrecoverable
anyway. Those are decided per item; these are not decided at all.

---

## Scheduling (Optional)

For automatic maintenance, add to crontab:

```bash
# Run Tier 1 weekly (Sunday 3am). Tier 1 only: it is the sole tier that needs neither a network
# nor a decision, which is what makes it safe to run unattended.
# Same idiom as everywhere else -- cron runs /bin/sh, where an
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
