# Server Hygiene

Periodic health and hygiene review for servers and VPS instances. A calm, repeatable ritual for detecting drift, bloat, and silent degradation before they become incidents.

**Mindset:** Server hygiene embodies `/pb-design-rules` thinking: Robustness (catch degradation before failure), Transparency (make server state visible and explainable), and Simplicity (predictable cleanups beat clever automation). Apply `/pb-preamble` thinking to challenge assumptions about what's "probably fine."

**Resource Hint:** sonnet (procedural, well-defined scope)

This is not firefighting. This is the periodic physical exam that prevents the emergency room visit.

---

## When to Use This Command

- **Monthly hygiene pass** — Routine review of a running server
- **Quarterly full audit** — Deep drift analysis and capacity planning
- **After a period of neglect** — Server hasn't been reviewed in months
- **Before scaling or migration** — Understand current state before changes
- **Post-incident verification** — Confirm the server is clean after recovery
- **Onboarding to an inherited server** — Build a mental model of what's running

---

## Quick Reference

| Cadence | Scope | Time |
|---------|-------|------|
| **Weekly** | Glance: disk, errors, failed jobs | 5 min |
| **Monthly** | Hygiene: logs, images, packages, access | 30 min |
| **Quarterly** | Full: drift analysis, capacity, backup test | 1-2 hrs |

---

## Execution Flow

```
Phase 1: SNAPSHOT ──► Phase 2: HEALTH ──► Phase 3: DRIFT ──► Phase 4: CLEANUP ──► Phase 5: READINESS
  (inventory)         (signals)           (bloat detection)   (safe actions)       (future-proof)
       └── Weekly: phases 2-3 only ──┘
       └── Monthly: phases 1-4 ───────────────────────────┘
       └── Quarterly: all phases ──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Snapshot Reality

Goal: know exactly what the server is today. If you can't explain the server in 5 minutes, it's already drifting.

### Server Inventory

```bash
# System identity
hostname && uname -a
head -4 /etc/os-release
uptime

