---
name: my-code-review
description: |
  **ALWAYS use when user mentions:** "code review", "review this", "PR review",
  "check my code", "critique", "how should I write this", "raise the bar".

  Elevates code. Researches modern best practices FIRST, then delivers
  specific, actionable recommendations. No generic advice—only evidence-backed
  improvements that raise the bar.

  **DO NOT use for:** debugging specific bugs (use debug skills), explaining
  how code works (use docs), or general coding questions without review intent.
---

# my-code-review

Research. Analyze. Elevate.

## ⚡ Quick Start

**Before reviewing any code:**

1. **Check for project tests** — `find . -name '*.test.*' -o -name '*.spec.*' | head -5`
2. **Identify tech stack** — Check package.json, Cargo.toml, pyproject.toml
3. **Research patterns** — Use `context7_get_library_docs` for unfamiliar libraries
4. **Follow the workflow:**
   ```
   RESEARCH → ANALYZE → ELEVATE
   ```

**Output format:**
```markdown
## Critical (fix now)
**[Issue]** — Clear description
- **Why**: Impact + evidence
- **Fix**: Before/After code blocks

## Warning (fix soon)
...

## Suggestion (consider)
...
```

## Prerequisites

- Project context (language, framework, key libraries)
- Access to authoritative docs (via context7)
- Understanding of existing codebase patterns

## Workflow

```
RESEARCH → ANALYZE → ELEVATE
```

### 1. Research (MANDATORY)

Before any recommendation:

1. **Identify domain** — language, framework, key libraries
2. **Pull authoritative docs** — `context7_get_library_docs` for library-specific patterns
3. **Check the codebase** — grep for how this project handles similar patterns

**Never skip.** Generic advice is worthless. Evidence-backed recommendations only.

### 2. Analyze

| Area | What to look for |
|------|------------------|
| **Security** | Injection, XSS, secrets in code/env, unsafe eval |
| **Performance** | Blocking ops in async contexts, N+1 queries, memory leaks |
| **Correctness** | Race conditions, error handling gaps, edge cases |
| **Maintainability** | Complexity, unclear naming, missing types/docs |
| **Idioms** | Outdated patterns, anti-patterns for the ecosystem |
| **Tests** | Coverage for new code, updated tests for changed behavior |
| **Build vs Buy** | Reinventing wheels that mature libraries solve |

#### Build vs Buy Analysis

**Question**: Is this code reinventing something a mature library already solves?

**When to flag**:
- Common utility functions (date formatting, validation, HTTP retries)
- Security-sensitive operations (auth, crypto, parsing untrusted input)
- Complex state management with async operations
- Features with known edge cases (timezones, unicode, floating point)
- Data transformation with schema requirements

**Evaluation criteria**:
| Factor | Build | Buy |
|--------|-------|-----|
| **Complexity** | Simple, domain-specific | General, edge-case-heavy |
| **Security** | Non-critical | Auth, crypto, parsing |
| **Maintenance** | Core to business | Commodity feature |
| **Team expertise** | Deep knowledge | Learning curve acceptable |
| **Ecosystem** | Poor library options | Mature, well-maintained |

**Output when flagged**:
```markdown
### Consider library for [feature] (Suggestion)
**Current**: Hand-rolled [X] implementation (lines 34-78)

**Alternative**: [Library name] — [specific benefit]

**Why**: Mature, well-tested, handles [edge cases you missed].
Your implementation missing: [specific gap].

**Decision**: Keep custom if [specific reason], else migrate.
```

#### Test Coverage Rule

**If the project has tests → new code MUST have tests.**

Check first: `find . -name '*.test.*' -o -name '*.spec.*' -o -name 'test_*' | head -5`

| Situation | Requirement |
|-----------|-------------|
| Project has tests + new feature | Add tests covering happy path + edge cases |
| Project has tests + bug fix | Add regression test that would have caught the bug |
| Project has tests + refactored code | Ensure existing tests still pass; update if behavior changed |
| No test framework in project | Note: "Consider adding tests—project has none" |

**Coverage goal**: Meaningful coverage without bloat.
- Test the contract: inputs → outputs, success + failure paths
- Test edge cases: empty, null, extreme values, race conditions
- Don't test: language built-ins, trivial getters, implementation details
- One comprehensive test > three shallow tests

### 3. Elevate

Structure findings:

```markdown
## Summary
Brief: what's strong, what needs work, severity (Critical/Warning/Suggestion)

## Critical (fix now)
**[Issue]** — Clear description
- **Why**: Impact + evidence from docs
- **Fix**: Before/After code blocks
- **Source**: Context7 link or official docs

## Warning (fix soon)
[Same structure]

## Suggestion (consider)
[Same structure]

## What's Working
Specific praise. Trust comes from honesty.

## Consulted
- [source 1]
- [source 2]
```

