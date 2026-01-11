# Generate GitHub About & Tags

Create a concise, search-optimized GitHub "About" description and relevant topic tags.

---

## Objective

Write a compelling one-line description (≤160 chars) and suggest discoverable tags for the repository.

---

## About Section Guidelines

**Include:**
- What the project does (primary function)
- Who it's for (target audience)
- Key trait (reliable, fast, lightweight, etc.)
- Main tech stack or domain if relevant

**Avoid:**
- Marketing buzzwords ("revolutionary", "next-gen")
- Vague descriptions ("a tool for things")
- Redundant phrases ("written in Go" when Go is tagged)
- Starting with "A" or "An"

---

## Examples

**Good:**
```
High-performance job queue for Go with Redis backend and at-least-once delivery
```
```
Type-safe API client generator from OpenAPI specs for TypeScript
```
```
Lightweight feature flag service with real-time updates and audit logging
```

**Bad:**
```
A revolutionary next-generation tool for managing stuff efficiently  [NO]
```
```
My awesome project  [NO]
```
```
Node.js application  [NO]
```

---

## Tags Guidelines

**Suggest 6-10 tags mixing:**
- Broad category (e.g., `backend`, `cli`, `library`)
- Language/framework (e.g., `golang`, `typescript`, `react`)
- Domain (e.g., `authentication`, `payments`, `devops`)
- Specific tech (e.g., `redis`, `postgresql`, `grpc`)
- Use case (e.g., `microservices`, `serverless`, `real-time`)

**Format:**
- Lowercase
- Hyphenated for multi-word (`job-queue`, `feature-flags`)
- No spaces

**Avoid:**
- Generic: `opensource`, `software`, `code`, `project`
- Redundant: language name if obvious from repo
- Overly specific: internal project names

---

## Output Format

```text
About: [Concise 1-line summary, ≤160 chars]

Tags: tag1, tag2, tag3, tag4, tag5, tag6
```

---

## Process

### Step 1: Analyze the Repository
- Read README and main source files
- Identify primary purpose and functionality
- Note the tech stack and dependencies
- Understand the target user

### Step 2: Draft About
- Write 2-3 candidate descriptions
- Pick the most specific and clear one
- Verify it's under 160 characters

### Step 3: Select Tags
- Start with the primary language/framework
- Add the main domain or problem space
- Include specific technologies used
- Add use-case descriptors

### Step 4: Validate
- Does the About tell someone what this is in 5 seconds?
- Would the tags help someone discover this project?
- Is anything redundant or vague?

---

## Tag Categories Reference

| Category | Examples |
|----------|----------|
| Languages | `golang`, `typescript`, `python`, `rust` |
| Frameworks | `react`, `fastapi`, `gin`, `express` |
| Domains | `authentication`, `payments`, `analytics`, `devops` |
| Infrastructure | `kubernetes`, `docker`, `terraform`, `aws` |
| Databases | `postgresql`, `redis`, `mongodb`, `sqlite` |
| Patterns | `microservices`, `serverless`, `event-driven`, `rest-api` |
| Use Cases | `cli`, `library`, `sdk`, `api`, `backend`, `frontend` |

---

*Clear description, discoverable tags.*
