# BroadcastHashJoinExec

## Overview

BroadcastHashJoinExec performs hash joins by broadcasting the smaller relation to all executor nodes and avoiding shuffles of the streamed relation. It builds a hash table from the broadcast relation and probes it with rows from the streamed relation, supporting all join types including specialized null-aware anti joins.

## When Used

The query planner chooses this operator when:
- One side of the join is small enough to broadcast (controlled by `spark.sql.autoBroadcastJoinThreshold`)
- The join has equi-join conditions that can be used as hash keys
- The cost-based optimizer determines broadcasting is more efficient than shuffle-based joins
- For null-aware anti joins when specifically optimized conditions are met (single key, BuildRight, LeftAnti type)

## Input Requirements

- **Expected input partitioning**: Build side requires `BroadcastDistribution` with `HashedRelationBroadcastMode`, streamed side has `UnspecifiedDistribution`
- **Expected input ordering**: No specific ordering requirements
- **Number of children**: Binary operator (exactly two child plans - left and right)

## Output Properties

- **Output partitioning**: For inner-like joins, may expand the streamed plan's partitioning by substituting streamed keys with build keys (up to `broadcastHashJoinOutputPartitioningExpandLimit`). Other join types preserve streamed plan's partitioning.
- **Output ordering**: Inherits from streamed side
- **How output schema is derived**: Combines columns from both sides based on join type (inner includes all, outer includes nulls for non-matching side, semi/anti only include streamed side columns)

## Algorithm

- Asynchronously broadcast the build-side relation as a `HashedRelation` hash table
- For each partition of the streamed relation, obtain a read-only copy of the broadcast hash table
- Generate hash keys from streamed rows using `streamSideKeyGenerator`
- Probe the hash table with each streamed key to find matches
- For null-aware anti joins, handle three special cases: empty build relation, all-null keys, and null key filtering
- Apply additional join conditions if specified beyond the equi-join keys
- Track peak execution memory usage from the broadcast hash table size

## Memory Usage

- **Does it spill to disk?**: No, the broadcast relation must fit entirely in memory on each executor
- **Memory requirements/configuration**: Limited by `spark.sql.autoBroadcastJoinThreshold` (default 10MB) and available executor memory
- **Buffering behavior**: Each task gets a read-only copy of the broadcast hash table loaded into memory

## Partitioning Behavior

- **How it affects data distribution**: Streamed side maintains its original partitioning, no shuffle required
- **Shuffle requirements**: Only the build side is shuffled once to the driver for broadcasting
- **Partition count changes**: Output has same partition count as streamed side

## Supported Join/Aggregation Types

Supports all join types:
- **Inner**: Returns matching rows from both sides
- **Left Outer**: All left rows plus matches, nulls for non-matching right
- **Right Outer**: All right rows plus matches, nulls for non-matching left  
- **Full Outer**: All rows from both sides, nulls for non-matches
- **Left Semi**: Left rows that have matches on right side
- **Left Anti**: Left rows that have no matches on right side (including null-aware variant)
- **Cross**: Cartesian product (when no join keys specified)

## Metrics

- **numOutputRows**: Count of result rows produced by the join operation

## Code Generation

Yes, supports whole-stage code generation through `CodegenSupport` interface. Generates specialized code for:
- Key generation and hash probing
- Null-aware anti join optimizations with compile-time broadcast relation inspection
- Efficient row copying based on `needCopyResult` analysis

## Configuration Options

- `spark.sql.autoBroadcastJoinThreshold`: Maximum size for broadcast relations (default 10MB)
- `spark.sql.adaptive.coalescePartitions.enabled`: May affect streamed side partitioning
- `spark.sql.broadcastHashJoin.outputPartitioningExpandLimit`: Controls output partitioning expansion for inner joins (default value enables expansion)

## Edge Cases

- **Null handling**: Null keys in equi-join conditions don't match (except null-aware anti join). Null-aware anti join has special logic for all-null keys and empty relations.
- **Empty partition handling**: Empty partitions on streamed side produce no output. Empty broadcast relation handled efficiently in null-aware anti join.
- **Skew handling**: No built-in skew mitigation - relies on broadcast eliminating shuffle-induced skew

## Examples

```
BroadcastHashJoin [id#1], [id#2], Inner, BuildRight, false
:- LocalTableScan [id#1, name#3]
+- BroadcastExchange HashedRelationBroadcastMode(List(input[0, int, false]),false)
   +- LocalTableScan [id#2, value#4]
```

## See Also

- **SortMergeJoinExec**: Alternative for larger relations requiring shuffle
- **ShuffledHashJoinExec**: Hash join with shuffle when broadcast not feasible
- **BroadcastExchangeExec**: Handles the broadcasting mechanism
- **HashedRelation**: The broadcast hash table data structure