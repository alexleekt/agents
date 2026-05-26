---
name: my-workflow
description: |
  **ALWAYS use when:** assessing task direction, deciding whether to stay in the current worktrunk or switch; updating worktree names to match evolving work; managing session boundaries and context switching; spawning parallel subagents. Use whenever the user asks about worktrees, switching contexts, session starts/ends, or coordinating multiple agents.

  **DO NOT use for:** commit/push/ship actions — use @skills/my-vcs-hygiene. Plan/build/review/document phases — use @skills/my-project-lifecycle. `wt` CLI mechanics — use @skills/worktrunk.
---

# Personal Workflow Discipline

Core orchestration: worktrees, direction, session boundaries, and parallel agents.

> **Note:** This is a living document. Workflows evolve. Check the latest version
> before making decisions.

## ⚡ Quick Start

**Task doesn't match the current worktrunk?**
→ Ask the user before switching or spawning a new worktree.
→ If the user approves, prefer `/wt-switch-create <branch>` to create, switch, and relaunch in one step.

**Significant code change or irreversible file action?**
→ Consult @skills/my-vcs-hygiene — commit first. Prefer small, focused commits.

**Worktree name no longer describes the work?**
→ Propose renaming it to match the actual direction.

**Need parallel agents for a large task?**
→ Use `spawn_worktree_agent` to create isolated worktrees with subagents, or `/wt-switch-create` to open additional Pi sessions in new worktrees.

## Activation Condition

**This skill activates when the agent is managing worktree state, session context, or parallel coordination.**

Apply these rules when:
- Assessing whether a task fits the current worktrunk
- Starting or ending a session
- Switching contexts mid-session
- Spawning or coordinating parallel subagents
- Naming, renaming, or creating worktrees

Do **not** apply these rules when:
- The user issues a VCS command (commit, push, ship) → use @skills/my-vcs-hygiene
- Planning or reviewing a feature → use @skills/my-project-lifecycle
- Answering questions about `wt` CLI → use @skills/worktrunk

## Scope

This skill covers **agent behavioral rules** for:
- Direction assessment (does the task fit the current worktrunk?)
- Worktree naming hygiene (keeping names accurate)
- Session boundaries (start, end, context switching)
- Parallel work with subagents
- Worktrunk config maintenance

It does **not** cover:
- Commit/push discipline → @skills/my-vcs-hygiene
- Plan/build/review/document lifecycle → @skills/my-project-lifecycle
- `wt` CLI commands or syntax → @skills/worktrunk
- Hook configuration or project automation → @skills/worktrunk
- Commit message generation → @skills/worktrunk

## Direction Assessment

When the user's task changes or diverges from the current worktrunk's purpose:

1. **Compare against the current worktrunk name/purpose**
   - Does the task fit? Continue.
   - Does it diverge meaningfully? Flag it.

2. **Default behavior: ask first (conservative)**
   - "This seems like a new direction from `<current-worktree>`. Switch to a new worktree with `/wt-switch-create <name>`?"
   - Let the user decide. Do not switch unilaterally.

3. **When the user explicitly says "let's work on X"**
   - If X clearly differs from the current worktrunk's scope, propose switching.
   - If related, continue but note: "Continuing in `<worktree>` — say 'new worktree' if you want separation."

4. **Before spawning a parallel subagent, check `wt list` for active worktrees**
   - Look for 🤖 markers to see which worktrees already have running agents.
   - Avoid naming collisions and coordinate resource usage.

### Examples

| Situation | Action |
|-----------|--------|
| User asks to fix a bug in feature branch | Continue in current worktree |
| User asks to start an unrelated refactor | Ask: "New worktree with `/wt-switch-create refactor-auth`?" |
| User asks to review a different PR | Check `wt list` for that PR's worktree, then ask: "Switch to `<branch>`?" |
| Task evolved away from original intent | Propose renaming or switching |
| Large task (50+ files, multi-domain) | Propose: "Spawn parallel subagents with `spawn_worktree_agent`?" |

