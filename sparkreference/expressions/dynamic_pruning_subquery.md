# DynamicPruningSubquery

## Overview
`DynamicPruningSubquery` is a specialized predicate expression used in join operations to dynamically prune one side of the join using filtering data from the other side. It enables runtime partition pruning by creating a subquery that extracts filtering keys from the build side of a join to eliminate partitions on the probe side that cannot possibly contain matching rows.

## Syntax
This expression is not directly accessible through SQL syntax or DataFrame API. It is automatically inserted by Spark's optimizer during join planning when partition pruning opportunities are detected.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `pruningKey` | `Expression` | The filtering key expression from the plan to be pruned |
| `buildQuery` | `LogicalPlan` | The build side logical plan of the join operation |
| `buildKeys` | `Seq[Expression]` | The join key expressions from the build side |
| `broadcastKeyIndices` | `Seq[Int]` | Indices specifying which build keys to use for filtering |
| `onlyInBroadcast` | `Boolean` | When false, executes pruning even without broadcast reuse; when true, only executes if broadcast results can be reused |
| `exprId` | `ExprId` | Unique expression identifier (optional, auto-generated) |
| `hint` | `Option[HintInfo]` | Optional hint information for query planning |

## Return Type
Returns `Boolean` (as it extends `Predicate`), but this expression is `Unevaluable` and never directly evaluated.

## Supported Data Types
Supports any data type for the pruning key, provided that the pruning key data type exactly matches the corresponding build key data type at the specified broadcast key index.

## Algorithm
- Validates that pruning key and build keys are resolved and compatible
- Ensures exactly one broadcast key index is specified (multiple keys not currently supported)
- Verifies build key references are contained within the build query output
- During execution planning, gets converted to executable filtering logic
- The subquery extracts distinct values from build side to create an IN predicate for pruning

## Partitioning Behavior
This expression is specifically designed for partition pruning:
- **Preserves partitioning**: No, it's used to eliminate entire partitions
- **Requires shuffle**: No, it reduces data movement by eliminating partitions before shuffle
- **Effect**: Reduces the amount of data that needs to be processed in subsequent join operations

## Edge Cases
- **Null handling**: Inherits null handling from the underlying pruning key expression
- **Empty build side**: If build query returns no results, all partitions would be pruned
- **Resolution requirements**: Expression remains unresolved until all components (pruning key, build query, build keys) are resolved
- **Single key constraint**: Currently only supports single broadcast key (broadcastKeyIndices.size == 1)
- **Type compatibility**: Requires exact data type match between pruning key and corresponding build key

## Code Generation
This expression does not support code generation as it is marked `Unevaluable`. It serves as a planning-time construct that gets transformed into executable predicates during physical planning.

## Examples
```sql
-- This optimization is applied automatically in joins like:
SELECT * FROM large_table l
JOIN small_table s ON l.partition_key = s.join_key
WHERE s.filter_column = 'some_value'

-- The optimizer may insert DynamicPruningSubquery to prune
-- partitions of large_table before the join
```

```scala
// Not directly accessible through DataFrame API
// Applied automatically during join optimization:
val large = spark.table("large_table")
val small = spark.table("small_table").filter($"filter_column" === "some_value")
large.join(small, $"partition_key" === $"join_key")
// Optimizer may add dynamic pruning here
```

## See Also
- `DynamicPruningExpression` - The executable wrapper created during planning
- `SubqueryExpression` - Parent class for subquery-based expressions  
- `BroadcastHashJoinExec` - Physical operator that often triggers this optimization
- `PartitionPruning` - Related static partition pruning functionality