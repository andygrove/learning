# DirectShufflePartitionID

## Overview
DirectShufflePartitionID is a Catalyst expression that enables direct specification of target partition IDs during shuffle operations. Unlike hash-based partitioning expressions, this allows explicit control over which partition each row is assigned to by evaluating a child expression that returns the target partition ID.

## Syntax
```scala
DirectShufflePartitionID(child: Expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | An expression that evaluates to an integral type representing the target partition ID. Must be non-null and within valid partition range [0, numPartitions). |

## Return Type
The expression returns the same data type as its child expression (typically an integral type like IntegerType or LongType).

## Supported Data Types
- **Input**: IntegerType only (enforced by `inputTypes: Seq[AbstractDataType] = IntegerType :: Nil`)
- **Output**: Same as input (child.dataType)

## Algorithm
- Extends UnaryExpression to operate on a single child expression
- Implements ExpectsInputTypes to enforce IntegerType constraint on input
- Marked as Unevaluable, meaning it cannot be directly evaluated in standard expression evaluation
- Acts as a metadata wrapper indicating direct partition assignment intent
- The actual partitioning logic is handled by the physical planning layer, not during expression evaluation

## Partitioning Behavior
- **Preserves partitioning**: No, this expression is specifically designed to control partitioning
- **Requires shuffle**: Yes, this expression is used during shuffle operations to directly assign partition IDs
- **Partition assignment**: Enables explicit partition targeting rather than hash-based distribution
- **Range validation**: Target partition IDs must be within [0, numPartitions) range

## Edge Cases
- **Null handling**: The expression is marked as non-nullable (`nullable: Boolean = false`), and the child expression must not evaluate to null
- **Range validation**: Partition IDs outside [0, numPartitions) range will cause runtime errors
- **Type enforcement**: Only IntegerType inputs are accepted; other types will be rejected during analysis
- **Unevaluable nature**: Cannot be used in contexts requiring direct expression evaluation (e.g., SELECT clause projections)

## Code Generation
This expression does not support code generation as it extends Unevaluable. It serves as a planning-time construct that gets processed during physical planning rather than during query execution. The actual partitioning logic is implemented in the shuffle operations themselves.

## Examples
```sql
-- DirectShufflePartitionID is not directly accessible via SQL
-- It's used internally by the Catalyst optimizer for specific partitioning strategies
```

```scala
// Internal usage in Catalyst planning (not public API)
import org.apache.spark.sql.catalyst.expressions._

// This expression is typically created during physical planning
val partitionExpr = DirectShufflePartitionID(Literal(2))
// Used in shuffle operations to direct rows to partition 2

// Note: This is not intended for direct user consumption
// but rather as an internal optimization hint
```

## See Also
- **HashPartitioning**: Standard hash-based partitioning for comparison
- **RangePartitioning**: Range-based partitioning alternative
- **UnaryExpression**: Base class for single-child expressions
- **ExpectsInputTypes**: Trait for type constraint enforcement
- **Unevaluable**: Marker trait for non-evaluable expressions used in planning