---
name: my-web-search-kagi
description: >
  Search the web using Kagi via agent-browser. Use this skill whenever the user
  wants to search the web, find information online, look up docs, check prices,
  research a topic, or verify facts. Also use when no dedicated web search MCP
  server is available. Triggers on phrases like "search the web", "look up",
  "find online", "google", "kagi search", "web search", "search for", or when
  the agent needs current/real-time information not in its training data.
---

# Web Search via Kagi + agent-browser

Perform web searches using Kagi Search through the agent-browser Chrome automation.

## When to Use

- User asks to "search the web", "look up", "find online", "google something"
- Need current/real-time information (news, prices, versions, recent docs)
- No web search MCP server is connected
- Kagi subscription is active (the browser profile already has Kagi as default search)
- Prefer free subscription-based search over pay-per-query APIs

## How to Search

### One-shot Search + Extract Text

```bash
agent-browser open "https://kagi.com/search?q=URL_ENCODED_QUERY" && agent-browser get text
```

Or with `npx` fallback if `agent-browser` is not in PATH:

```bash
npx agent-browser open "https://kagi.com/search?q=URL_ENCODED_QUERY" && npx agent-browser get text
```

**Example:**
```bash
agent-browser open "https://kagi.com/search?q=rust+tokio+async+runtime" && agent-browser get text
```

### Interactive Search (Multi-step)

For complex queries requiring interaction (filtering, clicking tabs):

```bash
agent-browser open "https://kagi.com"
agent-browser type "input[placeholder*='Search']" "your query"
agent-browser press Enter
agent-browser wait 2000
agent-browser get text
```

### Navigate to a Specific Result

After getting search results, extract a URL and deep-dive:

```bash
agent-browser open "URL_FROM_RESULTS" && agent-browser get text
```

## Best Practices

1. **Encode queries**: Replace spaces with `+`, special chars with percent-encoding
2. **Use `get text` for readable output**: Returns page innerText (clean, no HTML)
3. **Use `snapshot` for structure**: When you need to interact with specific elements
4. **Limit result count**: Add `&limit=10` to Kagi URL for shorter output
5. **Chain searches**: First search broad, then follow URLs for deep info

## Limitations

- **Speed**: ~2-5s per page (slower than API's ~100-500ms)
- **Format**: Raw text, not structured JSON
- **Fragility**: May break if Kagi UI changes
- **Requires subscription**: Active Kagi plan needed

## Alternative: Kagi Search API

For high-volume or structured programmatic search:

- **Cost**: $25 per 1,000 queries (2.5¢ each)
- **Status**: Closed beta — email `support@kagi.com` for invite
- **Docs**: https://help.kagi.com/kagi/api/search.html
- **Use when**: Agent needs 10+ searches/hour or structured JSON results

## Related

- [[agent-browser]] — Browser automation tool
- [[my-crawl4ai]] — For crawling entire sites, not single queries
