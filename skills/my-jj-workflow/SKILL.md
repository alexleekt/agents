---
name: my-jj-workflow
description: |
  **ALWAYS use when user mentions:** "jj", "jujutsu", OR implies VCS without naming
  a tool ("commit", "status", "diff", "push") when user hasn't specified git.

  **Assumption:** "commit" without "git" prefix means jj, NOT git.

  **DO NOT use for:** releases/semver (@skills/my-semantic-release) or when user
  explicitly prefers git.

  **For all jj commands, see @skills/jujutsu**
---

# My JJ Workflow

**Agent-optimized guide for jujutsu (jj).** For full command reference, see **@skills/jujutsu**.

---

## ⚡ Agent Quick Start

**Before any jj operation, verify:**
1. ✅ This is a jj repo (`ls .jj` or `jj st` succeeds)
2. ✅ **CRITICAL: Always use `-m` flag for commits** (never rely on editor in non-interactive mode)
3. ✅ Never use `jj split` (use patterns below)
4. ✅ After `jj commit`, run `jj new` to continue
5. ✅ Use `jj edit`, not `git checkout`

**⚠️ NON-INTERACTIVE SAFETY:** In scripts/agents, `jj commit` without `-m` will abort or hang. Always use:
   - `jj commit -m "message"`
   - `jj describe -m "message"`
   - `jj new -m "message"`

**If stuck:** `EDITOR=cat timeout 10 jj <command>` (recovery only)

---

## Prerequisites

- **jj** — Jujutsu VCS (install: `cargo install jj` or package manager)
- **git** — For push/pull to GitHub/GitLab (jj uses git as backend)
- **Shell** — Any POSIX-compatible shell (bash, zsh, fish)
- **Optional: just** — For pre-commit check examples

## Decision Guide: User Says → You Do

