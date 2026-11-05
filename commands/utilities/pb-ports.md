---
name: "pb-ports"
title: "Port Management"
category: "utilities"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-doctor', 'pb-debug', 'pb-storage']
last_reviewed: "2026-11-05"
version: "1.1.0"
version_notes: "v1.1.0: Every kill goes through one escalation in Step 4 (SIGTERM, check, then SIGKILL) on the listener only (`-sTCP:LISTEN`), so clients on the port survive. The kill quick commands, port-range and clean-slate loops, `pkill -f node` and the `killport` alias are gone."
breaking_changes: []
---
# Port Management

Find processes using ports, kill stale listeners, and resolve port conflicts. A common developer pain point solved.

**Platform:** macOS/Linux
**Use Case:** "What's using port 3000?" / "Kill whatever's blocking my server"

**Mindset:** Apply `/pb-design-rules` thinking: silence when nothing to say. Only report conflicts that need action.

**Resource Hint:** sonnet - Port scanning and process identification.

## When to Use

- Dev server fails to start with "port already in use" error
- After a crash left orphan processes holding ports open
- Before starting a multi-service stack to ensure ports are free

---

## Quick Commands

### Find What's Using a Port

```bash
# Single port
lsof -i :3000

# Multiple ports
lsof -i :3000 -i :8080 -i :5432

# All listening ports
lsof -i -P | grep LISTEN
```

To free a port, use the escalation in Step 4.

---

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. SCAN         List all listening ports                   │
│         ↓                                                   │
│  2. IDENTIFY     Show process name, PID, user for each      │
│         ↓                                                   │
│  3. CATEGORIZE   Group by: dev servers, databases, system   │
│         ↓                                                   │
│  4. SELECT       User picks which to investigate/kill       │
│         ↓                                                   │
│  5. CONFIRM      Show full process details before kill      │
│         ↓                                                   │
│  6. EXECUTE      Kill selected processes                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Scan All Listening Ports

```bash
# Comprehensive port scan with process details
lsof -i -P -n | grep LISTEN | awk '{print $1, $2, $9}' | sort -u

# Alternative using netstat (shows more detail)
netstat -anv | grep LISTEN

# macOS-specific: show all TCP listeners
sudo lsof -iTCP -sTCP:LISTEN -P -n
```

**Output format:**
```
COMMAND    PID    ADDRESS
node       12345  *:3000
postgres   67890  127.0.0.1:5432
redis      11111  *:6379
```

---

## Step 2: Common Port Categories

### Development Servers

| Port | Typical Use |
|------|-------------|
| 3000 | React, Rails, Express default |
| 3001 | React secondary |
| 4000 | Phoenix, custom |
| 5000 | Flask default |
| 5173 | Vite default |
| 8000 | Django, Python HTTP |
| 8080 | Alternative HTTP, Java |
| 8888 | Jupyter |

### Databases

| Port | Service |
|------|---------|
| 5432 | PostgreSQL |
| 3306 | MySQL |
| 27017 | MongoDB |
| 6379 | Redis |
| 9200 | Elasticsearch |

### System Services

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 53 | DNS |

---

## Step 3: Investigate Specific Port

```bash
# Full details about port 3000
lsof -i :3000

# Show the parent PID (what spawned it)
ps -f $(lsof -ti :3000 -sTCP:LISTEN)

# Show process start time and command
ps -p $(lsof -ti :3000 -sTCP:LISTEN) -o pid,lstart,command
```

---

## Step 4: Free the Port

One escalation for every kill: ask, check, then force. `-sTCP:LISTEN` selects the listener only; plain `lsof -ti :PORT` also returns clients connected to it (a browser, `curl`).

```bash
PORT=3000

# 1. SIGTERM: the process can clean up
kill $(lsof -ti :$PORT -sTCP:LISTEN)

# 2. Check, then 3. SIGKILL (no cleanup) only if it is still listening
sleep 2
if PIDS=$(lsof -ti :$PORT -sTCP:LISTEN); then kill -9 $PIDS; else echo "port $PORT free"; fi
```

For several ports, run the same three steps per port.

### Port Held by a Docker Container

```bash
# List Docker port mappings
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Stop container using port
docker stop $(docker ps -q --filter "publish=3000")
```

---

## User Interaction Flow

When executing this playbook:

1. **Scan** - Show all listening ports with process names
2. **Categorize** - Group into dev servers, databases, system
3. **Ask** - "Which ports do you want to investigate or free up?"
4. **Confirm** - Show full process details before any kill
5. **Execute** - Kill with user's chosen method (graceful vs force)

### AskUserQuestion Structure

**Action Selection:**
```
Question: "What would you like to do?"
Options:
  - Scan all listening ports
  - Free specific port (I'll ask which)
  - Show me what's using the most ports
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" on lsof | Use `sudo lsof -i :PORT` |
| Process respawns after kill | Check if it's a managed service (launchd, systemd) |
| "No such process" | Process already exited, port should be free |
| Docker container won't release port | `docker stop` then `docker rm` the container |
| Process ignores SIGTERM | Step 4: check, then `kill -9` |

---

## Aliases (Optional)

Add to your shell profile:

```bash
# What's using this port?
port() { lsof -i :$1; }

# List all listening ports
ports() { lsof -i -P | grep LISTEN; }
```

---

## Related Commands

- `/pb-doctor` - Diagnose system health issues
- `/pb-debug` - General debugging methodology
- `/pb-storage` - Free disk space when builds fail

---

*Use when: port conflicts, stale dev servers, debugging network issues.*
