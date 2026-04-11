# my-crawl4ai Skill Creation Plan

## Skill Overview

Custom skill for setting up and using **crawl4ai** web crawler with the user's specific tech stack preferences: `uv`, `just`, Fish shell, `mise`, and TypeScript integration.

---

## Directory Structure

```
~/agents/skills/my-crawl4ai/
├── SKILL.md                           # Main skill file (triggers, instructions)
├── references/
│   ├── setup-workflow.md            # Step-by-step project setup
│   ├── code-templates.md            # Python code templates
│   └── integration-guides/
│       ├── typescript.md            # TS/JS project integration
│       └── python.md                # Python project integration
└── evals/
    └── evals.json                   # Test cases for skill evaluation
```

---

## SKILL.md Content Outline

### Frontmatter
```yaml
name: my-crawl4ai
description: |
  Set up and use crawl4ai for web crawling/scraping using uv, just, and project-based workflows.
  Use when the user mentions crawl4ai, web scraping, crawling sites, or needs to extract 
  web content as markdown/JSON. Assumes uv for Python, just for tasks, Fish shell, and 
  mise for version management. For TypeScript/Node projects, provides CLI/MCP integration patterns.
```

### Body Sections

1. **Quick Reference**
   - One-liner commands for common tasks
   - Decision tree: CLI vs API vs MCP vs Docker

2. **Project Setup Workflow**
   - Create `~/projects/crawler/`
   - `uv init --name crawler --python 3.12`
   - `uv add "crawl4ai[all]"`
   - `uv run python -c "import crawl4ai; crawl4ai.setup()"`
   - Create justfile with tasks

3. **Code Templates**
   - Basic single-page crawler
   - Batch crawler with config
   - Authenticated crawler (with bws secrets)
   - Screenshot + markdown extraction

4. **Integration Guides**
   - TypeScript/Node projects (via uvx CLI)
   - TypeScript/Node projects (via MCP server)
   - Docker approach
   - HTTP API mode

5. **Shell Integration**
   - Fish abbreviations: `crawl`, `crawl-proj`
   - Add to `~/.config/fish/conf.d/abbreviations.fish`

6. **Troubleshooting**
   - Browser setup issues
   - Permission errors
   - Memory/performance tuning

---

## Reference Files to Create

### references/setup-workflow.md
Detailed commands for:
- Initial project creation
- Browser binary installation
- First test crawl
- Justfile task definitions

### references/code-templates.md
Copy-paste ready Python modules:
- `quick.py` — CLI-equivalent single URL
- `batch.py` — Multiple URLs from file
- `auth.py` — Authenticated crawling with bws
- `config.py` — Reusable BrowserConfig/CrawlerRunConfig

### references/integration-guides/typescript.md
Options for TS projects:
- uvx CLI via `bun.$`
- MCP server setup
- Data pipeline approach (crawler → shared data dir → TS consumer)

### references/integration-guides/python.md
Native Python project setup:
- Import patterns
- Async context managers
- Error handling

---

## Test Cases (evals/evals.json)

### Test 1: Basic Setup
**Prompt:** "Set up crawl4ai for my project"
**Expected:** Creates `~/projects/crawler/` with:
- `pyproject.toml` with crawl4ai dependency
- `justfile` with `crawl`, `setup-browser`, `example` tasks
- `src/crawler/basic.py` template

### Test 2: TypeScript Integration
**Prompt:** "How do I crawl a site from my TypeScript app?"
**Expected:** Explains MCP server or uvx CLI approach, provides code snippet for `bun.$`

### Test 3: Authenticated Crawler
**Prompt:** "Create a crawler that logs in before scraping"
**Expected:** Generates `src/crawler/auth.py` with:
- bws secret loading
- BrowserContext with storage state
- Login flow + crawl sequence

### Test 4: Fish Abbreviations
**Prompt:** "Add Fish abbreviations for crawl4ai"
**Expected:** Updates `~/.config/fish/conf.d/abbreviations.fish` with:
```fish
abbr -a crawl 'uvx run crawl4ai'
abbr -a crawl-proj 'cd ~/projects/crawler && just crawl'
```

---

## User Confirmation Needed

1. **Project location**: Default to `~/projects/crawler/` or prompt user?
2. **Default extras**: `crawl4ai[all]` or prefer `crawl4ai[basic,browser,markdown]`?
3. **Fish abbreviations**: Add automatically or ask user first?
4. **Test scope**: Include evaluation with actual crawl4ai execution or mock?

---

## Files Created ✓

- [x] SKILL.md
- [x] references/setup-workflow.md
- [x] references/code-templates.md
- [x] references/integration-guides/typescript.md
- [x] references/integration-guides/python.md
- [x] evals/evals.json

## Notes

- Removed bitwarden/bws integration as requested
- Using generic environment variables (os.getenv) for credentials
- Default project location: ~/projects/crawler/
- Default install: crawl4ai[basic,browser,markdown] (selective)

- [ ] SKILL.md
- [ ] references/setup-workflow.md
- [ ] references/code-templates.md
- [ ] references/integration-guides/typescript.md
- [ ] references/integration-guides/python.md
- [ ] evals/evals.json
