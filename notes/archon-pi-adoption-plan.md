# Archon → Pi Adoption Plan

## What Archon Is

Archon is an open-source workflow engine for AI coding agents. It defines development processes as YAML workflows (planning → implementation → validation → review → PR creation) and runs them deterministically across projects.

**Key capabilities:**
- YAML DAG workflow executor with loop nodes, approval gates, script nodes
- Git worktree isolation for concurrent workflow runs
- Multi-platform adapters (Web UI, CLI, Telegram, Slack, GitHub, Discord)
- Database-backed session persistence
- 17 built-in workflows for common dev tasks
- AI assistant abstraction (Claude Code, Codex, **Pi**)

## Current Archon ↔ Pi Integration

Archon **already integrates Pi** as a community AI provider (`builtIn: false`).

From the Archon Pi provider source (`packages/providers/src/community/pi/provider.ts`):
- Dynamically imports `@mariozechner/pi-coding-agent` to avoid compiled-binary startup crashes
- Bridges Pi's callback-based events to Archon's `AsyncGenerator<MessageChunk>` streaming contract
- Supports Pi skills, extensions, thinking levels, tool restrictions
- Reads Pi credentials from `~/.pi/agent/auth.json` and env vars
- Pi sessions are fresh per `sendQuery()` call (no resume)
- Maps Pi tools: `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`

**What this means today:** You can already use Pi as the AI brain inside Archon. Install Archon, configure `assistants.pi.model` in `.archon/config.yaml`, and Archon orchestrates Pi through its workflow engine.

## The Reverse: Bringing Archon INTO Pi

The user wants Archon's **workflow engine** capabilities available *within* Pi's interactive harness.

### Why This Matters

Pi is a fantastic interactive coding harness, but it's fundamentally a REPL:
- You type a prompt, the agent responds, repeat.
- No built-in multi-step deterministic workflows.
- No git worktree isolation.
- No human-in-the-loop approval gates.
- No persistent session state across restarts.

Archon solves exactly these problems. Porting Archon's workflow engine into Pi would give Pi users:
1. **Deterministic workflows** — "fix this bug" always follows: plan → implement → validate → review → PR
2. **Isolation** — concurrent tasks in separate git worktrees without conflicts
3. **Approval gates** — pause workflow for human review, then resume
4. **Loop nodes** — iterate implementation until tests pass
5. **Multi-agent review** — spin up parallel review agents

## Adoption Strategies

### Strategy A: Pi Extension (Recommended)

Build a `pi-extension-archon` npm package that:
1. Parses `.archon/workflows/*.yaml` files in the current repo
2. Executes workflow nodes using Pi's built-in tools
3. Provides new slash commands: `/archon run <workflow>`, `/archon list`, `/archon status`
4. Manages git worktree isolation via shell commands
5. Persists workflow run state to disk (SQLite or JSON)

**Pros:** Native to Pi's extension model, leverages existing tool ecosystem.
**Cons:** Need to reimplement the DAG executor and node handlers.

### Strategy B: Archon-as-Backend (Easiest)

Use Archon as the orchestrator and Pi as one of its AI providers. This already works.

**Steps:**
1. Install Archon (`brew install coleam00/archon/archon` or `curl -fsSL https://archon.diy/install | bash`)
2. Configure `.archon/config.yaml`:
   ```yaml
   assistants:
     pi:
       model: fireworks/accounts/fireworks/routers/kimi-k2p6-turbo
       enableExtensions: true
   ```
3. Set `DEFAULT_AI_ASSISTANT=pi`
4. Use Archon's CLI or Web UI to run workflows

**Pros:** Zero development, full Archon feature set immediately.
**Cons:** You leave Pi's interactive CLI; Archon becomes the primary interface.

### Strategy C: Hybrid Skill + Extension

Create a Pi skill (`@skills/archon-workflows`) plus a lightweight extension:
- Skill defines workflow authoring conventions and prompt templates
- Extension adds worktree isolation and session persistence
- Pi's existing interactive mode remains primary; workflows are opt-in via `/archon` commands

## Technical Deep Dive: What Needs Building

If pursuing Strategy A (Pi Extension), here's the implementation breakdown:

### 1. Workflow YAML Parser

Archon workflows are YAML DAGs. Example:
```yaml
nodes:
  - id: plan
    prompt: "Explore the codebase and create an implementation plan"

  - id: implement
    depends_on: [plan]
    loop:
      prompt: "Read the plan. Implement the next task. Run validation."
      until: ALL_TASKS_COMPLETE
      fresh_context: true

  - id: run-tests
    depends_on: [implement]
    bash: "bun run validate"

  - id: review
    depends_on: [run-tests]
    prompt: "Review all changes against the plan. Fix any issues."

  - id: approve
    depends_on: [review]
    loop:
      prompt: "Present the changes for review. Address any feedback."
      until: APPROVED
      interactive: true

  - id: create-pr
    depends_on: [approve]
    prompt: "Push changes and create a pull request"
```

