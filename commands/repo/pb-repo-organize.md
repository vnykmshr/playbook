# Organize Repository Structure

Clean up and reorganize the project root for clarity and maintainability.

---

## Objective

Review all files and directories in the project root. Keep only essential files at the top level, move everything else into logical subfolders.

---

## Guidelines

### Keep at Root
Essential files that belong at the top level:

```
README.md           # Project overview
LICENSE             # License file
CHANGELOG.md        # Version history
CONTRIBUTING.md     # Contribution guidelines
CODE_OF_CONDUCT.md  # Community guidelines
SECURITY.md         # Security policy

# Build/Config
Makefile            # Build commands
Dockerfile          # Container definition
docker-compose.yml  # Container orchestration
.env.example        # Environment template

# Language-specific
go.mod / go.sum     # Go modules
package.json        # Node.js
pyproject.toml      # Python
Cargo.toml          # Rust

# Editor/CI
.gitignore
.editorconfig
```

### Move to Subfolders

| Content | Destination |
|---------|-------------|
| Documentation | `/docs` |
| Shell scripts | `/scripts` |
| Example code | `/examples` |
| Internal packages | `/internal` |
| Static assets | `/assets` |
| CI/CD configs | `/.github` or `/ci` |
| Kubernetes/Helm | `/deploy` or `/k8s` |

### Protected Folders

**Do not remove or modify:**
- `/todos` — Development tracker (gitignored)
- `/.git` — Version control

---

## GitHub Special Files

GitHub auto-detects certain files in specific locations:

```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
├── PULL_REQUEST_TEMPLATE.md
├── FUNDING.yml
├── CODEOWNERS
└── workflows/
    └── ci.yml

# Root level (GitHub detects these)
README.md
LICENSE
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
```

---

## Process

### Step 1: Audit Current State
```bash
# List all root-level files and folders
ls -la

# Find files that might need reorganization
find . -maxdepth 1 -type f | grep -v -E '^\./\.|README|LICENSE|Makefile|go\.|package|pyproject'
```

### Step 2: Create Target Folders
```bash
mkdir -p docs scripts examples assets
```

### Step 3: Move Files
```bash
# Example moves (adjust for your project)
mv *.sh scripts/           # Shell scripts
mv docs/*.md docs/         # Documentation
mv examples/* examples/    # Example code
```

### Step 4: Update References
- Fix any hardcoded paths in code
- Update import statements if needed
- Verify build still works

### Step 5: Verify
```bash
# Ensure build passes
make build  # or equivalent

# Ensure tests pass
make test

# Check nothing is broken
git status
```

---

## Ideal Root Layout

After cleanup, the root should look like:

```
project/
├── .github/            # GitHub configs
├── cmd/                # Entry points (Go)
├── src/                # Source code
├── internal/           # Private packages
├── pkg/                # Public packages
├── docs/               # Documentation
├── scripts/            # Utility scripts
├── examples/           # Example code
├── assets/             # Static assets
├── deploy/             # Deployment configs
├── todos/              # Dev tracking (gitignored)
│
├── README.md
├── LICENSE
├── CHANGELOG.md
├── Makefile
├── Dockerfile
├── .gitignore
└── [language config]   # go.mod, package.json, etc.
```

---

## Anti-Patterns to Fix

| Problem | Solution |
|---------|----------|
| Random scripts at root | Move to `/scripts` |
| Multiple READMEs | Consolidate or move extras to `/docs` |
| Config files scattered | Group in root or `/config` |
| Test fixtures at root | Move to `/testdata` or `/tests/fixtures` |
| Unused files | Delete them |

---

*Clean roots lead to clear thinking.*
