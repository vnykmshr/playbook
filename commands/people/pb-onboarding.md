# Developer Onboarding & Knowledge Transfer

Effective onboarding reduces time to productivity, builds confidence, and prevents knowledge loss.

---

## Purpose

Good onboarding:
- **Accelerates productivity**: New person contributes within days, not months
- **Improves retention**: Strong onboarding = people stay longer
- **Transfers knowledge**: Prevents loss when people leave
- **Sets culture**: First impression shapes how people work
- **Reduces mistakes**: Clear training prevents common errors

Bad onboarding:
- "Here's your laptop, good luck"
- New person struggles for weeks
- Knowledge exists only in one person's head
- People leave quickly (bad first impression)

**Culture First:** Onboarding should teach both frameworks on day one.

Teach `/pb-preamble`: new team members need to know—challenge assumptions, disagree when needed, prefer correctness. Teach `/pb-design-rules`: introduce the design principles (Clarity, Simplicity, Modularity, Robustness) that guide how this team builds systems. This is how you set culture from the start.

---

## Onboarding Timeline

### Before First Day

**Hiring & Preparation (2-3 weeks before)**

```
☐ Equipment ordered (laptop arrives before first day)
☐ Accounts created (email, GitHub, Slack, VPN, etc.)
☐ Welcome message written by manager
☐ Buddy assigned (person to answer questions)
☐ Documentation prepared (key docs linked, not overwhelming)
☐ First project identified (small, real, supported)
```

**What to send before day 1:**

```
Email from manager:
"Welcome! I'm excited to have you join.
Before you start, here's what to expect:

Day 1: Setup, meet the team, understand our workflow
Week 1: Learning the codebase and key systems
Week 2-4: First code contributions with support
Month 1-3: Ramping up to full productivity

Your buddy is [Name]. Slack them anytime.
Your first small project will be [project].
We'll have daily 15-min check-ins first week.
Questions? Ask—this is what we're here for.

See you Monday!"
```

### Day 1: Setup & Welcome

**Goal: Get working, feel welcomed, know who to ask**

```
Morning (2 hours):
  - Equipment works (this matters!)
  - Development environment sets up (with buddy help)
  - Slack/email/VPN/GitHub access works
  - Welcome from team (Slack message with emoji reactions)

Afternoon (2 hours):
  - 1-on-1 with manager (get to know you, answer questions)
  - Async video tour of systems (record this for future hires)
  - Read company mission/culture docs
  - No meetings, just setup

Day 1 success: Person can build the code and start exploring
```

**Equipment checklist:**
```
☐ Laptop works, fast enough
☐ Monitor, keyboard, mouse (if office)
☐ Phone/access badge (if office)
☐ All software installed before arrival
```

### Week 1: Learning Pace

**Goal: Understand codebase, systems, and process**

**Daily schedule:**
```
9:30am: 15 min check-in with manager
        "What did you learn? Questions? Blockers?"
        (Builds rapport, catches confusion early)

Morning: Self-paced learning
        - Read key architecture docs
        - Watch system demo video (recorded)
        - Explore codebase (with guide from senior engineer)

Afternoon: Pairing session (1-2 hours)
        - Senior engineer shows how to:
          * Run the tests
          * Deploy to staging
          * Debug a common issue
          * Review a PR

Evening: Self-directed exploration
        - Try to run tests alone
        - Read relevant code
        - Write down questions
```

**What to learn by end of week 1:**
```
☐ Codebase compiles/runs locally
☐ How to run tests
☐ How to deploy to staging
☐ Key system architecture (high level)
☐ Code review process
☐ How to get help (who to ask what)
☐ Company culture and values
```

**Red flags if person is lost:**
- Can't run code after 2 days (fix environment, not person)
- Doesn't know who to ask questions (assign a buddy immediately)
- Setup still broken (devops needed)
- Feels unwelcome (check in more often)

### Week 2-3: First Contributions

**Goal: Make first code changes with support**

**Process:**

```
Monday: Small, bounded task assigned
        - "Fix this typo in error message" (30 min)
        - "Add a test for this function" (1-2 hours)
        - "Update documentation" (1 hour)
        (Real work, but contained)

Create PR, pair with senior for review
        - "Here's what I'd change and why"
        - "Let's discuss your approach"
        - Not just approving, educating

Merge together, person learns from process

Repeat 2-3 times, gradually increase difficulty
```

**Task progression:**
```
Week 2: Documentation, tests, small fixes (low risk)
Week 3: Real features with guidance (medium risk)
Week 4: Independent with code review (normal risk)
```

**Example first task:**
```
Task: Add input validation error message
Scope: 1 file, 10 lines added, well-tested
Learning: Code change process, testing, review
Risk: Very low (only affects error message)
```

**What NOT to do:**
```
[NO] Throw person at complex system
[NO] Make them read 10,000 lines of code first
[NO] Assign a huge feature with no support
[NO] Disappear and let them struggle alone
```

### Month 1: Building Confidence

**Goal: Feel competent, ask fewer questions, enjoy the work**

