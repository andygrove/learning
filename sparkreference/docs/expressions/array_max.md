# ArrayMax

## Overview
The ArrayMax expression returns the maximum element from an array. It compares all non-null elements in the input array using the natural ordering of the element data type and returns the largest value found.

## Syntax
```sql
array_max(array_expr)
```

```scala
// DataFrame API
col("array_column").expr("array_max(array_column)")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array_expr | ArrayType | Input array from which to find the maximum element |

## Return Type
Returns the same data type as the array elements. For example, if the input is `array<int>`, the return type is `int`. If the input is `array<string>`, the return type is `string`.

## Supported Data Types
Supports arrays containing any orderable data types:

- Numeric types (byte, short, int, long, float, double, decimal)
- String types (string, varchar, char)
- Date and timestamp types
- Boolean type
- Binary type

The element type must support ordering comparison operations.

## Algorithm
The expression evaluates the maximum using the following approach:

- Iterates through each element in the input array
- Skips null elements during comparison
- Maintains the current maximum value using the data type's natural ordering
- Uses `TypeUtils.getInterpretedOrdering()` to perform element comparisons
- Returns the final maximum value or null if no valid elements exist

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning schemes
- Does not require data shuffle as it operates on individual array values
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null array input**: Returns null if the entire input array is null
- **Empty array**: Returns null for empty arrays
- **All null elements**: Returns null if all array elements are null  
- **Mixed null/non-null**: Ignores null elements and finds maximum among non-null values
- **Single element**: Returns that element (or null if the single element is null)
- **Duplicate maximums**: Returns one instance of the maximum value

## Code Generation
This expression supports Tungsten code generation for optimized performance. The generated code:

- Uses efficient loop iteration over array elements
- Leverages `ctx.reassignIfGreater()` for optimized comparison logic
- Avoids boxing/unboxing overhead for primitive types
- Falls back to interpreted evaluation (`nullSafeEval`) when code generation is disabled

## Examples
```sql
-- Basic numeric array
SELECT array_max(array(1, 20, null, 3));
-- Result: 20

-- String array  
SELECT array_max(array('apple', 'zebra', 'banana'));
-- Result: 'zebra'

-- Array with all nulls
SELECT array_max(array(null, null));
-- Result: null

-- Empty array
SELECT array_max(array());
-- Result: null
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("array_max(numbers_array)").as("max_value"))

// With array literal
df.select(expr("array_max(array(1, 5, 3, 9, 2))").as("max_num"))
```

## See Also

- `array_min` - Find minimum element in array
- `array_sort` - Sort array elements  
- `sort_array` - Sort array in ascending/descending order
- `greatest` - Find maximum across multiple columns
- `max` - Aggregate maximum function