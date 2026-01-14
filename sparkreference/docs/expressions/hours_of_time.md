# HoursOfTime

## Overview
The `HoursOfTime` expression extracts the hour component from time-based data types. It's implemented as a runtime replaceable expression that delegates to the `DateTimeUtils.getHoursOfTime` method for the actual computation.

## Syntax
```sql
HOUR(time_expression)
```

```scala
// DataFrame API
col("time_column").hour
// or
hour(col("time_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The time expression from which to extract the hour component |

## Return Type
`IntegerType` - Returns an integer representing the hour component (0-23 in 24-hour format).

## Supported Data Types
Accepts `AnyTimeType` input data types, which includes:

- TimestampType
- DateType  
- TimeType (if supported by the implementation)

## Algorithm
The expression evaluation follows these steps:

- Validates that the input expression conforms to `AnyTimeType`
- Delegates computation to `DateTimeUtils.getHoursOfTime` static method
- The underlying implementation extracts the hour component from the time-based value
- Returns the hour as an integer value between 0 and 23
- Handles null propagation automatically through the runtime replacement mechanism

## Partitioning Behavior
This expression has minimal impact on partitioning:

- Preserves existing partitioning as it's a projection operation
- Does not require data shuffling
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null when the input expression evaluates to null
- **Invalid time values**: Behavior depends on the underlying `DateTimeUtils.getHoursOfTime` implementation
- **Timezone considerations**: Hour extraction may be affected by session timezone settings
- **Date-only inputs**: When applied to date types, typically returns 0 for the hour component

## Code Generation
This expression uses runtime replacement rather than direct code generation. The `StaticInvoke` replacement enables:

- Efficient bytecode generation through Catalyst's code generation framework
- Direct method invocation of `DateTimeUtils.getHoursOfTime` in generated code
- Optimized execution without interpreted expression evaluation overhead

## Examples
```sql
-- Extract hour from timestamp
SELECT HOUR(TIMESTAMP '2023-12-25 14:30:45') AS hour_part;
-- Returns: 14

-- Extract hour from current timestamp  
SELECT HOUR(NOW()) AS current_hour;

-- Use in WHERE clause
SELECT * FROM events WHERE HOUR(event_time) BETWEEN 9 AND 17;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract hour from timestamp column
df.select(hour($"timestamp_col").as("hour_part"))

// Filter by hour range
df.filter(hour($"event_time").between(9, 17))

// Group by hour
df.groupBy(hour($"created_at").as("hour")).count()
```

## See Also

- `MinutesOfTime` - Extract minutes from time expressions
- `SecondsOfTime` - Extract seconds from time expressions  
- `DayOfMonth` - Extract day component from date/timestamp
- `Month` - Extract month component from date/timestamp
- `Year` - Extract year component from date/timestamp