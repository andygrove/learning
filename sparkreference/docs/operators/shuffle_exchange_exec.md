# ShuffleExchangeExec

## Overview
ShuffleExchangeExec performs a shuffle operation to redistribute data across partitions according to a desired partitioning scheme. It creates a shuffle dependency that writes data from the input partitions and makes it available for reading by downstream operators with the target partitioning. This operator is fundamental to achieving data locality requirements for joins, aggregations, and other operations that need specific data distribution patterns.

## When Used
The query planner inserts ShuffleExchangeExec when:
- Child operator's output partitioning doesn't match the required partitioning for downstream operations
- Sort-merge joins need co-partitioned inputs on join keys
- Hash-based aggregations require grouping keys to be co-located
- Window operations need data partitioned by window partition keys
- The `shuffleOrigin` indicates requirements from stateful operators or general requirement enforcement

## Input Requirements
- **Expected input partitioning**: Any partitioning scheme (will be reshuffled regardless)
- **Expected input ordering**: No specific ordering required (ordering may be lost during shuffle)
- **Number of children**: Unary operator (exactly one child SparkPlan)

## Output Properties
- **Output partitioning**: Specified by the `outputPartitioning` parameter passed to constructor
- **Output ordering**: No guaranteed ordering (shuffle typically destroys input ordering)
- **Output schema**: Identical to child's output schema - no schema transformation occurs

## Algorithm
- Creates a `ShuffleDependency` using `prepareShuffleDependency` with input RDD, output schema, target partitioning, and UnsafeRowSerializer
- Configures write metrics for tracking shuffle write performance (bytes written, records written, write time)
- During execution, writes data to shuffle files using the partitioner defined by target partitioning scheme
- Returns a `ShuffledRowRDD` that reads from the shuffle files when downstream operators request data
- Supports Adaptive Query Execution (AQE) by providing `mapOutputStatisticsFuture` for runtime optimization decisions
- Updates SQL metrics including data size, number of partitions, and various read/write statistics
- Handles empty partitions by returning successful null future when input has zero partitions

## Memory Usage
- **Spill behavior**: Uses Spark's shuffle writer which spills to disk when memory buffers are full
- **Memory requirements**: Controlled by `spark.sql.shuffle.partitions` and shuffle-related memory configs
- **Buffering**: Buffers data in memory during shuffle write phase, with spillable sort-based shuffle writer

## Partitioning Behavior
- **Data distribution**: Redistributes all data according to the target partitioning scheme (hash, range, round-robin, etc.)
- **Shuffle requirements**: Always requires a shuffle operation - this is the primary shuffle-introducing operator
- **Partition count changes**: Output partition count determined by `outputPartitioning.numPartitions`, can increase or decrease from input

## Supported Join/Aggregation Types
Not directly applicable - ShuffleExchangeExec is a data movement operator that enables other operators to perform their operations on properly partitioned data. It supports the partitioning requirements for all join types (inner, left, right, full, semi, anti, cross) and aggregation patterns.

## Metrics
- **dataSize**: Total bytes of data shuffled
- **numPartitions**: Number of output partitions created
- **shuffle records written**: Number of records written during shuffle
- **shuffle write time**: Time spent writing shuffle data
- **shuffle bytes written**: Bytes written to shuffle files
- **shuffle records read**: Number of records read from shuffle
- **shuffle read time**: Time spent reading shuffle data
- **shuffle bytes read**: Bytes read from shuffle files

## Code Generation
ShuffleExchangeExec does not participate in whole-stage code generation as it represents a shuffle boundary. Code generation stages are broken at shuffle operators, with separate code-generated stages before and after the shuffle.

## Configuration Options
- `spark.sql.shuffle.partitions`: Default number of partitions for shuffles (200)
- `spark.sql.adaptive.enabled`: Enables adaptive query execution for runtime shuffle optimization
- `spark.sql.adaptive.advisoryPartitionSizeInBytes`: Target partition size for AQE
- `spark.serializer`: Serializer for shuffle data (uses UnsafeRowSerializer internally)
- `spark.sql.shuffle.checksum.enabled`: Enable checksums for shuffle data integrity

## Edge Cases
- **Empty partitions**: Handles zero input partitions by returning successful null `mapOutputStatisticsFuture`
- **Null handling**: Preserves nulls during shuffle using UnsafeRowSerializer which handles null values correctly
- **Skew handling**: Relies on the partitioning scheme (hash partitioning may create skew, range partitioning attempts to balance)
- **Serialization**: Uses UnsafeRowSerializer which requires fixed schema and doesn't support complex nested types with variable schemas

## Examples
```
Exchange hashpartitioning(customer_id#123, 200), ENSURE_REQUIREMENTS
+- LocalTableScan [customer_id#123, order_total#124]

Exchange rangepartitioning(order_date#125 ASC NULLS FIRST, 200), ENSURE_REQUIREMENTS  
+- Filter (order_total#124 > 100.0)
   +- Scan parquet orders[order_date#125, order_total#124]
```

## See Also
- **ShuffledRowRDD**: The RDD implementation returned by this operator
- **BroadcastExchangeExec**: Alternative data movement operator using broadcast instead of shuffle
- **SortMergeJoinExec**: Common downstream operator requiring co-partitioned inputs
- **HashAggregateExec**: Aggregation operator that may require shuffled input