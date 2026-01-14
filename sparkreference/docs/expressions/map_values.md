# MapValues

## Overview
The `MapValues` expression extracts all values from a map data structure and returns them as an array. This is a unary expression that operates on map-type columns and preserves the original order of values as they appear in the map.

## Syntax
```sql
map_values(map_expr)
```

```scala
// DataFrame API
df.select(map_values(col("map_column")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | A map expression from which to extract values |

## Return Type
Returns an `ArrayType` containing elements of the same type as the map's value type. The array element type matches the `valueType` of the input `MapType`.

## Supported Data Types

- Input: `MapType` only
- Output: `ArrayType` with element type matching the map's value type

## Algorithm

- Validates that the input expression is of `MapType`
- Extracts the underlying `MapData` from the input map
- Calls the `valueArray()` method on the `MapData` to retrieve all values
- Returns the values as an array while preserving their original order
- Applies null-safe evaluation semantics

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data partitioning since it's a column-wise transformation
- Can be pushed down to individual partitions for parallel processing

## Edge Cases

- **Null handling**: The expression is null-intolerant, meaning if the input map is null, the result will be null
- **Empty map behavior**: Returns an empty array when applied to an empty map
- **Duplicate values**: All values are preserved in the output array, including duplicates
- **Value ordering**: The order of values in the resulting array matches the internal ordering of the map

## Code Generation
This expression supports Tungsten code generation for optimized performance. It uses the `nullSafeCodeGen` method to generate efficient Java code that directly calls the `valueArray()` method on the MapData object.

## Examples
```sql
-- Extract values from a map literal
SELECT map_values(map(1, 'a', 2, 'b'));
-- Result: ["a", "b"]

-- Extract values from a map column
SELECT map_values(properties) FROM users;

-- Use in combination with other functions
SELECT explode(map_values(user_attributes)) FROM user_data;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract values from map column
df.select(map_values(col("user_properties")))

// Create map and extract values
df.select(map_values(map(lit("key1"), lit("value1"), lit("key2"), lit("value2"))))
```

## See Also

- `map_keys()` - Extract keys from a map
- `map_entries()` - Convert map to array of key-value structs
- `explode()` - Explode array elements into separate rows
- `map()` - Create map from key-value pairs