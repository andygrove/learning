# ArrayAggregate

## Overview
ArrayAggregate is a higher-order function that reduces an array to a single value by applying a merge function to each element with an accumulator, then applying a finish function to the final accumulator. It's equivalent to a fold operation followed by a transformation on arrays.

## Syntax
```sql
aggregate(array_expr, initial_value, merge_function, finish_function)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array_expr | ArrayType | The input array to aggregate |
| initial_value | AnyDataType | The initial accumulator value |
| merge_function | LambdaFunction | Function that takes (accumulator, element) and returns new accumulator |
| finish_function | LambdaFunction | Function that transforms the final accumulator to the result |

## Return Type
The data type returned by the `finish_function` expression.

## Supported Data Types

- **Array**: Any ArrayType for the input array
- **Initial Value**: Any data type for the initial accumulator
- **Accumulator**: Must maintain consistent type throughout merge operations
- **Result**: Determined by the finish function's return type

## Algorithm

- Initialize accumulator with the `initial_value`
- Iterate through each element in the input array
- Apply `merge_function(accumulator, element)` to update the accumulator
- After processing all elements, apply `finish_function(accumulator)` to get final result
- Return null if the input array is null

## Partitioning Behavior
How this expression affects partitioning (if applicable):

- Preserves partitioning as it operates on individual array values within rows
- Does not require shuffle operations
- Each array is processed independently within its partition

## Edge Cases

- **Null Array**: Returns null if the input array is null
- **Empty Array**: Processes zero elements, applies finish function to initial value
- **Null Elements**: Null array elements are passed to the merge function as-is
- **Type Consistency**: The merge function output type must match the initial value type structurally
- **Nullable Accumulator**: Always treats accumulator as nullable for safety

## Code Generation
This expression extends `CodegenFallback`, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode.

## Examples
```sql
-- Sum array elements with final multiplication
SELECT aggregate(array(1, 2, 3), 0, (acc, x) -> acc + x, acc -> acc * 10);
-- Result: 60

-- Concatenate strings with prefix
SELECT aggregate(array('a', 'b', 'c'), '', (acc, x) -> concat(acc, x), acc -> concat('prefix:', acc));
-- Result: 'prefix:abc'

-- Find maximum with default handling
SELECT aggregate(array(5, 2, 8, 1), 0, (acc, x) -> greatest(acc, x), acc -> acc);
-- Result: 8
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  expr("aggregate(numbers, 0, (acc, x) -> acc + x, acc -> acc * 2)")
).show()

// Using higher-order functions API
df.select(
  aggregate(
    col("array_col"), 
    lit(0), 
    (acc, x) => acc + x,
    acc => acc * 2
  )
).show()
```

## See Also

- `array_reduce` - Simplified version without finish function
- `transform` - Apply function to each array element
- `filter` - Filter array elements with predicate
- `exists` - Check if any array element satisfies condition