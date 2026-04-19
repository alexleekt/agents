---
name: my-team-orchestrate
description: |
  **ALWAYS use when tasks exhibit these characteristics:**
  
  **Scale signals:** "refactor the entire codebase", "50+ files involved", "whole project migration",
  "massive change", "large-scale" — scope too big for single-agent completion
  
  **Complexity signals:** "too complex", "multi-part problem", "needs exploration first",
  "overwhelming", "don't know where to start" — complexity requiring staged analysis
  
  **Parallelism opportunities:** "can work on X and Y separately", "parallel streams",
  "independent parts" — work that can be divided across agents
  
  **Multi-domain needs:** "review from security/performance/DX perspective",
  "needs architecture review" — requiring expertise from multiple domains simultaneously
  
  **Explicit triggers (if mentioned):** "start a team", "delegate", "spawn agents",
  "divide and conquer", "parallelize", "get multiple opinions"
  
  **DO NOT use for:** single-file changes, one-step debugging, focused Q&A, OR when user
  explicitly wants solo work. Use when task CHARACTERISTICS suggest multi-agent value.

  **Agent-Agnostic:** Works with Pi, Claude Code, or any system with subagent capabilities.
---

# Team Orchestration Skill

Multi-agent delegation patterns that work across any AI system with subagent support.

## Platform-Specific Implementations

| Platform | Subagent Mechanism | Key Tools |
|----------|-------------------|-----------|
| **Pi** | `team_create`, `spawn_teammate`, `send_message` | Native team coordination |
| **Claude Code** | `/subagent` command | Built-in subagent spawning |
| **Codex/Cursor** | Limited/None | May require external orchestration |
| **Babysitter** | Process definitions + `@team` | Workflow-based delegation |

> **Note:** Adapt the implementation patterns below to your platform's specific subagent API.

## Implicit Trigger Recognition

Don't wait for users to say "start a team". Recognize when tasks *need* teams:

| Signal Type | Examples | Pattern to Use |
|-------------|----------|----------------|
| **Scale** | "refactor entire codebase", "50 files", "whole project" | Divide and Conquer |
| **Complexity** | "too complex", "explore first", "don't understand structure" | Scout → Planner → Worker |
| **Multi-domain** | "security review", "performance check", "architecture validation" | Expert Panel |
| **Parallelism** | "X and Y are independent", "can work in parallel" | Divide and Conquer |
| **Time pressure** | "need this fast", "urgent", "many moving parts" | Any parallel pattern |

**Key insight:** Users rarely say "I want to delegate this." They say "this is overwhelming" or "this touches everything." Those are the triggers.

## Core Patterns (Platform-Agnostic)

### Pattern 1: Scout → Planner → Worker
Best for: Complex tasks requiring exploration before implementation

**Concept:** Chain specialized agents where each builds on previous findings.

**Pi Implementation:**
```typescript
await team_create({ team_name: "feature-crew", description: "Build new feature" });

// Scout explores
await spawn_teammate({
  team_name: "feature-crew",
  name: "scout",
  cwd: projectPath,
  prompt: `Explore codebase to understand current authentication flow.
Return structured findings.`
});

// Planner designs (receives scout's findings via inbox)
await send_message({
  team_name: "feature-crew",
  recipient: "planner",
  summary: "Design auth integration",
  content: `Based on scout's findings (check inbox), design OAuth2 integration...`
});

// Worker implements (receives design via inbox)
await send_message({
  team_name: "feature-crew",
  recipient: "worker",
  summary: "Implement auth feature",
  content: `Based on planner's design (check inbox), implement the OAuth2 integration...`
});

await team_shutdown({ team_name: "feature-crew" });
```

**Claude Code Implementation:**
```
/subagent scout "Explore codebase auth patterns, return structured findings"
# Wait for results, then...
/subagent planner "Design OAuth2 integration based on these findings: [scout output]"
# Wait for design, then...
/subagent worker "Implement based on this design: [planner output]"
```

### Pattern 2: Parallel Expert Panel
Best for: Getting multiple perspectives simultaneously

**Concept:** Spawn multiple specialized agents with the same input, collect diverse viewpoints.

**Pi Implementation:**
```typescript
await team_create({ team_name: "experts", description: "Architecture review" });

const experts = [
  { name: "security-rep", role: "Security and threat modeling" },
  { name: "perf-rep", role: "Performance and scalability" },
  { name: "dx-rep", role: "Developer experience" },
  { name: "ops-rep", role: "Operations" }
];

for (const expert of experts) {
  await spawn_teammate({
    team_name: "experts",
    name: expert.name,
    cwd: projectPath,
    prompt: `You are the ${expert.role} expert.
Review this proposal from your domain perspective...`
  });
}

await broadcast_message({
  team_name: "experts",
  summary: "Architecture proposal for review",
  content: `## Proposal: [Description]...`
});
```

**Claude Code Implementation:**
```
# Spawn all experts simultaneously (Claude Code runs in parallel)
/subagent security-rep "Review from security perspective: [proposal]"
/subagent perf-rep "Review from performance perspective: [proposal]"
/subagent dx-rep "Review from DX perspective: [proposal]"
/subagent ops-rep "Review from ops perspective: [proposal]"

# Collect all responses, then synthesize
```

### Pattern 3: Divide and Conquer
Best for: Large tasks split into independent workstreams

**Concept:** Break work into discrete tasks, assign to parallel workers, coordinate completion.

**Pi Implementation:**
```typescript
await team_create({ team_name: "squad", description: "Multi-file refactoring" });

