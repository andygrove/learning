# Hours

## Overview
The Hours expression is a v2 partition transform that extracts the hour component from timestamp values for partitioning purposes. It is designed to partition data based on hourly intervals, converting timestamp values to integer representations of hours.

## Syntax
```sql
hours(timestamp_column)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
hours(col("timestamp_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression, typically a timestamp column |

## Return Type
`IntegerType` - Returns an integer representing the hour component.

## Supported Data Types

- TimestampType
- TimestampNTZType (Timestamp without timezone)

## Algorithm

- Extracts the hour component from the input timestamp expression
- Converts the hour value to an integer representation
- The transformation is applied at the partition level for data organization
- Inherits common partition transform behaviors from the parent class
- Supports code generation optimizations through the Catalyst framework

## Partitioning Behavior
How this expression affects partitioning:

- Creates partitions based on hourly intervals
- Enables time-based partition pruning for queries filtering by hour
- Does not require shuffle as it's a deterministic transform
- Improves query performance for time-series data access patterns

## Edge Cases

- Null input values: Returns null for null timestamp inputs
- Invalid timestamp formats: May throw exceptions during evaluation
- Timezone handling: Behavior depends on the specific timestamp type used
- Hour range: Returns values from 0-23 representing the 24-hour format

## Code Generation
This expression supports Tungsten code generation as it extends `PartitionTransformExpression`, which inherits code generation capabilities from the Catalyst expression framework.

## Examples
```sql
-- Partition table by hour
CREATE TABLE events_hourly 
USING DELTA 
PARTITIONED BY (hours(event_timestamp))
AS SELECT * FROM events;

-- Query with hour-based filtering
SELECT * FROM events_hourly 
WHERE hours(event_timestamp) = 14;
```

```scala
// DataFrame API usage for partitioning
import org.apache.spark.sql.functions._

// Create partitioned dataset
df.write
  .partitionBy(hours(col("timestamp")).toString)
  .parquet("path/to/hourly_partitioned_data")

// Filter by specific hour
val afternoonData = df.filter(hours(col("timestamp")) === 14)
```

## See Also

- `Days` - Partition transform for daily intervals
- `Months` - Partition transform for monthly intervals  
- `Years` - Partition transform for yearly intervals
- `Bucket` - Hash-based partition transform
- `PartitionTransformExpression` - Base class for partition transforms