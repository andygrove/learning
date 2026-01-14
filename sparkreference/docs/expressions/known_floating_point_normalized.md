# KnownFloatingPointNormalized

## Overview
`KnownFloatingPointNormalized` is a tagging expression in Spark Catalyst that marks floating-point values as being in normalized form. This expression serves as a metadata hint to the optimizer that the wrapped floating-point expression produces values that conform to IEEE 754 normalization standards, enabling potential optimizations in downstream operations.

## Syntax
This is an internal Catalyst expression not directly exposed in SQL syntax. It's used internally by the optimizer.

```scala
KnownFloatingPointNormalized(child: Expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The wrapped expression that produces normalized floating-point values |

## Return Type
Returns the same data type as the child expression, typically `FloatType` or `DoubleType`.

## Supported Data Types

- FloatType (32-bit floating-point)
- DoubleType (64-bit floating-point)

## Algorithm

- Acts as a transparent wrapper around the child expression
- Does not modify the actual computation or values produced by the child
- Serves as a catalyst optimizer hint indicating normalized floating-point representation
- Preserves all evaluation semantics of the wrapped expression
- Used by the optimizer to make assumptions about floating-point value properties

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not affect partitioning since it's a transparent wrapper
- Maintains the same partitioning properties as the child expression
- No shuffle operations are introduced

## Edge Cases

- Null handling: Inherits null handling behavior from the child expression
- NaN values: Tagging remains valid as NaN is a normalized IEEE 754 representation
- Infinite values: Both positive and negative infinity are considered normalized
- Zero values: Both +0.0 and -0.0 are normalized representations
- The tagging assumes the child expression actually produces normalized values

## Code Generation
Inherits code generation capabilities from the child expression:

- If child supports code generation, this expression supports it
- Acts transparently during code generation phase
- Does not add overhead to generated code

## Examples
```sql
-- Not directly accessible in SQL
-- Used internally by Catalyst optimizer
```

```scala
// Internal usage in Catalyst optimizer rules
val normalizedExpr = KnownFloatingPointNormalized(child = floatColumn)

// Typically created by optimization rules, not user code
val optimizedPlan = plan.transformExpressions {
  case expr: Expression if isNormalizedFloatingPoint(expr) =>
    KnownFloatingPointNormalized(expr)
}
```

## See Also

- `KnownNotNull` - Similar tagging expression for null constraints
- `TaggingExpression` - Base class for optimizer hint expressions
- IEEE 754 floating-point standard for normalization rules