---
name: my-semantic-release
description: |
  **ALWAYS use when user mentions:** "release", "ship it", "cut a release", "changelog", 
  "version bump", "semver", "conventional commit", or "what version should this be".

  **DO NOT use for:** daily jj/git operations (status, diff, commit, push) —
  use @skills/my-jj-workflow for version control workflows.

  Automates semantic versioning, changelog generation, and release workflows.
  Assumes jj or git for VCS operations.
---

# My Semantic Release

Automate semantic versioning, changelog generation, and release workflows.

## Overview

This skill provides workflows for:
1. **Semantic versioning** — Determine version bumps from conventional commits
2. **Changelog generation** — Auto-generate CHANGELOG.md from commit history
3. **Conventional commits** — Format commits for release automation
4. **Release workflow** — Full release automation chain

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
1. Find last release tag/version
2. Collect commits since last release
3. Categorize by conventional commit type
4. Write/update CHANGELOG.md

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

### 3. Format Conventional Commit

**Trigger phrases:** "format this commit", "conventional commit for release", "write commit message for feat/fix"

Use this to write properly formatted commit messages that feed into release automation:

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
├─────────────────────────────────────────────────────────────┤
│  STEP 2: Changelog Generation                                 │
│  └─> Generate CHANGELOG.md with new version section            │
├─────────────────────────────────────────────────────────────┤
│  STEP 3: Version Bump                                         │
│  └─> Update package.json, Cargo.toml, etc.                 │
│      └─> Commit version bump                                 │
├─────────────────────────────────────────────────────────────┤
│  STEP 4: Release Commit & Tag                                 │
│  └─> Commit: "chore(release): X.Y.Z"                        │
│      └─> Tag: vX.Y.Z                                         │
└─────────────────────────────────────────────────────────────┘
```

**Execution:**
```bash
# Use jj or git for commits (see @skills/my-jj-workflow)
jj commit -m "chore(release): $(cat VERSION)"
git tag -a "v$(cat VERSION)" -m "Release v$(cat VERSION)"
```

## Integration with VCS

This skill assumes you have version control set up (see @skills/my-jj-workflow for jj/git workflows). The release workflow:

1. **Reads** commit history via jj/git
2. **Writes** changelog, version bumps, commits, tags
3. **Uses** jj or git depending on your setup

## Example Release Session

```bash
# User: "ship it"

# 1. Determine version bump
→ feat: add user profiles + fix: auth bug
→ Recommendation: MINOR bump (1.2.0 → 1.3.0)

# 2. Generate changelog
→ Update CHANGELOG.md with new "1.3.0" section

# 3. Bump version files
→ package.json: 1.2.0 → 1.3.0

# 4. Commit and tag
→ jj commit -m "chore(release): 1.3.0"
→ git tag -a v1.3.0 -m "Release v1.3.0"

# 5. Push (use @skills/my-jj-workflow for push commands)
→ git push origin main && git push origin v1.3.0
```

## When NOT to Use This Skill

- Daily commit operations → Use @skills/my-jj-workflow
- Checking what changed → Use @skills/my-jj-workflow
- Push to GitHub → Use @skills/my-jj-workflow
- Worktree management → Use @skills/my-jj-workflow

Use this skill **only** when the conversation is about releases, versioning, or changelog.
