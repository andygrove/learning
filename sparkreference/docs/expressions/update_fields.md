# UpdateFields

## Overview
UpdateFields is a Spark Catalyst expression that modifies fields within a struct by applying a sequence of field operations. It enables adding new fields, dropping existing fields, or modifying field values and metadata in struct-typed data without recreating the entire structure.

## Syntax
```sql
-- Used internally by Spark SQL for struct field operations
-- Typically invoked through higher-level struct manipulation functions
```

```scala
// DataFrame API usage through struct manipulation functions
import org.apache.spark.sql.catalyst.expressions._
UpdateFields(structExpr, fieldOps)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| structExpr | Expression | The input struct expression to be modified |
| fieldOps | Seq[StructFieldsOperation] | Sequence of operations to apply to struct fields (add, drop, modify) |

## Return Type
Returns a `StructType` with the modified field structure based on the applied field operations.

## Supported Data Types

- Input: StructType only
- Output: StructType with potentially different field composition

## Algorithm

- Validates that the input expression is of StructType and that not all fields are being dropped
- Extracts existing field expressions from the input struct, handling both CreateNamedStruct and regular struct expressions
- Applies each field operation sequentially using foldLeft to build the new field structure
- Creates a CreateNamedStruct expression with the resulting fields and expressions
- Wraps the result in null-handling logic if the input struct is nullable

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual rows without changing data distribution
- Does not require shuffle operations
- Maintains the same number of rows and their relative positions

## Edge Cases

- **Null handling**: If the input struct is nullable, the expression wraps the result in an If statement that returns null when the input struct is null
- **Empty operations**: Validation prevents dropping all fields, which would result in an invalid empty struct
- **Type validation**: Strictly enforces that the input expression must be of StructType
- **Nested field access**: Handles both CreateNamedStruct expressions and regular struct field access patterns

## Code Generation
This expression is marked as `Unevaluable`, meaning it does not support direct code generation. Instead, it transforms into an `evalExpr` (typically a CreateNamedStruct wrapped in conditional logic) that supports Tungsten code generation.

## Examples
```sql
-- UpdateFields is used internally by struct manipulation functions
-- Example of equivalent high-level operations:
SELECT struct_col.field1, 'new_value' as field2, struct_col.field3 
FROM table_name
```

```scala
// Internal Catalyst usage
val structExpr = // some struct expression
val addFieldOp = // StructFieldsOperation to add a field  
val updateFieldsExpr = UpdateFields(structExpr, Seq(addFieldOp))

// The expression transforms to an evaluable form:
val evaluableExpr = updateFieldsExpr.evalExpr
```

## See Also

- CreateNamedStruct - Used internally to construct the final struct
- GetStructField - Used to extract existing field values
- StructFieldsOperation - Operations applied to modify struct fields
- If/IsNull - Used for null-safe struct field updates