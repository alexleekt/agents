---
name: my-context-strategy
description: |
  **ALWAYS use when:** processing large outputs (logs, diffs, build output, API responses), analyzing files over 50KB, running commands that produce more than 20 lines, or deciding which tool to use for data gathering. Use when the user says "analyze logs", "process this output", "check build output", "count lines", "find TODOs", or any task involving filtering, counting, aggregating, or transforming data. Also use when deciding between bash, read, ctx_execute, ctx_execute_file, or ctx_batch_execute for a task.

  **DO NOT use for:** editing files — use Edit/Write directly. Navigating directories — use Bash cd/ls. Short fixed-output observation — use Bash directly.
---

# Context Strategy

Tool selection discipline for context efficiency.

## ⚡ Quick Start

**Need to analyze, filter, count, or transform data?**
→ Use context-mode tools (ctx_execute, ctx_execute_file, ctx_batch_execute). Never read raw output into conversation.

**Need to observe a short, fixed output?**
→ Use Bash directly. Simple and correct.

**Need to edit a file?**
→ Use Read to get exact bytes, then Edit. Never ctx_execute for file mutations.

## The Hierarchy

```
1. OBSERVE short fixed output → Bash
2. PROCESS data (filter/count/parse) → ctx_execute / ctx_execute_file / ctx_batch_execute
3. INDEX documentation → ctx_index
4. SEARCH indexed content → ctx_search
5. EDIT a file → Read → Edit
6. NAVIGATE → Bash cd/ls/find
```

## Activation Condition

**This skill activates when deciding which tool to use for data gathering or processing.**

Apply these rules when:
- A command or file produces large or unpredictable output
- The task involves filtering, counting, aggregating, or transforming data
- Deciding between bash, read, ctx_execute, or ctx_batch_execute
- The user mentions logs, build output, diffs, or large files

Do **not** apply these rules when:
- Editing files directly → use Read/Edit
- Running a short command with known small output → use Bash

## Rules

### Rule 1: Process in Sandbox, Surface Summary Only

When output size cannot be predicted:
- **Use ctx_execute** — raw bytes stay in sandbox, only summary enters conversation
- **Never read raw output** — 700KB of log costs 700KB of reasoning capacity

Example:
```bash
# ❌ Wrong — reads 700KB into conversation
bash({ command: "npm test 2>&1" })

# ✅ Right — processes in sandbox, surfaces 3KB summary
ctx_execute({ language: "shell", code: "npm test 2>&1 | grep -E '(FAIL|✓|Error:|Tests +.*(failed|passed))' | head -60" })
```

### Rule 2: Prefer ctx_execute_file for File Analysis

When analyzing a single large file:
- **Use ctx_execute_file** — file bytes stay in sandbox, only derived answer enters conversation
- **Never read the whole file** unless you intend to edit it

Example:
```bash
# ❌ Wrong — reads entire file
read({ path: "huge.log" })

# ✅ Right — analyzes in sandbox
ctx_execute_file({ path: "huge.log", language: "javascript", code: "const errs = FILE_CONTENT.split('\\n').filter(l => /ERROR|FATAL/.test(l)); console.log(`${errs.length} error lines`); console.log(errs.slice(-5).join('\\n'))" })
```

### Rule 3: Batch Parallel Research with ctx_batch_execute

When running 3+ related commands:
- **Use ctx_batch_execute** — parallel execution, auto-indexed output, inline queries
- **Never run sequentially** — wastes round-trips

Example:
```bash
# ❌ Wrong — 3 sequential calls
bash({ command: "gh issue view 1" })
bash({ command: "gh issue view 2" })
bash({ command: "gh issue view 3" })

# ✅ Right — one call, parallel execution, indexed output
ctx_batch_execute({ commands: [{label: "issue 1", command: "gh issue view 1"}, {label: "issue 2", command: "gh issue view 2"}, {label: "issue 3", command: "gh issue view 3"}], queries: ["root cause", "proposed fix"], concurrency: 3 })
```

### Rule 4: Index Documentation, Don't Inline It

