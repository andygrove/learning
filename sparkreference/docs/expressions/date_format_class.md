# DateFormatClass

## Overview
The DateFormatClass expression formats timestamp values into string representations using customizable date/time format patterns. It provides SQL function `date_format` that converts timestamp data to formatted strings according to specified formatting patterns.

## Syntax
```sql
date_format(timestamp_expr, format_string)
```

```scala
// DataFrame API
df.select(date_format(col("timestamp_column"), "yyyy-MM-dd HH:mm:ss"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left (timestamp_expr) | TimestampType | The timestamp value to be formatted |
| right (format_string) | StringType | The format pattern string (e.g., "yyyy-MM-dd", "MM/dd/yyyy HH:mm") |
| timeZoneId | Option[String] | Optional timezone identifier for formatting (internal parameter) |

## Return Type
StringType - Returns a UTF8String containing the formatted timestamp representation.

## Supported Data Types

- **Input**: TimestampType for the timestamp value, StringType with collation support for the format pattern
- **Output**: StringType (UTF8String)

## Algorithm

- Accepts a timestamp (as Long microseconds) and a format pattern string as inputs
- Creates or reuses a TimestampFormatter based on the format pattern and timezone
- Applies the formatter to convert the timestamp into a string representation
- Returns the formatted result as a UTF8String
- Supports both interpreted evaluation and code generation for performance optimization

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partitioning since it's a row-level transformation
- Can be pushed down to individual partitions for parallel processing

## Edge Cases

- **Null handling**: Returns null if either timestamp or format string is null (nullIntolerant = true)
- **Invalid format patterns**: May throw runtime exceptions for malformed format strings
- **Timezone awareness**: Uses provided timezone or falls back to system default
- **Legacy format support**: Maintains compatibility with SimpleDateFormat patterns through LegacyDateFormats

## Code Generation
This expression supports Tungsten code generation for optimized performance:

- Generates efficient Java code when format pattern is known at compile time
- Falls back to runtime formatter creation for dynamic format patterns
- Uses TimestampFormatter class for consistent formatting behavior
- Optimizes repeated formatting operations by caching formatter instances

## Examples
```sql
-- Format timestamp as date string
SELECT date_format(current_timestamp(), 'yyyy-MM-dd') as formatted_date;

-- Format with custom pattern
SELECT date_format(timestamp_col, 'MM/dd/yyyy HH:mm:ss') as custom_format
FROM events_table;

-- Format with different patterns
SELECT 
  date_format(created_at, 'yyyy') as year,
  date_format(created_at, 'MMMM') as month_name
FROM transactions;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic date formatting
df.select(date_format(col("timestamp"), "yyyy-MM-dd"))

// Multiple format patterns
df.select(
  date_format(col("created_at"), "yyyy-MM-dd").as("date"),
  date_format(col("created_at"), "HH:mm:ss").as("time")
)
```

## See Also

- UnixTimestamp - Convert formatted strings back to timestamps
- FromUnixTime - Format Unix timestamps to strings  
- DateAdd/DateSub - Date arithmetic operations
- ToDate/ToTimestamp - Date/timestamp conversion functions