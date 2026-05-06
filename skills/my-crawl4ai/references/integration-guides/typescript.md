# TypeScript Integration Guide

Using crawl4ai from TypeScript/Node projects.

## Overview

Since crawl4ai is a Python tool, you have several options for integrating it with TypeScript projects:

1. **uvx CLI** — Simple, works from any directory
2. **MCP Server** — Structured API for complex workflows
3. **Data Pipeline** — Separate crawler process + file-based communication
4. **HTTP API** — REST interface for service-oriented architectures

---

## Option 1: uvx CLI (Simplest)

Execute crawl4ai CLI commands directly from TypeScript using Bun or Node.

### Using Bun

```typescript
// scripts/crawl.ts
import { $ } from "bun";

async function crawlToMarkdown(url: string): Promise<string> {
    const result = await $`uvx --from crawl4ai crwl ${url} --format markdown`.text();
    return result;
}

// Usage
const markdown = await crawlToMarkdown("https://example.com");
console.log(markdown);
```

### Using Node with child_process

```typescript
// scripts/crawl.ts
import { execSync } from "child_process";

function crawlToMarkdown(url: string): string {
    return execSync(`uvx --from crawl4ai crwl ${url} --format markdown`, {
        encoding: "utf-8",
        maxBuffer: 10 * 1024 * 1024  // 10MB for large pages
    });
}
```

### Batch Processing

```typescript
// scripts/batch-crawl.ts
import { $ } from "bun";

async function crawlMultiple(urls: string[]): Promise<Map<string, string>> {
    const results = new Map<string, string>();
    
    for (const url of urls) {
        try {
            const markdown = await $`uvx --from crawl4ai crwl ${url} --format markdown`.text();
            results.set(url, markdown);
        } catch (error) {
            console.error(`Failed to crawl ${url}:`, error);
            results.set(url, "");
        }
    }
    
    return results;
}
```

---

## Option 2: MCP Server (Structured)

If crawl4ai supports MCP (Model Context Protocol), you can call it as a service.

### Setup

```bash
# Terminal 1: Start MCP server
uvx --from crawl4ai crawl4ai-mcp

# Or add to your project's Procfile/dev configuration
```

### TypeScript Client

```typescript
// lib/crawl4ai-client.ts
interface CrawlOptions {
    url: string;
    format?: "markdown" | "html" | "json";
    screenshot?: boolean;
}

interface CrawlResult {
    url: string;
    markdown?: string;
    html?: string;
    metadata?: Record<string, any>;
}

class Crawl4AIClient {
    constructor(private mcpEndpoint: string = "http://localhost:11235") {}
    
    async crawl(options: CrawlOptions): Promise<CrawlResult> {
        const response = await fetch(`${this.mcpEndpoint}/crawl`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(options)
        });
        
        if (!response.ok) {
            throw new Error(`Crawl failed: ${response.statusText}`);
        }
        
        return response.json();
    }
}

export const crawler = new Crawl4AIClient();
```

### Usage

```typescript
// app.ts
import { crawler } from "./lib/crawl4ai-client";

const result = await crawler.crawl({
    url: "https://example.com",
    format: "markdown"
});

console.log(result.markdown);
```

---

## Option 3: Data Pipeline (Most Robust)

Separate concerns: crawler runs independently, TypeScript app consumes results.

### Architecture

```
crawler-project/              (Python + uv)
├── src/
│   └── scheduled-crawl.ts    # Runs on cron/schedule
└── data/
    └── raw/                  # Markdown outputs

my-app/                       (TypeScript + bun)
├── scripts/
│   └── sync-crawl-data.ts    # Pulls data from crawler
└── data/
    └── crawled/              # Local copy of crawled content
```

### Crawler (Python)

Runs on schedule (cron, GitHub Actions, etc.):

```python
# crawler-project/src/scheduled-crawl.py
import asyncio
from pathlib import Path
from crawl4ai import AsyncWebCrawler

SITES = [
    "https://docs.example.com",
    "https://blog.example.com",
]

async def scheduled_crawl():
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with AsyncWebCrawler() as crawler:
        for url in SITES:
            result = await crawler.arun(url=url)
            filename = url.replace("https://", "").replace("/", "_")
            (output_dir / f"{filename}.md").write_text(result.markdown)

if __name__ == "__main__":
    asyncio.run(scheduled_crawl())
```

### Sync Script (TypeScript)

```typescript
// my-app/scripts/sync-crawl-data.ts
import { $ } from "bun";

async function syncCrawlData() {
    // Pull latest crawled data
    await $`rsync -av ../crawler-project/data/raw/ ./data/crawled/`;
    
    // Process into your app's format
    const files = await $`ls ./data/crawled/*.md`.lines();
    
    for (const file of files) {
        const content = await Bun.file(file).text();
        // Index, chunk, or process as needed
        await processCrawledContent(file, content);
    }
}

async function processCrawledContent(path: string, content: string) {
    // Your processing logic here
    console.log(`Processing ${path}: ${content.length} chars`);
}

await syncCrawlData();
```

### Justfile Integration

```just
# my-app/justfile

# Sync latest crawled data
sync-crawl:
    bun run scripts/sync-crawl-data.ts

# Full pipeline: sync + process
pipeline: sync-crawl
    bun run build
```

---

## Option 4: Docker (Isolated)

Use Docker for complete isolation, especially in CI/CD.

### Docker Setup

```bash
# Pull image
docker pull unclecode/crawl4ai:latest

# Create wrapper script
alias crawl4ai='docker run --rm -v $(pwd)/data:/data unclecode/crawl4ai:latest'
```

### TypeScript Integration

```typescript
// scripts/crawl-docker.ts
import { execSync } from "child_process";

function crawlWithDocker(url: string, outputDir: string): string {
    const containerOutput = "/data/output.md";
    const hostOutput = `${outputDir}/output.md`;
    
    execSync(
        `docker run --rm -v ${outputDir}:/data unclecode/crawl4ai:latest ` +
        `crawl "${url}" --output ${containerOutput}`,
        { stdio: "inherit" }
    );
    
    return hostOutput;
}
```

---

## Comparison

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| **uvx CLI** | One-off scripts | Simple, no setup | Spawns process per call |
| **MCP Server** | Production apps | Structured API, batching | Requires running service |
| **Data Pipeline** | Scheduled/sync workflows | Decoupled, cacheable | Delay between crawl and use |
| **Docker** | CI/CD, isolation | No local Python needed | Slower startup |

---

## Recommended Setup

For most TypeScript projects:

1. **Start with uvx CLI** for quick prototyping
2. **Move to Data Pipeline** when you need caching/scheduled updates
3. **Consider MCP** if you need real-time crawling with complex options

---

## Type Definitions

```typescript
// types/crawl4ai.ts

export interface Crawl4AIOptions {
    url: string;
    format?: "markdown" | "html" | "text" | "json";
    screenshot?: boolean;
    pdf?: boolean;
    wait_for?: string;  // CSS selector to wait for
    timeout?: number;   // milliseconds
}

export interface Crawl4AIResult {
    url: string;
    markdown?: string;
    html?: string;
    text?: string;
    screenshot?: Buffer;  // Base64 or Buffer
    pdf?: Buffer;
    metadata: {
        title?: string;
        description?: string;
        keywords?: string[];
        [key: string]: any;
    };
    links?: string[];
    images?: string[];
}

export type Crawl4AICallback = (result: Crawl4AIResult) => Promise<void> | void;
```
