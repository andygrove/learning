# CurrentDate

## Overview
The `CurrentDate` expression returns the current date in the session time zone. It is a deterministic function that returns the same date value throughout a single query execution, making it foldable for optimization purposes.

## Syntax
```sql
CURRENT_DATE
CURRENT_DATE()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.current_date
df.select(current_date())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| timeZoneId | Option[String] | Optional time zone identifier for date calculation (internal parameter) |

## Return Type
Returns `DateType` - a date value without time component.

## Supported Data Types
This expression takes no input data types as it is a leaf expression that generates a date value based on the current system time.

## Algorithm

- Evaluates the current system timestamp in the configured time zone
- Extracts only the date component, discarding time information
- Returns the same date value for all calls within a single query execution
- Uses the session time zone or explicitly set time zone for date calculation
- Implements foldable optimization since the value is constant per query

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning schemes as it adds computed columns
- Does not require shuffle operations
- Can be used safely in partitioned operations without performance impact

## Edge Cases

- Never returns null values (nullable = false)
- Returns consistent date across all nodes in a distributed execution
- Date boundary depends on the configured time zone
- Behavior is deterministic within query execution but varies between queries
- Time zone changes affect the returned date value

## Code Generation
This expression uses `CodegenFallback`, meaning it falls back to interpreted evaluation mode rather than generating optimized Java code via Tungsten code generation.

## Examples
```sql
-- Get current date
SELECT CURRENT_DATE;

-- Use in WHERE clause
SELECT * FROM events WHERE event_date = CURRENT_DATE;

-- Compare with timestamp column
SELECT *, CURRENT_DATE AS today FROM logs;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add current date column
df.withColumn("current_date", current_date())

// Filter by current date
df.filter(col("date_column") === current_date())

// Select current date
spark.sql("SELECT CURRENT_DATE").show()
```

## See Also

- `CurrentTimestamp` - returns current timestamp with time component
- `Now` - alias for current timestamp
- `UnixTimestamp` - returns current time as Unix timestamp
- `DateFormatClass` - for formatting date values