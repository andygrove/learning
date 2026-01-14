# ArrayMin

## Overview

ArrayMin is a Spark Catalyst expression that returns the minimum element from an array. It compares all non-null elements within the input array and returns the smallest value according to the element's natural ordering. This expression has been available since Spark 2.4.0 and is part of the array functions group.

## Syntax

```sql
array_min(array_expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.array_min
df.select(array_min(col("array_column")))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| array_expr | ArrayType | An array expression containing elements of any orderable data type |

## Return Type

Returns the same data type as the array's element type. For example, if the input is `ArrayType(IntegerType)`, the return type is `IntegerType`.

## Supported Data Types

The expression supports arrays containing any data type that has a defined ordering, including:

- Numeric types (IntegerType, LongType, DoubleType, FloatType, DecimalType, etc.)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Binary types (BinaryType)
- Boolean types (BooleanType)

## Algorithm

- Iterates through each element in the input array sequentially
- Skips null elements during comparison
- Maintains the current minimum value using the data type's interpreted ordering
- Updates the minimum when a smaller non-null element is found
- Returns null if all elements are null or if the array is empty

## Partitioning Behavior

This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be executed independently on each partition

## Edge Cases

- **Null array input**: Returns null when the input array itself is null
- **Empty array**: Returns null for empty arrays
- **All null elements**: Returns null when all array elements are null
- **Mixed null/non-null**: Ignores null elements and finds minimum among non-null values
- **Single element**: Returns that element if non-null, otherwise returns null
- **Duplicate minimums**: Returns one instance of the minimum value

## Code Generation

This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized Java code that:

- Performs efficient loop iteration over array elements
- Uses type-specific comparisons via `ctx.reassignIfSmaller`
- Avoids boxing/unboxing overhead for primitive types
- Falls back to interpreted evaluation (`nullSafeEval`) when code generation is not available

## Examples

```sql
-- Basic usage with integers
SELECT array_min(array(1, 20, null, 3));
-- Result: 1

-- Empty array
SELECT array_min(array());
-- Result: null

-- All nulls
SELECT array_min(array(null, null));
-- Result: null

-- String array
SELECT array_min(array('banana', 'apple', 'cherry'));
-- Result: 'apple'
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Integer array
df.select(array_min(array(lit(1), lit(20), lit(null), lit(3))))

// From existing column
df.select(array_min(col("numbers_array")))

// With other transformations
df.select(array_min(split(col("csv_string"), ",")))
```

## See Also

- `ArrayMax` - Returns the maximum element from an array
- `SortArray` - Sorts array elements in ascending or descending order
- `ArraySort` - Sorts array with custom ordering
- `Size` - Returns the size of an array