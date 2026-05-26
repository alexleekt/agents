---
name: my-session-retrospective
description: |
  **ALWAYS use when:** the user says "review this session", "how did we do", "assess adherence", "did we follow the workflow", or signals session completion. Also use when the user asks to evaluate skill invocation, check what skills were missed, or improve skill automatic triggering. Use at the end of any significant session (10+ turns, file mutations, or multi-phase work) to assess adherence against my-workflow, my-vcs-hygiene, my-project-lifecycle, and all other my-* skills.

  **DO NOT use for:** planning the next session — use @skills/my-project-lifecycle. Code review of output — use @skills/my-code-review.
---

# Session Retrospective

Review a completed session. Assess skill invocation, adherence, and propose improvements.

## ⚡ Quick Start

**User says "review this session" or work feels complete?**
→ Run the retrospective. It takes 30 seconds and produces actionable insight.

**Process:**
1. Gather session evidence (git diff, commits, context-mode stats, memex)
2. Score against each my-* skill
3. Flag missed invocations and adherence failures
4. Recommend skill updates

## Activation Condition

**This skill activates at session end or when the user explicitly requests a review.**

Apply these rules when:
- The user says "review this session", "how did we do", or similar
- A significant session is ending (10+ turns, file mutations, multi-phase work)
- The user asks to evaluate skill effectiveness or automatic invocation

## Scope

This skill covers:
- Skill invocation audit (what was used, what was missed)
- Workflow adherence check (did we follow my-workflow, my-vcs-hygiene, etc.)
- Automatic invocation assessment (did skills trigger when they should have?)
- Improvement recommendations (description updates, new sections, new skills)

## Retrospective Process

### 1. Gather Evidence

```bash
# Git evidence
git log --oneline -10
git diff --stat HEAD~1  # or since session start
git diff HEAD~1 --name-only

# Context-mode evidence (if available)
ctx stats

# Session memory
cd <project> && grep -E "tool|skill|invoke" ~/.pi/session.log 2>/dev/null || echo "no session log"
```

### 2. Score Against my-* Skills

For each applicable skill, answer:

| Skill | Should Have Triggered? | Did Trigger? | Adherence | Notes |
|-------|------------------------|-------------|-----------|-------|
| my-workflow | Direction assessment at start? | Yes/No | Good/Poor | |
| my-vcs-hygiene | Commits made? VCS commands given? | Yes/No | Good/Poor | |
| my-project-lifecycle | Plan/review/document phases? | Yes/No | Good/Poor | |
| my-code-review | Code reviewed before ship? | Yes/No | Good/Poor | |
| my-tech-stack | Tool decisions made? | Yes/No | Good/Poor | |
| my-context-strategy | Large outputs processed properly? | Yes/No | Good/Poor | |
| my-error-recovery | Errors handled gracefully? | Yes/No | Good/Poor | |
| my-communication-style | User feedback on verbosity? | Yes/No | Good/Poor | |
| my-decision-log | Decisions tracked? | Yes/No | Good/Poor | |
| my-agent-file-conventions | Agent files created? | Yes/No | Good/Poor | |

### 3. Identify Patterns

**Missed invocations** — skills that should have triggered but didn't:
- Why? Description too narrow? Trigger phrases missing?
- Fix: Expand description, add activation examples

**Adherence failures** — skill triggered but rules not followed:
- Example: my-vcs-hygiene triggered but branch-from-main guard skipped
- Fix: Strengthen the rule, add to Common Mistakes

**Over-invocation** — skill triggered when it shouldn't:
- Why? Description too broad? Ambiguous trigger?
- Fix: Tighten description, add "DO NOT use for" cases

### 4. Recommend Improvements

Produce a structured report:

```markdown
# Session Retrospective: <date>

## Session Summary
- Turns: ~N
- Files changed: N
- Commits: N
- Skills invoked: list

## Skill Invocation Audit
| Skill | Triggered | Should Have | Score |
|-------|-----------|-------------|-------|
| ... | ... | ... | ✅/❌ |

## Adherence Failures
1. **<Skill>** — <What went wrong>
   - **Impact**: <Why it matters>
   - **Fix**: <Specific change to skill>

## Improvement Recommendations
1. **<Skill>** — <What to change>
   - **Rationale**: <Why this helps>
   - **Priority**: High/Medium/Low

## Skill Update Candidates
- <skill>: <specific change>
```

## Continuous Improvement Loop

```
Session completed
├── Retrospective runs (this skill)
│   ├── Produces adherence report
│   └── Recommends skill updates
└── User or agent applies updates
    ├── Edit skill description (better triggers)
    ├── Add new sections (new patterns observed)
    ├── Create new skill (new domain emerges)
    └── Commit via @skills/my-vcs-hygiene
```

**Goal**: Each retrospective makes the my-* suite more accurate and more automatic.

## Examples

### Good: Retrospective after feature build

Session: Built async status widget for pi-event-horizon-provider.

Retrospective finds:
- ✅ my-project-lifecycle triggered — Plan, Build, Review, Document phases all present
- ✅ my-vcs-hygiene triggered — branch-from-main guard applied correctly
- ❌ my-context-strategy missed — processed 720-line diff with `git diff` instead of `ctx_execute`
- ❌ my-error-recovery missed — no graceful handling for fetch timeout

Recommendations:
- my-context-strategy: Add trigger for "large diff" to ctx_execute instead of read
- my-error-recovery: Add section on HTTP timeout retry patterns

### Good: Retrospective reveals under-triggering

Session: User gave visual feedback 5 times. No skill triggered for UI iteration.

Retrospective finds:
- ❌ my-vcs-hygiene under-triggered — description didn't include "move this left"

Fix: Expand description to include visual/UX feedback phrases.

## Common Mistakes

❌ **Wrong:** Running retrospective without checking git evidence
✅ **Right:** Always check git log and diff — the ground truth of what happened

❌ **Wrong:** Retrospective that only lists what went well
✅ **Right:** Focus on misses and adherence failures — that's where improvement lives

❌ **Wrong:** Recommending skill updates without specific examples from the session
✅ **Right:** Every recommendation must cite a concrete session event

## Related Skills

- **@skills/my-workflow** — What should have happened during the session
- **@skills/my-vcs-hygiene** — Commit discipline that was assessed
- **@skills/my-project-lifecycle** — Lifecycle phases that were assessed
- **@skills/skill-creator** — For implementing skill updates recommended by retrospective

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.0
