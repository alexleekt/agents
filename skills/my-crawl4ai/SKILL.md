---
name: my-crawl4ai
description: |
  Set up and use crawl4ai for web crawling/scraping using uv, just, and project-based workflows.
  Use when the user mentions crawl4ai, web scraping, crawling sites, or needs to extract 
  web content as markdown/JSON. Assumes uv for Python, just for tasks, Fish shell, and 
  mise for version management. For TypeScript/Node projects, provides CLI/MCP integration patterns.
---

# crawl4ai

Web crawling with crawl4ai using your preferred stack: uv, just, Fish, and mise.

## Quick Start

```bash
# One-off crawl (any directory)
uvx --from crawl4ai crwl https://example.com --format markdown

# Project-based setup (recommended)
mkdir -p ~/projects/crawler && cd ~/projects/crawler
uv init --name crawler --python 3.12
uv add "crawl4ai[basic,browser,markdown]"
uv run python -c "import crawl4ai; crawl4ai.setup()"
```

## When to Use What

| Situation | Approach |
|-----------|----------|
| Quick one-page crawl | **uvx CLI** — `uvx --from crawl4ai crwl URL` |
| Regular crawling needs | **Python API** — project at `~/projects/crawler/` |
| From TypeScript project | **uvx via `bun.$`** or **MCP server** |
| Isolated/containerized | **Docker** — `unclecode/crawl4ai:latest` |

---

## Project Setup

Read `references/setup-workflow.md` for detailed steps.

### 1. Create Project

```bash
mkdir -p ~/projects/crawler
cd ~/projects/crawler
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
# ~/projects/crawler/justfile

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

```bash
# ~/projects/crawler/ (Python) runs on schedule
# ~/projects/my-app/ (TypeScript) reads ./data/

# justfile in TS project:
sync-crawl-data:
    rsync -av ~/projects/crawler/data/ ./data/
```

---

## Fish Shell Integration (Optional)

Add to `~/.config/fish/conf.d/abbreviations.fish`:

```fish
# System-wide: quick crawls from any directory
abbr -a crawl 'uvx --from crawl4ai crwl'
```

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
~/projects/crawler/
├── .python-version          # mise-managed
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
