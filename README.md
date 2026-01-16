# Learning - DataFusion, Comet & Spark Expert System

A knowledge base and tooling for becoming an expert in Apache DataFusion, DataFusion Comet, and Apache Spark. Includes:

- **RAG System**: Semantic code search over 103k+ indexed code chunks
- **Spark Reference**: Comprehensive documentation for 442 Spark expressions
- **Claude Code Prompts**: Structured prompts for PR review and implementation

## Quick Start

### 1. Clone and Setup

```bash
git clone <this-repo>
cd learning

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install sentence-transformers chromadb anthropic
```

### 2. Clone Source Repositories

```bash
git clone --depth 1 https://github.com/apache/datafusion.git
git clone --depth 1 https://github.com/apache/datafusion-comet.git
git clone --depth 1 https://github.com/apache/spark.git
```

### 3. Build the Index

```bash
python scripts/build_index.py
```

## Core Features

### Semantic Code Search

Query the indexed codebases using natural language:

```bash
# Interactive mode
python scripts/query.py --backend local

# Single query with repo filter
python scripts/query.py -r datafusion -q "How does DataFusion implement hash joins?"
python scripts/query.py -r spark -q "DateTrunc expression implementation"
```

### Spark Reference Documentation

Comprehensive documentation for Spark SQL expressions:

```bash
# View expression spec
cat sparkreference/docs/expressions/date_trunc.md

# Serve as website
./scripts/docs-serve.sh
```

### Claude Code Prompts

Structured prompts for common workflows:

| Prompt | Purpose |
|--------|---------|
| `prompts/pr-review/datafusion-pr-review.md` | Review DataFusion PRs |
| `prompts/pr-review/comet-pr-review.md` | Review Comet PRs |
| `prompts/implementation/comet-expression.md` | Implement Comet expressions |

### GitHub Issue Generation

Create well-formatted issues for Comet expressions:

```bash
# Preview
python scripts/generate_comet_issues.py --expression levenshtein --dry-run

# Create
python scripts/generate_comet_issues.py --expression levenshtein --create-issues
```

## Project Structure

```
learning/
├── prompts/                    # Claude Code session prompts
│   ├── pr-review/              # PR review prompts
│   └── implementation/         # Implementation prompts
├── docs/                       # Project documentation
├── src/                        # RAG system modules
│   ├── chunker.py              # Code parsing
│   ├── indexer.py              # ChromaDB indexing
│   └── query.py                # Query interface
├── scripts/                    # CLI tools
├── sparkreference/             # Spark expression docs (442 files)
├── chroma_db/                  # Vector database
├── datafusion/                 # DataFusion source
├── datafusion-comet/           # Comet source
└── spark/                      # Spark source
```

## Requirements

- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM (for local LLM inference)
- ~15GB disk space

## LLM Backends

### Local Models (Free)

```bash
python scripts/query.py --backend local --model deepseek-coder-1.3b
```

### Claude API

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/query.py --backend claude
```

### Context Only (No LLM)

```bash
python scripts/query.py -q "your query"
```

## Contributing

See `CLAUDE.md` for detailed instructions on:
- Reviewing PRs
- Implementing Comet expressions
- Creating GitHub issues
