# AI Agent Skills Repository

This directory contains **skills** that guide how AI agents work with your projects. Skills are modular, reusable expertise modules that agents consult automatically based on triggers.

**New to skills?** See [Getting Started](#getting-started) below, then read `AGENTS.md` for creation guidelines.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Skills Overview](#skills-overview)
- [Getting Started](#getting-started)
- [For AI Agents](#for-ai-agents)
- [For Users](#for-users)
- [Legacy Note](#legacy-note)

## Directory Structure

```
agents/
├── README.md           # This file
├── AGENTS.md           # Skill creation and management guidelines
├── skills/             # Personal skills
│   ├── cua-computer-use/
│   ├── my-agent-file-conventions/
│   ├── my-code-review/
│   ├── my-crawl4ai/
│   ├── my-krea/
│   ├── my-semantic-release/
│   ├── my-team-orchestrate/
│   ├── my-tech-stack/
│   ├── my-web-search-kagi/
│   └── my-workflow/
└── .pi/
    └── agents/         # Agent definitions
```

## Skills Overview

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `cua-computer-use` | "computer-use", "screen control", "GUI automation" | macOS app control, screenshots, clicking |
| `my-agent-file-conventions` | "AGENT.md", "claude.md", "agent file" | What belongs in agent files, templates, boundaries |
| `my-code-review` | "code review", "PR review", "check my code" | Research-based code quality reviews |
| `my-crawl4ai` | "crawl4ai", "web scraping", "scrape data" | Web crawling with crawl4ai |
| `my-krea` | "generate image", "make a video", "AI image" | Image and video generation with Krea AI |
| `my-semantic-release` | "release", "changelog", "semver" | Semantic versioning and release workflows |
| `my-tech-stack` | "what should I use", "bun or node" | Preferred tools and technology recommendations |
| `my-web-search-kagi` | "search the web", "look up", "google" | Web search via agent-browser + Kagi |
| `my-workflow` | "assessing task direction", "should I switch" | Worktrunk discipline, commit timing, naming hygiene |

## Getting Started

**Quick setup for new users:**

1. **Clone this repo:**
   ```bash
   git clone https://github.com/alexleekt/agents.git ~/agents
   ```

2. **Symlink skills for Pi:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -sf ~/git/my-agent-skills/skills/* ~/.agents/skills/
   ```

3. **Verify setup:**
   ```bash
   ls ~/.agents/skills/  # Should show: my-agent-file-conventions, my-code-review, etc.
   ```

**Creating your first skill:**
- Read `AGENTS.md` → "Creating New Skills" section
- Description must be **≤1024 characters** (Pi constraint)
- Use `wc -c` to check: `head -20 SKILL.md | grep -A 100 "^description:" | wc -c`

## For AI Agents

When starting work:

1. **Check for project-specific agent files** — Look for `AGENT.md` or `claude.md` in the project root
2. **Use skill references** — Consult `@skills/my-tech-stack` for tool recommendations, `@skills/my-agent-file-conventions` for agent file creation
3. **Skills auto-load** — Pi reads from `~/.agents/skills/` (symlinked from this directory)

## For Users

- **Adding skills:** See `AGENTS.md` for skill creation workflow
- **Updating skills:** Edit files in `skills/<skill-name>/SKILL.md`, changes auto-commit via chezmoi
- **Distributing:** Skills are symlinked to `~/.agents/skills/` for Pi and `~/.claude/skills/` for Claude Code

## Legacy Note

Previous `conventions/agent-conventions.md` and `preferences/tech-preferences.md` have been superseded by `my-agent-file-conventions` and `my-tech-stack` skills respectively. The legacy files are preserved in git history but removed from the working tree.
 are preserved in git history but removed from the working tree.
