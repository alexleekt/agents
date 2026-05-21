---
name: my-krea
description: |
  **ALWAYS use when user asks for:** image generation, video generation,
  creating pictures, making visual content, "generate image", "make a video",
  "create a picture", "AI image", "text to image", "text to video".

  **DO NOT use for:** photo editing or retouching, production-grade graphic
  design, video editing, or any non-generative visual tasks.

  Generate images and videos with Krea AI using the mcp2cli-baked CLI.
---

# Krea AI Generation

Generate images and videos via the Krea MCP server, accessed through the
`krea` CLI wrapper (baked mcp2cli tool).

## ⚡ Quick Start

```bash
# Generate an image
krea generate-image --prompt "a cyberpunk cityscape at night" --model flux --width 1024 --height 1024

# Generate a video (image-to-video)
krea generate-video --image_url "https://..." --prompt "camera pans across the scene"

# Check a job status
krea check-status --job_id <job_id>
```

**Image models:** `flux` (default), `flux-pro`, `ideogram`, `imagen-4`, `krea-1`,
`chatgpt-image`, `nano-banana`, `seedream`

## Prerequisites

- `krea_api_key` must be present in chezmoi data (`~/.config/chezmoi/chezmoi.toml`).
- A Fish function wrapper reads the key at runtime and exports it locally for
  the `krea` process only. No global env var needed.
- If missing from chezmoi data, add it under `[data]` in `chezmoi.toml` and run
  `chezmoi apply`.

**How the secret injection works:**

```fish
# In ~/.config/fish/functions/krea.fish
function krea
  set -lx KREA_API_KEY (chezmoi data | jq -r '.krea_api_key // empty')
  command krea $argv
end
```

`set -lx` means the variable is **local to this function call** and exported
only to child processes. It is never visible in the global shell environment.

## Core Workflow

### 1. Discover available commands

```bash
krea --list
krea <command> --help
```

### 2. Generate an image

```bash
krea generate-image --prompt "a cyberpunk cityscape at night" --model flux --width 1024 --height 1024
```

**Image models:** `flux` (default), `flux-pro`, `ideogram`, `imagen-4`,
`krea-1`, `chatgpt-image`, `nano-banana`, `seedream`

**Returns:** `{"job_id": "...", "status": "scheduled", "type": "flux"}`

### 3. Generate a video

```bash
krea generate-video --prompt "ocean waves crashing at golden hour" --model hailuo --duration 5 --aspect-ratio 16:9
```

**Video models:** `hailuo` (default), `kling`, `runway`, `pika`, `veo-3`,
`wan`, `sora`, `luma`

**Aspect ratios:** `16:9`, `9:16`, `1:1`

### 4. Poll for results

All generations are **async**. You get a `job_id`. Poll `get-job` until
`status` is `completed`:

```bash
krea get-job --job-id <job_id>
```

Completed jobs include `result.urls` with the generated media URL.

### 5. Check recent jobs

```bash
krea list-jobs --limit 10 --status completed
```

## Before Generating — Checklist

- **Model**: Which model matches the user's quality/speed needs?
- **Dimensions**: Default is 1024×1024 (images) and 16:9 5s (video).
- **Source image**: For image-to-image or image-to-video, get an asset URL
  first (see Assets below).
- **Async nature**: Tell the user the job is queued. Offer to check status.

## Assets & Uploads

### List uploaded assets

```bash
krea list-assets --limit 10
```

### Upload an asset (URL only)

⚠️ `upload-asset` accepts a **remote URL**, not a local file path.

```bash
krea upload-asset --url "https://example.com/photo.jpg" --name "source-photo"
```

The returned `image_url` can then be passed to `--image-url` for
image-to-image or image-to-video generation.

## Styles & LoRAs

### Search styles

```bash
krea search-styles --query "cyberpunk" --limit 5
```

⚠️ This endpoint often returns `404 - Style not found` even for common
queries. If search fails, proceed without a `style_id`.

### Get style details

```bash
krea get-style --style-id <style_id>
```

## Anti-Patterns & Gotchas

| Issue | Detail |
|---|---|
| **Async by design** | Every `generate-*` returns a `job_id`. Never expect an instant URL. |
| **upload-asset takes URLs only** | `--url https://...` — local file paths will not work. |
| **search-styles is flaky** | Frequently returns 404. Do not block on style lookup. |
| **No `--pretty` flag** | The `krea` CLI outputs raw JSON. Pipe to `jq` or parse directly. |
| **Runtime secret injection** | The Fish function pulls `krea_api_key` from chezmoi data at call time. No global `KREA_API_KEY` env var is kept in the shell. Do not pass secrets via mcp2cli `--env` (stdio bug). |
| **Poll responsibly** | Wait 3–5s between `get-job` polls. Typical generation time: 5–15s. |

## Response Format for Users

**After generation:**
> Queued job `8089cf88-...` (type: flux, status: scheduled). I'll check the result...

**After job completes:**
> ✅ Done! Result: https://gen.krea.ai/images/....png

**If failed:**
> ❌ Job failed: `{status}` — check `list-jobs` for details.

## Examples

```bash
# Image with specific model
krea generate-image --prompt "neon samurai in rain" --model flux-pro --width 1536 --height 1024

# Video from image (i2v)
krea upload-asset --url "https://i.imgur.com/abc123.jpg" --name "base"
# Then use the returned URL:
krea generate-video --prompt "camera slowly zooms out" --image-url "https://gen.krea.ai/assets/..." --model kling --duration 5

# Poll loop
krea get-job --job-id 8089cf88-ce7c-4fcc-80ea-2902a2c9b070
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `krea: command not found` | Check if krea CLI is installed: `which krea` |
| `KREA_API_KEY not set` | Run `chezmoi data \| jq -r '.krea_api_key'` to verify |
| Job stuck in "scheduled" | Poll with `krea check-status --job_id <id>`; jobs take 30-120s |
| Generation fails with "content policy" | Rephrase prompt to avoid disallowed content |
| Image URL returns 403 | Use `krea upload-asset` to host locally first |
| Style search returns 404 | Proceed without `style_id`; style lookup is optional |

## Common Agent Mistakes

❌ **Wrong:** Passing `--url` with a local file path to `upload-asset`
✅ **Right:** `upload-asset` accepts remote URLs only; use `https://...`

❌ **Wrong:** Expecting instant results from `generate-image`
✅ **Right:** Every call returns a `job_id`; poll with `check-status` or `get-job`

❌ **Wrong:** Using `mcp2cli --env` to pass `KREA_API_KEY`
✅ **Right:** Use the Fish wrapper function; it pulls from chezmoi data at runtime

## Related Skills

- **@skills/my-web-search-kagi** — For searching reference images or style inspiration online
- **@skills/my-tech-stack** — For tool recommendations if extending the pipeline
- **@skills/my-workflow** — For commit discipline when saving generated assets to version control
