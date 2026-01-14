# ArrayPosition

## Overview
The `ArrayPosition` expression finds the position of the first occurrence of a specified element within an array. It returns a 1-based index of the element's position, or 0 if the element is not found in the array.

## Syntax
```sql
array_position(array, element)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(array_position(col("array_column"), lit(value)))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The input array to search within |
| element | Any (matching array element type) | The element to find within the array |

## Return Type
`LongType` - Returns a 1-based position index as a long integer, or 0 if the element is not found.

## Supported Data Types

- Array element types must be orderable (support comparison operations)
- The search element type must be compatible with the array's element type through type coercion
- Null types are explicitly rejected and will cause a type mismatch error

## Algorithm

- Iterates through the array elements sequentially from index 0
- Uses ordering-based equality comparison to match elements with the search value
- Skips null elements in the array during comparison
- Returns the 1-based position (index + 1) of the first matching element
- Returns 0 if no matching element is found after scanning the entire array

## Partitioning Behavior
This expression operates on individual rows and does not affect partitioning:

- Preserves existing partitioning as it's a row-level operation
- Does not require shuffle operations
- Can be executed independently on each partition

## Edge Cases

- **Null array input**: Returns null due to `nullIntolerant = true`
- **Null search element**: Returns null due to `nullIntolerant = true`
- **Null elements in array**: Skipped during comparison, never match the search element
- **Empty array**: Returns 0 (no elements to match)
- **Element type mismatch**: Compile-time error with detailed type mismatch information
- **Multiple occurrences**: Only returns the position of the first occurrence

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, generating optimized Java code for array traversal and element comparison rather than falling back to interpreted evaluation.

## Examples
```sql
-- Find position of element in array
SELECT array_position(array(312, 773, 708, 708), 414);
-- Returns: 0

SELECT array_position(array(312, 773, 708, 708), 773);
-- Returns: 2

SELECT array_position(array('a', 'b', 'c', 'b'), 'b');
-- Returns: 2 (first occurrence)

-- With null values
SELECT array_position(array(1, null, 3, null), 3);
-- Returns: 3
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Find position of specific value
df.select(array_position(col("numbers"), lit(42)))

// Find position with column reference
df.select(array_position(col("items"), col("search_value")))

// Using in filter conditions
df.filter(array_position(col("tags"), lit("important")) > 0)
```

## See Also

- `array_contains` - Check if array contains an element (boolean result)
- `element_at` - Get element at specific position in array
- `array_remove` - Remove all occurrences of element from array
- `size` - Get the size/length of an array