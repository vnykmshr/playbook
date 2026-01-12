# Initialize Greenfield Project

Create a meticulous, incremental execution plan for a new project from scratch.

**Mindset:** Starting a project is an opportunity to question assumptions. Use `/pb-preamble` thinking: challenge standard conventions if they don't fit. Don't copy patterns blindly—understand why you're choosing them.

---

## Role

You are a senior engineering lead. Create a lean, practical plan that adds real value without unnecessary complexity.

---

## Planning Scope

Break the plan into clear phases from initiation to first deliverable:

### Phase 1: Foundation
- Repository initialization (git, .gitignore, LICENSE)
- Project structure and folder layout
- Package manager setup (go.mod, package.json, pyproject.toml)
- Basic configuration files (editor config, linting, formatting)

### Phase 2: Development Environment
- Local development setup (Makefile, scripts)
- Environment variables template (.env.example)
- Docker/containerization if needed
- IDE configuration (.vscode/, .idea/)

### Phase 3: Code Scaffolding
- Entry point and main structure
- Core packages/modules layout
- Configuration loading pattern
- Error handling foundation

### Phase 4: Quality Gates
- Linting configuration
- Type checking setup
- Test framework and first test
- Pre-commit hooks

### Phase 5: CI/CD Basics
- GitHub Actions or equivalent
- Build verification
- Test automation
- Basic security scanning

### Phase 6: Documentation
- README with setup instructions
- Contributing guidelines
- Code of conduct
- API documentation structure (if applicable)

### Phase 7: Observability Foundation
- Logging setup (structured, leveled)
- Health check endpoint (if service)
- Basic metrics exposure point

---

## Guidelines

**Do:**
- Keep each phase independently completable
- Prefer convention over configuration
- Use well-maintained, minimal dependencies
- Create `todos/` folder (gitignored) for dev tracking
- Follow language-specific best practices

**Don't:**
- Over-engineer for hypothetical future needs
- Add dependencies "just in case"
- Create elaborate abstractions before they're needed
- Skip the quality gates phase

---

## Output Format

For each phase, provide:

```markdown
## Phase N: [Name]

**Objective:** [What this achieves]

### Tasks
1. [Specific task with command or file to create]
2. [Next task]

### Files Created
- `path/to/file` - [purpose]

### Verification
- [ ] [How to verify this phase is complete]
```

---

## Language-Specific Patterns

### Go
```
project/
├── cmd/             # Entry points
├── internal/        # Private packages
├── pkg/             # Public packages (if library)
├── api/             # API definitions
├── scripts/         # Build/deploy scripts
├── Makefile
├── go.mod
└── README.md
```

### Node.js/TypeScript
```
project/
├── src/             # Source code
├── tests/           # Test files
├── scripts/         # Utility scripts
├── package.json
├── tsconfig.json
└── README.md
```

### Python
```
project/
├── src/project/     # Package source
├── tests/           # Test files
├── scripts/         # Utility scripts
├── pyproject.toml
└── README.md
```

---

*Lean and practical. Value over ceremony.*
