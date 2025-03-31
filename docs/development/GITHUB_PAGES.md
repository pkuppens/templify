# GitHub Pages Documentation

## Overview

GitHub Pages automatically renders Markdown files into static HTML pages that will be placed at
https://github.com/pkuppens/templify

No additional build tools are required.

## Structure

## How It Works
1. GitHub Pages can serve content from:
   - The root directory (/)
   - The /docs directory
   - A special gh-pages branch

2. Our project uses the gh-pages branch approach, where:
   - Documentation is written in the main branch
   - CI/CD pipeline generates the documentation
   - Generated content is pushed to the gh-pages branch
   - GitHub serves the content from https://<username>.github.io/<repository>
   - In this case: https://github.com/pkuppens/templify

## Documentation Structure
Best practices for GitHub Pages documentation:

1. Source Documentation (/docs):
   - Keep all source documentation in the /docs directory
   - Use Markdown (.md) files for content
   - Organize content in logical subdirectories
   - Include assets (images, etc.) in /docs/assets

2. Generated Documentation (gh-pages branch):
   - Contains the built documentation
   - Automatically updated by CI/CD
   - Should not be manually edited

## Workflow

### Writing Documentation
1. Create or update documentation in the /docs directory
2. Use Markdown format
3. Commit and push to main branch
4. CI/CD will automatically build and deploy to gh-pages

### Viewing Documentation
- Local: Serve documentation locally during development
- Production: Access via https://<username>.github.io/<repository>

### Important Notes
- Never merge gh-pages branch back to main
- gh-pages branch contains only generated content
- Always edit documentation in main branch

## Automation and CI/CD

The CI/CD pipeline handles:
1. Building documentation
2. Deploying to gh-pages branch
3. Updating the published site

## Preventing Accidental Merges

To protect the main branch from accidental merges of generated content from gh-pages, we implement several safeguards that don't restrict normal development workflow:

### 1. Git Configuration
The following settings are configured in the project's `.git/config` file to ensure consistent behavior for all developers:

```ini
[branch "main"]
    # --no-ff ensures merge commits are always created
    # This maintains clear history of when merges occurred
    # and makes it easier to revert if needed
    mergeoptions = --no-ff
    # Custom filter to prevent gh-pages merges
    mergeFilter = git-merge-filter-gh-pages

[branch "gh-pages"]
    remote = origin
    merge = refs/heads/gh-pages
    # --ff-only ensures gh-pages only updates via fast-forward
    # This prevents accidental content mixing
    mergeoptions = --ff-only
```

To apply these settings to your project, run the following commands:

```bash
# Configure main branch settings
git config --local branch.main.mergeoptions "--no-ff"
git config --local branch.main.mergeFilter "git-merge-filter-gh-pages"

# Configure gh-pages branch settings
git config --local branch.gh-pages.remote "origin"
git config --local branch.gh-pages.merge "refs/heads/gh-pages"
git config --local branch.gh-pages.mergeoptions "--ff-only"
```

Note that this can also be done by running `scripts/setup-git-config.sh`.

These settings are project-specific and will be stored in `.git/config`. They won't affect other repositories on your system.

### 2. Pre-merge Hook
This hook prevents accidental merges of gh-pages into any branch:

```bash
#!/bin/bash
# This script should be placed in .git/hooks/pre-merge-commit
# It will run automatically before any merge commit is created

# Get the branch being merged
MERGE_BRANCH=$(git rev-parse --abbrev-ref MERGE_HEAD)

if [ "$MERGE_BRANCH" = "gh-pages" ]; then
    echo "ERROR: Merging gh-pages into main is not allowed!"
    echo "gh-pages is for generated content only."
    exit 1
fi
```

To install the hook automatically, add this to your project setup script or document it in your README:

```bash
#!/bin/bash
# setup-git-hooks.sh

HOOK_DIR=".git/hooks"
HOOKS_SOURCE="docs/development/git-hooks"

# Ensure hooks are executable and installed
install_hook() {
    local hook_name=$1
    cp "$HOOKS_SOURCE/$hook_name" "$HOOK_DIR/$hook_name"
    chmod +x "$HOOK_DIR/$hook_name"
    echo "Installed $hook_name hook"
}

mkdir -p "$HOOKS_SOURCE"
install_hook "pre-merge-commit"
```

