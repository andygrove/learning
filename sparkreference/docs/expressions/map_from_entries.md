# MapFromEntries

## Overview
The `MapFromEntries` expression converts an array of struct entries into a map. Each struct in the input array must contain exactly two fields, where the first field becomes the key and the second field becomes the value in the resulting map.

## Syntax
```sql
map_from_entries(array_of_structs)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | An array of struct expressions where each struct has exactly two fields |

## Return Type
Returns a `MapType` where the key type corresponds to the first field type of the input struct and the value type corresponds to the second field type.

## Supported Data Types

- Input: Array of struct types with exactly two fields
- The struct fields can be of any supported Spark SQL data type
- Key types must be orderable/hashable types (cannot be complex types like arrays, maps, or structs)
- Value types can be any Spark SQL data type

## Algorithm

- Takes an array of struct entries as input
- Iterates through each struct element in the array
- Extracts the first field of each struct as the map key
- Extracts the second field of each struct as the map value
- Constructs a new map from the key-value pairs
- Returns the resulting map structure

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be evaluated locally on each partition

## Edge Cases

- Null handling: If the input array is null, returns null
- Empty array: Returns an empty map
- Null struct elements: Null entries in the array are skipped
- Duplicate keys: Later entries with the same key will overwrite earlier entries
- Struct validation: Runtime error if structs don't have exactly two fields

## Code Generation
This expression supports Tungsten code generation for improved performance when processing large datasets with map transformations.

## Examples
```sql
-- Convert array of structs to map
SELECT map_from_entries(array(struct(1, 'a'), struct(2, 'b')));
-- Result: {1:"a", 2:"b"}

-- Using with named struct fields
SELECT map_from_entries(array(struct(1 as id, 'Alice' as name), struct(2 as id, 'Bob' as name)));
-- Result: {1:"Alice", 2:"Bob"}

-- Empty array case
SELECT map_from_entries(array());
-- Result: {}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_from_entries(
  array(
    struct(lit(1), lit("a")),
    struct(lit(2), lit("b"))
  )
))

// Using existing array column
df.select(map_from_entries(col("struct_array")))
```

## See Also

- `map_entries()` - Reverse operation that converts map to array of structs
- `map()` - Direct map construction from alternating key-value arguments
- `struct()` - Creates struct expressions used as input to this function