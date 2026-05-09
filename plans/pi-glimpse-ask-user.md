# Plan: pi-glimpse-ask-user Plugin

## Context

Create a new Pi extension that leverages **`glimpseui`** (native WebView micro-UI) to replace the interactive user-prompt capabilities of two existing packages:

- **`npm:pi-ask-user`** — Terminal-based TUI with searchable single/multi-select, freeform input, split-pane preview, overlay/inline modes, and `ask_user` tool integration.
- **`npm:@juicesharp/rpiv-ask-user-question`** — Structured questionnaire system with typed options, tab-based navigation, and stateful sessions.

**Goal:** A single native-WebView-based Pi extension that registers the `ask_user` tool (replacing any existing implementation) and a `/ask` slash command, rendering rich HTML dialogs via `glimpseui`. Lives in `~/git/pi-ask-user-glimpse` and is symlinked into this repo for Pi discovery.

## What We Know

### pi-ask-user Features (to port)
- Searchable single-select option lists with wrapped titles + descriptions
- Multi-select option lists
- Optional freeform responses
- Split-pane details preview
- User-toggleable extra context on structured selections
- Structured `details` on all results for session state reconstruction
- Graceful fallback when interactive UI unavailable

**Not porting:** overlay/inline display modes (WebView is inherently a separate dialog), timeouts, `ask-user` skill (extension-only approach).

### rpiv-ask-user-question Features (to port)
- Structured questionnaire the model can pose instead of guessing
- Typed options (not free-form)
- Tab-based UI components
- Stateful questionnaire sessions
- Response formatting + validation

**Not porting:** i18n bridge.

### glimpseui Capabilities
- Native WebView window (macOS WKWebView, Linux GTK4/WebKitGTK, Windows WebView2)
- Node.js API: `open(html, options)`, `prompt(html, options)` → Promise
- Window flags: `frameless`, `floating`, `transparent`, `clickThrough`, `noDock`
- JSON Lines protocol over stdin/stdout
- `window.glimpse.send(data)` from HTML → host receives `{type:"message",data}`
- Pi package installable via `pi install npm:glimpseui`
- `prompt()` is one-shot: opens, waits for first message, closes, returns data/null

## Decisions

| Topic | Decision |
|-------|----------|
| **Package name** | `@alexleekt/pi-ask-user-glimpse` (npm) |
| **Repo location** | `~/git/pi-ask-user-glimpse` (new repo), symlinked here for Pi discovery |
| **Tool name** | `ask_user` — **intentionally replaces** existing `ask_user` from `pi-ask-user` / `rpiv-ask-user-question` |
| **Registration** | Pi **extension** (`pi.extensions`) only |
| **Slash command** | `/ask` |
| **UI framework** | **shadcn/ui design system** via React app bundled with Vite + Tailwind CSS |
| **Window style** | Titled window, normal stacking (not floating), **centered dialog** |
| **Cursor following** | Off by default; available as a configurable option |
| **Fallback** | Terminal-based `readline` prompt when `glimpseui` binary is missing or fails |
| **Excluded features** | No i18n, no timeout auto-dismiss |
| **Removed feature** | Escalation notifications (cancelled) |

## Open Questions (Resolved)

1. **Cursor-follow** — Configurable option, off by default.
2. **ask_user replacement strategy** — Detect existing `pi-ask-user` / `rpiv-ask-user-question` and **warn that it may conflict**.
3. **shadcn component scope** — Use a **lightweight React app** inside the Glimpse WebView for maintainability. Bundle React + Tailwind + shadcn primitives via Vite build.
4. **Questionnaire layout** — Render questions as **cards/containers in a vertical list** inside one dialog, not tabs or sequential windows.

## Proposed Approach

### Architecture
- **Pi extension entry** (`index.ts`): registers the `ask_user` tool and `/ask` slash command via Pi's extension API.
- **Tool handler** (`tool/ask-user.ts`): receives the question/options payload, constructs shadcn-styled HTML, and calls `glimpseui.prompt()`.
- **WebView React app** (`webview/`): a Vite-built React + Tailwind + shadcn-styled app. The extension builds it and embeds the compiled HTML/JS/CSS string into the payload sent to `glimpseui.prompt()`.
  - Prompt types rendered as React components:
    - `SingleSelect` — searchable list with details preview pane
    - `MultiSelect` — checkbox list with submit/cancel
    - `Questionnaire` — cards/containers in a vertical list
    - `Freeform` — textarea + submit
- **Result formatter** (`tool/response-formatter.ts`): normalizes the WebView response into the same structured `details` format both legacy packages use, ensuring backward compatibility.
- **Fallback layer** (`fallback/terminal-prompt.ts`): if `glimpseui` binary is missing or fails to spawn, falls back to a minimal terminal `readline` prompt.


### Files to Create
- `package.json` — `pi.extensions` metadata, `glimpseui` dependency, no `pi.skills`
- `index.ts` — extension entrypoint: tool + slash command registration
- `tool/ask-user.ts` — main tool handler, payload validation, HTML dispatch
- `tool/response-formatter.ts` — normalize WebView payload → Pi-compatible result
- `fallback/terminal-prompt.ts` — readline-based fallback when `glimpseui` is unavailable
- `util/detect-conflict.ts` — warn if `pi-ask-user` or `rpiv-ask-user-question` is also loaded
- `webview/` — Vite-built React app for the Glimpse HTML payload:
  - `webview/src/App.tsx` — root component, routes between prompt types
  - `webview/src/components/SingleSelect.tsx` — shadcn-styled searchable single-select
  - `webview/src/components/MultiSelect.tsx` — shadcn-styled multi-select
  - `webview/src/components/Questionnaire.tsx` — shadcn-styled questionnaire as cards in a list
  - `webview/src/components/Freeform.tsx` — shadcn-styled textarea
  - `webview/src/components/PreviewPane.tsx` — split-pane details preview
  - `webview/src/index.css` — Tailwind + shadcn token CSS
  - `webview/index.html` — entry HTML
  - `webview/vite.config.ts` — build config

### Reuse
- `glimpseui`'s own `prompt()` API handles the full open/send/close lifecycle.
- shadcn/ui primitives (Button, Card, Input, Checkbox, RadioGroup, ScrollArea, etc.) via `@radix-ui/react-*` or equivalent lightweight headless components, styled with Tailwind.
- Vite `build.lib` or `build.rollupOptions` to bundle the webview into a single self-contained HTML string that can be passed to `glimpseui`.

### Verification
- `npm run check` (dry-run pack)
- `pi install npm:pi-ask-user-glimpse` in a test project
- Manual test: invoke `ask_user` with single-select, multi-select, questionnaire, freeform payloads
- Conflict test: install alongside `pi-ask-user` and verify ours takes precedence
- Fallback test: temporarily remove `glimpseui` binary and verify terminal fallback works
- Platform test: validate on macOS and Linux (Windows optional)


