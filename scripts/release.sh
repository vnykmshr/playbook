#!/bin/bash

# Engineering Playbook Release Script
# Automates version bumping, changelog updates, and git tagging

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Verify we're in the repo root
if [ ! -f "README.md" ] || [ ! -d ".git" ]; then
    print_error "Must be run from playbook repo root"
    exit 1
fi

# Get current version from git tags
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
print_info "Latest tag: $LATEST_TAG"

# Parse current version
CURRENT_VERSION=${LATEST_TAG#v}  # Remove 'v' prefix

# Prompt for new version
print_info "Current version: $CURRENT_VERSION"
echo -n "Enter new version (e.g., 1.2.1): "
read NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    print_error "Version cannot be empty"
    exit 1
fi

NEW_TAG="v$NEW_VERSION"

# Verify version format (basic semantic versioning check)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_warning "Version doesn't match semantic versioning (X.Y.Z). Proceeding anyway..."
fi

# Check if tag already exists
if git rev-parse "$NEW_TAG" >/dev/null 2>&1; then
    print_error "Tag $NEW_TAG already exists"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    print_error "Uncommitted changes exist. Commit or stash them first."
    exit 1
fi

# Confirm release
print_info ""
print_info "Release summary:"
print_info "  Current version: $CURRENT_VERSION"
print_info "  New version: $NEW_VERSION"
print_info "  New tag: $NEW_TAG"
echo ""
read -p "Proceed with release? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Release cancelled"
    exit 1
fi

# Create git tag with instructions
print_info "Creating git tag..."
git tag -a "$NEW_TAG" -m "Release $NEW_TAG

Automated release via scripts/release.sh

To view release details:
  git show $NEW_TAG

To push tag to remote:
  git push origin $NEW_TAG

To delete this tag:
  git tag -d $NEW_TAG
  git push origin --delete $NEW_TAG"

print_success "Tag $NEW_TAG created"

print_info ""
print_info "Next steps:"
print_info "1. Update CHANGELOG.md with release highlights"
print_info "2. Commit CHANGELOG changes: git add CHANGELOG.md && git commit -m 'docs: release notes for $NEW_TAG'"
print_info "3. Amend tag with final commit: git tag -d $NEW_TAG && git tag -a $NEW_TAG ..."
print_info "4. Push tag: git push origin $NEW_TAG"
print_info "5. GitHub will create a Release automatically"
print_info ""
print_success "Release preparation complete!"
