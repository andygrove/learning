# First

## Overview
The `First` expression is an aggregate function that returns the first value in a group of rows. It is non-deterministic because its results depend on the order of rows, which may be non-deterministic after a shuffle operation.

## Syntax
```sql
FIRST(expression [, ignoreNulls])
```

```scala
first(col("column_name"))
first(col("column_name"), ignoreNulls = true)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression whose first value should be returned |
| ignoreNulls | Boolean | Whether to ignore null values when finding the first value (default: false) |

## Return Type
Returns the same data type as the input expression (`child.dataType`). The result is always nullable.

## Supported Data Types
Supports all data types (`AnyDataType`) for the main expression input. The `ignoreNulls` parameter must be of `BooleanType`.

## Algorithm
The expression maintains an internal buffer with two components:

- Tracks the first encountered value in a `first` attribute
- Maintains a `valueSet` boolean flag to indicate whether a value has been captured
- In update phase: captures the first non-null value (if `ignoreNulls=true`) or simply the first value
- In merge phase: prioritizes the left buffer's value if it has been set, otherwise uses the right buffer's value
- Returns the stored first value as the final result

## Partitioning Behavior
This expression does not preserve partitioning and may require shuffling for global aggregation:

- Results depend on row order within partitions
- Cross-partition merging uses the merge expressions to combine partial results
- Non-deterministic behavior after shuffle operations

## Edge Cases

- **Null handling**: When `ignoreNulls=false`, null values are treated as valid first values
- **Null handling with ignoreNulls=true**: Only non-null values are considered for the first position
- **Empty input**: Returns null when no qualifying values are found
- **All nulls with ignoreNulls=true**: Returns null if all input values are null
- **Buffer initialization**: Starts with null value and `valueSet=false`

## Code Generation
This is a `DeclarativeAggregate`, which means it supports Catalyst's expression-based code generation through the defined `updateExpressions`, `mergeExpressions`, and `evaluateExpression`.

## Examples
```sql
-- Get first salary in each department
SELECT department, FIRST(salary) as first_salary
FROM employees 
GROUP BY department;

-- Get first non-null hire_date
SELECT department, FIRST(hire_date, true) as first_hire_date
FROM employees 
GROUP BY department;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.groupBy("department")
  .agg(first("salary").as("first_salary"))

// With ignore nulls
df.groupBy("department")
  .agg(first("hire_date", ignoreNulls = true).as("first_hire_date"))
```

## See Also
- `Last` - Returns the last value in a group
- `FirstValue` - Window function equivalent for first value
- Aggregate functions in the `agg_funcs` group