---
name: jj-to-git-migration
description: >
  Migrate a Jujutsu (jj) repository back to pure Git without losing commits,
  branches, bookmarks, tags, or working-copy changes. Use when the user wants
  to abandon jj, export jj state to git, remove jj traces, or transition from
  colocated/non-colocated jj back to git-only workflow.
  Trigger phrases: 'jj to git', 'migrate from jj', 'remove jj', 'jj export',
  'stop using jj', 'colocated to git', 'jj cleanup', 'jj uninstall repo'.
---

# jj-to-git Migration Skill

Migrate any jj repository (colocated or standalone) back to pure Git while
preserving **all** history, branches, tags, bookmarks, and working-copy changes.
Then safely remove jj traces using `trash-cli`.

## Prerequisites

- `jj` CLI installed and functional
- `git` CLI installed
- `trash-cli` (`trash`) installed for safe deletion (uses macOS Trash/Recycle Bin)
- Shell: Fish, Zsh, or Bash

## Quick Reference

| Scenario | Command |
|----------|---------|
| Check if repo is colocated | `ls -la .jj .git` |
| List jj bookmarks | `jj bookmark list -a` |
| List all jj changes | `jj log --all` |
| Export jj → git | `jj git export` (or automatic in colocated) |
| Ensure git branch matches jj | `git branch -a -vv` |
| Trash `.jj` | `trash .jj` |
| Trash jj config file | `trash ~/.config/jj/config.toml` |

## Full Migration Procedure

### 1. Assess Current State

Run these in the repository root (the directory containing `.jj` or `.git`):

```fish
# Check repo type
if test -d .jj; and test -d .git
    echo "COLLOCATED repo (.jj + .git present)"
else if test -d .jj
    echo "JJ-ONLY repo (jj with remote git backend)"
else
    echo "No jj repo found here"
end

# Show all jj bookmarks (these become git branches)
jj bookmark list -a

# Show full jj history
jj log --all --no-pager

# Show current git state
git branch -a -vv
git status
```

**Key things to note:**
- Any jj bookmark not at `@git` needs to be pushed to git refs
- Working-copy changes (jj status shows `M`, `A`, `D`) need to be handled
- Detached HEAD in git means jj imported it; you may need to `git checkout <branch>`

### 2. Preserve Working-Copy Changes

jj maintains the working copy as a commit (`@`). Before removing jj, ensure
uncommitted changes are either committed or stashed in git:

**Option A: Commit via jj (recommended — preserves history)**
```fish
jj describe -m "WIP: working copy before jj-to-git migration"
```

**Option B: Export working copy to git stash**
```fish
# In colocated repos, jj auto-exports. Check git status:
git status
# If there are changes, stash them:
git stash push -m "jj migration working copy"
```

### 3. Sync All Bookmarks to Git

In colocated mode, jj automatically mirrors bookmarks to git branches.
Verify this:

```fish
# For each jj bookmark, check if a git branch exists
for bookmark in (jj bookmark list -T "name" --no-pager)
    if git show-ref --verify --quiet refs/heads/$bookmark
        echo "OK: $bookmark exists in git"
    else
        echo "MISSING: $bookmark not in git — creating..."
        # Find the commit the bookmark points to
        set commit (jj bookmark list $bookmark -T "commit_id" --no-pager)
        git branch $bookmark $commit
    end
end
```

For **non-colocated** jj repos (where `.jj` is separate from the backing git repo):
```fish
# Export all jj changes to the backing git repo
jj git export
# Then cd to the git repo and pull/fetch the exported refs
```

### 4. Ensure Git HEAD is on a Branch

jj often leaves git in detached HEAD state because it imports HEAD:

```fish
# Check if detached
if git symbolic-ref --quiet HEAD > /dev/null 2>&1
    echo "HEAD is on a branch — OK"
else
    echo "DETACHED HEAD — checking out main/master branch"
    # Find the branch matching jj's main bookmark
    set main_branch (jj bookmark list main -T "name" --no-pager 2>/dev/null; or echo "main")
    if contains $main_branch (git branch --format="%(refname:short)")
        git checkout $main_branch
    else
        git checkout -b $main_branch (jj bookmark list main -T "commit_id" --no-pager)
    end
end
```

### 5. Preserve Tags (Optional but Recommended)

jj may have created tags during releases. Ensure they're in git:

```fish
git tag -l
# Compare with any jj-managed tags. jj doesn't natively manage tags,
# but if your workflow created them via git, they're already present.
```

### 6. Archive Orphan Commits (CRITICAL — prevents code loss)

**This is the most important step.** In colocated repos, jj creates
`refs/jj/keep/*` in `.git/refs/jj/keep/` to prevent garbage collection of
commits it cares about. Many of these commits have **no corresponding git
branch or tag** and will be lost when jj refs are cleaned up.

**Check for orphan commits:**
```bash
#!/bin/bash
# Run from repo root
orphan_count=0
for keep_ref in .git/refs/jj/keep/*; do
  commit=$(cat "$keep_ref")
  contained=$(git branch -a --contains "$commit" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$contained" -eq 0 ]; then
    orphan_count=$((orphan_count + 1))
    echo "ORPHAN: $(git log -1 --oneline "$commit" 2>/dev/null || echo $commit)"
  fi
done
echo "Total orphan commits: $orphan_count"
```