When encountering documentation, API references, or large guides:
- **Use ctx_index** — stores in searchable knowledge base
- **Never paste large docs** into conversation

Example:
```bash
# ❌ Wrong — 50KB of docs enters conversation
read({ path: "docs/api.md" })

# ✅ Right — indexed, searchable later
ctx_index({ path: "docs/api.md", source: "project-api-docs" })
```

### Rule 5: Bash for Simple Observation

When the output is short, fixed, and you intend to consume it verbatim:
- **Use Bash** — simpler, no sandbox overhead

Example:
```bash
# ✅ Right — short fixed output
bash({ command: "git status --short" })
bash({ command: "pwd" })
bash({ command: "whoami" })
```

### Rule 6: Read for Editing

When you intend to edit a file:
- **Use Read** — exact bytes must match for Edit tool
- **Never ctx_execute** for file mutations — sandbox FS is discarded

Example:
```bash
# ✅ Right — need exact bytes for Edit
read({ path: "src/index.ts" })

# ❌ Wrong — sandbox changes don't persist
ctx_execute({ language: "javascript", code: "fs.writeFileSync('src/index.ts', 'new content')" })
```

## The Processing Reflex

Before calling `bash` for ANY non-mutating command, ask:
> **"Do I need the raw output, or only a derived result?"**

| Intent | Correct Tool |
|--------|-------------|
| Need raw output for editing | Read / Bash |
| Need derived result (count, filter, parse, aggregate) | **ctx_execute / ctx_execute_file / ctx_batch_execute** |

**Hard rule:** If you intend to `bash` a command and then `read` or `grep` its output, you **must** use `ctx_execute` instead.

## Post-Hoc Migration Rule

If a `bash` command returns **>20 lines** or the output is unpredictable:
1. **Do NOT read** the raw output with `read`
2. **Re-run** the analysis using `ctx_execute` or `ctx_batch_execute`
3. **Surface only** the derived summary (counts, filtered lines, aggregates)

This rule **overrides** the general "Bash for simple observation" hierarchy when output size exceeds the threshold.

## Trigger Phrases

| User Says | Correct Tool |
|-----------|-------------|
| "analyze logs" | ctx_execute |
| "check build output" | ctx_execute |
| "count lines" | ctx_execute |
| "find TODOs" | ctx_execute |
| "process this output" | ctx_execute |
| "large file analysis" | ctx_execute_file |
| "run tests" | ctx_execute |
| "list containers" | ctx_execute |
| "git log" | ctx_execute |
| "diff between branches" | ctx_execute |
| "fetch docs" | ctx_fetch_and_index |
| "API reference" | ctx_index |
| "short output, read it" | Bash |
| "edit this file" | Read → Edit |
| "cd into X" | Bash |

## Common Mistakes

❌ **Wrong:** Reading a 700KB log file with `read`
✅ **Right:** Using `ctx_execute_file` to filter/count in sandbox

❌ **Wrong:** Running 5 sequential research commands
✅ **Right:** Using `ctx_batch_execute` with concurrency

❌ **Wrong:** Pasting 50KB of documentation into conversation
✅ **Right:** Using `ctx_index` for searchable storage

❌ **Wrong:** Using `ctx_execute` to mutate files
✅ **Right:** Using `Edit` or `Write` for file mutations

❌ **Wrong:** Using `ctx_execute` for `git status` on a clean tree
✅ **Right:** Using `bash` for short fixed observation

❌ **Wrong:** Using `bash` to grep a log, then `read` the grep output
✅ **Right:** Using `ctx_execute` — one call, processed in sandbox

❌ **Wrong:** Processing 10,000 lines through bash into conversation memory
✅ **Right:** Using `ctx_execute` to derive counts/filters, surfacing only the summary

## Related Skills

- **@skills/my-workflow** — Session boundaries and parallel agent coordination
- **@skills/my-session-retrospective** — Assess whether context-mode was used correctly

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.1
- **Update notes:** Added Processing Reflex (pre-flight gate before any bash call) and Post-Hoc Migration Rule (bash >20 lines → re-run via ctx_execute). These address the 71% bash-misuse pattern found in retrospective analysis of 697 sessions.
