# Flatten

## Overview
The `flatten` expression transforms a nested array (array of arrays) into a single-level array by concatenating all inner arrays. It flattens exactly one level of nesting, converting `Array[Array[T]]` to `Array[T]`.

## Syntax
```sql
flatten(array_of_arrays)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.flatten
df.select(flatten(col("nested_array")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array_of_arrays | Array[Array[T]] | A nested array where each element is itself an array |

## Return Type
Returns an array with the same element type as the inner arrays. If the input is `Array[Array[T]]`, the output is `Array[T]`.

## Supported Data Types

- Array of arrays with any element type (numeric, string, complex types, etc.)
- The inner arrays must all have the same element type
- Supports nested arrays with nullable elements

## Algorithm

- Validates that input is an array of arrays during type checking
- Counts total number of elements across all inner arrays
- Checks if total element count exceeds maximum array length limit
- Creates a new flat array and copies elements from each inner array sequentially
- Returns null if any inner array is null (null-intolerant behavior)

## Partitioning Behavior
This expression does not affect partitioning:

- Preserves existing partitioning schemes
- Does not require data shuffling
- Operates row-by-row within each partition

## Edge Cases

- **Null handling**: Returns null if the input array is null or if any inner array is null
- **Empty arrays**: Empty inner arrays are skipped, contributing no elements to the result
- **Size limits**: Throws `QueryExecutionErrors.arrayFunctionWithElementsExceedLimitError` if flattened array would exceed `ByteArrayMethods.MAX_ROUNDED_ARRAY_LENGTH`
- **Type validation**: Fails at analysis time if input is not an array of arrays
- **Nullable elements**: Preserves nullability of inner array elements in the result

## Code Generation
This expression supports Tungsten code generation (`doGenCode`) for optimized execution. It generates specialized code for:

- Counting total elements across inner arrays
- Allocating the result array with proper size
- Copying elements using nested loops with bounds checking

## Examples
```sql
-- Flatten array of arrays
SELECT flatten(array(array(1, 2), array(3, 4)));
-- Result: [1, 2, 3, 4]

-- With empty inner arrays
SELECT flatten(array(array(1, 2), array(), array(3)));
-- Result: [1, 2, 3]

-- With null handling
SELECT flatten(array(array(1, 2), null, array(3)));
-- Result: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = Seq(
  Seq(Seq(1, 2), Seq(3, 4)),
  Seq(Seq(5), Seq(6, 7, 8))
).toDF("nested_arrays")

df.select(flatten(col("nested_arrays"))).show()
// +-------------------+
// |flatten(nested_arrays)|
// +-------------------+
// |        [1, 2, 3, 4]|
// |     [5, 6, 7, 8]   |
// +-------------------+
```

## See Also

- `array()` - Creates arrays from individual elements
- `explode()` - Converts array elements to separate rows  
- `array_contains()` - Checks if array contains a value
- `size()` - Returns the size of an array