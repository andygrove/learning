# Spark Expression Reference Documentation Prompt

Use this prompt with Claude Code to generate Spark expression reference documentation for the `sparkreference/docs/expressions/` directory.

## Usage

```
Generate Spark reference documentation for the <expression_name> expression.

Use the RAG system to research:
- Spark source code implementation
- Edge cases and null handling
- Supported data types
- Examples from Spark tests
```

## Workflow

### 1. Research Using RAG System

Query the local RAG system to gather information about the expression:

```bash
# Query Spark codebase for the expression implementation
python scripts/query.py --backend local -r spark -q "How does Spark implement <expression_name>?"

# Find edge cases and null handling
python scripts/query.py --backend local -r spark -q "<expression_name> null handling edge cases"

# Find test cases for examples
python scripts/query.py --backend local -r spark -q "<expression_name> test cases examples"

# Check for related expressions
python scripts/query.py --backend local -r spark -q "expressions similar to <expression_name>"
```

### 2. Supplement with Spark Documentation

If RAG results are insufficient, check:
- Spark SQL function documentation: https://spark.apache.org/docs/latest/api/sql/
- Spark source code on GitHub for the expression class

### 3. Generate Documentation

Create the markdown file following the standard template below.

## Documentation Template

```markdown
# <ExpressionClassName>

## Overview
Brief description of what the expression does and its primary use cases.

## Syntax
```sql
-- SQL syntax
function_name(arg1 [, arg2] [, options])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.function_name
df.select(function_name($"column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| arg1 | Type | Description |
| arg2 | Type (optional) | Description |

## Return Type
Description of the return type.

## Supported Data Types
- List of supported input data types
- Any type restrictions or coercion rules

## Algorithm
- High-level description of how the expression works
- Key implementation details relevant to users
- Performance characteristics if notable

## Partitioning Behavior
How this expression affects partitioning:
- Whether it preserves partitioning
- Whether it requires shuffle
- Any distributed execution considerations

## Edge Cases
- Null handling behavior
- Empty input handling
- Overflow/underflow behavior (for numeric)
- Invalid input handling
- Special values (NaN, Infinity for floats)
- Timezone considerations (for datetime)

## Examples
```sql
-- SQL examples with expected output
SELECT function_name(value) FROM table;
-- Result: expected_output
```

```scala
// DataFrame API examples
df.select(function_name($"column"))
```

## See Also
- Related expression 1
- Related expression 2
```

## Quality Checklist

Before saving the documentation:

- [ ] All sections from template are included
- [ ] Edge cases are thoroughly documented (especially null handling)
- [ ] Examples show both SQL and DataFrame API usage
- [ ] Return type is clearly specified
- [ ] Supported data types are listed
- [ ] Related expressions are linked in "See Also"
- [ ] No placeholder text remains

## File Naming Convention

- Use snake_case for file names
- Match the Spark expression class name (e.g., `JsonToStructs` -> `json_to_structs.md`)
- Place in `sparkreference/docs/expressions/`

## Example RAG Queries for Common Expression Types

### JSON Expressions
```bash
python scripts/query.py --backend local -r spark -q "JsonToStructs from_json implementation"
python scripts/query.py --backend local -r spark -q "JSON parsing options schema inference Spark"
```

### Date/Time Expressions
```bash
python scripts/query.py --backend local -r spark -q "DateAdd expression timezone handling"
python scripts/query.py --backend local -r spark -q "timestamp formatting patterns Spark"
```

### String Expressions
```bash
python scripts/query.py --backend local -r spark -q "StringTrim expression null handling"
python scripts/query.py --backend local -r spark -q "string collation Spark expressions"
```

### Aggregate Expressions
```bash
python scripts/query.py --backend local -r spark -q "Sum aggregate expression overflow handling"
python scripts/query.py --backend local -r spark -q "aggregate function partial aggregation"
```

## Notes

- Focus on behavior that matters for Comet compatibility
- Document any ANSI mode vs legacy mode differences
- Include Spark version notes if behavior changed between versions
- Cross-reference with existing Comet implementations when available
