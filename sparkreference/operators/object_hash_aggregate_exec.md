# ObjectHashAggregateExec

## Overview
ObjectHashAggregateExec is a hash-based aggregate operator that supports `TypedImperativeAggregate` functions which may use arbitrary JVM objects as aggregation states. Unlike `HashAggregateExec`, it uses safe rows as aggregation buffers and falls back to sort-based aggregation when the entry count threshold is exceeded rather than byte size.

## When Used
The query planner chooses this operator when:
- Aggregation expressions contain `TypedImperativeAggregate` functions that require JVM objects as state
- `spark.sql.execution.useObjectHashAggregateExec` is enabled (default: true)
- The aggregation cannot be handled by the more efficient `HashAggregateExec` due to complex object state requirements

## Input Requirements
- **Expected input partitioning**: Any partitioning (no specific requirements)
- **Expected input ordering**: No ordering requirements
- **Number of children**: Unary operator (exactly one child)

## Output Properties
- **Output partitioning**: Preserves child's partitioning for the grouping key columns
- **Output ordering**: No guaranteed output ordering
- **Output schema**: Derived from `resultExpressions` containing grouping expressions and aggregate results

## Algorithm
• Creates an `ObjectAggregationIterator` for each partition to process input rows
• Uses a hash map to group rows by grouping key expressions, tracking entry count instead of memory size
• Maintains aggregation states as JVM objects in safe row buffers for each group
• Falls back to sort-based aggregation when hash map entry count exceeds `fallbackCountThreshold`
• Upon fallback, feeds all remaining input rows to external sorters rather than building additional hash maps
• Handles empty input specially: returns empty iterator for grouped aggregates, single row for ungrouped aggregates
• Applies `resultExpressions` to produce final output rows

## Memory Usage
- **Spills to disk**: Yes, falls back to sort-based aggregation with external sorting when hash map becomes too large
- **Memory requirements**: Controlled by `spark.sql.objectHashAggregate.sortBased.fallbackThreshold` (entry count threshold)
- **Buffering behavior**: Uses safe rows as aggregation buffers to support arbitrary JVM object states

## Partitioning Behavior
- **Data distribution**: Maintains input partitioning; does not repartition data
- **Shuffle requirements**: Relies on `requiredChildDistributionExpressions` for any needed shuffling upstream
- **Partition count**: No change in partition count

## Supported Join/Aggregation Types
This operator supports all standard SQL aggregation patterns:
- Grouped aggregations (with `GROUP BY` clauses)
- Ungrouped aggregations (global aggregates)
- Complex aggregation functions that maintain JVM object state
- Streaming aggregations (when `isStreaming = true`)

## Metrics
- `numOutputRows`: Number of output rows produced
- `aggTime`: Time spent in aggregation processing (milliseconds)
- `spillSize`: Total bytes spilled to disk during sort fallback
- `numTasksFallBacked`: Number of tasks that fell back to sort-based aggregation

## Code Generation
Code generation is **not supported**. The operator explicitly mentions "CodeGen is not supported yet" due to the complexity of handling arbitrary JVM object states in generated code.

## Configuration Options
- `spark.sql.execution.useObjectHashAggregateExec`: Enables/disables this operator (default: true)
- `spark.sql.objectHashAggregate.sortBased.fallbackThreshold`: Controls when to fall back to sort-based aggregation based on hash map entry count

## Edge Cases
- **Null handling**: Handled through the underlying aggregation iterator and safe row implementations
- **Empty partition handling**: Grouped aggregates return empty iterator; ungrouped aggregates return single row with initial aggregate values
- **Memory pressure**: Falls back to sort-based aggregation when hash map grows too large, feeding all remaining input to external sorters to avoid GC issues

## Examples
```
ObjectHashAggregate(keys=[customer_id#1], functions=[collect_list(purchase_data#2, 0, 0)])
+- Exchange hashpartitioning(customer_id#1, 200)
   +- LocalTableScan [customer_id#1, purchase_data#2]
```

## See Also
- `HashAggregateExec`: Standard hash-based aggregation for simpler aggregate functions
- `SortAggregateExec`: Sort-based aggregation used as fallback
- `BaseAggregateExec`: Base class defining common aggregation behavior