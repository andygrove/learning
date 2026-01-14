# MinutesOfTime

## Overview
The `MinutesOfTime` expression extracts the minute component from a time-based value. This expression is implemented as a `RuntimeReplaceable` that delegates to the `DateTimeUtils.getMinutesOfTime` method at runtime. It returns an integer representing the minutes portion (0-59) of the input time value.

## Syntax
```sql
minute(time_expr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | AnyTimeType | The time expression from which to extract the minute component |

## Return Type
`IntegerType` - Returns an integer value representing the minute component (0-59).

## Supported Data Types
The expression accepts any time-based data type through the `AnyTimeType` constraint:

- TimeType
- TimestampType
- TimestampNTZType

## Algorithm
The expression evaluation follows these steps:

- The expression is replaced at runtime with a `StaticInvoke` call
- Delegates to `DateTimeUtils.getMinutesOfTime` method for actual computation
- The method extracts the minute component from the time representation
- Returns the minute value as an integer between 0 and 59
- Input type information is preserved through the `Seq(child.dataType)` parameter

## Partitioning Behavior
This expression has the following partitioning characteristics:

- Preserves partitioning as it's a deterministic transformation
- Does not require shuffle operations
- Can be safely used in partition pruning scenarios
- Maintains data locality when applied to partitioned datasets

## Edge Cases

- **Null handling**: Returns null when the input time expression is null
- **Invalid time values**: Behavior depends on the underlying `DateTimeUtils.getMinutesOfTime` implementation
- **Timezone considerations**: For timestamp types, the minute extraction may be affected by timezone settings
- **Leap seconds**: Standard minute extraction logic applies, leap seconds are handled by the underlying time utilities

## Code Generation
This expression uses runtime replacement rather than direct code generation:

- Implemented as `RuntimeReplaceable` which means it's replaced with a `StaticInvoke` during analysis
- The actual code generation is handled by the `StaticInvoke` expression
- Supports Tungsten code generation through the static method invocation mechanism
- Performance is optimized through the compiled static method call

## Examples
```sql
-- Extract minute from current timestamp
SELECT minute(current_timestamp()) AS current_minute;

-- Extract minute from time literal
SELECT minute(TIME '14:35:20') AS time_minute;

-- Extract minute from timestamp column
SELECT minute(created_at) AS creation_minute FROM events;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract minute from timestamp column
df.select(minute(col("timestamp_col")).alias("minute_value"))

// Using with current timestamp
df.select(minute(current_timestamp()).alias("current_minute"))
```

## See Also

- `HourOfTime` - Extract hour component from time values
- `SecondsOfTime` - Extract seconds component from time values
- `DateTimeUtils` - Underlying utility class for time operations
- `TimeExpression` - Base trait for time-related expressions