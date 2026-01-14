# AnyValue

## Overview
`AnyValue` is an aggregate function that returns an arbitrary (non-deterministic) value from a group of rows. It is implemented as a runtime-replaceable aggregate that internally uses the `First` function to select the first encountered value, making it non-deterministic across different executions.

## Syntax
```sql
any_value(expr [, ignoreNulls])
```

```scala
// DataFrame API
df.agg(any_value($"column_name"))
df.agg(any_value($"column_name", lit(true))) // ignore nulls
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `child` | `Expression` | The expression or column from which to return an arbitrary value |
| `ignoreNulls` | `Boolean` | Optional flag to ignore null values when selecting a value (defaults to false) |

## Return Type
Returns the same data type as the input expression (`child`).

## Supported Data Types

- All data types are supported (`AnyDataType`)
- The `ignoreNulls` parameter must be of `BooleanType`

## Algorithm

- Uses the `First` aggregate function as its runtime replacement
- Selects the first encountered value from the group of rows
- If `ignoreNulls` is true, skips null values when searching for the first value
- If `ignoreNulls` is false, returns the first value even if it's null
- The result is non-deterministic across different query executions

## Partitioning Behavior
As an aggregate function, `AnyValue`:

- Does not preserve partitioning from input to output
- Requires data shuffle for grouping operations
- Results in a single row per group in the output

## Edge Cases

- **Null handling**: When `ignoreNulls` is false (default), null values are treated as valid return values
- **Empty groups**: Returns null for empty groups or when all values are null and `ignoreNulls` is true
- **Non-deterministic**: The same query may return different values across executions
- **Single value groups**: Always returns that single value regardless of `ignoreNulls` setting

## Code Generation
Since `AnyValue` is a `RuntimeReplaceableAggregate`, it delegates to the `First` function for execution. Code generation support depends on the underlying `First` implementation, which typically supports Tungsten code generation for optimal performance.

## Examples
```sql
-- Get any value from each group
SELECT department, any_value(salary) as sample_salary
FROM employees 
GROUP BY department;

-- Get any non-null value from each group
SELECT category, any_value(description, true) as sample_description
FROM products 
GROUP BY category;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic usage
df.groupBy("department").agg(any_value($"salary").as("sample_salary"))

// Ignoring nulls
df.groupBy("category").agg(any_value($"description", lit(true)).as("sample_description"))
```

## See Also

- `First` - Returns the first value in a group (deterministic within a sort order)
- `Last` - Returns the last value in a group  
- `CollectList` - Collects all values into an array
- `CollectSet` - Collects unique values into an array