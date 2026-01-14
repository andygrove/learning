#!/usr/bin/env python3
"""Query the code index interactively."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.query import create_rag

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query the code index")
    parser.add_argument(
        "--backend",
        choices=["context", "claude", "local"],
        default="context",
        help="LLM backend to use (default: context-only)",
    )
    parser.add_argument("--model", help="Model name for claude/local backends")
    parser.add_argument("--query", "-q", help="Single query (otherwise interactive mode)")
    parser.add_argument("--repo", "-r", help="Filter by repository name")
    args = parser.parse_args()

    persist_dir = str(Path(__file__).parent.parent / "chroma_db")
    rag = create_rag(backend_type=args.backend, model_name=args.model, persist_dir=persist_dir)

    if args.query:
        print(rag.query(args.query, repo_filter=args.repo))
    else:
        rag.interactive()
