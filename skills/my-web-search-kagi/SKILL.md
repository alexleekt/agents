---
name: my-web-search-kagi
description: >
  Search the web using agent-browser. Use this skill whenever the user wants to
  search the web, find information online, look up docs, check prices, research a
  topic, or verify facts. Also use when no dedicated web search MCP server is
  available. Triggers on phrases like "search the web", "look up", "find online",
  "google", "kagi search", "web search", "search for", or when the agent needs
  current/real-time information not in its training data.
---

# Web Search via agent-browser

Perform web searches using browser automation. Kagi is preferred if available,
Bing is the fallback that works without authentication.

## ⚠️ Important: CAPTCHA / Login Requirement

**Kagi search via browser automation is blocked by Cloudflare Turnstile CAPTCHA
unless the browser is logged into a Kagi account.**

### To use Kagi (recommended, best results)

You must log in once. The agent-browser Chrome instance does NOT share cookies
with your regular Chrome browser.

**One-time setup:**
```bash
agent-browser open "https://kagi.com"
# Manually sign in with your Kagi credentials in the opened browser
# Once logged in, the session persists for subsequent agent-browser runs
```

After login, Kagi search works:
```bash
agent-browser open "https://kagi.com/search?q=URL_ENCODED_QUERY" && agent-browser get text
```

### To use Bing (no login needed, works immediately)

If Kagi is not logged in, fall back to Bing — it does not block automation:

```bash
agent-browser open "https://www.bing.com/search?q=URL_ENCODED_QUERY" && agent-browser get text
```

## How to Search

### 1. Preferred: Kagi (after login)

```bash
agent-browser open "https://kagi.com/search?q=rust+tokio+async+runtime" && agent-browser get text
```

### 2. Fallback: Bing (no login required)

```bash
agent-browser open "https://www.bing.com/search?q=rust+tokio+async+runtime" && agent-browser get text
```

### 3. Interactive search (if UI interaction needed)

```bash
agent-browser open "https://kagi.com"   # or https://www.bing.com
agent-browser type "input[placeholder*='Search']" "your query"
agent-browser press Enter
agent-browser wait 2000
agent-browser get text
```

### 4. Navigate to a specific result

After getting search results, extract a URL and deep-dive:

```bash
agent-browser open "URL_FROM_RESULTS" && agent-browser get text
```

## Best Practices

1. **Try Kagi first** if the user has a subscription and may have logged in previously
2. **Fallback to Bing** if Kagi hits a CAPTCHA / login wall
3. **Encode queries**: Replace spaces with `+`, special chars with percent-encoding
4. **Use `get text` for readable output**: Returns page innerText (clean, no HTML)
5. **Use `snapshot` for structure**: When you need to interact with specific elements
6. **Chain searches**: First search broad, then follow URLs for deep info

## Limitations

- **Kagi requires login**: Cloudflare blocks unauthenticated Kagi searches from automation
- **Speed**: ~2-5s per page (slower than API's ~100-500ms)
- **Format**: Raw text, not structured JSON
- **Fragility**: May break if search UI changes

## Alternative: Kagi Search API

For high-volume or structured programmatic search:

- **Cost**: $25 per 1,000 queries (2.5¢ each)
- **Status**: Closed beta — email `support@kagi.com` for invite
- **Docs**: https://help.kagi.com/kagi/api/search.html
- **Use when**: Agent needs 10+ searches/hour or structured JSON results

## Related

- [[agent-browser]] — Browser automation tool
- [[my-crawl4ai]] — For crawling entire sites, not single queries
