# GetArrayItem

## Overview
The `GetArrayItem` expression extracts an element from an array at a specified ordinal position. It performs bounds checking and supports both fail-fast (ANSI) and null-returning error handling modes depending on the SQL configuration.

## Syntax
```sql
array_column[index]
```

```scala
col("array_column").getItem(index)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The array expression from which to extract the element |
| ordinal | Expression | The zero-based index position of the element to extract |
| failOnError | Boolean | Whether to throw an exception on invalid index (defaults to SQLConf.ansiEnabled) |

## Return Type
Returns the element type of the input array. The data type is determined by `ArrayType.elementType` of the child expression.

## Supported Data Types

- **Input**: ArrayType containing elements of any data type
- **Index**: Any IntegralType (int, long, short, byte)
- **Output**: Same as the array's element type

## Algorithm

- Validates that the child expression is an ArrayType and ordinal is an IntegralType
- Converts the ordinal expression to an integer index value
- Performs bounds checking (index >= 0 and index < array.length)
- If index is out of bounds: throws exception (failOnError=true) or returns null (failOnError=false)
- If the element at the index is null, returns null
- Otherwise returns the element value at the specified index

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be pushed down to individual partitions

## Edge Cases

- **Null array**: Returns null if the input array is null
- **Null index**: Returns null if the ordinal expression evaluates to null
- **Negative index**: Throws exception (ANSI mode) or returns null (non-ANSI mode)
- **Index out of bounds**: Throws `QueryExecutionErrors.invalidArrayIndexError` (ANSI mode) or returns null
- **Null array elements**: Returns null if the element at the valid index is null, regardless of containsNull flag

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized Java code that:

- Performs null-safe evaluation using `nullSafeCodeGen`
- Includes conditional null checking for array elements when `ArrayType.containsNull` is true
- Generates different error handling branches based on the `failOnError` flag

## Examples
```sql
-- Basic array indexing
SELECT arr[0] FROM table_with_arrays;

-- Accessing nested array elements
SELECT nested_data[1][2] FROM complex_table;

-- Using with array functions
SELECT filter(array_col, x -> x > 0)[0] FROM my_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("array_column").getItem(0))

// Using with dynamic index
df.select(col("items").getItem(col("position")))

// Chaining with other array operations
df.select(array_sort(col("values")).getItem(0).alias("min_value"))
```

## See Also

- `GetMapValue` - For extracting values from map types
- `GetStructField` - For accessing struct field values
- `ArraysZip` - For combining multiple arrays
- `ElementAt` - Alternative function for array/map element access