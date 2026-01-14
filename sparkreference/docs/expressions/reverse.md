# Reverse

## Overview
The `Reverse` expression reverses the order of elements in an array or the order of characters in a string. It is a unary expression that operates on a single input and returns the reversed result while preserving the original data type.

## Syntax
```sql
REVERSE(expr)
```

```scala
// DataFrame API
col("column_name").reverse()
reverse(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression containing an array or string to be reversed |

## Return Type
Returns the same data type as the input expression:

- For `ArrayType`: Returns an `ArrayType` with the same element type and nullability
- For `StringType`: Returns a `StringType`

## Supported Data Types

- `StringType` with collation support (including trim collation support)
- `ArrayType` of any element type

## Algorithm

- For strings, delegates to the UTF8String's reverse() method which reverses character order
- For arrays, converts the ArrayData to an object array, applies Scala's reverse operation, and wraps in GenericArrayData
- Preserves the original array's element nullability characteristics
- Uses lazy evaluation pattern with `doReverse` function computed once based on data type

## Partitioning Behavior
- Preserves partitioning as it operates on individual rows without requiring data movement
- Does not require shuffle operations
- Can be executed in parallel across partitions

## Edge Cases

- **Null handling**: Expression is null-intolerant, meaning null inputs produce null outputs without evaluation
- **Empty arrays**: Returns an empty array of the same type
- **Empty strings**: Returns an empty string
- **Single element collections**: Returns the same single element unchanged
- **Array nullability**: Preserves the `containsNull` property of the original array type

## Code Generation
Supports Tungsten code generation with optimized implementations:

- **String reversal**: Generates direct call to UTF8String.reverse() method
- **Array reversal**: Generates optimized loop code that iterates through elements in reverse order using index arithmetic
- Falls back to interpreted mode (`nullSafeEval`) when code generation is disabled

## Examples
```sql
-- String reversal
SELECT REVERSE('hello') AS result;
-- Returns: 'olleh'

-- Array reversal
SELECT REVERSE(ARRAY(1, 2, 3, 4)) AS result;
-- Returns: [4, 3, 2, 1]

-- With null values in array
SELECT REVERSE(ARRAY(1, null, 3)) AS result;
-- Returns: [3, null, 1]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.reverse

// String reversal
df.select(reverse(col("name"))).show()

// Array reversal
df.select(reverse(col("numbers_array"))).show()
```

## See Also

- `array` - Create arrays
- `concat` - Concatenate arrays or strings
- `slice` - Extract array subset
- `sort_array` - Sort array elements