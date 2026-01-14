# KnownNotContainsNull

## Overview
`KnownNotContainsNull` is a Catalyst tagging expression that wraps an array expression to indicate that the array is known to not contain any null elements. This expression serves as a metadata hint to the Catalyst optimizer about the nullability characteristics of array elements without changing the actual data or evaluation logic.

## Syntax
This is an internal Catalyst expression not directly accessible through SQL syntax. It is created by the Catalyst optimizer during query planning and optimization phases.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The wrapped array expression that is known to not contain null elements |

## Return Type
Returns an `ArrayType` with the same element type as the child expression, but with `containsNull` explicitly set to `false`.

## Supported Data Types

- ArrayType expressions of any element type
- The child expression must evaluate to an ArrayType

## Algorithm

- Inherits from `TaggingExpression`, making it a metadata-only wrapper
- Returns a modified `ArrayType` with `containsNull = false` 
- Delegates actual code generation directly to the child expression without modification
- Provides type system guarantees about array element nullability
- Used by Catalyst optimizer for type inference and optimization decisions

## Partitioning Behavior
This expression has no impact on partitioning behavior:

- Preserves existing partitioning schemes
- Does not require shuffle operations
- Acts as a transparent wrapper for partitioning purposes

## Edge Cases

- Does not perform runtime null checking - relies on optimizer's static analysis
- If the optimizer's assumption is incorrect and nulls are present, no runtime error occurs
- The tagging is purely for optimization and type system benefits
- Child expression must be an ArrayType or ClassCastException may occur during type casting

## Code Generation
Supports full code generation through delegation - calls `child.genCode(ctx)` directly, providing the same code generation performance as the underlying child expression.

## Examples
```sql
-- Not directly accessible in SQL
-- Created internally by Catalyst optimizer
```

```scala
// Internal Catalyst usage example
// Created during optimization phases
val arrayExpr: Expression = // some array expression
val taggedExpr = KnownNotContainsNull(arrayExpr)
// taggedExpr.dataType.asInstanceOf[ArrayType].containsNull == false
```

## See Also

- `KnownNotNull` - Similar tagging expression for non-array types
- `TaggingExpression` - Base class for metadata wrapper expressions
- `ArrayType` - The data type this expression operates on