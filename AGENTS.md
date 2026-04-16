# Agent Guidelines: Saddle Skills Repository

## Scope
These rules apply when working in the `~/agents/` directory and its subdirectories.

## Environment Awareness

### Directory Structure
- `SADDLE_DIR` = `~/agents` (this repository root)
- `SADDLE_CONFIG` = `~/agents/config.yaml`
- `SADDLE_RULES_DIR` = `~/agents/rules`
- Skills live in `~/agents/skills/<skill-name>/SKILL.md`

### Skills System
- Skills are managed by `saddle` (symlink manager for AI skills)
- Each skill is a directory containing `SKILL.md`
- Skills are registered via symlinks for agent discovery

## Workflow Rules

### After Modifying Any Skill
**ALWAYS run:**
```bash
saddle --all
```
This registers all skills by creating/updating symlinks.

### Creating New Skills
1. Create directory: `mkdir -p skills/<skill-name>`
2. Write `skills/<skill-name>/SKILL.md`
3. Run `saddle --all` to register

### Skill Naming Conventions
- Personal conventions: `my-<thing>` (e.g., `my-tech-stack`)
- General tools: descriptive name (e.g., `skill-creator`)

### Configuration Files
- `config.yaml` — Saddle main configuration
- `installed.json` — Tracks registered skills
- `rules/` — Custom agent behavioral rules

## Communication Style
- When suggesting new skills, check `skills/` for existing patterns
- Prefer skill-based workflows over one-off shell scripts
- Document skill purposes clearly in SKILL.md frontmatter
