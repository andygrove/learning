# ArraySort

## Overview
ArraySort is a higher-order function expression that sorts the elements of an array using a custom comparator function. It accepts an array and a lambda function that compares two elements, returning an integer indicating their relative order.

## Syntax
```sql
array_sort(array, lambda_function)
array_sort(array)  -- uses default comparator
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| argument | ArrayType | The input array to be sorted |
| function | LambdaFunction | A lambda function that takes two elements and returns an integer for comparison (negative, zero, or positive) |
| allowNullComparisonResult | Boolean | Internal flag controlling whether null comparison results are allowed (defaults to legacy configuration) |

## Return Type
Returns an ArrayType with the same element type and nullability as the input array.

## Supported Data Types

- Input: Any ArrayType containing elements of any data type
- Lambda function must return IntegerType for comparison results
- Supports arrays with null elements when containsNull is true

## Algorithm

- Converts the input ArrayData to a Java array for sorting
- Creates a custom Comparator that evaluates the lambda function for each pair of elements
- Uses Java's Arrays.sort() method with the custom comparator
- Lambda variables are bound to the two elements being compared during evaluation
- Returns a new GenericArrayData containing the sorted elements

## Partitioning Behavior
- Preserves partitioning as it operates on individual array values within each partition
- Does not require shuffle operations
- Each array is sorted independently within its partition

## Edge Cases

- **Null arrays**: Returns null if the input array is null
- **Null elements**: Supported when the array type allows null elements
- **Null comparison results**: Throws QueryExecutionErrors.comparatorReturnsNull when allowNullComparisonResult is false and comparator returns null
- **Empty arrays**: Returns empty array unchanged
- **NullType elements**: Arrays with NullType elements are returned unsorted
- **Default comparator**: When no lambda function provided, uses ArraySort.defaultComparator

## Code Generation
This expression extends CodegenFallback, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode.

## Examples
```sql
-- Sort array in ascending order using custom comparator
SELECT array_sort(array(3, 1, 4, 1, 5), (left, right) -> 
  CASE WHEN left < right THEN -1 
       WHEN left > right THEN 1 
       ELSE 0 END);

-- Sort array in descending order
SELECT array_sort(array('c', 'a', 'b'), (left, right) -> 
  CASE WHEN left > right THEN -1 
       WHEN left < right THEN 1 
       ELSE 0 END);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  array_sort(
    col("array_column"), 
    (left, right) => when(left < right, -1)
      .when(left > right, 1)
      .otherwise(0)
  )
)
```

## See Also

- ArrayBasedSimpleHigherOrderFunction (parent class)
- LambdaFunction (for lambda expression handling)
- Other array functions: array_min, array_max, sort_array