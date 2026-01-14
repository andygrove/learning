# CreateArray

## Overview
The `CreateArray` expression creates an array from a sequence of individual elements. It takes multiple input expressions as children and combines them into a single array value, handling type coercion to ensure all elements have a compatible common type.

## Syntax
```sql
array(expr1, expr2, ..., exprN)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.array
array(col("col1"), col("col2"), lit(3))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Variable number of expressions that will become array elements |
| useStringTypeWhenEmpty | Boolean | Flag determining default element type for empty arrays (StringType if true, NullType if false) |

## Return Type
`ArrayType` with element type determined by finding the common type among all input expressions. The array is marked as containing nulls if any input expression is nullable.

## Supported Data Types

- All primitive types (numeric, string, boolean, binary, date, timestamp)
- Complex types (arrays, maps, structs) 
- All input expressions must have compatible types that can be coerced to a common type

## Algorithm

- Validates that all input expressions have compatible data types using `TypeUtils.checkForSameTypeInputExpr`
- Determines the common element type using `TypeCoercion.findCommonTypeDifferentOnlyInNullFlags`
- Falls back to default element type (StringType or NullType) if no common type can be found
- Evaluates each child expression and wraps results in a `GenericArrayData` structure
- Sets containsNull flag based on whether any input expression is nullable

## Partitioning Behavior
This expression preserves partitioning as it operates row-by-row without requiring data movement:

- Preserves existing partitioning schemes
- Does not require shuffle operations
- Can be executed independently on each partition

## Edge Cases

- **Empty arrays**: Uses `defaultElementType` (StringType or NullType) based on `useStringTypeWhenEmpty` flag
- **Null elements**: Individual null values are preserved as array elements; the array itself is never null
- **Type coercion**: Automatically promotes compatible types (e.g., int and long become long array)
- **Mixed nullability**: Array is marked as containing nulls if any input expression is nullable, even if actual values are non-null

## Code Generation
This expression supports full code generation through the `doGenCode` method. It uses `GenArrayData.genCodeToCreateArrayData` to generate optimized Java code that creates the array data structure directly without interpretation overhead.

## Examples
```sql
-- Basic array creation
SELECT array(1, 2, 3);
-- Result: [1, 2, 3]

-- Mixed compatible types (promoted to double)
SELECT array(1, 2.5, 3);
-- Result: [1.0, 2.5, 3.0]

-- String array
SELECT array('a', 'b', 'c');
-- Result: ["a", "b", "c"]

-- Array with nulls
SELECT array(1, null, 3);
-- Result: [1, null, 3]

-- Empty array
SELECT array();
-- Result: []
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Create array from column values
df.select(array(col("col1"), col("col2"), col("col3")))

// Mix columns and literals
df.select(array(col("name"), lit("constant"), col("other")))

// Nested in other operations
df.select(array(col("a"), col("b")).alias("arr"))
  .filter(size(col("arr")) > 0)
```

## See Also

- `CreateMap` - Creates map structures from key-value pairs
- `CreateNamedStruct` - Creates struct objects from field name-value pairs
- `GetArrayItem` - Extracts elements from arrays by index
- `ArrayContains` - Checks if array contains specific values