| User says | Your exact steps |
|-----------|------------------|
| **"commit this"** | 1. `jj st` → 2. If no description: `jj describe -m "..."` → 3. `jj commit -m "..."` (⚠️ `-m` required!) → 4. `jj new -m "wip: next"` |
| **"what changed?"** | `jj st` then `jj diff` |
| **"check status"** | `jj st` |
| **"split this" / "break into commits"** | 1. `jj diff --summary` → 2. `ask_user` how to split → 3. Use [Split Workflow](#split-workflow) below |
| **"new branch" / "create branch"** | Explain: "jj uses changes, not branches. Use: `jj new main -m \"feat: ...\"`" |
| **"checkout X"** | `jj edit X` (X = bookmark name, change ID, or `@--`) |
| **"go back" / "undo"** | `jj undo` (undoes last jj operation) |
| **"push to github"** | `git push` or `jj git push --bookmark main` |
| **"pull from github"** | `jj git fetch` then `jj rebase -d main@origin` |
| **"worktree" / "new worktree"** | Explain: "jj uses workspaces: `jj workspace add ../ws`" |
| **"squash/fixup"** | `jj squash -m "final message"` (into parent) or `jj squash --from @ --into X -m "..."` |
| **"amend last commit"** | `jj edit @-` → make edits → `jj squash` OR `jj describe -m "new message"` if just changing message |
| **"see history"** | `jj log --limit 10` |
| **"diff against main"** | `jj diff --from main --to @` |

---

## Standard Workflows (Step-by-Step)

### Workflow 1: Normal Commit

```bash
# Step 1: Check current state
jj st

# Step 2: Run pre-commit checks (if project has them)
just check 2>/dev/null || npm test 2>/dev/null || echo "No checks configured"
# Fix any issues before committing!

# Step 3: If changes exist but no description, describe them
jj describe -m "feat(scope): what this does"

# Step 4: Commit
jj commit -m "feat(scope): what this does"

# Step 5: CRITICAL - Create new change for next work
jj new -m "wip: next task"
# (Or just `jj new` if you want to describe later)
```

### Workflow 2: Describe-First (Preferred)

Start with intent, evolve message, commit when ready:

```bash
# Start with intent
jj new main -m "wip: auth flow"

# Make edits...

# Refine description as work progresses  
jj describe -m "feat(auth): JWT authentication"

# Make more edits...

# Final description
jj describe -m "feat(auth): add JWT authentication with refresh tokens"

# Now commit
jj commit -m "feat(auth): add JWT authentication with refresh tokens"

# Continue with new change
jj new -m "wip: next task"
```

### Workflow 3: Fixup Previous Commit

```bash
# Option A: Quick message change (not yet pushed)
jj edit @-                    # Go to parent commit
jj describe -m "new message"  # Update message
jj edit @+                    # Return to current work

# Option B: Add more changes to previous commit
jj edit @-                    # Go to parent
# ...make edits...
jj squash -m "updated message" # Squash working copy into parent
jj edit @+                    # Return to current work
```

### Workflow 4: Split Workflow

**NEVER use `jj split`** — it's interactive only. Use this instead:

```bash
# Step 1: See what files we have
jj diff --summary
# Output:
# M src/auth.js
# M src/login.js  
# M README.md

# Step 2: Decide split strategy (use ask_user if unclear)
# Strategy A: Code vs Docs
# Strategy B: File by file

# --- Strategy A: Code vs Docs ---

# Create new change for docs (current change keeps code)
jj new @- -m "docs: update readme"
# (Now @ has docs, @- has code)

# Commit the code first
jj edit @-
jj commit -m "feat: add authentication"

# Now commit the docs
jj edit @+
jj commit -m "docs: document authentication"

# --- Strategy B: File by File ---

# Abandon mixed change, create clean ones
change_id=$(jj log -r @ -T 'change_id')

# Create first commit
jj new @- -m "feat(auth): add auth endpoints"
# Ensure only auth.js is present

# Create second commit  
jj new @-- -m "feat(login): add login page"
# Ensure only login.js is present

# Abandon original mixed change
jj abandon $change_id

# Result: Two clean commits instead of one mixed
```

### Workflow 5: Context Switch

```bash
# Current work is WIP, need to do something else

# Option 1: Describe and leave
jj describe -m "wip: feature X on hold"
jj new main -m "feat: urgent fix"

# Option 2: Bookmark for later, start fresh
jj bookmark create feature-x -r @
jj new main -m "feat: urgent fix"

# Come back later
jj edit feature-x
```

### Workflow 6: Workspace with Sparse Checkout

```bash
# Create minimal workspace for focused work
jj workspace add --sparse-patterns empty ../feature-ws
cd ../feature-ws

# Add only what you need
jj sparse set --add src/auth/ --add README.md

# Work only with those files present
# ...

# When done, clean up
jj workspace forget ../feature-ws
```

### Workflow 7: Pre-Push Verification

**ALWAYS run this before pushing to CI/CD or releasing:**

```bash
# Step 1: Check for any uncommitted changes
jj st

# Step 2: Run full check suite (project-specific)
just check 2>/dev/null || npm test 2>/dev/null || cargo test 2>/dev/null

# Common checks that must pass:
# ✅ Biome/Prettier formatting (no "would have printed" errors)
# ✅ Linting (no warnings/errors)
# ✅ Tests (all pass)
# ✅ TypeScript typecheck (no errors)

# Step 3: If any checks fail, fix before pushing
just fix 2>/dev/null || npx @biomejs/biome check --write .
jj commit -m "style: fix formatting"

# Step 4: Now safe to push/release
just release  # or: git push, jj git push, etc.
```

**Why this matters:** CI failures after tagging require force-pushing the tag, which is messy and risks race conditions with npm registry.

---

## Error Recovery

### Problem: Editor Opened (Forgot `-m` Flag)

```
WHAT HAPPENED: You ran `jj commit` without `-m`, editor opened

RECOVERY:
1. Cancel editor immediately:
   - Vim: Press Escape, type `:q!`, press Enter
   - Nano: Press Ctrl+X

2. Re-run with `-m` flag:
   jj commit -m "feat: actual message"

PREVENTION: Always use `-m` flag. Never rely on editor.
```

### Problem: Command Stuck/Hanging

```
WHAT HAPPENED: Command waiting for input (forgot `-m` or interactive prompt)

RECOVERY:
1. Force non-interactive completion:
   EDITOR=cat timeout 10 jj <command>

2. Or kill and retry:
   Ctrl+C or kill -9 <pid>
   Then retry with `-m` flag

WARNING: EDITOR=cat creates empty messages. Fix immediately with:
   jj describe -m "proper message"  # if not committed
   # or edit @- and squash if already committed
```

### Problem: `jj commit` Aborts in Non-Interactive Mode

```
WHAT HAPPENED: Ran `jj commit` without `-m` flag in non-interactive mode

SYMPTOM: Command aborts with "Command aborted" or hangs indefinitely

RECOVERY:
1. Check if commit actually happened:
   jj log --limit 3

2. If not committed, retry with `-m` flag:
   jj commit -m "feat: actual message"

3. If partially committed (change ID changed), check status:
   jj st

PREVENTION: ALWAYS use `-m` flag in scripts/automation:
   ✅ jj commit -m "feat: x"
   ✅ jj commit --message "feat: x"
   ❌ jj commit  # Never use without -m in non-interactive mode
```

### Problem: "No .jj Directory Found"

```
CAUSE: Not a jj repo yet

SOLUTION:
1. If git repo exists: Run `jj git init --colocate` to set up jj alongside git

2. If new project: jj git init
```

### Problem: "Nothing Changed" After Commit

```
THIS IS NORMAL. After `jj commit`:
- Your changes were saved to the commit
- Working copy is now "empty" (no files, no description)

NEXT STEP: Always run `jj new` to continue working:
   jj new -m "wip: next task"
```

### Problem: Accidentally Used Git Commands

```
DANGER: git commit, git rebase, git merge, git cherry-pick, git reset --hard
CORRUPT jj history in colocated repos.

IF YOU JUST DID IT (< 1 minute):
   jj undo                    # May recover

IF PUSHED/PERSISTED:
   jj op log                  # See operation history
   jj op restore <op-id>      # Restore from before git command
   # Or manually recreate changes

SAFE git commands (read-only):
   git log, git diff, git show, git blame, git grep
```

---

## Essential Reference

### Revset Symbols (Navigation)

| Symbol | Means | Use in |
|--------|-------|--------|
| `@` | Current working copy | `jj diff -r @` |
| `@-` | Parent of current | `jj edit @-` |
| `@--` | Grandparent | `jj log -r @--` |
| `@+` | Child of current | `jj edit @+` |
| `main` | Bookmark (like branch) | `jj new main` |
| `abc123` | Change ID | `jj edit abc123` |

**⚠️ Git syntax that breaks in jj:**
- ❌ `@~1` → ✅ `@-`
- ❌ `@^` → ✅ `@-`  
- ❌ `@~-1` → ✅ `@+`

### Common Commands

| Task | Command |
|------|---------|
| Status | `jj st` |
| Diff | `jj diff` |
| Log | `jj log --limit 20` |
| New change | `jj new main -m "feat: x"` |
| Describe | `jj describe -m "feat: x"` |
| Commit | `jj commit -m "feat: x"` |
| Squash | `jj squash -m "final"` |
| Edit change | `jj edit @-` or `jj edit <id>` |
| Undo | `jj undo` |

### Timeout Wrapper (For Automation)

```bash
jj_with_retry() {
  local cmd="$1"
  local max_retries=3
  local timeout_sec=10
  local delay=2
  
  for ((attempt=1; attempt<=max_retries; attempt++)); do
    echo "Attempt $attempt/$max_retries: $cmd"
    if timeout $timeout_sec bash -c "$cmd"; then
      return 0
    fi
    echo "  → Retrying in ${delay}s..."
    sleep $delay
    delay=$((delay * 2))
  done
  return 1
}

# Usage: jj_with_retry "jj commit -m 'feat: x'"
```

### Sparse Patterns

```bash
# See current:    jj sparse list
# Add paths:      jj sparse set --add src/
# Remove paths:   jj sparse set --remove tests/
# Reset to full:  jj sparse reset
```

### Git Interop

| Situation | Tool |
|-----------|------|
| Daily work | jj |
| Push to GitHub | git push or jj git push |
| Clone | git clone → then `jj git init --colocate` |
| Submodules | git (jj limited) |
| Complex split | git (jj split is interactive) |

**CRITICAL:** Never use `git commit`, `git rebase`, `git merge` in colocated jj repos.

---

📚 **Full command reference:** @skills/jujutsu