## Worktree Naming Hygiene

Worktree names should describe the **actual work being done**, not the original intent.

### When to Rename

- The work evolved significantly from the original branch name
- The name is misleading or too vague
- The task changed scope after creation

### How to Propose

- "This worktree is named `fix-login` but we're now refactoring auth. Rename to `refactor-auth`?"
- Let the user approve. Do not rename silently.

### Naming Conventions

- Use kebab-case: `fix-auth-timeout`, `add-oauth-login`
- Be specific: `fix-login` → `fix-session-timeout-5min`
- Avoid generic names: `wip`, `temp`, `stuff`

## Worktrunk Config Maintenance

When creating a new worktree or working in a repo without `.config/wt.toml`, consider improving the worktrunk configuration so future worktrees benefit.

### Checklist when spawning/creating worktrees

1. **Does `.config/wt.toml` exist?**
   - If missing, check if the project warrants one (any non-trivial repo with hooks, build steps, or shared tooling)
   - If present, review whether it's still accurate for the current build system

2. **Read the build system** before designing hooks:
   - `justfile` → use `just check`, `just test`, `just safety-check`, etc.
   - `package.json` → use `npm ci`, `npm run lint`, `npm test`
   - `Cargo.toml` → use `cargo build`, `cargo clippy`, `cargo test`
   - `pyproject.toml`/`setup.py` → use `pip install`, `pytest`, `ruff check`, `mypy`
   - No build manifest → skip or use lightweight shell checks

3. **Handle gitignored files (`.env`, caches, local state):**
   - Add `wt step copy-ignored` to `pre-start` when `.env` or other gitignored files are needed in new worktrees
   - Use `[[pre-start]]` **pipeline** syntax (not `[pre-start]` table) to control ordering:
     ```toml
     [[pre-start]]
     copy = "wt step copy-ignored"  # Step 1: .env is now present

     [[pre-start]]
     check = "just check"            # Step 2: can validate .env
     ```
   - **Never** use `[pre-start]` table form with multiple keys — steps run concurrently and ordering is undefined
   - Add an `.env` fallback step after `copy-ignored` for first-time clones where main lacks `.env`:
     ```toml
     [[pre-start]]
     env-fallback = "sh -c '[ -f .env ] || cp .env.example .env'"
     ```

4. **Use `.worktreeinclude` as a whitelist for what to copy:**
   - Create `.worktreeinclude` in the repo root alongside `.gitignore` to explicitly list gitignored files that should be copied to new worktrees
   - **Project-level** — assess what the repo needs (e.g., `.env`, `node_modules/`, `target/`)
   - **User-level** — keep personal excludes (`.pi/`, `.vscode/`, `.idea/`) in `~/.config/worktrunk/config.toml` under `[step.copy-ignored]`
   - `.worktreeinclude` is more intentional than `step.copy-ignored.exclude` in project config — you say what TO copy, not what NOT to copy
   - Example `.worktreeinclude`:
     ```text
     # Whitelist of gitignored files to copy into new worktrees
     .env
     node_modules/
     ```

5. **Trust mise if the repo uses it:**
   - If `mise.toml` exists, add a `pre-start` step that trusts mise tools — but only if mise is installed
   - Wrap in `sh -c` for shell portability (works in bash, fish, zsh):
     ```toml
     [[pre-start]]
     mise = "sh -c 'command -v mise >/dev/null 2>&1 && mise trust || true'"
     ```

6. **Avoid fragile hooks:**
   - Don't put server-requiring tests in `pre-merge` — they break in CI/non-interactive contexts
   - Don't put destructive commands (`rm -rf`, `DROP TABLE`) in any hook
   - Don't put network fetches (`curl`, `wget`) in hooks

### Common config patterns by project type