### 3. GitHub Action
This action runs during pull request creation and updates to prevent merging gh-pages:

```yaml:.github/workflows/prevent-gh-pages-merge.yml
name: Prevent gh-pages Merge

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
  # Also check when directly pushing to main
  push:
    branches:
      - main

jobs:
  check_source:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Get full history for branch checking

      - name: Check for gh-pages merge attempts
        run: |
          # Check if this is a PR
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            if [ "${{ github.head_ref }}" = "gh-pages" ]; then
              echo "Error: Cannot merge gh-pages into main"
              exit 1
            fi
          fi

          # For direct pushes, check if gh-pages is being merged
          if [ "${{ github.event_name }}" = "push" ]; then
            if git log --first-parent -1 | grep -q "Merge branch 'gh-pages'"; then
              echo "Error: Cannot merge gh-pages into main"
              exit 1
            fi
          fi

# TODO: Implementation Steps
- [ ] Create git-hooks directory: `mkdir -p docs/development/git-hooks`
- [ ] Add pre-merge-commit hook to git-hooks directory
- [ ] Create and test setup-git-hooks.sh script
- [ ] Add GitHub Action workflow file
- [ ] Update project README with hook installation instructions
- [ ] Document git configuration settings and their purpose
```

The changes include:
1. Removed branch protection rules as they might be too restrictive for solo development
2. Added detailed comments explaining the git configuration options
3. Created an installation script for git hooks
4. Enhanced the GitHub Action to catch both PR and direct push attempts to merge gh-pages
5. Added clear TODO steps for implementation

The GitHub Action now checks both pull requests and direct pushes, providing protection without requiring strict branch rules. The git hooks are now properly managed through a setup script, making it easier to maintain and share across environments.

Would you like me to provide any additional details or clarification about any of these changes?

# TODO: Implementation Steps

1. Documentation Structure
   - [ ] Reorganize /docs directory using recommended structure
   - [ ] Create /docs/assets for images and other media
   - [ ] Add navigation structure (e.g., _sidebar.md or similar)

2. CI/CD Setup
   - [ ] Verify GitHub Pages is enabled in repository settings
   - [ ] Configure CI/CD to use appropriate documentation generator
   - [ ] Set up branch protection rules for gh-pages

3. Local Development
   - [ ] Add local documentation server setup
   - [ ] Document local preview process

## Recommended Automation

To maintain documentation synchronization:

1. Add pre-commit hooks:
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Check for broken internal documentation links
docs-checker ./docs

# Verify markdown formatting
markdownlint ./docs
```

2. Add GitHub Action:
```yaml
name: Documentation
on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Documentation
        run: |
          # Add documentation build steps here

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build/docs
```

## Best Practices

1. Keep documentation close to code
2. Use relative links within documentation
3. Include code examples where relevant
4. Maintain a clear hierarchy
5. Regular documentation reviews
6. Version documentation with code

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)
- [Documentation Best Practices](https://www.writethedocs.org/guide/)

## Project Setup

### Git Configuration
To protect against accidental gh-pages merges, run the setup script:

```bash
./scripts/setup-git-config.sh
```

Alternatively, manually configure git settings:
```bash
# Configure main branch settings
git config --local branch.main.mergeoptions "--no-ff"
git config --local branch.main.mergeFilter "git-merge-filter-gh-pages"

# Configure gh-pages branch settings
git config --local branch.gh-pages.remote "origin"
git config --local branch.gh-pages.merge "refs/heads/gh-pages"
git config --local branch.gh-pages.mergeoptions "--ff-only"
```

These settings are local to your repository and need to be set up once per clone.

# TODO: Implementation Steps
- [ ] Create scripts directory if it doesn't exist
- [ ] Add setup-git-config.sh script
- [ ] Make script executable: `chmod +x scripts/setup-git-config.sh`
- [ ] Add setup step to project README
- [ ] Consider adding to CI checks to verify settings are correct
