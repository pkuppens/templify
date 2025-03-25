#!/bin/bash
# Setup script to configure git settings for the project

# > GitHub Pages branch protections
# Configure main branch settings
git config --local branch.main.mergeoptions "--no-ff"
git config --local branch.main.mergeFilter "git-merge-filter-gh-pages"

# Configure gh-pages branch settings
git config --local branch.gh-pages.remote "origin"
git config --local branch.gh-pages.merge "refs/heads/gh-pages"
git config --local branch.gh-pages.mergeoptions "--ff-only"

echo "Git configuration for GitHub Pages protection has been set up"
# < GitHub Pages branch protections
