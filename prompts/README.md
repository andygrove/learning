# Prompts

This directory contains prompts for Claude Code sessions focused on DataFusion, Comet, and Spark development.

## Directory Structure

```
prompts/
├── pr-review/                    # PR review prompts
│   ├── datafusion-pr-review.md   # Review DataFusion PRs
│   └── comet-pr-review.md        # Review Comet PRs
├── implementation/               # Implementation prompts
│   └── comet-expression.md       # Implement Comet expressions
└── issues/                       # Issue creation prompts
    └── comet-issue.md            # Create Comet feature issues
```

## Available Prompts

### PR Review

| Prompt | Use When |
|--------|----------|
| `pr-review/datafusion-pr-review.md` | Reviewing Apache DataFusion PRs |
| `pr-review/comet-pr-review.md` | Reviewing DataFusion Comet PRs |

### Implementation

| Prompt | Use When |
|--------|----------|
| `implementation/comet-expression.md` | Implementing a Spark expression in Comet |

### Issue Creation

| Prompt | Use When |
|--------|----------|
| `issues/comet-issue.md` | Creating GitHub issues for unsupported Spark expressions |

## Using Prompts with Claude Code

### Option 1: Copy the prompt into your session

```bash
# Start Claude Code and paste the relevant prompt section
claude
```

### Option 2: Reference the prompt file

```bash
# Tell Claude Code to read and follow the prompt
claude "Read prompts/pr-review/comet-pr-review.md and use it to review PR #123"
```

## Supporting Resources

All prompts leverage these resources:

1. **ChromaDB Index** - Semantic search over DataFusion, Comet, and Spark codebases
   ```bash
   python scripts/query.py -r <repo> -q "your query"
   ```

2. **Spark Reference Docs** - Comprehensive documentation for Spark expressions
   ```bash
   cat sparkreference/docs/expressions/<expression_name>.md
   ```

## Adding New Prompts

When adding a new prompt:

1. Place it in the appropriate subdirectory (`pr-review/`, `implementation/`, or `issues/`)
2. Include sections for:
   - Quick start / usage
   - How to use ChromaDB queries
   - How to use Spark reference docs
   - Step-by-step workflow
   - Common patterns or templates
3. Update this README
