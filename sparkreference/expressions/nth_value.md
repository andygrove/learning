# NthValue

## Overview
`NthValue` is an aggregate window function that returns the value of the input expression at the nth row within the window frame. It supports optional null handling where null values can be ignored when determining which row constitutes the nth position.

## Syntax
```sql
nth_value(input, offset) [IGNORE NULLS]
```

```scala
// DataFrame API usage would typically be through window functions
import org.apache.spark.sql.expressions.Window
df.select(nth_value(col("column"), lit(2)).over(Window.partitionBy("partition_col")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `input` | Any | The expression whose value should be returned from the nth row |
| `offset` | Integer | The 1-based position of the row to retrieve (must be > 0 and foldable) |
| `ignoreNulls` | Boolean | Optional flag to ignore null values when counting rows (default: false) |

## Return Type
Returns the same data type as the input expression. If no nth row exists or the nth row contains null, returns null.

## Supported Data Types
- **Input**: Any data type (`AnyDataType`)
- **Offset**: Integer types only (`IntegerType`)
- **Return**: Same as input data type

## Algorithm
- Maintains an internal counter starting at 1 for each window partition
- When `ignoreNulls` is false: increments counter for every row and captures input value when counter equals offset
- When `ignoreNulls` is true: only increments counter for non-null input values and captures value when counter equals offset for non-null input
- Uses an aggregation buffer with two attributes: result value and current count
- Evaluates to the captured result value or null if nth position never reached

## Partitioning Behavior
- Preserves input partitioning as this is a window function that operates within partitions
- Does not require shuffle if proper partitioning already exists
- Works with `UnspecifiedFrame` - operates on the entire window partition by default

## Edge Cases
- **Null handling**: When `ignoreNulls` is true, null values don't count toward the offset position
- **Invalid offset**: Offset must be a positive integer (> 0), compile-time validated
- **Non-foldable offset**: Offset expression must be evaluable at compile time (constant)
- **Insufficient rows**: Returns null if there aren't enough (non-null) rows to reach the nth position
- **Empty partitions**: Returns null for partitions with no rows

## Code Generation
This expression extends `AggregateWindowFunction` which supports Tungsten code generation through the Catalyst framework. The update expressions and evaluation logic are code-generated for optimal performance.

## Examples
```sql
-- Get the 2nd highest salary per department
SELECT employee_name, salary,
       nth_value(salary, 2) OVER (
         PARTITION BY department 
         ORDER BY salary DESC
       ) as second_highest
FROM employees;

-- Get 3rd non-null value, ignoring nulls
SELECT nth_value(commission, 3) IGNORE NULLS OVER (
  PARTITION BY region 
  ORDER BY hire_date
) as third_commission
FROM sales_reps;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val windowSpec = Window.partitionBy("department").orderBy(desc("salary"))
df.select(
  col("employee_name"),
  col("salary"),
  nth_value(col("salary"), lit(2)).over(windowSpec).alias("second_highest")
)
```

## See Also
- `FirstValue` - Gets the first value in a window frame
- `LastValue` - Gets the last value in a window frame  
- `Lag` / `Lead` - Access values at relative offsets from current row
- `RowNumber` - Assigns sequential numbers within window partitions