**Archive them as git tags before migration:**
```bash
#!/bin/bash
ARCHIVE_PREFIX="jj-archive"
for keep_ref in .git/refs/jj/keep/*; do
  commit=$(cat "$keep_ref")
  contained=$(git branch -a --contains "$commit" 2>/dev/null | wc -l | tr -d ' ')
  [ "$contained" -gt 0 ] && continue

  desc=$(git log -1 --format=%s "$commit" 2>/dev/null || echo "")
  short=$(git rev-parse --short=8 "$commit")
  if [ -n "$desc" ]; then
    slug=$(echo "$desc" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
    tag_name="${ARCHIVE_PREFIX}/${slug}-${short}"
  else
    tag_name="${ARCHIVE_PREFIX}/orphan-${short}"
  fi

  suffix=1
  base_tag="$tag_name"
  while git show-ref --verify --quiet "refs/tags/${tag_name}" 2>/dev/null; do
    tag_name="${base_tag}-${suffix}"
    suffix=$((suffix + 1))
  done

  git tag "$tag_name" "$commit"
  echo "Tagged: $tag_name -> $short"
done
```

> **Warning:** Skipping this step can permanently lose commits that contain
> real work — abandoned changes, old bookmarks, superseded revisions, etc.

### 7. Verify Complete Git Parity

Before destroying jj state, verify git has everything:

```fish
# 1. Git log should match jj log (same commits, same messages)
git log --oneline --all --graph | head -20
jj log --no-graph --no-pager | head -20

# 2. Every jj bookmark should have a git branch counterpart
jj bookmark list -a -T "name" --no-pager | while read -l b
    git show-ref --verify --quiet refs/heads/$b
    or echo "WARNING: bookmark $b missing from git"
end

# 3. Working copy should be clean or intentionally preserved
git status

# 4. All orphan commits should now have archive tags
for tag in (git tag -l 'jj-archive/*')
    git show-ref --verify --quiet refs/tags/$tag
    or echo "WARNING: archive tag $tag missing"
end
```

### 8. Remove jj Traces

**Trash the jj repo directory:**
```fish
# From the repo root
trash .jj
```

**Remove jj `refs/jj/keep/*` from `.git/`** (these are now redundant since
orphan commits were archived as tags):
```bash
rm -rf .git/refs/jj
```

**Remove jj-specific git configs** (colocated repos may have these):
```bash
git config --local --unset-all jj.autoinstall 2>/dev/null || true
git config --local --unset-all jj.colocate 2>/dev/null || true
```

**Remove jj hooks** (if any):
```bash
ls .git/hooks/ | grep jj 2>/dev/null || echo "No jj hooks found"
```

**Trash jj global config (only if abandoning jj entirely):**
```fish
# WARNING: Only do this if you are quitting jj completely across ALL repos
trash ~/.config/jj/config.toml 2>/dev/null; or true
trash ~/.jj 2>/dev/null; or true
```

### 9. Verify Clean Git-Only State

```bash
# Should report "There is no jj repo"
jj status 2>&1 | head -1

# Should show normal git status
git status

# Should show branches without jj references
git branch -a

# Should not have .jj directory
if test -d .jj
    echo "ERROR: .jj still exists!"
else
    echo "SUCCESS: jj fully removed, git-only repo"
end

# Should still have all archive tags
git tag -l 'jj-archive/*' | wc -l
```

## Fish Wrapper Cleanup

If you were using the [jj auto-colocate Fish wrapper](https://github.com/jj-vcs/jj), remove it:

```fish
# Remove the wrapper function
functions --erase jj
# Remove the file
rm ~/.config/fish/functions/jj.fish
# Reload
source ~/.config/fish/config.fish
```

## Multi-Repo Batch Migration

To migrate **all** jj repos under a directory:

```fish
#!/usr/bin/env fish
# jj-migrate-all.fish

for dir in (find $argv[1] -name ".jj" -type d -maxdepth 3 2>/dev/null)
    set repo_root (dirname $dir)
    echo "\n=== Migrating $repo_root ==="
    cd $repo_root

    # Step 2: Commit working copy
    jj describe -m "WIP: pre-migration working copy" 2>/dev/null; or true

    # Step 3: Export
    jj git export 2>/dev/null; or true

    # Step 4: Ensure branch checkout
    set main_branch (jj bookmark list -T "name" --no-pager 2>/dev/null | head -1; or echo "main")
    git checkout $main_branch 2>/dev/null; or git checkout -b $main_branch (git rev-parse HEAD)

    # Step 7: Trash .jj
    trash .jj

    # Verify
    if test -d .jj
        echo "FAIL: $repo_root"
    else
        echo "OK: $repo_root"
    end
end
```

## Recovery (If Something Goes Wrong)

If you trash `.jj` prematurely and need to recover:

```fish
# Restore from macOS Trash
cp -R ~/.Trash/.jj ./.jj
# Or if trash-cli was used:
trash-restore .jj
```

Then re-run the migration steps.

## What Gets Lost vs. Preserved

| Item | Preserved? | Notes |
|------|-----------|-------|
| Git commits | ✅ Yes | All git history is untouched |
| jj bookmarks | ✅ Yes | Become git branches |
| Working copy | ✅ Yes | Commit to branch or stash |
| **Orphan jj commits** | ⚠️ **Risk** | Archive `refs/jj/keep/*` as tags first |
| jj operation log | ❌ No | `.jj/op_store/` is jj-specific |
| jj change IDs | ❌ No | Git uses commit SHAs only |
| jj aliases/config | ❌ No | jj-specific, not portable |
| jj conflicts | ⚠️ Partial | Resolve before migration |
| Git tags | ✅ Yes | Already in `.git/refs/tags/` |

## References

- jj docs: `jj git export --help`
- [jj colocation documentation](https://jj-vcs.github.io/jj/latest/git-compatibility/#co-located-jujutsugit-repos)
- `trash-cli`: `npm install -g trash-cli` or `brew install trash`