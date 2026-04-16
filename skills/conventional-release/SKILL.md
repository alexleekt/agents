---
name: conventional-release
description: |
  **ALWAYS use when user mentions:** "release", "ship it", "cut a release", "changelog", 
  "version bump", "semver", "conventional commit", or "jj commit" with formatting needs.
  
  **Chains:** semantic versioning → changelog → jj/git commit.
  
  **DO NOT use for:** generic git operations without release/changelog context.
  
  Automates semantic versioning, conventional commits, and changelog generation for projects using jujutsu (jj) or git. Prefer jj over git when available.
---

# Conventional Release Skill

Automate semantic versioning, conventional commits, and changelog generation.

## Overview

This skill provides workflows for:
1. **Semantic versioning** — Determine version bumps from conventional commits
2. **Changelog generation** — Auto-generate CHANGELOG.md from commit history
3. **Conventional commits** — Format jj/git commits properly
4. **Release workflow** — Full release automation

## Prerequisites

The project should follow **Conventional Commits** specification:
- `feat:` — New features (minor version bump)
- `fix:` — Bug fixes (patch version bump)
- `BREAKING CHANGE:` — Breaking changes (major version bump)
- `docs:`, `style:`, `refactor:`, `test:`, `chore:` — No version bump

## Workflows

### 1. Generate Changelog

**Trigger phrases:** "generate changelog", "update CHANGELOG.md", "create changelog"

**Steps:**
1. Detect version control (jj vs git)
2. Find last release tag/version
3. Collect commits since last release
4. Categorize by conventional commit type
5. Write/update CHANGELOG.md

**Changelog format:**
```markdown
## [Unreleased]

### Added
- New features...

### Fixed
- Bug fixes...

## [1.2.0] - 2026-04-16
...
```

### 2. Determine Version Bump

**Trigger phrases:** "what version bump", "should this be major/minor/patch", "semantic version"

**Steps:**
1. Analyze commits since last tag
2. Check for BREAKING CHANGE markers
3. Check for feat: commits
4. Check for fix: commits
5. Recommend version bump

**Rules:**
- `BREAKING CHANGE:` in any commit → **MAJOR**
- `feat:` present → **MINOR** (if no breaking change)
- `fix:` present → **PATCH** (if no feat/breaking)
- Only docs/style/refactor → **No bump**

### 3. Create Conventional Commit

**Trigger phrases:** "commit this", "jj commit", "git commit", "commit with message"

**Steps:**
1. Analyze changes made (staged in git, or described by user)
2. Determine appropriate commit type
3. Write commit message following convention
4. Execute commit with proper formatting

**Commit types:**
| Type | Use when | Example |
|------|----------|---------|
| `feat` | Adding features | `feat(auth): add JWT token support` |
| `fix` | Fixing bugs | `fix(api): handle null response` |
| `docs` | Documentation only | `docs(readme): update install steps` |
| `style` | Formatting, no logic | `style: run biome format` |
| `refactor` | Code restructuring | `refactor(db): extract connection pool` |
| `test` | Adding tests | `test(auth): add login flow tests` |
| `perf` | Performance improvements | `perf(db): optimize query` |
| `chore` | Maintenance tasks | `chore(deps): update dependencies` |

### 4. Full Release Workflow (Chained)

**Trigger phrases:** "create release", "release version", "bump version and release", "ship it"

