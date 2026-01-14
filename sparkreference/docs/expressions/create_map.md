# CreateMap

## Overview
The CreateMap expression creates a map (key-value pairs) from a sequence of alternating key and value expressions. Keys and values are paired sequentially from the input expressions, where odd-positioned expressions become keys and even-positioned expressions become values.

## Syntax
```sql
map(key1, value1, key2, value2, ...)
```

```scala
// DataFrame API
map(col("key1"), col("value1"), col("key2"), col("value2"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | Sequence of expressions where odd positions are keys and even positions are values |
| useStringTypeWhenEmpty | Boolean | When true, creates a map with string type for both keys and values when no children are provided |

## Return Type
Returns a MapType where the key type is inferred from the odd-positioned expressions and the value type is inferred from the even-positioned expressions. When empty and useStringTypeWhenEmpty is true, returns MapType(StringType, StringType).

## Supported Data Types
Supports all Spark SQL data types for both keys and values. Key expressions must be of a type that can be used as map keys (hashable and comparable types). Common supported types include:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- StringType
- DateType
- TimestampType
- BooleanType

## Algorithm
The CreateMap expression evaluation follows these steps:

- Validates that the number of children expressions is even (pairs of key-value)
- Evaluates odd-positioned expressions (0, 2, 4, ...) as map keys
- Evaluates even-positioned expressions (1, 3, 5, ...) as map values
- Creates a MapData structure pairing each key with its corresponding value
- Returns null if any key expression evaluates to null

## Partitioning Behavior
The CreateMap expression has the following partitioning characteristics:

- Preserves input partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null keys**: If any key expression evaluates to null, the entire map creation fails and returns null
- **Null values**: Null values are allowed and preserved in the resulting map
- **Empty input**: When no expressions are provided and useStringTypeWhenEmpty is true, creates an empty map of type Map[String, String]
- **Type coercion**: All key expressions must be promotable to a common type, same for value expressions
- **Duplicate keys**: Later key-value pairs with the same key will overwrite earlier ones

## Code Generation
This expression supports Catalyst code generation (Tungsten) for improved performance. The generated code directly creates the map structure without intermediate object creation, leading to faster execution compared to interpreted mode.

## Examples
```sql
-- Create a simple map
SELECT map(1.0, '2', 3.0, '4');
-- Result: {1.0:"2", 3.0:"4"}

-- Create a map with column values
SELECT map('name', first_name, 'age', age) FROM users;

-- Empty map
SELECT map();
-- Result: {}
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.map

df.select(map(lit("key1"), col("value1"), lit("key2"), col("value2")))

// Create map from multiple columns
df.select(map(
  lit("name"), col("first_name"),
  lit("age"), col("age"),
  lit("city"), col("city")
))
```

## See Also

- **map_keys**: Extract keys from a map
- **map_values**: Extract values from a map  
- **CreateArray**: Create arrays from expressions
- **CreateStruct**: Create struct/row objects from expressions