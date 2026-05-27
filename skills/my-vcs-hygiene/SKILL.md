---
name: my-vcs-hygiene
description: |
  **ALWAYS use when:** the user says commit, push, stage, ship, "looking good", "done", "wrap it up", or signals completion; when making commits; when starting a session with uncommitted changes or on a dirty main branch; when the user gives visual or UX feedback during building ("move this left", "make it smaller", "change the color"). Use whenever the user mentions committing, pushing, shipping, or wrapping up work — even if they don't explicitly use git terminology. Also use when deciding commit scope, handling monorepo cross-package changes, managing visual iteration loops, or amending commits.

  **DO NOT use for:** worktree switching or naming — use @skills/my-workflow. Plan/build/review phases — use @skills/my-project-lifecycle. `wt` CLI mechanics — use @skills/worktrunk.
---

# VCS Hygiene

Commit discipline, branch safety, and shipping discipline.

## ⚡ Quick Start

**User says "commit it", "push it", "ship it", or "looking good"?**
→ Execute directly — confirm scope briefly, don't ask permission. Branch-from-Main Guard applies.

**User gives visual/UX feedback ("move this left", "group these together")?**
→ Batch related tweaks into a single commit. Don't commit every pixel tweak. Commit per logical grouping.

**Starting session with uncommitted work?**
→ If on main, apply Branch-from-Main Guard first. Ask: "Commit this first, or continue editing?"

**About to make large/irreversible change?**
→ Commit first. Prefer small, focused commits.

## Activation Condition

**This skill activates when the agent is performing or deciding VCS actions.**

Apply these rules when:
- The user issues VCS commands or wrap-up signals ("commit it", "ship it", "done")
- The user gives visual/UX feedback that implies a change-and-commit cycle
- The session starts with uncommitted changes from a prior session
- Deciding when or what to commit
- About to amend, rebase, or rewrite history
- Working in a monorepo and deciding commit scope

Do **not** apply these rules when:
- The user asks about worktrees or direction → use @skills/my-workflow
- The user is planning or reviewing a feature → use @skills/my-project-lifecycle

## Scope

This skill covers **agent behavioral rules** for:
- User-initiated VCS actions (commit, push, stage, ship)
- Implicit commit signals ("looking good", "done", "wrap it up")
- Branch-from-Main Guard (never commit to main)
- Resuming with uncommitted work
- Commit discipline (when, what, and why to commit)
- Visual iteration (handling repeated user UI feedback)
- Monorepo commit scope
- Amend safety

It does **not** cover:
- Worktree switching or naming → @skills/my-workflow
- Plan/build/review lifecycle → @skills/my-project-lifecycle
- `wt` CLI commands or syntax → @skills/worktrunk

## User-Initiated VCS Actions

When the user explicitly commands a commit, push, stage, or ship:

1. **Do not ask for permission** — they already gave it. Asking adds friction.
2. **Confirm scope briefly** — "Committing these 6 files on branch `docs/foo`?" gives them a chance to correct without blocking.
3. **Apply Branch-from-Main Guard** — if on `main` with uncommitted changes, create a feature branch first.
4. **Execute** — stage → commit → push (if requested).

### Why this matters
The default "ask first" behavior is for **unsolicited** actions — when the agent initiates. When the user explicitly commands a VCS action, asking is patronizing and slows the loop. Confirm scope, then execute.

## Implicit Commit Signals

Phrases that signal the user wants to wrap up and commit:

| Explicit | Implicit |
|----------|----------|
| "commit it" | "looking good" |
| "push it" | "that's it" |
| "stage this" | "done" |
| "ship it" | "wrap it up" |
| "commit and push" | "finish up" |
| | "let's ship this" |

When you hear these:
1. Check `git status` to see what's changed
2. Confirm what to include: "Commit the changes to `<files>`?"
3. Apply Branch-from-Main Guard if needed
4. Execute

## Branch-from-Main Guard

If on `main` (or any protected default branch) with uncommitted changes:

1. **Create a descriptive feature branch**: `git checkout -b <kebab-case-name>`
2. **Then commit** — never commit directly to main

