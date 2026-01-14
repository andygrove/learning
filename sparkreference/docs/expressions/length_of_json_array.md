# LengthOfJsonArray

## Overview

The `LengthOfJsonArray` expression returns the number of elements in a JSON array string. It is implemented as a runtime-replaceable expression that delegates to the JsonExpressionUtils utility class for actual JSON parsing and length calculation.

## Syntax

```sql
json_array_length(json_string)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.expr
df.select(expr("json_array_length(json_column)"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| json_string | String (with collation support) | A JSON string representing an array whose length is to be calculated |

## Return Type

Returns `IntegerType` representing the number of elements in the JSON array.

## Supported Data Types

- String types with collation support (specifically supports trim collation)

- Input must be a valid JSON array string format

## Algorithm

- Accepts a string expression containing JSON array data

- Delegates actual processing to `JsonExpressionUtils.lengthOfJsonArray()` method via `StaticInvoke`

- Parses the JSON string to identify array structure and count elements

- Returns integer count of array elements

- Handles malformed JSON according to JsonExpressionUtils implementation

## Partitioning Behavior

- Preserves partitioning as it operates on individual rows without requiring data movement

- Does not require shuffle operations

- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- Returns `NULL` when input is `NULL` (expression is nullable)

- Behavior with malformed JSON depends on JsonExpressionUtils implementation

- Empty JSON array `[]` should return `0`

- Non-array JSON values (objects, primitives) handling depends on underlying utility

- Invalid JSON strings may return `NULL` or throw exceptions based on implementation

## Code Generation

This expression uses `RuntimeReplaceable` pattern and delegates to `StaticInvoke`, which supports whole-stage code generation. The actual code generation is handled by the `StaticInvoke` mechanism calling the static method in `JsonExpressionUtils`.

## Examples

```sql
-- Basic usage
SELECT json_array_length('[1, 2, 3, 4]') AS length;
-- Returns: 4

-- Empty array
SELECT json_array_length('[]') AS length;  
-- Returns: 0

-- NULL input
SELECT json_array_length(NULL) AS length;
-- Returns: NULL

-- With table data
SELECT id, json_array_length(json_data) AS array_size 
FROM table_with_json 
WHERE json_data IS NOT NULL;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val df = spark.createDataFrame(Seq(
  ("1", "[1, 2, 3]"),
  ("2", "[]"),
  ("3", null)
)).toDF("id", "json_array")

df.select(
  col("id"),
  expr("json_array_length(json_array)").as("length")
).show()
```

## See Also

- Other JSON functions in the `json_funcs` group
- `JsonExpressionUtils` utility class
- `StaticInvoke` expression for runtime delegation
- JSON parsing and extraction functions