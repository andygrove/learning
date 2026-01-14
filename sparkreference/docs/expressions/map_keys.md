# MapKeys

## Overview
The MapKeys expression extracts all keys from a map data structure and returns them as an array. It is a unary expression that takes a single map input and produces an array containing all the keys from that map in their original order.

## Syntax
```sql
map_keys(map_expr)
```

```scala
// DataFrame API
col("map_column").map_keys()
// or using functions
import org.apache.spark.sql.functions._
map_keys(col("map_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | MapType | The map expression from which to extract keys |

## Return Type
Returns an `ArrayType` where the element type matches the key type of the input map. For example, if the input is `MapType(IntegerType, StringType)`, the return type will be `ArrayType(IntegerType)`.

## Supported Data Types
Accepts any `MapType` as input, regardless of the specific key and value types. The key type can be any valid map key type including:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- StringType
- BinaryType
- DateType
- TimestampType
- Other primitive types that can serve as map keys

## Algorithm
The expression evaluation follows these steps:

- Input validation ensures the child expression produces a MapType
- The input map is cast to MapData for internal processing
- The keyArray() method is called on the MapData to extract all keys
- Keys are returned in their original insertion/iteration order
- Code generation produces optimized bytecode for the key extraction operation

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual map values
- Maintains existing partitioning scheme since it's a row-level transformation
- Can be executed independently on each partition

## Edge Cases

- **Null handling**: Returns null when the input map is null (nullIntolerant = true)
- **Empty map behavior**: Returns an empty array when the input map is empty
- **Key ordering**: Preserves the iteration order of keys as defined by the underlying MapData implementation
- **Duplicate handling**: Not applicable since map keys are unique by definition

## Code Generation
This expression supports Spark's Tungsten code generation framework. It uses `nullSafeCodeGen` to generate optimized Java bytecode that directly calls the `keyArray()` method on the MapData object, avoiding the overhead of interpreted evaluation.

## Examples
```sql
-- Extract keys from a literal map
SELECT map_keys(map(1, 'a', 2, 'b', 3, 'c'));
-- Result: [1, 2, 3]

-- Extract keys from a table column
SELECT map_keys(user_preferences) FROM users;

-- Use in WHERE clause
SELECT * FROM events WHERE array_contains(map_keys(event_data), 'timestamp');
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract keys from map column
df.select(map_keys(col("properties")))

// Combine with other operations
df.select(
  col("id"),
  map_keys(col("metadata")).as("available_fields")
)

// Filter based on keys
df.filter(array_contains(map_keys(col("config")), lit("timeout")))
```

## See Also

- `map_values` - Extracts values from a map
- `map_entries` - Converts a map to an array of key-value structs
- `map_from_arrays` - Creates a map from key and value arrays
- `element_at` - Retrieves a specific value from a map by key