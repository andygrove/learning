# BroadcastExchangeExec

## Overview
The `BroadcastExchangeExec` operator collects data from its child plan, transforms it into a broadcast-optimized format, and distributes it to all executors in the cluster. This operator enables broadcast joins by making small tables available locally on every executor, eliminating the need for shuffling during join operations.

## When Used
The query planner selects this operator when:
- A table is small enough to be broadcast (under `spark.sql.adaptiveExecutionEnabled` or explicit broadcast hints)
- The table size is below `spark.sql.autoBroadcastJoinThreshold` (default 10MB)
- A broadcast join strategy is chosen over shuffle-based joins
- The `broadcast()` hint is explicitly used in the query

## Input Requirements
- **Expected input partitioning**: Any partitioning (will be collected to driver)
- **Expected input ordering**: No specific ordering requirements
- **Number of children**: Unary operator (exactly one child)

## Output Properties
- **Output partitioning**: `BroadcastPartitioning(mode)` where mode defines the broadcast strategy
- **Output ordering**: Not applicable (broadcast data doesn't have traditional ordering)
- **Output schema**: Identical to child's output schema

## Algorithm
- **Data Collection**: Executes `child.executeCollectIterator()` to gather all data to the driver
- **Row Count Validation**: Checks if row count exceeds `maxBroadcastRows` limit (varies by broadcast mode)
- **Data Transformation**: Applies `mode.transform()` to convert data into broadcast-optimized format (e.g., `HashedRelation`)
- **Size Validation**: Verifies transformed data size is under `spark.sql.maxBroadcastTableSizeInBytes`
- **Broadcasting**: Uses `sparkContext.broadcastInternal()` with `serializedOnly = true` to distribute data
- **Promise Completion**: Fulfills the completion promise to signal availability to waiting operations
- **Metrics Update**: Posts driver metrics including collect time, build time, and broadcast time

## Memory Usage
- **Spill behavior**: Does not spill to disk; fails if data doesn't fit in memory
- **Memory requirements**: Must fit entire dataset plus transformed representation in driver memory
- **Buffering**: Temporarily holds both original collected data and transformed broadcast format
- **Configuration**: Limited by `spark.sql.maxBroadcastTableSizeInBytes` (default 8GB)

## Partitioning Behavior
- **Data distribution**: Replicates entire dataset to all executors
- **Shuffle requirements**: Eliminates shuffle need in downstream join operations
- **Partition changes**: Transforms from N input partitions to broadcast distribution across all executors

## Supported Join/Aggregation Types
This operator supports broadcast modes for:
- **Inner joins**: Most common usage with `HashedRelationBroadcastMode`
- **Left/Right outer joins**: When the broadcasted side is the build side
- **Semi/Anti joins**: Broadcasting the filtering relation
- **Cross joins**: Broadcasting one side for Cartesian products

## Metrics
- **dataSize**: Total size in bytes of the broadcast data
- **numOutputRows**: Number of rows in the broadcast relation
- **collectTime**: Time spent collecting data from child executors to driver
- **buildTime**: Time spent transforming collected data into broadcast format
- **broadcastTime**: Time spent broadcasting the data to all executors

## Code Generation
This operator does not support whole-stage code generation as it's an exchange operator that materializes data rather than processing it row-by-row in a pipeline.

## Configuration Options
- `spark.sql.broadcastTimeout`: Timeout for broadcast operations (default 300s)
- `spark.sql.maxBroadcastTableSizeInBytes`: Maximum size for broadcast tables (default 8GB)
- `spark.sql.autoBroadcastJoinThreshold`: Threshold for automatic broadcast join selection (default 10MB)
- `spark.serializer`: Affects broadcast serialization performance

## Edge Cases
- **Row limit enforcement**: Throws `QueryExecutionErrors.cannotBroadcastTableOverMaxTableRowsError` when exceeding `maxBroadcastRows`
- **Size limit enforcement**: Fails if transformed data exceeds `maxBroadcastTableSizeInBytes`
- **OutOfMemoryError handling**: Wraps OOM errors with context about source tables
- **Timeout handling**: Cancels broadcast job and related operations on timeout
- **Non-resettable metrics**: Metrics are not reset after materialization to preserve broadcast job statistics

## Examples
```
== Physical Plan ==
BroadcastHashJoin [id#1], [small_id#5], Inner, BuildRight, false
:- *(1) FileScan parquet [id#1, name#2] 
+- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, false]),false), [id=#15]
   +- *(2) FileScan parquet [small_id#5, value#6]
```

## See Also
- `BroadcastHashJoinExec`: Primary consumer of broadcast exchanges
- `HashedRelationBroadcastMode`: Common broadcast transformation mode
- `BroadcastNestedLoopJoinExec`: Alternative broadcast join implementation