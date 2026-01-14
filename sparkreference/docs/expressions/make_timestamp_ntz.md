# MakeTimestampNTZ

## Overview
`MakeTimestampNTZ` creates a timestamp without timezone (NTZ) by combining a date with a time value. This expression is a runtime replaceable binary expression that delegates its implementation to the `DateTimeUtils.makeTimestampNTZ` method.

## Syntax
```sql
make_timestamp_ntz(date_expr, time_expr)
```

```scala
// DataFrame API
col("date_col").make_timestamp_ntz(col("time_col"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | DateType | The date component for the timestamp |
| right | AnyTimeType | The time component (can be time or timestamp type) |

## Return Type
`TimestampNTZType` - A timestamp without timezone information.

## Supported Data Types

- **Left operand**: `DateType` only
- **Right operand**: Any time-related type (`AnyTimeType` which includes time and timestamp types)

## Algorithm

- Takes a date value as the first argument to provide the date component
- Takes a time value as the second argument to provide the time component  
- Delegates evaluation to `DateTimeUtils.makeTimestampNTZ` static method via `StaticInvoke`
- Combines the date and time components into a single timestamp without timezone
- Returns the resulting timestamp in NTZ format

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it's a row-level transformation
- Does not require data shuffle
- Can be applied within partition boundaries

## Edge Cases

- **Null handling**: If either input is null, the result will be null
- **Invalid dates**: Behavior depends on the underlying `DateTimeUtils.makeTimestampNTZ` implementation
- **Time overflow**: Time values that exceed 24-hour boundaries may wrap or cause errors depending on implementation
- **Timezone considerations**: Output explicitly excludes timezone information (NTZ = No Time Zone)

## Code Generation
This expression uses `RuntimeReplaceable` with `StaticInvoke`, which supports Tungsten code generation. The actual code generation is handled by the replacement `StaticInvoke` expression calling the static method.

## Examples
```sql
-- Create timestamp NTZ from date and time
SELECT make_timestamp_ntz(DATE '2023-12-25', TIME '14:30:00') as christmas_afternoon;

-- Using with table columns
SELECT make_timestamp_ntz(date_col, time_col) as full_timestamp 
FROM events_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("make_timestamp_ntz(event_date, event_time)"))

// With column references  
df.withColumn("full_timestamp", expr("make_timestamp_ntz(date_col, time_col)"))
```

## See Also

- `MakeDate` - Creates date values from year, month, day components
- `MakeTimestamp` - Creates timestamp with timezone
- `DateTimeUtils` - Underlying utility class containing the implementation
- `TimestampNTZType` - The return data type for timezone-naive timestamps