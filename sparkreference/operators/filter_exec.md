# FilterExec

## Overview
FilterExec is a physical operator that filters rows based on a predicate condition. It evaluates the filter condition against each input row and only passes through rows that satisfy the condition, while also optimizing null-handling by separating `IsNotNull` predicates from other conditions.

## When Used
The query planner chooses FilterExec when:
- A `WHERE` clause is present in a SQL query
- Filter conditions exist in subqueries or views
- Predicate pushdown optimizations place filters close to data sources
- Join conditions contain additional filter predicates beyond equi-join conditions

## Input Requirements
- **Expected input partitioning**: No specific partitioning requirements - accepts any partitioning scheme
- **Expected input ordering**: No ordering requirements - preserves input ordering
- **Number of children**: Unary operator (exactly one child operator)

## Output Properties
- **Output partitioning**: Preserves the child's output partitioning unchanged
- **Output ordering**: Maintains the child's output ordering since filtering doesn't reorder rows
- **How output schema is derived**: Output schema matches child schema but with improved nullability - attributes filtered by `IsNotNull` predicates are marked as non-nullable

## Algorithm
- Split the filter condition into `IsNotNull` predicates and other predicates for optimization
- Identify attributes that become non-nullable due to `IsNotNull` filtering
- Generate optimized predicate evaluation code that takes advantage of short-circuiting
- For each input row, evaluate `IsNotNull` predicates first, then other predicates
- Mark previously nullable columns as non-null in the output for downstream optimization
- Increment the `numOutputRows` metric for rows that pass the filter
- Pass qualifying rows to the parent operator in the execution tree

## Memory Usage
- **Does it spill to disk?**: No, FilterExec does not spill to disk
- **Memory requirements/configuration**: Minimal memory usage - only holds temporary variables for predicate evaluation
- **Buffering behavior**: No buffering - processes rows in a streaming fashion one at a time

## Partitioning Behavior
- **How it affects data distribution**: May create uneven partition sizes if filter selectivity varies across partitions
- **Shuffle requirements**: No shuffle required - filter operates locally within each partition
- **Partition count changes**: Partition count remains unchanged, though some partitions may become empty

## Supported Join/Aggregation Types
Not applicable - FilterExec is a selection operator, not a join or aggregation operator.

## Metrics
- **numOutputRows**: Tracks the total number of rows that pass the filter condition and are output to the next operator

## Code Generation
Yes, FilterExec implements `CodegenSupport` and participates in whole-stage code generation. It generates optimized Java code for predicate evaluation and integrates seamlessly with code generation from child and parent operators.

## Configuration Options
- **spark.sql.execution.usePartitionEvaluator**: Controls whether to use partition evaluators (`mapPartitionsWithEvaluator`) or the legacy `mapPartitionsWithIndexInternal` approach
- Standard predicate evaluation configurations that affect expression evaluation performance

## Edge Cases
- **Null handling**: `IsNotNull` predicates are separated and evaluated first for optimization; null values in other predicates follow SQL three-valued logic
- **Empty partition handling**: Empty partitions pass through unchanged without creating additional overhead
- **Skew handling**: Not applicable at the operator level, but uneven filter selectivity can create downstream skew issues

## Examples
```
== Physical Plan ==
*(2) Project [id#1L, name#2]
+- *(2) Filter ((isnotnull(age#3) AND (age#3 > 25)) AND isnotnull(id#1L))
   +- *(2) ColumnarToRow
      +- FileScan parquet [id#1L,name#2,age#3]
```

## See Also
- **ProjectExec**: Often paired with FilterExec for column pruning and row filtering
- **SortExec**: May follow FilterExec when ordering is required on filtered results  
- **FileSourceScanExec**: Frequently has FilterExec as a direct child when predicate pushdown occurs
- **BroadcastHashJoinExec**: Often uses FilterExec for additional join conditions beyond equi-join predicates