# DirectShufflePartitionID

## Overview
DirectShufflePartitionID is a Spark Catalyst expression that passes through a partition ID value directly for use in shuffle partitioning operations. This expression is primarily used with RepartitionByExpression to allow users to explicitly specify target partition IDs rather than relying on hash-based partitioning algorithms.

## Syntax
```scala
// DataFrame API usage (internal - not directly exposed to users)
DirectShufflePartitionID(partitionIdExpression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | An expression that evaluates to an integral value representing the target partition ID |

## Return Type
Returns the same data type as the child expression (must be an integral type).

## Supported Data Types
- **Input**: IntegerType and other integral types
- **Output**: Same as input type (integral types only)

## Algorithm
- Takes a child expression that must evaluate to an integral type
- Validates that the child expression is not null at evaluation time
- Passes the partition ID value through directly without transformation
- The resulting partition ID must be within the valid range [0, numPartitions)
- Used internally by the partitioning subsystem to direct records to specific partitions

## Partitioning Behavior
- **Partitioning Impact**: This expression is specifically designed to control partitioning behavior
- **Shuffle Requirement**: Typically requires a shuffle operation when used with RepartitionByExpression
- **Partitioning Preservation**: Does not preserve existing partitioning; creates new partitioning based on explicit partition IDs

## Edge Cases
- **Null Handling**: Expression is marked as non-nullable (`nullable = false`), indicating null values are not permitted
- **Range Validation**: Partition IDs must be within [0, numPartitions) range, though validation occurs at runtime
- **Type Enforcement**: Input must be integral type, enforced by `inputTypes = IntegerType :: Nil`
- **Evaluation**: Marked as `Unevaluable`, meaning it's used for planning but not direct evaluation

## Code Generation
This expression extends `Unevaluable`, indicating it does not support direct code generation or interpreted evaluation. It serves as a planning-time construct that is consumed by the partitioning subsystem rather than being evaluated row-by-row.

## Examples
```scala
// Internal usage example (not directly accessible to end users)
import org.apache.spark.sql.catalyst.expressions._

// Create expression with literal partition ID
val partitionExpr = DirectShufflePartitionID(Literal(2))

// Typically used within RepartitionByExpression
// This would direct records to partition 2
```

```sql
-- No direct SQL syntax available
-- This is an internal Catalyst expression used by the optimizer
```

## See Also
- `RepartitionByExpression` - Primary consumer of this expression
- `UnaryExpression` - Base class for single-child expressions
- `ExpectsInputTypes` - Trait for type validation
- `Unevaluable` - Marker for planning-only expressions