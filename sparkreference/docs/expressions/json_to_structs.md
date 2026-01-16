# JsonToStructs

## Overview
The JsonToStructs expression parses JSON strings into Spark SQL structured data types (StructType, ArrayType, or MapType). This expression is exposed through the `from_json` SQL function and enables deserialization of JSON data for structured processing within Spark.

## Syntax
```sql
-- SQL syntax
from_json(jsonStr, schema [, options])
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.from_json
import org.apache.spark.sql.types._

val schema = new StructType()
  .add("name", StringType)
  .add("age", IntegerType)

df.select(from_json($"json_column", schema))
```

```python
# PySpark API
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType()),
    StructField("age", IntegerType())
])

df.select(from_json("json_column", schema))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| jsonStr | StringType | Column containing JSON strings to parse |
| schema | DataType, StructType, ArrayType, MapType, or DDL String | Target schema defining the structure of the parsed output |
| options | Map[String, String] (optional) | JSON parsing options (same as JSON datasource options) |

## Return Type
Returns a column matching the provided schema type:
- StructType schema returns a struct column
- ArrayType schema returns an array column
- MapType schema returns a map column

## Supported Data Types

**Input:**
- StringType containing valid JSON

**Schema Types:**
- StructType - for JSON objects
- ArrayType - for JSON arrays
- MapType(StringType, StringType) - for arbitrary key-value JSON objects
- Nested combinations of the above

**Field Types within Schema:**
- All primitive types (StringType, IntegerType, LongType, DoubleType, BooleanType, etc.)
- DateType and TimestampType (with configurable formatting)
- DecimalType
- BinaryType (Base64 encoded)
- Nested StructType, ArrayType, MapType

## Options

| Option | Default | Description |
|--------|---------|-------------|
| mode | PERMISSIVE | Parse mode: PERMISSIVE, FAILFAST |
| columnNameOfCorruptRecord | (none) | Field name to store malformed records (PERMISSIVE mode only) |
| dateFormat | yyyy-MM-dd | Format for parsing date fields |
| timestampFormat | yyyy-MM-dd'T'HH:mm:ss[.SSS][XXX] | Format for parsing timestamp fields |
| primitivesAsString | false | Infer all primitive values as StringType |
| prefersDecimal | false | Infer floating-point values as DecimalType |
| allowComments | false | Allow Java/C++ style comments in JSON |
| allowUnquotedFieldNames | false | Allow unquoted JSON field names |
| allowSingleQuotes | true | Allow single quotes instead of double quotes |
| allowNumericLeadingZeros | false | Allow leading zeros in numbers |
| allowBackslashEscapingAnyCharacter | false | Allow backslash escaping any character |
| allowUnquotedControlChars | false | Allow unquoted control characters |
| multiLine | false | Parse multi-line JSON records |
| encoding | UTF-8 | Character encoding |
| locale | en-US | Locale for parsing |

## Algorithm

1. Parses the input JSON string using Jackson parser
2. Validates JSON structure against the provided schema
3. Converts JSON values to corresponding Spark SQL types
4. Applies configured options for date/timestamp formatting and error handling
5. Returns structured data matching the schema

## Partitioning Behavior

- Preserves existing partitioning as it operates row-wise
- Does not require shuffle operations
- Can be executed locally on each partition independently
- Timezone-aware: uses session timezone for timestamp parsing

## Edge Cases

### Null Handling
- Null input returns null output
- Missing fields in JSON are set to null in the output struct
- Empty string input returns null (not an empty struct)

### Parse Mode Behavior (Spark 3.0+)

**PERMISSIVE Mode (default):**
- Malformed JSON records return a row with parseable fields populated and unparseable fields as null
- If `columnNameOfCorruptRecord` is specified in schema, malformed JSON string is stored there
- Without `columnNameOfCorruptRecord`, malformed records are silently converted with null fields

**FAILFAST Mode:**
- Throws exception immediately on malformed JSON
- Does not support `columnNameOfCorruptRecord` option
- Useful for strict validation requirements

### Spark 3.0 Breaking Changes
- In Spark 2.4 and below: malformed JSON returned row with ALL fields as null
- In Spark 3.0+: malformed JSON returns row with successfully parsed fields populated, only unparseable fields as null
- JSON arrays cannot be parsed as StructType (use ArrayType instead)

### Schema Mismatch
- Extra fields in JSON not in schema are ignored
- Field names are case-sensitive and must match exactly
- Type mismatches (e.g., string value for integer field) result in null for that field

### Special Values
- JSON `null` maps to Spark SQL null
- Empty JSON object `{}` maps to struct with all null fields
- Empty JSON array `[]` maps to empty array

## Examples

```sql
-- Basic struct parsing
SELECT from_json('{"name":"Alice","age":30}', 'name STRING, age INT') AS parsed;
-- Result: {Alice, 30}

-- Parsing to MapType
SELECT from_json('{"key1":"value1","key2":"value2"}', 'MAP<STRING,STRING>') AS parsed;
-- Result: {key1 -> value1, key2 -> value2}

-- Array of structs
SELECT from_json('[{"a":1},{"a":2}]', 'ARRAY<STRUCT<a:INT>>') AS parsed;
-- Result: [{1}, {2}]

-- With options
SELECT from_json(
  '{"date":"2024-01-15"}',
  'date DATE',
  map('dateFormat', 'yyyy-MM-dd')
) AS parsed;
-- Result: {2024-01-15}

-- FAILFAST mode
SELECT from_json('{"a":1}', 'a INT', map('mode', 'FAILFAST')) AS parsed;

-- Handling corrupt records (PERMISSIVE mode)
SELECT from_json(
  '{"a": invalid}',
  'a INT, _corrupt_record STRING',
  map('columnNameOfCorruptRecord', '_corrupt_record')
) AS parsed;
-- Result: {null, {"a": invalid}}
```

```scala
// DataFrame API examples
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

// Define schema
val schema = new StructType()
  .add("name", StringType)
  .add("age", IntegerType)
  .add("address", new StructType()
    .add("city", StringType)
    .add("zip", StringType))

// Parse JSON column
df.select(from_json($"json_col", schema).as("parsed"))

// Expand to multiple columns
df.select(from_json($"json_col", schema).as("parsed"))
  .select($"parsed.*")

// With options
val options = Map(
  "mode" -> "PERMISSIVE",
  "timestampFormat" -> "yyyy-MM-dd HH:mm:ss"
)
df.select(from_json($"json_col", schema, options))

// Parse to MapType for dynamic keys
df.select(from_json($"json_col", MapType(StringType, StringType)))
```

```python
# PySpark examples
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

# Define schema
schema = StructType([
    StructField("name", StringType()),
    StructField("age", IntegerType()),
    StructField("scores", ArrayType(IntegerType()))
])

# Parse and expand
df.select(from_json(col("json_col"), schema).alias("parsed")) \
  .select("parsed.*")

# With DDL string schema
df.select(from_json("json_col", "name STRING, age INT"))
```

## See Also

- [StructsToJson](structs_to_json.md) - Convert structs back to JSON strings (to_json)
- [GetJsonObject](get_json_object.md) - Extract single values from JSON using path expressions
- [JsonTuple](json_tuple.md) - Extract multiple values from JSON into columns
- [SchemaOfJson](schema_of_json.md) - Infer schema from JSON string sample
