---
name: my-jj-workflow
description: |
  **ALWAYS use when user mentions:** "jj", "jujutsu", OR user implies VCS without naming
  a specific tool ("commit", "what changed", "check status", "push to github", "worktree",
  "branch", "merge", "rebase", "diff", "stash", "pull") when the user hasn't specified
  a different VCS tool.

  **Assumption:** When user says "commit" without specifying "git commit", they want
  jj workflow, NOT git.

  **DO NOT use for:** semantic versioning, changelog generation, release workflows,
  OR when user explicitly mentions "git" as their preferred tool —
  use @skills/my-semantic-release for those.

  **For all jj commands, see @skills/jujutsu**
---

# My JJ Workflow

Personal workflow patterns for jujutsu (jj). For full command reference, see **@skills/jujutsu**.

---

## Core Philosophy

| Principle | What it means |
|-----------|---------------|
| **jj-first** | Use jj for all local operations |
| **Auto-colocation** | First `jj` command in a git repo auto-runs `jj git init --colocate` |
| **Describe-first** | Write messages with `jj describe -m` before committing |
| **git for push** | Push via git (jj colocation makes this seamless) |

---

## Quick Decision Guide

**When user says... → Do this:**

| User says | Your action |
|-----------|-------------|
| "commit this" | `jj st` → `jj describe -m "..."` or `jj commit -m "..."` |
| "what changed?" | `jj st` + `jj diff` |
| "split this" | `jj diff --summary` → `ask_user` for strategy → use [split patterns](#pattern-1-split-by-file-automated) |
| "new branch" | Explain jj doesn't use branches; use `jj new main -m "feat: ..."` |
| "checkout X" | `jj edit X` (X = bookmark, change_id, or revset like `@--`) |
| "undo" | `jj undo` (undoes last jj operation) |
| "push to github" | `git push` or `jj git push` |
| "worktree" | Explain jj uses **workspaces**: `jj workspace add ../ws` |

---

## Quick Reference (Non-Interactive)

**Always use `-m` flag to skip editors in agent workflows:**

| Task | Command |
|------|---------|
| Check status | `jj st` |
| Create change | `jj new main -m "feat: start work"` |
| Update message | `jj describe -m "feat: updated message"` |
| Commit change | `jj commit -m "feat: complete"` |
| Squash to parent | `jj squash -m "final message"` |
| Cross-commit squash | `jj squash --from <src> --into <dst> -m "msg"` |
| Show log | `jj log --limit 20` |
| Show diff | `jj diff` |

**❌ Interactive (avoid in agents):** `jj split`, `jj describe` (without `-m`), `jj commit` (without `-m`)

**⚠️ Nuclear option:** `EDITOR=cat jj <command>` forces non-interactive mode

---

## Essential Revset Navigation

jj uses revsets (revision sets) to navigate. Learn these first:

| Symbol | Meaning | Example use |
|--------|---------|-------------|
| `@` | Current working copy | `jj diff -r @` |
| `@-` | Parent of current | `jj edit @-` |
| `@--` | Grandparent | `jj log -r @--` |
| `@+` | Child of current | `jj log -r @+` |
| `main` | Bookmark (like branch) | `jj new main` |
| `abc123` | Change ID prefix | `jj edit abc123` |

**⚠️ Common mistakes:**
- ❌ `@~1` (git syntax) → ✅ `@-` (jj syntax)
- ❌ `@^` (git syntax) → ✅ `@-` (jj syntax)
- ❌ `git checkout` → ✅ `jj edit`
- ❌ `git branch` → ✅ `jj bookmark create`

---

## Daily Workflows

### Describe-First Workflow

Don't commit immediately — describe your intent first, commit when ready:

```bash
jj new main
# ... make edits ...
jj describe -m "wip: auth flow"
# ... more edits ...
jj describe -m "feat: JWT authentication"
jj commit -m "feat: JWT authentication"  # Now commit
```

**After committing, start fresh:**

```bash
# After jj commit, the working copy is now "empty" (no description set)
# Create a new change to continue working:
jj new -m "wip: next task"

# The previous commit is now your parent (@-)
# Future changes can be squashed into it if needed
```

**Key pattern:** `jj commit` → `jj new` → work → `jj commit` creates a linear chain. If you need to fixup the previous commit, use `jj edit @-` then `jj squash`.

### Context Switching (JJ's Superpower)

Multiple in-progress changes without branches:

```bash
jj edit @--           # Go back one change
jj edit feature-x     # Jump to bookmark
jj new main           # Start fresh work
jj log                # See your change stack
```

### Organizing Changes

**Squash fixups into parent:**
```bash
jj squash -m "final message"

# Cross-commit squash
jj squash --from <src> --into <dst> -m "message"
```

**Split mixed concerns:** See [Agent-Specific Patterns](#handling-split-and-interactive-commands) below for non-interactive alternatives to `jj split`.

---

## Workspaces & Sparse Checkouts

jj uses "workspaces" — separate working directories linked to the same repo:

```bash
# Create a new workspace
jj workspace add ../feature-ws
cd ../feature-ws

# Remove when done
jj workspace forget ../feature-ws
```

### Sparse Patterns (Checkout Only What You Need)

Sparse patterns control which files exist in each workspace's working copy:

**Create sparse workspaces:**
```bash
# Empty workspace, add manually
jj workspace add ../frontend-ws --sparse-patterns empty
cd ../frontend-ws
jj sparse set --add frontend/ --add README.md

# Full checkout (default inherits parent's sparsity)
jj workspace add ../full-ws --sparse-patterns full
```

**Manage sparse patterns:**
```bash
jj sparse list                    # See current patterns
jj sparse set --add src/          # Add paths to working copy
jj sparse set --remove tests/     # Remove paths (deletes from workspace, not repo)
jj sparse reset                   # Reset to full checkout
```

**Sparse vs .gitignore:**

| | `.gitignore` | `jj sparse` |
|---|---|---|
| **Purpose** | Prevents VCS tracking | Controls checkout presence |
| **Scope** | All workspaces globally | Per-workspace only |
| **Effect** | Files ignored from status | Files missing from disk |
| **Use for** | Build artifacts, secrets, deps | Large repos, focused work |

---

## Agent-Specific Patterns

### Handling Split and Interactive Commands

`jj split` is inherently interactive and cannot run non-interactively. **Never attempt `jj split` in agent workflows.**

#### Decision Tree: User Asks to "Split" a Change

```
User says: "Split this commit"
    │
    ├─→ Step 1: Check what's in the change
    │   $ jj diff --summary
    │   M src/auth.js
    │   M src/login.js
    │   M README.md
    │
    ├─→ Step 2: Ask user for split strategy
    │   "This change has 3 files. Split by:
    │    1. File (each file separate)
    │    2. Type (code vs docs)
    │    3. Manual (you specify)"
    │
    └─→ Step 3: Execute without `jj split`
```

#### Pattern 1: Split by File (Automated)

When user wants each file as separate commit:

```bash
# Current change has: src/auth.js, src/login.js, README.md

# Extract first file to new commit
jj new @- -m "feat(auth): add authentication"
cp src/auth.js /tmp/  # save temporarily
jj restore --from @- src/auth.js  # restore to this change
# ...copy file back, stage, commit...

# Actually easier: describe original partially, then new
jj describe -m "feat(auth): add authentication"  # for auth.js
jj commit -m "feat(auth): add authentication"
jj new -m "feat(login): add login page"  # remaining files get new change
```

**Simpler approach:** Create fresh changes from parent:

```bash
# Abandon current mixed change
change_id=$(jj log -r @ -T 'change_id')

# Create clean change for first file
jj new @- -m "feat(auth): add authentication"
# Manually ensure only auth.js is in working copy

# Create clean change for second file
jj new @-- -m "feat(login): add login"
# Manually ensure only login.js

# Abandon original
jj abandon $change_id
```

#### Pattern 2: Split by Concern (Most Common)

User wants "code changes" separate from "docs":

```bash
# Step 1: Show what's in the change
$ jj diff --summary
M src/auth.js      # code
M src/login.js     # code  
M README.md        # docs
M CHANGELOG.md     # docs

# Step 2: Create new change for docs
jj new @- -m "docs: update readme and changelog"
# Working copy now at new change, parent has code files

# Step 3: Go back and commit code
jj edit @-
jj commit -m "feat: add authentication system"

# Step 4: Go to docs change and commit
jj edit @+
jj commit -m "docs: document authentication"
```

#### Pattern 3: Prevent Need for Split (Best Practice)

Instead of splitting later, use **describe-first** to create focused changes:

```bash
# ❌ Don't: One big change then split later
jj new main
# edit auth.js, login.js, README.md
# now need to split...

# ✅ Do: Separate changes from start
jj new main -m "wip: auth endpoints"
# edit auth.js
jj describe -m "feat(api): add auth endpoints"

jj new @ -m "wip: login ui"
# edit login.js
jj describe -m "feat(ui): add login form"

jj new @ -m "wip: docs"
# edit README.md
jj describe -m "docs: add auth documentation"
```

#### Pattern 4: Emergency Git Fallback

If you must do complex split operations:

```bash
# In colocated repo only
jj st  # note the change_id

# Use git to split (unstage, then selective add)
git reset --mixed HEAD~1
git add -p  # interactive patch selection
EDITOR=true git commit -m "part 1"
git add .
EDITOR=true git commit -m "part 2"

# Sync jj state (may need)
jj workspace update-stale
```

⚠️ Only use this for complex splits. Prefer jj-native patterns above.

---

### Common Agent Scenarios

#### Scenario: "Commit these changes"

```bash
# Step 1: Check current state
jj st

# If no description yet:
jj describe -m "feat(scope): description"

# If already described:
jj commit

# If want to commit without describing:
jj commit -m "feat(scope): description"

# Step 2: After commit, create new change for next work
jj new -m "wip: next task"
# Or just: jj new (describe later)
```

**Note:** After `jj commit`, the working copy is empty. Always run `jj new` to continue working. The previous commit becomes your parent (`@-`), available for fixups via `jj edit @-` + `jj squash` if needed.

#### Scenario: "What changed?"

```bash
# Summary of files
jj diff --summary

# Detailed diff
jj diff

# Last N changes
jj log --limit 5
```

#### Scenario: "I need to work on something else"

```bash
# Option 1: Describe current, start new
jj describe -m "wip: current task"
jj new main -m "feat: new task"

# Option 2: Shelve-like (create new, leave current)
jj new -m "feat: new task"  # @ now points here, @- has wip

# Option 3: Create bookmark for later
jj bookmark create my-feature -r @
jj new main

# Come back later
jj edit my-feature
```

---

## Git Interop

### When to Use Git Fallback

| Situation | Use |
|-----------|-----|
| Status, diff, log | **jj** |
| Commit | **jj commit** (default) |
| Push to GitHub | **git push** or **jj git push** |
| Clone new repo | **git clone**, then auto-colocate |
| Submodules | **git** (jj limited support) |
| Complex split | **git** (jj split is interactive only) |

### Auto-Colocation

Fish shell auto-colocates on first `jj` command:

```bash
# In a git repo without .jj/, first jj command auto-runs:
# jj git init --colocate
```

🚨 **CRITICAL:** Never use `git commit`, `git rebase`, `git cherry-pick`, `git merge`, or `git reset --hard` in a colocated repo — they silently corrupt jj history. Read-only git commands (`log`, `diff`, `show`, `blame`) are safe.

---

## Shell Setup

### Fish Abbreviations

```fish
abbr -a js 'jj status'
abbr -a jl 'jj log'
abbr -a jd 'jj diff'
abbr -a jdesc 'jj describe'
abbr -a jc 'jj commit'
abbr -a jsw 'jj workspace add'
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No .jj directory found" | First `jj` command auto-colocates (via Fish wrapper), or run `jj git init --colocate` |
| Merge conflicts | `jj resolve` or use git in colocated repo |
| Need to split interactively | Use [agent patterns](#handling-split-and-interactive-commands) above, or use git in colocated repo |
| Accidentally used git commit | Run `jj undo` if immediately after, or manually recover from jj op log |
| Editor opens (vim/nano) | Cancel with `:q!` or Ctrl+C, then retry with `-m` flag: `jj commit -m "msg"` |
| "command not found: jj" | jj not installed; use git instead |
| "nothing changed" after commit | Working copy is empty (normal jj behavior); changes were committed |

### Agent-Specific Debugging

**Problem: `jj describe` without `-m` opened an editor**
```bash
# What happened: User tried to set commit message, editor opened
# Solution: Cancel editor, use non-interactive form

# Cancel vim: :q!
# Cancel nano: Ctrl+X

# Then:
jj describe -m "feat: actual message"
```

**Problem: Change already has description, need to commit**
```bash
$ jj st
Working copy (@): xyz123abc (empty) (no description set)
# ^ This means change IS empty - files were already committed

# If there ARE files:
$ jj st
Working copy (@): xyz123abc my description here
$ jj commit  # Will use existing description
```

**Problem: User wants to "amend" last commit**
```bash
# In git: git commit --amend
# In jj: just edit @- and squash

jj edit @-              # Go to parent (the commit to amend)
# make edits
jj squash               # Squash working copy into this commit
# or just commit if @- was empty
jj commit -m "new message"
```

---

📚 **Full command reference:** @skills/jujutsu

---

## Appendix: JJ vs Git Quick Map

| Git Concept | JJ Equivalent | Notes |
|-------------|-------------|-------|
| `git add` | (not needed) | jj snapshots automatically |
| `git commit` | `jj commit -m` | Or `jj describe` + `jj commit` |
| `git commit --amend` | `jj squash` or edit `@-` | Describe-first makes this rare |
| `git checkout branch` | `jj edit bookmark` | Bookmarks ≈ branches |
| `git checkout -b` | `jj bookmark create` + `jj new` | Or just `jj new` without bookmark |
| `git stash` | `jj new` or `jj describe` | Multiple changes = natural stashing |
| `git rebase` | `jj rebase -s -d` | `-s` = source, `-d` = destination |
| `git cherry-pick` | `jj new -B change` | `-B` = change description |
| `git log` | `jj log` | `-T` for custom templates |
| `git worktree` | `jj workspace add` | With sparse pattern support |
