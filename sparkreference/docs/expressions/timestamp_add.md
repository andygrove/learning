# TimestampAdd

## Overview
The `TimestampAdd` expression adds a specified quantity of time units to a timestamp value. It supports various time units (like days, hours, minutes, seconds) and is timezone-aware, returning a timestamp of the same type as the input timestamp.

## Syntax
```sql
TIMESTAMPADD(unit, quantity, timestamp)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| unit | String | The time unit to add (e.g., "YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND") |
| quantity | Long | The number of units to add to the timestamp |
| timestamp | AnyTimestampType | The base timestamp to which the quantity will be added |
| timeZoneId | Option[String] | Optional timezone identifier for timezone-aware calculations |

## Return Type
Returns the same data type as the input `timestamp` parameter (preserves whether it's `TimestampType` or `TimestampNTZType`).

## Supported Data Types

- **quantity**: `LongType` only
- **timestamp**: Any timestamp type (`TimestampType` or `TimestampNTZType`)
- **unit**: String literal representing valid time units

## Algorithm

- Converts the unit string parameter to a standardized format for internal processing
- Determines the appropriate timezone based on the timestamp data type using `zoneIdForType`
- Delegates the actual timestamp arithmetic to `DateTimeUtils.timestampAdd`
- Performs null-safe evaluation where any null input results in null output
- Maintains the original timestamp's data type in the result

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning schemes
- Does not require data shuffling
- Operates on individual rows independently

## Edge Cases

- **Null handling**: Returns null if any input parameter (quantity or timestamp) is null (`nullIntolerant = true`)
- **Timezone handling**: Automatically selects appropriate timezone based on timestamp data type
- **Unit validation**: Invalid unit strings are handled during expression conversion phase
- **Overflow**: Large quantity values may cause timestamp overflow, behavior depends on underlying `DateTimeUtils` implementation

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code that directly calls `DateTimeUtils.timestampAdd` for better performance.

## Examples
```sql
-- Add 5 days to a timestamp
SELECT TIMESTAMPADD('DAY', 5, TIMESTAMP '2010-01-01 01:02:03.123456');

-- Add 3 hours to current timestamp
SELECT TIMESTAMPADD('HOUR', 3, current_timestamp());

-- Subtract time by using negative quantity
SELECT TIMESTAMPADD('MINUTE', -30, TIMESTAMP '2010-01-01 12:00:00');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add 7 days to a timestamp column
df.select(expr("TIMESTAMPADD('DAY', 7, timestamp_col)"))

// Using column references for quantity
df.select(expr("TIMESTAMPADD('HOUR', quantity_col, timestamp_col)"))
```

## See Also

- `DateAdd` - For date-only arithmetic
- `DateSub` - For subtracting from dates
- `Interval` expressions for duration-based calculations
- `TimeZoneAwareExpression` trait for timezone handling