# Learning - Code RAG for DataFusion, Comet, and Spark

A retrieval-augmented generation (RAG) system for querying the Apache DataFusion, DataFusion Comet, and Apache Spark codebases. Ask natural language questions about the code and get answers grounded in the actual source.

## Features

- **103k+ indexed code chunks** from DataFusion (Rust), Comet (Rust/Scala), and Spark (Scala/Java)
- **Semantic search** using sentence-transformers embeddings
- **Multiple LLM backends**: local models (free), Claude API, or context-only mode
- **Smart code chunking** that respects function/class boundaries

## Quick Start

### 1. Clone the Repository

```bash
git clone <this-repo>
cd learning
```

### 2. Clone Source Repositories

```bash
git clone --depth 1 https://github.com/apache/datafusion.git
git clone --depth 1 https://github.com/apache/datafusion-comet.git
git clone --depth 1 https://github.com/apache/spark.git
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip
```

### 4. Install Dependencies

```bash
# Install PyTorch with CUDA support (for NVIDIA GPUs)
pip install torch --index-url https://download.pytorch.org/whl/cu121

# Install remaining dependencies
pip install sentence-transformers chromadb numpy pandas matplotlib jupyter tqdm

# For local LLM inference
pip install transformers accelerate bitsandbytes

# Optional: for Claude API
pip install anthropic
```

### 5. Build the Index

This indexes all source files into a vector database (~5-10 minutes):

```bash
python scripts/build_index.py
```

### 6. Query the Codebase

```bash
# Interactive mode with local model (recommended)
python scripts/query.py --backend local

# Single query
python scripts/query.py --backend local -q "How does DataFusion implement hash joins?"

# Filter by repository
python scripts/query.py --backend local -r spark -q "How does Catalyst optimize queries?"

# Context-only mode (just shows retrieved code, no LLM)
python scripts/query.py -q "shuffle implementation"
```

## Usage Modes

### Local Model (Free, Runs on GPU)

Uses code-focused models that run entirely on your GPU:

```bash
python scripts/query.py --backend local
```

Available model presets:

| Preset | Size | Quantized | Notes |
|--------|------|-----------|-------|
| `deepseek-coder-1.3b` | 2.5GB | No | Default, fast, good quality |
| `deepseek-coder-6.7b` | ~4GB | Yes (4-bit) | Better quality, slower |
| `codellama-7b` | ~4GB | Yes (4-bit) | Good for code |
| `qwen-coder-1.5b` | ~3GB | No | Alternative small model |

```bash
# Use a specific model
python scripts/query.py --backend local --model deepseek-coder-6.7b
```

### Claude API (Requires API Key)

For higher quality answers using Claude:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/query.py --backend claude
```

Get an API key at https://console.anthropic.com

### Context-Only Mode

Just retrieves and displays relevant code without LLM generation:

```bash
python scripts/query.py -q "your question"
```

## Interactive Commands

When running in interactive mode:

- Type your question and press Enter
- `@repo question` - filter by repository (e.g., `@datafusion how are plans executed?`)
- `stats` - show index statistics
- `quit` - exit

## Project Structure

```
learning/
├── src/
│   ├── __init__.py
│   ├── chunker.py      # Code parsing and chunking
│   ├── indexer.py      # Embedding and ChromaDB indexing
│   └── query.py        # RAG query interface with LLM backends
├── scripts/
│   ├── build_index.py  # Build/rebuild the vector index
│   └── query.py        # CLI query interface
├── chroma_db/          # Vector database (created after indexing)
├── datafusion/         # DataFusion source (clone separately)
├── datafusion-comet/   # Comet source (clone separately)
├── spark/              # Spark source (clone separately)
├── .venv/              # Python virtual environment
├── pyproject.toml      # Project configuration
└── README.md
```

## Requirements

- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM (for local models)
- ~15GB disk space (repos + index + model)

## Rebuilding the Index

If you update the source repositories:

```bash
# Pull latest changes
cd datafusion && git pull && cd ..
cd datafusion-comet && git pull && cd ..
cd spark && git pull && cd ..

# Rebuild index (only indexes new/changed files)
python scripts/build_index.py
```

## Troubleshooting

**CUDA out of memory**: Try a smaller model (`deepseek-coder-1.3b`) or ensure no other GPU processes are running.

**Slow first query**: The embedding model and LLM are loaded on first query. Subsequent queries are faster.

**Import errors**: Make sure the virtual environment is activated (`source .venv/bin/activate`)