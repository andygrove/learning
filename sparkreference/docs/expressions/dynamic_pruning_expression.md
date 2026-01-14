# DynamicPruningExpression

## Overview
DynamicPruningExpression is a marker expression used during query planning to enable dynamic partition pruning optimization. It wraps an underlying predicate expression and defers all evaluation logic to its child expression while providing metadata for the Catalyst optimizer to identify dynamic pruning opportunities.

## Syntax
This expression is created internally during query planning and is not directly accessible through SQL or DataFrame API syntax. It wraps predicates that can benefit from dynamic pruning optimization.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The underlying predicate expression that performs the actual evaluation |

## Return Type
Returns the same data type as its child expression, as it delegates all evaluation to the child.

## Supported Data Types
Supports all data types that the underlying child expression supports, as this is purely a wrapper expression that does not modify the evaluation logic.

## Algorithm

- Acts as a transparent wrapper around the child expression during evaluation

- Delegates `eval()` calls directly to the child expression without modification

- Provides tree pattern matching capability through `DYNAMIC_PRUNING_EXPRESSION` pattern

- Maintains expression tree structure while adding pruning metadata

- Supports both interpreted and code-generated evaluation modes

## Partitioning Behavior
How this expression affects partitioning:

- Does not directly affect partitioning as it's evaluation-transparent

- Enables partition pruning optimizations that can reduce the number of partitions scanned

- May allow the optimizer to eliminate entire partitions before execution

## Edge Cases

- Null handling: Inherits null handling behavior from the child expression

- Empty input: Behavior depends entirely on the child expression's implementation

- Error propagation: Any exceptions from child evaluation are propagated unchanged

- Planning phase: Expression must be resolved during planning or query execution may fail

## Code Generation
Supports Tungsten code generation through the `doGenCode()` method, which delegates code generation to the child expression. The generated code is identical to what the child expression would produce.

## Examples
```sql
-- This expression is not directly accessible in SQL
-- It is created internally during optimization of queries like:
SELECT * FROM table1 t1 
JOIN table2 t2 ON t1.id = t2.id 
WHERE t2.category = 'active'
```

```scala
// Not directly accessible through DataFrame API
// Created internally during catalyst planning phase
// when dynamic pruning optimization is applicable
```

## See Also

- DynamicPruning (trait) - The marker trait this expression implements
- UnaryExpression - The base class for single-child expressions
- TreePattern.DYNAMIC_PRUNING_EXPRESSION - The pattern used for matching this expression type