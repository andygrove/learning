# MergingSessionsExec

## Overview
MergingSessionsExec is a physical aggregation operator that merges session windows while simultaneously applying aggregations on the merged windows. It is a variant of SortAggregateExec optimized for session window processing, eliminating the need to buffer inputs by leveraging pre-sorted input data ordered by group keys and session window start time.

## When Used
The query planner chooses this operator for session window aggregations when:
- Processing session windows that need to be merged based on gap conditions
- Input data can be pre-sorted by grouping keys plus session window start time
- The optimizer determines that merging sessions locally before shuffling will be beneficial
- Both streaming and batch processing scenarios with session window functions

## Input Requirements
- **Expected input partitioning**: Configurable via `requiredChildDistributionExpressions` parameter
- **Expected input ordering**: Group keys (excluding session expression) followed by session expression, all in ascending order
- **Number of children**: Unary operator (single child SparkPlan)
- Input must be sortable by the combination of grouping expressions and session window specification

## Output Properties
- **Output partitioning**: Inherits the child's output partitioning characteristics
- **Output ordering**: Preserves the child's output ordering (`child.outputOrdering`)
- **Output schema**: Identical to child's output schema (`child.output`), maintaining the same attribute structure

## Algorithm
- Receives pre-sorted input partitions ordered by group keys and session window start time
- Creates `MergingSessionsIterator` for each partition to handle the actual merging logic
- Processes rows sequentially, merging overlapping or adjacent session windows based on gap conditions
- Applies aggregate functions directly on merged windows without intermediate buffering
- Handles empty partitions specially: returns empty iterator for grouped aggregates, single row for non-grouped
- Updates `numOutputRows` metric as rows are produced
- Uses `MutableProjection` for efficient row transformations during processing

## Memory Usage
- **Spill behavior**: Does not explicitly spill to disk; relies on iterator-based processing
- **Memory requirements**: Minimal buffering since it processes rows in streaming fashion
- **Buffering behavior**: Eliminates necessity of buffering inputs by leveraging pre-sorted data and direct aggregation on merged windows

## Partitioning Behavior
- **Data distribution**: Controlled by `requiredChildDistributionExpressions` and `numShufflePartitions` parameters
- **Shuffle requirements**: Optional shuffling based on constructor parameters; setting both to None avoids shuffle
- **Partition count**: May change based on `numShufflePartitions` setting; local partition sorting always occurs

## Supported Join/Aggregation Types
This operator specifically handles aggregation types:
- Session window aggregations with merging capabilities
- Supports all standard aggregate functions (sum, count, avg, min, max, etc.) via `aggregateExpressions`
- Works with both grouped and non-grouped aggregations
- Handles complex aggregation expressions through `AggregateExpression` instances

## Metrics
- **numOutputRows**: SQLMetric tracking the total number of rows produced by the operator
- Metrics are updated incrementally as the `MergingSessionsIterator` produces output rows
- Essential for monitoring session window aggregation performance

## Code Generation
The source code does not show explicit whole-stage code generation support. The operator relies on `MergingSessionsIterator` and `MutableProjection` for row processing, with code generation likely handled at the projection level.

## Configuration Options
- **requiredChildDistributionExpressions**: Controls data distribution requirements before processing
- **numShufflePartitions**: Determines partition count for shuffle operations
- **isStreaming**: Boolean flag indicating streaming vs batch processing mode
- Standard Spark SQL aggregation configurations apply to the underlying aggregate expressions

## Edge Cases
- **Empty partitions with grouping**: Returns empty iterator when no input exists and grouping expressions are present
- **Empty partitions without grouping**: Produces single output row via `outputForEmptyGroupingKeyWithoutInput()`
- **Null handling**: Handled through underlying aggregate expressions and projection mechanisms
- **Iterator state**: Carefully checks `iter.hasNext` before creating aggregation iterator to handle empty inputs

## Examples
```
== Physical Plan ==
*(3) MergingSessionsExec
  requiredChildDistributionExpressions: [user_id]
  groupingExpressions: [user_id, session_window]
  sessionExpression: session_window
  aggregateExpressions: [sum(amount), count(*)]
  +- Sort [user_id ASC NULLS FIRST, session_window ASC NULLS FIRST]
     +- Exchange hashpartitioning(user_id, 200)
        +- *(1) Project [user_id, session_window(timestamp, interval 30 minutes), amount]
```

## See Also
- **BaseAggregateExec**: Parent class providing common aggregation functionality
- **SortAggregateExec**: Standard sort-based aggregation operator that this extends
- **MergingSessionsIterator**: Core iterator implementation handling the merging logic
- **HashAggregateExec**: Hash-based aggregation alternative for non-session scenarios