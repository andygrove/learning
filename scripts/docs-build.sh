#!/bin/bash
# Build the Spark reference documentation as a static site

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "MkDocs not found. Installing dependencies..."
    pip install -r docs-requirements.txt
fi

# Default output directory
OUTPUT_DIR="${1:-site}"

echo "Building documentation..."
mkdocs build --site-dir "$OUTPUT_DIR"

echo ""
echo "Documentation built successfully!"
echo "Output: $PROJECT_ROOT/$OUTPUT_DIR"
echo ""
echo "To preview locally, run: python -m http.server -d $OUTPUT_DIR"
