# MapZipWith

## Overview

MapZipWith is a higher-order function that combines two maps by applying a lambda function to corresponding key-value pairs. It creates a new map containing the union of all keys from both input maps, where the lambda function receives the key and values from both maps (or null if a key doesn't exist in one map) to compute the resulting value.

## Syntax

```sql
map_zip_with(map1, map2, lambda_function)
```

```scala
// DataFrame API usage would be through expr() or selectExpr()
df.selectExpr("map_zip_with(map_col1, map_col2, (k, v1, v2) -> v1 + v2)")
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| left | Map | The first input map |
| right | Map | The second input map |
| function | Lambda | A three-parameter lambda function (key, value1, value2) -> result |

## Return Type

Returns a MapType with the same key type as the input maps and value type determined by the lambda function's return type.

## Supported Data Types

- Input maps must have the same key type
- Input maps can have different value types
- Lambda function can return any supported Spark data type
- Keys must be of a type that supports equality comparison

## Algorithm

- Collects all unique keys from both input maps
- For each key, retrieves the corresponding values from both maps (null if key doesn't exist)
- Applies the lambda function with parameters (key, value_from_left_map, value_from_right_map)
- Constructs a new map with the key and the lambda function's result
- Returns the combined map containing all processed key-value pairs

## Partitioning Behavior

- Preserves partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be executed locally on each partition independently

## Edge Cases

- If a key exists in only one map, the missing value is passed as null to the lambda function
- If either input map is null, the result is null
- Empty maps are handled gracefully - the result contains only keys from the non-empty map
- Lambda function must handle null values appropriately using functions like `coalesce()`
- Duplicate processing is avoided by taking the union of keys rather than iterating both maps separately

## Code Generation

This expression likely supports Tungsten code generation for the map iteration and key processing, but falls back to interpreted mode for lambda function evaluation, as higher-order functions typically require dynamic code evaluation.

## Examples

```sql
-- Combine two maps by adding values, treating missing keys as 0
SELECT map_zip_with(
  map('a', 1, 'b', 2), 
  map('b', 3, 'c', 4), 
  (k, v1, v2) -> coalesce(v1, 0) + coalesce(v2, 0)
);
-- Result: {"a":1,"b":5,"c":4}

-- Combine maps with string concatenation
SELECT map_zip_with(
  map('x', 'hello', 'y', 'world'), 
  map('y', '!', 'z', 'new'), 
  (k, v1, v2) -> concat(coalesce(v1, ''), coalesce(v2, ''))
);
-- Result: {"x":"hello","y":"world!","z":"new"}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.selectExpr("""
  map_zip_with(
    map_col1, 
    map_col2, 
    (k, v1, v2) -> coalesce(v1, 0) + coalesce(v2, 0)
  ) as combined_map
""")
```

## See Also

- `map_from_arrays` - Create maps from key and value arrays
- `map_concat` - Concatenate multiple maps
- `transform` - Apply lambda functions to arrays
- `map_filter` - Filter map entries using predicates