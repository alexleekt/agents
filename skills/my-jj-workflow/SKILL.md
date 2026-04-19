---
name: my-jj-workflow
description: |
  **ALWAYS use when user mentions:** "jj", "jujutsu", "commit" (assumes jj commit),
  "what changed", "check status", "push to github", "worktree", or any daily version control operations.

  **DO NOT use for:** semantic versioning, changelog generation, or release workflows —
  use @skills/my-semantic-release for those.

  Daily version control workflows using jujutsu (jj) with git/github as fallback.
  When user says "commit", they mean `jj commit` unless they explicitly say "git commit".
  Auto-colocation, worktrees, and practical day-to-day VCS operations.
---

# My JJ Workflow

Day-to-day version control with jujutsu (jj), preferring jj over git when available.

## Core Philosophy

- **jj-first**: Use jj for all local operations
- **Auto-colocation**: Running `jj` in a git repo without jj initialized triggers automatic `jj git init --colocate`
- **git for push**: Push to GitHub via git (jj's git colocation makes this seamless)
- **Worktrees**: Use jj's native worktree support instead of git worktrees

## Quick Commands

### Status & Overview
```bash
jj status              # What's changed (alias: jj st)
jj log                 # Commit history with graph
jj diff                # Current changes
jj show <revision>     # Details of a specific commit
```

### Making Changes — Prefer `jj describe` over `jj commit`

**Key insight:** In jj, you can describe (write a commit message) without committing. This lets you:
- Write commit messages incrementally as you work
- Keep work-in-progress changes without committing
- Separate "what I did" from "when I lock it in"

```bash
jj describe            # ⭐ Edit commit message of current change (do this first!)
jj describe -m "feat: add user authentication"  # Set message inline
jj commit              # Create new commit from described change
jj new <parent>        # Create new empty change on top of parent
jj edit <revision>     # Move to and edit a specific change
```

**Workflow:**
1. `jj new main` — start fresh change
2. ... make some edits ...
3. `jj describe -m "wip: working on auth flow"` — capture intent
4. ... more edits ...
5. `jj describe -m "feat: add JWT-based authentication"` — refine message
6. `jj commit` — when ready, commit the described change
7. `jj new` — automatically start next change

### Working with Branches/Bookmarks
```bash
jj bookmark list       # List bookmarks (jj's lightweight branches)
jj bookmark set <name> # Create/update bookmark at current change
jj bookmark delete <name>
```

### Push to GitHub
```bash
# In a colocated repo, use git for push
jj st                  # Ensure clean state
git push origin <bookmark>  # Push via git (seamless with jj colocation)

# Or set up jj push (if configured)
jj git push --bookmark <name>
```

## Auto-Colocation Workflow

The Fish shell has an auto-colocation wrapper. When you run `jj` in a git repo:

1. Detects if `.jj/` directory exists
2. If not, runs `jj git init --colocate` automatically
3. Then executes your jj command

**Result:** Zero-friction jj adoption in existing git repos.

## Worktrees with JJ

JJ has native worktree support that's simpler than git worktrees:

```bash
# Create new worktree for parallel work
jj workspace add ../feature-branch-worktree

# Work in that directory
cd ../feature-branch-worktree
jj st                  # Independent change stack

# Go back to main work
cd -

# When done, remove worktree
jj workspace forget ../feature-branch-worktree
rm -rf ../feature-branch-worktree
```

## When to Use Git Fallback

| Situation | Use |
|-----------|-----|
| Daily status, diff | **jj** |
| **Commit** | **jj commit** (default assumption) |
| Push to GitHub | **git push** or **jj git push** |
| Clone new repo | **git clone**, then auto-colocate on first `jj` |
| Submodules | **git** (jj doesn't fully support yet) |
| Complex rebase/merge conflicts | Either, but git may have better tooling |

**Note:** When user says "commit", they mean `jj commit` unless explicitly stated otherwise.

## Fish Abbreviations

```fish
abbr -a js 'jj status'
abbr -a jl 'jj log'
abbr -a jd 'jj diff'
abbr -a jdesc 'jj describe'   # ⭐ Describe changes (don't commit yet)
abbr -a jc 'jj commit'
```

**Pro tip:** Use `jdesc` liberally. It saves your intent without locking you in.

## Common Patterns

### Start New Feature
```bash
jj new main            # Create new change on main
# ... make changes ...
jj bookmark set feature-x
jj st
```

### Check What Changed Before Committing
```bash
jj diff                # See current changes
jj st                  # What's tracked/untracked
jj describe            # ⭐ Write commit message (describe before you commit!)
```

**Remember:** Describe early and often. You can always update the message with another `jj describe` before committing.

### Quickly Fix Something on Main
```bash
jj new main            # Start fresh change on main
jj describe -m "fix: correct typo in docs"  # ⭐ Describe first
# ... edit files ...
jj commit              # Commit when done
git push origin main
```

### Switch Context (JJ's Superpower)
```bash
jj edit @--           # Go back one change
jj edit feature-x     # Jump to bookmark
jj new main           # Start fresh work
```

JJ lets you have multiple in-progress changes without branches. Use `jj log` to see your change stack.

## Troubleshooting

**"No .jj directory found"**
- First `jj` command in a git repo auto-colocates (via Fish wrapper)
- Or manually: `jj git init --colocate`

**Push rejected**
- JJ doesn't directly push to GitHub by default
- Use: `git push origin <branch>` or configure `jj git push`

**Merge conflicts**
- `jj resolve` or use git's familiar conflict resolution
- Both work in colocated repos
