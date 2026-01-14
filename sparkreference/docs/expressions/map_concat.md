# MapConcat

## Overview
MapConcat is a Catalyst expression that concatenates multiple maps into a single map. It takes a sequence of map expressions as input and merges them together, with later maps overwriting values for duplicate keys from earlier maps.

## Syntax
```sql
map_concat(map1, map2, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Variable number of map expressions to be concatenated |

## Return Type
Returns a MapType with the same key and value types as the input maps.

## Supported Data Types
Supports MapType expressions where:

- All input maps must have compatible key types
- All input maps must have compatible value types
- Keys can be any comparable data type
- Values can be any Spark SQL data type

## Algorithm
The expression evaluates by:

- Iterating through each input map expression in order
- Creating a new result map starting with the first map's contents
- For each subsequent map, adding all key-value pairs to the result
- When duplicate keys are encountered, the value from the later map overwrites the earlier value
- Returns the final merged map containing all unique keys with their most recent values

## Partitioning Behavior
This expression has neutral partitioning behavior:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be executed locally on each partition

## Edge Cases

- **Null handling**: If any input map is null, the result will be null
- **Empty maps**: Empty maps are ignored in the concatenation process
- **Duplicate keys**: Values from maps appearing later in the argument list take precedence
- **Type compatibility**: All input maps must have compatible key and value types, otherwise compilation fails
- **Single argument**: If only one map is provided, returns that map unchanged

## Code Generation
This expression supports Tungsten code generation for improved performance when processing large datasets with map concatenation operations.

## Examples
```sql
-- Basic map concatenation
SELECT map_concat(map(1, 'a', 2, 'b'), map(3, 'c'));
-- Result: {1:"a", 2:"b", 3:"c"}

-- Handling duplicate keys (later values win)
SELECT map_concat(map(1, 'old'), map(1, 'new', 2, 'b'));
-- Result: {1:"new", 2:"b"}

-- Concatenating multiple maps
SELECT map_concat(map(1, 'a'), map(2, 'b'), map(3, 'c'));
-- Result: {1:"a", 2:"b", 3:"c"}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_concat(
  map(lit(1), lit("a"), lit(2), lit("b")),
  map(lit(3), lit("c"))
))

// Using column references
df.select(map_concat(col("map1"), col("map2")))
```

## See Also

- `map()` - Creates a map from key-value pairs
- `map_keys()` - Extracts keys from a map
- `map_values()` - Extracts values from a map
- `map_entries()` - Converts a map to an array of key-value structs