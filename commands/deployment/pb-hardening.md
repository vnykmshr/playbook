# Production Security Hardening

Harden servers and containers before deploying to production. Defense-in-depth across OS, container runtime, network, and application layers.

**Mindset:** Security hardening embodies `/pb-design-rules` thinking: Robustness (fail safely), Transparency (make security visible), and Least Surprise (secure defaults). Use `/pb-preamble` thinking to challenge assumptions about what's "secure enough."

The goal is defense-in-depth: multiple layers of protection so that if one fails, others still protect. Never rely on a single security control.

---

## When to Use This Command

- **New production deployment** — Hardening servers before go-live
- **Security audit** — Reviewing and improving security posture
- **Container security** — Locking down container runtime
- **Compliance requirements** — Meeting security standards (SOC2, etc.)
- **After security incident** — Strengthening defenses

---

## Quick Reference

| Layer | Key Actions |
|-------|-------------|
| **Server** | SSH hardening, firewall, fail2ban, auditd |
| **Container** | cap_drop ALL, no-new-privileges, non-root, read-only fs |
| **Network** | Internal networks, no external DB exposure, service auth |
| **Host** | Kernel hardening, automatic updates, log aggregation |

---

## Server Setup Checklist

### SSH Hardening

Secure SSH is the first line of defense.

**Configuration** (`/etc/ssh/sshd_config`):

```bash
# Disable password authentication - keys only
PasswordAuthentication no
PubkeyAuthentication yes

# Restrict root login
PermitRootLogin prohibit-password

# Limit authentication attempts
MaxAuthTries 3

# Disable unused authentication methods
ChallengeResponseAuthentication no
UsePAM yes

# Timeout idle sessions
ClientAliveInterval 300
ClientAliveCountMax 2
```

**Apply changes:**
```bash
sudo systemctl restart sshd
```

**Verification:**
```bash
# Test key-based login works BEFORE disabling password auth
ssh -o PasswordAuthentication=no user@server

# Verify password auth is disabled
grep "PasswordAuthentication no" /etc/ssh/sshd_config
```

### Firewall (UFW)

Default deny, explicit allow.

```bash
# Enable UFW with default deny
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Enable firewall
sudo ufw enable

# Verify rules
sudo ufw status verbose
```

**For internal services:**
```bash
# Allow from specific IP only
sudo ufw allow from 10.0.0.0/8 to any port 5432  # PostgreSQL from internal network
```

### Fail2ban

Protect against brute-force attacks.

```bash
# Install
sudo apt install fail2ban

# Configure (/etc/fail2ban/jail.local)
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400   # 24 hours
findtime = 600    # 10 minute window
```

**Verification:**
```bash
# Check status
sudo fail2ban-client status sshd

# View banned IPs
sudo fail2ban-client status sshd | grep "Banned IP"
```

### Audit Logging (auditd)

Track security-relevant events.

```bash
# Install
sudo apt install auditd

# Enable and start
sudo systemctl enable auditd
sudo systemctl start auditd

# Basic audit rules (/etc/audit/rules.d/audit.rules)
# Log all commands run as root
-a always,exit -F arch=b64 -F euid=0 -S execve -k root_commands

# Log changes to passwd/shadow
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity

# Log SSH config changes
-w /etc/ssh/sshd_config -p wa -k sshd_config
```

**Query audit logs:**
```bash
# Search for specific events
sudo ausearch -k root_commands --start today

# Generate summary report
sudo aureport --summary
```

---

## Docker Container Security

Apply these controls to all production containers.

### Capability Dropping

Start with no capabilities, add only what's needed.

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to ports < 1024
    security_opt:
      - no-new-privileges:true
