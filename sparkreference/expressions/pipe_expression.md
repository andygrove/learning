# PipeExpression

## Overview
PipeExpression represents a pipe operator (`|>`) used in Spark SQL for chaining operations in a pipeline-style syntax. This expression serves as a placeholder during query parsing and planning phases, distinguishing between aggregate and non-aggregate pipe operations based on the presence of aggregate functions in the child expression.

## Syntax
```sql
-- Pipe operator syntax (parsed into PipeExpression internally)
expression |> TRANSFORM
expression |> AGGREGATE
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The child expression that contains the actual computation logic |
| isAggregate | Boolean | Flag indicating whether this is an aggregate pipe operator (`|> AGGREGATE`). When true, child must contain aggregate functions; when false, child must not contain aggregate functions |
| clause | String | The SQL clause identifier used for generating contextual error messages during query analysis |

## Return Type
Returns the same data type as the child expression (`child.dataType`). The actual return type depends entirely on what the child expression evaluates to.

## Supported Data Types
Supports all data types that the child expression supports, as PipeExpression acts as a transparent wrapper. No data type restrictions are imposed by the pipe expression itself.

## Algorithm
- Acts as a container for the child expression during query planning
- Validates aggregate function usage based on the `isAggregate` flag
- Remains unresolved (`resolved = false`) throughout its lifecycle
- Gets replaced or transformed by later optimization phases
- Provides error context through the `clause` parameter when validation fails

## Partitioning Behavior
PipeExpression itself does not affect partitioning as it is an `Unevaluable` expression:
- Does not preserve or alter partitioning directly
- Partitioning behavior depends on how the child expression is eventually processed
- No shuffle operations are triggered by PipeExpression itself

## Edge Cases
- **Null handling**: Inherits null handling behavior from the child expression
- **Empty input**: Behavior determined by the child expression's implementation
- **Unresolved state**: Always remains unresolved (`resolved = false`), requiring transformation during analysis
- **Evaluation attempts**: Throws runtime exception if `eval()` is called since it extends `Unevaluable`
- **Aggregate validation**: Strict enforcement of aggregate function presence based on `isAggregate` flag

## Code Generation
Does not support code generation as it extends `Unevaluable`. PipeExpression is designed to be transformed away during query analysis phases before code generation occurs. Any attempt to generate code for this expression will result in fallback to interpreted mode or throw an exception.

## Examples
```sql
-- This would be parsed into PipeExpression internally
-- Non-aggregate pipe operation
SELECT col1 |> TRANSFORM upper(value) FROM table1;

-- Aggregate pipe operation  
SELECT col1 |> AGGREGATE sum(value) FROM table1 GROUP BY col1;
```

```scala
// PipeExpression is typically created during SQL parsing
// Not directly instantiated in DataFrame API
val pipeExpr = PipeExpression(
  child = someExpression,
  isAggregate = false,
  clause = "TRANSFORM"
)

// Note: This would be part of internal Catalyst expression tree
// and not user-facing DataFrame API
```

## See Also
- `UnaryExpression` - Base class for expressions with single child
- `Unevaluable` - Trait for expressions that cannot be directly evaluated
- Aggregate expressions for `isAggregate = true` scenarios
- Transform expressions for `isAggregate = false` scenarios