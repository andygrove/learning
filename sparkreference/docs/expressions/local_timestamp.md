# LocalTimestamp

## Overview

The `LocalTimestamp` expression returns the current timestamp without timezone information at the time of query execution. It provides a timestamp in the local timezone as a TimestampNTZ (timestamp without timezone) data type, representing the current date and time when the expression is evaluated.

## Syntax

```sql
LOCALTIMESTAMP()
-- or
SELECT localtimestamp();
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("localtimestamp()"))
```

## Arguments

This expression takes no arguments. The `timeZoneId` parameter is used internally for timezone-aware processing but is not exposed to users.

## Return Type

`TimestampNTZType` - Timestamp without timezone information, represented as microseconds since epoch.

## Supported Data Types

This is a leaf expression that generates timestamp values and does not accept input data of any type.

## Algorithm

- Retrieves the current system time using `LocalDateTime.now(zoneId)`

- Converts the LocalDateTime to microseconds since epoch using `localDateTimeToMicros`

- Uses the configured timezone (`zoneId`) to determine the local time context

- Returns the timestamp value as TimestampNTZ type without timezone information

- The expression is foldable, meaning it can be constant-folded during optimization

## Partitioning Behavior

- Preserves partitioning as it generates the same value for all rows in a given query execution

- Does not require shuffle operations

- Can be used safely in partitioned operations without affecting partition boundaries

## Edge Cases

- Never returns null (nullable = false)

- Returns the same timestamp value for all rows within a single query execution due to constant folding

- Timezone handling depends on the session's configured timezone

- The timestamp represents the query execution time, not row processing time

## Code Generation

This expression uses `CodegenFallback`, meaning it falls back to interpreted mode rather than generating optimized Java code. The evaluation uses the `eval` method for all executions.

## Examples

```sql
-- Get current local timestamp
SELECT localtimestamp();
-- Output: 2020-04-25 15:49:11.914

-- Use in SELECT with other columns
SELECT id, name, localtimestamp() as created_at FROM users;

-- Use in WHERE clause for time-based filtering
SELECT * FROM events WHERE event_time > localtimestamp() - INTERVAL 1 HOUR;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add current timestamp column
df.withColumn("processed_at", expr("localtimestamp()"))

// Filter using current timestamp
df.filter(col("updated_at") > expr("localtimestamp() - INTERVAL 1 DAY"))
```

## See Also

- `CurrentTimestamp` - Returns current timestamp with timezone information
- `Now` - Alias for current timestamp
- `UnixTimestamp` - Returns current time as Unix timestamp
- `CurrentDate` - Returns current date without time component