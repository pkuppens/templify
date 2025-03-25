# GitHub Pages Documentation Guide

## Overview
GitHub Pages is a static site hosting service that takes files directly from a GitHub repository and publishes a website. It's perfect for project documentation, as it supports Markdown files and can be automatically updated through CI/CD pipelines.

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
   - In this case: https://pkuppens.github.io/templify

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
