# MakeTimestampFromDateTime

## Overview
The `MakeTimestampFromDateTime` expression combines a date value with an optional time value to create a timestamp. It serves as a runtime-replaceable expression that delegates to the `DateTimeUtils.makeTimestamp` method for the actual timestamp construction.

## Syntax
```sql
make_timestamp(date_expr [, time_expr] [, timezone_expr])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| date | DateType | The date component for the timestamp |
| time | AnyTimeType (optional) | The time component; defaults to midnight (00:00:00) if not provided |
| timezone | StringType (optional) | The timezone identifier; defaults to session timezone if not provided |

## Return Type
TimestampType - A timestamp value combining the date and time components in the specified timezone.

## Supported Data Types

- **Date argument**: DateType only
- **Time argument**: AnyTimeType (when provided)  
- **Timezone argument**: StringType with collation support (when provided)

## Algorithm

- Uses midnight (00:00:00) as default when time argument is not provided
- Uses session timezone as default when timezone argument is not provided
- Delegates actual timestamp creation to `DateTimeUtils.makeTimestamp` via `StaticInvoke`
- Preserves nullability based on whether any child expressions are nullable
- Implements timezone-aware behavior through `TimeZoneAwareExpression` trait

## Partitioning Behavior
This expression does not directly affect partitioning behavior as it is a runtime-replaceable expression that operates on individual rows without requiring data movement or shuffling.

## Edge Cases

- **Null handling**: Returns null if any non-optional argument is null, based on child expression nullability
- **Missing time**: Automatically defaults to `Literal(0L, TimeType(0))` representing midnight
- **Missing timezone**: Falls back to the configured session timezone via `timeZoneId.get`
- **Invalid combinations**: Relies on underlying `DateTimeUtils.makeTimestamp` for validation of date/time combinations

## Code Generation
This expression supports code generation through Tungsten as it uses `StaticInvoke` for its replacement, which can generate efficient Java code for the `DateTimeUtils.makeTimestamp` method call.

## Examples
```sql
-- Create timestamp from date only (uses midnight and session timezone)
SELECT make_timestamp(DATE '2023-12-25');

-- Create timestamp with specific time
SELECT make_timestamp(DATE '2023-12-25', TIME '14:30:15');

-- Create timestamp with specific timezone
SELECT make_timestamp(DATE '2023-12-25', TIME '14:30:15', 'America/New_York');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// With date only
df.withColumn("timestamp_col", expr("make_timestamp(date_col)"))

// With date and time
df.withColumn("timestamp_col", expr("make_timestamp(date_col, time_col)"))

// With all parameters
df.withColumn("timestamp_col", expr("make_timestamp(date_col, time_col, 'UTC')"))
```

## See Also

- `MakeTimestamp` - Creates timestamps from individual numeric components
- `DateTimeUtils.makeTimestamp` - The underlying utility method that performs the actual conversion
- `TimeZoneAwareExpression` - Base trait for timezone-sensitive expressions