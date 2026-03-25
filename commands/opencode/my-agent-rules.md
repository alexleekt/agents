---
description: Display agent configuration rules and conventions
---

**Agent Configuration Rules Loaded**

This command references the `@skills/my-agent-rules` skill, which defines how to create and manage agent configuration files.

## When to Use This

- Creating or editing AGENT.md or claude.md files
- Validating agent file content
- Understanding what belongs in agent files vs project docs
- Setting up agent workflows

## Key Rules

### What BELONGS in Agent Files
- Behavioral rules and workflows
- Communication style preferences
- Decision-making guidelines
- Tool usage patterns
- Code conventions
- Testing requirements
- Approval workflows

### What does NOT Belong
- Project descriptions or overviews
- Architecture documentation
- Feature specifications
- Business logic
- API documentation

### File Locations
- **AGENT.md** → Repository root (project-wide rules)
- **claude.md** → `.agent/` directory (context-specific rules)

## Quick Test

| Behavioral (✓) | Documentation (✗) |
|----------------|-------------------|
| "Always run tests before committing" | "This is a React-based dashboard" |
| "Ask before installing dependencies" | "The app uses PostgreSQL" |
| "Use TypeScript for all new files" | "Users can create projects" |

**Rule of Thumb:** If it describes HOW to work → agent file. If it describes WHAT the project is → README/docs.

Always consult this skill before creating or modifying agent configuration files.
