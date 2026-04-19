---
name: my-team-orchestrate
description: |
  **ALWAYS use when tasks exhibit:**
  - **Scale:** "refactor entire codebase", "50+ files"
  - **Complexity:** "needs exploration", "overwhelming"
  - **Parallelism:** "work on X and Y separately"
  - **Multi-domain:** "security review", "architecture"
  - **Explicit:** "start a team", "delegate", "yolo"

  **DO NOT use for:** single-file changes, one-step tasks, solo work preference.
---

# Team Orchestration Skill

Multi-agent delegation patterns for any system with subagent support.

## ⚡ Agent Quick Start

**Pick pattern by signal:**

| Signal | Pattern | Section |
|--------|---------|---------|
| "refactor everything" / "50+ files" | Divide and Conquer | Pattern 3 |
| "explore first, then build" | Scout → Planner → Worker | Pattern 1 |
| "security + performance review" | Expert Panel | Pattern 2 |
| "keep fixing till clean" / "yolo" | Till Done | Pattern 5 |
| "use my expert team" | Predefined Teams | Pattern 4 |

**Platform notes:**
- **Pi:** Use `team_*` tools (`team_create`, `spawn_teammate`, `send_message`)
- **Claude Code:** Use `/subagent` command
- **Other:** Adapt patterns to available subagent API

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

### Pattern 5: Till Done (Iterative Refinement Loop)
Best for: Any task requiring repeated cycles until quality threshold met

**Trigger phrases:** "till done", "until clean", "keep going", "don't stop", **"yolo"**

**Concept:** Loop between checker→fixer agents until checker returns "DONE" or zero issues. Generic pattern applicable to code review, tests, docs, refactoring, etc.

**The "Yolo" Modifier:**
When user says **"yolo"** with any pattern, it means:
- Don't pause for human confirmation between cycles
- Autonomously iterate until done or safety limit
- Maximum autonomy, zero hand-holding

Apply "yolo" to any pattern: Scout→Planner→Worker YOLO, Divide-and-Conquer YOLO, etc.

**Generic Structure:**
```
Loop:
  1. CHECKER validates current state → Issues?
     ├── "DONE" → Exit loop
     └── Issues list → Continue
  2. FIXER addresses issues
  3. (Optional) VERIFIER confirms fixes
  4. Back to step 1 (with max rounds safety)
```

**Pi Implementation (Generic):**
```typescript
await team_create({ team_name: "refinement-loop", description: "Iterative till done" });

let round = 1;
const maxRounds = 5;
let done = false;

while (!done && round <= maxRounds) {
  // CHECK PHASE
  await spawn_teammate({
    team_name: "refinement-loop",
    name: `checker-r${round}`,
    cwd: projectPath,
    prompt: `[DOMAIN-SPECIFIC CHECK]
For code: Check src/ for bugs, style, tests. Return "DONE" or numbered issues.
For tests: Run test suite. Return "DONE" (all pass) or failing test list.
For docs: Check README completeness. Return "DONE" or missing sections.

Always return machine-parseable:
- "DONE" if complete
- Numbered list of specific issues otherwise`
  });

  const checkResult = await waitForResult(`checker-r${round}`);
  
  if (checkResult.includes("DONE") || checkResult.trim() === "") {
    done = true;
    break;
  }

  // FIX PHASE
  await spawn_teammate({
    team_name: "refinement-loop",
    name: `fixer-r${round}`,
    cwd: projectPath,
    prompt: `Address these issues:
${checkResult}

Apply fixes directly. Report what changed.`
  });

  await waitForResult(`fixer-r${round}`);
  round++;
}

await team_shutdown({ team_name: "refinement-loop" });
```

**Domain-Specific Examples:**

| Domain | Checker Prompt | Fixer Prompt | Done Signal |
|--------|---------------|--------------|-------------|
| **Code Review** | Review src/ for bugs, style, security. Return "DONE" or issues list. | Fix listed issues in code | "DONE" or empty |
| **Tests** | Run `npm test`. Return "DONE" or failing test names. | Fix failing tests | "DONE" or all pass |
| **Docs** | Check README covers setup, API, examples. Return "DONE" or gaps. | Add missing documentation | "DONE" |
| **Refactor** | Check if migration complete (old API calls remain?). Return "DONE" or locations. | Replace old patterns | "DONE" |

**Claude Code Implementation:**
```
# YOLO mode: chain with no human between rounds
/subagent checker "Check if task complete. Return 'DONE' or what remains."
/subagent fixer "Fix what checker found. Apply directly."
/subagent checker "Check again. Return 'DONE' or continue."
# ...loop until DONE or max rounds
```

**Checker Agent Rules:**
- Return "DONE" (machine-parseable) when complete
- Otherwise: numbered, specific, actionable issues
- No prose — just pass/fail criteria

**Fixer Agent Rules:**
- Apply fixes, don't just suggest
- Preserve existing patterns
- Run verification if available (tests, lint)

**Stopping Conditions:**
- Checker returns "DONE"
- Empty issues list
- Max rounds reached (safety valve)
- Fixer makes no changes (stuck detection)

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
- Include **full context in initial prompt** - subagents don't see your conversation
- Set **clear deliverables** - what should they return?
- Define **communication protocol** - how/when to report back

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

❌ **Vague assignments** - "Help with this" vs "Audit src/auth.ts for SQL injection risks"
❌ **Context overload** - Dumping entire conversation vs focused, relevant context
❌ **Orphaned agents** - Starting subagents without plan to collect results
❌ **Unclear handoffs** - Chain patterns need explicit "check X for previous output"
❌ **Agent sprawl** - 3-5 focused agents > 10 generalists
❌ **Platform confusion** - Using Pi syntax in Claude Code or vice versa

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
    ├── Can be split independently? → Divide and Conquer
    └── Needs iterative refinement? → Till Done (checker→fixer loop)
```

**Till Done Loop** (generic):
```
Loop:
  1. CHECKER validates → Issues found?
     ├── "DONE" → Exit successfully
     └── Issues list → Continue
  2. FIXER addresses issues
  3. (Optional) VERIFIER confirms
  4. Back to step 1
Safety: Max 5 rounds or no-progress detection
```

### YOLO as Pattern Modifier

**"Yolo"** works with ANY pattern, not just Till Done:

| Base Pattern | YOLO Variant | Effect |
|-------------|--------------|--------|
| Scout→Planner→Worker | **Scout→Planner→Worker YOLO** | No human between stages |
| Divide and Conquer | **Divide and Conquer YOLO** | Spawn all workers at once |
| Expert Panel | **Expert Panel YOLO** | Return raw outputs, no synthesis |
| Till Done | **Till Done YOLO** | Autonomous looping |

**When to YOLO:** User says "yolo", time pressure, batch processing.
**When NOT:** High-stakes, novel situations, user wants to learn.
