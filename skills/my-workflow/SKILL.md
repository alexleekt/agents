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

**Significant code change or irreversible file action?**
→ Make a commit first. Prefer small, focused commits.

**Worktree name no longer describes the work?**
→ Propose renaming it to match the actual direction.

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
   - "This seems like a new direction from `<current-worktree>`. Switch to a new worktree?"
   - Let the user decide. Do not switch unilaterally.

3. **When the user explicitly says "let's work on X"**
   - If X clearly differs from the current worktrunk's scope, propose switching.
   - If related, continue but note: "Continuing in `<worktree>` — say 'new worktree' if you want separation."

### Examples

| Situation | Action |
|-----------|--------|
| User asks to fix a bug in feature branch | Continue in current worktree |
| User asks to start an unrelated refactor | Ask: "New worktree for this?" |
| User asks to review a different PR | Ask: "Switch worktrees?" |
| Task evolved away from original intent | Propose renaming or switching |

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
3. Ask whether to stay in the current worktree or switch
4. When returning, read the previous summary to resume context

## Relationship to Other Skills

| Skill | Responsibility |
|-------|---------------|
| **my-workflow** (this) | When to use worktrunks, commit discipline, naming hygiene |
| **worktrunk** | How to run `wt` commands, hooks, config, troubleshooting |
| **my-semantic-release** | Release workflows, versioning, changelog generation |
| **my-team-orchestrate** | Multi-agent delegation, parallel work, team spawning |

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
├── Yes → Ask user: "Switch worktrees?"
│         ├── User says yes → Switch (use @skills/worktrunk)
│         └── User says no → Continue, note divergence
└── No → Continue in current worktree

About to make large/irreversible change?
├── Yes → Commit first
└── No → Proceed

Worktree name no longer fits?
├── Yes → Propose rename, wait for approval
└── No → Leave as-is
```

## Versioning

- **Last updated:** 2026-05-21
- **Version:** 1.0
- **Update notes:** Initial workflow discipline rules