**Activities:**
```
Week 2-4: Increasing task complexity
        Small tasks → Medium features → System understanding

1-on-1s: Weekly (1 hour)
        - How are you feeling?
        - What's going well? What's hard?
        - Career expectations (long term)
        - Feedback on code quality

Pairing: 1-2 sessions per week (decreasing)
        - Now pairing on their tasks
        - Eventually observing code reviews instead

Code review: Every PR reviewed, feedback given
        - Pointing out learning opportunities
        - Teaching not just approving/rejecting
```

**Success criteria by end of month 1:**

Quantitative milestones (can measure):
```
☐ First PR merged by day 5 (shows you can code)
☐ 5+ PRs merged by end of week 3 (demonstrates productivity)
☐ Can run tests/deploy independently (self-sufficient)
☐ Average PR takes <1 day to merge (not blocked)
☐ Code review feedback positive (quality meeting standard)
```

Qualitative milestones (team feedback):
```
☐ Asks targeted questions (not "how do I set up?")
☐ Code quality comparable to team
☐ Comfortable speaking in meetings
☐ Knows team members and can pair with them
☐ Takes initiative (suggests improvements)
```

Red flags (needs help):
```
[NO] No PR by week 2 (blocked or overwhelmed)
[NO] PRs have major quality issues (misunderstood standards)
[NO] Silent in meetings (not engaged or confused)
[NO] Many questions about basics (environment still broken)
[NO] Asking to be switched to different project (didn't fit)
```

### Month 2-3: Full Ramp

**Goal: Fully productive, independent, integrated**

**Activities:**
```
1-on-1s: Biweekly (align with other team members)
        - Technical growth
        - Career development
        - Team fit

Tasks: Normal difficulty, assigned like any team member
        - Bugs, features, infrastructure work

Mentorship: If they show strength, pair them with junior
        - Teaches them system deeply
        - Builds leadership skills
```

**End of month 3 assessment:**
```
☐ Can work independently (doesn't need daily check-ins)
☐ Code quality meets team standard
☐ Contributing to design discussions
☐ Helping other team members
☐ Feels integrated (invited to social events)
☐ No questions about what to do (knows how to get work)
```

---

## Knowledge Transfer Essentials

Most knowledge in engineering is in people's heads. Capture it.

### What to Document

**Critical (Must document):**
```
- System architecture (diagrams, how pieces connect)
- How to set up development environment
- How to deploy and rollback
- Common troubleshooting (fixes, not explanations)
- Company policies and processes
- Security practices (how to handle secrets)
```

**Important (Should document):**
```
- Key design decisions (why built this way)
- Common gotchas ("Don't use X, it causes Y")
- How to test locally
- How to debug common issues
- Code organization (why code is where it is)
```

**Nice to have (Could document):**
```
- Detailed code explanations (good code is self-documenting)
- Historical context (why we chose X over Y 2 years ago)
- Personal preferences (I like comments here)
```

### Documentation for Onboarding

**README for new developers:**
```markdown
# Getting Started as a Developer

## Before you start
- Clone the repo
- Install Docker
- Install Node 18+

## First 5 minutes
```bash
npm install
npm run dev
```
Should see "Server running on localhost:3000"

## First hour
- Read architecture.md (5 min)
- Watch system-overview.mp4 (10 min)
- Explore `/src/components` (15 min)
- Ask buddy any questions (30 min)

## First day
- Set up local database (with buddy's help)
- Run test suite
- Make a small change (fix typo)
- Submit PR (buddy will review)

## Useful commands
- `npm test` — Run tests
- `npm run dev` — Start server
- `npm run deploy-staging` — Deploy to staging
- `npm run lint` — Check code style

## Getting help
- Slack #engineering for questions
- Buddy: [Name] (@slack-handle)
- Common issues: See TROUBLESHOOTING.md
```

**Architecture document:**
```markdown
# System Architecture

## Overview
[Diagram showing: Frontend → API → Database]

## Key components
1. **Frontend** (React)
   - Location: `/src`
   - Entry point: `/src/index.js`
   - Build: `npm run build`

2. **API** (Node.js)
   - Location: `/api`
   - Entry point: `/api/server.js`
   - Port: 5000

3. **Database** (PostgreSQL)
   - Lives in Docker
   - Schema: `/database/schema.sql`
   - How to reset: `npm run reset-db`

## How they connect
Frontend makes HTTP requests to API at http://localhost:5000
API talks to database
```

**Troubleshooting document:**
```markdown
# Common Issues

## "npm install fails"
Solution: Delete node_modules, clear npm cache, reinstall
```bash
rm -rf node_modules
npm cache clean --force
npm install
```

## "Database connection refused"
Solution: Make sure Docker is running
```bash
docker ps
docker-compose up -d
```

## "Tests fail locally but pass in CI"
Likely cause: Different Node version
Solution: `nvm use 18.0.0` (see .nvmrc)

## "Port 3000 already in use"
Solution: Kill the process
```bash
lsof -i :3000
kill -9 [PID]
```
```

### Video Documentation

For critical processes, record a video (~5-10 min):

