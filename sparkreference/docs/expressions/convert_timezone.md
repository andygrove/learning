# ConvertTimezone

## Overview
The `ConvertTimezone` expression converts a timestamp from one timezone to another timezone. It takes a timestamp without timezone (TimestampNTZ) and interprets it in the source timezone, then converts it to the equivalent timestamp in the target timezone.

## Syntax
```sql
convert_timezone(source_tz, target_tz, source_timestamp)
convert_timezone(target_tz, source_timestamp)  -- uses current session timezone as source
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| source_tz | String | Source timezone identifier (optional, defaults to current session timezone) |
| target_tz | String | Target timezone identifier |
| source_timestamp | TimestampNTZ | Timestamp without timezone to convert |

## Return Type
Returns `TimestampNTZType` - a timestamp without timezone information representing the equivalent time in the target timezone.

## Supported Data Types

- Source and target timezone parameters must be string types with collation support
- Source timestamp must be TimestampNTZ type
- Supports string trimming collations for timezone parameters

## Algorithm

- Interprets the input TimestampNTZ as a local time in the source timezone
- Converts the timestamp to UTC based on the source timezone rules
- Applies the target timezone offset and daylight saving rules
- Returns the equivalent local time as TimestampNTZ in the target timezone
- Uses `DateTimeUtils.convertTimestampNtzToAnotherTz` for the core conversion logic

## Partitioning Behavior
How this expression affects partitioning (if applicable):

- Preserves partitioning as it's a row-level transformation
- Does not require shuffle operations
- Can be pushed down in query optimization

## Edge Cases

- Null handling: Returns null if any input parameter is null (null intolerant behavior)
- Invalid timezone identifiers will cause runtime errors
- Ambiguous times during DST transitions follow Java timezone handling rules
- Non-existent times during DST transitions are handled according to the target timezone's rules

## Code Generation
This expression supports Tungsten code generation and will generate optimized Java code rather than falling back to interpreted mode. The generated code directly calls `DateTimeUtils.convertTimestampNtzToAnotherTz`.

## Examples
```sql
-- Convert from UTC to Pacific Time
SELECT convert_timezone('UTC', 'America/Los_Angeles', timestamp_ntz'2021-12-06 08:00:00');
-- Result: 2021-12-06 00:00:00

-- Convert using current session timezone as source
SELECT convert_timezone('Europe/London', timestamp_ntz'2021-12-06 12:00:00');
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._
df.select(
  expr("convert_timezone('UTC', 'Asia/Tokyo', timestamp_col)").as("tokyo_time")
)

// Using two-parameter version
df.select(
  expr("convert_timezone('Europe/Berlin', timestamp_col)").as("berlin_time")
)
```

## See Also

- `CurrentTimeZone` - gets the current session timezone
- `ToUTCTimestamp` - converts to UTC timezone
- `FromUTCTimestamp` - converts from UTC timezone
- Other datetime functions in the `datetime_funcs` group