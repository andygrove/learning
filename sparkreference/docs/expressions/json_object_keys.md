# JsonObjectKeys

## Overview
The `JsonObjectKeys` expression extracts the keys from a JSON object and returns them as an array of strings. This expression is implemented as a runtime-replaceable unary expression that delegates to the `JsonExpressionUtils.jsonObjectKeys` method for actual evaluation.

## Syntax
```sql
json_object_keys(json_string)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("json_object_keys(json_column)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| json_string | StringType | A valid JSON object string from which to extract keys |

## Return Type
`ArrayType(StringType)` - Returns an array of strings containing the keys from the JSON object.

## Supported Data Types

- String types with collation support (including trim collation)
- Input must be a valid JSON object string

## Algorithm

- Accepts a string input representing a JSON object
- Delegates evaluation to `JsonExpressionUtils.jsonObjectKeys` via `StaticInvoke`
- Parses the JSON string to extract object keys
- Returns the keys as an array of strings
- Handles null inputs by returning null (nullable = true)

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations
- Can be evaluated independently on each partition
- Does not affect data distribution across partitions

## Edge Cases

- **Null handling**: Returns null when input is null (expression is nullable)
- **Empty JSON object**: Returns empty array for `{}`
- **Invalid JSON**: Behavior depends on underlying `JsonExpressionUtils` implementation
- **Non-object JSON**: Arrays, primitives, and other JSON types may return null or throw exceptions
- **Nested objects**: Only extracts top-level keys, does not traverse nested structures

## Code Generation
This expression uses runtime replacement via `StaticInvoke` rather than direct code generation:

- Implements `RuntimeReplaceable` trait
- Evaluation is delegated to `JsonExpressionUtils.jsonObjectKeys` method
- Does not generate custom Tungsten code, relies on static method invocation

## Examples
```sql
-- Extract keys from a simple JSON object
SELECT json_object_keys('{"name": "John", "age": 30, "city": "NYC"}');
-- Result: ["name", "age", "city"]

-- Handle empty JSON object
SELECT json_object_keys('{}');
-- Result: []

-- Handle null input
SELECT json_object_keys(NULL);
-- Result: NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.createDataFrame(Seq(
  ("""{"f1": "value1", "f2": "value2"}"""),
  ("""{"a": 1, "b": 2, "c": 3}"""),
  (null)
)).toDF("json_col")

df.select(expr("json_object_keys(json_col)")).show()
```

## See Also

- `get_json_object` - Extract specific values from JSON
- `json_extract` - Extract JSON values using path expressions
- `from_json` - Parse JSON strings into structured data
- Other JSON manipulation functions in the `json_funcs` group