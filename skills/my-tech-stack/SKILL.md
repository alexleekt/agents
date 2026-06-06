---
name: my-tech-stack
description: |
  **MANDATORY REFERENCE** for all tool recommendations. ALWAYS consult BEFORE
  suggesting tools, libraries, frameworks, or technologies.

  **ALWAYS use when user asks about:** preferred tools, tech recommendations
  ("bun or node", "uv or pip"), or stack decisions.

  **ALWAYS use when agent decides:** to install a package, add a dependency,
  choose a library/framework, select a build tool, or make any technology choice
  that affects the project's stack.

  **DO NOT use for:** agent configuration (@skills/my-agent-file-conventions) or VCS
  operations.

  **CRITICAL:** Do NOT suggest unlisted tools without asking first.
---

# Technology Preferences

Preferred tools and technologies. Defaults, not hard rules.

> **Note:** This is a living document. Preferences evolve as new tools emerge and requirements change. Check the latest version before making decisions.

## ⚡ Quick Start

**Starting a new project?** Default stack:

```bash
# JavaScript/TypeScript
bun init              # Runtime + package manager
biome init            # Lint + format
just --init           # Task runner (optional)

# Python
uv init               # Python project + deps
uv add pytest         # Testing

# Version control
git init
```

**Quick decision guide:**
| Need | Use |
|------|-----|
| JS/TS runtime | **bun** |
| Python packages | **uv** |
| Lint/format | **biome** (JS/TS) |
| Search code | **ripgrep** (`rg`) |
| Find files | **fd** |
| Tasks | **just** |
| Editor | **zed** |

## Prerequisites

- **OS:** macOS (desktop), Ubuntu (servers)
- **Shell:** Any (examples work in bash/zsh/fish)
- **Package managers:** Homebrew (macOS), system package manager (Linux)

## How to Use This

When working with this user:

1. **Check this file first** — Before suggesting tools, consult these preferences
2. **Prefer listed tools** — When multiple solutions exist, default to these
3. **Respect "Exploring"** — Tools marked as exploring are for learning only
4. **Ask before adding** — Don't install unlisted tools without confirmation
5. **Note deviations** — If project requirements override preferences, document it

## Automatic Agent Invocation

**The agent must self-trigger this skill** — not just when the user asks, but when the agent itself is about to make a technology decision. This includes:

| Agent Action | Must Check my-tech-stack? |
|--------------|---------------------------|
| Installing a new npm/pip/cargo package | ✅ YES |
| Adding a dependency to package.json/pyproject.toml/Cargo.toml | ✅ YES |
| Choosing between two libraries/frameworks | ✅ YES |
| Selecting a build tool, linter, or formatter | ✅ YES |
| Adding a new dev tool to the project | ✅ YES |
| Recommending a runtime (bun vs node, uv vs pip) | ✅ YES |
| Choosing a testing framework | ✅ YES |
| Adding infrastructure tools (docker, terraform, k3s) | ✅ YES |
| Using a code search tool (rg vs grep vs ag) | ✅ YES |
| Standard library usage (e.g., `fetch` vs `axios`) | ⚠️ Prefer listed preferences |

### Decision Flow

```
Agent about to recommend/install a tool?
├── Is it in the preferred list above? → Use it
├── Is it in the "Exploring" section? → Ask user before using
├── Is it unlisted? → Ask user: "This tool isn't in my preferred stack. Use it anyway?"
└── Is there a project-specific override? → Follow project, note deviation
```

**Example self-trigger:**
> "I need to add a JSON parser. Checking @skills/my-tech-stack... The project uses TypeScript with bun. I'll use a native solution or check if `yaml` is already preferred for config."

**Never silently install unlisted tools.** Always consult this skill first, even when the user hasn't explicitly asked.

## By Category

### Development Environment

