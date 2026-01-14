# KnownNotNull

## Overview
KnownNotNull is a Spark Catalyst tagging expression that wraps a child expression to explicitly mark its result as non-nullable. This expression is used internally by the Catalyst optimizer to track nullability constraints and enable null-aware optimizations during query planning and execution.

## Syntax
This is an internal Catalyst expression and is not directly accessible through SQL syntax. It is created by the optimizer during query analysis and optimization phases.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The wrapped expression whose result is guaranteed to be non-null |

## Return Type
Returns the same data type as the child expression, but with nullable set to false.

## Supported Data Types
Supports all data types since it acts as a transparent wrapper around any child expression. The data type is determined by the wrapped child expression.

## Algorithm

- Wraps the child expression without modifying its evaluation logic
- Forces the nullable property to return false regardless of child's nullability
- During code generation, overrides the isNull check to always return false (FalseLiteral)
- Preserves all other characteristics of the child expression (data type, evaluation, etc.)
- Acts as a compile-time assertion that the result will never be null

## Partitioning Behavior
This expression preserves partitioning behavior since it's a transparent wrapper:

- Does not affect partitioning schemes
- Does not require shuffle operations
- Maintains the same partitioning properties as the child expression

## Edge Cases

- The expression assumes the child will never produce null values at runtime
- If the child expression actually produces null, this could lead to incorrect query results
- Only used when the optimizer can prove through constraint analysis that nulls are impossible
- Does not perform any runtime null checking or validation

## Code Generation
Supports Tungsten code generation through the doGenCode method. The generated code evaluates the child expression normally but hardcodes the isNull flag to false (FalseLiteral), eliminating runtime null checks.

## Examples
```sql
-- Not directly accessible in SQL
-- Created internally by optimizer during constraint propagation
```

```scala
// Internal usage example (not for end users)
val childExpr = Literal(42)
val knownNotNull = KnownNotNull(childExpr)
// knownNotNull.nullable returns false
// knownNotNull.dataType returns IntegerType
```

## See Also

- KnownNullable - complementary expression for marking expressions as definitely nullable
- TaggingExpression - parent trait for constraint tagging expressions
- IsNull/IsNotNull - runtime null checking expressions