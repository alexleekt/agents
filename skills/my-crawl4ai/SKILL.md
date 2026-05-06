---
name: my-crawl4ai
description: |
  **ALWAYS use when user mentions:** "crawl4ai", "web scraping", "crawl a site",
  "extract web content", "scrape data from URL", or needs to extract web content
  as markdown/JSON.

  **DO NOT use for:** Browser automation (clicking, filling forms, screenshots,
  testing web apps) — use @skills/agent-browser for those.

  Set up and use crawl4ai for web crawling/scraping using uv, just, and project-based workflows.
  Assumes uv for Python and just for task automation.
---

# crawl4ai

Web crawling with crawl4ai using modern Python tooling: uv, just, and project-based workflows.

## Quick Start

```bash
# One-off crawl (any directory)
uvx --from crawl4ai crwl https://example.com --format markdown

# Project-based setup (recommended)
mkdir -p ./my-crawler && cd ./my-crawler
uv init --name crawler --python 3.12
uv add "crawl4ai[basic,browser,markdown]"
uv run python -c "import crawl4ai; crawl4ai.setup()"
```

## Prerequisites

- **uv** — Python package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **just** — Task runner (optional, install: `cargo install just` or package manager)
- **Shell** — bash, zsh, or fish (all examples are POSIX-compatible)
- **Disk space** — ~200MB for browser binaries (downloaded once)

## Reference Files

This skill references detailed guides for specific situations:

| Read this | When you need to... |
|-----------|---------------------|
| `references/setup-workflow.md` | Set up a new crawler project from scratch |
| `references/code-templates.md` | Get ready-to-use code for batch crawling, auth, screenshots |
| `references/integration-guides/typescript.md` | Use crawl4ai from a TypeScript/Node project |

**Always check reference files when:**
- Setting up a new project → read `setup-workflow.md`
- Need code examples → read `code-templates.md`
- Working with TypeScript → read `integration-guides/typescript.md`

## When to Use What

| Situation | Approach |
|-----------|----------|
| Quick one-page crawl | **uvx CLI** — `uvx --from crawl4ai crwl URL` |
| Regular crawling needs | **Python API** — dedicated project directory |
| From TypeScript project | **uvx via `bun.$`** or **MCP server** |
| Isolated/containerized | **Docker** — `unclecode/crawl4ai:latest` |

---

## Project Setup

Read `references/setup-workflow.md` for detailed steps.

### 1. Create Project

```bash
mkdir -p ./my-crawler
cd ./my-crawler
uv init --name crawler --python 3.12
```

### 2. Add Dependencies

```bash
# Recommended: basic + browser + markdown (smaller than [all])
uv add "crawl4ai[basic,browser,markdown]"

# Or full install with all features
uv add "crawl4ai[all]"
```

### 3. Setup Browser (one-time)

```bash
uv run python -c "import crawl4ai; crawl4ai.setup()"
```

### 4. Create Justfile

```just
# justfile

_default:
    @just --list

install:
    uv sync

crawl url *args:
    uv run python -m crawler "{{url}}" {{args}}

example:
    uv run python src/crawler/quick.py https://example.com

setup-browser:
    uv run python -c "import crawl4ai; crawl4ai.setup()"

clean:
    rm -rf data/raw/* data/processed/*
```

---

## Code Templates

Read `references/code-templates.md` for full templates.

### Basic Single Page

```python
# src/crawler/quick.py
import asyncio
import sys
from pathlib import Path
from crawl4ai import AsyncWebCrawler

async def main(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        print(result.markdown)

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    asyncio.run(main(url))
```

### Batch Crawler

```python
# src/crawler/batch.py
import asyncio
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def crawl_urls(urls: list[str], output_dir: Path):
    config = CrawlerRunConfig(cache_mode=True)
    
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            result = await crawler.arun(url=url, config=config)
            output_file = output_dir / f"{url.replace('/', '_')}.md"
            output_file.write_text(result.markdown)
```

---

## TypeScript Integration

Read `references/integration-guides/typescript.md` for full details.

### Option 1: uvx CLI via bun

```typescript
// scripts/crawl.ts
import { $ } from "bun";

const result = await $`uvx --from crawl4ai crwl ${url} --format markdown`.text();
// Process result in TypeScript
```

### Option 2: MCP Server

```bash
# Terminal 1: Start MCP server
uvx --from crawl4ai crawl4ai-mcp

# In your TS code, call via MCP client
const crawlResult = await mcpClient.call("crawl", { url, format: "markdown" });
```

### Option 3: Data Pipeline

Separate crawler project and TypeScript app sharing data directory:

```bash
# Crawler project (Python + uv) runs on schedule
# TypeScript app reads from shared data location

# justfile in TS project:
sync-crawl-data:
    rsync -av ./crawler-data/raw/ ./data/crawled/
```

---

## Shell Integration (Optional)

Add to your shell configuration (e.g., `.bashrc`, `.zshrc`, `config.fish`):

```bash
# System-wide: quick crawls from any directory
alias crawl='uvx --from crawl4ai crwl'
```

Or for project-specific:

```bash
# Project-based: requires justfile in project directory
alias crawl-proj='cd ./my-crawler && just crawl'
```

---

## Common Agent Mistakes

**Mistake 1: Using crawl4ai for browser automation**
- ❌ Wrong: "Click the login button and take a screenshot"
- ✅ Right: Use `@skills/agent-browser` for clicking, filling forms, screenshots
- **Rule:** crawl4ai = content extraction, agent-browser = interaction automation

**Mistake 2: Not reading reference files when setting up**
- ❌ Wrong: Trying to write setup steps from memory
- ✅ Right: Read `references/setup-workflow.md` for complete step-by-step setup
- **Rule:** Reference files exist for a reason — use them

**Mistake 3: Skipping browser setup**
- ❌ Wrong: Running crawler without `crawl4ai.setup()` first
- ✅ Right: Always run browser setup before first use (one-time)
- **Rule:** Check error messages for "browser not found" → run setup

**Mistake 4: Confusing one-off vs project approaches**
- ❌ Wrong: Creating a full project for a single URL crawl
- ✅ Right: Use `uvx --from crawl4ai crwl URL` for one-off crawls
- **Rule:** Project setup only for recurring crawling needs

**Mistake 5: Not using justfile**
- ❌ Wrong: Typing long `uv run python ...` commands repeatedly
- ✅ Right: Create justfile with common tasks (`just crawl <url>`)
- **Rule:** Save time with task automation

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Browser not found | Run `uv run python -c "import crawl4ai; crawl4ai.setup()"` |
| Chromium download fails | Check internet, try `export PLAYWRIGHT_BROWSERS_PATH=0` |
| Permission denied | Ensure `~/.cache/crawl4ai` is writable |
| Memory issues | Reduce `max_concurrent` in CrawlerRunConfig |
| Headless fails | Set `headless=False` temporarily to debug |

---

## Project Structure Reference

```
./my-crawler/
├── .python-version          # Python version file
├── pyproject.toml           # uv project config
├── justfile                 # Task automation
├── README.md
├── data/
│   ├── raw/                 # Crawled content
│   └── processed/           # Transformed data
└── src/
    └── crawler/
        ├── __init__.py
        ├── quick.py         # Single URL
        ├── batch.py         # Multiple URLs
        ├── auth.py          # Authenticated crawling
        └── config.py        # Shared configurations
```
