# Last

## Overview

The `Last` aggregate function returns the last value in a group of rows, optionally ignoring null values. The function is non-deterministic because its results depend on the order of the rows, which may be non-deterministic after a shuffle.

## Syntax

```sql
LAST(expression [, ignoreNulls])
```

```scala
// DataFrame API
df.agg(last("column_name"))
df.agg(last("column_name", ignoreNulls = true))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `child` | `Expression` | The expression to evaluate for each row |
| `ignoreNulls` | `Boolean` | Whether to ignore null values (default: false) |

## Return Type

Returns the same data type as the input expression. The result is always nullable (`nullable = true`).

## Supported Data Types

Supports any data type (`AnyDataType`) for the main expression:

- Numeric types (integers, decimals, floating-point)
- String types
- Date and timestamp types
- Boolean types
- Complex types (arrays, maps, structs)
- Binary types

## Algorithm

The `Last` aggregate function maintains two buffer attributes during evaluation:

- Initializes buffer with null value for `last` and false for `valueSet`
- For each row, updates the `last` value with the current expression value
- If `ignoreNulls` is true, only updates when the current value is not null
- If `ignoreNulls` is false, updates with every value including nulls
- During merge operations, prefers the right-hand side buffer if it has been set

## Partitioning Behavior

This expression affects partitioning behavior:

- Does not preserve partitioning as it's an aggregate function
- May require shuffle operations to collect all values in each group
- Results are non-deterministic across different shuffle operations
- Order dependency makes it sensitive to partition boundaries

## Edge Cases

Null handling behavior varies based on the `ignoreNulls` parameter:

- When `ignoreNulls = false`: Returns the last value encountered, even if null
- When `ignoreNulls = true`: Skips null values and returns the last non-null value
- Empty input groups return null
- If all values are null and `ignoreNulls = true`, returns null
- The `valueSet` flag tracks whether any valid value has been encountered

## Code Generation

This expression extends `DeclarativeAggregate`, which supports Catalyst's code generation framework (Tungsten). The aggregate operations are expressed declaratively through `updateExpressions`, `mergeExpressions`, and `evaluateExpression`, allowing for efficient code generation.

## Examples

```sql
-- Get the last salary in each department
SELECT department, LAST(salary) as last_salary
FROM employees 
GROUP BY department;

-- Get the last non-null salary in each department
SELECT department, LAST(salary, true) as last_non_null_salary
FROM employees 
GROUP BY department;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions.last

// Get last value (including nulls)
df.groupBy("department").agg(last("salary"))

// Get last non-null value
df.groupBy("department").agg(last("salary", ignoreNulls = true))

// With column expressions
df.groupBy("department").agg(last(col("salary") * 1.1))
```

## See Also

- `First` - Returns the first value in a group
- `LastValue` window function - Similar functionality in window operations
- `CollectList` - Collects all values into an array
- Other aggregate functions like `Max`, `Min`