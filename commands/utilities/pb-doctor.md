# System Health Check

Diagnose system health issues: disk space, memory pressure, CPU usage, and common developer environment problems. The "what's wrong" before "how to fix."

**Platform:** macOS (with Linux alternatives noted)
**Use Case:** "Something's slow" / "Builds are failing" / "Machine feels sluggish"

**Mindset:** Design Rules say "fail noisily and early" — surface system problems before they cascade.

**Resource Hint:** haiku — mechanical system checks and status reporting.

## When to Use

- Machine feels slow or unresponsive during development
- Builds or tests are failing unexpectedly
- Before running storage cleanup or tool updates (baseline check)

---

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. DISK         Check available space, large consumers     │
│         ↓                                                   │
│  2. MEMORY       Check RAM usage, swap pressure             │
│         ↓                                                   │
│  3. CPU          Check load, runaway processes              │
│         ↓                                                   │
│  4. PROCESSES    Find resource hogs                         │
│         ↓                                                   │
│  5. DEV TOOLS    Check dev environment health               │
│         ↓                                                   │
│  6. REPORT       Summary with recommendations               │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Health Check

Run this for a fast overview:

```bash
echo "=== Disk ===" && df -h / | tail -1
echo "=== Memory ===" && vm_stat | head -5
echo "=== CPU Load ===" && uptime
echo "=== Top Processes ===" && ps aux | sort -nrk 3,3 | head -6
```

---

## Step 1: Disk Health

### Check Available Space

```bash
# Overall disk usage
df -h /

# Check if approaching limits
USAGE=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$USAGE" -gt 80 ]; then
  echo "WARNING: Disk usage at ${USAGE}%"
fi
```

### Find Large Directories

```bash
# Top 10 largest directories in home
du -sh ~/* 2>/dev/null | sort -hr | head -10

# Developer-specific large directories
du -sh ~/Library/Developer 2>/dev/null
du -sh ~/Library/Caches 2>/dev/null
du -sh ~/.docker 2>/dev/null
du -sh node_modules 2>/dev/null
```

**Thresholds:**
| Usage | Status | Action |
|-------|--------|--------|
| < 70% | Healthy | None needed |
| 70-85% | Warning | Consider `/pb-storage` |
| > 85% | Critical | Run `/pb-storage` immediately |

---

## Step 2: Memory Health

### Check Memory Pressure

```bash
# macOS memory stats
vm_stat

# Human-readable summary
vm_stat | awk '
  /Pages free/ {free=$3}
  /Pages active/ {active=$3}
  /Pages inactive/ {inactive=$3}
  /Pages wired/ {wired=$3}
  END {
    page=4096/1024/1024
    print "Free: " free*page " GB"
    print "Active: " active*page " GB"
    print "Wired: " wired*page " GB"
  }
'

# Check for memory pressure (macOS)
memory_pressure
```

### Check Swap Usage

```bash
# Swap usage (high swap = memory pressure)
sysctl vm.swapusage

# If swap is being used heavily, memory is constrained
```

### Find Memory Hogs

```bash
# Top 10 by memory usage
ps aux --sort=-%mem | head -11

# Or using top (snapshot)
top -l 1 -n 10 -o mem
```

**Thresholds:**
| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Memory Pressure | Normal | Warn | Critical (yellow/red in Activity Monitor) |
| Swap Used | < 1GB | 1-4GB | > 4GB |
| Free + Inactive | > 2GB | 1-2GB | < 1GB |

---

## Step 3: CPU Health

### Check Load Average

```bash
# Current load
uptime

# Load interpretation:
# - Load < cores: healthy
# - Load = cores: fully utilized
# - Load > cores: overloaded
sysctl -n hw.ncpu  # Number of cores
```

### Find CPU Hogs

```bash
# Top 10 by CPU
ps aux --sort=-%cpu | head -11

# Real-time view (quit with 'q')
top -o cpu

# Find processes using > 50% CPU
ps aux | awk '$3 > 50 {print $0}'
```

### Check for Runaway Processes

```bash
# Processes running > 1 hour with high CPU
ps -eo pid,etime,pcpu,comm | awk '$3 > 50 && $2 ~ /-/ {print}'
```

**Thresholds:**
| Cores | Healthy Load | Warning | Overloaded |
|-------|--------------|---------|------------|
| 8 | < 6 | 6-10 | > 10 |
| 10 | < 8 | 8-12 | > 12 |
| 12 | < 10 | 10-15 | > 15 |

---

## Step 4: Process Analysis

### Find Resource Hogs

```bash
# Combined CPU + Memory view
ps aux | awk 'NR==1 || $3 > 10 || $4 > 5' | head -20
```

