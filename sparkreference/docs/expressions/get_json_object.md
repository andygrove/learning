# GetJsonObject

## Overview
The `GetJsonObject` expression extracts JSON values from a JSON string using JSONPath expressions. It takes a JSON string and a JSONPath query, returning the matching value(s) as a string representation.

## Syntax
```sql
get_json_object(json_string, path)
```

```scala
// DataFrame API usage
col("json_column").getItem(path)
// or using expr()
expr("get_json_object(json_column, '$.field')")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| json | Expression | The JSON string to query against |
| path | Expression | The JSONPath expression to extract values |

## Return Type
Returns `StringType` - the extracted JSON value as a string representation.

## Supported Data Types

- **json parameter**: String type containing valid JSON
- **path parameter**: String type containing valid JSONPath expressions

## Algorithm

- Parse the input JSON string into an internal JSON representation
- Compile the JSONPath expression for efficient querying
- Apply the JSONPath query against the parsed JSON structure
- Extract matching values and convert them to string representation
- Return the result as a string, preserving JSON formatting for complex types

## Partitioning Behavior
How this expression affects partitioning:

- Preserves existing partitioning schemes as it's a row-level transformation
- Does not require shuffle operations
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null if either json or path parameters are null
- **Invalid JSON**: Returns null for malformed JSON input strings
- **Invalid JSONPath**: Returns null for syntactically incorrect JSONPath expressions
- **No matches**: Returns null when the JSONPath doesn't match any elements
- **Multiple matches**: For array results, returns JSON array string representation

## Code Generation
This expression supports Catalyst code generation (Tungsten) for optimal performance in tight loops and aggregations.

## Examples
```sql
-- Extract simple field
SELECT get_json_object('{"name":"John","age":30}', '$.name');
-- Result: "John"

-- Extract from array
SELECT get_json_object('[{"a":"b"},{"a":"c"}]', '$[*].a');
-- Result: ["b","c"]

-- Extract nested field
SELECT get_json_object('{"user":{"profile":{"name":"Alice"}}}', '$.user.profile.name');
-- Result: "Alice"

-- Array element access
SELECT get_json_object('{"items":["apple","banana","cherry"]}', '$.items[1]');
-- Result: "banana"
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(get_json_object(col("json_data"), "$.field"))

// Using expr for complex JSONPath
df.select(expr("get_json_object(json_column, '$[*].nested.field')"))

// Multiple extractions
df.select(
  get_json_object(col("json_data"), "$.name").alias("name"),
  get_json_object(col("json_data"), "$.age").alias("age")
)
```

## See Also

- `json_tuple` - Extract multiple JSON fields in a single operation
- `from_json` - Parse JSON string into structured data types
- `to_json` - Convert structured data to JSON strings
- `json_array_length` - Get length of JSON arrays