# ArrayTransform

## Overview
ArrayTransform is a higher-order function that applies a lambda function to each element of an array, optionally providing the element's index as a second parameter. It returns a new array with the transformed elements, where each element is the result of applying the lambda function to the corresponding element in the input array.

## Syntax
```sql
transform(array, lambda_function)
transform(array, (element) -> expression)
transform(array, (element, index) -> expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The input array to transform |
| lambda_function | LambdaFunction | A lambda function that takes 1-2 parameters (element and optionally index) and returns a transformed value |

## Return Type
Returns an `ArrayType` where the element type matches the return type of the lambda function. The array's nullability is determined by the lambda function's nullability.

## Supported Data Types
Supports arrays of any data type. The lambda function can transform elements to any other data type, allowing for flexible type conversions during the transformation process.

## Algorithm

- Iterates through each element of the input array sequentially
- For each element, sets the element variable in the lambda function context
- If the lambda function takes two parameters, also sets the index variable to the current position
- Evaluates the lambda function for the current element (and index if provided)
- Copies the result value and stores it in the corresponding position of the result array
- Returns a new GenericArrayData containing all transformed elements

## Partitioning Behavior
This expression preserves partitioning as it operates on individual arrays within each partition:

- Does not require data shuffling between partitions
- Maintains the same partitioning scheme as the input
- Each partition processes its arrays independently

## Edge Cases

- **Null arrays**: If the input array is null, the result is null
- **Null elements**: Individual null elements are passed to the lambda function; null handling depends on the lambda function implementation
- **Empty arrays**: Returns an empty array of the target type
- **Lambda function exceptions**: Any exceptions thrown by the lambda function will propagate up and fail the operation
- **Index parameter**: When using two-parameter lambda functions, the index starts at 0 and is always non-null

## Code Generation
This expression uses `CodegenFallback`, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode for all operations.

## Examples
```sql
-- Transform array elements by adding 10 to each
SELECT transform(array(1, 2, 3), x -> x + 10);
-- Result: [11, 12, 13]

-- Transform using both element and index
SELECT transform(array(1, 2, 3), (x, i) -> x + i);
-- Result: [1, 3, 5]

-- Transform strings to their lengths
SELECT transform(array('hello', 'world'), x -> length(x));
-- Result: [5, 5]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Transform array column
df.select(transform(col("numbers"), x => x + 10))

// Transform with index
df.select(transform(col("values"), (x, i) => x + i))
```

## See Also

- `filter` - Filters array elements based on a predicate
- `aggregate` - Reduces array elements to a single value
- `exists` - Checks if any array element satisfies a condition
- `forall` - Checks if all array elements satisfy a condition