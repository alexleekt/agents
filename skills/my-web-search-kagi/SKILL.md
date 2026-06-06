---
name: my-web-search-kagi
description: |
  **ALWAYS use when user asks for:** searching the web, looking up information
  online, finding docs, checking prices, researching a topic, verifying facts.
  Also use when no dedicated web search MCP server is available. Triggers on
  phrases like "search the web", "look up", "find online", "google", "kagi search",
  "web search", "search for", or when current/real-time information is needed.

  **DO NOT use for:** questions answerable from training data alone, tasks where
  the user explicitly says "don't search", or when a dedicated MCP search server
  is available and preferred.
---

# Web Search via agent-browser

Perform web searches using browser automation. Kagi is preferred if available,
Bing is the fallback that works without authentication.

## ⚡ Quick Start

**Pick the fastest path for your setup:**

| Path | When to use | One-time setup | Search command |
|------|-------------|---------------|----------------|
| **API** (fastest) | You have a Kagi API token | Get token at [kagi.com/settings?p=api](https://kagi.com/settings?p=api) | `curl -H "Authorization: Bot $KAGI_API_KEY" "https://kagi.com/api/v1/search?q=<query>"` |
| Firefox/Zen/LibreWolf | Browser automation, already logged in | `python3 ~/.pi/agent/skills/my-web-search-kagi/scripts/sync-kagi-cookies.py --browser zen` | `agent-browser open "https://kagi.com/search?q=<query>" && agent-browser get text` |
| Chromium/Chrome/Arc/Brave/Edge | Browser automation, already logged in | `agent-browser open "https://kagi.com"` (reuse profile) | Same as above |
| Any (no Kagi login) | No auth needed | None | `agent-browser open "https://www.bing.com/search?q=<query>" && agent-browser get text` |

## ⚠️ Important: CAPTCHA / Login Requirement

**Kagi search via browser automation is blocked by Cloudflare Turnstile CAPTCHA
unless the browser session has authenticated Kagi cookies.**

The **API path** avoids this entirely. This skill provides **four viable paths**:

---

## Path 0: API Direct (Fastest — Recommended for Programmatic Use)

If you have a Kagi API token, use the official API directly. It's **~10-50x faster**
(~100-500ms) than browser automation and returns structured JSON.

### Prerequisites

- Kagi API token from [kagi.com/settings?p=api](https://kagi.com/settings?p=api)
- Kagi Search API is now in **public preview** — all subscribers get **$5 free API credits**

### Quick search with curl

```bash
# Set your token
export KAGI_API_KEY="your_token_here"

# Search
curl -H "Authorization: Bot $KAGI_API_KEY" \
  "https://kagi.com/api/v1/search?q=rust+tokio+async+runtime"
```

### Python (official `kagiapi` package)

```bash
pip install kagiapi
```

```python
from kagiapi import KagiClient
import os

kagi = KagiClient(os.environ["KAGI_API_KEY"])
results = kagi.search("rust tokio async runtime", limit=10)

for result in results["data"]:
    if result['t'] == 0:  # t=0 is search result, t=1 is related searches
        print(f"{result['title']}\n{result['url']}\n")
```

### MCP Server (official `kagimcp`)

For Claude Desktop, Codex CLI, Cline, or any MCP client:

```bash
# Install uv first (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to Codex CLI
codex mcp add kagi --env KAGI_API_KEY=<YOUR_API_KEY> -- uvx kagimcp

# Or add to Claude Desktop config (~/Library/Application Support/Claude/claude_desktop_config.json)
{
  "mcpServers": {
    "kagi": {
      "command": "uvx",
      "args": ["kagimcp"],
      "env": {
        "KAGI_API_KEY": "your_token_here"
      }
    }
  }
}
```

Tools exposed: `kagi_search_fetch` (web/news/videos/podcasts/images), `kagi_extract` (page as markdown)

### API vs Browser Automation

| Factor | API | Browser Automation |
|--------|-----|-------------------|
| Speed | ~100-500ms | ~2-5s |
| Format | Structured JSON | Raw text |
| Auth | API token | Browser cookies |
| Cost | $25/1,000 queries (2.5¢ each) | Free (uses subscription) |
| Rate limits | Yes (see docs) | No hard limit |
| Best for | 10+ searches/hour, structured data | Occasional searches, no setup |

---

## Path 1: Firefox / Zen / LibreWolf / Waterfox users (Recommended for Browser Automation)

If the user uses a Firefox-variant browser and is already logged into Kagi,
cookies can be synced into agent-browser automatically.

### One-time setup

```bash
# Sync Kagi cookies from Zen (or firefox, librewolf, waterfox, floorp)
python3 ~/.pi/agent/skills/my-web-search-kagi/scripts/sync-kagi-cookies.py --browser zen
```

The script:
1. Finds the browser's default profile
2. Extracts Kagi cookies from `cookies.sqlite`
3. Injects them into the running agent-browser session via CDP

### Search after cookie sync

```bash
agent-browser open "https://kagi.com/search?q=rust+tokio+async+runtime" && agent-browser get text
```

---

## Path 2: Chromium / Chrome / Arc / Brave / Edge users

If the user uses a Chromium-based browser and is logged into Kagi there,
reuse that profile directly.

### One-time setup

```bash
# List available Chrome profiles
agent-browser profiles

# Use the profile that has Kagi logged in (e.g. "Default", "Profile 2", etc.)
agent-browser --profile "Profile 2" open "https://kagi.com"
# If Kagi shows you as logged in, you're done. Otherwise log in once.
```

### Search with persistent profile

Always use `--profile` so the login state is preserved:

```bash
agent-browser --profile "Profile 2" open "https://kagi.com/search?q=QUERY" && agent-browser --profile "Profile 2" get text
```

To avoid typing `--profile` every time, set the env var:

```bash
export AGENT_BROWSER_PROFILE="Profile 2"
agent-browser open "https://kagi.com/search?q=QUERY" && agent-browser get text
```

Or set it in `~/.agent-browser/config.json`:

```json
{"profile": "Profile 2"}
```

---

## Path 3: No Kagi login available → Bing fallback

If neither path 1 nor 2 is viable, use **Bing** as the search engine.
Bing does not block automation and requires no authentication:

```bash
agent-browser open "https://www.bing.com/search?q=QUERY" && agent-browser get text
```

---

## How to Search (General)

### One-shot search + extract

```bash
# Kagi (after cookies synced or profile set)
agent-browser open "https://kagi.com/search?q=URL_ENCODED_QUERY" && agent-browser get text

# Bing (no setup needed)
agent-browser open "https://www.bing.com/search?q=URL_ENCODED_QUERY" && agent-browser get text
```

### Interactive search

```bash
agent-browser open "https://kagi.com"
agent-browser type "input[placeholder*='Search']" "your query"
agent-browser press Enter
agent-browser wait 2000
agent-browser get text
```

### Navigate to a specific result

```bash
agent-browser open "URL_FROM_RESULTS" && agent-browser get text
```

---

## Best Practices

1. **Use API first** — if you have a token, it's 10-50x faster and more reliable
2. **Try Kagi browser automation** — better results, ad-free, respects user's subscription
3. **Sync cookies** for Firefox-variant users via the included script
4. **Reuse Chrome profile** for Chromium users via `--profile`
5. **Fallback to Bing** if Kagi auth is unavailable
6. **Encode queries**: Replace spaces with `+`, special chars with percent-encoding
7. **Use `get text`**: Clean innerText, no HTML clutter
8. **Use `snapshot`**: When you need to interact with specific elements
9. **Chain searches**: Search broad → extract URL → deep-dive

---

## Limitations

- **API requires token**: Must get API key from Kagi settings
- **Browser Kagi requires auth**: Cloudflare Turnstile blocks unauthenticated automation
- **Browser speed**: ~2-5s per page (slower than API's ~100-500ms)
- **Browser format**: Raw text, not structured JSON
- **Browser fragility**: May break if search UI changes
- **Cookie expiry**: If Kagi sessions expire, re-run the sync script or re-login

---

## Alternative: Kagi Search API (Now in Public Preview)

For high-volume or structured programmatic search, the Kagi Search API is now
**publicly available** (no invite needed):

- **Cost**: $25 per 1,000 queries (2.5¢ each)
- **Free credits**: $5 added to all subscriber accounts (May 2026)
- **Status**: Public preview — ready for production use
- **Docs**: https://kagi.com/api/docs
- **Python package**: `pip install kagiapi` ([github.com/kagisearch/kagiapi](https://github.com/kagisearch/kagiapi))
- **MCP server**: `uvx kagimcp` ([github.com/kagisearch/kagimcp](https://github.com/kagisearch/kagimcp))
- **Use when**: Agent needs 10+ searches/hour or structured JSON results

See **Path 0** above for setup instructions.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API returns 401 Unauthorized | Check `KAGI_API_KEY` is set and token is valid at kagi.com/settings?p=api |
| API returns 429 Rate Limited | Slow down requests or check Kagi API rate limits |
| Kagi returns CAPTCHA page | Cookies expired → re-run sync script or use Bing fallback |
| `agent-browser` not found | Install pi extension: `pi extensions install agent-browser` |
| Cookie sync script fails | Check browser is installed: `which zen` or `which firefox` |
| Results are stale/old | Check URL includes current year or recent terms |
| Blank page after navigate | Wait for JS to load: add `sleep 2` or use `wait_for_selector` |
| Search results truncated | Use `get text` for full page; `snapshot` for structured DOM |

## Common Agent Mistakes

❌ **Wrong:** Searching for information already in training data alone
✅ **Right:** Use search only for current/real-time info or specific facts not in training data

❌ **Wrong:** Using browser automation when you have an API token
✅ **Right:** Use the API (Path 0) for speed and reliability; save browser automation for when you don't have a token

❌ **Wrong:** Using Kagi browser automation without checking cookies first
✅ **Right:** Verify cookie sync worked before relying on Kagi results; fall back to Bing if needed

❌ **Wrong:** Falling back to Bing when Kagi API or browser automation works fine
✅ **Right:** Only use Bing fallback when Kagi is unavailable or unauthenticated

❌ **Wrong:** Using web search for tasks better suited to API calls
✅ **Right:** Use httpie/curl for known endpoints; web search is for discovery, not repeated API work

## Related Skills & Tools

- **@skills/my-crawl4ai** — For crawling entire sites, not single search queries
- **@skills/my-tech-stack** — For tool recommendations (httpie vs curl, etc.)
- **@skills/cua-computer-use** — For GUI interactions when browser automation isn't sufficient
- **Official Kagi MCP Server** — `uvx kagimcp` for Claude Desktop, Codex CLI, Cline ([github.com/kagisearch/kagimcp](https://github.com/kagisearch/kagimcp))
- **Official Kagi Python Package** — `pip install kagiapi` ([github.com/kagisearch/kagiapi](https://github.com/kagisearch/kagiapi))
