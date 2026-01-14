# LateralColumnAliasReference

## Overview
`LateralColumnAliasReference` is a special leaf expression that represents a reference to a lateral column alias in Spark SQL query plans. It serves as a wrapper around named expressions to enable resolution and unwrapping of lateral column aliases during query analysis, allowing columns to reference other columns defined earlier in the same SELECT clause.

## Syntax
This is an internal Catalyst expression and is not directly exposed to end users through SQL syntax or DataFrame API. It is created internally during query analysis when lateral column aliases are detected.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `ne` | `NamedExpression` | The underlying named expression being referenced |
| `nameParts` | `Seq[String]` | Name parts of the original UnresolvedAttribute, used for restoration |
| `a` | `Attribute` | Attribute of the referenced lateral column alias for matching during resolution |

## Return Type
Returns the same data type as the underlying `NamedExpression` (`ne.dataType`). The actual return type depends on the wrapped expression.

## Supported Data Types
Supports all data types since it acts as a transparent wrapper around any `NamedExpression`. The supported data types are determined by the underlying named expression being referenced.

## Algorithm

- Acts as a transparent proxy to the underlying `NamedExpression`
- Delegates all attribute properties (name, exprId, qualifier) to the wrapped expression
- Maintains reference information needed for lateral alias resolution
- Preserves resolution state and nullability of the underlying expression
- Cannot be directly evaluated (marked as `Unevaluable`)

## Partitioning Behavior
This expression does not directly affect partitioning behavior:

- Partitioning behavior is inherited from the underlying named expression
- Does not introduce additional shuffle operations
- Preserves the partitioning characteristics of the referenced expression

## Edge Cases

- Null handling is delegated to the underlying `NamedExpression`
- Requires that the underlying expression is either resolved or an `UnresolvedAttribute`
- Cannot be directly evaluated and will throw an exception if evaluation is attempted
- Resolution state depends entirely on the wrapped expression's resolution state

## Code Generation
This expression is marked as `Unevaluable`, meaning:

- Does not support code generation (Tungsten)
- Should be resolved and unwrapped before code generation phase
- Intended to be eliminated during query analysis, not execution

## Examples
```sql
-- This expression is created internally for queries like:
SELECT a + 1 AS b, b * 2 AS c FROM table
-- Where 'b' in the second column references the first column
```

```scala
// Internal usage during query analysis - not exposed to users
val ref = LateralColumnAliasReference(
  ne = someNamedExpression,
  nameParts = Seq("column_name"), 
  a = attributeReference
)
```

## See Also

- `NamedExpression` - The base trait for expressions with names
- `UnresolvedAttribute` - Used for unresolved column references
- `Attribute` - Represents resolved column references
- `LeafExpression` - Base class for expressions with no child expressions