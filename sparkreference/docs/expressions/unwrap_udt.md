# UnwrapUDT

## Overview
The `UnwrapUDT` expression unwraps User-Defined Type (UDT) columns to expose their underlying SQL type representation. This is an internal Catalyst expression used during query optimization to convert UDT columns into their corresponding SQL types for processing.

## Syntax
This is an internal expression not directly accessible through SQL syntax. It's automatically applied by Catalyst during query planning when UDT columns need to be processed.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression containing a UserDefinedType that needs to be unwrapped |

## Return Type
Returns the underlying SQL type of the UserDefinedType. The actual return type depends on the `sqlType` property of the input UDT.

## Supported Data Types
This expression only supports:

- UserDefinedType[_] - Any user-defined type that extends the UDT base class

## Algorithm
The expression evaluation follows these steps:

- Validates that the input expression has a UserDefinedType data type
- During type checking, ensures the child expression is indeed a UDT
- Returns the underlying sqlType of the UserDefinedType as the output data type
- In evaluation, performs a pass-through operation returning the input value unchanged
- The unwrapping is purely a type-level operation exposing the underlying representation

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data distribution since it's a type-level transformation
- Preserves partition keys and ordering properties

## Edge Cases

- Null handling: Preserves null values as-is through `nullSafeEval`
- Type validation: Throws `DataTypeMismatch` error if child expression is not a UserDefinedType
- Pass-through evaluation: The actual data values remain unchanged, only the type interpretation changes
- Code generation: Delegates entirely to the child expression's code generation

## Code Generation
This expression fully supports Tungsten code generation by delegating to its child expression's `genCode` method. No fallback to interpreted mode occurs at this level.

## Examples
```sql
-- Not directly accessible in SQL
-- Applied automatically by Catalyst optimizer
```

```scala
// Internal usage during catalyst optimization
// Not exposed through public DataFrame API
import org.apache.spark.sql.catalyst.expressions.UnwrapUDT

// This would be used internally when processing UDT columns
val unwrapped = UnwrapUDT(udtExpression)
```

## See Also

- UserDefinedType base class
- Catalyst expression optimization rules
- Type coercion expressions