Node types to support:
- `prompt` — AI node (delegates to Pi's agent loop)
- `bash` — Deterministic script node
- `loop` — Iteration with `until` condition
- `interactive` — Human approval gate
- `hooks` — Per-node pre/post validation

### 2. DAG Executor

Core algorithm:
1. Parse YAML → node graph
2. Topological sort by `depends_on`
3. Execute nodes in parallel where possible
4. Stream events (node_start, node_end, tool_call, error) back to Pi's UI
5. Handle loop conditions and interactive gates

Archon's DAG executor lives in `packages/core/src/dag/` — would need a TypeScript reimplementation for the Pi extension.

### 3. Event Bridge

Archon's Pi provider has an event bridge (`event-bridge.ts`) that maps Pi callbacks to `MessageChunk` types. For a Pi extension, we need the **inverse**: map workflow events into Pi's extension lifecycle.

Pi's extension API exposes:
- `session.extensionRunner` — lifecycle hooks
- `uiContext` — UI notifications
- `setFlagValue` — feature flags

The extension would emit workflow progress via Pi's UI context so users see real-time updates.

### 4. Isolation (Git Worktrees)

Archon's `WorktreeProvider` (`packages/isolation/src/providers/worktree.ts`):
- Creates worktree at `~/.archon/workspaces/<owner>/<repo>/worktrees/<branch>/`
- Adopts existing worktrees before creating new ones
- Cleans up on workflow completion

For a Pi extension, this maps to bash commands:
```bash
git worktree add ../.archon-worktrees/task-foo -b archon/task-foo
cd ../.archon-worktrees/task-foo
# ... run workflow ...
git worktree remove ../.archon-worktrees/task-foo
git branch -D archon/task-foo
```

### 5. Session Persistence

Archon uses SQLite/PostgreSQL with 7 tables. A Pi extension could use:
- SQLite via `better-sqlite3` (lightweight, no server)
- Simple JSONL files in `~/.pi/agent/archon-runs/`

Key entities:
- `workflow_run` — top-level execution
- `workflow_event` — per-node events
- `isolation_environment` — worktree state

### 6. Pi Capability Mapping

From Archon's `PI_CAPABILITIES`:
```typescript
{
  sessionResume: true,      // Pi supports this; Archon doesn't reuse Pi sessions
  mcp: false,               // Pi doesn't expose MCP to Archon
  hooks: false,             // Pi per-node hooks not wired in Archon
  skills: true,             // ✅ Archon passes skill paths to Pi
  agents: false,            // Pi subagents not exposed
  toolRestrictions: true,   // ✅ `allowed_tools` / `denied_tools` wired
  structuredOutput: true,   // ✅ Best-effort via prompt engineering
  envInjection: true,       // ✅ Bash env vars + runtime API keys
  costControl: false,
  effortControl: true,      // ✅ `effort` nodeConfig → Pi thinkingLevel
  thinkingControl: true,    // ✅ `thinking` nodeConfig → Pi thinkingLevel
  fallbackModel: false,
  sandbox: false,
}
```

For a Pi extension, ALL Pi capabilities become available natively — no mapping needed since we're running inside Pi itself.

## Recommended Path Forward

Given the user's existing Pi-centric workflow:

### Phase 1: Use Archon-as-Backend (Immediate, ~30 min)

Install Archon and configure it to use Pi as the AI provider. This gives full workflow capabilities TODAY without any development.

```bash
# Install Archon
brew install coleam00/archon/archon

# Configure to use Pi
mkdir -p ~/.archon
cat > ~/.archon/config.yaml << 'EOF'
defaultAIAssistant: pi
assistants:
  pi:
    model: fireworks/accounts/fireworks/routers/kimi-k2p6-turbo
    enableExtensions: true
    env:
      # Any Pi extension env vars
      PLANNOTATOR_REMOTE: "1"
EOF

# Run a workflow
archon workflow run archon-idea-to-pr --project /path/to/your/project
```

### Phase 2: Build `pi-extension-archon` (Medium, ~1-2 weeks)

Create a Pi extension that embeds Archon's workflow engine:
1. Fork/clone Archon monorepo
2. Extract the DAG executor and YAML parser into a standalone package
3. Create a Pi extension that registers `/archon` slash commands
4. Wire worktree isolation via bash commands
5. Add workflow run persistence (SQLite)
6. Publish to npm as `pi-extension-archon`

### Phase 3: Deep Integration (Long-term)

- Make Pi's built-in loop understand Archon workflow semantics
- Add visual workflow editor to Pi's TUI
- Cross-pollinate: Pi skills ↔ Archon commands, Pi extensions ↔ Archon hooks

## Key Files to Study

| File | Purpose |
|------|---------|
| `packages/providers/src/community/pi/provider.ts` | How Archon wraps Pi |
| `packages/providers/src/community/pi/event-bridge.ts` | Pi callback → async generator bridge |
| `packages/providers/src/community/pi/capabilities.ts` | Pi capability flags |
| `packages/core/src/dag/` | Workflow executor (need to find exact path) |
| `packages/isolation/src/providers/worktree.ts` | Git worktree isolation |
| `.archon/workflows/defaults/*.yaml` | Built-in workflow definitions |

## Open Questions

1. Does the user want to **use Archon as-is** with Pi as the backend (Strategy B), or **port Archon into Pi** (Strategy A)?
2. Which Archon features are most valuable? Workflows? Isolation? Multi-platform adapters?
3. Should this be a one-person effort or leverage Archon's existing community?

## Next Actions

1. **Validate Strategy B** — Install Archon, configure Pi provider, run a workflow on a test repo
2. **Explore Archon source** — Clone repo, trace the DAG executor code path
3. **Decide scope** — Full port vs. subset (workflows only? isolation only?)
4. **Prototype** — Start with a Pi skill that can parse and execute a simple 3-node workflow
