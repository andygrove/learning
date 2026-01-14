# TryMultiply

## Overview
`TryMultiply` is a runtime replaceable expression that performs multiplication with error handling, returning NULL instead of throwing exceptions when overflow or other arithmetic errors occur. It serves as the safe multiplication operator that implements the `try_multiply` SQL function introduced in Spark 3.3.0.

## Syntax
```sql
try_multiply(expr1, expr2)
```

```scala
// DataFrame API (internal usage)
TryMultiply(leftExpr, rightExpr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand for multiplication |
| right | Expression | Right operand for multiplication |
| replacement | Expression | Internal replacement expression that handles the actual computation |

## Return Type
Returns the same numeric type as the input operands following Spark's type promotion rules. For interval types multiplied by numeric types, returns interval type.

## Supported Data Types
- **Numeric types**: All numeric types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType)
- **Interval arithmetic**: Interval types multiplied by numeric types
- **Mixed numeric operations**: Follows standard Spark type coercion rules

## Algorithm
- Inherits analysis rules from its child expressions through `InheritAnalysisRules`
- For numeric type pairs: Creates `Multiply(left, right, EvalMode.TRY)` for direct TRY evaluation
- For non-numeric types (like intervals): Wraps `Multiply(left, right, EvalMode.ANSI)` with `TryEval` 
- Implements `RuntimeReplaceable` pattern, delegating actual evaluation to the replacement expression
- The replacement expression handles overflow detection and NULL return on arithmetic errors

## Partitioning Behavior
- **Preserves partitioning**: Yes, since multiplication is a row-level operation that doesn't require data movement
- **Requires shuffle**: No, operates on individual rows independently
- **Partition-wise operation**: Can be executed within each partition without cross-partition dependencies

## Edge Cases
- **Null handling**: If either operand is NULL, returns NULL
- **Overflow behavior**: Returns NULL instead of throwing overflow exceptions (key difference from regular multiply)
- **Zero multiplication**: Follows standard arithmetic rules (any number × 0 = 0)
- **Interval edge cases**: For interval arithmetic, delegates to TryEval wrapper which handles interval-specific overflow scenarios
- **Decimal precision**: Maintains decimal precision rules but returns NULL on precision overflow

## Code Generation
Supports Tungsten code generation through its replacement expression. The actual codegen implementation depends on the replacement:
- Numeric `Multiply` with `EvalMode.TRY` generates optimized code with overflow checks
- `TryEval`-wrapped expressions may fall back to interpreted mode depending on the wrapped expression's codegen support

## Examples
```sql
-- Basic numeric multiplication
SELECT try_multiply(5, 10);
-- Returns: 50

-- Overflow case (returns NULL instead of error)
SELECT try_multiply(9223372036854775807, 2);
-- Returns: NULL

-- Interval arithmetic example from source comments
SELECT try_multiply(interval 2 year, 3);
-- Returns: 6-0 (6 years, 0 months)

-- NULL handling
SELECT try_multiply(NULL, 5);
-- Returns: NULL
```

```scala
// DataFrame API usage (typically internal)
import org.apache.spark.sql.catalyst.expressions._
val tryMult = TryMultiply(col1.expr, col2.expr)

// Through SQL function
df.selectExpr("try_multiply(column1, column2)")
```

## See Also
- `Multiply` - Regular multiplication operator that throws on overflow
- `TryEval` - General try-catch wrapper for expressions  
- `TryAdd`, `TrySubtract`, `TryDivide` - Related safe arithmetic operations
- `RuntimeReplaceable` - Base trait for expressions that transform into other expressions