| Build System | `pre-start` | `pre-commit` | `pre-merge` |
|---|---|---|---|
| npm/Node | `npm ci` | `npm run lint` + `npm run typecheck` | `npm test` |
| Cargo/Rust | `cargo build` | `cargo clippy` + `cargo fmt --check` | `cargo test` |
| Python/just | `just check` | `just safety-check` | (skip if tests need running server) |
| Generic | `cp .env.example .env` | — | — |

### Service projects (APIs, proxies, servers)

For repos that run a local service, add a `[list]` URL so `wt list --full` shows whether the service is listening:

```toml
[list]
url = "http://localhost:4000"
```

This lights up the URL column in `wt list` when any worktree has the service running.

### What NOT to add

- `switch.create` — **not a valid config key** anywhere (global or per-project). It's CLI-only. `wt switch <branch>` already auto-creates worktrees for existing branches without any flag.

## Session Boundaries

### Starting a Session

1. Check the current worktrunk name and purpose
2. Run `git status` — if dirty, consult @skills/my-vcs-hygiene for **Resuming with Uncommitted Work**
3. Confirm with the user if the task fits
4. If no worktree exists and the task is non-trivial, suggest creating one
5. If creating a worktree and `.config/wt.toml` is missing, consider the **Worktrunk Config Maintenance** checklist above

### Ending a Session

1. **Commit any uncommitted work** — consult @skills/my-vcs-hygiene. Even if WIP.
2. Summarize what was done and what's left
3. Note the current worktree name for next time
4. If the work is complete, consult @skills/my-project-lifecycle for documentation, then suggest merging or closing the worktree

### Context Switching

When the user switches contexts mid-session:

1. Commit current work (consult @skills/my-vcs-hygiene)
2. Note the stopping point
3. Check `wt list` to see available worktrees and their activity (🤖/💬 markers)
4. Ask whether to stay in the current worktree or switch
5. If switching, prefer `/wt-switch-create <branch>` for a quick create+switch, or switch to an existing worktree
6. When returning, read the previous summary to resume context

## Parallel Work with Subagents

For large or complex tasks, spawn parallel Pi subagents in isolated worktrees:

### When to Spawn Parallel Agents

- **Scale signal**: "50+ files", "refactor everything", "whole codebase"
- **Complexity signal**: "explore first, then build", multi-domain task
- **Independence**: Work can be split into non-overlapping chunks

### Spawning Pattern

1. **Break the task** into 2–4 independent chunks
2. **Pre-check `wt list`** — avoid colliding with existing active worktrees (🤖 markers)
3. **Spawn subagents** using the `spawn_worktree_agent` tool:
   ```json
   {
     "branch": "scout-auth",
     "task": "Explore the auth module. Return a summary of current flow, files, and dependencies."
   }
   ```
4. **Each subagent runs in its own worktree** with isolated context
5. **Collect results** from each subagent's output
6. **Integrate** findings in the parent session

### Coordination

- Use `wt list` to monitor which worktrees are active (🤖 = working, 💬 = idle)
- Use `/wt-statusline-refresh` for an up-to-date footer
- Herdr users: each subagent can run in its own tab/pane via `/wt-switch-create`

## Relationship to Other Skills

| Skill | Responsibility |
|-------------------|---------------|
| **my-workflow** (this) | Worktrees, direction, naming, session boundaries, parallel coordination |
| **my-vcs-hygiene** | Commit discipline, user-initiated VCS, implicit signals, branch-from-main, amend safety, monorepo commits, visual iteration |
| **my-project-lifecycle** | Plan → Build → Review → Document → Ship, when to review, post-build docs, skill self-improvement |
| **worktrunk** | `wt` CLI commands, hooks, config, troubleshooting |
| **my-team-orchestrate** | Multi-agent delegation patterns (scout→planner→worker, expert panel, etc.) |
| **pi-worktrunk-bridge** | Activity tracking, `/wt-switch-create`, statusline, `spawn_worktree_agent` tool |
| **herdr** | Workspace/tab/pane management when running inside herdr |
| **my-semantic-release** | Release workflows when a worktree is ready to merge |

