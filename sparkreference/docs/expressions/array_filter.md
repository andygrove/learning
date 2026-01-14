# ArrayFilter

## Overview

ArrayFilter is a higher-order function expression that filters elements from an array based on a lambda predicate function. It applies the given lambda function to each element (and optionally its index) in the input array, returning a new array containing only the elements for which the predicate returns true.

## Syntax

```sql
filter(array, lambda_function)
-- With element only
filter(array, x -> condition)
-- With element and index (since 3.0.0)
filter(array, (x, i) -> condition)
```

```scala
// DataFrame API
col("array_column").filter(lambda_function)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| argument | Expression (ArrayType) | The input array expression to be filtered |
| function | Expression (LambdaFunction) | Lambda function that takes 1-2 arguments (element, optional index) and returns Boolean |

## Return Type

Returns the same ArrayType as the input argument, preserving the element type and nullability characteristics of the original array.

## Supported Data Types

Supports arrays of any element type:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- String types
- Date/Timestamp types  
- Complex types (StructType, ArrayType, MapType)
- User-defined types

The lambda function must return BooleanType.

## Algorithm

- Iterates through each element in the input array sequentially
- For each element, sets the element variable (and index variable if provided) in the lambda function scope
- Evaluates the lambda predicate function for the current element
- If the predicate returns true, adds the element to the output buffer
- Returns a new GenericArrayData containing only the filtered elements

## Partitioning Behavior

ArrayFilter preserves partitioning behavior:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be executed locally on each partition

## Edge Cases

- **Null arrays**: Returns null when the input array is null
- **Empty arrays**: Returns an empty array of the same type
- **Null elements**: Null elements are passed to the lambda function; nullability is preserved from input
- **Lambda exceptions**: Runtime exceptions in the lambda function will propagate and fail the query
- **Index bounds**: Index parameter (when used) is guaranteed to be within [0, array.length-1]

## Code Generation

This expression extends `CodegenFallback`, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode for all operations.

## Examples

```sql
-- Filter even numbers
SELECT filter(array(1, 2, 3, 4, 5), x -> x % 2 = 0);
-- Result: [2, 4]

-- Filter elements at even indices (using index parameter)
SELECT filter(array('a', 'b', 'c', 'd'), (x, i) -> i % 2 = 0);
-- Result: ['a', 'c']

-- Filter null values
SELECT filter(array(1, null, 3, null, 5), x -> x IS NOT NULL);
-- Result: [1, 3, 5]
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Filter positive numbers
df.select(expr("filter(numbers, x -> x > 0)"))

// Filter based on string length
df.select(expr("filter(words, w -> length(w) > 3)"))

// Using index to filter first half of array
df.select(expr("filter(items, (item, idx) -> idx < size(items) / 2)"))
```

## See Also

- `ArrayTransform` - applies transformation function to array elements
- `ArrayExists` - checks if any array element satisfies a condition  
- `ArrayForAll` - checks if all array elements satisfy a condition
- `ArrayAggregate` - reduces array elements to a single value