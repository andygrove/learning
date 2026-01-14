# Shuffle

## Overview

The `Shuffle` expression randomly shuffles the elements of an array using a random number generator seeded for deterministic behavior within the same partition. This is a non-deterministic function that returns the input array with its elements reordered in a random sequence.

## Syntax

```sql
shuffle(array)
shuffle(array, seed)
```

```scala
// DataFrame API
shuffle(col("array_column"))
shuffle(col("array_column"), lit(42))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| array | ArrayType | The input array to be shuffled |
| seed | Expression (optional) | Random seed for deterministic shuffling across runs |

## Return Type

Returns an `ArrayType` with the same element type and nullability as the input array.

## Supported Data Types

- **Input**: `ArrayType` containing elements of any data type
- **Output**: Same `ArrayType` as input with preserved element types and nullability

## Algorithm

- Evaluates the input array expression to get the source `ArrayData`
- Initializes a `RandomIndicesGenerator` using the provided seed plus partition index
- Generates a random permutation of indices from 0 to array length - 1
- Creates a new `GenericArrayData` by mapping the shuffled indices to the original array elements
- Preserves null elements and array structure while only reordering positions

## Partitioning Behavior

- **Preserves partitioning**: Yes, operates element-wise within each partition
- **Requires shuffle**: No, this is a local transformation per partition
- **Seed behavior**: Uses `randomSeed + partitionIndex` to ensure different shuffling across partitions while maintaining deterministic results

## Edge Cases

- **Null array input**: Returns `null` without processing
- **Empty array**: Returns empty array (no elements to shuffle)  
- **Single element array**: Returns the same single-element array
- **Null elements**: Preserves null elements within the array structure
- **Unresolved seed**: Expression remains unresolved until seed is provided or generated

## Code Generation

Supports Tungsten code generation through the `doGenCode` method:

- Generates optimized Java code using `nullSafeCodeGen`
- Creates mutable state for `RandomIndicesGenerator` instance
- Produces inline array creation and assignment loops
- Falls back to interpreted `evalInternal` when code generation is disabled

## Examples

```sql
-- Basic array shuffling
SELECT shuffle(array(1, 2, 3, 4, 5));
-- Result: [3, 1, 5, 2, 4] (random order)

-- Deterministic shuffling with seed
SELECT shuffle(array('a', 'b', 'c'), 42);
-- Result: ['c', 'a', 'b'] (deterministic with seed 42)

-- Shuffling arrays with null elements
SELECT shuffle(array(1, null, 3, null, 5));
-- Result: [null, 1, null, 5, 3] (nulls preserved, positions shuffled)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic shuffle
df.select(shuffle(col("array_col")))

// With specific seed for reproducibility
df.select(shuffle(col("array_col"), lit(12345)))

// Chaining with other array operations
df.select(shuffle(array_distinct(col("array_col"))))
```

## See Also

- `array_sort` - Sort array elements in ascending order
- `reverse` - Reverse the order of array elements  
- `slice` - Extract a subset of array elements
- `transform` - Apply transformation to array elements