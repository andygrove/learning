# Slice

## Overview
The Slice expression extracts a subsequence from an array by specifying a starting position and length. It supports both positive and negative indexing, where negative start positions count backwards from the end of the array.

## Syntax
```sql
slice(array, start, length)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.expr
df.select(expr("slice(array_col, start_pos, num_elements)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The input array to slice |
| start | IntegerType | Starting position (1-based indexing, negative values count from end) |
| length | IntegerType | Number of elements to extract |

## Return Type
Returns the same ArrayType as the input array, preserving the element type and nullability characteristics.

## Supported Data Types

- Input array: Any ArrayType with any element data type
- Start position: IntegerType only
- Length: IntegerType only

## Algorithm

- Converts 1-based SQL indexing to 0-based internal indexing by subtracting 1 from positive start values
- Handles negative start positions by adding them to the array length to count backwards
- Validates that start is not 0 (throws error) and length is not negative (throws error)
- Returns empty array if the calculated start index is out of bounds
- Extracts elements using Scala's slice method on the underlying array data
- Truncates length if it extends beyond array boundaries

## Partitioning Behavior

- Preserves partitioning as it operates element-wise on individual arrays
- Does not require shuffle operations
- Maintains the original partitioning scheme of the DataFrame

## Edge Cases

- **Null handling**: Returns null if any input (array, start, or length) is null (nullIntolerant = true)
- **Zero start position**: Throws QueryExecutionErrors.unexpectedValueForStartInFunctionError
- **Negative length**: Throws QueryExecutionErrors.unexpectedValueForLengthInFunctionError
- **Out of bounds start**: Returns empty array if start index is before beginning or after end
- **Length exceeds bounds**: Automatically truncates to available elements
- **Empty input array**: Returns empty array regardless of start/length values

## Code Generation
Supports Tungsten code generation through the `doGenCode` method, generating optimized Java code that avoids object creation overhead and provides better performance than interpreted evaluation.

## Examples
```sql
-- Extract 2 elements starting from position 2
SELECT slice(array(1, 2, 3, 4, 5), 2, 2) AS result;
-- Returns: [2, 3]

-- Extract elements from end using negative start
SELECT slice(array(1, 2, 3, 4, 5), -2, 2) AS result;
-- Returns: [4, 5]

-- Length exceeds array bounds
SELECT slice(array(1, 2, 3), 2, 10) AS result;
-- Returns: [2, 3]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
import spark.implicits._

val df = Seq(
  Array(1, 2, 3, 4, 5)
).toDF("numbers")

df.select(expr("slice(numbers, 2, 3)").alias("sliced")).show()
// Output: [2, 3, 4]
```

## See Also

- `array_except` - Set difference between arrays
- `array_intersect` - Set intersection of arrays  
- `array_union` - Set union of arrays
- `element_at` - Extract single element from array
- `size` - Get array length