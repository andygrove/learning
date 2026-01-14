# TimestampAddInterval

## Overview
The `TimestampAddInterval` expression adds a time interval to a timestamp value. It supports both day-time intervals (containing days, hours, minutes, seconds) and calendar intervals (containing months, days, and microseconds), with proper timezone handling for accurate temporal arithmetic.

## Syntax
```sql
timestamp_column + INTERVAL '1' DAY
timestamp_column + INTERVAL '1-2' YEAR TO MONTH
```

```scala
// DataFrame API usage
df.select(col("timestamp_col") + expr("INTERVAL '1' DAY"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| start | Expression | The base timestamp value (TimestampType or TimestampNTZType) |
| interval | Expression | The interval to add (CalendarIntervalType or DayTimeIntervalType) |
| timeZoneId | Option[String] | Optional timezone identifier for timezone-aware operations |

## Return Type
Returns the same data type as the input `start` expression (either `TimestampType` or `TimestampNTZType`).

## Supported Data Types

- **Input timestamp**: `AnyTimestampType` (both `TimestampType` and `TimestampNTZType`)
- **Input interval**: `CalendarIntervalType` or `DayTimeIntervalType`

## Algorithm

- Determines the interval type and delegates to appropriate internal methods
- For `DayTimeIntervalType`: calls `timestampAddDayTime` with microseconds precision
- For `CalendarIntervalType`: calls `timestampAddInterval` with separate month, day, and microsecond components
- Applies timezone conversion using the configured `ZoneId` for proper temporal arithmetic
- Handles timezone-aware calculations to account for DST transitions and timezone rules

## Partitioning Behavior
- **Preserves partitioning**: No, adding intervals to timestamps typically changes the partition key values
- **Requires shuffle**: No, this is a per-row transformation that doesn't require data movement

## Edge Cases

- **Null handling**: Returns null if either the timestamp or interval input is null (`nullIntolerant = true`)
- **Timezone transitions**: Properly handles daylight saving time transitions and timezone offset changes
- **Calendar arithmetic**: Month additions handle variable month lengths (e.g., adding 1 month to Jan 31 may result in Feb 28/29)
- **Overflow behavior**: May produce invalid results for extremely large interval values that exceed timestamp boundaries

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized bytecode that calls the appropriate `DateTimeUtils` static methods (`timestampAddDayTime` or `timestampAddInterval`) directly, avoiding object creation overhead during evaluation.

## Examples
```sql
-- Add 1 day to a timestamp
SELECT timestamp_col + INTERVAL '1' DAY FROM events;

-- Add 2 months and 15 days
SELECT timestamp_col + INTERVAL '2-0' YEAR TO MONTH + INTERVAL '15' DAY FROM events;

-- Add precise time intervals
SELECT timestamp_col + INTERVAL '1 2:30:45.123' DAY TO SECOND FROM events;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add interval using SQL expression
df.select(col("timestamp_col") + expr("INTERVAL '1' DAY"))

// Using interval functions
df.select(col("timestamp_col") + expr("make_interval(0, 1, 0, 0, 0, 0)"))
```

## See Also

- `TimestampDiff` - Calculate difference between timestamps
- `DateAdd` - Add days to date values  
- `AddMonths` - Add months to date/timestamp values
- `IntervalExpression` - Create interval literals