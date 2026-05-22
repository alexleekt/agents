---
name: my-workflow
description: |
  **ALWAYS use when:** assessing task direction, deciding whether to stay in the
  current worktrunk or switch; making commits; performing large or irreversible
  file actions; updating worktree names to match evolving work.

  **DO NOT use for:** `wt` CLI mechanics, hooks, or config — use @skills/worktrunk.

  Guides agent behavioral discipline around idea separation, commit timing,
  and worktree hygiene. Conservative by default: ask before switching.
---

# Personal Workflow Discipline

How the agent should manage worktrunks, commits, and context while working.

> **Note:** This is a living document. Workflows evolve. Check the latest version
> before making decisions.

## ⚡ Quick Start

**Task doesn't match the current worktrunk?**
→ Ask the user before switching or spawning a new worktree.
→ If the user approves, prefer `/wt-switch-create <branch>` to create, switch, and relaunch in one step.

**Significant code change or irreversible file action?**
→ Make a commit first. Prefer small, focused commits.

**Worktree name no longer describes the work?**
→ Propose renaming it to match the actual direction.

**Need parallel agents for a large task?**
→ Use `spawn_worktree_agent` to create isolated worktrees with subagents, or `/wt-switch-create` to open additional Pi sessions in new worktrees.

## Activation Condition

**This skill activates only when the agent is performing file-mutating operations.**

Apply these rules when:
- Creating, editing, deleting, or renaming files
- Running commands that modify the working tree (install, scaffold, generate)
- Performing any non-temporary file action

Do **not** apply these rules when:
- Reading or analyzing code (explain, review, search)
- Answering questions about the codebase
- Any purely read-only interaction

## Scope

This skill covers **agent behavioral rules** for:
- Direction assessment (does the task fit the current worktrunk?)
- Commit discipline (when and why to commit)
- Worktree naming hygiene (keeping names accurate)
- Session boundaries (end-of-session rituals, context switching)

It does **not** cover:
- `wt` CLI commands or syntax → see @skills/worktrunk
- Hook configuration or project automation → see @skills/worktrunk
- Commit message generation → see @skills/worktrunk

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

## Commit Discipline

Make commits **early and often**. Prefer small, focused commits over large bundles.

### Must Commit Before

- Large file moves, deletions, or renames
- Irreversible operations ( destructive edits, schema changes )
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

## Session Boundaries

### Starting a Session

1. Check the current worktrunk name and purpose
2. Confirm with the user if the task fits
3. If no worktrunk exists and the task is non-trivial, suggest creating one

### Ending a Session

1. **Commit any uncommitted work** — even if WIP
2. Summarize what was done and what's left
3. Note the current worktrunk name for next time
4. If the work is complete, suggest merging or closing the worktree

### Context Switching

When the user switches contexts mid-session:

1. Commit current work (WIP is fine)
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

| Skill / Extension | Responsibility |
|-------------------|---------------|
| **my-workflow** (this) | When to use worktrunks, commit discipline, naming hygiene, parallel coordination |
| **worktrunk** | How to run `wt` commands, hooks, config, troubleshooting |
| **my-team-orchestrate** | Multi-agent delegation patterns (scout→planner→worker, expert panel, etc.) |
| **pi-worktrunk-bridge** | Activity tracking, `/wt-switch-create`, statusline, `spawn_worktree_agent` tool |
| **herdr** | Workspace/tab/pane management when running inside herdr |
| **my-semantic-release** | Release workflows when a worktree is ready to merge |

## Examples

### Good Direction Check

User: "Let's add OAuth login."
Agent (current worktree: `fix-auth-timeout`): "This is related to auth but a new feature. Continue in `fix-auth-timeout` or spawn a new worktree?"

### Good Commit Timing

Agent: "About to delete the old auth module. Committing current progress first."

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
├── Yes → Commit first
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
| User says "just commit it" but worktree is wrong | Commit in current worktree, then suggest switching for next task |
| User wants to rename worktree mid-session | Save state, rename, restore — or finish current work then rename |
| Multiple worktrees with similar names | Use `wt list` to disambiguate; propose clearer naming |
| User asks to "go back to previous task" | Check `wt list` for recent worktrees, ask which one to resume |
| Commit fails due to untracked files | Stage with `git add .` or `git add -p` for selective staging |
| Worktree name too long | Keep under 30 chars; use abbreviations: `refactor-auth` not `refactor-authentication-system` |
| Stale 🤖 marker in `wt list` | Run `wt config state marker clear` to remove it |
| `/wt-switch-create` didn't relaunch Pi | Check multiplexer (tmux/Zellij/herdr). Without one, `cd` into the worktree path and restart Pi manually |
| `spawn_worktree_agent` returned no output | Check `wt list` to confirm worktree exists; verify the subagent completed |
| Footer statusline is outdated | Run `/wt-statusline-refresh` to force a cache refresh |

## Common Mistakes

❌ **Wrong:** Switching worktrees without asking the user first
✅ **Right:** Always ask: "This is a new direction. Switch to a new worktree?"

❌ **Wrong:** Committing after every tiny tweak (whitespace, typo)
✅ **Right:** Batch trivial fixes; commit on logical units or before irreversible actions

❌ **Wrong:** Letting the user work in a misleadingly named worktree
✅ **Right:** Propose renaming when work evolves away from the original name

❌ **Wrong:** Ending a session without committing WIP
✅ **Right:** Always commit before ending, even if the commit message is "WIP"

❌ **Wrong:** Using generic worktree names like `wip`, `temp`, `stuff`
✅ **Right:** Use specific kebab-case names: `fix-auth-timeout-5min`

## Related Skills

- **@skills/worktrunk** — For `wt` CLI commands, hooks, config, troubleshooting
- **@skills/my-semantic-release** — For release workflows when a worktree is ready to merge
- **@skills/my-team-orchestrate** — For spawning agents in parallel worktrees
- **@skills/my-code-review** — For reviewing changes before committing in a worktree

## Versioning

- **Last updated:** 2026-05-22
- **Version:** 1.1
- **Update notes:** Integrated `pi-worktrunk-bridge` extension patterns: `/wt-switch-create`, `spawn_worktree_agent`, `wt list` coordination, statusline awareness, and parallel subagent workflows.
