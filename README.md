# AI Agent Configuration

This directory contains configuration files that guide how AI agents (like Claude) should work with your projects.

## Directory Structure

```
agents/
├── README.md
├── config.yaml       # Saddle configuration
├── rules/            # Sync rules per tool
│   ├── claude.yaml
│   ├── codex.yaml
│   ├── copilot.yaml
│   ├── cursor.yaml
│   ├── gemini.yaml
│   └── opencode.yaml
└── skills/           # Reusable agent skills
    ├── my-agent-rules/
    └── my-tech-stack/
```

## Skills

| Skill | Use When |
|-------|----------|
| `@skills/my-tech-stack` | Recommending tools, libraries, or technologies |
| `@skills/my-agent-rules` | Creating/editing AGENT.md or agent configuration files |

## For AI Agents

When starting work on a project:

1. **Check for project-specific agent files** — Look for `AGENT.md` or `claude` files in the project root
2. **Reference tech preferences** — Consult `@skills/my-tech-stack` when making tool recommendations
3. **Follow conventions** — Consult `@skills/my-agent-rules` when creating or editing agent files

## For Users

These are living documents. Update them as your preferences and workflows evolve.