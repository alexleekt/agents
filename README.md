# AI Assistant Configs

Centralized configuration for AI coding assistants, synced across multiple tools using [Saddle](https://saddle.sh/).

## Tools Supported

- [OpenCode](https://opencode.ai/)
- [Claude Code](https://claude.ai/code)
- [Codex](https://github.com/openai/codex)
- [Cursor](https://cursor.com/)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [GitHub Copilot](https://github.com/features/copilot)

## Quick Start

### Initial Setup

1. Source the environment setup:
```bash
source ~/agents/setup.sh
```

2. Add to your shell profile (`.zshrc`, `.bashrc`, etc.):
```bash
echo 'source ~/agents/setup.sh' >> ~/.zshrc
```

3. Preview what will be synced:
```bash
saddle --dry-run --all
```

4. Apply the configuration:
```bash
saddle --yes --all
```

5. Check sync status:
```bash
saddle --check
```

## Directory Structure

```
~/agents/
├── config.yaml              # Main Saddle configuration
├── setup.sh                 # Environment setup script
├── README.md                # This file
├── agents/                  # Agent definitions (AGENTS.md)
│   └── opencode/
│       └── AGENTS.md
├── commands/                # Slash commands
│   └── opencode/
├── configurations/          # Tool-specific configs
│   └── opencode/
│       └── opencode.jsonc
├── rules/                   # Saddle rule files
│   ├── opencode.yaml
│   ├── claude.yaml
│   ├── codex.yaml
│   ├── cursor.yaml
│   ├── gemini.yaml
│   └── copilot.yaml
└── skills/                  # Reusable AI skills
    └── <skill-name>/
        └── SKILL.md
```

## Configuration Files

### `config.yaml`

Main Saddle configuration defining the source root and global settings.

### Rule Files (`rules/*.yaml`)

Each tool has a rule file that defines:
- Which files/directories to sync
- Source locations in this repo
- Target locations in the tool's config directory
- Mapping types (file, directory, skills)

### Skills

Reusable AI capabilities organized by function. Each skill is a directory containing a `SKILL.md` file with:
- Description of the capability
- When to use it
- Usage instructions
- Examples

## Usage

### Adding a New Skill

1. Create a new directory in `skills/`:
```bash
mkdir skills/my-new-skill
cat > skills/my-new-skill/SKILL.md << 'EOF'
# My New Skill

## Description
What this skill does...

## When to Use
- Use case 1
- Use case 2

## Instructions
How to use this skill...
EOF
```

2. Sync to all tools:
```bash
saddle --yes --all
```

### Adding Tool-Specific Commands

1. Create command file:
```bash
mkdir -p commands/opencode
cat > commands/opencode/my-command.md << 'EOF'
# /my-command

Description of what this command does.

## Usage
/my-command <args>

## Examples
/my-command example1
/my-command example2
EOF
```

2. Run Saddle:
```bash
saddle --yes --all
```

### Customizing Agent Behavior

Edit `agents/<tool>/AGENTS.md` to customize agent instructions for each tool.

## Commands

| Command | Description |
|---------|-------------|
| `saddle --dry-run --all` | Preview changes without applying |
| `saddle --yes --all` | Apply all configurations |
| `saddle --check` | Verify sync status |
| `saddle --list` | Show available profiles |
| `saddle --uninstall` | Remove all symlinks |

## Environment Variables

| Variable | Description | Value |
|----------|-------------|-------|
| `SADDLE_DIR` | Base config directory | `~/git/agents` |
| `SADDLE_CONFIG` | Path to config file | `~/agents/config.yaml` |
| `SADDLE_RULES_DIR` | Path to rules directory | `~/agents/rules` |

These are set automatically when you source `setup.sh`.

## Checking Sync Status

Verify everything is in sync:
```bash
saddle --check
```

This will report how many symlinks are in sync and flag any that need attention.

## Best Practices

1. **Edit in one place** - Always edit files in `~/agents/`, never in individual tool directories
2. **Use version control** - Track this directory in git for backup and sharing
3. **Test changes** - Use `--dry-run` before applying changes
4. **Keep skills focused** - Each skill should do one thing well
5. **Document everything** - Add clear descriptions and usage examples

## Troubleshooting

### Sync shows "out of sync"

Run `saddle --yes --all` to re-apply symlinks.

### Tool not detected

Ensure the tool is installed and its binary is in your PATH.

### Permission errors

Saddle only creates symlinks, so it doesn't need special permissions. If you see permission errors, check that target directories exist and are writable.

## License

MIT - See individual skill directories for their specific licenses.