The branch name should describe the actual work, not be generic.

**Good**: `docs/event-horizon-provider-context`, `fix-auth-timeout-5min`
**Bad**: `wip`, `temp`, `stuff`

## Resuming with Uncommitted Work

When a session starts and `git status` shows changes:

1. Check if on main → if yes, apply Branch-from-Main Guard
2. Ask: "I see uncommitted work from a prior session. Commit this first, or continue editing?"
3. If the user says continue without committing, note it and proceed

Do **not** silently ignore a dirty tree — it means work from a prior session may be at risk.

## Commit Discipline

Make commits **early and often**. Prefer small, focused commits over large bundles.

### Must Commit Before

- Large file moves, deletions, or renames
- Irreversible operations (destructive edits, schema changes)
- Switching worktrees or ending a session
- Any change you'd regret losing if the terminal crashed

### Good Commit Hygiene

- Commit when a logical unit of work is complete
- Commit before running risky commands
- Commit when the user says "let me think" or pauses for a while
- Do not wait for perfection — imperfect commits are better than lost work

### Don't Commit Unnecessarily

- Trivial tweaks (whitespace, typo fixes) — batch if possible
- Work-in-progress that breaks the build — unless it's end of session

## Session-End Commit Gate ("3×5" Heuristic)

If the session has made edits or writes and the user has **not** given an explicit VCS signal, the agent **must** check for uncommitted work before ending.

### Trigger Conditions (any one of)
| Dimension | Threshold | Action |
|-----------|-----------|--------|
| **Files touched** | ≥ 3 files edited or written | Prompt to commit at next natural pause |
| **Turns elapsed** | ≥ 5 agent turns that included `edit` or `write` | Prompt to commit at next natural pause |
| **Irreversible op** | Any delete, rename, schema change | Commit immediately, no threshold |
| **Session end** | Any `edit`/`write` occurred and zero VCS commands | **Mandatory** commit reminder |

### Agent-Initiated Prompt

Before ending the session:
1. Check `git status` (or `yadm status` for dotfiles)
2. If changes exist and no commit was made in this session:
   > "I edited `<files>`. Should I commit these changes?"
3. Show `git diff --stat` for scope confirmation
4. If user approves → apply Branch-from-Main Guard → commit with generated message
5. If user declines → note why and proceed

### Config-File Auto-Commit

For paths under `~/.config/`, `~/.pi/`, dotfiles repo, or `*.json`/`*.yaml`/`*.toml` in home:
- **Threshold:** 1 file changed → auto-commit at session end
- **Prefix:** Use `config:` for config-only commits
- **Message format:** `config: <what changed> in <file>`

Example: `config: add EVENTHORIZON_DEBUG to fish env abbreviations`

## Visual Iteration

When the user gives repeated visual or UX feedback during building:

**Pattern**: Build → Show → User tweaks → Adjust → User tweaks → Adjust → ... → Commit

### Rules

1. **Batch related tweaks** — "move the bullet left" + "group cost with cache" = one style commit
2. **Commit per logical grouping** — each distinct visual concern gets its own commit if the feedback comes separately
3. **Don't commit every pixel tweak** — if three tweaks are all about the same component, batch them
4. **Use `style:` prefix** for pure visual changes: `style: reposition bullet and group cost/cache per user request`
5. **Note the user request in the commit body** — preserves context for future reviewers

### Example from practice

```
style: reposition bullet and group cost/cache per user request
style: group bullet with status word
style: fixed-width status column with indicator left of online
```

Three separate commits because each was a distinct visual concern raised by the user. Batch only when the tweaks are obviously related.

## Monorepo Commit Scope

In a monorepo, decide commit scope by concern, not by package boundary:

| Rule | Example |
|------|---------|
| **Same concern → same commit** | Docs for both `pi-event-horizon-provider` and `pi-extension-reloader` in one `docs:` commit |
| **Different concerns → separate commits** | `feat` in package A and `fix` in package B = two commits |
| **Cross-package refactor → one commit** | Shared type moved from A to B = one `refactor:` commit |
| **Package-scoped release → separate** | Version bump for A only = scoped commit |