**Examples:**
```
1. "Setting up local environment" (7 min video)
   - Clear screen
   - Explain each step
   - Show common errors and fixes
   - End result: Working dev environment

2. "How to deploy to staging" (5 min video)
   - How to check if deploy is working
   - What logs to look at
   - How to rollback if something breaks

3. "Code review process" (5 min video)
   - How we check PRs
   - What we look for
   - Common feedback
```

Tools: Loom (free, simple), Asciinema (terminal recordings), ScreenFlow (Mac)

---

## Onboarding Checklist

### Before Arrival
- [ ] Equipment ordered and tested
- [ ] Accounts created (email, GitHub, Slack, VPN)
- [ ] Welcome message from manager
- [ ] Buddy assigned and briefed
- [ ] First project identified
- [ ] Key documentation linked
- [ ] Development environment setup guide created/updated

### Day 1
- [ ] Equipment works (laptop, monitor, mouse, etc.)
- [ ] Software is installed
- [ ] Development environment compiles
- [ ] Slack/email/GitHub access works
- [ ] Welcome from team (all-hands message)
- [ ] 1-on-1 with manager (30 min)
- [ ] Async video tour of systems
- [ ] No meetings beyond above
- [ ] Person goes home excited (not overwhelmed)

### Week 1
- [ ] Daily 15-min check-ins (quick questions)
- [ ] Architecture overview understood (high-level)
- [ ] Code compiles and tests run locally
- [ ] Pairing session with senior engineer (1-2 hours)
- [ ] First small task assigned and completed
- [ ] Questions are welcomed and answered
- [ ] Person feels safe to ask "dumb" questions

### Week 2-3
- [ ] 2-3 small code contributions merged
- [ ] Code review process understood
- [ ] How to test and deploy known
- [ ] Team members' names learned
- [ ] Comfortable in team meetings
- [ ] Buddy is readily available
- [ ] Tasks are getting slightly harder

### Month 1
- [ ] 5+ PRs merged (small to medium tasks)
- [ ] Understands codebase organization
- [ ] Can debug simple issues independently
- [ ] Knows how to get help for hard problems
- [ ] Code quality meets team standard
- [ ] Feels like part of the team
- [ ] Weekly 1-on-1s with manager established

### Month 2-3
- [ ] Fully productive on normal tasks
- [ ] Doesn't need daily check-ins
- [ ] Contributing to design discussions
- [ ] Starting to mentor others (if strong)
- [ ] Comfortable asking questions without anxiety
- [ ] Integrated into team social activities
- [ ] Clear on career path and growth areas

---

## Retention Factors

People who have good onboarding stay longer. Key factors:

| Factor | Importance | How to Provide |
|--------|-----------|----------------|
| Clear expectations | Critical | Manager explains goals, metrics, culture |
| Technical ramp support | Critical | Buddy, pairing, documentation |
| Belonging | Critical | Include in team, welcome openly |
| Competence | Critical | Achievable first tasks, support |
| Growth path | Important | Discuss long-term goals in first month |
| Fair compensation | Important | Set clear salary/equity upfront |
| Interesting work | Important | Assign meaningful first project |

People who feel lost after month 1 often leave by month 6.

---

## Remote Onboarding Specifics

Same as above, but emphasize:

**1. Async documentation**
- Everything written, not just meetings
- Videos for complex topics
- Can be done on their schedule

**2. Recorded sessions**
- Record all pairing sessions
- Record architecture walkthroughs
- They can watch at their pace

**3. Extra communication**
- Check in slightly more (time zone isolation)
- Video not just voice calls
- Clear async communication norms

**4. Social connection**
- Schedule virtual coffee chats
- Include in team chat (don't feel left out)
- Virtual onboarding lunch with team

---

## Knowledge Preservation

When someone leaves, their knowledge shouldn't leave with them.

### During Employment

**Quarterly knowledge capture:**
```
Each person documents:
  - Systems they own (architecture, how to debug)
  - Decisions they made (why, alternatives considered)
  - Critical processes they do
  - People and relationships they maintain
```

**Code quality:**
```
- Self-documenting code (good naming, structure)
- Comments for why, not what
- Code reviews that explain thinking
```

### When Someone Leaves

**Exit interview:**
```
Manager: "What knowledge should others have that I don't have?"
Manager: "What systems do only you understand?"
Person: Document critical processes

2-week transition:
  - Document your work
  - Pair with your replacement
  - Write down gotchas and lessons learned
  - Introduce to your contacts
```

**Knowledge handoff:**
```
Before last day:
  - List of systems you owned
  - How each system works (document or record)
  - Key people to know for each system
  - Critical processes you did
```

---

## Integration with Playbook

**Part of SDLC cycle:**
- `/pb-team` — Team culture onboarding
- `/pb-guide` — Engineering practices to learn
- `/pb-commit` — Code review process training
- `/pb-standards` — Code style to learn

---

## Related Commands

- `/pb-team` — Where onboarding fits in team
- `/pb-documentation` — How to write for onboarding
- `/pb-cycle` — Code review process they'll follow
- `/pb-knowledge-transfer` — KT session preparation

---

*Created: 2026-01-11 | Category: People | Tier: M/L*

