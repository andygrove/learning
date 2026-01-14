# CreateNamedStruct

## Overview
CreateNamedStruct is a Catalyst expression that creates a struct (row) value from pairs of field names and values. It takes an even number of arguments where odd-positioned arguments are field names (must be string literals) and even-positioned arguments are the corresponding field values.

## Syntax
```sql
named_struct(name1, value1, name2, value2, ...)
struct(value1, value2, ...)  -- alias form
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name1, name2, ... | String literal | Field names for the struct (must be foldable string expressions) |
| value1, value2, ... | Any | Field values corresponding to each name |

## Return Type
Returns a `StructType` with fields defined by the provided name-value pairs. Each field's data type matches the corresponding value expression's data type.

## Supported Data Types
- Field names: Must be string literals or foldable string expressions
- Field values: Any data type supported by Spark SQL
- Preserves nullability of individual field expressions
- Preserves metadata from NamedExpression or GetStructField inputs

## Algorithm

- Validates that the number of arguments is even and greater than 0
- Groups arguments into name-value pairs
- Evaluates name expressions at planning time (must be foldable)
- Creates StructType with fields based on name-value pairs
- At runtime, evaluates value expressions and constructs InternalRow

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it's a row-level transformation
- Does not require shuffle operations
- Can be applied within existing partitions

## Edge Cases

- Null field names: Throws DataTypeMismatch error with UNEXPECTED_NULL subclass
- Non-string field names: Throws DataTypeMismatch error with CREATE_NAMED_STRUCT_WITHOUT_FOLDABLE_STRING subclass  
- Odd number of arguments: Throws QueryCompilationError expecting "2n (n > 0)" arguments
- Null field values: Preserves null values in the resulting struct
- The struct itself is never null (nullable = false)

## Code Generation
This expression supports Tungsten code generation. It generates optimized code that:

- Creates an Object array for field values
- Evaluates each value expression with null checking
- Constructs a GenericInternalRow from the values array
- Uses code splitting for expressions to avoid Java method size limits

## Examples
```sql
-- Create a struct with named fields
SELECT named_struct('id', 1, 'name', 'John', 'age', 25) as person;

-- Using struct alias (field names inferred)
SELECT struct(1, 'John', 25) as person;

-- With complex expressions
SELECT named_struct('total', col1 + col2, 'ratio', col1 / col2) FROM table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(struct(col("id"), col("name")).alias("person"))

// With named fields
df.select(expr("named_struct('id', id, 'name', name)").alias("person"))
```

## See Also
- CreateStruct - Creates structs without explicit field names
- GetStructField - Extracts fields from struct values
- StructType - The data type representing struct schemas