---
name: my-project-lifecycle
description: |
  **ALWAYS use when:** planning a new feature or system, deciding when to code review, documenting what was built, reflecting on a completed session to improve skills, or mapping the overall flow from plan → build → review → document → ship. Use when the user asks "how should we build this?", "when should we review?", "document what we did", "reflect on the session", or "update my skills". Also use when a feature feels complete and the user needs guidance on what comes next.

  **DO NOT use for:** committing or pushing — use @skills/my-vcs-hygiene. Worktree management — use @skills/my-workflow.
---

# Project Lifecycle

Plan → Build → Review → Document → Ship.

## ⚡ Quick Start

**Starting a new feature or system?**
→ Plan first. Use @skills/grill-with-docs if the domain model is unclear or terminology needs sharpening. Otherwise, sketch the approach and start building.

**Feature feels complete?**
→ Review before shipping. Invoke @skills/my-code-review for critical paths. Fix critical findings before commit; warnings can be next commit.

**About to end session?**
→ Document what was built. Update CONTEXT.md with new terms. Create ADR if a hard-to-reverse decision was made. Write review notes if the code is significant.

**Work complete, reviewed, and documented?**
→ Ship via @skills/my-vcs-hygiene. Commit, push, suggest merge.

## Activation Condition

**This skill activates when the agent is planning, reviewing, documenting, or reflecting on work.**

Apply these rules when:
- Starting a new feature or system
- Deciding whether to plan more or start building
- A feature feels complete — what comes next?
- Determining when and what to review
- Documenting what was built (CONTEXT.md, ADRs, review notes)
- The user asks to reflect on a session or update skills

Do **not** apply these rules when:
- The user issues a VCS command → use @skills/my-vcs-hygiene
- The user asks about worktrees → use @skills/my-workflow

## Scope

This skill covers **agent behavioral rules** for:
- Project lifecycle phases (Plan → Build → Review → Document → Ship)
- When to plan vs. when to just build
- When to invoke code review and how to handle findings
- Post-build documentation (CONTEXT.md, ADRs, reviews)
- Skill self-improvement after shipping

It does **not** cover:
- Commit/push discipline → @skills/my-vcs-hygiene
- Worktree management → @skills/my-workflow

## Project Lifecycle

```
┌─────┐    ┌──────┐    ┌───────┐    ┌──────────┐    ┌─────┐
│ Plan│ → │ Build│ → │ Review│ → │ Document │ → │ Ship│
└─────┘    └──────┘    └───────┘    └──────────┘    └─────┘
```

Each phase has an exit condition. Don't skip phases unless the work is trivial.

| Phase | Exit Condition | Skip If |
|-------|---------------|---------|
| Plan | Shared understanding of domain and approach | Trivial fix (< 5 lines) |
| Build | Feature works, tests pass | — |
| Review | Critical findings fixed, warnings noted | Trivial fix |
| Document | CONTEXT.md updated, ADRs created if needed | Trivial fix |
| Ship | Committed, pushed, PR/merge suggested | — |

## Plan Phase

Decide how much planning a task needs:

| Signal | Action |
|--------|--------|
| New domain, unfamiliar terminology, cross-cutting concerns | Use @skills/grill-with-docs. Produce CONTEXT.md and ADRs before building. |
| Well-understood domain, clear scope, familiar codebase | Sketch approach in 1–2 sentences, then start building. |
| "Just fix this bug" or "update this config" | Skip planning. Go straight to Build. |

**Rule of thumb**: If you'd need to explain the domain to another developer, plan first. If the change is obvious from the codebase, build first.

## Build Phase

While building, consult @skills/my-vcs-hygiene for commit discipline and visual iteration rules.

### Build Exit Checklist

- [ ] Feature works as intended
- [ ] No obvious regressions
- [ ] Tests pass (if project has tests)
- [ ] Code is in a commitable state

If any item is missing, keep building. Don't proceed to Review with broken code.

## Review Phase

Invoke @skills/my-code-review at natural breakpoints:

| When | Why |
|------|-----|
| After completing a major feature | Catch design issues before they fossilize |
| Before shipping critical paths | Security, performance, correctness |
| When the user asks "review this" | Direct request — honor it |
| After a refactor that touched > 10 files | Refactors are review-prone |

### Handling Review Findings

| Severity | Action |
|----------|--------|
| **Critical** (security, correctness, crash) | Fix before committing. Amend or new commit. |
| **Warning** (maintainability, idioms) | Fix in next commit, or note for follow-up. |
| **Suggestion** (nice-to-have) | Optional. Mention to user, let them decide. |

