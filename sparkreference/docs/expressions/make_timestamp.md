# MakeTimestamp

## Overview
The `MakeTimestamp` expression constructs a timestamp value from separate year, month, day, hour, minute, and second components, with optional timezone specification. It supports microsecond precision through decimal seconds and can operate in both fail-on-error (ANSI) and null-on-error modes depending on configuration.

## Syntax
```sql
make_timestamp(year, month, day, hour, min, sec [, timezone])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| year | IntegerType | The year component (e.g., 2023) |
| month | IntegerType | The month component (1-12) |
| day | IntegerType | The day component (1-31) |
| hour | IntegerType | The hour component (0-23) |
| min | IntegerType | The minute component (0-59) |
| sec | DecimalType(16,6) | The second component with microsecond precision (0-59.999999) |
| timezone | StringType (optional) | The timezone identifier (e.g., "UTC", "America/New_York") |

## Return Type
Returns the configured timestamp type (`SQLConf.get.timestampType`), which can be either `TimestampType` (timestamp with timezone) or `TimestampNTZType` (timestamp without timezone).

## Supported Data Types

- Year, month, day, hour, minute: Integer types that can be cast to `IntegerType`
- Seconds: Numeric types that can be cast to `DecimalType(16,6)` to preserve microsecond precision
- Timezone: String types with collation support

## Algorithm

- Converts the decimal seconds to separate seconds and nanoseconds components using floor division and modulo operations
- Handles the special case where seconds = 60 by adding one minute to the timestamp (PostgreSQL compatibility)
- Creates a `LocalDateTime` object from the validated components
- For `TimestampType`, converts to an `Instant` using the specified timezone, then to microseconds since epoch
- For `TimestampNTZType`, directly converts the local datetime to microseconds
- Throws exceptions in ANSI mode or returns null for invalid inputs depending on `failOnError` configuration

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Can be evaluated independently for each row
- Maintains existing partition boundaries

## Edge Cases

- Null inputs: Returns null if any input is null (null intolerant)
- Invalid dates: Returns null in non-ANSI mode, throws exception in ANSI mode (e.g., February 30th)
- Seconds = 60: Supported only when nanoseconds = 0, adds one minute for PostgreSQL compatibility
- Fractional seconds > 60: Throws `invalidFractionOfSecondError`
- Invalid timezone strings: Throws exception during timezone parsing
- Overflow conditions: Handled by underlying Java time libraries with appropriate exceptions

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code for:

- Direct conversion operations without object allocation overhead
- Inline timezone handling and validation
- Exception handling branches based on `failOnError` configuration
- Efficient decimal arithmetic for microsecond precision

## Examples
```sql
-- Create timestamp with explicit timezone
SELECT make_timestamp(2023, 12, 25, 14, 30, 45.123456, 'UTC');

-- Create timestamp using session timezone
SELECT make_timestamp(2023, 1, 1, 0, 0, 0.0);

-- Handle leap seconds (PostgreSQL compatibility)
SELECT make_timestamp(2023, 6, 30, 23, 59, 60.0, 'UTC');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.withColumn("timestamp", 
  expr("make_timestamp(year_col, month_col, day_col, hour_col, min_col, sec_col, 'America/New_York')"))

// Using literals
df.select(expr("make_timestamp(2023, 12, 25, 14, 30, 45.123456)"))
```

## See Also

- `MakeDate` - Creates date values from year, month, day components
- `ToTimestamp` - Parses timestamp from string with format
- `DateAdd` / `DateSub` - Arithmetic operations on dates
- `FromUnixTime` - Converts Unix timestamp to formatted date string