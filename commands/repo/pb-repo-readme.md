# Generate Project README

Write or rewrite a clear, professional, developer-friendly README.

**Philosophy:** A good README invites scrutiny. Use `/pb-preamble` thinking: examples and assumptions must be clear enough that errors are obvious. Unclear READMEs hide problems.

---

## Objective

Create a README that helps developers understand, install, and use the project quickly. Prioritize clarity and practical examples over lengthy explanations.

---

## Tone & Style

- Concise, technical, professional
- Like well-maintained library documentation
- Focus on what it does, why it matters, how to use it
- No marketing language, fluff, or AI-sounding phrases
- No emojis unless project has established emoji usage
- Examples over prose

---

## Structure

### 1. Title & One-Line Summary
```markdown
# Project Name

Brief description of purpose (one line).
```

### 2. Badges (Optional but Recommended)
```markdown
[![Build Status](url)](link)
[![Coverage](url)](link)
[![Version](url)](link)
[![License](url)](link)
```

**Common badges by language:**
- **Go:** Go Reference, Go Report Card, Coverage
- **Node:** npm version, bundle size, downloads
- **Python:** PyPI version, Python versions, Coverage

### 3. Overview / Features
- What problem it solves
- Key capabilities (3-5 bullet points max)
- When to use it

### 4. Installation

**Go:**
```markdown
## Installation

```bash
go get github.com/user/project
```
```

**Node:**
```markdown
## Installation

```bash
npm install package-name
# or
yarn add package-name
```
```

**Python:**
```markdown
## Installation

```bash
pip install package-name
```
```

### 5. Quick Start
Minimal runnable example that demonstrates core functionality.

```markdown
## Quick Start

```go
// Minimal example showing primary use case
```
```

### 6. Usage / API
- Primary functions or methods
- Configuration options
- Common patterns

### 7. Configuration (if applicable)
- Environment variables
- Config file format
- Default values

### 8. How It Works (Optional)
- Brief architecture or algorithm overview
- Useful for complex projects

### 9. Performance / Benchmarks (Optional)
- Only if performance is a key feature
- Include actual numbers, not claims

### 10. License
```markdown
## License

MIT License - see [LICENSE](LICENSE) for details.
```

### 11. Contributing (Optional)
```markdown
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
```

---

## Guidelines

**Do:**
- Keep examples self-contained and runnable
- Link to detailed API docs if available
- Use syntax-highlighted code blocks
- Keep under ~200 lines for libraries

**Don't:**
- Explain obvious things
- Use marketing superlatives
- Include implementation details in README
- Leave placeholder sections

---

## Template

```markdown
# Project Name

One-line description of what this does.

[![Build](badge-url)](link) [![Coverage](badge-url)](link)

## Overview

[2-3 sentences: what problem it solves and for whom]

**Key Features:**
- Feature one
- Feature two
- Feature three

## Installation

```bash
[install command]
```

## Quick Start

```language
// Minimal working example
```

## Usage

### Basic Usage

```language
// Common use case
```

### Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | `string` | `""` | What it does |

## API Reference

[Link to full API docs or brief inline reference]

## License

MIT
```

---

## Language-Specific Notes

### Go
- Link to pkg.go.dev for API reference
- Include Go version requirements
- Show module import path

### Node/TypeScript
- Mention TypeScript support if applicable
- Show both CommonJS and ESM imports if supported
- Note browser vs Node compatibility

### Python
- Specify Python version requirements
- Link to PyPI and ReadTheDocs if available
- Show type hints in examples

---

*Clear README, happy developers.*
