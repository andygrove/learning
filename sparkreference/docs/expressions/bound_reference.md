# BoundReference

## Overview

BoundReference is a leaf expression that represents a bound reference to a specific slot (column position) in an input tuple. It provides efficient access to column values by directly referencing their ordinal position after all column transformations like pruning have been completed.

## Syntax

BoundReference is an internal Catalyst expression not directly accessible through SQL syntax. It's created during query planning and optimization phases.

```scala
BoundReference(ordinal: Int, dataType: DataType, nullable: Boolean)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| ordinal | Int | The zero-based column position in the input tuple |
| dataType | DataType | The expected data type of the referenced column |
| nullable | Boolean | Whether the referenced column can contain null values |

## Return Type

Returns the data type specified in the `dataType` parameter. The actual return type matches the column's data type at the specified ordinal position.

## Supported Data Types

Supports all Spark SQL data types including:

- Primitive types (Boolean, Byte, Short, Int, Long, Float, Double)
- String and binary types
- Date and timestamp types
- Complex types (Array, Map, Struct)
- Decimal types
- User-defined types

## Algorithm

- Uses `InternalRow.getAccessor()` to create a type-specific accessor function for efficient value retrieval
- Direct ordinal-based lookup in the input row without name resolution
- Leverages specialized getters for primitive types when using UnsafeRow format
- Assumes the input tuple layout is finalized (no further column pruning will occur)
- Caches the accessor function to avoid repeated creation overhead

## Partitioning Behavior

BoundReference is partition-preserving:

- Does not require shuffle operations
- Maintains existing data partitioning
- Operates locally on each partition independently

## Edge Cases

- **Null handling**: Respects the nullable flag and properly propagates null values using the type-specific accessor
- **Invalid ordinal**: May throw IndexOutOfBoundsException if ordinal exceeds tuple width
- **Type mismatch**: Assumes the actual column type matches the specified dataType parameter
- **Code generation fallback**: Falls back to interpreted evaluation if code generation context is not available

## Code Generation

Fully supports Tungsten code generation with two execution paths:

- **With currentVars**: Reuses existing generated code variables when available
- **Without currentVars**: Generates direct row access code using `CodeGenerator.getValue()`
- Generates optimized null-checking code only when the column is nullable
- Uses Java primitive types for better performance when possible

## Examples

```sql
-- BoundReference is not directly accessible in SQL
-- It's created internally during query planning
SELECT column1, column2 FROM table1;
```

```scala
// Internal usage during Catalyst expression binding
val boundRef = BoundReference(0, IntegerType, nullable = true)
// Evaluates to the value at position 0 in the input row
val result = boundRef.eval(inputRow)
```

## See Also

- `AttributeReference` - Unbound column references by name
- `BindReferences` - Utility for converting AttributeReference to BoundReference
- `LeafExpression` - Base class for expressions with no child expressions
- `InternalRow` - The row format used for evaluation