# Resources
nproc && free -h && df -h
```

| Item | Command | What to Record |
|------|---------|----------------|
| OS and kernel | `uname -a`, `cat /etc/os-release` | Version, last update date |
| CPU, RAM, disk | `nproc`, `free -h`, `df -h` | Limits and current usage |
| Uptime | `uptime` | Last reboot, load average |
| Users | `cat /etc/passwd \| grep -v nologin` | Who has shell access |
| SSH keys | `ls /home/*/.ssh/authorized_keys` | Which keys are present |
| Open ports | `ss -tlnp` | What's listening, on which interfaces |
| Running services | `systemctl list-units --type=service --state=running` | Active services |
| Containers | `docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'` | Running containers |
| Cron jobs | `crontab -l; ls /etc/cron.d/` | Scheduled tasks |

### Application Footprint

| Item | What to Check |
|------|---------------|
| Deployed apps | Versions, last deploy date |
| Active vs abandoned | Is everything running actually needed? |
| Deployment method | systemd, Docker, PM2, bare process |
| Runtime versions | node, go, python, java — are they current? |

### Configuration Sources

| Item | What to Check |
|------|---------------|
| Environment variables | Where are they defined? (systemd, .env, shell profile) |
| Secrets location | Env files, vaults, or plaintext? |
| Reverse proxy | nginx, caddy, traefik — which sites are configured? |
| TLS certificates | Source (Let's Encrypt, manual), renewal status, expiry date |

**Deliverable:** A short server manifest. Write it down — even a few bullet points in a markdown file beats nothing.

---

## Phase 2: Health Signals

Goal: detect slow degradation before users feel it.

### Resource Trends

Look at trends, not just current values. A server at 60% disk today that was at 40% last month is a problem. Compare with your previous server manifest — if you don't have one, record today's numbers. That's where trends start.

```bash
# Disk usage by mount
df -h

# Largest directories
du -sh /* 2>/dev/null | sort -hr | head -10

# Memory with swap
free -h

# CPU load (1, 5, 15 min averages)
uptime

# Disk IO wait (if iostat available)
iostat -x 1 3 2>/dev/null
```

**Thresholds:**

| Resource | Healthy | Warning | Critical |
|----------|---------|---------|----------|
| Disk | < 70% | 70-85% | > 85% |
| Memory | < 80% | 80-90% | > 90% or swapping |
| CPU load | < cores | 1-2x cores | > 2x cores sustained |
| Swap | None | Any active | Growing over time |

### Process Health

```bash
# Long-running processes sorted by memory
ps aux --sort=-%mem | head -15

# Zombie processes
ps aux | awk '$8 ~ /Z/ {print}'

# Failed systemd units
systemctl --failed

# OOM killer history
dmesg | grep -i "out of memory" | tail -5
journalctl -k | grep -i "oom" | tail -5
```

**Ask:** Is anything slowly leaking memory? Are there zombie processes? Has the OOM killer fired recently?

### Application Health

| Signal | How to Check | Red Flag |
|--------|-------------|----------|
| Error rates | `journalctl -u <service> --since "1 hour ago" \| grep -i error \| wc -l` | Increasing trend |
| Restart loops | `systemctl show <service> -p NRestarts` | Count > 0 unexpectedly |
| Queue backlog | Application-specific | Growing, not draining |
| DB connections | `ss -tnp \| grep 5432 \| wc -l` | Approaching pool limit |

### System Health

```bash
# Kernel warnings
dmesg --level=err,warn | tail -10

# Time sync
timedatectl status | grep "synchronized"

# Pending security updates (Debian/Ubuntu)
apt list --upgradable 2>/dev/null | grep -i security
```

**Rule of thumb:** If something spikes periodically, find out why. If something slowly rises, that's a leak or accumulation.

---

## Phase 3: Drift and Bloat Detection

This is where most server rot happens. Things quietly accumulate until one day the disk is full or a forgotten service gets exploited.

### Disk Bloat

```bash
# Log sizes
du -sh /var/log/ /var/log/journal/

# Docker waste
docker system df
docker images -f "dangling=true" -q | wc -l
docker volume ls -f "dangling=true" -q | wc -l

# Old build artifacts, temp files, core dumps
find /tmp -type f -mtime +30 | head -20
find / -name "core" -type f 2>/dev/null | head -5
```

| Bloat Source | Where to Look |
|-------------|---------------|
| Logs without rotation | `/var/log/`, application log directories |
| Old log archives | `.gz` files never cleaned |
| Docker images and volumes | `docker system df` |
| Build artifacts | `/tmp`, project build directories |
| Core dumps | `/`, `/var/crash/` |
| Package manager cache | `apt clean`, `yum clean all` |

### Service Bloat

| Check | Command | Red Flag |
|-------|---------|----------|
| Enabled but unused services | `systemctl list-unit-files --state=enabled` | Services you don't recognize |
| Stale reverse proxy configs | `ls /etc/nginx/sites-enabled/` | Sites for apps no longer running |
| Unused firewall rules | `ufw status` or `iptables -L` | Rules for decommissioned services |
| Stale cron jobs | `crontab -l` | Jobs for things that moved or stopped |
| Orphaned containers | `docker ps -a --filter status=exited` | Exited containers piling up |

### Config Drift

- Hand-edited config files with no source of truth
- Inconsistent environment variables across applications
- One-off fixes never documented ("I'll remember why I changed this")
- Secrets duplicated in multiple places

**Ask:** Could you rebuild this server's configuration from version control alone? If not, what's missing?

### Security Drift

```bash
# Users with shell access
grep -v "nologin\|false" /etc/passwd

# SSH keys — do you recognize all of them?
for user_home in /home/*/; do
  [ -f "$user_home.ssh/authorized_keys" ] && echo "=== $(basename $user_home) ===" && cat "$user_home.ssh/authorized_keys"
done

# Packages not updated recently
apt list --upgradable 2>/dev/null | wc -l

# TLS certificate expiry
openssl s_client -connect localhost:443 -servername $(hostname) </dev/null 2>/dev/null | openssl x509 -noout -dates
```

| Drift Type | What to Check |
|-----------|---------------|
| Unused SSH keys | Keys for people who no longer need access |
| Stale users | Accounts that should have been removed |
| Overly permissive firewall | Rules broader than necessary |
| Outdated TLS | Weak ciphers, approaching expiry |
| Unpatched packages | Security updates pending for weeks |

**Deliverable:** Two lists: "safe to remove now" and "needs planning before removal."

---

## Phase 4: Hygiene Actions

Golden rule: no "clever" changes during hygiene. Predictable beats smart. Only safe, reversible actions during routine reviews.

### Safe Cleanups

Inspect before acting. Review output, then confirm.

```bash
# Rotate and prune journal logs
journalctl --vacuum-time=30d
journalctl --vacuum-size=500M

# Show removable packages, then clean
apt --dry-run autoremove
apt autoremove && apt clean

# Show what Docker would prune (images, containers, build cache)
docker system prune --dry-run
docker system prune
```

**Requires judgment** — these can destroy data if containers are temporarily stopped:

```bash
# Review temp files before deleting
find /tmp -type f -mtime +30 | head -20
# Only delete after reviewing: find /tmp -type f -mtime +30 -delete

