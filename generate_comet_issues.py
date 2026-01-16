#!/usr/bin/env python3
"""
Generate GitHub issues for unsupported Spark expressions in Comet.

This script reads Spark reference documentation and generates GitHub issues
formatted according to the datafusion-comet feature request template.

Usage:
    python generate_comet_issues.py --expression levenshtein
    python generate_comet_issues.py --all --dry-run
    python generate_comet_issues.py --all --create-issues
"""

import argparse
import os
import re
import subprocess
import json
from pathlib import Path
from typing import Optional

# Paths
SPARK_REF_DOCS = Path("sparkreference/docs/expressions")
COMET_REPO = Path("datafusion-comet")

# Sections to exclude from the issue (not relevant to Comet implementation)
EXCLUDED_SECTIONS = [
    "Code Generation",
    "Partitioning Behavior",  # Usually not relevant
]

# Expressions already implemented in Comet (from QueryPlanSerde.scala analysis)
IMPLEMENTED_EXPRESSIONS = {
    # Math
    "abs", "acos", "add", "asin", "atan", "atan2", "ceil", "cos", "cosh",
    "cot", "divide", "exp", "expm1", "floor", "hex", "integral_divide",
    "is_nan", "log", "log2", "log10", "multiply", "pow", "rand", "randn",
    "remainder", "round", "signum", "sin", "sinh", "sqrt", "subtract",
    "tan", "tanh", "unary_minus", "unhex",
    # String
    "ascii", "bit_length", "btrim", "char", "chr", "concat", "concat_ws",
    "contains", "ends_with", "initcap", "instr", "length", "like", "lower",
    "lpad", "ltrim", "octet_length", "regexp_replace", "repeat", "replace",
    "reverse", "rlike", "rpad", "rtrim", "space", "starts_with", "substring",
    "translate", "trim", "upper",
    # Array
    "array", "array_append", "array_compact", "array_contains", "array_distinct",
    "array_except", "array_filter", "array_insert", "array_intersect",
    "array_join", "array_max", "array_min", "array_remove", "array_repeat",
    "array_union", "arrays_overlap", "element_at", "flatten", "get_array_item",
    "size",
    # DateTime
    "date_add", "date_sub", "day_of_month", "day_of_week", "day_of_year",
    "from_unixtime", "hour", "minute", "month", "quarter", "second",
    "trunc_date", "trunc_timestamp", "week_day", "week_of_year", "year",
    # Hash
    "md5", "murmur3_hash", "sha1", "sha2", "xxhash64",
    # Predicate
    "and", "equal_to", "equal_null_safe", "greater_than", "greater_than_or_equal",
    "in", "in_set", "is_not_null", "is_null", "less_than", "less_than_or_equal",
    "not", "or",
    # Bitwise
    "bitwise_and", "bitwise_count", "bitwise_get", "bitwise_not", "bitwise_or",
    "bitwise_xor", "shift_left", "shift_right",
    # Conditional
    "case_when", "coalesce", "if",
    # Map
    "get_map_value", "map_entries", "map_from_arrays", "map_keys", "map_values",
    # Struct
    "create_named_struct", "get_array_struct_fields", "get_struct_field",
    "json_to_structs", "structs_to_json",
    # Aggregate
    "avg", "bit_and_agg", "bit_or_agg", "bit_xor_agg", "bloom_filter_aggregate",
    "corr", "count", "cov_population", "cov_sample", "first", "last", "max",
    "min", "stddev_pop", "stddev_samp", "sum", "variance_pop", "variance_samp",
    # Misc
    "alias", "attribute_reference", "bloom_filter_might_contain", "cast",
    "check_overflow", "known_floating_point_normalized", "literal",
    "make_decimal", "monotonically_increasing_id", "scalar_subquery",
    "spark_partition_id", "sort_order", "static_invoke", "unscaled_value",
}

