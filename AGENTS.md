# Agent Guidelines: Saddle Skills Repository

## Scope
These rules apply when working in the `~/agents/` directory and its subdirectories.

## Environment Awareness

### Directory Structure
- `AGENTS_DIR` = `~/agents` (this repository root)
- Skills live in `~/agents/skills/<skill-name>/SKILL.md`
- Agent definitions live in `~/agents/.pi/agents/`
- Team templates live in `~/agents/.pi/teams.yaml`

### Skills System
- Each skill is a directory containing `SKILL.md`
- Skills are distributed via symlinks for agent discovery (Claude Code)
- Pi reads skills directly from source (no symlinks needed)

## Workflow Rules

### Skill Availability Principle
**All skills in this repository must be available across all projects and all agents.**

Skills are developed in `~/agents/skills/` (JJ-tracked) and **symlinked to `~/.agents/skills/`** for universal agent discovery.

| Tool | Discovery Method | Status |
|------|------------------|--------|
| **Pi** | Reads `~/.agents/skills/` (symlinked) | ✅ Working |
| **Claude Code** | Symlinks in `~/.claude/skills/` | ✅ Working |
| **Codex/Cursor/etc** | Via symlinks in their skill dirs | ⚠️ On demand |

**Required for every new skill:**
```bash
# 1. Create in source directory
mkdir -p ~/agents/skills/<skill-name>

# 2. Symlink to ~/.agents/skills/ (Pi + other agents)
ln -sf ~/agents/skills/<skill-name> ~/.agents/skills/<skill-name>

# 3. For Claude Code (if using)
ln -sf ~/.agents/skills/<skill-name> ~/.claude/skills/<skill-name>
```

### Creating New Skills
1. Create directory: `mkdir -p skills/<skill-name>`
2. Write `skills/<skill-name>/SKILL.md`
3. **Symlink to `~/.agents/skills/` (required):**
   ```bash
   ln -sf ~/agents/skills/<skill-name> ~/.agents/skills/<skill-name>
   ```
4. Add Claude Code symlink (if using Claude Code):
   ```bash
   ln -sf ~/.agents/skills/<skill-name> ~/.claude/skills/<skill-name>
   ```
5. Follow naming conventions

### When to Create Separate Skills
Consider splitting into separate skills when:
- **Different trigger conditions** — When to use each skill is distinct
- **Different expertise domains** — Knowledge areas don't significantly overlap
- **Independent utility** — Users might want one skill without the other
- **Clear boundaries** — Each skill has a focused, well-defined scope

**Example:** `my-crawl4ai` (web scraping) and `my-tech-stack` (tooling preferences) are separate because they have different triggers and expertise, even though both relate to development workflows.

### Skill Naming Conventions
- Personal conventions: `my-<thing>` (e.g., `my-tech-stack`)
- General tools: descriptive name (e.g., `skill-creator`)

### See Also
- [[skill-distribution-manual-symlinks]] — Why we use manual symlinks
- [[skill-separation-of-concerns]] — When to split skills
- [[skill-representatives-team]] — Multi-domain discussion team

## Skill Representatives Team

For multi-domain discussions, a team of skill representatives is available:

| Representative | Domain |
|----------------|--------|
| `agent-rules-rep` | Agent configuration (AGENT.md, claude.md) |
| `generalist-rep` | Cross-domain topics, bridges gaps |
| `jj-workflow-rep` | Daily version control (jj, git, worktrees) |
| `my-crawl4ai-rep` | Web crawling/scraping with crawl4ai |
| `my-semantic-release-rep` | Semantic versioning and releases |
| `skill-bar-raiser` | Quality assurance — triggers, expertise, separation |
| `tech-stack-rep` | Preferred tooling recommendations |

**Template:** `skill-representatives`

Use `create_predefined_team()` to instantiate for discussions spanning multiple skill domains.

**Recent Split:** `my-jj-workflow` was separated from `my-semantic-release` because they have different triggers (daily VCS vs release workflows) and independent utility.

### Skill Bar Raiser Role

The `skill-bar-raiser` ensures skill quality by reviewing:
- **Triggers** — Clear, specific when-to-use conditions
- **Expertise** — Deep, actionable knowledge with examples
- **Separation of concerns** — Proper boundaries, minimal overlap

## Tool-Specific Notes

### Pi
Pi discovers skills from `~/.agents/skills/` automatically. **The symlink from `~/agents/skills/` to `~/.agents/skills/` is required** to make JJ-tracked skills available to Pi.

### Claude Code
Requires symlinks in `~/.claude/skills/` to discover skills. Add manually when creating new skills.

### Other Agents
Configure on demand when using Codex, Cursor, Gemini, etc. Most follow similar symlink patterns.

## Communication Style
- When suggesting new skills, check `skills/` for existing patterns
- Prefer skill-based workflows over one-off shell scripts
- Document skill purposes clearly in SKILL.md frontmatter