# List unused volumes — verify none belong to stopped services you intend to restart
docker volume ls -f "dangling=true"
# Only prune after reviewing: docker volume prune
```

### Stability Improvements

| Action | Why |
|--------|-----|
| Add log rotation where missing | Prevent disk exhaustion from logs |
| Set resource limits on containers | Prevent one service from starving others |
| Add health checks to services | Detect failures before users report them |
| Configure restart policies | `RestartSec=5`, `Restart=on-failure` for systemd |
| Document non-obvious decisions | Future you will forget why that cron job exists |

### Performance Tuning

Only if measurements justify it. Don't tune what you haven't measured.

| Area | Action | Prerequisite |
|------|--------|-------------|
| Worker counts | Adjust based on CPU cores | Know current CPU utilization |
| DB connections | Tune pool size | Know current connection count vs limit |
| Compression | Enable gzip/brotli in reverse proxy | Verify CPU headroom |
| Unnecessary background jobs | Remove or reduce frequency | Know what each job does |

---

## Phase 5: Future Readiness

This is where the ritual pays off long-term.

### Backup Verification

**The question is not "do you have backups" but "can you restore them."**

| Check | Status |
|-------|--------|
| What is backed up? | Data, config, secrets, or all three? |
| Backup frequency | Matches your acceptable data loss? |
| Last restore test | If "never," schedule one now |
| Off-server storage | Backups on the same VPS are not backups |
| Retention and cost | How far back can you go? What does it cost? |

For comprehensive backup and recovery planning, see `/pb-dr`.

### Monitoring Coverage

- [ ] Resource metrics (CPU, RAM, disk) — collected and retained
- [ ] Application error rates — visible and trended
- [ ] Uptime checks — external, not self-reported
- [ ] Log visibility — searchable, not just stored
- [ ] Alerts — fire when needed, reach someone who can act

For monitoring design guidance, see `/pb-observability`.

### Scaling Headroom

- **Current capacity:** How much headroom before hitting limits?
- **First bottleneck:** What resource runs out first?
- **Single points of failure:** What has no redundancy?
- **Growth trajectory:** At current growth rate, when do you hit limits?

### Disaster Questions

Answer honestly:

1. How long to rebuild this server from scratch?
2. What steps are manual vs automated?
3. What secrets would block recovery if lost?
4. Who else knows how this server works?

**If rebuild takes more than a few hours, the system is fragile.** See `/pb-dr` for disaster recovery planning.

---

## Server Manifest Template

Maintain a living document per server. Even a few lines beats nothing.

```markdown
# Server: [hostname]

**Provider:** [e.g., DigitalOcean, Hetzner, AWS]
**Size:** [CPU, RAM, disk]
**OS:** [distro and version]
**Last review:** [date]

## Services Running
- [service 1] — [purpose] — [deployment method]
- [service 2] — [purpose] — [deployment method]

## Access
- SSH: [who has keys]
- Firewall: [ports open]

## Backups
- [what, where, how often, last tested]

## Known Issues
- [things to watch or fix next time]
```

---

## Quick Commands

| Action | Command |
|--------|---------|
| Largest directories | `du -sh /* 2>/dev/null \| sort -hr \| head -10` |
| Open ports | `ss -tlnp` |
| Running services | `systemctl list-units --type=service --state=running` |
| Failed services | `systemctl --failed` |
| Docker waste | `docker system df` |
| Journal cleanup | `journalctl --vacuum-time=30d` |
| Security updates | `apt list --upgradable 2>/dev/null` |
| TLS expiry | `openssl s_client -connect localhost:443 </dev/null 2>/dev/null \| openssl x509 -noout -dates` |
| OOM history | `dmesg \| grep -i "out of memory"` |

---

## Red Flags

Signs the server needs a hygiene pass now:

- "We'll deal with it when it becomes a problem"
- Deploys are getting slower with no code changes
- Memory usage "mysteriously" grows between deploys
- Nobody knows what's safe to delete
- A restart broke something that was working
- Last backup test was "never"

---

## Related Commands

- `/pb-maintenance` — Strategic maintenance patterns and thinking triggers
- `/pb-hardening` — Initial server security setup (run before first deploy)
- `/pb-dr` — Disaster recovery planning and testing
- `/pb-sre-practices` — Toil reduction, error budgets, operational culture
- `/pb-observability` — Monitoring and alerting design

---

**Last Updated:** 2026-02-07
**Version:** 1.0.0

---

*Production systems accumulate entropy. This ritual is how you pay down the interest before it compounds.*
