# ArrayForAll

## Overview
The `ArrayForAll` expression tests whether all elements in an array satisfy a given predicate condition. It applies a lambda function to each element and returns true only if the predicate evaluates to true for every non-null element in the array.

## Syntax
```sql
forall(array_expression, lambda_function)
```

```scala
// DataFrame API usage
df.select(forall(col("array_column"), x => x % 2 === 0))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array_expression | ArrayType | The input array to evaluate |
| lambda_function | LambdaFunction | A lambda function that takes an array element and returns a Boolean |

## Return Type
`BooleanType` - Returns true if all elements satisfy the condition, false if any element fails the condition, or null under specific null-handling scenarios.

## Supported Data Types

- Input: Any `ArrayType` containing elements of any data type
- Lambda function must return `BooleanType`
- Array elements can be nullable

## Algorithm

- Iterates through each element in the input array sequentially
- Applies the lambda function to each array element
- Short-circuits evaluation when the first false result is encountered
- Tracks whether any null values were encountered during evaluation
- Applies specific null-handling logic based on the combination of results and null presence

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be executed independently on each partition

## Edge Cases

- **Null array**: Returns null if the input array itself is null
- **Empty array**: Returns true (vacuous truth - all zero elements satisfy the condition)
- **Null elements with all true**: Returns null if any element evaluation returns null AND all non-null evaluations return true
- **Null elements with any false**: Returns false if any element evaluation returns false, regardless of null presence
- **All null elements**: Returns null if all element evaluations return null

## Code Generation
This expression uses `CodegenFallback`, meaning it does not support Tungsten code generation and falls back to interpreted evaluation mode for all operations.

## Examples
```sql
-- All elements are even
SELECT forall(array(2, 4, 6), x -> x % 2 = 0);
-- Returns: true

-- Not all elements are even  
SELECT forall(array(2, 3, 4), x -> x % 2 = 0);
-- Returns: false

-- Contains null with all non-null elements satisfying condition
SELECT forall(array(2, null, 8), x -> x % 2 = 0);
-- Returns: null

-- Contains null but has false element
SELECT forall(array(1, null, 8), x -> x % 2 = 0);  
-- Returns: false
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Check if all numbers are positive
df.select(forall(col("numbers"), x => x > 0))

// Check if all strings have length > 3
df.select(forall(col("words"), x => length(x) > 3))
```

## See Also

- `ArrayExists` - Tests if any element satisfies a condition
- `ArrayFilter` - Filters array elements based on a predicate
- `ArrayTransform` - Transforms array elements using a lambda function