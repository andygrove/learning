# ArrayRepeat

## Overview
ArrayRepeat is a Spark Catalyst expression that creates an array by repeating a given element a specified number of times. It takes any data type as the element to repeat and an integer count to determine how many times the element should be duplicated in the resulting array.

## Syntax
```sql
array_repeat(element, count)
```

```scala
// DataFrame API
df.select(array_repeat(col("element"), col("count")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| element | Any | The element to be repeated in the array |
| count | Integer | The number of times to repeat the element |

## Return Type
Returns an `ArrayType` with the element type matching the input element's data type. The array's element nullability matches the nullability of the input element.

## Supported Data Types

- **Element**: Any data type (`AnyDataType`)
- **Count**: Integer types only (`IntegerType`)

## Algorithm

- Evaluates the count parameter first and returns null if count is null
- Validates that the count doesn't exceed `ByteArrayMethods.MAX_ROUNDED_ARRAY_LENGTH` to prevent memory issues
- Evaluates the element parameter once and reuses the same value for all array positions
- Creates a `GenericArrayData` using `Array.fill()` to efficiently populate the array
- Handles null elements by either setting all positions to null or copying the non-null value

## Partitioning Behavior
This expression does not affect partitioning as it operates on individual rows:

- Preserves existing partitioning since it's a row-level transformation
- Does not require shuffle operations
- Can be executed independently on each partition

## Edge Cases

- Returns null if the count parameter is null (nullable behavior depends on count nullability)
- Returns empty array if count is 0 or negative (negative counts are treated as 0)
- Throws `QueryExecutionErrors.createArrayWithElementsExceedLimitError` if count exceeds maximum array length
- Properly handles null elements by setting all array positions to null
- Maintains the nullability characteristics of the input element type

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized code for array allocation using `CodeGenerator.createArrayData`
- Uses efficient loops for element assignment with `CodeGenerator.setArrayElement`
- Includes null-safety checks and proper exception handling in generated code
- Avoids interpreted evaluation overhead for better performance

## Examples
```sql
-- Create array with repeated string
SELECT array_repeat('hello', 3);
-- Result: ["hello", "hello", "hello"]

-- Create array with repeated number
SELECT array_repeat(42, 2);
-- Result: [42, 42]

-- Handle null count (returns null)
SELECT array_repeat('test', null);
-- Result: null

-- Empty array for zero count
SELECT array_repeat('item', 0);
-- Result: []
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.array_repeat

df.select(array_repeat(lit("value"), col("repeat_count")))

// With column values
df.select(array_repeat(col("item"), lit(5)))
```

## See Also

- `array()` - Create arrays from multiple expressions
- `explode()` - Expand arrays into multiple rows  
- `array_contains()` - Check if array contains element
- `size()` - Get array length