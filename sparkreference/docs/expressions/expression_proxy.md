# ExpressionProxy

## Overview
ExpressionProxy is a catalyst expression that acts as a caching proxy wrapper around another expression. It intercepts evaluation requests and delegates them to a SubExprEvaluationRuntime, which provides cached evaluation results to avoid redundant computation of common subexpressions during interpreted expression evaluation.

## Syntax
This is an internal Catalyst expression used by the Spark SQL engine and is not directly accessible through SQL syntax or DataFrame API. It is automatically created by the query optimizer for subexpression elimination.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The wrapped expression that this proxy represents |
| id | Int | Unique identifier for this proxy instance used for caching and equality |
| runtime | SubExprEvaluationRuntime | Runtime cache manager that handles evaluation and caching logic |

## Return Type
Returns the same data type as the wrapped child expression (`child.dataType`).

## Supported Data Types
Supports all data types that the wrapped child expression supports, as it acts as a transparent proxy without type restrictions.

## Algorithm

- When `eval()` is called, delegates to `runtime.getEval(this)` instead of directly evaluating the child
- The runtime checks its cache first before falling back to actual expression evaluation
- If cache miss occurs, calls `proxyEval()` which directly evaluates the child expression
- Uses the unique `id` for cache key management and proxy instance equality
- Maintains the same nullability and data type characteristics as the wrapped expression

## Partitioning Behavior
Does not affect partitioning behavior as it operates at the expression evaluation level within individual partitions:

- Preserves existing partitioning schemes
- No shuffle operations required
- Operates independently on each partition's data

## Edge Cases

- Null handling behavior matches the wrapped child expression exactly
- Throws `QueryExecutionErrors.cannotGenerateCodeForExpressionError` if code generation is attempted
- Equality comparison only considers the `id` field, ignoring child expression differences
- Hash code computation uses only the `id` to ensure consistent caching behavior
- Falls back to direct child evaluation through `proxyEval()` when cache mechanisms fail

## Code Generation
Does not support Tungsten code generation and will throw a `QueryExecutionErrors.cannotGenerateCodeForExpressionError` if code generation is attempted. This expression is designed exclusively for interpreted expression evaluation mode.

## Examples
```sql
-- Not directly accessible through SQL
-- Automatically used by Spark internally for subexpression elimination
```

```scala
// Internal usage only - not accessible through DataFrame API
// Created automatically by Catalyst optimizer during query planning
```

## See Also

- SubExprEvaluationRuntime - The runtime cache manager used by this proxy
- UnaryExpression - The base class that ExpressionProxy extends
- Expression evaluation and subexpression elimination in Catalyst optimizer