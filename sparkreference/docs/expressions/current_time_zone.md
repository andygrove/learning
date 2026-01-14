# CurrentTimeZone

## Overview
The `CurrentTimeZone` expression returns the current session time zone as a string. This is a non-deterministic expression that retrieves the time zone setting for the current Spark session without requiring any input parameters.

## Syntax
```sql
SELECT current_timezone();
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("current_timezone()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | N/A | This expression takes no arguments |

## Return Type
`StringType` - Returns the time zone identifier as a string (e.g., "Asia/Shanghai", "UTC").

## Supported Data Types
This expression does not accept input data types as it is a leaf expression with no parameters.

## Algorithm

- Retrieves the current session's time zone configuration
- Returns the time zone identifier as a string representation
- Operates as a leaf expression in the Catalyst expression tree
- Extends `Unevaluable` trait, indicating special evaluation handling
- Uses `DefaultStringProducingExpression` for consistent string output behavior

## Partitioning Behavior
This expression has minimal impact on partitioning:

- Preserves existing partitioning as it generates the same value across all partitions
- Does not require shuffle operations
- Can be safely used in partitioned operations without affecting data distribution

## Edge Cases

- Never returns null values (`nullable = false`)
- Always returns a valid time zone string based on session configuration
- Behavior is consistent within a single session but may vary across different sessions
- No overflow or underflow conditions as it returns configuration data

## Code Generation
This expression extends `Unevaluable`, which means it does not support standard Tungsten code generation and falls back to interpreted evaluation mode during query execution.

## Examples
```sql
-- Get current session timezone
SELECT current_timezone();
-- Result: Asia/Shanghai

-- Use in a query with other datetime functions
SELECT current_timestamp(), current_timezone();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add timezone column to existing DataFrame
df.withColumn("session_tz", expr("current_timezone()"))

// Select timezone with other columns
df.select($"id", expr("current_timezone()").as("timezone"))
```

## See Also

- `current_timestamp()` - Returns current timestamp in session timezone
- `current_date()` - Returns current date in session timezone
- Timezone conversion functions for working with different time zones