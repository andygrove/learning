# ReusedExchangeExec

## Overview
`ReusedExchangeExec` is a wrapper operator that enables reuse of exchange operations while maintaining distinct output attribute IDs. It acts as a proxy to an existing Exchange operator, preserving the original attribute identifiers that downstream operators expect while avoiding duplicate computation of identical exchange operations.

## When Used
This operator is chosen by the query planner's exchange reuse optimization when:
- Multiple parts of the query plan require logically identical data exchanges
- The catalyst optimizer detects that an exchange operation can be reused
- Different downstream operators expect different attribute ID sets from the same exchange result
- The `spark.sql.exchange.reuse` configuration is enabled (default: true)

## Input Requirements
- **Expected input partitioning**: Inherits from the wrapped child Exchange operator
- **Expected input ordering**: Inherits from the wrapped child Exchange operator  
- **Number of children**: Leaf node (0 children) - wraps an existing Exchange rather than having direct children

## Output Properties
- **Output partitioning**: Derived from child's `outputPartitioning` with attribute IDs updated via `updateAttr` transformation
- **Output ordering**: Child's `outputOrdering` with attribute references mapped to new output attribute IDs
- **Output schema**: Explicitly provided during construction, maintaining the expected attribute IDs for downstream operators

## Algorithm
- Creates an attribute mapping (`originalAttrToNewAttr`) between child output attributes and expected output attributes
- Delegates all execution calls (`doExecute`, `doExecuteColumnar`, `doExecuteBroadcast`) directly to the wrapped child Exchange
- Transforms partitioning and ordering expressions using `updateAttr` to replace old attribute references with new ones
- Returns the same RDD/ColumnarBatch/Broadcast data as the child but with updated metadata
- Uses lazy evaluation for the attribute transformation function to avoid unnecessary computation
- Bypasses itself during canonicalization by returning `child.canonicalized`

## Memory Usage
- **Spill behavior**: Inherits spill characteristics from the wrapped Exchange operator
- **Memory requirements**: No additional memory overhead beyond the child Exchange
- **Buffering behavior**: Acts as a zero-cost wrapper with no buffering of its own

## Partitioning Behavior
- **Data distribution**: No changes to actual data distribution - purely metadata transformation
- **Shuffle requirements**: No additional shuffles - reuses existing Exchange shuffle results
- **Partition count**: Maintains same partition count as the wrapped Exchange

## Supported Join/Aggregation Types
Not applicable - this is a utility wrapper operator that doesn't perform joins or aggregations.

## Metrics
Inherits all metrics from the wrapped child Exchange operator. Does not introduce additional metrics of its own. The `verboseStringWithOperatorId()` method shows reuse information with the original operator ID.

## Code Generation
- **Columnar support**: Delegates `supportsColumnar` to child Exchange
- **Whole-stage codegen**: Not directly involved in codegen as it's a passthrough wrapper
- **Code generation**: Execution methods delegate to child, so codegen behavior matches the wrapped Exchange

## Configuration Options
- `spark.sql.exchange.reuse` (default: true) - Controls whether exchange reuse optimization is enabled
- `spark.sql.adaptive.enabled` - May affect when exchange reuse opportunities are detected
- All configuration options that affect the wrapped Exchange operator apply transitively

## Edge Cases
- **Null handling**: Delegates to child Exchange - no special null handling logic
- **Empty partition handling**: Inherits empty partition behavior from wrapped Exchange
- **Attribute mapping**: Safely handles cases where attribute mapping is not found via `getOrElse(attr, attr)`
- **Expression transformation**: Only updates Partitioning expressions that are also Expression instances

## Examples
```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- Project [id#1L, name#2]
   +- SortMergeJoin [id#1L], [user_id#5L], Inner
      :- Sort [id#1L ASC NULLS FIRST]
      :  +- ReusedExchange [id#1L, name#2] [Reuses operator id: 4]
      +- Sort [user_id#5L ASC NULLS FIRST]
         +- Exchange hashpartitioning(user_id#5L, 200), ENSURE_REQUIREMENTS
            +- Scan parquet [user_id#5L, data#6]
```

## See Also
- `Exchange` - The base exchange operators that this wrapper reuses
- `ShuffleExchangeExec` - Common type of Exchange that gets reused
- `BroadcastExchangeExec` - Another Exchange type that can be wrapped
- `ReuseExchange` catalyst rule - The optimization rule that inserts ReusedExchangeExec nodes