# TransformKeys

## Overview
The `TransformKeys` expression transforms the keys of a map by applying a lambda function to each key-value pair. It creates a new map where each key is replaced by the result of the lambda function, while preserving the original values.

## Syntax
```sql
transform_keys(map_expr, lambda_function)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| map_expr | Map | The input map whose keys will be transformed |
| lambda_function | Lambda | A lambda function that takes two parameters (key, value) and returns the new key |

## Return Type
Returns a `Map` type with the same value type as the input map, but potentially different key type based on the lambda function's return type.

## Supported Data Types
The input map can have keys and values of any supported Spark data types. The lambda function determines the output key type, which must be a valid map key type (primitive types, strings, etc.).

## Algorithm

- Iterates through each key-value pair in the input map
- Applies the provided lambda function to each (key, value) pair
- Uses the lambda function result as the new key in the output map
- Preserves the original value for each transformed key
- Returns a new map with transformed keys and original values

## Partitioning Behavior
This expression preserves partitioning:

- Does not require data shuffling across partitions
- Operates independently on each partition's data
- Maintains the same partitioning scheme as the input

## Edge Cases

- Returns null if the input map is null
- Empty maps return empty maps
- If the lambda function produces duplicate keys, later entries may overwrite earlier ones
- If the lambda function returns null for a key, that entry's behavior depends on the map implementation
- The lambda function must return a valid map key type

## Code Generation
This expression supports Spark's Tungsten code generation for optimized performance when the lambda function and map operations can be compiled to Java bytecode.

## Examples
```sql
-- Transform keys by adding key and value
SELECT transform_keys(map_from_arrays(array(1, 2, 3), array(1, 2, 3)), (k, v) -> k + v);
-- Result: {2:1, 4:2, 6:3}

-- Transform string keys to uppercase
SELECT transform_keys(map('a', 1, 'b', 2), (k, v) -> upper(k));
-- Result: {'A':1, 'B':2}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(transform_keys(col("map_column"), (k, v) => k + v))

// Using lambda expressions
df.select(expr("transform_keys(map_col, (k, v) -> k * 2)"))
```

## See Also

- `transform_values` - transforms map values instead of keys
- `map_keys` - extracts all keys from a map
- `map_values` - extracts all values from a map
- `map_from_arrays` - creates a map from key and value arrays