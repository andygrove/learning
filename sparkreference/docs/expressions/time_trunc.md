# TimeTrunc

## Overview
The `TimeTrunc` expression truncates time values to a specified unit of time precision. It rounds down time components (hours, minutes, seconds, microseconds) to the nearest specified unit boundary, effectively "flooring" the time value to remove precision below the specified granularity.

## Syntax
```sql
time_trunc(unit, time_expr)
```

```scala
// DataFrame API
col("time_column").expr("time_trunc('HOUR', time_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| unit | String | The time unit to truncate to (e.g., 'HOUR', 'MINUTE', 'SECOND') |
| time | Time type | The time expression to be truncated |

## Return Type
Returns the same data type as the input `time` expression. The return type is dynamically determined based on the input time data type.

## Supported Data Types

- **unit**: String type with collation support (must support trim collation)
- **time**: Any time-related data type (`AnyTimeType`) including TIME, TIMESTAMP, etc.

## Algorithm

- Parses the unit string parameter to determine the truncation granularity
- Extracts time components from the input time expression
- Sets all time components below the specified unit to their minimum values (e.g., 0 for seconds/minutes)
- Reconstructs the time value with the truncated precision
- Delegates actual implementation to `DateTimeUtils.timeTrunc` method via `StaticInvoke`

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffling as it operates on individual rows
- Maintains partition boundaries since it's a deterministic row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if either `unit` or `time` arguments are null
- **Invalid unit**: Throws runtime exception for unrecognized time unit strings
- **Boundary values**: Minimum time values remain unchanged when truncated
- **Case sensitivity**: Unit parameter handling depends on `DateTimeUtils.timeTrunc` implementation

## Code Generation
This expression uses runtime replacement with `StaticInvoke` rather than direct code generation. It falls back to calling the interpreted `DateTimeUtils.timeTrunc` method, which may limit Tungsten code generation optimization opportunities.

## Examples
```sql
-- Truncate to hour boundary
SELECT time_trunc('HOUR', TIME '14:32:05.123') AS truncated_time;
-- Result: 14:00:00.000

-- Truncate to minute boundary  
SELECT time_trunc('MINUTE', TIME '09:32:05.123') AS truncated_time;
-- Result: 09:32:00.000
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("time_trunc('HOUR', time_col)").as("hour_truncated"))
df.withColumn("minute_trunc", expr("time_trunc('MINUTE', timestamp_col)"))
```

## See Also

- `date_trunc` - For truncating date/timestamp values to date units
- `DateTimeUtils.timeTrunc` - The underlying implementation method
- Time and timestamp manipulation functions in the datetime_funcs group