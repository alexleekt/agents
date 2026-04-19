---
name: my-agent-rules
description: |
  **PRIMARY SKILL** for creating, validating, and editing AI agent behavioral configuration files (AGENT.md, claude.md, etc.)

  **ALWAYS use when user mentions:**
  - "AGENT.md", "claude.md", "agent configuration", "agent rules", "behavioral rules"
  - Creating, editing, reviewing, or updating agent files
  - "what should go in agent files", "how to structure agent files"
  - Agent file location (where to put AGENT.md, when to use claude.md)
  - Validating agent file content
  - "difference between AGENT.md and claude.md"
  - Setting up AI agent workflows or defining how agents should behave

  **DO NOT use for:**
  - Technology/tool recommendations → use @skills/my-tech-stack
  - Version control operations → use @skills/my-jj-workflow

  **CRITICAL:** Never write or modify agent configuration files without consulting this skill first.

  This skill defines what content BELONGS in agent files (behavioral rules, workflows,
  communication style) vs what DOES NOT belong (project documentation, architecture, feature specs).
---

# Agent File Conventions

## Overview

Agent configuration files (`AGENT.md`, `claude.md`, etc.) define **behavioral rules** for AI agents — how to work with a project.

> **Note:** This is a living document. Guidelines evolve as workflows change. Check the latest version before making decisions.

## What Are Agent Files?

Agent files contain **instructions for AI agents**, not documentation for humans.

### Include: Behavioral Rules

These files should describe:

- **How to approach tasks** — workflows, priorities, and methodologies
- **Communication style** — how to interact with the user
- **Decision-making rules** — what to prioritize or avoid
- **Tool usage patterns** — when and how to use specific tools
- **Code conventions** — style preferences and patterns to follow
- **Testing requirements** — what must be run before committing
- **Approval workflows** — when to ask before proceeding

### Exclude: Project Documentation

These files should NOT contain:

- Project descriptions or overviews
- Architecture documentation
- Feature specifications
- Business logic explanations
- User-facing documentation
- API documentation
- Deployment instructions

## Quick Check

| Behavioral (✓) | Documentation (✗) |
|----------------|-------------------|
| "Always run tests before committing" | "This is a React-based dashboard" |
| "Ask before installing new dependencies" | "The app uses PostgreSQL for data storage" |
| "Use TypeScript for all new files" | "Users can create and manage projects" |
| "Prefer functional components over classes" | "The backend exposes a REST API" |

## The Rule

> **If it describes what the project is** → belongs elsewhere (README, docs/, Architecture.md)
> **If it describes how the agent should behave** → belongs here

## File Locations

### AGENT.md
- **Location:** Repository root
- **Scope:** Applies to the entire project
- **Use for:** Project-wide behavioral rules, coding standards, workflows

### claude.md
- **Location:** `.agent/` directory (e.g., `.agent/claude.md`)
- **Scope:** Applies to specific contexts or subdirectories
- **Use for:** Nested rules, specific workflow contexts, subdirectory-specific behaviors
- **Note:** Can have multiple claude.md files in different `.agent/` directories

## Creating Agent Files

### AGENT.md Template

```markdown
# Agent Guidelines

## Communication Style
- Be direct and to the point
- Ask clarifying questions when requirements are unclear
- Always run lint/typecheck commands after making changes

## Code Conventions
- Follow existing code conventions in the project
- Use TypeScript for all new files
- Prefer functional components over classes

## Workflow Rules
- Always run tests before committing
- Ask before installing new dependencies
- Never commit changes unless explicitly asked

## Tool Usage
- When editing files, use the Edit tool for precise changes
- When searching, prefer grep over manual file reading
- Use glob patterns for file discovery
```

### claude.md Template (for specific contexts)

```markdown
# Agent Guidelines: [Context Name]

## Scope
These rules apply to: `src/frontend/`

## Special Rules
- Use React functional components
- Run `npm run lint` after JS/TS changes
- Always test responsive behavior
```

## Common Mistakes to Avoid

1. **Writing project documentation in AGENT.md** → Move to README.md
2. **Being too vague** → Be specific: "Always run X" not "Consider running X"
3. **Forgetting file location rules** → AGENT.md in root, claude.md in .agent/
4. **Including feature specs** → Those belong in issues or docs/
5. **Not updating when workflows change** → Treat as living document

## Versioning

- **Last updated:** 2024-01-XX
- **Version:** 1.0
- **Update notes:** Initial conventions

## Examples

### Good Content

```markdown
## Git Workflow
ALWAYS run these commands in order before committing:
1. `npm run lint` - Check for style issues
2. `npm run typecheck` - Verify TypeScript
3. `npm test` - Run test suite

Never use `git push --force` on main branch.
```

### Bad Content

```markdown
## Project Overview
This is a SaaS application for project management.
Built with React and Node.js, it helps teams collaborate.

## Features
- User authentication
- Project creation
- Task management
```

(The above belongs in README.md, not AGENT.md)

## Decision Tree

When deciding what goes in an agent file, ask:

1. **Does this tell the agent HOW to work?** → Yes, include it
2. **Does this describe WHAT the project is?** → No, put it elsewhere
3. **Is this for AI agent behavior or human understanding?** → Only agent behavior belongs here
4. **Would this change if we switched AI agents?** → If yes, it's behavioral

## Skill Naming Conventions

When creating or naming skill files (SKILL.md), follow these naming patterns:

### Personal Skills
Skills that define personal preferences and conventions should be prefixed with `my-`:

| Pattern | Example | Purpose |
|---------|---------|---------|
| `my-tech-stack` | Technology preferences, tool choices | Personal technology stack and preferences |
| `my-agent-conventions` | Agent behavioral rules | How agents should behave and work |
| `my-workflow` | Personal workflows | Custom workflows and processes |

### General Skills
Skills that are reusable across projects or users should use descriptive names without the `my-` prefix:

| Pattern | Example | Purpose |
|---------|---------|---------|
| `skill-creator` | Creating new skills | Tool for generating skill files |
| `find-skills` | Skill discovery | Locating and listing available skills |

### Directory Naming
Skill directories should match the skill name:
- `skills/my-tech-stack/SKILL.md` → name: `my-tech-stack`
- `skills/my-agent-conventions/SKILL.md` → name: `my-agent-conventions`

## Related Files

- Project overview → `README.md`
- Architecture → `docs/architecture.md` or `ARCHITECTURE.md`
- API docs → `docs/api.md` or inline code comments
- Feature specs → Issues, PRs, or `docs/features/`
- User docs → `docs/user/` or separate documentation site
