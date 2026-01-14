# CollationKey

## Overview
The `CollationKey` expression generates collation-specific byte arrays for string values to enable binary-stable comparisons and sorting operations for non-binary collations. This expression is primarily used internally by the Catalyst optimizer to transform string operations into efficient byte array operations while preserving collation semantics.

## Syntax
This expression is primarily used internally by Spark's Catalyst optimizer and is not directly exposed as a SQL function. It is automatically injected during query planning for operations involving non-binary collated strings.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Expression | The string expression to generate collation key bytes for |

## Return Type
`BinaryType` - Returns a byte array representing the collation key for the input string.

## Supported Data Types
- `StringType` with any collation (the expression specifically expects `StringTypeWithCollation` with trim collation support)
- Automatically handles `StructType`, `ArrayType` containing non-binary collated strings through recursive injection

## Algorithm
- Extracts the collation ID from the input string expression's data type
- Delegates to `CollationFactory.getCollationKeyBytes()` to generate the binary collation key
- For complex types (structs, arrays), recursively processes nested fields/elements
- Preserves null values through null-safe evaluation
- Uses binary-stable transformations to enable efficient comparisons

## Partitioning Behavior
- **Preserves partitioning**: The transformation maintains data distribution characteristics since collation keys preserve ordering relationships
- **No shuffle required**: The expression operates on individual rows without requiring data redistribution
- **Binary stability**: Enables hash-based operations and partitioning on the resulting byte arrays

## Edge Cases
- **Null handling**: Null input values are preserved as null outputs through `nullSafeEval`
- **Complex type nullability**: For struct types, wraps transformed structs with null checks when the original expression is nullable
- **Binary-stable types**: Skips transformation for types that are already binary-stable (checked via `UnsafeRowUtils.isBinaryStable`)
- **Map types**: Explicitly not supported as joins are not supported on map types
- **Unchanged transformations**: Returns original expression if recursive processing yields no changes

## Code Generation
**Supports code generation**: The expression implements `doGenCode()` and generates efficient Java code that directly calls `CollationFactory.getCollationKeyBytes()` with the collation ID as a compile-time constant.

## Examples
```sql
-- CollationKey is not directly callable in SQL
-- It's automatically injected for operations like:
SELECT * FROM table1 t1 JOIN table2 t2 ON t1.name_utf8_lcase = t2.name_utf8_lcase
-- Internal transformation converts collated string comparisons to binary key comparisons
```

```scala
// DataFrame API - automatic injection during optimization
import org.apache.spark.sql.catalyst.expressions.CollationKey

// Internal usage during expression transformation
val stringExpr: Expression = // some string expression with collation
val collationKeyExpr = CollationKey(stringExpr)

// Recursive injection for complex expressions
val transformedExpr = CollationKey.injectCollationKey(originalExpr)
```

## See Also
- `CollationFactory` - Factory class for collation operations and key generation
- `StringTypeWithCollation` - String type with collation metadata
- `UnsafeRowUtils.isBinaryStable` - Utility for checking binary stability of data types
- `ArrayTransform` - Used for processing array elements recursively
- `CreateNamedStruct` - Used for reconstructing struct types after field transformation