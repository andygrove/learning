# ExpandExec

## Overview
The ExpandExec operator applies multiple sets of projection expressions to every input row, producing multiple output rows for each input row. It is primarily used to implement GROUPING SETS, ROLLUP, and CUBE operations by expanding each input row into multiple rows with different grouping combinations.

## When Used
The query planner chooses ExpandExec when executing SQL queries with:
- `GROUP BY ... GROUPING SETS` clauses
- `GROUP BY ... ROLLUP` clauses  
- `GROUP BY ... CUBE` clauses
- Any operation requiring multiple projections of the same input row with different grouping expressions

## Input Requirements
- **Expected input partitioning**: Any partitioning scheme (no specific requirements)
- **Expected input ordering**: No ordering requirements
- **Number of children**: Unary operator (exactly one child)

## Output Properties
- **Output partitioning**: `UnknownPartitioning(0)` - the operator produces arbitrary partitioning due to row expansion
- **Output ordering**: No guaranteed output ordering
- **Output schema**: Derived from the `output` parameter, which must match the schema produced by all projection expressions

## Algorithm
- For each input row, iterate through all projection expression sets in the `projections` parameter
- Apply each projection set to the input row using `UnsafeProjection.create()`
- Generate one output row per projection set, effectively multiplying the number of rows
- Use an internal iterator that tracks current projection index (`idx`) and input row state
- Initialize all projections with partition index for proper code generation
- Reset projection index when all projections for current input are exhausted and more input exists
- Increment the `numOutputRows` metric for each generated output row

## Memory Usage
- **Disk spilling**: No, this operator does not spill to disk
- **Memory requirements**: Minimal - only stores current input row and projection results
- **Buffering behavior**: No buffering - processes one input row at a time in streaming fashion

## Partitioning Behavior
- **Data distribution**: Destroys input partitioning by expanding rows, resulting in unknown partitioning
- **Shuffle requirements**: No shuffle required by this operator itself
- **Partition count**: Maintains same number of partitions as input, but data distribution becomes unpredictable

## Supported Join/Aggregation Types
Not applicable - ExpandExec is a projection operator, not a join or aggregation operator.

## Metrics
- **numOutputRows**: Counts the total number of output rows produced (will be input rows × number of projections)

## Code Generation
Yes, implements `CodegenSupport` with whole-stage code generation:
- Generates optimized code that declares variables for each output column
- Uses switch/case statements to efficiently compute different projections
- Optimizes by computing constant expressions only once when they're the same across all projections
- Includes method splitting when generated code exceeds `spark.sql.codegen.methodSplitThreshold`
- Sets `needCopyResult = true` to ensure proper memory management

## Configuration Options
- **spark.sql.codegen.methodSplitThreshold**: Controls when generated code is split into separate methods to avoid JVM method size limits

## Edge Cases
- **Null handling**: Properly propagates nulls through projection expressions using generated null-checking code
- **Empty partition handling**: Gracefully handles empty input partitions by producing no output
- **Large projection sets**: Automatically splits generated code when threshold is exceeded to prevent compilation issues

## Examples
```
== Physical Plan ==
*(2) HashAggregate(keys=[col1#1, spark_grouping_id#4], functions=[count(1)])
+- Exchange hashpartitioning(col1#1, spark_grouping_id#4, 200)
   +- *(1) HashAggregate(keys=[col1#1, spark_grouping_id#4], functions=[partial_count(1)])
      +- *(1) Expand [List(col1#1, 0), List(null, 1)], [col1#1, spark_grouping_id#4]
         +- *(1) Project [col1#1]
            +- *(1) FileScan parquet [col1#1]
```

## See Also
- **HashAggregateExec**: Often follows ExpandExec to perform grouping operations
- **ProjectExec**: Similar projection functionality but for single projection sets
- **GenerateExec**: Another row-expanding operator for table-valued functions