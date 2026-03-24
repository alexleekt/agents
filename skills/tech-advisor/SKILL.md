---
name: tech-advisor
description: |
  **MANDATORY REFERENCE** for all tool recommendations and technology decisions. 
  
  ALWAYS consult this skill BEFORE:
  - Recommending ANY tools, libraries, frameworks, or technologies
  - Setting up new projects, development environments, or repositories
  - Choosing package managers (bun vs npm vs pnpm vs yarn)
  - Selecting cloud providers, infrastructure tools, or deployment platforms
  - Making runtime decisions (Node.js vs Deno vs Bun, Python versions)
  - Choosing code editors, linters, formatters, or quality tools
  - Answering "what should I use for X?" or "which tool is best for Y?"
  - Comparing alternatives for any technical decision
  
  This skill contains the user's explicit technology preferences organized by category: Development Environment, AI Agents, Code Quality, Infrastructure & Cloud, Local Development, API & Testing, Security & Secrets, Remote Access, Task Automation, Operating System, and Shell preferences.
  
  **CRITICAL:** Do NOT suggest tools that are NOT listed in this skill without first checking here and asking the user if they want to deviate from their stated preferences.
  
  **DO NOT** proceed with technology recommendations without consulting this skill first.
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
| [**opencode**](https://opencode.ai/) | AI coding agent harness; preferred for agent-driven development workflows |

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
| [**httpie**](https://github.com/httpie/cli) | Testing APIs, making HTTP requests, debugging endpoints; preferred over curl for readability |

### Security & Secrets

| Tool | When to Use |
|------|-------------|
| [**bitwarden**](https://bitwarden.com/) / [**bws**](https://github.com/bitwarden/sdk) | Password management, secure secret storage; bws CLI for programmatic access in scripts and CI/CD |
| [**wireguard**](https://www.wireguard.com/) | Simple, fast, modern VPN; secure point-to-point connections; mesh networking |

### Remote Access

| Tool | When to Use |
|------|-------------|
| [**eternal-terminal**](https://github.com/MisterTea/EternalTerminal) | Remote shell that auto-reconnects without interrupting session; resilient alternative to SSH |

### Task Automation

| Tool | When to Use |
|------|-------------|
| [**just**](https://github.com/casey/just) | Running project tasks, build scripts, command shortcuts; Makefile replacement with better cross-platform support |
| [**mise**](https://github.com/jdx/mise) (tasks) | Defining and running project tasks when already using mise for version management |
| [**worktrunk**](https://worktrunk.dev/) | Git worktree management for parallel AI agent workflows; creating, switching, cleaning up worktrees |

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
| [**dotenvx**](https://github.com/dotenvx/dotenvx) | Managing environment variables across environments, encrypting secrets |
| [**json-render**](https://github.com/vercel-labs/json-render) | Rendering JSON as UI components; quick admin dashboards |
| [**mulch**](https://github.com/jayminwest/mulch) | Structured expertise management for AI agents |
| [**mastra**](https://github.com/mastra-ai/mastra) | Building AI agents, orchestrating LLM workflows |
| [**rust**](https://www.rust-lang.org/) | Systems programming, performance-critical apps, WebAssembly, CLI tools |
| [**varlock.dev**](https://varlock.dev/) | Securely sharing environment variables with team members |
| [**bouné**](https://boune.dev/docs/introduction/) | Modern task runner and build system with great DX |

## Quick Decision Reference

### Starting a new project?
- Use **bun** for JS/TS runtime and package management
- Use **TypeScript** for type safety
- Use **biome** for linting/formatting
- Use **zed** as code editor
- Use **mise** for version management

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

- **Last updated:** 2024-01-XX
- **Version:** 1.0
- **Update notes:** Initial preferences list

## Related Skills

- **agent-conventions** — For creating AGENT.md files (not tech recommendations)
