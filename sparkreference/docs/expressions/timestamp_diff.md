# TimestampDiff

## Overview
TimestampDiff calculates the difference between two timestamp values in a specified unit of time. It returns a Long value representing the number of complete time units between the start and end timestamps, taking timezone information into account for proper temporal calculations.

## Syntax
```sql
TIMESTAMPDIFF(unit, start_timestamp, end_timestamp)
```

```scala
// DataFrame API usage
timestampdiff(lit("SECOND"), col("start_time"), col("end_time"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| unit | String | Time unit for the difference calculation (e.g., "SECOND", "MINUTE", "HOUR", "DAY") |
| startTimestamp | Expression | Starting timestamp value |
| endTimestamp | Expression | Ending timestamp value |
| timeZoneId | Option[String] | Optional timezone identifier for timezone-aware calculations |

## Return Type
Long - representing the number of complete time units between the timestamps.

## Supported Data Types

- Input types: TimestampType for both start and end timestamp arguments
- The unit parameter must be a valid time unit string
- Supports timezone-aware timestamp calculations

## Algorithm

- Converts both input timestamps to microseconds since epoch
- Applies timezone conversion using the specified or default timezone
- Calculates the difference in microseconds between end and start timestamps
- Converts the microsecond difference to the requested time unit
- Returns the result as a Long value representing complete time units

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates row-by-row without requiring data movement
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Null handling: Returns null if either start or end timestamp is null (nullIntolerant = true)
- Negative results: When start timestamp is later than end timestamp, returns negative values
- Timezone handling: Uses the expression's timezone context or falls back to session timezone
- Precision: Calculations are performed at microsecond precision internally
- Unit validation: Invalid time units will cause runtime errors during evaluation

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code that directly calls `DateTimeUtils.timestampDiff` for better performance compared to interpreted evaluation.

## Examples
```sql
-- Calculate difference in seconds
SELECT TIMESTAMPDIFF('SECOND', '2023-01-01 10:00:00', '2023-01-01 10:05:30');
-- Returns: 330

-- Calculate difference in days
SELECT TIMESTAMPDIFF('DAY', '2023-01-01', '2023-01-15');
-- Returns: 14
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(timestampdiff(lit("HOUR"), col("start_time"), col("end_time")))

// With timezone consideration
df.select(timestampdiff(lit("MINUTE"), 
  col("start_timestamp").cast("timestamp"), 
  col("end_timestamp").cast("timestamp")))
```

## See Also

- DateDiff - for date-only difference calculations
- TimestampAdd - for adding time intervals to timestamps  
- Extract - for extracting specific time components from timestamps
- TimeZoneAwareExpression - base interface for timezone-aware temporal operations