# Years

## Overview
The `Years` expression is a v2 partition transform that extracts the year component from date/timestamp values for partitioning purposes. It converts temporal data into integer year values, enabling efficient time-based partitioning strategies in Spark SQL tables.

## Syntax
```sql
YEARS(column_name)
```

```scala
// DataFrame API usage
Years(col("date_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression, typically a date or timestamp column |

## Return Type
`IntegerType` - Returns the year as an integer value.

## Supported Data Types

- DateType
- TimestampType
- TimestampNTZType (timestamp without timezone)

## Algorithm

- Extracts the year component from the input date/timestamp expression
- Converts the temporal value to its corresponding year as an integer
- Handles timezone considerations for timestamp inputs based on session timezone
- Returns null if the input expression evaluates to null
- Uses Spark's internal date/time calculation routines for consistent results

## Partitioning Behavior
How this expression affects partitioning:

- Preserves co-location of data within the same year
- Enables partition pruning for year-based queries
- Creates separate partitions for each distinct year in the dataset
- Does not require shuffle when used as a partition transform during table creation
- Allows efficient time-range queries by eliminating irrelevant partitions

## Edge Cases

- Null handling: Returns null when the input expression is null
- Invalid dates: Follows Spark's standard date parsing and validation rules
- Year boundaries: Correctly handles leap years and year transitions
- Timezone effects: For timestamp inputs, the year extraction respects the session timezone setting
- Historical dates: Supports dates across the full range supported by Spark's date types

## Code Generation
This expression extends `PartitionTransformExpression` which typically supports Catalyst code generation for optimized execution. The actual year extraction logic is delegated to Spark's built-in temporal functions that support Tungsten code generation.

## Examples
```sql
-- Creating a table partitioned by years
CREATE TABLE events (
  id BIGINT,
  event_time TIMESTAMP,
  data STRING
) USING DELTA
PARTITIONED BY (YEARS(event_time))

-- Query that benefits from partition pruning
SELECT * FROM events 
WHERE event_time >= '2023-01-01' AND event_time < '2024-01-01'
```

```scala
// DataFrame API usage in partition transforms
import org.apache.spark.sql.catalyst.expressions.Years
import org.apache.spark.sql.functions.col

// Transform expression for partitioning
val yearTransform = Years(col("timestamp_col").expr)

// Usage in DataFrameWriter for partitioned writes
df.write
  .partitionBy("year_partition")
  .option("partitionOverwriteMode", "dynamic")
  .save("/path/to/table")
```

## See Also

- `Months` - Monthly partition transform
- `Days` - Daily partition transform  
- `Hours` - Hourly partition transform
- `Bucket` - Hash-based partition transform
- `PartitionTransformExpression` - Base class for partition transforms