# Port Management

Find processes using ports, kill stale listeners, and resolve port conflicts. A common developer pain point solved.

**Platform:** macOS/Linux
**Use Case:** "What's using port 3000?" / "Kill whatever's blocking my server"

**Mindset:** Design Rules say "silence when nothing to say" — only report conflicts that need action.

**Resource Hint:** haiku — port scanning and process lookup are mechanical tasks.

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

### Kill Process on Port

```bash
# Find and kill (interactive)
lsof -ti :3000 | xargs kill -9

# Or two-step (safer)
lsof -i :3000  # Note the PID
kill -9 <PID>
```

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

# Show process tree (what spawned it)
ps -f $(lsof -ti :3000)

# Show process start time and command
ps -p $(lsof -ti :3000) -o pid,lstart,command
```

---

## Step 4: Kill Strategies

### Safe Kill (SIGTERM)

```bash
# Graceful shutdown - process can cleanup
kill $(lsof -ti :3000)
```

### Force Kill (SIGKILL)

```bash
# Immediate termination - no cleanup
kill -9 $(lsof -ti :3000)
```

### Kill All on Port Range

```bash
# Kill everything on ports 3000-3010
for port in {3000..3010}; do
  lsof -ti :$port | xargs kill -9 2>/dev/null
done
```

---

## Common Scenarios

### Scenario: "Port already in use"

```bash
# Find what's using it
lsof -i :3000

# If it's a zombie process from crashed dev server
kill -9 $(lsof -ti :3000)

# Verify it's free
lsof -i :3000  # Should return nothing
```

### Scenario: Clean Slate for Development

```bash
# Kill common dev server ports
for port in 3000 3001 4000 5000 5173 8000 8080; do
  PID=$(lsof -ti :$port 2>/dev/null)
  if [ -n "$PID" ]; then
    echo "Killing process on port $port (PID: $PID)"
    kill -9 $PID
  fi
done
```

### Scenario: Find Rogue Node Processes

```bash
# Find all node processes listening
lsof -i -P | grep node | grep LISTEN

# Kill all node listeners
pkill -f node
```

### Scenario: Docker Port Conflicts

```bash
# List Docker port mappings
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Stop container using port
docker stop $(docker ps -q --filter "publish=3000")
```

---

## User Interaction Flow

When executing this playbook:

1. **Scan** — Show all listening ports with process names
2. **Categorize** — Group into dev servers, databases, system
3. **Ask** — "Which ports do you want to investigate or free up?"
4. **Confirm** — Show full process details before any kill
5. **Execute** — Kill with user's chosen method (graceful vs force)

### AskUserQuestion Structure

**Action Selection:**
```
Question: "What would you like to do?"
Options:
  - Scan all listening ports
  - Free specific port (I'll ask which)
  - Kill all dev server ports (3000, 5173, 8080, etc.)
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
| Kill doesn't work | Try `kill -9` (SIGKILL) instead of graceful |

---

## Aliases (Optional)

Add to your shell profile:

```bash
# What's using this port?
port() { lsof -i :$1; }

# Kill whatever's using this port
killport() { lsof -ti :$1 | xargs kill -9 2>/dev/null && echo "Killed" || echo "Nothing on port $1"; }

# List all listening ports
ports() { lsof -i -P | grep LISTEN; }
```

---

## Related Commands

- `/pb-doctor` — Diagnose system health issues
- `/pb-debug` — General debugging methodology
- `/pb-storage` — Free disk space when builds fail

---

*Use when: port conflicts, stale dev servers, debugging network issues.*
