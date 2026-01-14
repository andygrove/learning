# PipeExpression

## Overview

`PipeExpression` is a special wrapper expression used internally by Apache Spark's Catalyst optimizer to represent expressions within SQL pipe operator clauses. It enforces aggregate function constraints and provides metadata about the pipe operator context during query analysis.

## Syntax

PipeExpression is an internal Catalyst expression and is not directly accessible through SQL or DataFrame API. It is created during the parsing of SQL pipe operators like:

```sql
SELECT * FROM table |> SELECT column1, column2
SELECT * FROM table |> AGGREGATE sum(column1)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The wrapped child expression to be validated |
| isAggregate | Boolean | Whether the pipe operator is `AGGREGATE` (true) or other clauses (false) |
| clause | String | The name of the pipe operator clause (e.g., "SELECT", "AGGREGATE", "EXTEND") |

## Return Type

Returns the same data type as its child expression (`child.dataType`).

## Supported Data Types

Supports all data types since it acts as a transparent wrapper around the child expression. The actual data type support depends on the wrapped child expression.

## Algorithm

- Acts as a validation wrapper that is never actually evaluated (extends `Unevaluable`)
- Always reports as unresolved (`resolved = false`) to ensure analysis rules process it
- Preserves the child expression's data type through transparent delegation
- Gets stripped away after validation by `ValidateAndStripPipeExpressions` rule
- Validates aggregate function constraints based on the `isAggregate` flag and clause type

## Partitioning Behavior

PipeExpression itself has no partitioning impact since:
- It is an unevaluable wrapper expression
- It gets eliminated during the analysis phase
- Partitioning behavior depends on the underlying child expression after unwrapping

## Edge Cases

- **Null handling**: Inherits null handling from the child expression since it's never evaluated
- **Aggregate validation**: Throws `QueryCompilationErrors` if aggregate constraints are violated:
  - For `isAggregate = true`: child must contain at least one aggregate function
  - For `isAggregate = false` and non-SELECT clauses: child must not contain aggregate functions
- **Window functions**: Allowed in pipe operators and don't count as aggregate functions during validation
- **Unresolved state**: Always remains unresolved until stripped away by analysis rules

## Code Generation

Does not support code generation since it extends `Unevaluable`. The expression is designed to be eliminated during the analysis phase before code generation occurs.

## Examples

```sql
-- Internal representation during analysis of:
SELECT * FROM table |> AGGREGATE sum(salary), count(*)
-- Creates PipeExpression(child=sum(salary), isAggregate=true, clause="AGGREGATE")

-- Internal representation during analysis of:
SELECT * FROM table |> SELECT name, age
-- Creates PipeExpression(child=name, isAggregate=false, clause="SELECT")
-- Creates PipeExpression(child=age, isAggregate=false, clause="SELECT")
```

```scala
// Not directly accessible through DataFrame API
// Created internally during SQL parsing of pipe operators
```

## See Also

- `PipeOperator` - Logical plan node representing pipe operator boundaries
- `EliminatePipeOperators` - Rule that removes PipeOperator nodes after analysis
- `ValidateAndStripPipeExpressions` - Rule that validates and removes PipeExpression wrappers
- `UnaryExpression` - Parent class for expressions with single child
- `Unevaluable` - Trait for expressions that cannot be evaluated