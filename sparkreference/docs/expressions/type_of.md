# TypeOf

## Overview
The TypeOf expression returns the Catalyst data type name of its input expression as a string. It provides a way to introspect the data type information at runtime, returning the catalog string representation of the type.

## Syntax
```sql
typeof(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("typeof(column_name)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Any | The expression whose data type should be returned |

## Return Type
`StringType` - Returns a UTF8String containing the catalog string representation of the input expression's data type.

## Supported Data Types
This expression supports all Catalyst data types as input, including:

- All primitive types (IntegerType, StringType, BooleanType, etc.)
- Complex types (ArrayType, MapType, StructType)
- Decimal types with precision and scale
- Timestamp and date types
- Binary types

## Algorithm
The TypeOf expression evaluation follows these steps:

- Accesses the `dataType` property of the child expression
- Converts the DataType to its catalog string representation using `catalogString` method
- Wraps the result in a UTF8String for return
- Since it's foldable and context-independent, the result can be computed at compile time
- Code generation produces a constant string literal for optimal performance

## Partitioning Behavior
This expression has no impact on partitioning behavior:

- Preserves existing partitioning as it doesn't depend on data values
- Does not require shuffle operations
- Can be computed independently on each partition

## Edge Cases

- **Null input values**: The expression itself is never null (`nullable = false`) regardless of whether the input expression can produce null values
- **Complex nested types**: Returns the full type specification including nested structure (e.g., "array<struct<field1:int,field2:string>>")
- **Parameterized types**: Includes type parameters like precision/scale for decimals
- **Empty containers**: Returns the container type specification regardless of content

## Code Generation
This expression supports Tungsten code generation. The `doGenCode` method generates optimized bytecode that produces a constant UTF8String literal, eliminating runtime type inspection overhead.

## Examples
```sql
-- Basic primitive type
SELECT typeof(1);
-- Result: "int"

-- Array type
SELECT typeof(array(1, 2, 3));
-- Result: "array<int>"

-- Complex nested structure  
SELECT typeof(struct(1 as id, 'name' as label));
-- Result: "struct<id:int,label:string>"
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("typeof(age)")).show()
df.select(expr("typeof(array_col)")).show()
df.withColumn("col_type", expr("typeof(some_column)"))
```

## See Also

- `schema()` - Returns schema information for DataFrames
- Column metadata and schema inspection methods in DataFrame API