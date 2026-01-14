# Get

## Overview
The `Get` expression retrieves an element from an array at a specified index position. It is a runtime-replaceable expression that provides safe array access without throwing exceptions for invalid indices, returning NULL instead.

## Syntax
```sql
get(array_expression, index_expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| array_expression | ArrayType | The input array from which to retrieve an element |
| index_expression | IntegerType | The zero-based index position of the element to retrieve |

## Return Type
Returns the element type of the input array. If the array contains elements of type T, the expression returns type T or NULL.

## Supported Data Types

- **Input array**: Any ArrayType with elements of any supported Spark data type
- **Index**: IntegerType only (with implicit casting applied when the first argument is ArrayType)

## Algorithm

- Validates that the first argument is an ArrayType and second argument is IntegerType
- Performs implicit type casting on the index argument when the array type is detected
- Delegates actual execution to `GetArrayItem` expression with `failOnError = false`
- Returns the array element at the specified index position
- Returns NULL for out-of-bounds access instead of throwing exceptions

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffling across partitions
- Operates on individual rows within each partition independently
- Maintains existing partition boundaries and distribution

## Edge Cases

- **Negative indices**: Returns NULL (as shown in the documentation example with index -1)
- **Out-of-bounds indices**: Returns NULL instead of throwing ArrayIndexOutOfBoundsException  
- **NULL array input**: Returns NULL
- **NULL index input**: Returns NULL
- **Empty arrays**: Any index access returns NULL

## Code Generation
This expression supports Tungsten code generation through its replacement expression `GetArrayItem`. The runtime replacement mechanism ensures optimized code generation paths are utilized during query execution.

## Examples
```sql
-- Basic array element access
SELECT get(array(1, 2, 3), 0);  -- Returns: 1
SELECT get(array(1, 2, 3), 2);  -- Returns: 3

-- Out-of-bounds access (safe)
SELECT get(array(1, 2, 3), -1); -- Returns: NULL
SELECT get(array(1, 2, 3), 5);  -- Returns: NULL

-- Working with NULL values
SELECT get(NULL, 0);             -- Returns: NULL
SELECT get(array(1, 2, 3), NULL); -- Returns: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(get(col("array_column"), lit(0)))
df.select(get(array(lit(1), lit(2), lit(3)), col("index_column")))
```

## See Also

- `GetArrayItem` - The underlying implementation expression
- `element_at` - Alternative array access function with different null handling
- Array indexing operators in SQL expressions