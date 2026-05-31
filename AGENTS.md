# Agent Instructions

## GitHub CLI
The GitHub CLI (`gh`) is installed in this environment and should be used for managing pull requests and merges.

### Auto-merge PRs
After publishing a PR, you should enable auto-merge using:
```bash
gh pr merge --auto --squash --delete-branch
```
