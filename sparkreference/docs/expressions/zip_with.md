# ZipWith

## Overview
The `ZipWith` expression combines two arrays element-wise using a lambda function to produce a single result array. It applies the provided function to corresponding elements from both input arrays, with the result array length being the maximum of the two input array lengths.

## Syntax
```sql
zip_with(array1, array2, (left_elem, right_elem) -> expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | ArrayType | The first input array |
| right | ArrayType | The second input array |
| function | LambdaFunction | A lambda function that takes two arguments (left element, right element) and returns a single value |

## Return Type
Returns an `ArrayType` where the element type matches the return type of the lambda function. The nullability of the result array elements is determined by the nullability of the lambda function's return type.

## Supported Data Types
- **Input arrays**: Any `ArrayType` with any element data type
- **Lambda function parameters**: The lambda function receives elements with the same data types as the input arrays
- **Lambda function return**: Any data type (`AnyDataType`)

## Algorithm

- Evaluates both input arrays and returns null if either array is null
- Determines result length as the maximum of both input array lengths
- Iterates through indices from 0 to result length
- For each index, sets lambda variables to corresponding array elements (or null if index exceeds array bounds)
- Applies the lambda function to generate each result element

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates element-wise on arrays within each row
- Does not require shuffle operations since computation is local to each partition

## Edge Cases

- **Null arrays**: Returns null if either input array is null
- **Empty arrays**: If both arrays are empty, returns an empty array
- **Mismatched lengths**: Uses null values for missing elements when arrays have different lengths
- **Null elements**: Lambda function receives actual null values for out-of-bounds indices or null array elements
- **Lambda function nulls**: Result array can contain null elements if the lambda function returns null

## Code Generation
This expression uses `CodegenFallback`, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode for all operations.

## Examples
```sql
-- Combine two arrays by adding corresponding elements
SELECT zip_with(array(1, 2, 3), array(4, 5, 6), (x, y) -> x + y);
-- Result: [5, 7, 9]

-- Handle arrays of different lengths
SELECT zip_with(array(1, 2), array(10, 20, 30), (x, y) -> coalesce(x, 0) + coalesce(y, 0));
-- Result: [11, 22, 30]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  zip_with(
    col("array1"), 
    col("array2"), 
    (x, y) => x + y
  )
)
```

## See Also

- `transform` - Apply function to single array elements
- `array_zip` - Zip arrays into struct array without custom function
- `filter` - Filter array elements using lambda function
- `aggregate` - Reduce array elements using lambda function