#!/usr/bin/env python3
"""
Generate Spark reference documentation from source code.

Uses Claude API to analyze source code and generate structured markdown documentation.
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import anthropic
except ImportError:
    print("Install anthropic: pip install anthropic")
    sys.exit(1)


SPARK_ROOT = Path(__file__).parent.parent / "spark"
EXPRESSIONS_DIR = SPARK_ROOT / "sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions"
OPERATORS_DIR = SPARK_ROOT / "sql/core/src/main/scala/org/apache/spark/sql/execution"
OUTPUT_DIR = Path(__file__).parent.parent / "sparkreference" / "docs"


@dataclass
class SourceFile:
    """A source file with its content."""
    path: Path
    name: str
    content: str
    category: str  # 'expression' or 'operator'


def find_expression_files() -> Iterator[SourceFile]:
    """Find all expression source files."""
    if not EXPRESSIONS_DIR.exists():
        print(f"Warning: Expressions directory not found: {EXPRESSIONS_DIR}")
        return

    # Main expression files
    for scala_file in EXPRESSIONS_DIR.glob("*.scala"):
        if scala_file.name.startswith("package"):
            continue
        try:
            content = scala_file.read_text(encoding='utf-8')
            yield SourceFile(
                path=scala_file,
                name=scala_file.stem,
                content=content,
                category='expression',
            )
        except Exception as e:
            print(f"Warning: Could not read {scala_file}: {e}")

    # Aggregate expressions
    agg_dir = EXPRESSIONS_DIR / "aggregate"
    if agg_dir.exists():
        for scala_file in agg_dir.glob("*.scala"):
            if scala_file.name.startswith("package") or scala_file.name == "interfaces.scala":
                continue
            try:
                content = scala_file.read_text(encoding='utf-8')
                yield SourceFile(
                    path=scala_file,
                    name=f"agg_{scala_file.stem}",
                    content=content,
                    category='expression',
                )
            except Exception as e:
                print(f"Warning: Could not read {scala_file}: {e}")


def find_operator_files() -> Iterator[SourceFile]:
    """Find all physical operator source files."""
    if not OPERATORS_DIR.exists():
        print(f"Warning: Operators directory not found: {OPERATORS_DIR}")
        return

    # Key operator files and directories
    key_files = [
        "basicPhysicalOperators.scala",
        "SortExec.scala",
        "GenerateExec.scala",
        "ExpandExec.scala",
        "WholeStageCodegenExec.scala",
        "limit.scala",
        "SparkPlan.scala",
    ]

    key_dirs = ["aggregate", "joins", "exchange", "window"]

    # Main operator files
    for filename in key_files:
        scala_file = OPERATORS_DIR / filename
        if scala_file.exists():
            try:
                content = scala_file.read_text(encoding='utf-8')
                yield SourceFile(
                    path=scala_file,
                    name=scala_file.stem,
                    content=content,
                    category='operator',
                )
            except Exception as e:
                print(f"Warning: Could not read {scala_file}: {e}")

    # Key subdirectories
    for dirname in key_dirs:
        subdir = OPERATORS_DIR / dirname
        if subdir.exists():
            for scala_file in subdir.glob("*.scala"):
                if scala_file.name.startswith("package"):
                    continue
                # Only include *Exec.scala files (actual operators)
                if "Exec" in scala_file.name or dirname in ["joins", "aggregate", "exchange"]:
                    try:
                        content = scala_file.read_text(encoding='utf-8')
                        yield SourceFile(
                            path=scala_file,
                            name=f"{dirname}_{scala_file.stem}",
                            content=content,
                            category='operator',
                        )
                    except Exception as e:
                        print(f"Warning: Could not read {scala_file}: {e}")


def extract_classes_from_file(source: SourceFile) -> list[str]:
    """Extract concrete class names from a Scala file that extend appropriate base types.

    Only returns concrete (non-abstract) classes that implement Expression or SparkPlan.
    """

    # Expression base types that indicate a class is an actual expression
    EXPRESSION_BASES = [
        'Expression', 'UnaryExpression', 'BinaryExpression', 'TernaryExpression',
        'QuaternaryExpression', 'LeafExpression', 'Unevaluable', 'Predicate',
        'BinaryOperator', 'UnaryMathExpression', 'BinaryMathExpression',
        'AggregateFunction', 'DeclarativeAggregate', 'ImperativeAggregate',
        'TypedImperativeAggregate', 'Nondeterministic', 'Generator',
        'ExplodeBase', 'CollectionGenerator', 'BinaryArithmetic',
        'RuntimeReplaceable', 'HigherOrderFunction', 'WindowFunction',
        'OffsetWindowFunction', 'SizeBasedWindowFunction', 'String2TrimExpression',
        'StringPredicate', 'StringRegexExpression', 'DatetimeExpression',
        'IntegralDivide', 'Round', 'UnaryLogExpression',
    ]

    # Operator base types (SparkPlan and its subclasses)
    OPERATOR_BASES = [
        'SparkPlan', 'UnaryExecNode', 'BinaryExecNode', 'LeafExecNode',
        'BaseAggregateExec', 'HashJoin', 'ShuffledJoin', 'BaseJoinExec',
        'Exchange', 'AQEShuffleReadExec', 'V2CommandExec',
    ]

    # Abstract base class patterns to exclude
    ABSTRACT_PATTERNS = [
        r'^Base\w+',  # BaseXxx
        r'^Abstract\w+',  # AbstractXxx
        r'\w+Base$',  # XxxBase
        r'\w+Helper$',  # XxxHelper
        r'\w+Utils?$',  # XxxUtil, XxxUtils
    ]

    if source.category == 'operator':
        bases = OPERATOR_BASES
        # Pattern: case class NameExec [private](...) extends Base
        # Must have 'Exec' suffix and not be abstract
        # Handles optional 'private' after class name
        pattern = r'(?:case\s+)?class\s+(\w+Exec)\s*(?:private)?\s*(?:\[[^\]]*\])?\s*\([^)]*\)\s*extends\s+(\w+)'
    else:
        bases = EXPRESSION_BASES
        # Pattern: case class Name [private](...) extends Base
        # Must NOT be abstract (no 'abstract' keyword before 'class')
        # Handles optional 'private' after class name
        pattern = r'(?<!abstract\s)(?:case\s+)?class\s+(\w+)\s*(?:private)?\s*(?:\[[^\]]*\])?\s*\([^)]*\)\s*extends\s+(\w+)'

    # Also check for abstract classes to exclude
    abstract_classes = set()
    abstract_pattern = r'abstract\s+class\s+(\w+)'
    for match in re.finditer(abstract_pattern, source.content):
        abstract_classes.add(match.group(1))

    matches = []
    for match in re.finditer(pattern, source.content, re.MULTILINE | re.DOTALL):
        class_name = match.group(1)
        base_class = match.group(2)

        # Skip if it's an abstract class
        if class_name in abstract_classes:
            continue

        # Skip if it matches abstract naming patterns
        if any(re.match(p, class_name) for p in ABSTRACT_PATTERNS):
            continue

        # Check if base class is in our list of valid bases
        if any(base in base_class for base in bases):
            matches.append(class_name)

    # Deduplicate while preserving order
    seen = set()
    result = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            result.append(m)

    return result


EXPRESSION_PROMPT = '''Analyze this Spark Catalyst expression source code and generate a reference documentation page in Markdown format.

Source file: {filename}

```scala
{content}
```

Generate a comprehensive reference page with EXACTLY these sections:

# {class_name}

## Overview
Brief description of what this expression does (2-3 sentences).

## Syntax
Show the SQL syntax or DataFrame API usage.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
(list all arguments/parameters)

## Return Type
What data type(s) this expression returns.

## Supported Data Types
List which input data types are supported (e.g., numeric, string, timestamp, etc.)

## Algorithm
Explain how the expression is evaluated internally (3-5 bullet points).

## Partitioning Behavior
How this expression affects partitioning (if applicable):
- Does it preserve partitioning?
- Does it require shuffle?

## Edge Cases
- Null handling behavior
- Empty input behavior
- Overflow/underflow behavior (if numeric)
- Any special cases

## Code Generation
Whether this expression supports code generation (Tungsten) or falls back to interpreted mode.

## Examples
```sql
-- Example SQL usage
```

```scala
// Example DataFrame API usage
```

## See Also
Related expressions or operators.

---
IMPORTANT FORMATTING RULES:
1. Always add a blank line BEFORE any bullet list
2. Always add a blank line AFTER any bullet list
3. Each bullet point must start with "- " on its own line
4. Never put multiple bullet items on the same line

Be specific and technical. Reference the actual source code behavior.'''


OPERATOR_PROMPT = '''Analyze this Spark physical operator source code and generate a reference documentation page in Markdown format.

Source file: {filename}

```scala
{content}
```

Generate a comprehensive reference page with EXACTLY these sections:

# {class_name}

## Overview
Brief description of what this operator does (2-3 sentences).

## When Used
Describe when the query planner chooses this operator (conditions/rules).

## Input Requirements
- Expected input partitioning
- Expected input ordering
- Number of children (unary/binary/leaf)

## Output Properties
- Output partitioning
- Output ordering
- How output schema is derived

## Algorithm
Explain how the operator executes internally (5-7 bullet points covering the key steps).

## Memory Usage
- Does it spill to disk?
- Memory requirements/configuration
- Buffering behavior

## Partitioning Behavior
- How it affects data distribution
- Shuffle requirements
- Partition count changes

## Supported Join/Aggregation Types
(if applicable - for joins: inner, left, right, full, semi, anti, cross)

## Metrics
Key SQL metrics this operator reports (e.g., rows output, time spent, spill size).

## Code Generation
Whether this operator supports whole-stage code generation.

## Configuration Options
Relevant Spark configuration parameters that affect this operator.

## Edge Cases
- Null handling
- Empty partition handling
- Skew handling (if applicable)

## Examples
Show an example query plan snippet containing this operator.

## See Also
Related operators.

---
IMPORTANT FORMATTING RULES:
1. Always add a blank line BEFORE any bullet list
2. Always add a blank line AFTER any bullet list
3. Each bullet point must start with "- " on its own line
4. Never put multiple bullet items on the same line

Be specific and technical. Reference the actual source code behavior.'''


def extract_class_code(content: str, class_name: str) -> str:
    """Extract the code for a specific class from file content."""
    lines = content.split('\n')
    result = []
    in_class = False
    brace_count = 0
    class_pattern = re.compile(
        rf'(?:case\s+)?class\s+{re.escape(class_name)}\s*(?:private)?\s*(?:\[[^\]]*\])?\s*\('
    )

    for i, line in enumerate(lines):
        if not in_class:
            if class_pattern.search(line):
                in_class = True
                # Include some context before the class (imports, comments)
                start = max(0, i - 5)
                result.extend(lines[start:i])

        if in_class:
            result.append(line)
            brace_count += line.count('{') - line.count('}')
            # Class ends when braces are balanced after opening
            if brace_count <= 0 and len(result) > 1 and '{' in ''.join(result):
                break

    # If we couldn't extract the class, return truncated full content
    if not result:
        return content[:15000] if len(content) > 15000 else content

    return '\n'.join(result)


def generate_reference_page(
    client: anthropic.Anthropic,
    source: SourceFile,
    class_name: str,
) -> str:
    """Generate a reference page for a single class using Claude."""

    # Extract just the relevant class code
    class_code = extract_class_code(source.content, class_name)

    # Also include imports and package info
    header_lines = []
    for line in source.content.split('\n')[:50]:
        if line.startswith('package ') or line.startswith('import '):
            header_lines.append(line)
        elif line.strip() and not line.startswith('//') and not line.startswith('/*'):
            break

    content = '\n'.join(header_lines) + '\n\n' + class_code

    if source.category == 'expression':
        prompt = EXPRESSION_PROMPT.format(
            filename=source.path.name,
            content=content,
            class_name=class_name,
        )
    else:
        prompt = OPERATOR_PROMPT.format(
            filename=source.path.name,
            content=content,
            class_name=class_name,
        )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def sanitize_filename(name: str) -> str:
    """Convert class name to valid filename."""
    # Convert CamelCase to snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    filename = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return filename


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate Spark reference documentation")
    parser.add_argument("--type", choices=["expressions", "operators", "both"], default="both",
                        help="Type of documentation to generate")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of files to process")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files without generating")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip files that already have documentation")
    args = parser.parse_args()

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not args.dry_run:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = None if args.dry_run else anthropic.Anthropic(api_key=api_key)

    # Collect source files
    sources = []
    if args.type in ["expressions", "both"]:
        sources.extend(find_expression_files())
    if args.type in ["operators", "both"]:
        sources.extend(find_operator_files())

    if args.limit:
        sources = sources[:args.limit]

    # Collect all classes to process
    all_classes = []
    for source in sources:
        classes = extract_classes_from_file(source)
        for class_name in classes:
            all_classes.append((source, class_name))

    print(f"Found {len(sources)} source files with {len(all_classes)} classes to process")

    if args.limit:
        all_classes = all_classes[:args.limit]

    if args.dry_run:
        for source, class_name in all_classes:
            print(f"  {source.category}: {class_name} (from {source.path.name})")
        return

    # Generate documentation - one page per class
    generated = 0
    skipped = 0
    errors = 0

    for source, class_name in all_classes:
        # Determine output path
        if source.category == 'expression':
            out_dir = OUTPUT_DIR / "expressions"
        else:
            out_dir = OUTPUT_DIR / "operators"

        out_file = out_dir / f"{sanitize_filename(class_name)}.md"

        if args.skip_existing and out_file.exists():
            print(f"Skipping (exists): {out_file.name}")
            skipped += 1
            continue

        print(f"Generating: {class_name} -> {out_file.name}")

        try:
            content = generate_reference_page(client, source, class_name)
            out_file.write_text(content, encoding='utf-8')
            generated += 1

            # Rate limiting
            time.sleep(1)

        except Exception as e:
            print(f"  Error: {e}")
            errors += 1

    print(f"\nDone! Generated: {generated}, Skipped: {skipped}, Errors: {errors}")


if __name__ == "__main__":
    main()
