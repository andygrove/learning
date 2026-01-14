# TimeDiff

## Overview
The `TimeDiff` expression calculates the difference between two time-based values (timestamps, dates, or time intervals) in a specified unit. It is a ternary expression that takes a unit string and two temporal expressions, returning the numeric difference as a long integer.

## Syntax
```sql
TIME_DIFF(unit, start_time, end_time)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("time_diff('SECOND', start_col, end_col)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| unit | StringType | The unit of time difference to calculate (e.g., 'SECOND', 'MINUTE', 'HOUR', 'DAY') |
| start | AnyTimeType | The starting timestamp, date, or time value |
| end | AnyTimeType | The ending timestamp, date, or time value |

## Return Type
`LongType` - Returns a long integer representing the time difference in the specified unit.

## Supported Data Types

- **unit**: String type with collation support (trim collation supported)
- **start**: Any time-related type (TimestampType, DateType, etc.)
- **end**: Any time-related type (TimestampType, DateType, etc.)

## Algorithm

- Validates the unit string parameter to ensure it represents a valid time unit
- Converts both start and end temporal values to a common internal representation
- Calculates the absolute difference between the two temporal values
- Converts the difference to the requested unit (seconds, minutes, hours, etc.)
- Returns the result as a long integer, potentially negative if start > end

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partitioning scheme since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if any of the three arguments (unit, start, end) is null
- **Invalid unit**: Throws runtime exception for unrecognized time unit strings
- **Type mismatch**: Implicit casting is applied to make start and end compatible time types
- **Overflow**: May overflow for extremely large time differences that exceed Long.MAX_VALUE
- **Timezone handling**: Results depend on session timezone settings for timestamp calculations

## Code Generation
This expression uses `RuntimeReplaceable` interface and delegates to `DateTimeUtils.timeDiff` method via `StaticInvoke`. It supports Tungsten code generation through the static method invocation, providing optimized performance in generated code paths.

## Examples
```sql
-- Calculate difference in seconds
SELECT TIME_DIFF('SECOND', '2023-01-01 10:00:00', '2023-01-01 10:05:30') AS diff_seconds;
-- Returns: 330

-- Calculate difference in days
SELECT TIME_DIFF('DAY', '2023-01-01', '2023-01-15') AS diff_days;
-- Returns: 14
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.sql("SELECT '2023-01-01 10:00:00' as start_time, '2023-01-01 12:00:00' as end_time")
df.select(expr("time_diff('HOUR', start_time, end_time)").alias("hour_diff")).show()

// Using with column references
df.withColumn("minute_diff", expr("time_diff('MINUTE', start_time, end_time)"))
```

## See Also

- `DateDiff` - For date-only differences
- `DateAdd` - For adding time intervals
- `DateSub` - For subtracting time intervals
- `Extract` - For extracting specific time components