# SchemaOfJson

## Overview
The `SchemaOfJson` expression analyzes a JSON string and returns the inferred schema as a data type string. It parses the JSON structure and determines the appropriate Spark SQL data types for all fields, including support for complex nested structures like arrays and structs.

## Syntax
```sql
SELECT schema_of_json(json_string [, options_map])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(schema_of_json(col("json_column")))
df.select(schema_of_json(col("json_column"), map("allowNumericLeadingZeros" -> "true")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| json_string | STRING | The JSON string to analyze for schema inference |
| options_map | MAP<STRING, STRING> | Optional parsing options like `allowNumericLeadingZeros`, `allowBackslashEscapingAnyCharacter`, etc. |

## Return Type
Returns a `STRING` representing the inferred Spark SQL data type schema (e.g., "STRUCT<name: STRING, age: BIGINT>").

## Supported Data Types

- Input: STRING (JSON formatted)
- Inferred types: All Spark SQL data types including BOOLEAN, BIGINT, DOUBLE, STRING, ARRAY, STRUCT, MAP

## Algorithm

- Parses the input JSON string using Jackson JSON parser
- Traverses the JSON structure recursively to identify all fields and their types
- Applies type inference rules (numbers default to BIGINT/DOUBLE, strings remain STRING)
- Handles nested structures by creating STRUCT types for objects and ARRAY types for arrays
- Applies any specified parsing options during the inference process

## Partitioning Behavior
This expression preserves partitioning since it operates on individual rows without requiring data movement:

- Preserves existing partitioning
- Does not require shuffle operations
- Can be executed independently on each partition

## Edge Cases

- Null input returns null result
- Invalid JSON strings may throw parsing exceptions
- Empty JSON objects return "STRUCT<>" 
- Empty JSON arrays return "ARRAY<STRING>" (default array element type)
- Mixed type arrays are inferred as the most general common type
- Numeric values with leading zeros require `allowNumericLeadingZeros` option to parse correctly
- Very deeply nested JSON may hit recursion limits

## Code Generation
This expression supports Whole-Stage Code Generation (Tungsten) for the wrapper logic, but the actual JSON parsing falls back to interpreted mode using Jackson parser libraries for complex schema inference operations.

## Examples
```sql
-- Basic schema inference
SELECT schema_of_json('{"name":"John", "age":30}');
-- Result: STRUCT<age: BIGINT, name: STRING>

-- Array schema inference  
SELECT schema_of_json('[{"col":01}]', map('allowNumericLeadingZeros', 'true'));
-- Result: ARRAY<STRUCT<col: BIGINT>>

-- Complex nested structure
SELECT schema_of_json('{"users":[{"name":"John","scores":[95,87]}]}');
-- Result: STRUCT<users: ARRAY<STRUCT<name: STRING, scores: ARRAY<BIGINT>>>>
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = Seq("""{"name":"Alice","age":25}""").toDF("json_col")
df.select(schema_of_json(col("json_col"))).show(false)

// With options
val options = Map("allowNumericLeadingZeros" -> "true")
df.select(schema_of_json(col("json_col"), lit(options))).show(false)
```

## See Also

- `from_json` - Parse JSON strings into structured data using a schema
- `to_json` - Convert structured data to JSON strings  
- `json_tuple` - Extract multiple fields from JSON strings
- `get_json_object` - Extract single values from JSON using JSONPath