```

**Common capabilities and when needed:**

| Capability | When Required |
|------------|---------------|
| `NET_BIND_SERVICE` | Binding to ports < 1024 |
| `CHOWN` | Changing file ownership (rarely needed) |
| `SETUID/SETGID` | Dropping privileges (use with caution) |

**Default:** `cap_drop: ALL` with no `cap_add` unless explicitly required.

### Non-Root Users

Never run containers as root.

```dockerfile
# Dockerfile
FROM node:20-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set ownership
WORKDIR /app
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml - explicit UID/GID
services:
  app:
    user: "1000:1000"
```

### Read-Only Filesystem

Prevent runtime modifications.

```yaml
services:
  redis:
    image: redis:7-alpine
    read_only: true
    tmpfs:
      - /tmp:size=64M
      - /var/run:size=64M
    volumes:
      - redis-data:/data
```

**Pattern:** Read-only root + tmpfs for temporary files + volumes for persistent data.

### Resource Limits

Prevent resource exhaustion.

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
    pids_limit: 64
```

**Guidelines:**
- `pids_limit`: 64-256 depending on service complexity
- Memory: Set based on observed usage + headroom
- CPU: Set based on fair share across services

### Log Rotation

Prevent disk exhaustion from logs.

```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

Or in Docker daemon config (`/etc/docker/daemon.json`):
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Complete Secure Container Example

```yaml
services:
  api:
    image: myapp:v1.2.3
    user: "1000:1000"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=64M
    pids_limit: 64
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - internal
    # No ports exposed - accessed via reverse proxy
```

---

## Network Isolation

### Internal Docker Networks

Never expose databases or internal services externally.

```yaml
networks:
  internal:
    internal: true  # No external access
  frontend:
    # External access allowed

services:
  nginx:
    networks:
      - frontend
      - internal

  api:
    networks:
      - internal  # Only internal access

  postgres:
    networks:
      - internal  # Database never on frontend network
    # NO ports section - not exposed to host
```

**Pattern:**
- Frontend network: Only reverse proxy
- Internal network: All backend services
- Database: Internal network only, no host port binding

### Service Authentication

Internal services should authenticate each other.

```yaml
services:
  redis:
    command: redis-server --requirepass ${REDIS_PASSWORD}
    environment:
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    networks:
      - internal

  api:
    environment:
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379
    networks:
      - internal
```

**Even on internal networks**, use authentication. Defense-in-depth.

### Port Exposure Rules

| Service | External Port | Internal Only | Notes |
|---------|---------------|---------------|-------|
| Nginx/Traefik | 80, 443 | - | Only entry point |
| API | - | Yes | Behind reverse proxy |
| PostgreSQL | - | Yes | Never external |
| Redis | - | Yes | Never external |
| Monitoring | - | Yes | Access via VPN/bastion |

---

## Host Hardening

### Kernel Parameters

Security-focused sysctl settings (`/etc/sysctl.d/99-security.conf`):

```bash
# Prevent IP spoofing
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0

# Disable source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# Enable SYN flood protection
net.ipv4.tcp_syncookies = 1

# Log suspicious packets
net.ipv4.conf.all.log_martians = 1
```

Apply: `sudo sysctl -p /etc/sysctl.d/99-security.conf`

### Automatic Security Updates

```bash
# Ubuntu/Debian
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# Verify
cat /etc/apt/apt.conf.d/20auto-upgrades
```

**Configure** (`/etc/apt/apt.conf.d/50unattended-upgrades`):
```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Mail "admin@example.com";
```

### File Permissions

```bash
# Secure SSH directory
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Secure sensitive files
chmod 600 /etc/shadow
chmod 644 /etc/passwd

# Verify no world-writable files in sensitive locations
find /etc -perm -002 -type f
```

---

## Cloud-Agnostic Security Patterns

These patterns apply across AWS, GCP, Azure, or bare metal.

### Security Group Patterns

**Principle:** Default deny, explicit allow, least privilege.

| Rule | Source | Destination | Port | Notes |
|------|--------|-------------|------|-------|
| SSH | Bastion/VPN only | Servers | 22 | Never from 0.0.0.0/0 |
| HTTPS | Internet | Load balancer | 443 | Only entry point |
| App | Load balancer | App servers | 8080 | Internal only |
| DB | App servers | Database | 5432 | App tier only |

### VPC/Network Concepts

```
Internet
    │
    ▼
