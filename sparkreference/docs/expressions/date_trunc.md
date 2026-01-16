# DateTrunc

## Overview
The `TruncTimestamp` expression truncates a timestamp to the specified unit of time precision. It returns a timestamp with all components below the specified unit set to their minimum values (zeroed out for time components, or set to period start for date components). This is implemented as the `TruncTimestamp` case class extending `TruncInstant` with `TimeZoneAwareExpression`.

This function provides more granular control than `trunc()`, supporting truncation down to microsecond precision.

## Syntax
```sql
DATE_TRUNC(format, timestamp)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
date_trunc("hour", col("timestamp_column"))
date_trunc("day", col("timestamp_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| format | StringType | The unit to truncate to (see supported units below) |
| timestamp | TimestampType or StringType (castable to timestamp) | The timestamp value to truncate |

**Note:** The argument order is `(format, timestamp)`, which differs from `trunc(date, format)`.

## Return Type
Returns TimestampType. The result includes both date and time components, with precision below the specified unit zeroed out.

## Supported Format Units

| Unit | Aliases | Description |
|------|---------|-------------|
| year | 'YEAR', 'YYYY', 'YY' | First moment of the year (Jan 1, 00:00:00) |
| quarter | 'QUARTER' | First moment of the quarter |
| month | 'MONTH', 'MON', 'MM' | First moment of the month |
| week | 'WEEK' | Monday 00:00:00 of the week |
| day | 'DAY', 'DD' | Midnight (00:00:00) of that day |
| hour | 'HOUR' | Start of the hour (:00:00) |
| minute | 'MINUTE' | Start of the minute (:00) |
| second | 'SECOND' | Start of the second (.000000) |
| millisecond | 'MILLISECOND' | Truncate to millisecond precision |
| microsecond | 'MICROSECOND' | Truncate to microsecond precision |

## Internal Implementation

From `DateTimeUtils.truncTimestamp()`:
```scala
def truncTimestamp(micros: Long, level: Int, zoneId: ZoneId): Long = {
  // Time zone offsets have a maximum precision of seconds.
  // Truncation to microsecond, millisecond, and second can be done
  // without using time zone information (performance optimization).
  level match {
    case TRUNC_TO_MICROSECOND => micros
    case TRUNC_TO_MILLISECOND =>
      micros - Math.floorMod(micros, MICROS_PER_MILLIS)
    case TRUNC_TO_SECOND =>
      micros - Math.floorMod(micros, MICROS_PER_SECOND)
    case TRUNC_TO_MINUTE => truncToUnit(micros, zoneId, ChronoUnit.MINUTES)
    case TRUNC_TO_HOUR => truncToUnit(micros, zoneId, ChronoUnit.HOURS)
    case TRUNC_TO_DAY => truncToUnit(micros, zoneId, ChronoUnit.DAYS)
    case _ => // Date-level truncation (year, quarter, month, week)
      val dDays = microsToDays(micros, zoneId)
      daysToMicros(truncDate(dDays, level), zoneId)
  }
}
```

## Algorithm

- Parses the format string using `parseTruncLevel()` to get the truncation level constant
- For sub-second precision (MICROSECOND, MILLISECOND, SECOND): uses modulo arithmetic for performance
- For MINUTE, HOUR, DAY: uses `ChronoUnit` truncation with timezone awareness
- For date-level units (YEAR, QUARTER, MONTH, WEEK): converts to days, calls `truncDate()`, converts back
- Timezone handling is critical for correct truncation across DST boundaries

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be pushed down to individual partitions
- Commonly used for time-based aggregations and grouping

## Edge Cases

- **Null handling**: Returns null if the timestamp argument is null
- **Invalid format**: Returns null if the format string is not recognized
- **Case sensitivity**: Format string is case-insensitive
- **String timestamps**: String inputs are implicitly cast to TimestampType
- **Timezone handling**: Operates in the session timezone context
- **DST transitions**: Special handling for dates that fall into DST gaps (e.g., America/Sao_Paulo historic dates). When truncation moves time into a non-existent hour, the time is adjusted forward.

## Examples
```sql
-- Truncate to year
SELECT DATE_TRUNC('year', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-01-01 00:00:00

-- Truncate to month
SELECT DATE_TRUNC('month', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-03-01 00:00:00

-- Truncate to day
SELECT DATE_TRUNC('day', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-03-15 00:00:00

-- Truncate to hour
SELECT DATE_TRUNC('hour', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-03-15 14:00:00

-- Truncate to minute
SELECT DATE_TRUNC('minute', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-03-15 14:32:00

-- Truncate to second
SELECT DATE_TRUNC('second', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-03-15 14:32:05

-- Truncate to millisecond
SELECT DATE_TRUNC('millisecond', TIMESTAMP '2024-03-15 14:32:05.123456') AS result;
-- Returns: 2024-03-15 14:32:05.123
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Group events by hour
df.groupBy(date_trunc("hour", col("event_time"))).count()

// Truncate to day for daily aggregations
df.withColumn("day", date_trunc("day", $"timestamp"))
  .groupBy("day")
  .agg(sum("amount"))

// Multiple truncation levels
df.select(
  date_trunc("year", col("ts")).alias("year"),
  date_trunc("month", col("ts")).alias("month"),
  date_trunc("day", col("ts")).alias("day")
)
```

## See Also

- `trunc` - Truncate dates to year, quarter, month, or week (returns DateType)
- `time_trunc` - Truncate time values to time-level precision
- `extract` - Extract specific components from timestamps
- `to_date` - Convert timestamp to date (similar to truncating to day)
