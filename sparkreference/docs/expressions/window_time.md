# WindowTime

## Overview
WindowTime is a Spark Catalyst expression that extracts the timestamp from a window structure column created by windowing operations. This expression is used internally to access the time component of window aggregation results and is replaced during the analysis phase rather than being directly evaluated.

## Syntax
```sql
window_time(window_column)
```

```scala
// DataFrame API (internal usage through analyzer transformation)
window_time(col("window_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| windowColumn | StructType | A window structure column containing timestamp information from windowing operations |

## Return Type
Returns the same data type as the first field of the input struct (typically TimestampType).

## Supported Data Types

- Input: StructType (specifically window structures from windowing operations)

- Output: The data type of the first field in the window struct (usually TimestampType)

## Algorithm

- Accepts a window column (StructType) as input parameter

- Extracts the data type from the first field of the struct type

- Acts as a placeholder expression that gets replaced during query analysis

- Does not perform actual evaluation (marked as Unevaluable)

- Returns the timestamp component of the window structure

## Partitioning Behavior
How this expression affects partitioning:

- Does not directly affect partitioning as it's an unevaluable expression

- Partitioning behavior depends on the replacement expression created during analysis

- Typically preserves existing partitioning since it's extracting data from existing columns

## Edge Cases

- Null handling: Behavior depends on the analyzer replacement logic

- Invalid window structure: Will fail during analysis if input is not a proper window column

- Non-struct input: Enforced by inputTypes validation requiring StructType

- Resolution: Always returns false for resolved property, forcing analyzer transformation

## Code Generation
This expression does not support code generation as it implements the Unevaluable trait. The expression is replaced during the analysis phase with an evaluable expression that can participate in code generation.

## Examples
```sql
-- Example SQL usage (after windowing operation)
SELECT window_time(window), count(*) 
FROM (
  SELECT window(timestamp_col, '5 minutes') as window, *
  FROM events
  GROUP BY window(timestamp_col, '5 minutes')
)
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

val windowedDF = df
  .groupBy(window(col("timestamp"), "5 minutes"))
  .count()

// window_time would be applied internally by the analyzer
// when accessing window timestamp information
```

## See Also

- Window aggregation functions
- TimeWindow expression
- Windowing operations in Spark SQL
- StructType field extraction expressions