### Common Developer Culprits

```bash
# Check known resource hogs
for proc in "node" "webpack" "docker" "java" "Xcode" "Simulator" "Chrome"; do
  pgrep -f "$proc" > /dev/null && echo "$proc is running"
done

# Docker specifically
docker stats --no-stream 2>/dev/null | head -10
```

### Zombie Processes

```bash
# Find zombie processes
ps aux | awk '$8 ~ /Z/ {print}'
```

---

## Step 5: Developer Environment Health

### Check Critical Tools

```bash
echo "=== Git ===" && git --version
echo "=== Node ===" && node --version 2>/dev/null || echo "Not installed"
echo "=== npm ===" && npm --version 2>/dev/null || echo "Not installed"
echo "=== Python ===" && python3 --version 2>/dev/null || echo "Not installed"
echo "=== Docker ===" && docker --version 2>/dev/null || echo "Not installed/running"
echo "=== Homebrew ===" && brew --version 2>/dev/null | head -1 || echo "Not installed"
```

### Check for Outdated Tools

```bash
# Homebrew outdated
brew outdated 2>/dev/null | head -10

# npm outdated globals
npm outdated -g 2>/dev/null | head -10
```

### Check Docker Health

```bash
# Docker disk usage
docker system df 2>/dev/null

# Docker running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null
```

### Check Xcode (if installed)

```bash
# Xcode version and path
xcode-select -p 2>/dev/null && xcodebuild -version 2>/dev/null | head -2

# Xcode disk usage
du -sh ~/Library/Developer/Xcode 2>/dev/null
```

---

## Step 6: Generate Report

After running diagnostics, summarize:

```
=== SYSTEM HEALTH REPORT ===

DISK:     [OK/WARNING/CRITICAL] - XX% used (XX GB free)
MEMORY:   [OK/WARNING/CRITICAL] - XX GB active, XX GB swap
CPU:      [OK/WARNING/CRITICAL] - Load: X.XX (X cores)
DOCKER:   [OK/WARNING/N/A] - XX GB used

TOP RESOURCE CONSUMERS:
1. Process A - XX% CPU, XX% MEM
2. Process B - XX% CPU, XX% MEM
3. Process C - XX% CPU, XX% MEM

RECOMMENDATIONS:
- [ ] Run /pb-storage to free disk space
- [ ] Kill process X (runaway)
- [ ] Restart Docker (high memory)
```

---

## User Interaction Flow

When executing this playbook:

1. **Run full diagnostic** — All checks above
2. **Present findings** — Show health status per category
3. **Prioritize issues** — Critical first, then warnings
4. **Offer remediation** — Link to relevant playbooks

### AskUserQuestion Structure

**After Report:**
```
Question: "What would you like to address first?"
Options:
  - Free disk space (/pb-storage)
  - Kill resource hogs (I'll show which)
  - Update outdated tools (/pb-update)
  - Just wanted the report, thanks
```

---

## Automated Health Script

Save as `~/bin/doctor.sh`:

```bash
#!/bin/bash

echo "=== DISK ==="
df -h / | tail -1

echo -e "\n=== MEMORY ==="
memory_pressure 2>/dev/null || vm_stat | head -5

echo -e "\n=== CPU LOAD ==="
uptime

echo -e "\n=== TOP PROCESSES (CPU) ==="
ps aux --sort=-%cpu | head -6

echo -e "\n=== TOP PROCESSES (MEM) ==="
ps aux --sort=-%mem | head -6

echo -e "\n=== DOCKER ==="
docker system df 2>/dev/null || echo "Not running"

echo -e "\n=== OUTDATED BREW ==="
brew outdated 2>/dev/null | head -5 || echo "N/A"
```

---

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| High CPU, nothing obvious | Background indexing (Spotlight, Time Machine) | Wait, or exclude dev dirs from Spotlight |
| High memory, no heavy apps | Memory leaks in long-running processes | Restart Docker, browsers, IDEs |
| Disk full suddenly | node_modules, Docker images, Xcode | Run `/pb-storage` |
| Everything slow | Multiple causes | Check all metrics, address worst first |
| Fan running constantly | High CPU process | Find and kill, or improve ventilation |

---

## Related Commands

- `/pb-storage` — Free disk space
- `/pb-ports` — Check port usage and conflicts
- `/pb-update` — Update outdated tools
- `/pb-debug` — Deep debugging methodology
- `/pb-git-hygiene` — Git repository health audit (branches, large objects, secrets)

---

*Run monthly or when machine feels slow. Good first step before any cleanup.*
