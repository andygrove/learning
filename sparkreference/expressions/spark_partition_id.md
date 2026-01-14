# SparkPartitionID

## Overview
`SparkPartitionID` is a Catalyst expression that returns the current partition identifier for each row in a Spark DataFrame or Dataset. This expression provides access to Spark's internal partitioning information, allowing users to identify which partition a particular row belongs to during distributed processing.

## Syntax
```sql
SPARK_PARTITION_ID()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.spark_partition_id
df.select(spark_partition_id())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`IntegerType` - Returns a 32-bit integer representing the partition ID.

## Supported Data Types
This expression does not operate on input data types as it takes no arguments. It generates partition metadata independently of the underlying data.

## Algorithm
- The expression is initialized once per partition with the partition index during task setup
- The partition ID is stored as a transient field (`partitionId`) within each task
- During evaluation, the expression simply returns the stored partition ID value
- The partition ID remains constant for all rows within the same partition
- Partition IDs are zero-based integers assigned by Spark's task scheduler

## Partitioning Behavior
- **Preserves partitioning**: Yes, this expression does not affect the existing partitioning scheme
- **Requires shuffle**: No, the expression operates locally within each partition
- **Partition-aware**: This expression is inherently partition-aware and returns different values across partitions
- The returned partition ID corresponds to the RDD partition index, not necessarily the original data source partition

## Edge Cases
- **Null handling**: This expression never returns null (`nullable = false`)
- **Empty partitions**: Returns the partition ID even for empty partitions (though no rows would be present to display it)
- **Partition reassignment**: If data is repartitioned, partition IDs will reflect the new partitioning scheme
- **Determinism**: Marked as `Nondeterministic` because results depend on Spark's internal partitioning decisions, which may vary between executions

## Code Generation
This expression fully supports Tungsten code generation. The generated code:
- Creates an immutable state variable (`partitionId`) in the generated class
- Initializes the partition ID during the partition initialization phase
- Generates efficient Java code that directly returns the stored partition ID value
- Avoids null checks since the expression is never null

## Examples
```sql
-- Get partition ID for each row
SELECT SPARK_PARTITION_ID(), customer_id, order_date 
FROM orders;

-- Count rows per partition
SELECT SPARK_PARTITION_ID() as partition_id, COUNT(*) as row_count
FROM large_table
GROUP BY SPARK_PARTITION_ID();

-- Identify data skew by examining partition distribution
SELECT SPARK_PARTITION_ID() as partition, COUNT(*) as records
FROM dataset
GROUP BY SPARK_PARTITION_ID()
ORDER BY records DESC;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.spark_partition_id

// Add partition ID column
val dfWithPartitionId = df.withColumn("partition_id", spark_partition_id())

// Analyze partition distribution
df.select(spark_partition_id().as("partition"))
  .groupBy("partition")
  .count()
  .show()

// Filter data from specific partitions
df.filter(spark_partition_id() < 10)
```

## See Also
- `monotonically_increasing_id()` - For generating unique row identifiers
- `input_file_name()` - For accessing source file information
- Partitioning functions like `hash()` and `pmod()` for custom partitioning logic