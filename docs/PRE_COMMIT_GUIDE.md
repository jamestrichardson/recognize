# Pre-commit Hooks Setup Guide

This project uses [pre-commit](https://pre-commit.com/) to automatically run code quality checks before each commit.

## Quick Start

### 1. Install pre-commit

```bash
# Option 1: Using pip
pip install pre-commit

# Option 2: Using the Makefile
make install-dev
```text

### 2. Install the git hooks

```bash
# Install pre-commit hooks
pre-commit install

# Or use the Makefile
make install-hooks
```text

### 3. Done

Now pre-commit will run automatically on `git commit`.

## What Gets Checked

### Code Quality & Formatting

- **Black**: Code formatting (auto-fixes)
- **isort**: Import sorting (auto-fixes)
- **Flake8**: Style guide enforcement
- **Pylint**: Code analysis (via manual run)
- **MyPy**: Type checking

### Security

- **Bandit**: Security issue detection
- **Safety**: Known security vulnerabilities in dependencies
- **Detect Private Keys**: Prevents committing secrets

### General File Checks

- **Trailing Whitespace**: Removes trailing spaces (auto-fixes)
- **End of File Fixer**: Ensures files end with newline (auto-fixes)
- **Check YAML/JSON/TOML**: Validates syntax
- **Large Files**: Prevents committing files >10MB
- **Merge Conflicts**: Detects unresolved merge markers
- **Mixed Line Endings**: Enforces consistent line endings

### Documentation

- **Markdownlint**: Markdown formatting (auto-fixes)
- **Interrogate**: Docstring coverage check
- **YAML Lint**: YAML file linting

## Manual Execution

### Run on all files

```bash
pre-commit run --all-files

# Or use the Makefile
make pre-commit
```text

### Run on staged files only

```bash
pre-commit run
```text

### Run specific hook

```bash
pre-commit run black --all-files
pre-commit run flake8 --all-files
```text

## Makefile Commands

```bash
make install-dev        # Install all dependencies
make install-hooks      # Install pre-commit hooks
make lint              # Run all linters
make format            # Format code with black and isort
make test              # Run tests
make test-cov          # Run tests with coverage
make pre-commit        # Run pre-commit on all files
make pre-commit-update # Update pre-commit hooks
make security-check    # Run security checks
make verify            # Run lint + test
make ci                # Full CI pipeline
```text

## Bypassing Hooks (Not Recommended)

If you need to commit without running hooks (emergency only):

```bash
git commit --no-verify -m "Emergency fix"
```text

## Configuration Files

- `.pre-commit-config.yaml` - Pre-commit configuration
- `pyproject.toml` - Tool configurations (black, isort, bandit, etc.)
- `.flake8` - Flake8 configuration
- `.markdownlint.yaml` - Markdown linting rules
- `Makefile` - Convenient command shortcuts

## Hook Execution Order

1. **File checks** (trailing whitespace, large files, etc.)
2. **Code formatting** (black, isort) - Auto-fixes
3. **Linting** (flake8)
4. **Type checking** (mypy)
5. **Security** (bandit, safety)
6. **Documentation** (interrogate)
7. **Markdown/YAML** (markdownlint, yamllint) - Auto-fixes

## Troubleshooting

### Hook installation fails

```bash
# Clear cache and reinstall
pre-commit clean
pre-commit install --install-hooks
```text

### Specific hook is failing

```bash
# Skip a specific hook temporarily
SKIP=mypy git commit -m "message"

# Or skip multiple hooks
SKIP=mypy,flake8 git commit -m "message"
```text

### Update hooks to latest versions

```bash
pre-commit autoupdate

# Or use Makefile
make pre-commit-update
```text

### Hook runs too slowly

```bash
# Run hooks on changed files only (default behavior)
git commit

# Force run on all files
git commit --all-files
```text

## Code Style Standards

### Line Length

- **Maximum**: 100 characters
- Configured in: `pyproject.toml`, `.flake8`

### Import Order (isort)

1. Standard library imports
2. Third-party imports
3. Local application imports

### Type Hints

- Recommended but not enforced
- MyPy runs with `--ignore-missing-imports`

### Docstrings

- Minimum 50% coverage required
- Google or NumPy style preferred

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Lint and Test

on: [push, pull_request]

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: make install-dev
      - name: Run pre-commit
        run: make pre-commit
      - name: Run tests
        run: make test-cov
```text

### GitLab CI Example

```yaml
lint-test:
  image: python:3.11
  script:
    - make install-dev
    - make ci
```text

## Best Practices

1. **Run hooks before pushing**: `pre-commit run --all-files`
2. **Keep hooks updated**: `pre-commit autoupdate` monthly
3. **Fix issues, don't bypass**: Address linting issues rather than skipping
4. **Use make commands**: `make lint`, `make format`, etc.
5. **Test locally first**: Run `make verify` before pushing

## Adding Custom Hooks

Edit `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/your/custom-hook
    rev: v1.0.0
    hooks:
      - id: your-hook-id
        args: ['--custom-arg']
```text

Then update:

```bash
pre-commit install
```text

## Excluding Files

### Exclude from all hooks

Add to `.pre-commit-config.yaml`:

```yaml
exclude: '^(migrations/|legacy/)'
```text

### Exclude from specific tools

Edit tool config in `pyproject.toml`:

```toml
[tool.black]
extend-exclude = '''
/(
  legacy
  | old_code
)/
'''
```text

## Performance Tips

1. **Use pre-commit.ci** for faster CI runs
2. **Cache dependencies** in CI/CD
3. **Run locally first** to catch issues early
4. **Keep hooks updated** for performance improvements

## Getting Help

- Pre-commit docs: <https://pre-commit.com/>
- Tool-specific docs:
  - Black: <https://black.readthedocs.io/>
  - Flake8: <https://flake8.pycqa.org/>
  - MyPy: <https://mypy.readthedocs.io/>
  - Bandit: <https://bandit.readthedocs.io/>

## Summary

With pre-commit hooks installed:

- ✅ Code is automatically formatted
- ✅ Style issues are caught before commit
- ✅ Security vulnerabilities are detected
- ✅ Tests run automatically (optional)
- ✅ Documentation standards are enforced
- ✅ Team maintains consistent code quality

**Install now**: `make install-hooks`