const tasks = [
  { id: "migrate-auth", file: "src/auth.ts", description: "Migrate auth to new API" },
  { id: "migrate-db", file: "src/db.ts", description: "Migrate database layer" },
  { id: "migrate-cache", file: "src/cache.ts", description: "Migrate cache layer" }
];

// Create task list
for (const task of tasks) {
  await task_create({
    team_name: "squad",
    subject: task.id,
    description: task.description
  });
}

// Spawn workers with specific assignments
for (const task of tasks) {
  await spawn_teammate({
    team_name: "squad",
    name: `worker-${task.id}`,
    cwd: projectPath,
    prompt: `Your task: ${task.description}\nWork only on ${task.file}. Update task status as you work.`
  });
}

// Monitor: await task_list({ team_name: "squad" })
```

**Claude Code Implementation:**
```
# Track tasks manually or with a task file
/subagent worker-auth "Migrate src/auth.ts to new API. Report when done."
/subagent worker-db "Migrate src/db.ts to new API. Report when done."
/subagent worker-cache "Migrate src/cache.ts to new API. Report when done."

# Wait for all to complete, then verify
```

### Pattern 4: Predefined Expert Teams
Best for: Leveraging established domain expertise across projects

**Concept:** Maintain reusable agent definitions for common roles (security, performance, DX, etc.)

**Pi Implementation:**
```typescript
// Use existing predefined team
await create_predefined_team({
  team_name: "advisors",
  predefined_team: "skill-representatives",  // From ~/.pi/teams.yaml
  cwd: projectPath
});

await send_message({
  team_name: "advisors",
  recipient: "tech-stack-rep",
  summary: "Tool choice advice",
  content: "Should I use bun or node for this serverless project?"
});
```

**Claude Code Implementation:**
```
# Claude Code uses .claude/agents/ for agent definitions
# Create: ~/.claude/agents/security-expert.md, etc.

/subagent security-expert "Review this from security perspective..."
/subagent perf-expert "Review this from performance perspective..."
```

**Agent Definition Format (Cross-Platform):**
```markdown
---
name: security-expert
description: Security-focused code review and threat modeling
tools: read, grep, find  # Platform-specific
model: claude-sonnet-4   # Platform-specific
---
You are a security expert. Focus on:
- Injection vulnerabilities
- Authentication flaws
- Data exposure risks
- Supply chain concerns
```

## Team Lifecycle Best Practices (Generic)

### Creating Teams
| Platform | Command/Approach |
|----------|-------------------|
| Pi | `team_create({ team_name, description })` |
| Claude Code | Use `/subagent` with named sessions or track mentally |
| Generic | Define scope, assign clear roles, set expectations |

### Spawning Teammates
**Universal principles:**
- Give each agent a **specific, focused role** (not "help with this")
- Include **full context in initial prompt** — subagents don't see your conversation
- Set **clear deliverables** — what should they return?
- Define **communication protocol** — how/when to report back

### Task Management
| Approach | Use When |
|----------|----------|
| **Task list** (Pi) | `task_create` + `task_update` for trackable work |
| **File-based** (Generic) | Write `TASKS.md` or `progress.json` for cross-agent visibility |
| **Conversation-based** (Claude Code) | Rely on subagent responses in chat history |

### Communication Patterns
- **Broadcast** → Same message to all agents simultaneously
- **Direct** → Targeted message to specific agent
- **Chain** → Output of agent A becomes input to agent B
- **Aggregator** → Multiple agents report to one coordinator

### Monitoring
| Platform | Method |
|----------|--------|
| Pi | `check_teammate()`, `task_list()`, inbox polling |
| Claude Code | Watch chat responses, check status indicators |
| Generic | File-based status updates, explicit "ping" messages |

### Cleanup
- Always terminate/close subagents when done
- Save outputs before cleanup
- Pi: `team_shutdown()` | Claude Code: Implicit on session end | Generic: Manual tracking

## Common Anti-Patterns (All Platforms)

❌ **Vague assignments** — "Help with this" vs "Audit src/auth.ts for SQL injection risks"
❌ **Context overload** — Dumping entire conversation vs focused, relevant context
❌ **Orphaned agents** — Starting subagents without plan to collect results
❌ **Unclear handoffs** — Chain patterns need explicit "check X for previous output"
❌ **Agent sprawl** — 3-5 focused agents > 10 generalists
❌ **Platform confusion** — Using Pi syntax in Claude Code or vice versa

## Platform-Specific Troubleshooting

### Pi
| Issue | Solution |
|-------|----------|
| Agent not responding | `check_teammate()` then `send_message()` to nudge |
| Lost context | Use `broadcast_message()` to re-sync |
| Task stuck | `task_update()` to reassign or spawn replacement |

### Claude Code
| Issue | Solution |
|-------|----------|
| Subagent hanging | Check response status, may need to re-invoke |
| Context drift | Summarize previous outputs in new `/subagent` call |
| Result scattered | Manually collect outputs from chat history |

### Generic/Fallback
| Issue | Solution |
|-------|----------|
| No native subagents | Use file-based coordination (write status to disk) |
| Need parallelism | Queue tasks externally (just, make, etc.) |
| Result tracking | Maintain `RESULTS.md` or JSON status file |

## Decision Flowchart

```
Task complexity?
├── Simple (1-2 steps) → Handle directly
├── Medium (3-5 steps, single domain) → Single specialized agent
└── Complex (multi-domain or parallelizable) → Team approach
    ├── Needs exploration first? → Scout → Planner → Worker
    ├── Needs multiple perspectives? → Parallel Expert Panel
    └── Can be split independently? → Divide and Conquer
```