**This workflow chains all operations in sequence:**

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Semantic Versioning                                  │
│  └─> Analyze commits since last tag                          │
│      └─> Detect major/minor/patch (or none)                  │
│                                                               │
│  STEP 2: Update Version Files                                 │
│  └─> Bump version in package.json/Cargo.toml/etc             │
│      └─> Write new version                                   │
│                                                               │
│  STEP 3: Generate Changelog                                   │
│  └─> Collect commits since last release                      │
│      └─> Categorize (feat→Added, fix→Fixed, etc.)           │
│          └─> Write CHANGELOG.md                              │
│                                                               │
│  STEP 4: Conventional Commit (jj preferred, git fallback)   │
│  └─> Stage version files + changelog                         │
│      └─> Commit: "chore(release): bump version to X.Y.Z"    │
│                                                               │
│  [OPTIONAL] STEP 5: Create Tag                                │
│  └─> Create signed/annotated tag for the release             │
└─────────────────────────────────────────────────────────────┘
```

**Execution order (must be sequential):**
1. **Analyze** commits → determine bump type
2. **Update** version files (only after bump is known)
3. **Generate** changelog (includes the new version heading)
4. **Commit** everything with conventional message (jj first, git fallback)
5. **Tag** (optional, confirm with user)

** jj vs git logic:**
- Check for `.jj/` directory → use `jj commit`
- Fall back to `git commit`
- Same for tagging: `jj tag` or `git tag`

**Safety checks before chaining:**
- Verify working directory is clean (or confirm with user)
- Check that version files exist
- Confirm with user before major version bumps
- Show preview of changes before committing

## Tool Detection

**Prefer jujutsu (jj) over git** — check for `.jj/` directory or `jj` availability first.

| Command | jj | git |
|---------|-----|-----|
| Status | `jj status` | `git status` |
| Log | `jj log` | `git log` |
| Commit | `jj commit -m "..."` | `git commit -m "..."` |
| Tags | `jj tag` (list), `jj tag create v1.0` | `git tag`, `git tag -a v1.0` |
| Describe | `jj log -r ::. --no-graph -T "tags"` | `git describe --tags` |

## Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

**Examples:**
```
feat(api): add user authentication endpoint

fix(db): resolve connection pool exhaustion

feat!: redesign the API (BREAKING CHANGE)

chore(deps): update typescript to 5.4.0
```

## Version File Detection

Check these files in order:
1. `package.json` — `"version": "X.Y.Z"`
2. `pyproject.toml` — `version = "X.Y.Z"`
3. `version.txt` or `VERSION` — plain text version

## Pre-release Versioning

Support pre-release versions for beta testing:
- `1.0.0-alpha.1` → `1.0.0-alpha.2` → `1.0.0-beta.1` → `1.0.0`
- Bump pre-release: increment number after pre-release identifier
- Release: remove pre-release suffix (e.g., `1.0.0-rc.3` → `1.0.0`)

## Implementation Notes

### Detecting jj vs git
```bash
# Check for jj repo
if [ -d ".jj" ] || jj root 2>/dev/null; then
    VCS="jj"
else
    VCS="git"
fi
```

### Getting commits since last tag (jj)
```bash
# List tags and find latest
jj tag

# Log since last tag (simplified)
jj log -r "tags()..@" --no-graph -T "description"
```

### Getting commits since last tag (git)
```bash
# Find latest tag
git describe --tags --abbrev=0

# Log since tag
git log <tag>..HEAD --oneline
```

### Writing conventional commit (jj)
```bash
jj commit -m "feat(scope): description"
```

### Writing conventional commit (git)
```bash
git commit -m "feat(scope): description"
```

## Example Interactions

**User:** "Commit these changes"
**Agent:** Analyzes changes, determines type (feat/fix/docs/etc), runs `jj commit -m "type(scope): description"`

**User:** "What version bump should this be?"
**Agent:** Analyzes commits since last tag, reports: "Based on 2 feat commits and 1 fix, recommend MINOR bump (1.2.0 → 1.3.0)"

**User:** "Generate changelog"
**Agent:** Collects commits, categorizes, writes CHANGELOG.md with proper sections

**User:** "Create a release"
**Agent:** Full workflow: detect bump → update version file → generate changelog → commit → suggest tag creation

## Safety Checks

ALWAYS confirm before:
- Creating the first commit in a repo
- Making major version bumps (breaking changes)
- Overwriting existing CHANGELOG.md (check first)

ALWAYS verify:
- Working directory is clean (or changes are intentional)
- User has configured git/jj identity (for commits)
- Version files exist before trying to update them