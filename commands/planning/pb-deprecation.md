---
name: "pb-deprecation"
title: "Deprecation & Backwards Compatibility Strategy"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-adr', 'pb-release', 'pb-documentation']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Deprecation & Backwards Compatibility Strategy

Plan, communicate, and execute deprecations with zero surprises. Keep users moving forward while respecting their timelines.

---

## Purpose

Deprecation allows you to:
- Remove technical debt without breaking users
- Guide users toward better APIs or patterns
- Maintain stability while improving the system
- Plan breaking changes transparently

**The principle**: Give users time and clear guidance to migrate.

**Mindset:** Deprecation decisions should be made with both frameworks.

Use `/pb-preamble` thinking: challenge whether this change is really necessary; surface the impact on users; be honest about the cost vs. benefit. Use `/pb-design-rules` thinking: ensure the new approach is genuinely simpler (Simplicity), clearer (Clarity), and more robust than what it replaces. This is where critical thinking matters most.

**Resource Hint:** sonnet — Deprecation planning follows structured process; implementation-level guidance.

---

## When to Deprecate

Deprecate when:
- API endpoint needs replacement (new version, different design)
- Feature is being removed (no longer supported)
- Pattern is being phased out (better alternative exists)
- Library/dependency is outdated (security, performance)
- Database column/table is being removed

