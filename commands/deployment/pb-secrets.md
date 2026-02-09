---
name: "pb-secrets"
title: "Secrets Management"
category: "deployment"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-hardening', 'pb-security', 'pb-deployment']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Secrets Management

Manage secrets securely across development, CI/CD, and production environments. Never hardcode, always encrypt, rotate regularly.

**Mindset:** Secrets management embodies `/pb-design-rules` thinking: Repair (fail loudly when secrets are wrong), Transparency (audit who accessed what), and Least Surprise (secrets work the same way everywhere). Use `/pb-preamble` thinking to challenge "it's just for testing" excuses.

A leaked secret is a security incident. Treat secrets as radioactive: minimize exposure, contain carefully, dispose properly.

**Resource Hint:** sonnet — secrets workflow implementation and rotation patterns

---

## When to Use

- Setting up secrets management for a new project or environment
- Rotating credentials after a team member departure or suspected leak
- Reviewing secrets hygiene during a security audit or compliance check

---

## Quick Reference

| Environment | Storage | Access |
|-------------|---------|--------|
| **Local Dev** | `.env` (gitignored) | Developer only |
| **CI/CD** | Platform secrets (GitHub, GitLab) | Pipeline only |
| **Staging** | SOPS-encrypted files | Ops team |
| **Production** | Secrets manager or SOPS | Minimal access |

---

## Secrets Hierarchy

Different environments have different security requirements.

### Local Development

**Never commit secrets. Ever.**

```bash
# .gitignore - MUST include
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
```

**Local secrets pattern:**
```bash
# Create from template
cp .env.example .env

# Edit with real values (never committed)
vim .env
```

`.env.example` (committed, no real values):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp

# API Keys (get from team password manager)
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG...

# App secrets (generate with: openssl rand -hex 32)
SESSION_SECRET=
JWT_SECRET=
```

### CI/CD Secrets

Use platform-native secrets, never store in code.

**GitHub Actions:**
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh
```

**GitLab CI:**
```yaml
# .gitlab-ci.yml
deploy:
  script:
    - ./deploy.sh
  variables:
    DATABASE_URL: $DATABASE_URL  # From CI/CD settings
```

**Best practices:**
- Use environment-specific secrets (staging vs production)
- Rotate secrets after team member departures
- Audit secret access logs periodically

### Staging Environment

SOPS-encrypted files, limited access.

```bash
# Decrypt for deployment
sops -d secrets/staging.env > .env

# Deploy
docker-compose up -d

# Clean up decrypted file
rm .env
```

### Production Environment

Maximum security: secrets manager or SOPS with strict access control.

**Option A: Cloud Secrets Manager**
- AWS Secrets Manager
- GCP Secret Manager
- Azure Key Vault
- HashiCorp Vault

**Option B: SOPS-encrypted files**
- Encrypted at rest in git
- Decrypted only during deployment
- Age or GPG keys for decryption

---

## SOPS + Age Encryption

SOPS (Secrets OPerationS) with age encryption is the recommended approach for file-based secrets.

### Initial Setup

```bash
# Install SOPS
# macOS
brew install sops

# Linux (check https://github.com/getsops/sops/releases for latest version)
VERSION=3.8.1
curl -LO https://github.com/getsops/sops/releases/download/v${VERSION}/sops-v${VERSION}.linux.amd64
curl -LO https://github.com/getsops/sops/releases/download/v${VERSION}/sops-v${VERSION}.checksums.txt
sha256sum --check --ignore-missing sops-v${VERSION}.checksums.txt
sudo mv sops-v${VERSION}.linux.amd64 /usr/local/bin/sops
sudo chmod +x /usr/local/bin/sops

# Install age
# macOS
brew install age

# Linux
sudo apt install age
```

### Generate Keys

```bash
# Generate age key pair
mkdir -p ~/.config/sops/age
age-keygen -o ~/.config/sops/age/keys.txt

# Secure the key file (IMPORTANT!)
chmod 600 ~/.config/sops/age/keys.txt

# Output shows public key:
# Public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p

# BACKUP THIS FILE SECURELY
# If lost, encrypted secrets are unrecoverable
```

### Configure SOPS

Create `.sops.yaml` in repository root:

```yaml
creation_rules:
  # Production secrets - requires production key
  - path_regex: secrets/production\..*
    age: >-
      age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p

  # Staging secrets - different key
  - path_regex: secrets/staging\..*
    age: >-
      age1abc123...staging-public-key...

  # Default for other secrets
  - path_regex: secrets/.*
    age: >-
      age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

### Encrypt Secrets

```bash
# Create secrets directory
mkdir -p secrets

