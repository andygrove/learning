# KnownNullable

## Overview
KnownNullable is a tagging expression that wraps a child expression to explicitly mark it as nullable, overriding the child's nullability determination. This expression acts as a transparent wrapper that forces the nullable property to true while preserving all other behavior of the wrapped expression.

## Syntax
```scala
// Internal Catalyst expression - not directly exposed in SQL
KnownNullable(childExpression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The child expression to be wrapped and marked as nullable |

## Return Type
Returns the same data type as the child expression.

## Supported Data Types
Supports all data types since it acts as a transparent wrapper around any child expression.

## Algorithm

- Wraps the child expression without modifying its evaluation logic

- Forces the nullable property to return true regardless of child's nullability

- Delegates all evaluation and code generation to the child expression

- Acts as a metadata annotation for the Catalyst optimizer's nullability analysis

- Preserves the exact return value and behavior of the wrapped expression

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not affect partitioning as it's a transparent wrapper

- No shuffle operations are introduced

- Partitioning characteristics are inherited from the child expression

## Edge Cases

- Null handling: Inherits null handling behavior from child expression

- The expression itself never produces nulls beyond what the child produces

- Used internally by Catalyst optimizer for nullability inference corrections

- Does not change the actual runtime behavior, only compile-time nullability metadata

## Code Generation
Supports full code generation (Tungsten) by delegating code generation directly to the child expression without any wrapper overhead.

## Examples
```sql
-- Not directly accessible in SQL as this is an internal Catalyst expression
-- Used internally during query optimization phases
```

```scala
// Internal usage in Catalyst optimization
// This expression is typically created by optimizer rules
val childExpr = col("someColumn")
val nullableWrapper = KnownNullable(childExpr)
// Forces nullability analysis to treat the expression as nullable
```

## See Also

- TaggingExpression - Base class for metadata tagging expressions
- Expression nullability inference in Catalyst optimizer
- Other constraint expressions for optimizer hints