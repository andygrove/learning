# SparkPartitionID

## Overview
The `SparkPartitionID` expression returns the partition ID of the current partition during query execution. This is a non-deterministic leaf expression that provides access to Spark's internal partitioning information at runtime.

## Syntax
```sql
SPARK_PARTITION_ID()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("SPARK_PARTITION_ID()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This function takes no arguments |

## Return Type
`IntegerType` - Returns an integer representing the partition ID.

## Supported Data Types
This expression does not accept input data as it is a leaf expression. It operates independently of any input data types and always returns an integer partition ID.

## Algorithm
- The expression is initialized once per partition with the partition index value
- During initialization, the `partitionIndex` parameter is stored in the `partitionId` field
- For each row evaluation, it simply returns the stored partition ID value
- The partition ID remains constant for all rows within the same partition
- The expression is marked as `Nondeterministic` because the same logical row can have different partition IDs across different query executions

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect the existing partitioning scheme
- **No shuffle required**: Since it's a leaf expression that only reads partition metadata, no data movement is needed
- The returned value directly corresponds to Spark's internal partition numbering (0-indexed)

## Edge Cases
- **Null handling**: This expression never returns null (`nullable = false`)
- **Empty partitions**: Even empty partitions will have a valid partition ID
- **Single partition**: In single-partition datasets, always returns 0
- **Partition reassignment**: If partitions are redistributed during query execution, the partition ID reflects the current partition assignment

## Code Generation
This expression fully supports Tungsten code generation:
- Uses `doGenCode` method to generate efficient Java code
- Creates an immutable state variable `partitionId` in the generated code
- Initializes the partition ID once per partition using `addPartitionInitializationStatement`
- Generates inline code that directly returns the partition ID value without method calls

## Examples
```sql
-- Get partition ID for each row
SELECT SPARK_PARTITION_ID(), * FROM my_table;

-- Count rows per partition
SELECT SPARK_PARTITION_ID() as partition_id, COUNT(*) as row_count 
FROM my_table 
GROUP BY SPARK_PARTITION_ID();

-- Filter data from specific partitions
SELECT * FROM my_table WHERE SPARK_PARTITION_ID() IN (0, 1, 2);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add partition ID column
val dfWithPartitionId = df.withColumn("partition_id", expr("SPARK_PARTITION_ID()"))

// Group by partition ID
val partitionCounts = df.groupBy(expr("SPARK_PARTITION_ID()")).count()

// Filter by partition ID
val partition0Data = df.filter(expr("SPARK_PARTITION_ID() = 0"))
```

## See Also
- `MonotonicallyIncreasingID` - For generating unique IDs across partitions
- Partitioning functions like `pmod()` for custom partitioning logic
- `INPUT_FILE_NAME()` - For file-based partition information