# Difficulty classification
DIFFICULTY = {
    "small": [
        "acosh", "asinh", "atanh", "cbrt", "degrees", "radians", "e", "pi",
        "log1p", "rint", "hypot", "csc", "sec", "base64", "unbase64", "left",
        "right", "locate", "position", "soundex", "split", "split_part",
        "bit_count", "crc32", "hash", "nanvl", "typeof", "version", "uuid",
    ],
    "medium": [
        "bin", "conv", "bround", "pmod", "div", "factorial", "greatest", "least",
        "width_bucket", "decode", "encode", "elt", "find_in_set", "format_number",
        "format_string", "levenshtein", "mask", "overlay", "sentences",
        "substring_index", "to_char", "to_number", "to_binary", "regexp_count",
        "regexp_extract", "regexp_extract_all", "regexp_instr", "regexp_substr",
        "array_position", "arrays_zip", "sequence", "shuffle", "slice", "sort_array",
        "array_size", "cardinality", "add_months", "date_diff", "date_format",
        "date_from_unix_date", "last_day", "next_day", "months_between", "to_date",
        "to_timestamp", "unix_timestamp", "unix_date", "unix_seconds", "unix_millis",
        "unix_micros", "timestamp_seconds", "timestamp_millis", "timestamp_micros",
        "current_timestamp", "now", "map", "map_concat", "map_contains_key",
        "map_from_entries", "str_to_map", "try_element_at", "approx_count_distinct",
        "collect_list", "collect_set", "histogram_numeric", "kurtosis", "skewness",
        "max_by", "min_by", "mode", "median", "percentile", "try_avg", "try_sum",
        "array_agg", "named_struct", "struct", "input_file_name", "assert_true",
        "raise_error",
    ],
    "large": [
        "row_number", "rank", "dense_rank", "percent_rank", "cume_dist", "ntile",
        "lag", "lead", "nth_value", "explode", "explode_outer", "posexplode",
        "posexplode_outer", "inline", "inline_outer", "stack", "aggregate",
        "reduce", "array_sort", "exists", "filter", "forall", "transform",
        "transform_keys", "transform_values", "map_filter", "map_zip_with",
        "zip_with", "from_json", "to_json", "get_json_object", "json_array_length",
        "json_object_keys", "json_tuple", "schema_of_json", "from_csv", "to_csv",
        "schema_of_csv", "xpath", "xpath_boolean", "xpath_double", "xpath_float",
        "xpath_int", "xpath_long", "xpath_short", "xpath_string", "parse_url",
        "url_encode", "url_decode", "convert_timezone", "from_utc_timestamp",
        "to_utc_timestamp", "make_dt_interval", "make_ym_interval", "make_interval",
        "make_date", "make_timestamp", "grouping", "grouping_id", "count_min_sketch",
        "regr_intercept", "regr_r2", "regr_slope", "regr_sxx", "regr_sxy", "regr_syy",
        "aes_encrypt", "aes_decrypt",
    ],
}


def normalize_name(name: str) -> str:
    """Convert expression name to normalized form for comparison."""
    return name.lower().replace("-", "_").replace(" ", "_")


def is_implemented(expr_name: str) -> bool:
    """Check if expression is already implemented in Comet."""
    normalized = normalize_name(expr_name)
    return normalized in IMPLEMENTED_EXPRESSIONS


def get_difficulty(expr_name: str) -> str:
    """Get difficulty classification for an expression."""
    normalized = normalize_name(expr_name)
    for level, exprs in DIFFICULTY.items():
        if normalized in exprs:
            return level
    return "medium"  # Default to medium


def parse_spark_doc(doc_path: Path) -> dict:
    """Parse a Spark reference documentation file."""
    if not doc_path.exists():
        return None

    content = doc_path.read_text()

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else doc_path.stem

    # Split into sections
    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        section_match = re.match(r'^##\s+(.+)$', line)
        if section_match:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = section_match.group(1)
            current_content = []
        elif current_section:
            current_content.append(line)

    # Don't forget the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    # Filter out excluded sections
    for excluded in EXCLUDED_SECTIONS:
        sections.pop(excluded, None)

    return {
        'title': title,
        'sections': sections,
        'raw_content': content,
    }


def generate_issue_body(expr_name: str, doc: dict) -> str:
    """Generate GitHub issue body from parsed documentation."""
    sections = doc['sections']
    title = doc['title']
    difficulty = get_difficulty(expr_name)

    # Build the "What is the problem" section
    overview = sections.get('Overview', f'The {title} expression is not yet supported in Comet.')
    problem = f"""> **Note:** This issue was generated with AI assistance. The specification details have been extracted from Spark documentation and may need verification.

Comet does not currently support the Spark `{expr_name}` function, causing queries using this function to fall back to Spark's JVM execution instead of running natively on DataFusion.

{overview}

Supporting this expression would allow more Spark workloads to benefit from Comet's native acceleration."""

    # Build the "Describe the potential solution" section
    solution_parts = ["### Spark Specification\n"]

    if 'Syntax' in sections:
        solution_parts.append(f"**Syntax:**\n{sections['Syntax']}\n")

    if 'Arguments' in sections:
        solution_parts.append(f"**Arguments:**\n{sections['Arguments']}\n")

    if 'Return Type' in sections:
        solution_parts.append(f"**Return Type:** {sections['Return Type']}\n")

    if 'Supported Data Types' in sections:
        solution_parts.append(f"**Supported Data Types:**\n{sections['Supported Data Types']}\n")

    if 'Edge Cases' in sections:
        solution_parts.append(f"**Edge Cases:**\n{sections['Edge Cases']}\n")

    if 'Examples' in sections:
        solution_parts.append(f"**Examples:**\n{sections['Examples']}\n")

    # Implementation approach
    solution_parts.append("""### Implementation Approach

See the [Comet guide on adding new expressions](https://datafusion.apache.org/comet/contributor-guide/adding_a_new_expression.html) for detailed instructions.

1. **Scala Serde**: Add expression handler in `spark/src/main/scala/org/apache/comet/serde/`
2. **Register**: Add to appropriate map in `QueryPlanSerde.scala`
3. **Protobuf**: Add message type in `native/proto/src/proto/expr.proto` if needed
4. **Rust**: Implement in `native/spark-expr/src/` (check if DataFusion has built-in support first)
""")

    solution = '\n'.join(solution_parts)

    # Build additional context
    context_parts = [
        f"**Difficulty:** {difficulty.capitalize()}",
        f"**Spark Expression Class:** `org.apache.spark.sql.catalyst.expressions.{title.replace(' ', '')}`",
    ]

    if 'See Also' in sections:
        context_parts.append(f"\n**Related:**\n{sections['See Also']}")

    context_parts.append("\n---\n*This issue was auto-generated from Spark reference documentation.*")

    context = '\n'.join(context_parts)

    return {
        'title': f"[Feature] Support Spark expression: {expr_name}",
        'problem': problem,
        'solution': solution,
        'context': context,
        'labels': ['enhancement'],
    }


