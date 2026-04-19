# Code Templates

Ready-to-use Python code templates for common crawl4ai patterns.

## Table of Contents

1. [Basic Single Page](#basic-single-page)
2. [Batch Crawler](#batch-crawler)
3. [Authenticated Crawler](#authenticated-crawler)
4. [Configuration Module](#configuration-module)
5. [Screenshot + PDF Export](#screenshot--pdf-export)
6. [Structured Data Extraction](#structured-data-extraction)

---

## Basic Single Page

**File:** `src/crawler/quick.py`

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

---

## Batch Crawler

**File:** `src/crawler/batch.py`

```python
#!/usr/bin/env python3
"""Batch crawler for multiple URLs."""

import asyncio
import json
import sys
from pathlib import Path
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def crawl_batch(
    urls: list[str],
    output_dir: Path,
    max_concurrent: int = 3
) -> list[dict]:
    """Crawl multiple URLs with rate limiting."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        max_concurrent=max_concurrent
    )
    
    results = []
    
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            try:
                print(f"Crawling: {url}")
                result = await crawler.arun(url=url, config=config)
                
                # Save markdown
                filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                md_file = output_dir / f"{filename}.md"
                md_file.write_text(result.markdown)
                
                results.append({
                    "url": url,
                    "success": True,
                    "file": str(md_file),
                    "title": result.metadata.get("title", "")
                })
                
            except Exception as e:
                print(f"Error crawling {url}: {e}")
                results.append({
                    "url": url,
                    "success": False,
                    "error": str(e)
                })
    
    # Save results index
    index_file = output_dir / "index.json"
    index_file.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to: {index_file}")
    
    return results

def load_urls_from_file(path: Path) -> list[str]:
    """Load URLs from text file (one per line)."""
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]

async def main():
    if len(sys.argv) < 2:
        print("Usage: python batch.py <urls_file> [output_dir]")
        print("  urls_file: Text file with one URL per line")
        sys.exit(1)
    
    urls_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/raw")
    
    urls = load_urls_from_file(urls_file)
    print(f"Loaded {len(urls)} URLs from {urls_file}")
    
    await crawl_batch(urls, output_dir)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Authenticated Crawler

**File:** `src/crawler/auth.py`

```python
#!/usr/bin/env python3
"""Authenticated crawling with login flow."""

import asyncio
import os
import sys
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig

# Load credentials from environment variables
USERNAME = os.getenv("CRAWL_USERNAME")
PASSWORD = os.getenv("CRAWL_PASSWORD")

async def login_and_crawl(
    login_url: str,
    target_url: str,
    username_selector: str = "input[name='username']",
    password_selector: str = "input[name='password']",
    submit_selector: str = "button[type='submit']",
    output_dir: Path | None = None
) -> str:
    """Login and then crawl authenticated content."""
    
    if not USERNAME or not PASSWORD:
        raise ValueError("CRAWL_USERNAME and CRAWL_PASSWORD environment variables required")
    
    # Config with persistent context for session
    browser_config = BrowserConfig(
        headless=True,
        user_data_dir="./.browser_data"  # Persists session
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Navigate to login page
        print(f"Logging in at: {login_url}")
        
        # Execute login script
        await crawler.arun(
            url=login_url,
            js_code=f"""
                document.querySelector("{username_selector}").value = "{USERNAME}";
                document.querySelector("{password_selector}").value = "{PASSWORD}";
                document.querySelector("{submit_selector}").click();
            """
        )
        
        # Wait for login to complete (adjust as needed)
        await asyncio.sleep(2)
        
        # Now crawl target URL with same session
        print(f"Crawling: {target_url}")
        result = await crawler.arun(url=target_url)
        
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = target_url.replace("https://", "").replace("http://", "").replace("/", "_")
            output_file = output_dir / f"{filename}.md"
            output_file.write_text(result.markdown)
            print(f"Saved to: {output_file}")
        
        return result.markdown

async def main():
    if len(sys.argv) < 3:
        print("Usage: python auth.py <login_url> <target_url> [output_dir]")
        sys.exit(1)
    
    login_url = sys.argv[1]
    target_url = sys.argv[2]
    output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    
    content = await login_and_crawl(login_url, target_url, output_dir=output_dir)
    
    if not output_dir:
        print(content)

if __name__ == "__main__":
    asyncio.run(main())
```

**Usage with environment variables:**
```bash
# Set credentials
export CRAWL_USERNAME="your_username"
export CRAWL_PASSWORD="your_password"

# Run authenticated crawl
uv run python src/crawler/auth.py https://site.com/login https://site.com/data
```

---

## Configuration Module

**File:** `src/crawler/config.py`

```python
"""Shared configuration for crawlers."""

from crawl4ai import BrowserConfig, CrawlerRunConfig, CacheMode

# Browser settings
BROWSER_CONFIG = BrowserConfig(
    headless=True,
    viewport_width=1920,
    viewport_height=1080,
)

# Development/debug browser (visible)
BROWSER_CONFIG_DEBUG = BrowserConfig(
    headless=False,
    viewport_width=1920,
    viewport_height=1080,
)

# Standard crawl config
CRAWL_CONFIG = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,
    markdown=True,
)

# Full extraction config
FULL_CONFIG = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,
    markdown=True,
    screenshot=True,
    pdf=True,
    extract_images=True,
)

# Lightweight config (fast, minimal)
LIGHT_CONFIG = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown=True,
    screenshot=False,
)
```

**Usage:**
```python
from crawler.config import BROWSER_CONFIG, CRAWL_CONFIG

async with AsyncWebCrawler(config=BROWSER_CONFIG) as crawler:
    result = await crawler.arun(url=url, config=CRAWL_CONFIG)
```

---

## Screenshot + PDF Export

**File:** `src/crawler/export.py`

```python
#!/usr/bin/env python3
"""Crawl with screenshot and PDF export."""

import asyncio
import sys
from pathlib import Path
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def crawl_with_export(url: str, output_dir: Path) -> dict:
    """Crawl URL and save markdown, screenshot, and PDF."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
    
    config = CrawlerRunConfig(
        markdown=True,
        screenshot=True,
        pdf=True
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        
        # Save markdown
        md_file = output_dir / f"{filename}.md"
        md_file.write_text(result.markdown)
        
        # Save screenshot (if available)
        if result.screenshot:
            screenshot_file = output_dir / f"{filename}.png"
            screenshot_file.write_bytes(result.screenshot)
        
        # Save PDF (if available)
        if result.pdf:
            pdf_file = output_dir / f"{filename}.pdf"
            pdf_file.write_bytes(result.pdf)
        
        return {
            "url": url,
            "markdown": str(md_file),
            "screenshot": str(screenshot_file) if result.screenshot else None,
            "pdf": str(pdf_file) if result.pdf else None
        }

async def main():
    if len(sys.argv) < 2:
        print("Usage: python export.py <url> [output_dir]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/raw")
    
    result = await crawl_with_export(url, output_dir)
    print(f"Exported: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Structured Data Extraction

**File:** `src/crawler/extract.py`

```python
#!/usr/bin/env python3
"""Extract structured data using CSS selectors."""

import asyncio
import json
import sys
from pathlib import Path
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_structured(url: str, schema: dict) -> list[dict]:
    """Extract structured data from URL using schema."""
    
    strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(extraction_strategy=strategy)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        return json.loads(result.extracted_content)

# Example: Product extraction schema
PRODUCT_SCHEMA = {
    "name": "Product Extractor",
    "baseSelector": ".product",
    "fields": [
        {"name": "title", "selector": "h2.title", "type": "text"},
        {"name": "price", "selector": ".price", "type": "text"},
        {"name": "image", "selector": "img", "type": "attribute", "attribute": "src"},
        {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
    ]
}

async def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <url>")
        print("\nThis example extracts products using CSS selectors.")
        print("Modify PRODUCT_SCHEMA in the script for your needs.")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"Extracting from: {url}")
    data = await extract_structured(url, PRODUCT_SCHEMA)
    
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Justfile Tasks for Templates

Add to your `~/projects/crawler/justfile`:

```just
# Run quick single-page crawl
crawl-quick url:
    uv run python src/crawler/quick.py "{{url}}"

# Run batch crawl from file
crawl-batch urls-file:
    uv run python src/crawler/batch.py "{{urls-file}}" data/raw

# Run authenticated crawl (requires env vars)
crawl-auth login-url target-url:
    uv run python src/crawler/auth.py "{{login-url}}" "{{target-url}}"

# Crawl with screenshot/PDF export
crawl-export url:
    uv run python src/crawler/export.py "{{url}}" data/raw

# Extract structured data
crawl-extract url:
    uv run python src/crawler/extract.py "{{url}}"
```
