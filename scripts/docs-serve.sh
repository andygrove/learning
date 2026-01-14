#!/bin/bash
# Serve the Spark reference documentation locally with live reload

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "MkDocs not found. Installing dependencies..."
    pip install -r docs-requirements.txt
fi

echo "Starting MkDocs development server..."
echo "Open http://127.0.0.1:8000 in your browser"
echo ""

mkdocs serve
