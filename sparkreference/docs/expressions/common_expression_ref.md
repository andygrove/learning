# CommonExpressionRef

## Overview
CommonExpressionRef is a leaf expression that represents a reference to a common expression by its unique identifier. It acts as a placeholder that points to a shared expression definition that can be reused multiple times within a query plan, enabling common subexpression elimination optimizations.

## Syntax
This expression is not directly accessible through SQL syntax or DataFrame API. It is an internal Catalyst expression created during query optimization phases, specifically during common subexpression elimination.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| id | CommonExpressionId | Unique identifier of the referenced common expression |
| dataType | DataType | The data type of the referenced expression's result |
| nullable | Boolean | Whether the referenced expression can produce null values |

## Return Type
The return type matches the `dataType` parameter, which is inherited from the referenced common expression definition. The nullability is also inherited from the original expression.

## Supported Data Types
Since this is a reference expression, it supports all data types that Spark supports, as the actual data type is determined by the referenced common expression definition.

## Algorithm

- Acts as a pointer to a common expression definition stored elsewhere in the query plan

- Inherits the data type and nullability properties from the referenced expression

- Cannot be directly evaluated (implements Unevaluable trait)

- Requires resolution during query planning to establish the connection to the actual expression

- Serves as a placeholder that gets replaced or resolved during code generation

## Partitioning Behavior
CommonExpressionRef itself does not affect partitioning behavior, as it is merely a reference. The partitioning implications depend entirely on the referenced common expression's behavior.

## Edge Cases

- Cannot be evaluated directly due to Unevaluable trait - must be resolved first

- Requires that the referenced CommonExpressionDef is already resolved and available

- Null handling behavior is inherited from the referenced expression

- Invalid references (non-existent IDs) would cause resolution failures during query planning

## Code Generation
This expression is marked as Unevaluable, meaning it cannot generate code directly. It must be resolved and replaced with the actual common expression or its generated code during the code generation phase.

## Examples
```sql
-- Not directly accessible through SQL
-- Created internally during optimization
```

```scala
// Not directly accessible through DataFrame API
// Created internally by Catalyst optimizer during common subexpression elimination
```

## See Also

- CommonExpressionDef - defines the actual common expression being referenced

- TreePattern.COMMON_EXPR_REF - the tree pattern used for matching this expression type

- LeafExpression - the base class for expressions with no child expressions

- Unevaluable - trait indicating expressions that cannot be directly evaluated