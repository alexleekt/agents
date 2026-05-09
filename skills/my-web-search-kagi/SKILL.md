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
unless the browser session has authenticated Kagi cookies.**

This skill provides **three viable paths** depending on what browser the user uses.

---

## Path 1: Firefox / Zen / LibreWolf / Waterfox users (Recommended)

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

1. **Try Kagi first** — better results, ad-free, respects user's subscription
2. **Sync cookies** for Firefox-variant users via the included script
3. **Reuse Chrome profile** for Chromium users via `--profile`
4. **Fallback to Bing** if Kagi auth is unavailable
5. **Encode queries**: Replace spaces with `+`, special chars with percent-encoding
6. **Use `get text`**: Clean innerText, no HTML clutter
7. **Use `snapshot`**: When you need to interact with specific elements
8. **Chain searches**: Search broad → extract URL → deep-dive

---

## Limitations

- **Kagi requires auth**: Cloudflare Turnstile blocks unauthenticated automation
- **Speed**: ~2-5s per page (slower than API's ~100-500ms)
- **Format**: Raw text, not structured JSON
- **Fragility**: May break if search UI changes
- **Cookie expiry**: If Kagi sessions expire, re-run the sync script or re-login

---

## Alternative: Kagi Search API

For high-volume or structured programmatic search:

- **Cost**: $25 per 1,000 queries (2.5¢ each)
- **Status**: Closed beta — email `support@kagi.com` for invite
- **Docs**: https://help.kagi.com/kagi/api/search.html
- **Use when**: Agent needs 10+ searches/hour or structured JSON results

---

## Related

- [[agent-browser]] — Browser automation tool
- [[my-crawl4ai]] — For crawling entire sites, not single queries
