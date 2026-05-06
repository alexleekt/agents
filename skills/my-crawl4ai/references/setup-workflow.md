# Setup Workflow

Complete step-by-step guide for setting up crawl4ai with uv and just.

## Prerequisites

- `uv` installed (Python package manager)
- `just` installed (task runner)

## Step 1: Create Project Directory

```bash
mkdir -p ./my-crawler
cd ./my-crawler
```

## Step 2: Initialize uv Project

```bash
uv init --name crawler --python 3.12
```

This creates:
- `pyproject.toml` — Project configuration
- `README.md` — Project documentation
- `.python-version` — Python version pin

## Step 3: Add crawl4ai

### Option A: Recommended (smaller footprint)

```bash
uv add "crawl4ai[basic,browser,markdown]"
```

Includes:
- Core crawling engine
- Browser automation (Playwright)
- Markdown generation

### Option B: Full install

```bash
uv add "crawl4ai[all]"
```

Includes everything: cosine similarity, advanced extractors, etc.

## Step 4: Install Browser Binaries

One-time setup for Chromium/Chrome:

```bash
uv run python -c "import crawl4ai; crawl4ai.setup()"
```

Or via justfile (see Step 5):
```bash
just setup-browser
```

## Step 5: Create Justfile

Create `justfile` in project root:

```just
# Default recipe - list all tasks
_default:
    @just --list

# Install/sync dependencies from pyproject.toml
install:
    uv sync

# Run crawler on single URL
crawl url *args:
    uv run python -m crawler "{{url}}" {{args}}

# Run basic example
example:
    uv run python src/crawler/quick.py https://example.com

# Setup browser binaries (first time only)
setup-browser:
    uv run python -c "import crawl4ai; crawl4ai.setup()"

# Run all tests
test:
    uv run pytest tests/

# Clean data directories
clean:
    rm -rf data/raw/* data/processed/*
    @echo "Data directories cleaned"

# Format code with ruff (if installed)
format:
    uv run ruff format src/
    uv run ruff check --fix src/
```

## Step 6: Create Directory Structure

```bash
mkdir -p src/crawler data/raw data/processed
```

## Step 7: Create First Crawler Script

Create `src/crawler/quick.py`:

```python
#!/usr/bin/env python3
"""Quick single-page crawler using crawl4ai."""

import asyncio
import sys
from pathlib import Path
from crawl4ai import AsyncWebCrawler

async def crawl_single(url: str, output_dir: Path | None = None) -> str:
    """Crawl a single URL and return markdown content."""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            output_file = output_dir / f"{filename}.md"
            output_file.write_text(result.markdown)
            print(f"Saved to: {output_file}")
        
        return result.markdown

async def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    output_dir = Path("data/raw") if len(sys.argv) > 2 else None
    
    print(f"Crawling: {url}")
    content = await crawl_single(url, output_dir)
    
    if not output_dir:
        print(content)

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 8: Test the Setup

```bash
# Crawl and print to stdout
uv run python src/crawler/quick.py https://example.com

# Crawl and save to file
uv run python src/crawler/quick.py https://example.com data/raw

# Or using just
just example
just crawl https://example.com
```

## Step 9: Add Shell Aliases (Optional)

Add to your shell configuration:

```bash
# System-wide: quick crawls from any directory
alias crawl='uvx --from crawl4ai crwl'

# Project-based: requires justfile in project directory
alias crawl-proj='cd ./my-crawler && just crawl'
```

For Fish shell, use `abbr` instead of `alias`:

```fish
abbr -a crawl 'uvx --from crawl4ai crwl'
```

## Verification Checklist

- [ ] Project directory exists and has `pyproject.toml`
- [ ] `uv sync` completes without errors
- [ ] `just --list` shows available tasks
- [ ] Browser setup completes (run `just setup-browser`)
- [ ] `just example` successfully crawls example.com
- [ ] Shell aliases/abbreviations work: `crawl https://example.com`

## Next Steps

1. Read `code-templates.md` for advanced crawler patterns
2. Read `integration-guides/typescript.md` for TS project integration
3. Explore crawl4ai docs: https://docs.crawl4ai.com