**Don't let perfect be the enemy of shipped.** A warning about naming can be fixed later. A critical bug cannot.

## Document Phase

After building and reviewing, document what was built:

### CONTEXT.md

Update the glossary if the session introduced or clarified domain terms:

- New terms → add with definition
- Clarified terms → update existing definition
- Removed concepts → delete or mark deprecated

**Keep CONTEXT.md implementation-free.** It is a glossary, not a spec.

### ADRs

Create an ADR only when all three are true:

1. **Hard to reverse** — changing the decision later is costly
2. **Surprising without context** — a future reader will wonder "why?"
3. **Result of a real trade-off** — genuine alternatives existed

If any is missing, skip the ADR. Use the format from @skills/grill-with-docs.

### Review Notes

For significant features, create review artifacts:

- `review/code-review.md` — structured findings from @skills/my-code-review
- `review/ux-audit.md` — UX/usability findings (if UI involved)

These become reference material for future iterations.

## Ship Phase

Hand off to @skills/my-vcs-hygiene:

1. Commit any remaining changes
2. Push to origin
3. Summarize: "Pushed to `<branch>`. PR: `<url>`"
4. Suggest merge or next steps

## Skill Self-Improvement

After shipping, reflect on the session:

1. **What patterns emerged?** — visual iteration loops, review → fix cycles, cross-package commits
2. **What was awkward?** — Did the agent ask permission when it shouldn't? Skip a phase it shouldn't have?
3. **Update skills** — If a pattern recurs, consider updating @skills/my-workflow, @skills/my-vcs-hygiene, or this skill
4. **Save to memex** — Use `memex_retro` for atomic insights that should persist across sessions

### When to update skills

| Trigger | Action |
|---------|--------|
| Same awkward pattern in 2+ sessions | Update the relevant skill |
| User explicitly says "update my skill" | Update immediately |
| New tool or workflow adopted | Add to @skills/my-tech-stack or relevant skill |
| Skill description under-triggers | Optimize description per @skills/skill-creator |

## Examples

### Good: Plan → Build → Review → Document → Ship

1. **Plan**: Used @skills/grill-with-docs to define "Singularity" and "Health Check" for pi-event-horizon-provider. Produced CONTEXT.md and ADR-0001.
2. **Build**: Implemented async status widget. Committed via @skills/my-vcs-hygiene.
3. **Review**: Invoked @skills/my-code-review. Fixed critical feedback (try/finally, widget key, distinct glyphs).
4. **Document**: Updated CONTEXT.md with widget terminology. Created review/code-review.md and review/ux-audit.md.
5. **Ship**: User said "looking good. commit it and push" → @skills/my-vcs-hygiene executed directly. Branch created, committed, pushed.

### Good: Skipping Plan for Trivial Fix

User: "Fix the typo in the README"
Agent: No planning needed. Fixed typo. Committed directly via @skills/my-vcs-hygiene.

### Bad: Skipping Review for Major Feature

Agent ships a 500-line feature without review. ❌ Major features need review before shipping.

### Bad: Over-Documenting Trivial Changes

Agent creates an ADR for renaming a local variable. ❌ ADRs are for hard-to-reverse, surprising, trade-off decisions.

## Decision Tree

```
Starting new feature?
├── Trivial fix (< 5 lines) → Skip to Build
├── New domain or unclear terminology → Plan first (@skills/grill-with-docs)
└── Well-understood domain → Brief sketch, then Build

Feature feels complete?
├── Trivial fix → Ship directly
└── Non-trivial → Review first (@skills/my-code-review)

Review findings?
├── Critical → Fix before commit
├── Warning → Fix in next commit or note for follow-up
└── Suggestion → Optional, mention to user

About to end session?
├── Trivial fix → Commit and end
└── Non-trivial → Document first, then commit and end
```

## Related Skills

- **@skills/my-workflow** — Worktrees, direction, naming, session boundaries, parallel agents
- **@skills/my-vcs-hygiene** — Commit/push discipline, branch-from-main, amend safety, visual iteration
- **@skills/grill-with-docs** — Stress-test plans against domain model, produce CONTEXT.md and ADRs
- **@skills/my-code-review** — Research-backed code review before shipping
- **@skills/my-semantic-release** — Release workflows when a worktree is ready to merge
- **@skills/skill-creator** — Create or optimize skills, measure performance

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.0
- **Update notes:** New skill extracted from my-workflow v1.6 patterns. Covers the Plan → Build → Review → Document → Ship lifecycle, review timing, post-build documentation, and skill self-improvement based on observed session flows during pi-event-horizon-provider development.
