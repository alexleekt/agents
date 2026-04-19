# AI Agent Skills Repository

This directory contains **skills** that guide how AI agents work with your projects. Skills are modular, reusable expertise modules that agents consult automatically based on triggers.

## Directory Structure

```
agents/
├── README.md           # This file
├── AGENTS.md           # Skill creation and management guidelines
├── skills/             # Personal skills (JJ-tracked)
│   ├── my-agent-rules/
│   ├── my-code-review/
│   ├── my-crawl4ai/
│   ├── my-jj-workflow/
│   ├── my-semantic-release/
│   ├── my-team-orchestrate/
│   └── my-tech-stack/
└── .pi/
    ├── agents/         # Agent definitions for teams
    └── teams.yaml      # Predefined team templates
```

## Skills Overview

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `my-agent-rules` | "AGENT.md", "claude.md", "agent configuration" | Creating/editing agent behavioral config files |
| `my-code-review` | "code review", "PR review", "check my code" | Research-based code quality reviews |
| `my-crawl4ai` | "crawl4ai", "web scraping", "scrape data" | Web crawling with crawl4ai |
| `my-jj-workflow` | "jj", "jujutsu", "commit" (without git) | Daily version control with jj |
| `my-semantic-release` | "release", "changelog", "semver" | Semantic versioning and release workflows |
| `my-team-orchestrate` | "start a team", "delegate", "50+ files" | Multi-agent delegation patterns |
| `my-tech-stack` | "what should I use", "bun or node" | Preferred tools and technology recommendations |

## For AI Agents

When starting work:

1. **Check for project-specific agent files** — Look for `AGENT.md` or `claude.md` in the project root
2. **Use skill references** — Consult `@skills/my-tech-stack` for tool recommendations, `@skills/my-agent-rules` for agent file creation
3. **Skills auto-load** — Pi reads from `~/.agents/skills/` (symlinked from this directory)

## For Users

- **Adding skills:** See `AGENTS.md` for skill creation workflow
- **Updating skills:** Edit files in `skills/<skill-name>/SKILL.md`, changes auto-commit via chezmoi
- **Distributing:** Skills are symlinked to `~/.agents/skills/` for Pi and `~/.claude/skills/` for Claude Code

## Legacy Note

Previous `conventions/agent-conventions.md` and `preferences/tech-preferences.md` have been superseded by `my-agent-rules` and `my-tech-stack` skills respectively. The legacy files are preserved in git history but removed from the working tree.
