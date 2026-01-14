# ArrayBinarySearch

## Overview
ArrayBinarySearch performs a binary search operation on a sorted array to find the index of a specified value. It returns the index of the element if found, or a negative value indicating the insertion point if not found, following Java's Arrays.binarySearch semantics.

## Syntax
```sql
array_binary_search(array, value)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The sorted array to search in |
| value | Compatible with array element type | The value to search for in the array |

## Return Type
IntegerType - Returns the index of the found element or negative insertion point.

## Supported Data Types
The array element type and search value must be compatible types that support ordering operations:

- Numeric types (IntegerType, LongType, FloatType, DoubleType, etc.)
- StringType  
- DateType
- TimestampType
- Any type that has a defined ordering

The expression uses type coercion to find the tightest common type between the array element type and search value type.

## Algorithm
The expression is implemented as a RuntimeReplaceable that delegates to Java's binary search:

- For primitive types: Uses Arrays.binarySearch directly on the converted Java array
- For complex types: Uses Arrays.binarySearch with a custom Comparator based on Spark's PhysicalDataType.ordering
- Converts the Spark array to a Java array using ToJavaArray
- Invokes ArrayExpressionUtils.binarySearch via StaticInvoke
- Returns standard binary search semantics: exact index if found, or -(insertion_point + 1) if not found

## Partitioning Behavior
This expression does not affect partitioning:

- Preserves existing partitioning as it operates on individual array values within each partition
- Does not require shuffle operations
- Can be executed independently on each partition

## Edge Cases

- **Null array**: Throws DataTypeMismatch error with NULL_TYPE subclass
- **Null search value**: Throws DataTypeMismatch error with NULL_TYPE subclass  
- **Null elements in array**: Handled by custom comparator where nulls are ordered before non-null values
- **Empty array**: Returns -1 (standard binary search behavior for empty collections)
- **Unsorted array**: Undefined behavior as binary search requires sorted input
- **Incompatible types**: Throws DataTypeMismatch error with ARRAY_FUNCTION_DIFF_TYPES subclass

## Code Generation
This expression does not use Tungsten code generation. It is implemented as a RuntimeReplaceable that generates a StaticInvoke expression calling into ArrayExpressionUtils.binarySearch, which executes in interpreted mode.

## Examples
```sql
-- Search in sorted integer array
SELECT array_binary_search(array(1, 3, 5, 7, 9), 5);
-- Returns: 2

-- Search for non-existent value  
SELECT array_binary_search(array(1.0F, 2.0F, 3.0F), 1.1F);
-- Returns: -2

-- Search in string array
SELECT array_binary_search(array('apple', 'banana', 'cherry'), 'banana');
-- Returns: 1
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("array_binary_search(sorted_array_col, search_value)"))

// With literal array
df.select(expr("array_binary_search(array(1, 3, 5, 7), 3)"))
```

## See Also

- `array_contains` - Check if array contains a value without requiring sorted order
- `sort_array` - Sort an array before performing binary search
- `array_position` - Find first occurrence of value in unsorted array