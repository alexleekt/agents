# AI Assistant Configs

Manage all your AI coding assistant configurations in one place. This repository centralizes settings, skills, and behaviors across multiple tools using [Saddle](https://saddle.sh/) for seamless syncing.

## What This Does

- **One source of truth** for AI assistant configurations
- **Automatic syncing** across OpenCode, Claude, Codex, Cursor, Gemini, and Copilot
- **Reusable skills** that work across all supported tools
- **Version controlled** configurations you can track, share, and rollback

## Quick Start

```bash
# Set up the environment
source ~/agents/setup.sh

# Preview what will change
saddle --dry-run --all

# Apply to all tools
saddle --yes --all

# Check sync status anytime
saddle --check
```

To make this permanent, add to your shell profile:
```bash
echo 'source ~/agents/setup.sh' >> ~/.zshrc
```

## Repository Structure

```
~/agents/
├── skills/              # Reusable AI capabilities
│   ├── agent-conventions/   # Guidelines for creating AGENT.md files
│   └── tech-advisor/        # Technology preferences
├── agents/              # Tool-specific agent instructions
├── commands/            # Slash commands for assistants
├── configurations/      # Tool-specific settings
└── rules/               # Saddle sync rules
```

## Adding New Skills

Skills are reusable AI capabilities that work across all tools:

```bash
# Create the skill
mkdir skills/my-skill
cat > skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: |
  What this skill does and when to use it.
  
  ALWAYS use this skill when:
  - User asks about X
  - User needs help with Y
---

# Skill instructions here
EOF

# Sync to all tools
saddle --yes --all
```

## Key Concepts

### Skills
Reusable AI instructions organized by purpose. Each skill lives in `skills/<name>/SKILL.md` and automatically syncs to all supported tools.

### Agent Instructions
Tool-specific behavioral rules in `agents/<tool>/AGENTS.md`. Customize how each AI assistant behaves.

### Saddle
The sync tool that keeps configurations consistent across all your AI assistants. Changes made here are automatically reflected in each tool's config directory.

## Common Tasks

| Task | Command |
|------|---------|
| See what will change | `saddle --dry-run --all` |
| Apply changes | `saddle --yes --all` |
| Check sync status | `saddle --check` |
| List available tools | `saddle --list` |

## Supported Tools

- [OpenCode](https://opencode.ai/)
- [Claude Code](https://claude.ai/code)
- [Codex](https://github.com/openai/codex)
- [Cursor](https://cursor.com/)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [GitHub Copilot](https://github.com/features/copilot)

## Contributing

1. Edit files in this repository only
2. Never edit files directly in tool config directories
3. Use `saddle --dry-run` to preview changes before applying
4. Commit and push changes to share them

## Learn More

- [Saddle documentation](https://saddle.sh/)
- Agent instructions: `agents/opencode/AGENTS.md`
- Available skills: `skills/*/SKILL.md`