Don't deprecate:
- Bugs (fix, don't deprecate)
- Internal implementation details (users shouldn't depend on these)
- Things that change frequently (use feature flags instead)

---

## The Deprecation Timeline

Standard timeline: **6-12 months** (adjust for your users)

```
Day 1: Announce Deprecation
  └─ Mark as deprecated in code
  └─ Send notice to users (email, blog, release notes)
  └─ Provide migration guide
  └─ Publish removal date (6+ months out)

Month 1-5: Support & Guidance
  └─ Provide migration support
  └─ Maintain deprecated feature (don't break)
  └─ Answer questions, help migrations
  └─ Track adoption of new alternative

Month 6: Final Warning
  └─ Send final notice (30-60 days before removal)
  └─ Escalate to major users still on old path
  └─ Offer direct migration support

Month 7: Removal
  └─ Remove deprecated code
  └─ Update documentation
  └─ Provide post-removal support for issues

After Removal: Long-tail Support
  └─ Answer questions for users who didn't migrate
  └─ Provide limited migration support
  └─ Document what changed and why
```

**Timeline variations by stability level**:
- **Stable/Production APIs**: 12+ months (users depend on this)
- **Beta/Preview APIs**: 3-6 months (users expect changes)
- **Internal/Private APIs**: Can be immediate (only internal users)

---

## Communication Strategy

### Phase 1: Announcement

**What to communicate**:
1. What is being deprecated (be specific)
2. Why (what's better about the replacement)
3. What to use instead (concrete migration path)
4. When it will be removed (specific date)
5. How to get help

**Channels**:
- Blog post (main announcement)
- Email to affected users
- Release notes
- GitHub issues (if open source)
- Slack/Discord (if applicable)
- In-app notifications (if users log in)

**Template**:
```
DEPRECATION NOTICE

The /api/v1/users endpoint is deprecated as of [DATE].

Reason: We're consolidating to a single, more flexible API design.

Migration Path:
  Old: GET /api/v1/users/{id}
  New: GET /api/v2/users/{id}

  Differences: [describe changes]

  Migration guide: [link to detailed guide]

Removal Date: [6 months from now]

Support: [how to contact for help]
```

### Phase 2: Support Period

During 6-month window:
- **Weekly**: Monitor usage, see who's migrating
- **Monthly**: Share migration progress publicly
- **As-needed**: Provide direct support to major users
- **Final month**: Direct outreach to non-migrated users

### Phase 3: Final Warning (30-60 days before)

Send final notice:
- Strong tone ("this will be removed")
- Specific date and time
- Links to migration resources
- Direct contact for help
- List of any users still not migrated (if possible)

### Phase 4: Post-Removal

After removal:
- Update all documentation
- Blog post explaining what changed
- Provide "we removed X, here's how to fix it" guide
- Keep old documentation archived (for historical reference)
- Maintain some support for questions

---

## Code Examples: Marking Deprecated

### Python

```python
import warnings
from functools import wraps

def deprecated(replacement=None):
    """Decorator to mark functions as deprecated."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            msg = f"{func.__name__} is deprecated as of v2.0"
            if replacement:
                msg += f", use {replacement} instead"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@deprecated(replacement="get_user_v2")
def get_user(user_id):
    """Get user by ID. Use get_user_v2 instead."""
    return User.query.get(user_id)

# When called:
# UserWarning: get_user is deprecated as of v2.0, use get_user_v2 instead
```

### JavaScript/TypeScript

```typescript
/**
 * @deprecated Use getUserV2() instead (removal: 2026-07-01)
 */
export function getUser(userId: string): User {
  console.warn(
    "getUser() is deprecated and will be removed on 2026-07-01. " +
    "Use getUserV2() instead. " +
    "Migration guide: https://docs.example.com/migration"
  );
  return fetchUser(userId);
}

// Modern approach with TypeScript
export function getUser(userId: string): User {
  throw new Error(
    "getUser() was removed on 2026-07-01. Use getUserV2() instead. " +
    "Migration guide: https://docs.example.com/migration"
  );
}
```

### REST API Endpoints

```
GET /api/v1/users/{id}  (Deprecated: 2026-04-01, Removed: 2026-07-01)

Response headers:
  Deprecation: true
  Sunset: Sun, 01 Jul 2026 00:00:00 GMT
  Link: </api/v2/users/{id}>; rel="successor-version"

Body:
{
  "user": {...},
  "_deprecation": {
    "message": "This endpoint is deprecated",
    "removal_date": "2026-07-01",
    "migration_guide": "https://docs.example.com/api/v1-to-v2",
    "use_instead": "GET /api/v2/users/{id}"
  }
}
```

### Database Schema

```sql
-- Mark column as deprecated (PostgreSQL with comments)
COMMENT ON COLUMN users.old_phone_field IS
  'DEPRECATED (removal: 2026-07-01). Use phone_numbers table instead. '
  'Migration: https://docs.example.com/migrations/phone';

-- Add migration helper column
ALTER TABLE users ADD COLUMN phone_numbers_migrated BOOLEAN DEFAULT FALSE;

-- Track migration progress
SELECT COUNT(*) as unmigrated
FROM users
WHERE phone_numbers_migrated = FALSE;
```

---

## Migration Guide Template

Create a migration guide for each deprecated feature:

```markdown
# Migrating from X to Y

## What's changing
[Explain what's deprecated and why]

## Timeline
- Announced: [date]
- Removal date: [date]
- Support window: [duration]

## Step-by-step migration

### Step 1: Update imports
Before:
  import { getUserData } from 'old-api';

After:
  import { getUser } from 'new-api';

### Step 2: Update function calls
Before:
  const data = getUserData(userId, { include: ['profile', 'settings'] });

After:
  const user = getUser(userId);
  const profile = user.profile;
  const settings = user.settings;

### Step 3: Update error handling
Before:
  try {
    data = getUserData(userId);
  } catch (error) {
    // Handle 404, 403, 500
  }

After:
  try {
    user = getUser(userId);
  } catch (error) {
    // Handle NotFoundError, ForbiddenError, InternalError
  }

## Common issues & solutions

Q: What if I have custom code using old-api?
A: See [example](/docs/custom-code-migration)

Q: Will old code still work after [date]?
A: No, it will throw an error.

## Need help?
- Check [FAQ](/docs/faq)
- Ask in [community forum](/forum)
- Email support@example.com
```

---

## Testing Deprecated Code Paths

Keep deprecated features working as long as they're deprecated:

```python
# Test that deprecated function still works
def test_deprecated_get_user_still_works():
    """Deprecated getUser() should still return correct data."""
    with pytest.warns(DeprecationWarning):
        user = get_user(user_id=123)

    assert user.id == 123
    assert user.name == "Test User"

# Test that replacement works
def test_new_get_user_v2_works():
    """New getUserV2() should work identically."""
    user = get_user_v2(user_id=123)

    assert user.id == 123
    assert user.name == "Test User"

# Test both produce same result
def test_old_and_new_produce_same_result():
    """Both APIs should return identical data."""
    with pytest.warns(DeprecationWarning):
        old_result = get_user(user_id=123)

    new_result = get_user_v2(user_id=123)

    assert old_result.id == new_result.id
    assert old_result.name == new_result.name
```

---

## Tracking Deprecation Progress

Create a deprecation tracking dashboard:

```
Deprecation: GET /api/v1/users -> GET /api/v2/users

Timeline:
  Announced: 2026-01-15
  Removal: 2026-07-15
  Days until removal: 182
  Progress: 67%

Usage Statistics:
  Total requests: 10,000/day (baseline)
  v1 requests: 3,300/day (-67% from peak)
  v2 requests: 6,700/day (+67% from launch)

  Top users still on v1:
    1. company-a.com: 1,200 req/day (email sent 2x)
    2. company-b.com: 800 req/day (contact ongoing)
    3. internal-service: 600 req/day (team assigned)
    4. personal-projects: 700 req/day (not contacted)

Action Items:
  ☐ Send final notice to company-a (35 days to go)
  ☐ Escalate to company-b CTO
  ☐ Update internal service
  ☐ Check if personal projects still active
```

---

## Handling Late Migrations

Some users will migrate late. Plan for it:

### Option 1: Short grace period (7-30 days)
```
2026-07-15: Deprecation removed
2026-07-22: Last support date
2026-07-23: Hard error: "Feature removed, see migration guide"
```

### Option 2: Extended support (negotiated)
For major customers:
```
2026-07-15: Deprecation removed for most
2026-10-15: Extended deadline for Company X
2026-10-16: Hard error for Company X
```

### Option 3: Compatibility shim (short-term)
```
# Temporary shim that redirects old code to new
@app.route('/api/v1/users/<id>', methods=['GET'])
def v1_users(id):
    """Temporary shim for migrating users."""
    logging.warning(f"Deprecated v1 API called from {request.remote_addr}")
    return redirect(url_for('v2_users', id=id), code=301)
```

---

## Red Flags: When Deprecation Goes Wrong

⚠️ **Nobody knows about it**
- Solution: Better communication (blog, email, in-app notifications)

⚠️ **No clear migration path**
- Solution: Provide detailed guides and examples

⚠️ **Moving deadline**
- Solution: Commit to date, communicate early changes

⚠️ **Breaking changes after "deprecation"**
- Solution: Keep deprecated code working until removal date

⚠️ **Large sudden jump in errors**
- Solution: Gradual rollout, monitor metrics, extend deadline if needed

---

## Integration with Playbook

**Part of architecture and planning:**
- `/pb-plan` — Plan deprecations during scope phase
- `/pb-adr` — Document deprecation decisions (ADR-style)
- `/pb-guide` — Section 4.6 covers backwards compatibility
- `/pb-commit` — Mark deprecated code clearly in commits

**Related Commands:**
- `/pb-plan` — Feature planning (includes deprecation planning)
- `/pb-guide` — SDLC workflow
- `/pb-release` — Communication of deprecations in release notes

---

## Deprecation Checklist

Before marking something deprecated:

- [ ] Replacement exists (or plan to create it)
- [ ] Migration guide drafted
- [ ] Timeline decided (6+ months)
- [ ] Communication plan ready
- [ ] Code marked deprecated (warnings, docs)
- [ ] Tests updated to cover deprecated path
- [ ] Removal date documented everywhere

During deprecation period:

- [ ] Monitor usage metrics weekly
- [ ] Answer user questions promptly
- [ ] Track migration progress
- [ ] Send reminders at 1-month and 1-week marks
- [ ] Keep deprecated code working (don't break it)
- [ ] Document any extensions or special cases

At removal time:

- [ ] Remove deprecated code
- [ ] Update all documentation
- [ ] Add to migration guide
- [ ] Send final announcement
- [ ] Provide post-removal support

---

## Related Commands

- `/pb-adr` — Document deprecation decisions with rationale
- `/pb-release` — Communicate deprecations in release notes
- `/pb-documentation` — Write migration guides and deprecation notices

---

*Created: 2026-01-11 | Category: Planning | Tier: M/L*
