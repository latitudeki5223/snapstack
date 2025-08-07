# SnapStack

A project integrated with Claude Code GitHub Action for AI-powered development assistance.

## Claude Code GitHub Action Setup

This repository is configured with the Claude Code GitHub Action, which allows you to interact with Claude directly in GitHub issues and pull requests.

### How to Use

Simply mention `@claude` in:
- Pull request descriptions or comments
- Issue descriptions or comments
- Code review comments

Claude will analyze your request and can:
- Write new code and create PRs
- Review existing PRs for bugs and improvements
- Fix reported issues automatically
- Refactor code based on your instructions
- Update documentation

### Examples

In an issue or PR, you can write:
```
@claude please review this code for potential improvements
```

```
@claude can you help fix the bug in the authentication module?
```

```
@claude refactor this function to be more efficient
```

### Setup Requirements

Before using, you need to:

1. **Add the Anthropic API Key** to your repository secrets:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your Anthropic API key

2. **Enable GitHub Actions** if not already enabled in your repository

### Getting Started

1. Create an issue or pull request
2. Mention `@claude` with your request
3. Claude will respond with code suggestions or create PRs automatically

For more information, visit the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code).