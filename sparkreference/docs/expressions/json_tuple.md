# JsonTuple

## Overview

JsonTuple is a generator expression that extracts multiple fields from a JSON string and returns them as separate columns in a tuple format. It takes a JSON string as the first argument followed by one or more field path expressions, returning a row with the extracted values in the order specified.

## Syntax

```sql
json_tuple(json_string, field1, field2, ...)
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| json_string | String | The JSON string to parse and extract fields from |
| field1, field2, ... | String | One or more field names/paths to extract from the JSON |

## Return Type

Returns a StructType with columns named `c0`, `c1`, `c2`, etc., where each column corresponds to the extracted field values. All output columns have nullable string type matching the input JSON expression's data type.

## Supported Data Types

Input arguments must be string types with collation support (specifically StringTypeWithCollation with trimming support). All children expressions must accept string data types.

## Algorithm

- Parses the input JSON string using an internal JsonTupleEvaluator
- Evaluates field name expressions, with foldable (constant) field names pre-computed for optimization  
- Extracts the requested fields from the parsed JSON structure
- Returns an iterable of InternalRow objects containing the extracted values
- Missing or invalid fields result in null values in the corresponding output columns

## Partitioning Behavior

As a Generator expression, JsonTuple:

- Does not preserve partitioning since it can produce multiple output rows
- May require shuffle operations when used in contexts that need specific partitioning
- Each input row can generate one or more output rows

## Edge Cases

- Always returns at least one row (nullable = false), even for invalid JSON
- Null JSON input results in null values for all extracted fields
- Invalid or missing field paths return null for those specific columns
- Foldable (constant) field expressions are pre-evaluated for performance optimization
- Requires minimum 2 arguments (JSON string + at least one field name), throws QueryCompilationErrors.wrongNumArgsError otherwise

## Code Generation

This expression supports Tungsten code generation. It generates optimized code that:

- Pre-allocates UTF8String arrays for field names
- Reuses the JsonTupleEvaluator instance via context reference
- Handles null field name evaluation inline
- Avoids interpreted evaluation overhead for better performance

## Examples

```sql
-- Extract name and age from JSON
SELECT json_tuple('{"name":"John", "age":30, "city":"NYC"}', 'name', 'age') AS (name, age);
-- Returns: John, 30

-- Extract nested fields
SELECT json_tuple('{"user":{"id":123,"email":"test@example.com"}}', 'user.id', 'user.email') AS (id, email);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(json_tuple(col("json_col"), lit("field1"), lit("field2")).as(Seq("c0", "c1")))
```

## See Also

- `get_json_object` - Extract single JSON field
- `from_json` - Parse JSON with explicit schema
- `json_extract` - Alternative JSON field extraction