def create_github_issue(issue_data: dict, dry_run: bool = True) -> Optional[str]:
    """Create a GitHub issue using the gh CLI."""
    if dry_run:
        print(f"\n{'='*60}")
        print(f"TITLE: {issue_data['title']}")
        print(f"LABELS: {', '.join(issue_data['labels'])}")
        print(f"{'='*60}")
        print("\n## What is the problem the feature request solves?\n")
        print(issue_data['problem'])
        print("\n## Describe the potential solution\n")
        print(issue_data['solution'])
        print("\n## Additional context\n")
        print(issue_data['context'])
        return None

    # Format body for gh CLI
    body = f"""## What is the problem the feature request solves?

{issue_data['problem']}

## Describe the potential solution

{issue_data['solution']}

## Additional context

{issue_data['context']}
"""

    cmd = [
        'gh', 'issue', 'create',
        '--repo', 'apache/datafusion-comet',
        '--title', issue_data['title'],
        '--body', body,
        '--label', ','.join(issue_data['labels']),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print(f"Error creating issue: {result.stderr}")
        return None


def find_doc_file(expr_name: str) -> Optional[Path]:
    """Find the documentation file for an expression."""
    # Try various naming conventions
    candidates = [
        SPARK_REF_DOCS / f"{expr_name}.md",
        SPARK_REF_DOCS / f"{expr_name.replace('_', '-')}.md",
        SPARK_REF_DOCS / f"{expr_name.lower()}.md",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Search for partial matches
    for doc_file in SPARK_REF_DOCS.glob("*.md"):
        if normalize_name(doc_file.stem) == normalize_name(expr_name):
            return doc_file

    return None


def main():
    parser = argparse.ArgumentParser(description='Generate GitHub issues for Comet expressions')
    parser.add_argument('--expression', '-e', help='Single expression to process')
    parser.add_argument('--all', action='store_true', help='Process all unsupported expressions')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Print issue without creating')
    parser.add_argument('--create-issues', action='store_true', help='Actually create GitHub issues')
    parser.add_argument('--list-available', action='store_true', help='List available expression docs')

    args = parser.parse_args()

    if args.create_issues:
        args.dry_run = False

    if args.list_available:
        print("Available expression documentation files:")
        for doc_file in sorted(SPARK_REF_DOCS.glob("*.md")):
            if doc_file.name != "index.md":
                status = "✓" if not is_implemented(doc_file.stem) else "✗ (implemented)"
                print(f"  {doc_file.stem}: {status}")
        return

    if args.expression:
        expressions = [args.expression]
    elif args.all:
        # Get all unimplemented expressions that have docs
        expressions = []
        for doc_file in SPARK_REF_DOCS.glob("*.md"):
            if doc_file.name != "index.md" and not is_implemented(doc_file.stem):
                expressions.append(doc_file.stem)
    else:
        parser.print_help()
        return

    for expr_name in expressions:
        doc_path = find_doc_file(expr_name)
        if not doc_path:
            print(f"Warning: No documentation found for '{expr_name}'")
            continue

        if is_implemented(expr_name):
            print(f"Skipping '{expr_name}' - already implemented in Comet")
            continue

        doc = parse_spark_doc(doc_path)
        if not doc:
            print(f"Warning: Could not parse documentation for '{expr_name}'")
            continue

        issue_data = generate_issue_body(expr_name, doc)
        result = create_github_issue(issue_data, dry_run=args.dry_run)

        if result:
            print(f"Created issue: {result}")


if __name__ == '__main__':
    main()