┌─────────────────────────────────────────┐
│ Public Subnet                           │
│   - Load Balancer                       │
│   - Bastion Host (if needed)            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ Private Subnet (App Tier)               │
│   - Application servers                 │
│   - No direct internet access           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ Private Subnet (Data Tier)              │
│   - Databases                           │
│   - Caches                              │
│   - No direct internet access           │
└─────────────────────────────────────────┘
```

### IAM Principles

- **Least privilege**: Grant minimum permissions needed
- **No long-lived credentials**: Use temporary credentials, rotate regularly
- **Separate concerns**: Different roles for different functions
- **Audit access**: Log and review who accessed what

---

## Pre-Deployment Security Checklist

Before deploying to production:

### Server Level
- [ ] SSH key-only authentication enabled
- [ ] Root login restricted
- [ ] Firewall configured (default deny)
- [ ] Fail2ban installed and configured
- [ ] Audit logging enabled
- [ ] Automatic security updates enabled

### Container Level
- [ ] All containers: `cap_drop: ALL`
- [ ] All containers: `no-new-privileges: true`
- [ ] All containers: Non-root user
- [ ] Sensitive containers: Read-only filesystem
- [ ] All containers: Resource limits set
- [ ] All containers: Log rotation configured

### Network Level
- [ ] Databases on internal network only
- [ ] No unnecessary ports exposed
- [ ] Service-to-service authentication enabled
- [ ] TLS for external traffic
- [ ] Security groups follow least privilege

### Secrets
- [ ] No secrets in code or environment
- [ ] Secrets encrypted at rest
- [ ] Secret rotation configured
- [ ] See `/pb-secrets` for comprehensive guidance

---

## Post-Deployment Verification

After deployment, verify hardening:

```bash
# Verify SSH config
sudo sshd -t && echo "SSH config OK"

# Check firewall status
sudo ufw status verbose

# Verify fail2ban running
sudo systemctl status fail2ban

# Check Docker security
docker inspect <container> | jq '.[0].HostConfig.CapDrop'
docker inspect <container> | jq '.[0].HostConfig.SecurityOpt'

# Verify no containers running as root
docker ps -q | xargs docker inspect --format '{{.Name}}: User={{.Config.User}}'

# Check for exposed ports
docker ps --format "{{.Names}}: {{.Ports}}"

# Verify network isolation
docker network ls
docker network inspect internal
```

---

## Integration with Playbook

**Part of production readiness:**
- `/pb-hardening` — Harden infrastructure (this command)
- `/pb-secrets` — Manage secrets securely
- `/pb-security` — Application security review
- `/pb-deployment` — Deployment strategies
- `/pb-dr` — Disaster recovery planning

**Workflow:**
```
Development → Security Review (/pb-security)
           → Infrastructure Hardening (/pb-hardening)
           → Secrets Setup (/pb-secrets)
           → Deployment (/pb-deployment)
           → Monitoring (/pb-observability)
```

---

## Quick Commands

| Action | Command |
|--------|---------|
| Check SSH config | `sudo sshd -t` |
| UFW status | `sudo ufw status verbose` |
| Fail2ban status | `sudo fail2ban-client status` |
| Audit search | `sudo ausearch -k <key> --start today` |
| Docker security inspect | `docker inspect <container> \| jq '.[0].HostConfig'` |
| Find world-writable | `find /etc -perm -002 -type f` |

---

## Related Commands

- `/pb-secrets` — Manage secrets securely across environments
- `/pb-security` — Application-level security review
- `/pb-deployment` — Deploy hardened infrastructure

---

*Defense-in-depth: if one layer fails, others still protect.*
