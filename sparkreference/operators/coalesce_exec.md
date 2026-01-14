# CoalesceExec

## Overview
CoalesceExec is a physical operator that reduces the number of partitions in an RDD by combining adjacent partitions without performing a shuffle. It merges partitions locally on each executor to achieve the target partition count, making it more efficient than shuffle-based repartitioning when reducing partition count.

## When Used
The query planner chooses CoalesceExec when:
- A `coalesce()` operation is explicitly called in user code
- The optimizer determines that reducing partition count would improve performance
- When consolidating small partitions after filtering operations that significantly reduce data size
- As an alternative to `ShuffleExchange` when shuffle overhead outweighs parallel execution benefits

## Input Requirements
- **Expected input partitioning**: Any partitioning scheme (no specific requirements)
- **Expected input ordering**: No ordering requirements (preserves existing ordering within merged partitions)
- **Number of children**: Unary operator (exactly one child)

## Output Properties
- **Output partitioning**: 
  - `SinglePartition` when `numPartitions == 1`
  - `UnknownPartitioning(numPartitions)` for all other cases
- **Output ordering**: Inherits ordering from child within each coalesced partition
- **How output schema is derived**: Directly passes through child's output schema (`child.output`)

## Algorithm
- Executes the child plan to obtain the input RDD
- Checks if target is 1 partition and input has 0 partitions - creates `EmptyRDDWithPartitions` to ensure consistent partitioning guarantees
- Calls `rdd.coalesce(numPartitions, shuffle = false)` on the input RDD
- The coalesce operation groups adjacent partitions together on the same executor
- Each output partition is formed by concatenating multiple input partitions
- No data movement across network occurs (shuffle = false)
- Maintains data locality by keeping merged partitions on the same executor

## Memory Usage
- **Does it spill to disk?**: No, CoalesceExec does not spill to disk
- **Memory requirements**: Minimal additional memory overhead beyond storing partition data
- **Buffering behavior**: No explicit buffering - processes data as streaming concatenation of input partitions

## Partitioning Behavior
- **How it affects data distribution**: Reduces partition count by merging adjacent partitions, potentially creating uneven partition sizes
- **Shuffle requirements**: None - explicitly avoids shuffling (`shuffle = false`)
- **Partition count changes**: Always reduces from input partition count to `numPartitions` (target count)

## Supported Join/Aggregation Types
Not applicable - CoalesceExec is a repartitioning operator, not a join or aggregation operator.

## Metrics
CoalesceExec typically reports these SQL metrics:
- Number of output rows
- Data size output
- Time spent in operator execution
- Number of output partitions

## Code Generation
CoalesceExec does not support whole-stage code generation as it primarily performs RDD-level partition management rather than row-by-row processing that benefits from codegen.

## Configuration Options
- `spark.sql.adaptive.coalescePartitions.enabled`: Enables adaptive query execution to automatically coalesce partitions
- `spark.sql.adaptive.advisoryPartitionSizeInBytes`: Target size for partitions after coalescing
- `spark.sql.adaptive.coalescePartitions.minPartitionSize`: Minimum partition size threshold for coalescing

## Edge Cases
- **Null handling**: Transparent - nulls are preserved as-is during partition merging
- **Empty partition handling**: Creates `EmptyRDDWithPartitions` when target is 1 partition but input has 0 partitions to maintain `SinglePartition` contract
- **Skew handling**: Can worsen skew since it merges adjacent partitions without considering data size distribution

## Examples
```
== Physical Plan ==
CoalesceExec(1)
+- *(1) Project [id#0, name#1]
   +- *(1) Filter (id#0 > 100)
      +- FileScan parquet [id#0,name#1] ...
```

```sql
-- SQL that generates CoalesceExec
SELECT * FROM table WHERE id > 100 
-- Followed by .coalesce(1) in DataFrame API
```

## See Also
- **ShuffleExchangeExec**: Alternative for repartitioning that uses shuffle for even distribution
- **RepartitionByExpressionExec**: Hash-based repartitioning by expressions
- **UnionExec**: Combines multiple plans without changing partitioning