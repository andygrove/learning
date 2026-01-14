# ArrayInsert

## Overview
The ArrayInsert expression inserts an element into an array at a specified position, returning a new array with the element inserted. It supports both positive and negative indexing, with special handling for positions that extend beyond the current array bounds by padding with null values.

## Syntax
```sql
array_insert(array, pos, item)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The source array to insert an element into |
| pos | IntegerType | The 1-based position where to insert the element (supports negative indexing) |
| item | Any (compatible with array element type) | The element to insert into the array |

## Return Type
Returns an `ArrayType` with the same element type as the input array, but marked as nullable since out-of-range positions will add null values.

## Supported Data Types

- **Array**: Any `ArrayType` with elements of any data type
- **Position**: Any integral type except `LongType` (coerced to `IntegerType`)
- **Item**: Must be compatible with the array's element type through type coercion

## Algorithm

- Validates that position is not zero (throws error for zero-based indexing)
- For positive positions: inserts at the specified 1-based index, shifting existing elements right
- For negative positions: calculates position from the end of the array, with legacy mode differences
- When position extends beyond array bounds: creates a larger array and fills gaps with null values
- Enforces maximum array length limits to prevent memory issues
- Uses type coercion to find the tightest common type between array elements and the new item

## Partitioning Behavior
This expression preserves partitioning as it operates on individual array values within each partition:

- Does not require shuffle operations
- Maintains existing data distribution
- Can be executed locally on each partition

## Edge Cases

- **Null Arrays**: Returns null if the input array is null
- **Null Position**: Returns null if the position parameter is null
- **Zero Position**: Throws `invalidIndexOfZeroError` (1-based indexing required)
- **Out-of-bounds Positive**: Extends array with nulls between last element and insertion point
- **Out-of-bounds Negative**: Places item at beginning and shifts original array contents right
- **Legacy Mode**: Controlled by `legacyNegativeIndexInArrayInsert` configuration for backward compatibility
- **Array Size Limits**: Throws error if resulting array exceeds `MAX_ROUNDED_ARRAY_LENGTH`
- **Type Compatibility**: Performs automatic type coercion between item and array element types

## Code Generation
This expression supports full Tungsten code generation with optimized paths:

- Generates specialized code for compile-time known positive positions
- Includes runtime bounds checking and error handling
- Optimizes array allocation and element copying operations
- Falls back to interpreted mode only in case of code generation failures

## Examples
```sql
-- Insert at positive position
SELECT array_insert(array(1, 2, 3), 2, 'X');
-- Result: [1, 'X', 2, 3]

-- Insert at negative position (from end)
SELECT array_insert(array(5, 3, 2, 1), -4, 4);
-- Result: [5, 4, 3, 2, 1]

-- Insert beyond bounds (creates nulls)
SELECT array_insert(array(1, 2), 5, 'X');
-- Result: [1, 2, null, null, 'X']
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(array_insert(col("my_array"), lit(2), lit("new_item")))
```

## See Also

- `array_append` - Add element to end of array
- `array_prepend` - Add element to beginning of array
- `array_remove` - Remove elements from array
- `slice` - Extract portion of array