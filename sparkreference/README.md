# Spark Internals Reference Guide

A comprehensive reference guide to Apache Spark SQL internals, covering expressions and physical operators.

## Structure

- **[expressions/](expressions/)** - Catalyst expression reference (functions, operators, literals)
- **[operators/](operators/)** - Physical execution operator reference (joins, aggregates, exchanges)

## Generated Pages

### Expressions

| Expression | Description |
|------------|-------------|
| [BaseGroupingSets](expressions/base_grouping_sets.md) | CUBE, ROLLUP, GROUPING SETS |
| [ToNumberBase](expressions/to_number_base.md) | Number parsing expressions |
| [NumericEvalContext](expressions/numeric_eval_context.md) | Numeric evaluation context |
| [DirectShufflePartitionID](expressions/direct_shuffle_partition_id.md) | Shuffle partition identification |
| [EvalMode](expressions/eval_mode.md) | Expression evaluation modes |

### Operators

| Operator | Description |
|----------|-------------|
| [ProjectExec](operators/project_exec.md) | Column projection |
| [SortExec](operators/sort_exec.md) | Sorting operator |
| [GenerateExec](operators/generate_exec.md) | Generator/explode operations |
| [ExpandExec](operators/expand_exec.md) | GROUPING SETS expansion |
| [WholeStageCodegenExec](operators/whole_stage_codegen_exec.md) | Code generation wrapper |

## Page Structure

Each reference page includes:

### For Expressions
- Overview
- Syntax (SQL and DataFrame API)
- Arguments
- Return Type
- Supported Data Types
- Algorithm
- Partitioning Behavior
- Edge Cases
- Code Generation Support
- Examples
- See Also

### For Operators
- Overview
- When Used (planner rules)
- Input Requirements
- Output Properties
- Algorithm
- Memory Usage
- Partitioning Behavior
- Metrics
- Code Generation Support
- Configuration Options
- Edge Cases
- Examples
- See Also

## Generating More Pages

To generate additional reference pages:

```bash
# Set API key
export ANTHROPIC_API_KEY=your_key

# Generate all expressions
python scripts/generate_spark_reference.py --type expressions

# Generate all operators
python scripts/generate_spark_reference.py --type operators

# Generate both (with limit)
python scripts/generate_spark_reference.py --limit 50

# Dry run to see what would be generated
python scripts/generate_spark_reference.py --dry-run
```

The generator:
- Reads Spark source code
- Uses Claude to analyze and document each class
- Outputs structured markdown files
- Skips existing files (use `--skip-existing=false` to regenerate)

## Source Locations

- **Expressions**: `spark/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/`
- **Operators**: `spark/sql/core/src/main/scala/org/apache/spark/sql/execution/`
