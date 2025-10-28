#!/usr/bin/env bash
# Quick reference guide for conventional commits

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║          CONVENTIONAL COMMITS QUICK REFERENCE                ║
╚══════════════════════════════════════════════════════════════╝

FORMAT:
  <type>[optional scope]: <description>

COMMON TYPES:
  feat:       ✨ New feature (minor version bump)
  fix:        🐛 Bug fix (patch version bump)
  docs:       📝 Documentation changes
  style:      💄 Code style (formatting, missing semi-colons, etc)
  refactor:   ♻️  Code refactoring
  perf:       ⚡ Performance improvements
  test:       ✅ Adding or updating tests
  build:      📦 Build system or dependencies
  ci:         👷 CI configuration changes
  chore:      🔧 Maintenance tasks

BREAKING CHANGES:
  feat!:      💥 Breaking change (major version bump)
  Or use:     BREAKING CHANGE: in commit body

EXAMPLES:
  ✅ git commit -m "feat: add video thumbnail generation"
  ✅ git commit -m "fix(api): resolve timeout in video processing"
  ✅ git commit -m "docs: update deployment guide"
  ✅ git commit -m "feat!: change API response format"
  ❌ git commit -m "added new feature"
  ❌ git commit -m "Fixed bug"

WITH SCOPE (optional):
  api       - API endpoints
  worker    - Celery workers
  services  - Detection services
  ui        - Web interface
  docker    - Docker configuration

MULTI-LINE:
  git commit
  # Opens editor for detailed message:

  feat(api): add batch image processing

  Allow processing multiple images in a single API call.
  This improves efficiency for bulk uploads.

  Closes #123

VERSION BUMPING:
  fix:              0.0.X  (patch)
  feat:             0.X.0  (minor)
  BREAKING CHANGE:  X.0.0  (major)

TESTING YOUR COMMIT:
  ./test-commits.sh

SETUP:
  make install-hooks  # Install commit-msg validation

DOCUMENTATION:
  CONVENTIONAL_COMMITS.md  - Detailed guide
  RELEASE_SETUP.md         - Release automation

EOF
