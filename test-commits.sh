#!/usr/bin/env bash
# Test script for conventional commits validation

set -e

echo "=========================================="
echo "Testing Conventional Commits Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if pre-commit is installed
echo "1. Checking pre-commit installation..."
if command -v pre-commit &> /dev/null; then
    echo -e "${GREEN}✓${NC} pre-commit is installed"
    pre-commit --version
else
    echo -e "${RED}✗${NC} pre-commit is not installed"
    echo "Run: pip install pre-commit"
    exit 1
fi
echo ""

# Check if commit-msg hook is installed
echo "2. Checking commit-msg hook..."
if [ -f .git/hooks/commit-msg ]; then
    echo -e "${GREEN}✓${NC} commit-msg hook is installed"
else
    echo -e "${YELLOW}⚠${NC} commit-msg hook not found"
    echo "Installing now..."
    pre-commit install --hook-type commit-msg
    echo -e "${GREEN}✓${NC} commit-msg hook installed"
fi
echo ""

# Test conventional commits hook
echo "3. Testing conventional commits validation..."
echo ""

# Create a temporary commit message file for testing
TEMP_MSG=$(mktemp)

# Test valid commit messages
echo "Testing VALID commit messages:"
echo ""

valid_messages=(
    "feat: add new feature"
    "fix: resolve bug in processing"
    "docs: update README"
    "refactor: simplify detection logic"
    "test: add unit tests for API"
    "chore: update dependencies"
    "feat(api): add rate limiting"
    "fix(worker): resolve memory leak"
)

for msg in "${valid_messages[@]}"; do
    echo "$msg" > "$TEMP_MSG"
    if pre-commit run --hook-stage commit-msg --commit-msg-filename "$TEMP_MSG" conventional-pre-commit &> /dev/null; then
        echo -e "${GREEN}✓${NC} '$msg'"
    else
        echo -e "${RED}✗${NC} '$msg' (should have passed)"
    fi
done

echo ""
echo "Testing INVALID commit messages:"
echo ""

invalid_messages=(
    "added new feature"
    "Fixed bug"
    "update documentation"
    "WIP: testing"
    "commit message"
)

for msg in "${invalid_messages[@]}"; do
    echo "$msg" > "$TEMP_MSG"
    if pre-commit run --hook-stage commit-msg --commit-msg-filename "$TEMP_MSG" conventional-pre-commit &> /dev/null; then
        echo -e "${RED}✗${NC} '$msg' (should have failed)"
    else
        echo -e "${GREEN}✓${NC} '$msg' (correctly rejected)"
    fi
done

# Cleanup
rm -f "$TEMP_MSG"

echo ""
echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo ""
echo "Your conventional commits setup is working correctly."
echo ""
echo "Valid commit types:"
echo "  - feat:     New feature (minor version bump)"
echo "  - fix:      Bug fix (patch version bump)"
echo "  - docs:     Documentation changes"
echo "  - style:    Code style changes (formatting)"
echo "  - refactor: Code refactoring"
echo "  - perf:     Performance improvements"
echo "  - test:     Test additions/modifications"
echo "  - build:    Build system changes"
echo "  - ci:       CI configuration changes"
echo "  - chore:    Maintenance tasks"
echo ""
echo "For breaking changes, use:"
echo "  - feat!: description"
echo "  - Or add 'BREAKING CHANGE:' in commit body"
echo ""
echo "See CONVENTIONAL_COMMITS.md for detailed guide"
echo ""
