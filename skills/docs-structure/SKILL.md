---
name: docs-structure
description: Generate complete project documentation structure including AGENTS.md, README.md, ADRs, SOPs, and environment templates. Use this skill whenever the user wants to set up documentation for a new project, create project documentation templates, establish documentation standards, or scaffold documentation structure. This includes requests to create docs folders, setup documentation templates, initialize project documentation, or generate markdown documentation files. Also trigger when user mentions "documentation structure", "project templates", or "setup docs".
---

# Documentation Structure Generator

This skill creates a complete, standardized documentation structure for any project based on best practices.

## What Gets Created

The following files and directories are generated:

1. **AGENTS.md** - Guidelines for AI agents working on the project
2. **README.md** - User-facing documentation with quick start
3. **docs/adr/ADR-001-initial-setup.md** - Architecture Decision Record example
4. **docs/sop/getting-started.md** - Standard Operating Procedure example
5. **.env.example** - Environment variable template

## Execution Steps

When this skill triggers:

1. **Determine project name**: Check context for project name or ask user if unclear
2. **Create directory structure**: 
   - `docs/adr/`
   - `docs/sop/`
3. **Generate files**: For each template in skill's templates/ directory:
   - Read the template file
   - Replace `{{PROJECT_NAME}}` with actual project name
   - Write to appropriate location in user's working directory
4. **Confirm completion**: Report which files were created

## Templates Location

Templates are stored in the skill's bundled `templates/` directory:
- `templates/AGENTS.md`
- `templates/README.md`
- `templates/ADR-001-initial-setup.md`
- `templates/getting-started.md`
- `templates/.env.example`

## Output Structure

```
.
├── AGENTS.md
├── README.md
├── .env.example
└── docs/
    ├── adr/
    │   └── ADR-001-initial-setup.md
    └── sop/
        └── getting-started.md
```

## Customization Notes

All templates contain bracketed placeholders like `[Project Name]`, `[endpoint]`, `[tool1]` that serve as guides for the user to fill in project-specific details. Do not remove these - they are intentional templates.
