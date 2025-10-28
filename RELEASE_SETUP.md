# Release Please & Conventional Commits Setup

## What Was Implemented

### 1. GitHub Actions Release Workflow

Created `.github/workflows/release-please.yml` that:

- Runs automatically on every push to `main` branch
- Uses `googleapis/release-please-action@v4`
- Analyzes commit messages for version bumping
- Creates/updates release PR with changelog
- Creates GitHub releases when PR is merged

### 2. Conventional Commits Pre-commit Hook

Added to `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/compilerla/conventional-pre-commit
  rev: v3.0.0
  hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
```text

This validates every commit message follows the Conventional Commits specification.

### 3. Version File

Created `app/version.py` for Release Please to manage:

```python
__version__ = "0.0.0"
```text

Release Please will automatically update this file with each release.

### 4. Documentation

Created `CONVENTIONAL_COMMITS.md` with:

- Commit message format specification
- Type definitions (feat, fix, docs, etc.)
- Breaking change syntax
- Examples for common scenarios
- Scope usage guidelines
- Multi-line commit instructions

Updated `README.md` with:

- Conventional Commits section in Development
- Release Process section explaining automation
- Links to detailed guides

Updated `.github/workflows/README.md` with:

- Documentation of release-please.yml workflow
- Explanation of version bumping rules
- Release process overview

### 5. Makefile Enhancement

Updated `install-hooks` target to include helpful message about conventional commits.

## How It Works

### Commit Validation (Local)

1. Developer makes a commit
2. Pre-commit hook validates message format
3. If invalid, commit is rejected with error message
4. Developer fixes message and commits again

Example valid commits:

```bash
git commit -m "feat: add batch image processing"
git commit -m "fix(api): resolve timeout in video endpoint"
git commit -m "docs: update API documentation"
```text

### Release Automation (CI/CD)

1. Developer pushes conventional commits to feature branch
2. Feature branch merged to `main` via PR
3. Release Please workflow runs on `main` push
4. Analyzes commits since last release
5. Determines version bump:
   - `fix:` → Patch (0.0.X)
   - `feat:` → Minor (0.X.0)
   - `BREAKING CHANGE:` → Major (X.0.0)
6. Creates/updates release PR titled "chore(main): release X.X.X"
7. Release PR includes:
   - Updated `app/version.py`
   - Updated CHANGELOG.md with categorized changes
8. When release PR is merged:
   - Creates GitHub release
   - Adds git tag (vX.X.X)
   - Publishes release notes

## Installation

To enable conventional commits validation:

```bash
# Automated setup
./setup-dev.sh

# Or manually
make install-hooks

# Or with pre-commit directly
pre-commit install --hook-type commit-msg
```text

## Testing Locally

### Valid Commit (Should Succeed)

```bash
git commit -m "feat: add new feature"
# ✅ Commit succeeds
```text

### Invalid Commit (Should Fail)

```bash
git commit -m "added new feature"
# ❌ Rejected: [Commit message] does not follow Conventional Commits formatting
```text

### Breaking Change

```bash
git commit -m "feat!: change API response structure

BREAKING CHANGE: API now returns data in different format"
# ✅ Commit succeeds, will trigger major version bump
```text

## GitHub Actions Permissions

The release-please workflow requires:

```yaml
permissions:
  contents: write        # To create releases and tags
  pull-requests: write   # To create/update release PRs
```text

These are configured in the workflow file.

## First Release

When you're ready for the first release:

1. Ensure you have conventional commits in main branch
2. Push to main (or merge PR with conventional commits)
3. Release Please will create initial release PR
4. Review and merge the release PR
5. First release (v1.0.0) will be created!

## Configuration Options

Release Please can be customized via `.release-please-config.json`:

```json
{
  "release-type": "python",
  "packages": {
    ".": {
      "package-name": "recognize",
      "changelog-path": "CHANGELOG.md",
      "version-file": "app/version.py"
    }
  }
}
```text

This is optional - Release Please uses sensible defaults for Python projects.

## Benefits

### For Developers

- Clear commit message standards
- Automatic validation prevents mistakes
- No manual version management
- Standardized changelog format

### For Project

- Semantic versioning enforced
- Complete change history
- Professional release notes
- Automated release process
- Easy to track features/fixes between versions

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Release Please Documentation](https://github.com/googleapis/release-please)
- [Semantic Versioning](https://semver.org/)
- [Pre-commit Framework](https://pre-commit.com/)
