# MapContainsKey

## Overview
The `MapContainsKey` expression checks whether a given key exists in a map. It is implemented as a runtime-replaceable expression that internally uses `ArrayContains` on the map's keys to perform the lookup.

## Syntax
```sql
map_contains_key(map_expr, key_expr)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| map_expr | MapType | The map to search in |
| key_expr | Same as map key type or compatible | The key to search for |

## Return Type
Returns `BooleanType` - `true` if the key exists in the map, `false` otherwise.

## Supported Data Types

- Map input: Any `MapType` with orderable key types
- Key input: Must be the same type as the map's key type or a type that can be coerced to it through type widening
- Null key inputs are not supported and will result in a type check error

## Algorithm

- Extracts all keys from the input map using `MapKeys(left)`
- Uses `ArrayContains` to check if the provided key exists in the keys array
- Performs type coercion if the key type can be widened to match the map's key type
- Validates that the key type supports ordering operations (required for containment check)
- Returns boolean result indicating key presence

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations
- Can be evaluated per partition independently
- Partitioning is maintained as it's a row-level transformation

## Edge Cases

- **Null key handling**: Null keys are explicitly rejected during type checking and will cause a `DataTypeMismatch` error with `NULL_TYPE` subclass
- **Type mismatch**: If key type cannot be coerced to map key type, throws `DataTypeMismatch` with `MAP_FUNCTION_DIFF_TYPES` subclass  
- **Non-orderable keys**: Key types that don't support ordering operations will fail type validation
- **Empty maps**: Returns `false` for any key lookup in empty maps
- **Null maps**: Standard null propagation rules apply - null map input returns null result

## Code Generation
This expression supports code generation through its runtime replacement mechanism. Since it's implemented as `ArrayContains(MapKeys(left), right)`, it inherits the code generation capabilities of those underlying expressions.

## Examples
```sql
-- Basic usage
SELECT map_contains_key(map(1, 'a', 2, 'b'), 1);
-- Returns: true

SELECT map_contains_key(map(1, 'a', 2, 'b'), 3);
-- Returns: false

-- With string keys  
SELECT map_contains_key(map('name', 'John', 'age', '30'), 'name');
-- Returns: true
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_contains_key(col("my_map"), lit("search_key")))

// Creating map and checking key
df.select(map_contains_key(
  map(lit("key1"), lit("value1"), lit("key2"), lit("value2")), 
  lit("key1")
))
```

## See Also

- `MapKeys` - Extracts all keys from a map
- `ArrayContains` - Underlying implementation for containment check  
- `MapValues` - Extracts all values from a map
- `ElementAt` - Retrieves value by key from map