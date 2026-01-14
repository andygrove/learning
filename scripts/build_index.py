#!/usr/bin/env python3
"""Build the code index for all repositories."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.indexer import build_index

if __name__ == "__main__":
    build_index(
        repos_dir=str(Path(__file__).parent.parent),
        persist_dir=str(Path(__file__).parent.parent / "chroma_db"),
    )
