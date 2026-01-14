# MapFromArrays

## Overview
The MapFromArrays expression creates a map by using elements from two arrays as key-value pairs. It takes two array expressions where the first array provides the keys and the second array provides the corresponding values, combining them into a single map structure.

## Syntax
```sql
map_from_arrays(keys_array, values_array)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression (Array) | Array expression that provides the keys for the resulting map |
| right | Expression (Array) | Array expression that provides the values for the resulting map |

## Return Type
Returns a `MapType` where the key type matches the element type of the left array and the value type matches the element type of the right array.

## Supported Data Types

- Keys array: Any array type with elements that can serve as map keys (must be hashable)
- Values array: Any array type 
- Both arrays must have compatible lengths for successful evaluation
- Supports nested and complex data types as values

## Algorithm

- Evaluates both left and right array expressions to get the key and value arrays
- Validates that both arrays have the same length
- Iterates through both arrays simultaneously, pairing each key with its corresponding value
- Constructs a map data structure with the key-value pairs
- Returns the resulting map or null if either input array is null

## Partitioning Behavior
How this expression affects partitioning (if applicable):

- Preserves existing partitioning as it operates row-by-row without requiring data movement
- Does not require shuffle operations since it's a local transformation on each row

## Edge Cases

- Returns null if either the keys array or values array is null
- Throws runtime exception if the two input arrays have different lengths
- If duplicate keys exist in the keys array, the last occurrence's value will be retained in the map
- Empty arrays (length 0) for both inputs will produce an empty map
- Null elements within the keys array will result in null keys in the map

## Code Generation
This expression likely supports Whole-Stage Code Generation (Tungsten) for optimized execution, as it performs straightforward array iteration and map construction operations that can be efficiently compiled to Java bytecode.

## Examples
```sql
-- Create a map from two arrays
SELECT map_from_arrays(array(1.0, 3.0), array('2', '4'));
-- Result: {1.0:"2", 3.0:"4"}

-- Using with column references
SELECT map_from_arrays(key_column, value_column) FROM table_name;

-- Nested in other expressions
SELECT map_from_arrays(array('a', 'b'), array(1, 2)) as my_map;
-- Result: {"a":1, "b":2}
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_from_arrays(col("keys_array"), col("values_array")))

// Creating literal arrays
df.select(map_from_arrays(
  array(lit("key1"), lit("key2")), 
  array(lit(100), lit(200))
))
```

## See Also

- `map()` - Creates maps from alternating key-value arguments
- `map_keys()` - Extracts keys from an existing map
- `map_values()` - Extracts values from an existing map
- Array functions like `array()` for creating input arrays