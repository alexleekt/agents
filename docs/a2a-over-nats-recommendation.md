# A2A-over-NATS: Multi-Agent Pi Recommendation

> **Status**: Design decisions resolved via grill-with-docs session on 2026-05-21  
> **Scope**: Same-machine, role-based, peer-to-peer with contextual leader tiebreaker

---

## 1. Design Decisions (Resolved)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Topology** | Same machine | Start local; NATS trivially scales to cross-machine later |
| **Communication pattern** | Peer-to-peer with leader tiebreaker | Agents discover and message each other directly; disputes resolved by role-based leader |
| **Leadership model** | Role-based contextual | Each role has authority in its domain; no global bottleneck |
| **Autonomy** | Self-initiated with queue + pause | Agents can proactively message each other, but their own work gets queued and paused when handling external asks |
| **Transport** | NATS.io | Pub/sub, request/reply, JetStream persistence; single binary; trivial to add HTTP gateway later |
| **Application protocol** | A2A | AgentCard discovery, Task lifecycle, Message/Part semantics; future-proof for external interoperability |

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Same Machine                            │
│                                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐  │
│  │ Planner │   │ Worker  │   │ Reviewer│   │  Safety │  │
│  │  Agent  │◄──│  Agent  │◄──│  Agent  │◄──│  Agent  │  │
│  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘  │
│       │             │             │             │         │
│       └─────────────┴──────┬──────┴─────────────┘         │
│                            │                              │
│                    ┌───────┴───────┐                      │
│                    │   NATS Server │  (localhost:4222)      │
│                    │   + JetStream │                      │
│                    └───────┬───────┘                      │
│                            │                              │
│                    ┌───────┴───────┐                      │
│                    │   AgentCard   │                      │
│                    │   Registry    │  (NATS KV store)     │
│                    └───────────────┘                      │
│                                                             │
│  Future: HTTP Gateway ──► External A2A agents             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. A2A ↔ NATS Mapping

Since no existing package implements A2A-over-NATS, you build the mapping yourself.

### Subject Naming Convention

```
a2a.agent.{agent-id}.inbox          # Inbound messages to an agent
a2a.agent.{agent-id}.tasks         # Task creation/updates (JetStream)
a2a.agent.{agent-id}.agentcard     # AgentCard request/reply
a2a.broadcast.discovery            # Agent announces presence (pub)
a2a.system.registry                # AgentCard KV updates
```

### Operation Mapping

| A2A Operation | NATS Pattern | Notes |
|-------------|-------------|-------|
| `SendMessage` | Pub to `a2a.agent.{to}.inbox` | Fire-and-forget or use reply inbox for ack |
| `GetTask` | Request/Reply to `a2a.agent.{agent-id}.tasks.get` | |
| `SubscribeToTask` | Sub to `a2a.agent.{agent-id}.tasks.{task-id}.updates` | |
| `GetAgentCard` | Request/Reply to `a2a.agent.{agent-id}.agentcard` | |
| `UpdateAgentCard` | KV put to `a2a.system.registry` | |

### Message Serialization

A2A `Message` objects serialized as JSON, wrapped in a NATS envelope:

```json
{
  "a2aVersion": "1.0.0",
  "messageId": "uuid",
  "taskId": "uuid",
  "from": "planner-agent",
  "to": "worker-agent",
  "a2aPayload": { /* full A2A Message object */ },
  "timestamp": "2026-05-21T12:00:00Z"
}
```

---

## 4. Agent Spawning Model

Each agent is an independent Pi session with distinct resources:

```typescript
import { createAgentSession, ResourceLoader } from "@earendil-works/pi-coding-agent";
import { natsTransport } from "./transport"; // your A2A-over-NATS layer

// Each agent gets its own ResourceLoader with role-specific skills
const plannerLoader = ResourceLoader.create({
  skills: ["planning", "architecture"],
  prompts: ["planner-system-prompt"],
});

const { session: plannerAgent } = await createAgentSession({
  model: "anthropic/claude-sonnet-4",
  resourceLoader: plannerLoader,
  tools: ["read", "bash", "a2a_send_message"], // your custom A2A tool
});

// Connect to NATS and register AgentCard
await natsTransport.connect({
  agentId: "planner-agent",
  agentCard: {
    name: "Planner Agent",
    version: "1.0.0",
    capabilities: {
      streaming: true,
      pushNotifications: false,
    },
    skills: ["planning", "architecture", "delegation"],
  },
});
```