**Guideline**: If someone reading `git log --oneline` would understand the change without knowing monorepo structure, the scope is right.

## Amend Safety

`git commit --amend` rewrites the commit hash. The old commit becomes **unreachable** — invisible in `git log` but still in the object database.

**When amending is risky:**
- Right after a refactor that replaced a code pattern. Fixes from the old architecture may not exist in the new code.
- When the commit you're amending contained a fix that hasn't been verified in the refactored layout.

**Recovery if a fix was lost:**
```bash
git fsck --unreachable --no-reflogs | grep commit
# For each suspicious hash:
git show <hash> --stat
git show <hash> -- <file>
```

**Prevention:**
- Before amending during a refactor, review the diff one last time
- After refactoring a pattern, grep the new code for old pattern keywords to verify fixes migrated
- Never amend a commit that has already been pushed

## Decision Tree

```
User gave explicit VCS command or implicit commit signal?
├── Yes → Confirm scope briefly, then execute
│         ├── On main with changes? → Branch-from-Main Guard first
│         └── Then stage → commit → push (if requested)
└── No → Continue

User gave visual/UX feedback?
├── Yes → Apply the tweak
│         ├── More related tweaks coming? → Keep iterating
│         └── This grouping is done? → Commit with `style:` prefix
└── No → Continue

About to make large/irreversible change?
├── Yes → Commit first
└── No → Proceed

Committing in a monorepo?
├── Same concern across packages? → One commit
└── Different concerns? → Separate commits

Session ending with uncommitted changes?
├── ≥ 3 files OR ≥ 5 edit turns OR irreversible op?
│   └── Yes → Prompt: "Should I commit these changes?"
│       ├── User says yes → Branch-from-Main Guard → commit → end
│       └── User says no → Note reason → end
└── No → End normally
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Commit fails due to untracked files | Stage with `git add .` or `git add -p` for selective staging |
| Lost changes after `git commit --amend` | `git fsck --unreachable --no-reflogs \| grep commit` → `git show <hash>` to recover; then port the fix into the refactored architecture |
| User says "just commit it" but on main | Apply Branch-from-Main Guard first, then commit |

## Common Mistakes

❌ **Wrong:** Asking permission when the user already said "commit it"
✅ **Right:** Confirm scope briefly, then execute: "Committing these 4 files on `fix-auth`?"

❌ **Wrong:** Committing after every tiny tweak (whitespace, typo)
✅ **Right:** Batch trivial fixes; commit on logical units or before irreversible actions

❌ **Wrong:** Committing directly to main when in a worktree-less session
✅ **Right:** Apply Branch-from-Main Guard — create a feature branch first

❌ **Wrong:** Batching unrelated visual tweaks into one giant style commit
✅ **Right:** One commit per distinct visual concern; batch only obviously related tweaks

❌ **Wrong:** Splitting cross-package documentation into separate commits just because packages differ
✅ **Right:** Same concern (docs) = same commit, even across packages

❌ **Wrong:** Amending a commit during a refactor without verifying fixes migrated
✅ **Right:** After amending, grep the new code for old pattern keywords; run `git fsck --unreachable` if unsure

## Related Skills

- **@skills/my-workflow** — Worktrees, direction, naming, session boundaries, parallel agents
- **@skills/my-project-lifecycle** — Plan → Build → Review → Document → Ship
- **@skills/worktrunk** — `wt` CLI commands, hooks, config, troubleshooting
- **@skills/my-semantic-release** — Release workflows when a worktree is ready to merge
- **@skills/my-code-review** — Reviewing changes before committing in a worktree

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.1
- **Update notes:** Added Session-End Commit Gate ("3×5" heuristic: ≥3 files OR ≥5 edit turns → prompt to commit). Added Config-File Auto-Commit rule for dotfiles/config paths. Addresses glasskey/pi-heading/HongKongTaxiMeterCarThing VCS collapse (0.5–0.7% commit rates) where user never signals "commit it" and agent never asks.
