# ArrayContains

## Overview

The `ArrayContains` expression checks whether an array contains a specific value. It performs an element-wise comparison using ordering semantics and returns a boolean result indicating presence of the value in the array.

## Syntax

```sql
array_contains(array_expr, value_expr)
```

```scala
// DataFrame API
col("array_column").contains(value)
// or using function
array_contains(col("array_column"), lit(value))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| left | ArrayType | The array expression to search within |
| right | Any comparable type | The value to search for in the array |

## Return Type

Returns `BooleanType` - `true` if the value is found, `false` if not found, `null` if the result is indeterminate due to null values.

## Supported Data Types

The expression supports arrays of any data type that has ordering semantics, including:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- StringType
- DateType and TimestampType
- BooleanType
- Complex types with defined ordering

The array element type and search value type must be compatible through type coercion rules.

## Algorithm

- Iterates through each element in the input array using `ArrayData.foreach()`
- Compares each non-null element with the search value using `Ordering.equiv()`
- Returns `true` immediately when a matching element is found
- Tracks presence of null elements during iteration
- Returns `null` if no match found but null elements exist (indeterminate result)
- Returns `false` if no match found and no null elements exist

## Partitioning Behavior

This expression does not affect partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

**Null Handling:**
- Returns `null` if either the array or search value is null
- Returns `null` if array contains null elements and no match is found
- Null elements in array are tracked but not compared for equality

**Empty Array:**
- Returns `false` for empty arrays (no elements to match)

**Type Compatibility:**
- Throws `DataTypeMismatch` error if array element type and search value type are incompatible
- Throws `DataTypeMismatch` error if either input is `NullType`
- Uses type coercion to find wider compatible types when possible

## Code Generation

This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized Java code for the containment check
- Uses `nullSafeCodeGen` to handle null safety efficiently
- Implements loop unrolling for array iteration in generated code
- Optimizes null checking logic based on array nullability

## Examples

```sql
-- Basic usage
SELECT array_contains(array(1, 2, 3), 2);
-- Returns: true

-- With null elements
SELECT array_contains(array(1, null, 3), 2);  
-- Returns: null (indeterminate)

-- String arrays
SELECT array_contains(array('a', 'b', 'c'), 'b');
-- Returns: true

-- Not found
SELECT array_contains(array(1, 2, 3), 5);
-- Returns: false
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(array_contains(col("numbers"), lit(42)))

// Using column method
df.select(col("array_col").contains(lit("search_value")))

// With complex expressions  
df.filter(array_contains(col("tags"), col("search_tag")))
```

## See Also

- `ArrayPosition` - finds the position of an element in an array
- `ArrayExists` - checks if any element satisfies a predicate
- `ArraysOverlap` - checks if two arrays have common elements
- `In` - checks membership in a list of values