## Principles

### Specific > Generic
❌ "Use better error handling"
✅ "Use Result type pattern. Per Context7: [pattern]. Type-safe propagation without try/catch."

### Evidence > Opinion
❌ "I don't like this"
✅ "React docs discourage this pattern since v18 (breaks concurrent rendering). Use [alternative]."

### Actionable > Vague
❌ "Could be improved"
✅ "Replace lines 45-52 with: [code]. Eliminates intermediate array, 40% fewer allocations."

## Fix Format

```markdown
### Before (lines X-Y)
```ts
// problematic
```

### After
```ts
// fixed
```

### Why
- [specific benefit]
- [evidence-backed reasoning]
```

## Severity

- **Critical**: Security risk, data loss, broken functionality
- **Warning**: Performance hit, tech debt, maintainability issue
- **Suggestion**: Style, alternative pattern, future consideration

## Research Sources (priority order)

1. **Context7 library docs** — Most authoritative for specific libraries
2. **Official docs** — Framework/language best practices
3. **Codebase patterns** — grep for consistency with existing code
4. **Community guides** — With clear attribution

## Multi-File Reviews

For reviews spanning many files, use `@skills/my-team-orchestrate` to:
- Spawn parallel review agents for different modules
- Coordinate findings across the codebase
- Apply "Till Done" pattern for iterative review cycles

Example: "Review this entire codebase" → Use team orchestration with checker/fix loops.

## Red Flags (always catch)

- [ ] Unvalidated user input → database
- [ ] Secrets hardcoded or unvalidated env
- [ ] Async without error handling
- [ ] Blocking operations in request handlers
- [ ] Race conditions in concurrent code
- [ ] Memory leaks in long-running processes
- [ ] Sensitive data in logs/errors
- [ ] **New code without tests (when project has tests)**

## Troubleshooting

**Review feels overwhelming?**
→ Use `@skills/my-team-orchestrate` to divide large reviews into focused checks

**Can't find authoritative docs?**
→ Check similar code in the codebase (consistency > perfection)

**Unclear if issue is critical?**
→ Ask: "Does this affect security, data loss, or core functionality?"
→ If yes: Critical. If no: Warning or Suggestion.

**Build vs Buy decision unclear?**
→ Default to "buy" for: auth, crypto, date math, parsing
→ Default to "build" for: domain-specific logic

## When Context Is Unclear

Ask, don't guess:
- "What's intended behavior when [edge case]?"
- "Is this performance-sensitive?"
- "What versions are you targeting?"

Then deliver targeted recommendations.

## Example: Critical Finding

```markdown
### JWT secret without validation (Critical)
**Lines 12-15**

**Before**
```ts
const secret = process.env.JWT_SECRET;
```

**After**
```ts
const secret = process.env.JWT_SECRET;
if (!secret) throw new Error('JWT_SECRET required');
// Or use env validation library for schema enforcement
```

**Why**: Falls back to "undefined" string in dev. Creates predictable signing key. 
**Source**: [Context7: jsonwebtoken security practices]
```

## Example: Missing Test Coverage (Warning)

```markdown
### New feature lacks tests (Warning)
**Feature**: `validateUser()` in `auth.ts` (lines 45-72)

**Issue**: Project has `*.test.ts` files but no tests for this new function.

**Required tests**:
```ts
describe('validateUser', () => {
  it('returns user for valid credentials', async () => {
    // happy path
  });
  
  it('throws AuthError for invalid password', async () => {
    // failure case
  });
  
  it('throws NotFoundError for missing user', async () => {
    // edge case
  });
});
```

**Why**: Function has 3 branches (success, invalid password, missing user). 
Current test suite covers similar auth functions. Consistency + regression protection.
```

## Example: Build vs Buy (Suggestion)

```markdown
### Consider library for date formatting (Suggestion)
**Current**: Custom `formatDate()` in `utils.ts` (lines 12-34)

**Implementation**: 22 lines handling 3 formats, no timezone support.

**Alternative**: [Mature date library] — widely used, actively maintained.

**Why**: Your implementation missing:
- Timezone handling (bug reports incoming)
- Locale-aware formatting (i18n requirement)
- Edge cases (DST transitions, leap seconds)

**Migration**:
```ts
// Before
function formatDate(d: Date, fmt: string) { /* 22 lines */ }

// After  
import { formatDate } from '[library]';
const formatted = formatDate(date, 'yyyy-MM-dd HH:mm', { timezone: 'Europe/Berlin' });
```

**Decision**: Worth small dependency to eliminate maintenance burden + get correctness.
```

## Post-Review

Note for yourself:
- Patterns that keep coming up
- Best sources for [domain]
- What would speed up next review

Continuous improvement in practice.