# Create plaintext secrets file
cat > secrets/production.env << 'EOF'
DATABASE_URL=postgresql://prod_user:supersecret@db.example.com:5432/proddb
REDIS_PASSWORD=redis_secret_password
API_KEY=sk_live_abc123...
JWT_SECRET=32_byte_random_hex_value
EOF

# Encrypt with SOPS
sops -e secrets/production.env > secrets/production.env.enc

# Remove plaintext (IMPORTANT!)
rm secrets/production.env

# Verify encryption
cat secrets/production.env.enc  # Should show encrypted values
```

### Decrypt for Deployment

```bash
# Decrypt to stdout (preferred - no file on disk)
sops -d secrets/production.env.enc | docker-compose --env-file /dev/stdin up -d

# Or decrypt to file temporarily
sops -d secrets/production.env.enc > .env
docker-compose up -d
rm .env  # Clean up immediately
```

### Edit Encrypted Files

```bash
# SOPS opens in editor, decrypts, then re-encrypts on save
sops secrets/production.env.enc
```

### Key Rotation

```bash
# Add new key to .sops.yaml, then updatekeys
sops updatekeys secrets/production.env.enc

# Old keys can still decrypt during transition
# Remove old keys from .sops.yaml when rotation complete
```

---

## HashiCorp Vault Patterns

For organizations needing dynamic secrets, centralized management, or audit trails.

### When to Use Vault

| Use Case | SOPS | Vault |
|----------|------|-------|
| Static secrets (API keys) | ✓ | ✓ |
| Dynamic secrets (DB credentials) | - | ✓ |
| Secret rotation automation | Manual | ✓ |
| Centralized audit trail | - | ✓ |
| Multi-team access control | Limited | ✓ |

### Basic Vault Patterns

**Reading secrets:**
```bash
# CLI
vault kv get -field=password secret/myapp/database

# In application (using client library)
# Python example
import hvac
client = hvac.Client(url='https://vault.example.com')
secret = client.secrets.kv.v2.read_secret_version(path='myapp/database')
password = secret['data']['data']['password']
```

**AppRole authentication (for applications):**
```bash
# Get role_id (stored in config)
vault read auth/approle/role/myapp/role-id

# Get secret_id (generated at deploy time, short-lived)
vault write -f auth/approle/role/myapp/secret-id

# Application authenticates with both
vault write auth/approle/login \
  role_id=$ROLE_ID \
  secret_id=$SECRET_ID
```

**Dynamic database credentials:**
```bash
# Vault generates temporary credentials
vault read database/creds/myapp-role

# Returns:
# username: v-approle-myapp-xxxxx
# password: A1a-xxxxxxxx
# lease_duration: 1h

# Application uses these, Vault auto-rotates
```

---

## Cloud Secrets Managers

Overview of cloud-native options.

### AWS Secrets Manager

```python
# Python
import boto3

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='myapp/production')
secrets = json.loads(response['SecretString'])
database_url = secrets['DATABASE_URL']
```

```yaml
# In ECS task definition
{
  "secrets": [
    {
      "name": "DATABASE_URL",
      "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:myapp/production:DATABASE_URL::"
    }
  ]
}
```

### GCP Secret Manager

```python
# Python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/my-project/secrets/database-url/versions/latest"
response = client.access_secret_version(name=name)
database_url = response.payload.data.decode('UTF-8')
```

### Azure Key Vault

```python
# Python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)
database_url = client.get_secret("database-url").value
```

### Comparison

| Feature | AWS | GCP | Azure | Vault |
|---------|-----|-----|-------|-------|
| Auto-rotation | ✓ | Limited | ✓ | ✓ |
| Dynamic secrets | - | - | - | ✓ |
| Multi-cloud | - | - | - | ✓ |
| Self-hosted option | - | - | - | ✓ |
| Cost | Per-secret | Per-access | Per-secret | Self-managed |

---

## Rotation Strategies

### Manual Rotation Checklist

When rotating secrets manually:

1. **Generate new secret**
   ```bash
   # Generate secure random value
   openssl rand -hex 32
   ```

2. **Update secret storage** (SOPS, Vault, or secrets manager)

3. **Deploy with new secret** (rolling update)

4. **Verify new secret works**

5. **Revoke old secret** (after grace period)

6. **Update documentation** if needed

### Automated Rotation

**AWS Secrets Manager auto-rotation:**
```python
# Lambda function for rotation
def lambda_handler(event, context):
    secret_id = event['SecretId']
    step = event['Step']

    if step == 'createSecret':
        # Generate new secret value
        new_password = generate_password()
        # Store as pending

    elif step == 'setSecret':
        # Apply new secret to service

    elif step == 'testSecret':
        # Verify new secret works

    elif step == 'finishSecret':
        # Mark as current, remove old
