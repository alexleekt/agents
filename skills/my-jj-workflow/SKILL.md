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

Personal workflow patterns for jujutsu (jj). For command details, see **@skills/jujutsu**.

## Core Philosophy

- **jj-first**: Use jj for all local operations
- **Auto-colocation**: Running `jj` in a git repo without jj initialized triggers automatic `jj git init --colocate`
- **git for push**: Push to GitHub via git (jj's git colocation makes this seamless)
- **Describe-first**: Write commit messages incrementally with `jj describe -m "..."`, commit when ready

## Key Patterns

### Describe-First Workflow

Don't commit immediately — describe your intent first:

```bash
jj new main
# ... make edits ...
jj describe -m "wip: auth flow"
# ... more edits ...
jj describe -m "feat: JWT authentication"
jj commit -m "feat: JWT authentication"   # Now commit
```

### Organizing Changes

Group similar concerns. Squash fixups into parent, split mixed concerns:

```bash
# Squash fixup into parent (non-interactive with -m)
jj squash -m "final message"

# Cross-commit squash
jj squash --from <src> --into <dst> -m "message"

# Split mixed concerns
jj split
```

### Context Switching (JJ's Superpower)

Multiple in-progress changes without branches:

```bash
jj edit @--           # Go back one change
jj edit feature-x     # Jump to bookmark
jj new main           # Start fresh work
jj log                # See your change stack
```

## Auto-Colocation

Fish shell auto-colocates on first `jj` command in a git repo:

```bash
# In a git repo without .jj/, first jj command auto-runs:
# jj git init --colocate
```

## Workspaces (Multiple Working Directories)

jj uses "workspaces" (not worktrees) — separate working directories linked to the same repo:

```bash
# Create a new workspace
jj workspace add ../feature-ws
cd ../feature-ws

# Remove when done
jj workspace forget ../feature-ws
```

### Sparse Workspaces (Checkout Only What You Need)

Sparse patterns control which files exist in each workspace's working copy — perfect for large repos or focused work.

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
# See current patterns
jj sparse list

# Add paths to working copy
jj sparse set --add src/ --add docs/

# Remove paths (deletes from workspace, not repo)
jj sparse set --remove tests/

# Reset to full checkout
jj sparse reset
```

**Sparse vs .gitignore:**

| | `.gitignore` | `jj sparse` |
|---|---|---|
| **Purpose** | Prevents VCS tracking | Controls checkout presence |
| **Scope** | All workspaces globally | Per-workspace only |
| **Effect** | Files ignored from status | Files missing from disk |
| **Use for** | Build artifacts, secrets, deps | Large repos, focused work |

**Example workflow:**
```bash
# Main repo has everything
~/project $ ls
frontend/  backend/  docs/  assets/  .gitignore

# Frontend workspace (only frontend + docs)
~/project $ jj workspace add --sparse-patterns empty ../frontend-ws
cd ../frontend-ws
jj sparse set --add frontend/ --add docs/
$ ls
frontend/  docs/

# Backend workspace (only backend)
jj workspace add --sparse-patterns empty ../backend-ws
cd ../backend-ws
jj sparse set --add backend/
```

## Fish Abbreviations

```fish
abbr -a js 'jj status'
abbr -a jl 'jj log'
abbr -a jd 'jj diff'
abbr -a jdesc 'jj describe'
abbr -a jc 'jj commit'
```

## When to Use Git Fallback

| Situation | Use |
|-----------|-----|
| Status, diff, log | **jj** |
| Commit | **jj commit** (default) |
| Push to GitHub | **git push** or **jj git push** |
| Clone new repo | **git clone**, then auto-colocate |
| Submodules | **git** (jj limited support) |

## Troubleshooting

**"No .jj directory found"**
- First `jj` command auto-colocates (via Fish wrapper)
- Or: `jj git init --colocate`

**Merge conflicts**
- `jj resolve` or use git in colocated repo

---

📚 **Full command reference:** @skills/jujutsu
