# SubtractTimestamps

## Overview
The `SubtractTimestamps` expression computes the difference between two timestamp values. Depending on configuration, it returns either a legacy `CalendarInterval` (with microseconds field only) or a `DayTimeInterval` representing the time difference in microseconds.

## Syntax
```sql
timestamp_expr1 - timestamp_expr2
```

```scala
// DataFrame API
col("end_timestamp") - col("start_timestamp")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The end timestamp (minuend) |
| right | Expression | The start timestamp (subtrahend) |
| legacyInterval | Boolean | Whether to return CalendarInterval (true) or DayTimeInterval (false) |
| timeZoneId | Option[String] | Optional timezone identifier for timestamp interpretation |

## Return Type
- `CalendarInterval` when `legacyInterval` is true (controlled by `spark.sql.legacy.interval.enabled`)
- `DayTimeIntervalType` when `legacyInterval` is false

## Supported Data Types
- Input types: Any timestamp type (`TimestampType`, `TimestampNTZType`)
- Both operands must be timestamp types

## Algorithm

- Converts both timestamp expressions to microsecond values (Long)

- In legacy mode: Creates a `CalendarInterval` with months=0, days=0, and microseconds set to the difference

- In non-legacy mode: Calls `subtractTimestamps` utility method with timezone awareness to compute `DayTimeInterval`

- Uses timezone information from the left operand's data type for evaluation

- Performs null-safe evaluation, returning null if either operand is null

## Partitioning Behavior
- Preserves partitioning as it operates on individual rows without requiring data movement
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if either timestamp operand is null (null-intolerant behavior)

- **Timezone handling**: Uses timezone from left operand's data type; respects explicit timeZoneId parameter

- **Overflow**: Large timestamp differences may cause microsecond overflow in the resulting interval

- **Negative intervals**: When left timestamp is earlier than right timestamp, produces negative interval values

## Code Generation
Supports Tungsten code generation for optimized execution:

- Legacy mode: Generates inline `CalendarInterval` constructor code
- Non-legacy mode: Generates call to `DateTimeUtils.subtractTimestamps` with timezone parameter
- Falls back to interpreted mode only if code generation context limitations are reached

## Examples
```sql
-- Basic timestamp subtraction
SELECT end_time - start_time AS duration 
FROM events;

-- With explicit timestamps
SELECT TIMESTAMP '2023-12-25 10:30:00' - TIMESTAMP '2023-12-25 09:15:30' AS time_diff;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("end_timestamp") - col("start_timestamp") as "duration")

// With literal timestamps
df.select(
  (lit("2023-12-25 10:30:00").cast("timestamp") - 
   lit("2023-12-25 09:15:30").cast("timestamp")) as "duration"
)
```

## See Also
- `DateAdd` - Add intervals to dates
- `TimestampAdd` - Add intervals to timestamps  
- `DateDiff` - Calculate date differences
- `CalendarInterval` - Legacy interval representation
- `DayTimeIntervalType` - Modern interval type