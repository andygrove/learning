# GetStructField

## Overview
GetStructField is a Spark Catalyst expression that extracts a specific field from a struct data type by its ordinal position. It extends UnaryExpression and implements ExtractValue to safely access nested struct fields while preserving case-sensitive field names and handling null values appropriately.

## Syntax
```sql
struct_column.field_name
```

```scala
// DataFrame API
df.select($"struct_column".getField("field_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The struct expression to extract from |
| ordinal | Int | Zero-based index position of the field within the struct |
| name | Option[String] | Optional field name for case-preserving display (defaults to None) |

## Return Type
Returns the data type of the field at the specified ordinal position within the struct schema. The return type is dynamically determined from the struct's schema definition.

## Supported Data Types

- **Input**: StructType (for the child expression), IntegralType (for ordinal access)
- **Output**: Any DataType supported by Spark SQL, determined by the struct field's schema

## Algorithm

- Validates that the child expression is of StructType through ExtractValue type checking
- Accesses the struct schema to determine the target field's data type and nullability
- Uses zero-based ordinal indexing to locate the specific field within the InternalRow representation
- Performs null-safe evaluation by checking both child nullability and field-level nullability
- Generates optimized code using Tungsten code generation when possible

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations as it only accesses local row data
- Maintains the same partitioning scheme as the input dataset
- Can be used safely in partition-wise operations

## Edge Cases

- **Null handling**: Returns null if either the parent struct is null OR the specific field is null
- **Case preservation**: Maintains original field name casing when provided via the name parameter
- **Schema resolution**: Falls back to "_ordinal" naming pattern for unresolved expressions
- **Bounds checking**: Relies on ordinal being within valid range of struct fields
- **Metadata preservation**: Maintains field-level metadata from the original struct schema

## Code Generation
This expression fully supports Tungsten code generation through the `doGenCode` method. It generates null-safe code that directly accesses InternalRow data without object creation overhead, falling back to interpreted mode only when code generation limits are exceeded.

## Examples
```sql
-- Extract year field from a date struct
SELECT date_struct.year FROM events_table;

-- Access nested struct field
SELECT user_info.address.city FROM user_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract field from struct column
df.select($"address".getField("street"))

// Multiple struct field access
df.select(
  $"person".getField("firstName"),
  $"person".getField("lastName")
)
```

## See Also

- ExtractValue - Parent trait for value extraction operations
- GetArrayItem - For extracting elements from array types  
- GetMapValue - For extracting values from map types
- UnaryExpression - Base class for single-child expressions