## Examples

### Good Direction Check

User: "Let's add OAuth login."
Agent (current worktree: `fix-auth-timeout`): "This is related to auth but a new feature. Continue in `fix-auth-timeout` or spawn a new worktree?"

### Good Commit Timing

Agent: "About to delete the old auth module. Committing current progress first." → consults @skills/my-vcs-hygiene

### Good Naming Hygiene

Agent: "This worktree started as `ui-tweaks` but we're now rebuilding the component library. Rename to `rebuild-component-lib`?"

### Bad: Silent Switch

Agent switches to a new worktree without asking. ❌ Always ask first.

## Decision Tree

```
Task diverges from current worktrunk?
├── Yes → Ask user: "Switch worktrees with /wt-switch-create?"
│         ├── User says yes → /wt-switch-create <branch> (or wt switch)
│         └── User says no → Continue, note divergence
└── No → Continue in current worktree

Task is large/complex/parallelizable?
├── Yes → Propose parallel subagents (spawn_worktree_agent)
│         ├── User says yes → Spawn 2–4 agents in worktrees, coordinate
│         └── User says no → Continue solo in current worktree
└── No → Continue solo

About to make large/irreversible change?
├── Yes → Consult @skills/my-vcs-hygiene — commit first
└── No → Proceed

Worktree name no longer fits?
├── Yes → Propose rename, wait for approval
└── No → Leave as-is

Need to check what other worktrees are active?
├── Yes → Run /wt-list or check footer statusline
└── No → Proceed
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| User says "just commit it" but worktree is wrong | Commit in current worktree (consult @skills/my-vcs-hygiene), then suggest switching for next task |
| User wants to rename worktree mid-session | Save state, rename, restore — or finish current work then rename |
| Multiple worktrees with similar names | Use `wt list` to disambiguate; propose clearer naming |
| User asks to "go back to previous task" | Check `wt list` for recent worktrees, ask which one to resume |
| Worktree name too long | Keep under 30 chars; use abbreviations: `refactor-auth` not `refactor-authentication-system` |
| Stale 🤖 marker in `wt list` | Run `wt config state marker clear` to remove it |
| `/wt-switch-create` didn't relaunch Pi | Check multiplexer (tmux/Zellij/herdr). Without one, `cd` into the worktree path and restart Pi manually |
| `spawn_worktree_agent` returned no output | Check `wt list` to confirm worktree exists; verify the subagent completed |
| Footer statusline is outdated | Run `/wt-statusline-refresh` to force a cache refresh |

## Common Mistakes

❌ **Wrong:** Switching worktrees without asking the user first
✅ **Right:** Always ask: "This is a new direction. Switch to a new worktree?"

❌ **Wrong:** Letting the user work in a misleadingly named worktree
✅ **Right:** Propose renaming when work evolves away from the original name

❌ **Wrong:** Ending a session without committing WIP
✅ **Right:** Always commit before ending, even if the commit message is "WIP" — consult @skills/my-vcs-hygiene

❌ **Wrong:** Using generic worktree names like `wip`, `temp`, `stuff`
✅ **Right:** Use specific kebab-case names: `fix-auth-timeout-5min`

## Related Skills

- **@skills/my-vcs-hygiene** — Commit/push discipline, branch-from-main, amend safety, visual iteration
- **@skills/my-project-lifecycle** — Plan → Build → Review → Document → Ship
- **@skills/worktrunk** — `wt` CLI commands, hooks, config, troubleshooting
- **@skills/my-semantic-release** — Release workflows when a worktree is ready to merge
- **@skills/my-code-review** — Reviewing changes before committing in a worktree

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 2.0
- **Update notes:** Refactored into focused core orchestration skill. Extracted all VCS content to @skills/my-vcs-hygiene and all lifecycle content to @skills/my-project-lifecycle. This skill now covers worktrees, direction, naming, session boundaries, and parallel agents only.
