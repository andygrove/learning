# ArrayCompact

## Overview

The `ArrayCompact` expression removes all null elements from an array, returning a new array containing only the non-null elements in their original order. This function is implemented as a runtime replacement that internally uses `ArrayFilter` with a null-checking predicate.

## Syntax

```sql
array_compact(array_expr)
```

```scala
// DataFrame API
col("array_column").expr("array_compact(array_column)")
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| array_expr | ArrayType | The input array from which null elements will be removed |

## Return Type

Returns an `ArrayType` with the same element type as the input array, but with the `containsNull` flag set to `false` since all null elements are removed.

## Supported Data Types

Supports arrays of any element type:

- Arrays of primitive types (IntegerType, StringType, DoubleType, etc.)
- Arrays of complex types (StructType, ArrayType, MapType)
- Arrays with nullable elements (containsNull = true)

## Algorithm

- Creates a lambda function that checks if each array element is not null using `IsNotNull`
- Applies `ArrayFilter` with this lambda to remove null elements
- Wraps the result in `KnownNotContainsNull` to optimize the output array type
- The filtering preserves the original order of non-null elements
- Uses lazy evaluation for the lambda function and replacement expression

## Partitioning Behavior

- Preserves existing partitioning since it operates element-wise on arrays within each partition
- Does not require shuffle operations as the transformation is applied locally to each row
- No redistribution of data across partitions is needed

## Edge Cases

- **Null array input**: If the entire array is null, the behavior depends on the underlying `ArrayFilter` implementation
- **All null elements**: Returns an empty array if all elements in the input array are null
- **Empty array**: Returns an empty array unchanged
- **No null elements**: Returns the original array with `containsNull` set to false for type optimization

## Code Generation

This expression supports code generation through its `RuntimeReplaceable` interface. The actual code generation is handled by the underlying `ArrayFilter` and `IsNotNull` expressions, which both support Tungsten code generation for optimal performance.

## Examples

```sql
-- Remove null elements from string array
SELECT array_compact(array("a", null, "b", null, "c"));
-- Result: ["a", "b", "c"]

-- Remove null elements from integer array  
SELECT array_compact(array(1, null, 2, 3, null));
-- Result: [1, 2, 3]

-- All null elements
SELECT array_compact(array(null, null, null));
-- Result: []

-- Empty array
SELECT array_compact(array());
-- Result: []
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("array_compact(array_col)").as("compacted_array"))

// With column reference
df.select(col("array_column").expr("array_compact(array_column)"))
```

## See Also

- `ArrayFilter` - The underlying filtering mechanism used by ArrayCompact
- `array_remove` - Removes specific values from arrays
- `array_distinct` - Removes duplicate elements from arrays
- `IsNotNull` - The null-checking predicate used internally