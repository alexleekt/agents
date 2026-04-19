---
name: my-tech-stack
description: |
  **MANDATORY REFERENCE** for all tool recommendations. ALWAYS consult BEFORE
  suggesting tools, libraries, frameworks, or technologies.

  **ALWAYS use when user asks about:** preferred tools, tech recommendations
  ("bun or node", "uv or pip"), or stack decisions.

  **DO NOT use for:** agent configuration (@skills/my-agent-rules) or VCS
  operations (@skills/my-jj-workflow).

  **CRITICAL:** Do NOT suggest unlisted tools without asking first.
---

# Technology Preferences

Preferred tools and technologies. Defaults, not hard rules.

> **Note:** This is a living document. Preferences evolve as new tools emerge and requirements change. Check the latest version before making decisions.

## How to Use This

When working with this user:

1. **Check this file first** — Before suggesting tools, consult these preferences
2. **Prefer listed tools** — When multiple solutions exist, default to these
3. **Respect "Exploring"** — Tools marked as exploring are for learning only
4. **Ask before adding** — Don't install unlisted tools without confirmation
5. **Note deviations** — If project requirements override preferences, document it

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

### Infrastructure & Cloud

| Tool | When to Use |
|------|-------------|
| [**cloudflare**](https://www.cloudflare.com/) | DNS management, CDN, DDoS protection, serverless workers, fast global edge network |
| [**k3s**](https://github.com/k3s-io/k3s) | Lightweight Kubernetes for edge, IoT, CI/CD, resource-constrained environments |
| [**terraform**](https://github.com/hashicorp/terraform) | Infrastructure as Code for provisioning cloud resources; multi-cloud or complex infrastructure |

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

## Versioning

- **Last updated:** 2026-04-22
- **Version:** 1.6
- **Update notes:** Added AI Providers section with fireworks/firepass as default LLM provider; pi-coding-agent as primary agent; memex replacing mulch

## Related Skills

- **my-agent-rules** — For creating AGENT.md files (not tech recommendations)
- **my-jj-workflow** — For version control operations with jj
