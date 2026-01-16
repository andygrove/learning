# Claude Code Instructions

This repository is a knowledge base and tooling for becoming an expert in Apache DataFusion, DataFusion Comet, and Apache Spark.

## Repository Structure

```
learning/
├── prompts/                       # Claude Code session prompts
│   ├── pr-review/                 # PR review prompts
│   │   ├── datafusion-pr-review.md
│   │   └── comet-pr-review.md
│   ├── implementation/            # Implementation prompts
│   │   └── comet-expression.md
│   └── issues/                    # Issue creation prompts
│       └── comet-issue.md
├── docs/                          # Project documentation
│   ├── comet_expressions_pipeline.md  # Expression tracking
│   └── sample_github_issue.md         # Issue template example
├── src/                           # RAG system modules
├── scripts/                       # Utility scripts
│   └── generate_comet_issues.py   # Issue generation script
├── sparkreference/                # Spark expression reference docs
├── chroma_db/                     # Vector database
├── datafusion/                    # DataFusion source
├── datafusion-comet/              # Comet source
└── spark/                         # Spark source
```

## Core Workflows

### 1. Reviewing PRs

Use prompts in `prompts/pr-review/`:

```bash
# DataFusion PRs
# See: prompts/pr-review/datafusion-pr-review.md

# Comet PRs
# See: prompts/pr-review/comet-pr-review.md
```

### 2. Implementing Comet Expressions

Use `prompts/implementation/comet-expression.md` for step-by-step guidance.

Quick workflow:
1. Read Spark reference: `cat sparkreference/docs/expressions/<name>.md`
2. Query codebase: `python scripts/query.py -r datafusion-comet -q "..."`
3. Follow implementation steps in the prompt

### 3. Creating GitHub Issues

```bash
# Preview issue
python scripts/generate_comet_issues.py --expression <name> --dry-run

# Create issue
python scripts/generate_comet_issues.py --expression <name> --create-issues

# List available expressions
python scripts/generate_comet_issues.py --list-available
```

## Key Resources

### ChromaDB Code Search

Query the indexed codebases:

```bash
# General query
python scripts/query.py -q "your query"

# Filter by repo
python scripts/query.py -r datafusion -q "hash join implementation"
python scripts/query.py -r datafusion-comet -q "expression serde"
python scripts/query.py -r spark -q "DateTrunc expression"
```

### Spark Reference Documentation

Comprehensive docs for 442 Spark expressions:

```bash
# View expression spec
cat sparkreference/docs/expressions/<expression_name>.md

# List all documented expressions
ls sparkreference/docs/expressions/
```

### Comet Repository

Location: `/home/andy/git/personal/learning/datafusion-comet`

Key directories:
- `spark/src/main/scala/org/apache/comet/serde/` - Scala serde
- `spark/src/test/scala/org/apache/comet/` - Tests
- `native/spark-expr/src/` - Rust implementations
- `native/proto/src/proto/expr.proto` - Protobuf definitions

## Critical Build Commands

After modifying Rust code in Comet:

```bash
cd native && cargo build && cd ..
./mvnw install -pl common -DskipTests
```

Before creating a PR:

```bash
make  # format + build + test + docs
```

Clear stale cache:

```bash
rm -rf ~/.m2/repository/org/apache/datafusion/comet-*
```

## Expression Pipeline Tracking

See `docs/comet_expressions_pipeline.md` for:
- Implemented expressions
- Unimplemented expressions by difficulty
- Implementation progress
