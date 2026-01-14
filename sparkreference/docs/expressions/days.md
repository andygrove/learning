# Days

## Overview
The `Days` expression is a v2 partition transform that converts timestamp values to the number of days since a reference epoch. This transform is used for partitioning data by day buckets, allowing efficient querying of time-series data partitioned at the daily level.

## Syntax
```sql
-- SQL syntax (when used in partition transforms)
PARTITIONED BY (days(timestamp_column))
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.Days
Days(child = timestampColumn)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that should evaluate to a timestamp or date value |

## Return Type
`IntegerType` - Returns an integer representing the number of days since the epoch.

## Supported Data Types

- TimestampType
- DateType
- Any expression that can be implicitly cast to timestamp or date

## Algorithm

- Extracts the timestamp or date value from the child expression
- Converts the timestamp to the number of days since the Unix epoch (1970-01-01)
- Truncates any time component, keeping only the date portion
- Returns the day number as an integer for partitioning purposes
- Handles timezone considerations based on the session's timezone settings

## Partitioning Behavior
How this expression affects partitioning:

- Preserves co-location of data within the same day
- Does not require shuffle when used as a partition transform during table creation
- Creates partition buckets based on day boundaries
- Enables partition pruning for queries with date/timestamp predicates

## Edge Cases

- Null input values result in null output (standard null propagation)
- Timestamps before Unix epoch (1970-01-01) result in negative day numbers
- Leap years and daylight saving time transitions are handled according to the configured timezone
- Date boundary calculations respect the session timezone configuration

## Code Generation
This expression extends `PartitionTransformExpression` which typically supports Catalyst code generation for efficient evaluation. The actual computation delegates to underlying date/timestamp functions that are code-gen enabled.

## Examples
```sql
-- Creating a table partitioned by days
CREATE TABLE events (
    id BIGINT,
    event_time TIMESTAMP,
    data STRING
) PARTITIONED BY (days(event_time))
```

```scala
// DataFrame API usage in partition transforms
import org.apache.spark.sql.catalyst.expressions.Days

// Used internally when defining partition transforms
val dayTransform = Days(col("event_timestamp").expr)
```

## See Also

- `Hours` - Partition transform for hourly buckets
- `Months` - Partition transform for monthly buckets  
- `Years` - Partition transform for yearly buckets
- `Bucket` - Hash-based partition transform
- `PartitionTransformExpression` - Base class for partition transforms