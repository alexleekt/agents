---
name: my-krea
description: |
  **ALWAYS use when user asks for:** image generation, video generation,
  creating pictures, making visual content, "generate image", "make a video",
  "create a picture", "AI image", "text to image", "text to video".

  **DO NOT use for:** photo editing or retouching, production-grade graphic
  design, video editing, or any non-generative visual tasks.

  Generate images and videos with Krea AI using the official Krea CLI.
---

# Krea AI Generation

Generate images and videos via the official Krea CLI (`@krea-ai/cli`).

## ⚡ Quick Start

```bash
# Generate an image (async by default)
krea generate image -p "a cyberpunk cityscape at night" -m bfl/flux-1-dev --width 1024 --height 1024

# Generate and download immediately
krea generate image -p "..." -o ./output.png

# Generate a video
krea generate video -p "ocean waves crashing at golden hour" -m hailuo/mini-max --duration 5

# Check a job status
krea jobs wait <job_id>
```

## Prerequisites

- Install the CLI: `npm install -g @krea-ai/cli`
- Set `KREA_API_KEY` in your environment, or run `krea auth login` to store credentials.
- Verify with `krea doctor`

## Core Workflow

### 1. Discover available commands

```bash
krea --help
krea generate image --help
krea models list          # list all models
krea models list --json | jq '.[] | select(.category=="image") | .id'
```

### 2. Generate an image

```bash
krea generate image -p "a cyberpunk cityscape at night" -m bfl/flux-1-dev --width 1024 --height 1024
```

**Image models:** `bfl/flux-1-dev` (default), `bfl/flux-1.1-pro`, `bfl/flux-1.1-pro-ultra`,
`google/imagen-4`, `google/nano-banana`, `ideogram/ideogram-3`, `openai/gpt-image-2`,
`bytedance/seedream-5-lite`, `luma/uni-1`

**Returns:** `{"job_id": "...", "status": "completed", "urls": ["https://..."]}`

### 3. Generate a video

```bash
krea generate video -p "ocean waves crashing at golden hour" -m hailuo/mini-max --duration 5 --aspect 16:9
```

**Video models:** `hailuo/mini-max`, `kling/kling-2`, `runway/gen-4`, `pika/pika-2`,
`google/veo-3`, `luma/dream-machine`, `openai/sora`

**Aspect ratios:** `16:9`, `9:16`, `1:1`

### 4. Poll for results / download

All generations are **async** unless you use `--wait` or `-o`.

```bash
# Block until complete and print URL
krea generate image -p "..." --wait

# Block and save to file (implies --wait)
krea generate image -p "..." -o ./result.png

# Or manually poll
krea jobs wait <job_id>
```

Completed jobs include `urls` with the generated media URL. When using `-o`, the file is saved locally and the path is returned as `saved_path`.

### 5. Check recent jobs

```bash
krea jobs list --limit 10
```

## Before Generating — Checklist

- **Model**: Which model matches the user's quality/speed needs?
- **Dimensions**: Default is 1024×1024 (images) and 16:9 5s (video).
  - `bfl/flux-1.1-pro` max width: **1440px**
- **Source image**: For image-to-image, pass `--image <url>`.
- **Async nature**: Without `--wait` or `-o`, the job is queued and a `job_id` is returned. Offer to check status.

## Assets & Uploads

### Upload an asset (local file)

```bash
krea upload ./photo.jpg --name "source-photo"
```

The returned URL can then be passed to `--image` for image-to-image or video generation.

## Anti-Patterns & Gotchas

| Issue | Detail |
|---|---|
| **Async by design** | Without `--wait` or `-o`, only a `job_id` is returned. Use `krea jobs wait` to block. |
| **`-o` implies `--wait`** | When you specify an output path, the CLI blocks until the file is downloaded. |
| **Max width for flux-1.1-pro** | `bfl/flux-1.1-pro` has a max width of **1440px**. Use `bfl/flux-1-dev` for 1536px. |
| **Model IDs changed** | Old skill used `flux-pro`; new CLI uses `bfl/flux-1.1-pro`. Always check `krea models list`. |
| **No `--pretty` flag** | The CLI outputs raw JSON. Pipe to `jq` or parse directly. Use `--json` for machine-readable. |
| **Secret injection** | The CLI reads `KREA_API_KEY` from env or the system keyring (set via `krea auth login`). |
| **Poll responsibly** | Wait 3–5s between job polls. Typical generation time: 5–15s for images, 30–120s for video. |

## Response Format for Users

**After generation (async):**
> Queued job `8089cf88-...` (type: flux, status: scheduled). I'll check the result...

**After generation (with `-o` or `--wait`):**
> ✅ Done! Saved to `./result.png` (also available at https://gen.krea.ai/images/....png)

**If failed:**
> ❌ Job failed: `{status}` — check `krea jobs list` for details.

## Examples

```bash
# Image with specific model and output file
krea generate image -p "neon samurai in rain" -m bfl/flux-1.1-pro --width 1440 --height 480 -o ./banner.png

# Video from image
krea generate video -p "camera slowly zooms out" --image "https://gen.krea.ai/assets/..." -m kling/kling-2 --duration 5

# Poll loop for a known job
krea jobs wait 5d95517b-3c44-4a38-95eb-1bbdb3dbf118
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `krea: command not found` | `npm install -g @krea-ai/cli` |
| `krea doctor` fails on auth | `krea auth login` or `export KREA_API_KEY=...` |
| `422 Validation failed` | Check `width`/`height` limits for the chosen model (`krea models show <id>`) |
| Job stuck in "scheduled" | `krea jobs wait <id>` blocks until terminal; typical time is 30–120s |
| Generation fails with "content policy" | Rephrase prompt to avoid disallowed content |

## Migration from mcp2cli

If you previously used `mcp2cli @krea`, migrate to the native CLI:

```bash
npm install -g @krea-ai/cli
rm ~/.local/bin/krea   # remove old mcp2cli wrapper if present
```

Key syntax changes:
- `krea generate-image` → `krea generate image`
- `krea get-job` → `krea jobs wait`
- `krea list-jobs` → `krea jobs list`
- `krea upload-asset` → `krea upload`

## Related Skills

- **@skills/my-web-search-kagi** — For searching reference images or style inspiration online
- **@skills/my-tech-stack** — For tool recommendations if extending the pipeline
- **@skills/my-workflow** — For commit discipline when saving generated assets to version control
