# Python Integration Guide

Using crawl4ai in Python projects with uv.

## Quick Start

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com")
        print(result.markdown)

asyncio.run(main())
```

---

## Installation

### With uv (Recommended)

```bash
# Add to existing project
uv add "crawl4ai[basic,browser,markdown]"

# Or full install
uv add "crawl4ai[all]"
```

### Browser Setup

```bash
# Download Chromium/Chrome binaries
uv run python -c "import crawl4ai; crawl4ai.setup()"
```

---

## Core Concepts

### AsyncWebCrawler

The main entry point. Always use as an async context manager.

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# Basic usage
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")

# With custom config
browser_config = BrowserConfig(headless=True)
async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(url="https://example.com")
```

### BrowserConfig

Controls browser behavior.

```python
from crawl4ai import BrowserConfig

config = BrowserConfig(
    headless=True,           # Run without UI
    viewport_width=1920,     # Browser width
    viewport_height=1080,    # Browser height
    user_agent="Custom UA",  # Custom user agent
    user_data_dir="./data",  # Persist cookies/session
)
```

### CrawlerRunConfig

Controls crawl behavior.

```python
from crawl4ai import CrawlerRunConfig, CacheMode

config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,  # Cache responses
    markdown=True,                   # Generate markdown
    screenshot=True,                 # Capture screenshot
    pdf=True,                        # Generate PDF
    wait_for="css:.content",         # Wait for element
    delay_before_return_html=1.0,    # Extra wait time
)
```

---

## Common Patterns

### Single Page Crawl

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl_single(url: str) -> str:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

# Usage
markdown = asyncio.run(crawl_single("https://example.com"))
```

### Batch Crawling

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def crawl_batch(urls: list[str]):
    config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        max_concurrent=3  # Limit concurrent requests
    )
    
    async with AsyncWebCrawler() as crawler:
        tasks = [crawler.arun(url=url, config=config) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                print(f"Error crawling {url}: {result}")
            else:
                print(f"Success: {url} -> {len(result.markdown)} chars")

# Usage
urls = ["https://example1.com", "https://example2.com"]
asyncio.run(crawl_batch(urls))
```

### With CSS Selectors

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def crawl_with_wait(url: str, selector: str):
    config = CrawlerRunConfig(
        wait_for=f"css:{selector}",
        wait_for_timeout=5000  # 5 seconds
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        return result.markdown
```

### Error Handling

```python
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.errors import CrawlError

async def crawl_safe(url: str) -> str | None:
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    except CrawlError as e:
        print(f"Crawl failed for {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Working with Results

### Result Object

```python
result = await crawler.arun(url="https://example.com")

# Available attributes
result.markdown          # Markdown content
result.html             # Raw HTML
result.text             # Plain text
result.screenshot       # Screenshot bytes (if enabled)
result.pdf              # PDF bytes (if enabled)
result.metadata         # Page metadata (title, description, etc.)
result.links            # List of links found
result.images           # List of images found
```

### Metadata

```python
result = await crawler.arun(url="https://example.com")

meta = result.metadata
print(f"Title: {meta.get('title')}")
print(f"Description: {meta.get('description')}")
print(f"Keywords: {meta.get('keywords', [])}")
```

---

## Advanced Usage

### Custom Extraction Strategy

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# Define extraction schema
schema = {
    "name": "Article Extractor",
    "baseSelector": "article",
    "fields": [
        {"name": "title", "selector": "h1", "type": "text"},
        {"name": "content", "selector": ".content", "type": "text"},
        {"name": "author", "selector": ".author", "type": "text"},
        {"name": "date", "selector": "time", "type": "attribute", "attribute": "datetime"}
    ]
}

async def extract_articles(url: str):
    strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(extraction_strategy=strategy)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        import json
        return json.loads(result.extracted_content)
```

### Session/Cookie Persistence

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig

# Use user_data_dir to persist session
config = BrowserConfig(
    user_data_dir="./browser_data"
)

async with AsyncWebCrawler(config=config) as crawler:
    # First crawl - login or set cookies
    await crawler.arun(url="https://site.com/login")
    
    # Subsequent crawls use same session
    result = await crawler.arun(url="https://site.com/protected")
```

---

## Testing

### Mocking crawl4ai

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_crawler():
    with patch("crawl4ai.AsyncWebCrawler") as mock:
        instance = AsyncMock()
        instance.arun = AsyncMock(return_value=AsyncMock(
            markdown="# Test Content",
            html="<h1>Test</h1>",
            metadata={"title": "Test"}
        ))
        mock.return_value.__aenter__ = AsyncMock(return_value=instance)
        mock.return_value.__aexit__ = AsyncMock(return_value=False)
        yield mock

async def test_crawl(mock_crawler):
    result = await my_crawl_function("https://example.com")
    assert result == "# Test Content"
```

---

## Best Practices

1. **Always use context managers**: `async with AsyncWebCrawler()`
2. **Enable caching**: `cache_mode=CacheMode.ENABLED` for repeated crawls
3. **Limit concurrency**: Use `max_concurrent` to avoid overwhelming sites
4. **Handle errors**: Wrap crawls in try/except blocks
5. **Respect robots.txt**: Check site's crawling policy
6. **Add delays**: Use `delay_before_return_html` to let JS render

---

## Troubleshooting

### Browser not found

```bash
uv run python -c "import crawl4ai; crawl4ai.setup()"
```

### Timeout errors

Increase wait time:
```python
config = CrawlerRunConfig(
    wait_for_timeout=10000,  # 10 seconds
    delay_before_return_html=2.0
)
```

### Memory issues

Limit concurrent crawls:
```python
config = CrawlerRunConfig(max_concurrent=2)
```
