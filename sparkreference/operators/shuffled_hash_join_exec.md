# ShuffledHashJoinExec

## Overview
ShuffledHashJoinExec performs a hash join of two child relations by first shuffling the data using the join keys. It builds an in-memory hash table from the smaller relation (build side) and probes it with records from the larger relation (stream side) to find matching rows.

## When Used
The query planner chooses this operator when:
- A hash join is preferred over sort-merge join based on cost estimation
- The build side relation is estimated to fit in memory
- Both relations need to be shuffled (neither has the required partitioning on join keys)
- Configuration `spark.sql.join.preferSortMergeJoin` is disabled
- The join condition contains equi-join predicates suitable for hash-based lookup

## Input Requirements
- **Expected input partitioning**: HashPartitioning on join keys for both children
- **Expected input ordering**: No specific ordering required
- **Number of children**: Binary operator (requires exactly two child relations)
- **Join keys**: Must be hashable and support equality comparison

## Output Properties
- **Output partitioning**: Inherits HashPartitioning from input children based on join keys
- **Output ordering**: No guaranteed output ordering (hash join does not preserve order)
- **Output schema**: Derived by combining schemas of left and right children, with appropriate column pruning based on join type

## Algorithm
- Consume all records from the build side (smaller relation) during the open() phase
- Build an in-memory hash table using join key values as keys and matching rows as values
- For each input row from the stream side, compute hash of join keys
- Probe the hash table to find matching build-side rows
- Apply additional join conditions (non-equi predicates) if present
- Generate joined output rows based on join type semantics
- Handle null values in join keys according to join type requirements

## Memory Usage
- **Spill behavior**: Does not spill to disk - entire build side must fit in memory
- **Memory requirements**: Build side dataset must fit within available executor memory
- **Buffering**: Buffers entire build-side relation in memory using OpenHashSet/BitSet collections
- **Memory pressure**: Will fail with OOM if build side exceeds available memory

## Partitioning Behavior
- **Data distribution**: Requires shuffle of both input relations on join keys
- **Shuffle requirements**: Uses HashPartitioner to co-locate matching join keys
- **Partition count**: Typically maintains same partition count as configured by `spark.sql.shuffle.partitions`

## Supported Join Types
- **Inner joins**: Returns rows with matching keys in both relations
- **Left outer joins**: Returns all left rows, with nulls for non-matching right rows
- **Right outer joins**: Returns all right rows, with nulls for non-matching left rows
- **Full outer joins**: Returns all rows from both sides with nulls for non-matches
- **Left semi joins**: Returns left rows that have matches in right relation
- **Left anti joins**: Returns left rows that have no matches in right relation

## Metrics
- **numOutputRows**: Total number of rows produced by the join
- **buildDataSize**: Size in bytes of the build-side hash table
- **buildTime**: Time spent building the hash table
- **joinTime**: Time spent probing and generating output rows

## Code Generation
Supports whole-stage code generation when enabled. Generated code eliminates virtual function calls and optimizes the probe phase with inlined hash table lookups and row construction.

## Configuration Options
- `spark.sql.join.preferSortMergeJoin`: When false, increases likelihood of choosing hash join
- `spark.sql.shuffle.partitions`: Controls number of shuffle partitions
- `spark.sql.adaptive.enabled`: Enables adaptive query execution which may switch join strategies
- `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold`: Threshold for using local hash join

## Edge Cases
- **Null handling**: Null join keys never match (treated as not equal to anything including other nulls)
- **Empty partitions**: Gracefully handles empty partitions on either build or stream side
- **Memory pressure**: No built-in skew handling - relies on proper partitioning of join keys
- **Build side overflow**: Fails with OutOfMemoryError if build side exceeds available memory

## Examples
```
*(5) Project [id#0, name#1, dept_id#2, dept_name#5]
+- ShuffledHashJoin [dept_id#2], [id#4], Inner, BuildRight
   :- Exchange hashpartitioning(dept_id#2, 200)
   :  +- FileScan parquet [id#0,name#1,dept_id#2]
   +- Exchange hashpartitioning(id#4, 200)
      +- FileScan parquet [id#4,dept_name#5]
```

## See Also
- `SortMergeJoinExec`: Alternative join strategy that spills to disk
- `BroadcastHashJoinExec`: Hash join without shuffle when one side is small
- `CartesianProductExec`: For cross joins without equi-join conditions