---
name: my-semantic-release
description: |
  **ALWAYS use when user mentions:** "release", "ship it", "cut a release",
  "changelog", "version bump", "semver", "conventional commit".

  **DO NOT use for:** daily VCS operations — use @skills/my-jj-workflow.

  Automates semantic versioning, changelog generation, and release workflows.
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

**Concrete commands:**
```bash
# Find last tag (jj or git)
git describe --tags --abbrev=0

# Get commits since last tag
git log v1.2.0..HEAD --oneline --no-decorate

# Or with jj (in colocated repo)
jj log -r 'tags()::@' --no-graph
```

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

**Concrete analysis commands:**
```bash
# Get all commits since last tag with bodies (to check for BREAKING CHANGE)
git log v1.2.0..HEAD --format='%s%n%b%n---' | grep -E '(BREAKING CHANGE:|^feat:|^fix:|^docs:|^style:|^refactor:)'

# Quick count by type
git log v1.2.0..HEAD --format='%s' | grep -c '^feat:'  # count features
git log v1.2.0..HEAD --format='%s' | grep -c '^fix:'   # count fixes
git log v1.2.0..HEAD --format='%b' | grep -c 'BREAKING CHANGE'  # count breaking
```

**Decision rules:**
- `BREAKING CHANGE:` in any commit → **MAJOR** (1.2.0 → 2.0.0)
- `feat:` present → **MINOR** (1.2.0 → 1.3.0) (if no breaking change)
- `fix:` present → **PATCH** (1.2.0 → 1.2.1) (if no feat/breaking)
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
│  STEP 0: PRE-RELEASE VERIFICATION (Critical!)                 │
│  └─> Run full check suite (biome, tests, typecheck)          │
│      └─> Fix any format/lint issues BEFORE tagging           │
├─────────────────────────────────────────────────────────────┤
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

**⚠️ CRITICAL: Pre-Release Verification**

ALWAYS run full checks before tagging. CI failures after tagging require force-pushing the tag:

```bash
# Step 0: Verify everything passes BEFORE tagging
just check  # or: npm run check, make check, etc.

# Common pre-release failures:
# 1. Biome format issues (package.json indentation, import sorting)
# 2. Test failures
# 3. TypeScript errors
# 4. Missing test coverage
```

**Concrete execution (example: 1.2.0 → 1.3.0):**

```bash
# STEP 1: Determine version (found feat: commits, no breaking changes)
# Decision: MINOR bump → 1.3.0

# STEP 2: Update CHANGELOG.md (prepend new section)
# Edit file manually or use automated tool

# STEP 3: Bump version in package.json
# Using jq:
cat package.json | jq '.version = "1.3.0"' > package.json.tmp && mv package.json.tmp package.json

# Or edit Cargo.toml manually:
# version = "1.3.0"

# STEP 4: Describe the release (jj workflow)
jj describe -m "chore(release): 1.3.0"

# STEP 5: Commit the release
jj commit

# STEP 6: Tag the release (using git in colocated repo)
git tag -a "v1.3.0" -m "Release v1.3.0"

# STEP 7: Push (see @skills/my-jj-workflow for push commands)
git push origin main
git push origin v1.3.0
```

## Integration with VCS

This skill assumes you have version control set up (see @skills/my-jj-workflow for jj/git workflows). The release workflow:

1. **Reads** commit history via jj/git
2. **Writes** changelog, version bumps, commits, tags
3. **Uses** jj or git depending on your setup

## Custom Release Tools

Some projects have custom release automation (e.g., `just release`, `make release`, `npm run release`) that handles tagging and pushing automatically. **Check first** before manually tagging.

**Signs of custom release tools:**
- `justfile`, `Makefile`, or `package.json` scripts with `release` target
- Workflow files that trigger on tags but also create tags themselves
- Documentation saying "run `just release`" instead of manual tagging

**If custom tool exists:**
1. Bump version in `package.json` (or relevant file)
2. Update `CHANGELOG.md`
3. Commit with `chore(release): X.X.X` message
4. Run the custom tool (e.g., `just release`) - **it will tag and push for you**

**Do NOT manually run `git tag` if the tool does it automatically** - this creates duplicate or mismatched tags.

### Example: npm Project with just release

A typical npm project with `just release` which:
- Reads version from `package.json`
- Validates version matches conventional commits
- Creates and pushes the tag automatically
- **Monitors GitHub Actions with auto-retry (up to 3 times)**

**Correct workflow:**
```bash
# 1-3. Update files and commit
jj describe -m "chore(release): X.X.X"
jj commit

# 4. Run the tool (handles everything including monitoring)
just release
```

**Wrong workflow (creates tag at wrong commit):**
```bash
git tag -a vX.X.X -m "Release vX.X.X"  # DON'T do this manually!
just release  # Tool also tries to create tag - conflict!
```

**Advanced: Skip monitoring**
```bash
RELEASE_NO_WATCH=1 just release  # Push tag but don't watch CI
```

## Common CI Failures & Recovery

### Failure: Biome Format Errors

**Symptom:** CI fails with "Formatter would have printed the following content"

**Common causes:**
- `jq` modified `package.json` with wrong indentation (2 spaces vs tabs)
- New test files have unsorted imports
- File saved without final newline

**Fix:**
```bash
# Local fix
just fix  # or: npx @biomejs/biome check --write .

# Commit the fix
jj commit -m "style: fix biome formatting"

# Move tag to fixed commit (if already pushed)
git tag -d vX.Y.X
git tag -a vX.Y.X -m "Release vX.Y.X" <new-commit-hash>
git push --force origin vX.Y.X
```

### Failure: Test Failures

**Symptom:** CI fails during test phase

**Fix:**
```bash
# Run tests locally
just test

# Fix failures, commit, retag
```

### Failure: TypeScript Errors

**Symptom:** `npx tsc --noEmit` fails

**Fix:**
```bash
# Check types locally
npx tsc --noEmit --skipLibCheck

# Fix errors, commit, retag
```

## Example Release Session

**Before:** package.json has `"version": "1.2.0"`, last tag is `v1.2.0`

```bash
# User: "ship it"

# 1. Determine version bump
$ git log v1.2.0..HEAD --format='%s' | grep -E '^feat:|^fix:'
feat: add user profiles
fix: handle auth edge case
→ Recommendation: MINOR bump (1.2.0 → 1.3.0)

# 2. Update CHANGELOG.md (prepend new section)
$ cat > /tmp/changelog_section.md << 'EOF'
## [1.3.0] - 2026-04-19

### Added
- User profiles feature

### Fixed
- Auth edge case handling
EOF
$ cat /tmp/changelog_section.md CHANGELOG.md > CHANGELOG.md.new
$ mv CHANGELOG.md.new CHANGELOG.md

# 3. Bump version in package.json
$ cat package.json | jq '.version = "1.3.0"' > package.json.tmp
$ mv package.json.tmp package.json

# 4. Stage changes and describe
$ jj st  # shows modified: CHANGELOG.md, package.json
$ jj describe -m "chore(release): 1.3.0"

# 5. Commit the release
$ jj commit

# 6. Tag and push
$ git tag -a v1.3.0 -m "Release v1.3.0"
$ git push origin main && git push origin v1.3.0

# After: v1.3.0 tag exists, package.json shows 1.3.0, CHANGELOG.md updated
```

## When NOT to Use This Skill

- Daily commit operations → Use @skills/my-jj-workflow
- Checking what changed → Use @skills/my-jj-workflow
- Push to GitHub → Use @skills/my-jj-workflow
- Worktree management → Use @skills/my-jj-workflow

Use this skill **only** when the conversation is about releases, versioning, or changelog.
