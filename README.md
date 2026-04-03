# AI Agent Configuration

Centralized configuration for AI coding agents, managed by [Saddle](https://saddle.sh/). This repository serves as the single source of truth for agent behaviors.

## Quick Start

```bash
# Source the environment
source setup.sh

# Sync all configurations to tools
saddle --all
```

## Structure

```
.
├── config.yaml       # Saddle configuration
├── setup.sh          # Environment setup script
├── rules/            # Sync rules per tool
│   ├── claude.yaml
│   ├── codex.yaml
│   ├── copilot.yaml
│   ├── cursor.yaml
│   ├── gemini.yaml
│   └── opencode.yaml
├── skills/           # Reusable agent skills
│   ├── my-agent-rules/
│   └── my-tech-stack/
└── README.md         # This file
```

## Supported Tools

| Tool | Sync Method | Status |
|------|-------------|--------|
| Claude Code | Saddle | ✓ |
| OpenCode | Saddle | ✓ |
| Codex | Saddle | ✓ |
| Cursor | Saddle | ✓ |
| Gemini | Saddle | ✓ |
| Copilot | Saddle | ✓ |
| Pi | Dotfiles hook | ✓ (via `~/dotfiles/scripts/run_after_apply_50-pi-skills.sh`) |

## Workflow

1. **Create/edit skills in `skills/`** — Skills are the canonical source for agent behaviors
2. **Sync to tools** — Run `saddle --all` to distribute to all tools
3. **Never edit tool directories directly** — Changes there will be overwritten

### Pi Note

Pi is handled separately via the dotfiles chezmoi hook (`run_after_apply_50-pi-skills.sh`), which symlinks skills from `~/agents/skills/` to `~/.pi/agent/skills/`. Run `chezmoi apply` to sync Pi skills.

## Available Skills

| Skill | Use When |
|-------|----------|
| `@skills/my-agent-rules` | Creating/editing AGENT.md or agent configuration files |
| `@skills/my-tech-stack` | Recommending tools, libraries, or technologies |
