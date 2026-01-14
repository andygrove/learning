# FromUnixTime

## Overview
The `FromUnixTime` expression converts Unix timestamps (seconds since epoch) to formatted timestamp strings. It takes a Unix timestamp and an optional format pattern, returning a human-readable date-time string representation according to the specified format.

## Syntax
```sql
FROM_UNIXTIME(unix_timestamp [, format])
```

```scala
// DataFrame API
col("timestamp_col").cast("long") // unix timestamp in seconds
from_unixtime(col("unix_seconds"), "yyyy-MM-dd HH:mm:ss")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| sec | Long | Unix timestamp in seconds since epoch (1970-01-01 00:00:00 UTC) |
| format | String | Optional format pattern string (defaults to TimestampFormatter.defaultPattern()) |
| timeZoneId | String | Optional timezone identifier for formatting (internal parameter) |

## Return Type
Returns `StringType` - A UTF-8 encoded string representation of the formatted timestamp.

## Supported Data Types

- **sec parameter**: `LongType` only
- **format parameter**: `StringType` with collation support (supports trim collation)
- Implicit casting is supported for input types through `ImplicitCastInputTypes`

## Algorithm

- Converts the input Unix timestamp (seconds) to microseconds by multiplying by `MICROS_PER_SECOND`
- Creates or retrieves a `TimestampFormatter` instance using the provided format pattern
- Uses the formatter to convert the microsecond timestamp to a formatted string
- Returns the result as a UTF8String
- Handles timezone conversion if a specific timezone is provided

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it's a row-level transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel processing

## Edge Cases

- **Null handling**: Returns null if either input argument is null (null-intolerant behavior)
- **Invalid format patterns**: May throw runtime exceptions for malformed format strings
- **Timestamp overflow**: Large Unix timestamps may cause formatting errors or unexpected results
- **Timezone handling**: Uses system default timezone when no explicit timezone is provided
- **Negative timestamps**: Supports negative Unix timestamps (dates before 1970-01-01)

## Code Generation
This expression supports Tungsten code generation for optimal performance:

- Uses `defineCodeGen` for both cached formatter and dynamic formatter scenarios
- Pre-compiled formatters are stored as reference objects in generated code
- Falls back to runtime formatter creation when format is not constant
- Generates efficient multiplication by 1000000L for microsecond conversion

## Examples
```sql
-- Basic usage with default format
SELECT FROM_UNIXTIME(1672531200) AS formatted_time;
-- Result: "2023-01-01 00:00:00"

-- Custom format pattern
SELECT FROM_UNIXTIME(1672531200, 'yyyy/MM/dd HH:mm:ss') AS custom_format;
-- Result: "2023/01/01 00:00:00"

-- Handle null values
SELECT FROM_UNIXTIME(NULL) AS null_result;
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic conversion
df.select(from_unixtime(col("unix_seconds")))

// Custom format
df.select(from_unixtime(col("unix_seconds"), "dd/MM/yyyy HH:mm"))

// With timezone handling
df.select(from_unixtime(col("unix_seconds")).cast("timestamp"))
```

## See Also

- `UnixTimestamp` - Converts formatted timestamp strings back to Unix timestamps
- `ToTimestamp` - Converts strings to timestamp data type
- `DateFormatClass` - Related date formatting expressions
- `TimestampFormatter` - Underlying formatter implementation