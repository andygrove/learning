# SortMergeJoinExec

## Overview
`SortMergeJoinExec` is a physical operator that performs sort-merge joins between two sorted datasets. It leverages the fact that both input sides are already sorted on their join keys to efficiently merge the data streams without requiring hash tables, making it suitable for large datasets that might not fit in memory.

## When Used
The query planner chooses `SortMergeJoinExec` when:
- Both sides of the join can be sorted on their join keys
- The join is not suitable for broadcast join (data is too large)
- Sort-merge join is preferred over shuffle hash join based on cost estimation
- The join involves equi-join conditions on sortable data types
- Configuration allows sort-merge joins (enabled by default)

## Input Requirements
- **Expected input partitioning**: Co-partitioned on join keys (same partitioning scheme)
- **Expected input ordering**: Both children must be sorted on their respective join keys in ascending order
- **Number of children**: Binary operator (exactly 2 children - left and right)

## Output Properties
- **Output partitioning**: Maintains the partitioning of the input data
- **Output ordering**: Depends on join type:
  - Inner joins: Preserves ordering of join keys from both sides
  - Left/Right Outer: Preserves ordering of the streamed side's join keys
  - Full Outer: No guaranteed ordering (empty)
  - Left Existence: Preserves left side ordering
- **Output schema**: Concatenation of left and right schemas (except for semi/anti joins which only output left schema, and existence joins which add a boolean column)

## Algorithm
- **Step 1**: Initialize iterators for both left (streamed) and right (buffered) input partitions
- **Step 2**: Advance the streamed side iterator to find the next row with non-null join keys
- **Step 3**: Compare join keys between current streamed row and buffered rows using sort-merge algorithm
- **Step 4**: Buffer all matching rows from the right side that have the same join keys as the current left row
- **Step 5**: For each buffered match, evaluate additional join conditions and produce output rows
- **Step 6**: Handle unmatched rows according to join type (outer joins emit nulls, anti joins emit unmatched left rows)
- **Step 7**: Continue until both input streams are exhausted

## Memory Usage
- **Spills to disk**: Yes, uses `ExternalAppendOnlyUnsafeRowArray` for buffering matches
- **Memory requirements**: Configurable through multiple thresholds:
  - `spark.sql.sortMergeJoin.exec.buffer.in-memory.threshold` (default based on join type)
  - `spark.sql.sortMergeJoin.exec.buffer.spill.threshold` for row count
  - `spark.sql.sortMergeJoin.exec.buffer.spill.size.threshold` for memory size
- **Buffering behavior**: Buffers rows with matching join keys from the right side; optimized to buffer only first match for certain existence joins

## Partitioning Behavior
- **Data distribution**: Extends `ShuffledJoin`, indicating it requires shuffling to co-partition inputs
- **Shuffle requirements**: Both sides must be shuffled/sorted on join keys unless already properly partitioned and sorted
- **Partition count**: Maintains the same number of partitions as the input

## Supported Join Types
- **Inner**: `InnerLike` - returns matching rows from both sides
- **Left Outer**: Returns all left rows with nulls for unmatched right side
- **Right Outer**: Returns all right rows with nulls for unmatched left side  
- **Full Outer**: Returns all rows from both sides with nulls for unmatched rows
- **Left Semi**: Returns left rows that have matches on the right side
- **Left Anti**: Returns left rows that have no matches on the right side
- **Existence Join**: Returns left rows with additional boolean column indicating existence of match

## Metrics
- **`numOutputRows`**: Total number of output rows produced
- **`spillSize`**: Total size of data spilled to disk during buffering operations

## Code Generation
- **Whole-stage code generation**: Supported with conditions:
  - Full Outer joins: Controlled by `spark.sql.codegen.sort.merge.join.fullOuter.enabled`
  - Existence joins: Controlled by `spark.sql.codegen.sort.merge.join.existence.enabled`  
  - Other join types: Always supported
- **Implementation**: Generates specialized code for different join types with optimized loops and condition checking

## Configuration Options
- `spark.sql.sortMergeJoin.exec.buffer.in-memory.threshold`: In-memory buffer size before spilling
- `spark.sql.sortMergeJoin.exec.buffer.spill.threshold`: Row count threshold for spilling
- `spark.sql.sortMergeJoin.exec.buffer.spill.size.threshold`: Memory size threshold for spilling
- `spark.sql.execution.usePartitionEvaluator`: Whether to use partition evaluator for execution
- `spark.sql.codegen.sort.merge.join.fullOuter.enabled`: Enable codegen for full outer joins
- `spark.sql.codegen.sort.merge.join.existence.enabled`: Enable codegen for existence joins

## Edge Cases
- **Null handling**: Null join keys are treated specially:
  - Inner/Semi joins: Skip rows with null keys
  - Outer/Anti/Existence joins: Emit rows with null keys immediately
- **Empty partition handling**: Gracefully handles empty partitions by processing remaining data from non-empty side
- **Skew handling**: Supports skew join optimization through `isSkewJoin` parameter for handling data skew scenarios

## Examples
```
SortMergeJoin [id#1], [id#2], Inner
:- Sort [id#1 ASC NULLS FIRST], false, 0
:  +- Exchange hashpartitioning(id#1, 200)
:     +- Relation[id#1,name#3] parquet
+- Sort [id#2 ASC NULLS FIRST], false, 0
   +- Exchange hashpartitioning(id#2, 200)
      +- Relation[id#2,value#4] parquet
```

## See Also
- `ShuffledHashJoinExec` - Alternative hash-based join for smaller datasets
- `BroadcastHashJoinExec` - Broadcast join for small datasets
- `SortExec` - Sorts data as prerequisite for sort-merge join
- `ShuffleExchangeExec` - Shuffles data to achieve required partitioning