```

### Zero-Downtime Rotation Pattern

For secrets used by running services:

```
1. Add new secret (don't remove old)
   Old: secret_v1 ✓
   New: secret_v2 ✓

2. Deploy application that accepts BOTH
   App checks: secret_v2 || secret_v1

3. Verify all instances using new secret

4. Remove old secret
   Old: secret_v1 ✗
   New: secret_v2 ✓

5. Deploy application that only accepts new
```

---

## Incident: Secret Leaked

If a secret is exposed, act immediately.

### Immediate Response (< 5 minutes)

```bash
# 1. Rotate the leaked secret IMMEDIATELY
# Don't investigate first - rotate first

# 2. Revoke the old secret
# API keys: regenerate in provider dashboard
# Database: change password, kill sessions
# Tokens: invalidate in auth system

# 3. Deploy with new secret
sops -e secrets/production.env > secrets/production.env.enc
git add secrets/production.env.enc
git commit -m "security: rotate leaked credentials"
# Deploy immediately
```

### Investigation (after rotation)

```bash
# Check git history for the secret
git log -p --all -S 'leaked_secret_value'

# Check if secret was in any branch
git branch --contains <commit_with_secret>

# Remove from git history if needed
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret/file' \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (faster)
bfg --delete-files .env
```

### Post-Incident

1. **Document the incident**
   - How was it leaked?
   - How was it detected?
   - Timeline of response

2. **Review access logs**
   - Was the secret used maliciously?
   - What resources were accessed?

3. **Improve prevention**
   - Add pre-commit hooks
   - Review secret handling procedures
   - Train team on secret hygiene

### Prevention Tools

```bash
# Install git-secrets
brew install git-secrets

# Configure for repository
cd your-repo
git secrets --install
git secrets --register-aws  # Block AWS credentials

# Add custom patterns
git secrets --add 'password\s*=\s*.+'
git secrets --add 'api[_-]?key\s*=\s*.+'

# Scan existing history
git secrets --scan-history
```

**Pre-commit hook example:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
patterns="password\s*[=:]\s*['\"][^'\"]{8,}['\"]|secret\s*[=:]\s*['\"][^'\"]{16,}['\"]"
files=$(git diff --cached --name-only | grep -v '\.md$')
if [ -n "$files" ] && echo "$files" | xargs grep -lE "$patterns" 2>/dev/null; then
    echo "Potential secrets detected in commit"
    exit 1
fi
```

---

## Verification Checklist

### Pre-Deployment

- [ ] No secrets in code (run `git secrets --scan`)
- [ ] All secrets encrypted (SOPS or secrets manager)
- [ ] `.env` files in `.gitignore`
- [ ] Secrets manager access configured
- [ ] Rotation schedule documented

### Access Review (Quarterly)

- [ ] Who has access to production secrets?
- [ ] Are there unused secrets to revoke?
- [ ] Are rotation schedules being followed?
- [ ] Are audit logs being reviewed?

---

## Integration with Playbook

**Part of production readiness:**
- `/pb-hardening` — Infrastructure security
- `/pb-secrets` — Secrets management (this command)
- `/pb-security` — Application security review
- `/pb-deployment` — Deployment strategies

**Workflow:**
```
Development (local .env)
    ↓
CI/CD (platform secrets)
    ↓
Staging (SOPS-encrypted)
    ↓
Production (secrets manager or SOPS)
```

---

## Quick Commands

| Action | Command |
|--------|---------|
| Generate random secret | `openssl rand -hex 32` |
| Encrypt with SOPS | `sops -e file.env > file.env.enc` |
| Decrypt with SOPS | `sops -d file.env.enc` |
| Edit encrypted file | `sops file.env.enc` |
| Scan for secrets | `git secrets --scan` |
| Scan history | `git secrets --scan-history` |

---

## Related Commands

- `/pb-hardening` — Production security hardening for infrastructure
- `/pb-security` — Application-level security review
- `/pb-deployment` — Deploy with secure secrets handling

---

*A secret is only secret if no one who shouldn't know it, knows it.*
