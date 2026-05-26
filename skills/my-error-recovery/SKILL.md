---
name: my-error-recovery
description: |
  **ALWAYS use when:** a tool fails, a command errors, a request times out, a file read returns nothing unexpected, or something goes wrong during execution. Use when the user says "it failed", "error", "something went wrong", "that didn't work", or when any tool call returns an error, stderr, or non-zero exit code. Also use when a skill produces unexpected output, a provider is unavailable, or the agent needs to pivot strategy after a failure.

  **DO NOT use for:** code review of error-prone code — use @skills/my-code-review. Preventing errors through planning — use @skills/my-project-lifecycle.
---

# Error Recovery

Graceful failure handling, retry patterns, and strategic pivots.

## ⚡ Quick Start

**Tool failed or command errored?**
→ 1. Read the error carefully — stderr often contains the real cause
→ 2. Classify: transient, permanent, or user-correctable?
→ 3. Apply the appropriate recovery pattern
→ 4. Never silently ignore errors

## Error Classification

| Type | Characteristics | Recovery |
|------|----------------|----------|
| **Transient** | Network timeout, rate limit, temporary unavailability | Retry with backoff |
| **Permanent** | Syntax error, missing file, wrong path, logic bug | Fix root cause |
| **User-correctable** | Missing dependency, wrong branch, need auth | Ask user with specific fix |
| **Agent-correctable** | Wrong tool used, wrong file path, wrong syntax | Fix and retry immediately |

## Recovery Patterns

### Pattern 1: Retry with Backoff (Transient)

For network timeouts, rate limits, temporary failures:

```
Attempt 1 → fails (timeout)
  → Wait 2s → Attempt 2
    → fails (timeout)
      → Wait 4s → Attempt 3
        → succeeds or escalate
```

Max 3 attempts. If still failing, classify as permanent.

### Pattern 2: Fix and Retry (Agent-Correctable)

For wrong paths, wrong tools, wrong syntax:

```
1. Read error message carefully
2. Identify what was wrong
3. Fix the approach
4. Retry immediately (no user ask)
```

Example: `read` failed because file doesn't exist → check path, maybe `find` first, then read correct path.

### Pattern 3: Escalate to User (User-Correctable)

For missing dependencies, auth issues, branch conflicts:

```
1. Explain what failed and why
2. Provide the exact command/fix needed
3. Ask user to apply it, then retry
```

Example: `npm install` fails because Node.js version mismatch → tell user exact version needed.

### Pattern 4: Pivot Strategy (Permanent / Ambiguous)

When the approach itself is wrong:

```
1. Acknowledge the failure
2. Propose 2-3 alternative approaches
3. Let user choose or ask for clarification
```

Example: `web_scrape` fails because site blocks bots → propose `web_extract`, `ctx_fetch_and_index`, or ask for URL alternative.

## HTTP-Specific Recovery

| Status | Meaning | Recovery |
|--------|---------|----------|
| 429 | Rate limited | Retry with exponential backoff |
| 503 | Service unavailable | Retry once, then report |
| 404 | Not found | Check URL, fix path |
| 401/403 | Auth denied | Escalate to user |
| 500+ | Server error | Retry once, then report |
| Timeout | No response | Retry with longer timeout |

## Tool-Specific Recovery

### Bash (command errors)
- Check stderr first — stdout may be empty but stderr has the cause
- Common: `command not found` → check if tool is installed
- Common: `permission denied` → check file permissions or use sudo
- Common: `No such file or directory` → verify path with `ls` or `find`

### Edit (file mutations)
- `oldText` must match exactly — whitespace matters
- If edit fails, re-read the file to get current exact content
- Never guess — always re-read before retrying edit

### Read (file access)
- File doesn't exist → `find` or `ls` to locate it
- Permission denied → check with `ls -la`
- Binary file → use ctx_execute_file instead

### Write (new files)
- Directory doesn't exist → `mkdir -p` first
- Overwriting existing → confirm with user unless explicitly told to overwrite

## Common Mistakes

❌ **Wrong:** Silently retrying the exact same failed command
✅ **Right:** Read error, fix root cause, then retry

❌ **Wrong:** Asking user "what should I do?" without diagnosing first
✅ **Right:** Diagnose, classify, then ask with specific options or fix

❌ **Wrong:** Treating a permanent error as transient and retrying 5 times
✅ **Right:** 3 retries max for transient, then escalate or pivot

❌ **Wrong:** Ignoring stderr and assuming command succeeded
✅ **Right:** Always check stderr, especially for bash commands

❌ **Wrong:** Giving up after first failure without attempting recovery
✅ **Right:** Every error is recoverable with the right classification

## Related Skills

- **@skills/my-workflow** — Session boundaries when errors require context switch
- **@skills/my-session-retrospective** — Log errors for skill improvement
- **@skills/my-project-lifecycle** — Plan phase error prevention

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.0
