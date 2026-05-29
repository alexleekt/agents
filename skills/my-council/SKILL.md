---
name: my-council
description: |
  **ALWAYS use when user mentions:** "review council", "multi-agent review",
  "parallel review", "team review", "full code review", "review with experts",
  "spawn reviewers", "council pattern", "review all dimensions", "code review",
  "review this", "PR review", "check my code", "critique", "how should I write this",
  "raise the bar".

  **ALWAYS use when:** a codebase has changed >5 files or ~100+ lines, or when
  the user wants a thorough review across multiple dimensions (security, performance,
  correctness, maintainability, tests, accessibility, architecture, types, research).

  **DO NOT use for:** single-file quick checks, asking how a specific function works,
  or debugging a known bug (use the appropriate debug skill instead).
---

# my-council

Multi-agent parallel review → Council synthesis → Prioritized fix list.

## ⚡ Quick Start

**When the user asks for a review or changes cross a threshold:**

```bash
# Check if review threshold is met
find src -type f -newer .git/HEAD -name '*.ts' -o -name '*.tsx' | wc -l
# If >5 files or ~100+ lines changed, trigger review council
```

**Activate the council:**
```
Spawning 5 parallel reviewers → synthesizing findings → presenting prioritized list
```

**After user picks fixes, execute all approved items immediately.**

## The Pattern

### 1. Spawn Parallel Reviewers

Spawn 5 (or more) subagents in parallel, each with a **different focus dimension**:

| Dimension | What to review |
|-----------|---------------|
| **Security** | XSS, injection, sanitization, CSP, secrets, input validation |
| **Architecture** | Component boundaries, state management, duplication, coupling |
| **Type Safety / API** | Type correctness, edge cases, null safety, API surface |
| **UX / Accessibility** | ARIA, keyboard nav, focus management, screen readers, contrast |
| **Tests / Coverage** | Missing tests, untested branches, dead code, test quality |
| **Research** | Best practices, modern alternatives, API docs, security advisories, patterns |

Each reviewer:
- Receives the same task description + file list
- Focuses only on their dimension
- Writes a structured report to `/tmp/review-{dimension}.md`

### 2. Synthesize Reports

After all agents complete:
1. Read all 5 report files
2. Categorize every finding into:
   - **Critical** — fix now (security, data loss, crash)
   - **Warning** — fix soon (bug risk, UX barrier, type hole)
   - **Suggestion** — consider (style, refactor, enhancement)
3. De-duplicate findings that appear in multiple dimensions
4. Present as numbered list with severity

### 3. Execute Fixes

User says "fix all" or picks a subset:
- **Do NOT ask for confirmation on each individual fix**
- **Do NOT ask "which one next?"** — just execute the list
- Fix in order: Critical → Warning → Suggestion
- Run tests after every batch of related edits
- Commit after all fixes pass

## Reviewer Prompt Template

Each reviewer receives this prompt structure:

```markdown
You are a {DIMENSION} reviewer for this project.

Your task: Review the following files and write a report to /tmp/review-{DIMENSION}.md.

Focus ONLY on {DIMENSION} concerns. Do NOT review other dimensions.

Review scope: {FILE_LIST}

Report format:
## Critical (fix now)
- [File:line] — Issue description
- Why: Impact + evidence
- Fix: Before/After code

## Warning (fix soon)
...

## Suggestion (consider)
...
```

## Research Dimension

The **Research** reviewer is unique — it does not read the code for bugs. Instead, it:

- Researches modern best practices for technologies used in the project
- Looks up API documentation for unfamiliar libraries or patterns
- Checks for known security advisories on dependencies
- Finds alternative approaches that might be simpler or more robust
- Validates that the project's approach aligns with current community standards

**Research reviewer prompt:**
```markdown
You are a Research reviewer for this project.

Your task: Research the technologies and patterns used in the following files.
Write a report to /tmp/review-research.md.

Use @skills/my-web-search-kagi to search the web for current best practices,
security advisories, and modern alternatives.

Focus ONLY on:
- Are we using the current best practices for each technology?
- Are there newer, simpler, or more robust alternatives?
- Are there any known security issues or deprecations in our dependencies?
- Are we missing common patterns that similar projects use?

Do NOT review code for bugs. Focus on external research and knowledge.

Research scope: {FILE_LIST} + package.json / Cargo.toml / pyproject.toml
```

## Orchestrator Prompt

After reviewers complete, read all reports and produce:

