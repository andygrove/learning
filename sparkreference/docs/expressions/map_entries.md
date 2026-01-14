# MapEntries

## Overview
The `MapEntries` expression transforms a map into an array of struct objects, where each struct contains "key" and "value" fields representing the key-value pairs from the original map. This function is useful for converting map data into a more structured array format that can be easily processed or flattened.

## Syntax
```sql
map_entries(map_expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression (MapType) | The map expression to convert into an array of key-value struct entries |

## Return Type
Returns an `ArrayType` containing `StructType` elements with two fields:
- `key`: The key from the map (preserves original key type)
- `value`: The value from the map (preserves original value type)

## Supported Data Types
Supports any `MapType` input where:

- Keys can be any data type that is valid for map keys
- Values can be any data type that is valid for map values
- The resulting array will contain structs with the same key and value types as the input map

## Algorithm
The expression evaluation process follows these steps:

- Takes a map input and validates it is of MapType
- Iterates through each key-value pair in the input map
- Creates a struct object for each pair with "key" and "value" fields
- Collects all struct objects into an array
- Returns the array containing all key-value pair structs

## Partitioning Behavior
This expression has the following partitioning characteristics:

- Preserves existing partitioning as it operates on individual rows
- Does not require data shuffle since it's a row-level transformation
- Can be executed in parallel across partitions without coordination

## Edge Cases

- **Null input**: If the input map is null, returns null
- **Empty map**: If the input map is empty, returns an empty array
- **Null keys/values**: Preserves null keys and null values within the resulting struct entries
- **Large maps**: Performance may degrade with very large maps due to array creation overhead

## Code Generation
This expression supports Spark's Catalyst code generation (Tungsten) for optimized execution. The generated code efficiently iterates through map entries and constructs the result array without falling back to interpreted mode.

## Examples
```sql
-- Convert a simple map to key-value struct array
SELECT map_entries(map(1, 'a', 2, 'b'));
-- Result: [{"key":1,"value":"a"},{"key":2,"value":"b"}]

-- Use with complex data types
SELECT map_entries(map('name', 'John', 'city', 'NYC'));
-- Result: [{"key":"name","value":"John"},{"key":"city","value":"NYC"}]

-- Handle empty map
SELECT map_entries(map());
-- Result: []
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(map_entries(col("my_map_column")))

// Create map and convert to entries
df.select(map_entries(map(lit("key1"), lit("value1"), lit("key2"), lit("value2"))))
```

## See Also
- `map()` - Creates map from key-value pairs
- `map_keys()` - Extracts only keys from a map
- `map_values()` - Extracts only values from a map
- `explode()` - Can be used with map_entries result to create separate rows