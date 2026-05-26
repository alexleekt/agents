---
name: my-decision-log
description: |
  **ALWAYS use when:** a significant decision is made during a session (tool choice, architecture direction, library selection, workflow change, or approach pivot). Use when the user asks "why did we do X?", "document this decision", "what did we decide about Y?", or when creating ADRs. Also use proactively when a decision has trade-offs, is hard to reverse, or will affect future work. Track decisions with rationale so future sessions (or other agents) can understand the reasoning without re-deriving it.

  **DO NOT use for:** trivial decisions (variable names, formatting). Committed decisions with no trade-offs. Immediate technical fixes with obvious solutions.
---

# Decision Log

Track session decisions, rationale, and consequences.

## ⚡ Quick Start

**Making a decision with trade-offs?**
→ Log it. Future you (or another agent) will thank you.

**User asks "why did we do X?"**
→ Check the decision log. If missing, reconstruct and log it.

## What to Log

Log decisions that meet any of these criteria:

| Criterion | Example |
|-----------|---------|
| **Trade-offs exist** | "Used fetch over axios — zero deps vs richer API" |
| **Hard to reverse** | "Switched from jj to git — migration required" |
| **Affects future work** | "Split my-workflow into 3 skills — all AGENTS.md files need updates" |
| **Non-obvious** | "Dummy API key is intentional — proxy handles auth" |
| **User-overridden default** | "User chose Z over recommended Y" |

Skip trivial decisions:
- Variable naming
- Formatting choices
- Standard library usage
- Obvious fixes

## Log Format

Each decision entry:

```markdown
## <Decision Title>

**Date:** YYYY-MM-DD
**Context:** <What problem we were solving>
**Decision:** <What we chose>
**Alternatives considered:** <What we rejected and why>
**Rationale:** <Why this choice wins>
**Consequences:** <What this enables or constrains>
**Reversibility:** <Easy / Medium / Hard>
**Related:** <Links to ADRs, skills, memex cards>
```

## Where to Store

| Location | When to Use |
|----------|-------------|
| **Session memory** (ctx_search) | Decisions during active session — auto-captured |
| **Memex** (memex_retro) | Cross-session insights, atomic learnings |
| **ADR** (docs/adr/) | Hard-to-reverse architectural decisions |
| **CONTEXT.md** | Domain terminology and glossary updates |
| **Skill update** (SKILL.md) | Workflow or behavioral decisions that affect agent behavior |

## Decision Lifecycle

```
Decision made
├── Log immediately → session memory
├── If cross-session → memex_retro
├── If architectural → ADR
├── If domain term → CONTEXT.md
└── If behavioral → update relevant SKILL.md
```

## Retrospective Decision Recovery

When a decision wasn't logged and the user asks about it later:

1. **Reconstruct from git history** — `git log`, commits, PRs
2. **Reconstruct from session memory** — ctx_search for related terms
3. **Ask user for confirmation** — "My reconstruction: we chose X because Y. Is that right?"
4. **Log the recovered decision** — prevent future ambiguity

## Examples

### Good: Tool choice decision

```markdown
## Use yaml package for config parsing

**Date:** 2026-05-20
**Context:** Need to parse event-horizon instances.yaml in pi-event-horizon-provider
**Decision:** Use `yaml` npm package
**Alternatives considered:**
- js-yaml — popular but no anchor/comment support needed
- Native JSON.parse — instances.yaml uses YAML features
**Rationale:** yaml package handles full YAML spec including quoted strings, anchors, comments. Matches user's existing yaml files.
**Consequences:** Adds one dependency. Future configs can use advanced YAML features.
**Reversibility:** Easy — swap parser if needed
```

### Good: Architecture decision

```markdown
## Split my-workflow into 3 composable skills

**Date:** 2026-05-26
**Context:** my-workflow v1.6 was 490 lines, approaching 500-line limit. Adding 6 new sections would bloat it.
**Decision:** Extract VCS content to my-vcs-hygiene and lifecycle content to my-project-lifecycle
**Alternatives considered:**
- Keep monolithic — simpler but 620+ lines hurts triggering
- Split into 5+ skills — too granular, hard to discover
**Rationale:** Three skills with distinct triggers (orchestration, VCS, lifecycle) matches skill-separation-of-concerns principle. Each < 360 lines.
**Consequences:** All AGENTS.md files need reference updates. Users must learn 3 skill names.
**Reversibility:** Medium — can merge back but loses trigger precision
**Related:** ADR in agents repo, memex card skill-composability-workflow-split
```

### Bad: Unlogged decision

Agent chose `setWidget` over `notify` for UI without logging why. Future agent tries `notify`, wastes time debugging. ❌ Always log non-obvious choices.

## Common Mistakes

❌ **Wrong:** Logging every tiny choice — noise drowns signal
✅ **Right:** Log only decisions with trade-offs, reversibility concerns, or future impact

❌ **Wrong:** Logging only in session chat — lost after compaction
✅ **Right:** Persistent storage: memex for cross-session, ADR for architecture

❌ **Wrong:** Reconstructing decisions from memory without verification
✅ **Right:** Reconstruct, then confirm with user or git history

## Related Skills

- **@skills/my-project-lifecycle** — Document phase produces ADRs and CONTEXT.md
- **@skills/my-session-retrospective** — Assesses whether key decisions were logged
- **@skills/grill-with-docs** — Produces ADRs for hard-to-reverse decisions

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.0