```markdown
## Code Review Council: {PROJECT_NAME}

### Critical (fix now)
1. **[File:line]** — Issue (from {reviewer})
2. ...

### Warning (fix soon)
1. ...

### Suggestion (consider)
1. ...

### Estimated effort: {X} hours
```

## Auto-Review Threshold

Do not wait for the user to ask. **Auto-invoke review** before commit when:

| Trigger | Condition |
|---------|-----------|
| **File count** | `edit`/`write` touched > 5 files |
| **Line count** | Total diff exceeds ~100 lines |
| **Risk surface** | Change touches security, auth, or error-handling paths |

If threshold is met:
1. Run `git diff --stat` (or equivalent) to confirm scope
2. **Invoke @skills/my-council** (self-call)
3. Fix **Critical** findings before committing
4. Note **Warnings** for follow-up
5. Commit with clean code

**Why auto-review:** Review is almost always user-initiated. Agents ship multi-file changes without review because there is no automatic trigger. This threshold removes the activation barrier.

## Execution Rules

- **Fix Critical first** — never leave a Critical finding unaddressed
- **Batch related edits** — fix all items in one file before moving to next
- **Run tests after each batch** — unit tests + typecheck + e2e
- **Commit as a single batch** — one commit per dimension batch, or one commit for all
- **Remove dead code immediately** — if reviewers flag unused code, delete it
- **Add missing tests** — if reviewers flag uncovered code, write tests

## Test Coverage Rule

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

## Build vs Buy Analysis

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

## Red Flags (always catch)

- [ ] Unvalidated user input → database
- [ ] Secrets hardcoded or unvalidated env
- [ ] Async without error handling
- [ ] Blocking operations in request handlers
- [ ] Race conditions in concurrent code
- [ ] Memory leaks in long-running processes
- [ ] Sensitive data in logs/errors
- [ ] **New code without tests (when project has tests)**

## Principles

| Principle | ❌ Wrong | ✅ Right |
|-----------|---------|----------|
| **Specific > Generic** | "Use better error handling" | "Use Result type pattern. Per Context7: [pattern]" |
| **Evidence > Opinion** | "I don't like this" | "React docs discourage this since v18. Use [alternative]" |
| **Actionable > Vague** | "Could be improved" | "Replace lines 45-52: [code]. Eliminates intermediate array" |

## Research Sources (priority order)

1. **Context7 library docs** — Most authoritative for specific libraries
2. **Official docs** — Framework/language best practices
3. **Codebase patterns** — grep for consistency with existing code
4. **Community guides** — With clear attribution

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

## Common Mistakes

❌ **Wrong:** Reviewing code without researching current best practices first
✅ **Right:** Always consult Context7 or official docs before making recommendations

❌ **Wrong:** Giving vague feedback like "this could be better"
✅ **Right:** Provide specific before/after code with evidence-backed reasoning

❌ **Wrong:** Catching style issues but missing security red flags
✅ **Right:** Check Red Flags first: input validation, secrets, async errors, race conditions

❌ **Wrong:** Suggesting a rewrite when a small fix suffices
✅ **Right:** Prefer minimal, targeted changes. Only refactor when clearly justified

❌ **Wrong:** Reviewing 50+ files as a single monolithic review
✅ **Right:** Use @skills/my-council to spawn parallel reviewers across dimensions

## When Context Is Unclear

Ask, don't guess:
- "What's intended behavior when [edge case]?"
- "Is this performance-sensitive?"
- "What versions are you targeting?"

Then deliver targeted recommendations.

## When to Skip

- Single file changed (< 20 lines)
- Only documentation or config changes
- Only test file changes
- User explicitly says "skip review"

## When to Use Research Standalone

Sometimes the user wants research without a full code review:
- "Should we use X or Y library?"
- "What's the current best practice for Z?"
- "Are there any security issues with our dependencies?"

In these cases, spawn **only the Research reviewer** and present findings directly. No council synthesis needed.

## Post-Review

After fixes are applied:
1. Run full test suite
2. Run typecheck
3. Run build
4. Verify coverage report
5. Commit with message: `review: fix {N} {dimension} findings`
6. Push

If the Research reviewer found actionable improvements (e.g., "use library X instead of Y"), create a follow-up task or implement immediately if the change is small.

## Related Skills

- **@skills/my-tech-stack** — For tool recommendations when reviewers suggest new dependencies
- **@skills/my-workflow** — For commit discipline and worktree naming during review execution
- **@skills/my-vcs-hygiene** — For committing and pushing after review fixes

## Versioning

- **Last updated:** 2026-05-28
- **Version:** 1.0
- **Update notes:** Initial council pattern based on multi-dimension parallel review experience
