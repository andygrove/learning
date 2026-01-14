# StructsToJson

## Overview
The StructsToJson expression converts Spark SQL struct data types into their JSON string representation. This expression enables serialization of complex nested data structures into JSON format for storage, transmission, or interoperability with external systems.

## Syntax
```sql
to_json(struct_column [, options_map])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.to_json
df.select(to_json($"struct_column"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | StructType or ArrayType | The struct or array column to convert to JSON |
| options | Map[String, String] (optional) | JSON serialization options like dateFormat, timestampFormat, etc. |

## Return Type
StringType - Returns a JSON string representation of the input struct or array.

## Supported Data Types

- StructType (primary use case)
- ArrayType containing structs
- Nested combinations of structs and arrays
- All primitive types within structs (StringType, IntegerType, DoubleType, BooleanType, etc.)
- TimestampType and DateType (with configurable formatting)

## Algorithm

- Traverses the input struct or array recursively to build JSON representation
- Applies configured formatting options for dates and timestamps during serialization
- Handles nested structures by recursively converting child elements
- Uses Jackson library internally for efficient JSON generation
- Preserves field names and maintains structural hierarchy in output

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning as it operates row-wise without requiring data movement
- Does not require shuffle operations
- Can be executed locally on each partition independently

## Edge Cases

- Null handling: Returns null when input struct is null
- Empty structs: Converts to empty JSON object "{}"
- Empty arrays: Converts to empty JSON array "[]"
- Special float values: NaN and Infinity are serialized as JSON strings
- Nested nulls: Null fields within structs are included in JSON with null values
- Malformed options: Invalid date/timestamp format options may cause runtime errors

## Code Generation
This expression supports Whole-Stage Code Generation (Tungsten) for optimized performance. Falls back to interpreted mode only when code generation limits are exceeded or for extremely complex nested structures.

## Examples
```sql
-- Basic struct to JSON conversion
SELECT to_json(struct(name, age, city)) as json_data
FROM users;

-- Array of structs to JSON
SELECT to_json(array(struct(1 as a), struct(2 as a))) as json_array;

-- With formatting options
SELECT to_json(struct(event_time, data), map('timestampFormat', 'yyyy-MM-dd HH:mm:ss')) 
FROM events;
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._

// Basic conversion
df.select(to_json(struct($"name", $"age", $"city")).as("json_data"))

// With options
val options = Map("timestampFormat" -> "yyyy-MM-dd HH:mm:ss")
df.select(to_json(struct($"event_time", $"data"), options))

// Converting array column
df.select(to_json($"array_of_structs"))
```

## See Also

- JsonToStructs - for parsing JSON strings back to structs
- GetJsonObject - for extracting specific fields from JSON strings  
- JsonTuple - for parsing JSON into multiple columns
- StructType and ArrayType data types