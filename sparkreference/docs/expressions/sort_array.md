# SortArray

## Overview
The `SortArray` expression sorts the elements of an array in either ascending or descending order. It returns a new array with the same elements sorted according to the specified ordering, with null values handled according to a consistent null-first or null-last policy.

## Syntax
```sql
sort_array(array[, ascendingOrder])
```

```scala
sort_array(col("array_column"))
sort_array(col("array_column"), lit(false)) // descending order
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `base` | ArrayType | The input array to be sorted |
| `ascendingOrder` | BooleanType | Optional. If true (default), sorts in ascending order; if false, sorts in descending order. Must be a foldable expression (constant). |

## Return Type
Returns an `ArrayType` with the same element type and nullability as the input array.

## Supported Data Types
Supports arrays containing any orderable data types:

- Numeric types (IntegerType, LongType, DoubleType, FloatType, etc.)
- String types (StringType)
- Date and timestamp types
- Binary types
- Does NOT support arrays containing non-orderable types like MapType or complex nested structures

## Algorithm

- Creates specialized comparators (`lt` for ascending, `gt` for descending) that handle null values consistently
- Converts the input ArrayData to a Java array for efficient sorting
- Uses `java.util.Arrays.parallelSort()` for performance with the appropriate comparator
- Null values are sorted to the beginning in ascending order, end in descending order
- For primitive non-nullable arrays, uses optimized primitive array sorting when possible
- Returns a new GenericArrayData or UnsafeArrayData with sorted elements

## Partitioning Behavior
This expression preserves partitioning:

- Does not require shuffle operations
- Operates on individual arrays within each partition
- Maintains the same number of rows and partitioning scheme

## Edge Cases

- **Null arrays**: Returns null if the input array is null
- **Empty arrays**: Returns an empty array of the same type
- **Arrays with all nulls**: Returns an array with all nulls in the same positions (nulls are equal in comparison)
- **Mixed null and non-null elements**: Nulls are consistently placed at the beginning (ascending) or end (descending)
- **Non-foldable ascendingOrder**: Throws DataTypeMismatch error - the ordering parameter must be a constant
- **Non-orderable element types**: Throws DataTypeMismatch error during type checking

## Code Generation
Supports full code generation (Tungsten):

- Generates optimized code paths for primitive types without nulls
- Falls back to object-based sorting for complex types or nullable elements
- Uses `UnsafeArrayData.fromPrimitiveArray()` for primitive array optimizations
- Implements custom Comparator generation for null-safe comparisons

## Examples
```sql
-- Basic ascending sort (default)
SELECT sort_array(array(3, 1, 4, 1, 5)) AS sorted;
-- Result: [1, 1, 3, 4, 5]

-- Descending sort
SELECT sort_array(array('d', 'c', 'b', 'a', null), false) AS sorted_desc;
-- Result: ['d', 'c', 'b', 'a', null]

-- With null values (ascending)
SELECT sort_array(array(3, null, 1, null, 2)) AS sorted_with_nulls;
-- Result: [null, null, 1, 2, 3]
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(sort_array(col("numbers"))).show()
df.select(sort_array(col("strings"), lit(false))).show()

// With column reference for array
df.withColumn("sorted_values", sort_array(col("value_array"))).show()
```

## See Also

- `array_sort` - Alternative function name in some Spark versions
- `array_max`, `array_min` - For finding extremes without full sorting
- `shuffle` - For randomizing array element order
- `reverse` - For reversing array element order