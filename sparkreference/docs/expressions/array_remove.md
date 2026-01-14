# ArrayRemove

## Overview
The `ArrayRemove` expression removes all occurrences of a specified element from an array, returning a new array with the matching elements filtered out. It performs element-wise comparison using ordering semantics and handles null values by preserving them in the output unless they match the element to be removed.

## Syntax
```sql
array_remove(array, element)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(array_remove(col("array_column"), lit(value)))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The input array from which elements will be removed |
| element | Any (must be compatible with array element type) | The value to remove from the array |

## Return Type
Returns an `ArrayType` with the same element type and nullability as the input array, but potentially with fewer elements.

## Supported Data Types

- Input array can be of any `ArrayType` with elements of orderable types
- The element to remove must be type-compatible with the array's element type
- Both arguments undergo type coercion to find the tightest common type
- Requires that the element type supports ordering operations

## Algorithm

- Iterates through each element in the input array
- Uses ordering-based equality comparison (`ordering.equiv`) to match elements
- Preserves null elements unless the removal element is also null and matches
- Creates a new array containing only non-matching elements
- Maintains the original order of remaining elements

## Partitioning Behavior
This expression preserves partitioning since it operates element-wise on individual arrays within each partition:

- Does not require data shuffle
- Can be executed independently on each partition
- Maintains existing data distribution

## Edge Cases

- **Null array input**: Returns null (null intolerant behavior)
- **Null removal element**: Removes all null elements from the array
- **Null elements in array**: Preserved unless removal element is null
- **Empty array**: Returns empty array unchanged
- **No matches found**: Returns the original array unchanged
- **All elements match**: Returns empty array

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized bytecode for the removal operation
- Uses two-pass approach: first counts elements to remove, then builds result array
- Falls back to interpreted mode (`nullSafeEval`) when code generation is not available

## Examples
```sql
-- Remove integer from array
SELECT array_remove(array(1, 2, 3, 2, 4), 2);
-- Result: [1, 3, 4]

-- Remove null values
SELECT array_remove(array(1, null, 2, null, 3), null);
-- Result: [1, 2, 3]

-- Remove from string array
SELECT array_remove(array('a', 'b', 'c', 'b'), 'b');
-- Result: ['a', 'c']

-- No matching elements
SELECT array_remove(array(1, 2, 3), 4);
-- Result: [1, 2, 3]
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Remove specific values
df.select(array_remove(col("numbers"), lit(2)))

// Remove nulls from array column
df.select(array_remove(col("nullable_array"), lit(null)))

// Using with array literals
df.select(array_remove(array(lit(1), lit(2), lit(3)), lit(2)))
```

## See Also

- `array_distinct` - Remove duplicate elements from array
- `filter` - Filter array elements based on predicate
- `array_except` - Remove elements present in second array
- `array_union` - Combine arrays with deduplication