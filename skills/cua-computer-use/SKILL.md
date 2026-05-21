---
name: cua-computer-use
description: |
  **ALWAYS use when user asks for:** computer-use, screen control, UI automation,
  app automation, clicking elements, typing text, taking screenshots, or controlling
  macOS apps programmatically.

  **Assumption:** Any request involving GUI interaction, screenshots, or app control
  on macOS should use cua-driver tools via this skill.

  **DO NOT use for:** headless/scripted automation that doesn't need visual/GUI
  interaction (use shell scripts instead).
---

# cua-computer-use

Computer-use automation via the CuaDriver macOS app. Provides screen control, app automation, and UI interaction capabilities for Pi.

## Prerequisites

- CuaDriver.app installed at `/Applications/CuaDriver.app` (v0.1.5+)
- macOS Accessibility and Screen Recording permissions granted to CuaDriver

## ⚡ Quick Start

All tools are invoked via the `cua-pi` wrapper (auto-starts daemon if needed):

```bash
# List all available tools
cua-pi list-apps          # List running/installed macOS apps
cua-pi list-windows       # List all top-level windows with window_ids
cua-pi screenshot '{"window_id":1234}'  # Capture a window screenshot
cua-pi click '{"pid":844,"element_index":5}'  # Click a UI element
cua-pi type-text '{"pid":844,"text":"hello"}'  # Type text into an app
cua-pi press-key '{"pid":844,"key":"return"}'  # Press a key
cua-pi hotkey '{"pid":844,"keys":["command","c"]}'  # Press hotkey combo
cua-pi move-cursor '{"x":100,"y":200}'  # Move mouse cursor
cua-pi get-window-state '{"pid":844,"window_id":1234}'  # Get UI tree as markdown
cua-pi check-permissions   # Verify TCC permission status
cua-pi get-screen-size     # Get display dimensions
```

**Tool names use underscores** (e.g. `list_apps`, `get_window_state`). The wrapper handles them as-is.

## Common Workflows

### Inspect an app's UI

1. Find the app: `cua-pi list-apps | jq '.apps[] | select(.name=="Safari")'`
2. Find its window: `cua-pi list-windows | jq '.windows[] | select(.app_name=="Safari")'`
3. Get UI tree: `cua-pi get-window-state '{"pid":123,"window_id":456}'`

### Interact with a web page

1. Get window state to find element indices
2. Click: `cua-pi click '{"pid":123,"element_index":5}'`
3. Type: `cua-pi type-text '{"pid":123,"text":"search query"}'`
4. Press key: `cua-pi press-key '{"pid":123,"key":"return"}'`

### Take a screenshot

```bash
cua-pi list-windows | jq '.windows[0].window_id'
cua-pi screenshot '{"window_id":<id>,"format":"png"}'
```

## Important Notes

- **Permissions**: If tools silently fail or return empty results, run `cua-pi check-permissions`. CuaDriver needs both Accessibility and Screen Recording in System Settings → Privacy & Security.
- **Window ID required**: Most interaction tools need a `window_id` from `list-windows`.
- **PID vs Bundle ID**: Some tools take `pid` (process ID), others take `bundle_id`. Check tool schemas with `cua-driver describe <tool>`.
- **Daemon mode**: The wrapper auto-starts the cua-driver daemon via `open -n -g -a CuaDriver --args serve` if not running. The daemon preserves the AppStateEngine cache across calls and ensures TCC permissions are attributed to CuaDriver.app.
- **JSON arguments**: Always pass valid JSON. Use single quotes around the JSON string in bash.

## Python Integration

For complex automation, use the Python SDK directly:

```python
# ~/.cua-venv is the virtual environment with cua packages installed
import subprocess, json

def cua_call(tool: str, args: dict) -> dict:
    result = subprocess.run(
        ["/Applications/CuaDriver.app/Contents/MacOS/cua-driver", "call", tool, json.dumps(args)],
        capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)

# Example: list apps
apps = cua_call("list_apps", {})
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cua-driver: command not found` | PATH issue | Use full path `/Applications/CuaDriver.app/Contents/MacOS/cua-driver` |
| Empty screenshots | Missing Screen Recording permission | Grant in System Settings → Privacy & Security |
| Click/type has no effect | Missing Accessibility permission | Grant in System Settings → Privacy & Security |
| `check_permissions` shows false | TCC not granted | Open CuaDriver.app GUI once, or manually add in System Settings |

## Links

- Cua repo: https://github.com/trycua/cua
- CuaDriver is the macOS native driver component of the cua project
- For sandboxes (Linux VMs), see cua-sandbox documentation at https://cua.ai/docs
