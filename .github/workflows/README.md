# GitHub Actions CI/CD

This directory contains GitHub Actions workflow files for continuous integration and deployment.

## Workflows

### ci.yml - Continuous Integration

Runs on every push to main and feature branches, and on all pull requests.

**Jobs:**

1. **pre-commit** - Runs all pre-commit hooks
   - Code formatting (black, isort)
   - Linting (flake8, pylint)
   - Type checking (mypy)
   - Security scanning (bandit)
   - Documentation checks
   - File validation

2. **test** - Runs test suite
   - Tests on Python 3.9, 3.10, 3.11
   - Code coverage reporting
   - Uploads coverage to Codecov

3. **security** - Security scanning
   - Bandit for code security issues
   - Safety for dependency vulnerabilities

4. **docker** - Docker build validation
   - Builds Docker image
   - Tests container startup

### release-please.yml - Automated Releases

Runs on every push to `main` branch.

**Process:**

1. Analyzes commit messages using Conventional Commits
2. Determines version bump (MAJOR.MINOR.PATCH)
3. Creates/updates release PR with:
   - Updated version in `app/version.py`
   - Auto-generated CHANGELOG.md
4. When release PR is merged:
   - Creates GitHub release with tag
   - Publishes release notes
   - Optionally builds/pushes Docker images

**Commit Format Requirements:**

- `fix:` → Patch version bump (0.0.X)
- `feat:` → Minor version bump (0.X.0)
- `BREAKING CHANGE:` or `!` → Major version bump (X.0.0)

See [CONVENTIONAL_COMMITS.md](../../CONVENTIONAL_COMMITS.md) for detailed guide.

## Local Development

Before pushing code, run the same checks locally:

```bash
# Run all CI checks
make ci

# Or run individual checks
make lint          # Pre-commit hooks
make test          # Test suite
make security-check # Security scans
make docker-build  # Docker build
```text

## Required Secrets

No secrets are required for the default CI workflow. Optional secrets:

- `CODECOV_TOKEN` - For private repositories (Codecov coverage upload)

## Branch Protection

Recommended branch protection rules for `main`:

- Require status checks to pass before merging
- Required checks: `pre-commit`, `test`, `security`, `docker`
- Require branches to be up to date before merging
- Require pull request reviews

## Adding New Workflows

When adding new workflow files:

1. Place them in `.github/workflows/`
2. Use descriptive names (e.g., `deploy-production.yml`)
3. Document the workflow purpose in this README
4. Test locally before committing
