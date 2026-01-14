# OuterScopeReference

## Overview
OuterScopeReference is a special leaf expression that represents a named expression originating from outer scopes beyond the immediate subquery plan context. It serves as a marker indicating that the referenced attribute cannot be resolved within the current subquery or its immediate outer plan, but comes from an even higher scope in nested query structures.

## Syntax
This expression is not directly accessible through SQL syntax or DataFrame API as it's an internal Catalyst expression used during query planning and analysis phases.

```scala
OuterScopeReference(e: NamedExpression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| e | NamedExpression | The named expression from an outer scope that this reference wraps |

## Return Type
Returns the same data type as the wrapped NamedExpression. The return type is dynamically determined by the `dataType` property of the enclosed expression.

## Supported Data Types
Supports all data types since it acts as a transparent wrapper around any NamedExpression, inheriting the data type constraints from the wrapped expression.

## Algorithm

- Acts as a transparent proxy by delegating all core properties to the wrapped NamedExpression
- Preserves the original expression's data type, nullability, name, qualifier, and expression ID
- Overrides the pretty name to "outerScope" for debugging and display purposes
- Maintains referential integrity by forwarding `toAttribute` calls to the wrapped expression
- Supports instance creation through `newInstance()` while preserving the wrapper semantics

## Partitioning Behavior
This expression does not directly affect partitioning behavior as it's a reference wrapper:

- Preserves the partitioning characteristics of the underlying expression
- Does not trigger shuffles by itself
- Partitioning impact depends entirely on the wrapped NamedExpression

## Edge Cases

- Inherits null handling behavior from the wrapped NamedExpression
- Cannot be directly evaluated (extends Unevaluable trait)
- SQL representation includes the "outerScope" prefix for clarity: `outerScope(wrapped_expression_sql)`
- Expression ID and attributes are preserved from the original expression to maintain proper reference semantics
- NewInstance creation maintains the wrapper structure while creating a new instance of the underlying expression

## Code Generation
This expression does not support code generation as it extends the Unevaluable trait. It's designed for query planning and analysis phases rather than runtime evaluation, so it falls back to interpreted mode (though it's typically resolved before execution).

## Examples
```sql
-- Not directly accessible in SQL
-- Used internally during subquery processing
```

```scala
// Internal usage during query analysis
// Not directly creatable through DataFrame API
val outerRef = OuterScopeReference(someNamedExpression)
```

## See Also

- NamedExpression - The base trait that this expression implements
- LeafExpression - The expression category this belongs to
- SubqueryExpression - The context where this expression is commonly used
- Attribute - The target type that this expression can be converted to