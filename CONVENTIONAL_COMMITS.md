# Conventional Commits Guide

This project uses [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages. This enables automated versioning and changelog generation.

## Commit Message Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```text

## Types

- **feat**: A new feature (triggers MINOR version bump)
- **fix**: A bug fix (triggers PATCH version bump)
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding or modifying tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

## Breaking Changes

Add `!` after type/scope or include `BREAKING CHANGE:` in footer to trigger MAJOR version bump:

```text
feat!: remove support for Python 3.8

BREAKING CHANGE: Python 3.9+ is now required
```text

## Examples

### Feature Addition

```bash
git commit -m "feat: add video thumbnail generation"
git commit -m "feat(api): add rate limiting to detection endpoints"
```text

### Bug Fix

```bash
git commit -m "fix: correct face detection confidence threshold"
git commit -m "fix(worker): resolve memory leak in video processing"
```text

### Documentation

```bash
git commit -m "docs: update API endpoint documentation"
git commit -m "docs(readme): add deployment instructions"
```text

### Refactoring

```bash
git commit -m "refactor: simplify file upload validation logic"
git commit -m "refactor(services): extract common detection logic"
```text

### Breaking Change

```bash
git commit -m "feat!: change API response format to include metadata"
git commit -m "fix!: update Redis connection to require authentication

BREAKING CHANGE: Redis now requires password authentication.
Update REDIS_URL in .env to include credentials."
```text

## Pre-commit Validation

The conventional-pre-commit hook validates your commit messages automatically. If your commit message doesn't follow the convention, the commit will be rejected with an error message.

### Valid commit message

```bash
git commit -m "feat: add new detection algorithm"
# ✅ Commit succeeds
```text

### Invalid commit message

```bash
git commit -m "added new feature"
# ❌ Commit fails - missing type prefix
```text

### Bypass validation (not recommended)

```bash
git commit -m "WIP: testing" --no-verify
```text

## Multi-line Commits

For detailed commits with body and footer:

```bash
git commit -m "feat: implement batch processing for images

This allows multiple images to be processed in a single API call,
improving efficiency for users uploading multiple files.

Closes #123"
```text

Or use your editor:

```bash
git commit
# Opens editor for multi-line message
```text

## Scopes (Optional)

Add scope to provide additional context:

- `api` - API endpoints
- `worker` - Celery workers
- `services` - Detection services
- `ui` - Web interface
- `docker` - Docker configuration
- `deps` - Dependencies

Examples:

```bash
git commit -m "feat(api): add health check endpoint"
git commit -m "fix(worker): resolve task timeout issues"
git commit -m "chore(deps): update OpenCV to 4.9.0"
```text

## Release Process

1. Commit changes using conventional commits
2. Push to `main` branch
3. Release Please GitHub Action automatically:
   - Analyzes commit messages
   - Determines version bump (MAJOR.MINOR.PATCH)
   - Creates/updates release PR with changelog
   - Creates GitHub release when PR is merged

### Version Bumping

- `fix:` → Patch version (0.0.X)
- `feat:` → Minor version (0.X.0)
- `BREAKING CHANGE:` or `!` → Major version (X.0.0)
- Other types → No version bump

## Tips

1. **Write clear descriptions**: Keep first line under 72 characters
2. **Use imperative mood**: "add feature" not "added feature"
3. **Reference issues**: Use `Closes #123` or `Fixes #456` in footer
4. **Group related changes**: Make atomic commits per logical change
5. **Use body for context**: Explain "why" not "what" (code shows "what")

## Configuration

The conventional commit check is configured in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/compilerla/conventional-pre-commit
  rev: v3.0.0
  hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
```text

To install:

```bash
pre-commit install --hook-type commit-msg
```text

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Release Please Documentation](https://github.com/googleapis/release-please)
- [Semantic Versioning](https://semver.org/)
