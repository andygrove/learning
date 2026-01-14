# WindowGroupLimitExec

## Overview
WindowGroupLimitExec is a physical operator that efficiently limits the number of rows per partition based on window ranking functions (RowNumber, Rank, or DenseRank). It optimizes queries with ranking window functions followed by filters on rank values by applying the limit early in the execution pipeline, reducing the amount of data processed in downstream operations.

## When Used
The query planner chooses this operator when optimizing queries that contain:
- Window functions with ranking operations (ROW_NUMBER(), RANK(), DENSE_RANK())
- A filter condition on the ranking result with a numeric limit
- The optimizer determines that early filtering will significantly reduce data volume
- The query pattern matches `SELECT * FROM (SELECT *, ROW_NUMBER() OVER (...) as rn FROM table) WHERE rn <= N`

## Input Requirements
- **Expected input partitioning**: Depends on mode - Partial mode accepts any partitioning, Final mode requires ClusteredDistribution on partition columns (or AllTuples if no partitioning)
- **Expected input ordering**: Requires sorting by partition columns (ascending) followed by the window order specification
- **Number of children**: Unary operator (single child SparkPlan)

## Output Properties
- **Output partitioning**: Preserves the child's output partitioning unchanged
- **Output ordering**: Inherits the child's output ordering without modification
- **How output schema is derived**: Output schema is identical to the input schema (child.output) - no additional columns are added

## Algorithm
• **Partition Processing**: Processes input data partition by partition, maintaining partition boundaries defined by partitionSpec
• **Ranking Computation**: Applies the specified ranking function (RowNumber/Rank/DenseRank) to rows within each partition according to orderSpec
• **Early Termination**: For each partition group, stops processing and outputting rows once the ranking value exceeds the specified limit
• **Evaluator Selection**: Uses either partition evaluator (if enabled via configuration) or falls back to indexed partition mapping
• **Memory Efficiency**: Processes rows in streaming fashion without materializing entire partitions in memory
• **Metrics Tracking**: Counts output rows using the numOutputRows metric for monitoring and debugging
• **Two-Phase Execution**: Supports both Partial and Final modes for distributed execution across shuffle boundaries

## Memory Usage
- **Does it spill to disk?**: No, this operator does not spill to disk as it processes data in streaming fashion
- **Memory requirements/configuration**: Minimal memory footprint - only requires memory for the current row being processed and ranking state
- **Buffering behavior**: No buffering required since ranking functions can be computed incrementally and early termination prevents unnecessary data accumulation

## Partitioning Behavior
- **How it affects data distribution**: Does not change data distribution - preserves input partitioning scheme
- **Shuffle requirements**: Final mode may require shuffle to achieve ClusteredDistribution on partition columns, Partial mode requires no additional shuffling
- **Partition count changes**: Maintains the same number of partitions as input, though individual partitions may become smaller due to row filtering

## Supported Join/Aggregation Types
Not applicable - this operator handles window function optimization, not joins or aggregations.

## Metrics
- **numOutputRows**: Tracks the total number of rows output across all partitions, useful for understanding the effectiveness of the limit optimization

## Code Generation
This operator does not appear to support whole-stage code generation based on the source code. It relies on evaluator factories and runtime row processing rather than generated code.

## Configuration Options
- **spark.sql.execution.usePartitionEvaluator**: Controls whether to use partition evaluator for processing (newer approach) or fall back to indexed partition mapping
- Window-related configuration options that affect the underlying ranking function evaluation

## Edge Cases
- **Null handling**: Relies on the underlying ranking function's null handling behavior, typically treating nulls according to the specified sort order
- **Empty partition handling**: Gracefully handles empty partitions by producing no output rows for those partitions
- **Skew handling**: Not specifically designed for skew handling, but the early termination can help with partitions that have many rows in lower-ranked groups

## Examples
```
*(5) WindowGroupLimitExec [id#1], [score#2 DESC NULLS LAST], row_number(), 10, Final
+- *(4) Sort [id#1 ASC NULLS FIRST, score#2 DESC NULLS LAST], false, 0
   +- Exchange hashpartitioning(id#1, 200), ENSURE_REQUIREMENTS, [id=#123]
      +- *(3) WindowGroupLimitExec [id#1], [score#2 DESC NULLS LAST], row_number(), 10, Partial
         +- *(2) Sort [id#1 ASC NULLS FIRST, score#2 DESC NULLS LAST], false, 0
```

## See Also
- **WindowExec**: Full window function execution when optimization is not applicable
- **SortExec**: Often appears before WindowGroupLimitExec to satisfy ordering requirements  
- **GlobalLimitExec**: For global row limits without partitioning considerations