---

## 5. Queue + Pause Mechanism

Each agent maintains an internal work queue:

```
┌─────────────────┐
│  Agent Process  │
│                 │
│  ┌───────────┐  │
│  │ Own Queue │  │  ← Tasks the agent planned for itself
│  │  (paused) │  │     Paused when handling external asks
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Inbox     │  │  ← Messages from other agents
│  │ (active)  │  │     Processed immediately
│  └───────────┘  │
│                 │
│  Priority: Inbox > Own Queue  │
└─────────────────┘
```

When an agent receives an external ask:
1. **Pause** its own queue (current task state checkpointed)
2. **Process** the external ask
3. **Resume** its own queue from checkpoint

Implementation via a custom Pi extension that wraps the agent's event loop.

---

## 6. Role-Based Leader Tiebreaker

Leader authority is domain-scoped, not global:

| Dispute Domain | Leader Role | How Resolved |
|----------------|-------------|--------------|
| Architecture / planning | Planner Agent | Planner's design wins |
| Code correctness | Reviewer Agent | Reviewer's verdict wins |
| Security / safety | Safety Agent | Safety's block wins |
| Tooling / build | DevOps Agent | DevOps's config wins |
| Ambiguous / cross-domain | Escalate to human | Or consensus vote |

Agents publish their role in their `AgentCard.skills` array. The tiebreaker logic is a simple priority map in the transport layer.

---

## 7. What Exists vs. What You Build

| Component | Already Exists | You Build |
|-----------|---------------|-----------|
| Pi agent sessions | ✅ `createAgentSession()` | |
| Child process spawning | ✅ `pi-subagents` | |
| 1:1 IPC messaging | ✅ `pi-intercom` | |
| NATS server | ✅ `nats-server` binary | |
| NATS Node.js client | ✅ `@nats-io/transport-node` | |
| A2A protocol spec | ✅ `a2aproject.github.io` | |
| **A2A-over-NATS mapping** | ❌ | 🛠️ You build this |
| **AgentCard registry** | ❌ | 🛠️ NATS KV store |
| **Queue+pause mechanism** | ❌ | 🛠️ Custom extension |
| **Role-based tiebreaker** | ❌ | 🛠️ Transport layer logic |

---

## 8. Implementation Roadmap

### Phase 1: Foundation (same-machine)
1. Run `nats-server -js` locally
2. Build the A2A-over-NATS transport layer (NATS subject mapping, JSON envelope)
3. Build the AgentCard registry (NATS KV)
4. Spawn 2-3 Pi agents with distinct `ResourceLoader` configs
5. Test peer-to-peer messaging

### Phase 2: Autonomy
1. Add queue + pause mechanism
2. Add self-initiation logic (agents can `send_message` to others)
3. Add role-based tiebreaker
4. Stress-test with concurrent tasks

### Phase 3: Scale (future)
1. Add HTTP gateway for external A2A agents
2. Move NATS server to a dedicated host
3. Add JetStream persistence for durable tasks
4. Add observability (Prometheus metrics, tracing)

---

## 9. Why Not Just Use pi-crew or pi-subagents?

| Approach | Best For | Limitation |
|----------|----------|------------|
| **pi-subagents** | Delegation from one parent to child workers | Hub-and-spoke only; parent is always the orchestrator |
| **pi-crew** | Full team workflows with durable state | Complex; opinionated about workflow phases |
| **pi-intercom** | Ad-hoc 1:1 between sessions | No structured protocol; no discovery |
| **A2A-over-NATS** (this design) | Autonomous peer-to-peer, future cross-machine | You build the glue |

Your design fills a gap: agents that can talk to each other as equals, not just take orders from a parent, with a clean migration path to distributed operation.

---

## 10. Next Steps

1. **Confirm** this recommendation captures your intent
2. **Decide** on your first 2-3 agent roles (e.g., Planner + Worker + Reviewer)
3. **Implement** the A2A-over-NATS transport layer
4. **Test** with a simple "planner asks worker to research, worker replies" flow

Ready to start building?
