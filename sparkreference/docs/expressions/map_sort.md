# MapSort

## Overview

The `MapSort` expression sorts a map by its keys in ascending order. It takes a map as input and returns a new map with the same key-value pairs, but ordered by the natural ordering of the keys. This expression is null-intolerant, meaning it will return null if the input map is null.

## Syntax

```sql
map_sort(map_expr)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| base | MapType | The input map expression to be sorted by its keys |

## Return Type

Returns the same `MapType` as the input, with identical key and value types but with entries sorted by key.

## Supported Data Types

The input must be a `MapType` where the key type supports ordering. Supported key types include:

- Numeric types (IntegerType, LongType, FloatType, DoubleType, etc.)
- StringType 
- DateType
- TimestampType
- Any other types where `RowOrdering.isOrderable()` returns true

## Algorithm

The expression evaluates using the following steps:

- Extract keys and values from the input `MapData` into separate arrays
- Create an array of key-value tuples combining corresponding keys and values
- Sort the tuple array using the natural ordering of the key type via `PhysicalDataType.ordering`
- Extract the sorted keys and values back into separate arrays
- Construct a new `ArrayBasedMapData` with the sorted key and value arrays

## Partitioning Behavior

This expression does not affect partitioning:

- Preserves existing partitioning as it operates on individual map values
- Does not require shuffle operations
- Executes locally within each partition

## Edge Cases

- **Null handling**: Returns null if the input map is null (null-intolerant behavior)
- **Empty maps**: Returns an empty map of the same type
- **Duplicate keys**: Maintains existing behavior since maps cannot have duplicate keys by definition
- **Non-orderable keys**: Throws `DataTypeMismatch` error with `INVALID_ORDERING_TYPE` subclass
- **Wrong input type**: Throws `DataTypeMismatch` error with `UNEXPECTED_INPUT_TYPE` subclass for non-map inputs

## Code Generation

This expression supports Tungsten code generation through the `doGenCode` method:

- Generates optimized Java code using `java.util.Arrays.parallelSort()`
- Uses `SimpleEntry` objects to maintain key-value associations during sorting
- Implements custom comparator with primitive type optimizations when applicable
- Falls back to interpreted evaluation via `nullSafeEval` when code generation is disabled

## Examples

```sql
-- Sort a map by its keys
SELECT map_sort(map(3, 'c', 1, 'a', 2, 'b')) AS sorted_map;
-- Result: {1 -> 'a', 2 -> 'b', 3 -> 'c'}

-- Sort a string-keyed map
SELECT map_sort(map('zebra', 1, 'apple', 2, 'banana', 3)) AS sorted_map;
-- Result: {'apple' -> 2, 'banana' -> 3, 'zebra' -> 1}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_sort(col("map_column")))

// Creating and sorting a map
val df = spark.range(1).select(
  map_sort(map(lit(3), lit("c"), lit(1), lit("a"), lit(2), lit("b")))
)
```

## See Also

- `map_keys()` - Extract keys from a map
- `map_values()` - Extract values from a map  
- `map_from_entries()` - Create map from array of structs
- `sort_array()` - Sort arrays by element value