| Tool | When to Use |
|------|-------------|
| [**bun**](https://github.com/oven-sh/bun) | JavaScript/TypeScript runtime and package manager; fast installs, running JS/TS scripts, Node.js alternative |
| [**fd**](https://github.com/sharkdp/fd) | Fast, user-friendly alternative to `find`; searching for files and directories |
| [**fzf**](https://github.com/junegunn/fzf) | Fuzzy finder for command-line; interactive filtering of lists, files, command history, process management |
| [**github**](https://github.com/) | Git hosting; code collaboration; CI/CD with Actions; issue tracking |
| [**homebrew**](https://brew.sh/) | Installing system-wide dependencies, dev tools, macOS applications; preferred package manager for macOS |
| [**mise**](https://github.com/jdx/mise) | Managing multiple language versions, project-specific tool versions, unified version management across teams |
| [**ripgrep**](https://github.com/BurntSushi/ripgrep) (`rg`) | Fast, recursive text search; code searching across large codebases; faster alternative to grep |
| [**typescript**](https://www.typescriptlang.org/) | Type-safe JavaScript development; large-scale JS applications; better IDE support |
| [**uv**](https://github.com/astral-sh/uv) | Managing Python dependencies, virtual environments, Python version/package isolation |
| [**zed**](https://zed.dev/) | Primary code editor; fast, collaborative, Rust-based IDE |

### AI Agents

| Tool | When to Use |
|------|-------------|
| [**pi-coding-agent**](https://github.com/mariozechner/pi) | **Primary coding agent** — preferred harness for agent-driven development |
| [**opencode**](https://opencode.ai/) | Alternative agent harness; use when pi is unavailable |

### AI Providers

| Provider | When to Use |
|----------|-------------|
| [**fireworks**](https://fireworks.ai/) | **Default LLM provider** — fast inference, FirePass intelligent routing, cost-effective |
| [**firepass**](https://fireworks.ai/models?show=Serverless&filters=firepass) | Intelligent model routing; automatically selects optimal model for the task |

### Code Quality

| Tool | When to Use |
|------|-------------|
| [**biome**](https://github.com/biomejs/biome) | Fast linting and formatting for JavaScript/TypeScript/CSS; faster alternative to ESLint + Prettier |

#### Biome Configuration

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 4
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "trailingCommas": "all"
    }
  }
}
```

- **Indentation**: 4 spaces (not tabs)
- **Quote style**: double
- **Trailing commas**: `all` — always use trailing commas in arrays, objects, and function parameters
- Apply to all JS/TS projects using Biome

### Infrastructure & Cloud

| Tool | When to Use |
|------|-------------|
| [**cloudflare**](https://www.cloudflare.com/) | DNS management, CDN, DDoS protection, serverless workers, fast global edge network |
| [**colima**](https://github.com/abiosoft/colima) | **Default container runtime** — macOS Docker-compatible containers via Lima; free, open source, fast |
| [**docker**](https://www.docker.com/) | Container CLI and compose; used alongside colima as the client interface |
| [**k3s**](https://github.com/k3s-io/k3s) | Lightweight Kubernetes for edge, IoT, CI/CD, resource-constrained environments |
| [**terraform**](https://github.com/hashicorp/terraform) | Infrastructure as Code for provisioning cloud resources; multi-cloud or complex infrastructure |

**Colima vs alternatives:**
| | Colima | OrbStack | Docker Desktop | Finch |
|---|---|---|---|---|
| License | Apache 2.0 (OSS) | Proprietary | Proprietary | Apache 2.0 (OSS) |
| Cost | Free | Free / $8 Pro | Free / Enterprise | Free |
| Performance | Good | Excellent | Moderate | Good |
| UX | CLI-only | GUI app | GUI app | CLI-only |

**Preference:** Colima — best open-source license, modern macOS standard, CLI-native workflow.

### Local Development

| Tool | When to Use |
|------|-------------|
| [**portless**](https://github.com/unkeyed/portless) | Clean, memorable local URLs instead of `localhost:3000`; working with multiple local services |

### API & Testing

| Tool | When to Use |
|------|-------------|
| [**httpie**](https://github.com/httpie/cli) | **Default for API work** — testing APIs, debugging endpoints, agent workflows; natural syntax, auto JSON formatting |
| **curl** | Production scripts, CI/CD pipelines, binary data handling, systems where Python isn't available |

**httpie vs curl decision guide:**
| Situation | Use |
|-----------|-----|
| API exploration, debugging | **httpie** — `http GET api.example.com/users page==1` |
| Production deployment scripts | **curl** — universally available, reliable exit codes |
| Agent-driven workflows | **httpie** — more readable in logs, less flag memorization |
| JSON-heavy APIs | **httpie** — native JSON support, auto-pretty-printing |
| Binary file downloads | **curl** — more robust for non-text data |
| CI/CD pipelines | **curl** — no dependency on Python/HTTPie |

### Security & Secrets

| Tool | When to Use |
|------|-------------|
| [**bitwarden**](https://bitwarden.com/) / [**bws**](https://github.com/bitwarden/sdk) | Password management, secure secret storage; bws CLI for programmatic access in scripts and CI/CD |
| [**wireguard**](https://www.wireguard.com/) | Simple, fast, modern VPN; secure point-to-point connections; mesh networking |

### Remote Access

| Tool | When to Use |
|------|-------------|
| [**eternal-terminal**](https://github.com/MisterTea/EternalTerminal) | Remote shell that auto-reconnects without interrupting session; resilient alternative to SSH |
WR:
NV:### Web Frameworks
NV:
QB:| Tool | When to Use |
KR:|------|-------------|
HP:|[**SvelteKit**](https://svelte.dev/) | Preferred full-stack framework; minimal JS, compile-time optimizations |
HP:|[**React**](https://react.dev/) | When ecosystem/project requirements demand it; fallback option |
KR:
VZ:
NV:### Task Automation

| Tool | When to Use |
|------|-------------|
| [**just**](https://github.com/casey/just) | Running project tasks, build scripts, command shortcuts; Makefile replacement with better cross-platform support |
| [**mise**](https://github.com/jdx/mise) (tasks) | Defining and running project tasks when already using mise for version management |

### Operating System

| Context | Preference |
|---------|------------|
| **Desktop** | [**macOS**](https://www.apple.com/macos/) — Primary development and daily driver |
| **Servers** | [**Ubuntu**](https://ubuntu.com/) — Server environments, cloud VMs, production deployments |

### Shell

| Context | Preference | Notes |
|---------|------------|-------|
| **Interactive** | [**fish**](https://fishshell.com/) | Daily command-line work; autosuggestions, syntax highlighting |
| **Scripts / Agents** | [**zsh**](https://www.zsh.org/) | Automation; compatibility with existing bash scripts |

## Exploring

These tools are for learning and experimentation, not production use:

| Tool | Interest |
|------|----------|
| [**chat-sdk**](https://chat-sdk.dev/) | Building AI chat interfaces, streaming LLM responses |
| [**devbox**](https://www.jetify.com/devbox) | Nix-based reproducible dev environments; exploring alongside mise + smolvm |
| [**dotenvx**](https://github.com/dotenvx/dotenvx) | Managing environment variables across environments, encrypting secrets |
| [**gridland**](https://www.gridland.io/) | Building terminal apps with React and OpenTUI; works in both browser and terminal |
| [**endeavouros**](https://endeavouros.com/) | Arch-based Linux distribution; exploring as alternative desktop/server OS |
| [**json-render**](https://github.com/vercel-labs/json-render) | Rendering JSON as UI components; quick admin dashboards |
| [**memex**](https://github.com/iamtouchsky/memex) | Zettelkasten-based agent memory with bidirectional links; installed as pi package |
| [**smolvm**](https://github.com/smol-machines/smolvm) | MicroVMs for sandboxing untrusted code, portable executables, isolated dev environments |
| [**mastra**](https://github.com/mastra-ai/mastra) | Building AI agents, orchestrating LLM workflows |
| [**rust**](https://www.rust-lang.org/) | Systems programming, performance-critical apps, WebAssembly, CLI tools |
| [**varlock.dev**](https://varlock.dev/) | Securely sharing environment variables with team members |
| [**raganything**](https://github.com/HKUDS/RAG-Anything) | Multimodal RAG system for documents with images, tables, and equations |

## Quick Decision Reference

### Starting a new project?
- Use **bun** for JS/TS runtime and package management
- Use **TypeScript** for type safety
- Use **biome** for linting/formatting
- Use **zed** as code editor
RH:- Use **mise** for version management
RH:- Use **SvelteKit** for web framework (when applicable)

### Need to search code?
- Use **ripgrep** (`rg`) - it's faster than grep

### Need to find files?
- Use **fd** - more user-friendly than find

### Working with Python?
- Use **uv** for dependencies and virtual environments

### Need containers on macOS?
- Use **colima** + **docker** — free, OSS, Docker-compatible

### Setting up CI/CD?
- Use **GitHub Actions** on **GitHub**

### Need infrastructure?
- Use **Cloudflare** for edge/network
- Use **Terraform** for IaC
- Use **k3s** for lightweight Kubernetes

### Managing secrets?
- Use **bitwarden** / **bws** for password/secret management

## Handling Conflicts

When project requirements conflict with these preferences:

1. **Follow project requirements** — they're the authority for that codebase
2. **Note the deviation** — mention that you're using X instead of the preferred Y
3. **Don't update this file** — project-specific overrides don't change general preferences
4. **Consider asking** — if the conflict seems unnecessary, ask the user about it

Example:
> "The project uses npm instead of bun (your preferred package manager). I'll proceed with npm for consistency with the existing codebase."

## Common Agent Mistakes

❌ **Wrong:** Suggesting npm when bun is available and preferred
✅ **Right:** "The project uses npm, but bun is preferred. I'll proceed with npm for consistency, or we can migrate."

❌ **Wrong:** Installing unlisted tools without asking
✅ **Right:** "This tool isn't in my preferred stack. Should I use it anyway?"

❌ **Wrong:** Using "Exploring" tools in production code
✅ **Right:** "This tool is in my 'Exploring' list — learning only. I'll use a production-grade alternative instead."

❌ **Wrong:** Suggesting TypeScript for a one-off shell script
✅ **Right:** Use bash/fish for scripts; TypeScript for maintained projects

❌ **Wrong:** Forgetting to document deviations from preferred stack
✅ **Right:** Always note when project requirements override personal preferences

## Troubleshooting

**Tool not available?**
→ Check if it's in the "Exploring" section (learning only, not production-ready)
→ For missing tools, ask user before installing

**Preference conflicts with project requirements?**
→ Always follow project requirements
→ Document the deviation: "Using npm instead of preferred bun"

**Unclear which tool to use?**
→ Check "Quick Decision Reference" section
→ When in doubt, ask before adding new dependencies

**Version conflicts between tools?**
→ Use **mise** for version management
→ Pin versions in project config files

## Versioning

- **Last updated:** 2026-05-26
- **Version:** 1.8
- **Update notes:** Added Automatic Agent Invocation section based on retrospective finding that only 12/697 sessions consulted this skill. Agent must now self-trigger on any package install, dependency add, or tool selection.

## Related Skills

- **my-agent-file-conventions** — For creating AGENT.md files (not tech recommendations)
