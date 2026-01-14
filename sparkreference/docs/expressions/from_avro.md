# FromAvro

## Overview
The `FromAvro` expression converts binary Avro-encoded data to Spark SQL data types using a provided JSON schema. This is a runtime-replaceable ternary expression that internally delegates to `AvroDataToCatalyst` for the actual conversion logic.

## Syntax
```sql
FROM_AVRO(avro_data, json_schema [, options])
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("FROM_AVRO(avro_column, schema_string, options_map)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The binary Avro data to be converted |
| jsonFormatSchema | Expression | A constant string containing the JSON representation of the Avro schema |
| options | Expression | Optional constant map of string key-value pairs for conversion options |

## Return Type
The return type depends on the provided Avro schema and can be any Catalyst data type that corresponds to the Avro schema structure (primitives, arrays, maps, structs).

## Supported Data Types

**Input (child):** Binary data containing Avro-encoded values

**Schema (jsonFormatSchema):** 
- StringType (constant/foldable expressions only)
- NullType

**Options (options):**
- MapType(StringType, StringType) (constant/foldable expressions only)
- NullType

## Algorithm

- Validates that the schema argument is a constant string containing valid JSON schema representation
- Validates that the options argument is a constant map of strings (if provided)
- At runtime, evaluates the schema and options expressions to extract their values
- Uses reflection to instantiate `AvroDataToCatalyst` from the spark-avro module
- Delegates the actual Avro-to-Catalyst conversion to the instantiated expression

## Partitioning Behavior
This expression preserves partitioning as it operates row-by-row without requiring data movement between partitions:

- Does not require shuffle operations
- Maintains existing partitioning scheme
- Can be applied within partition boundaries

## Edge Cases

- **Null schema:** When jsonFormatSchema evaluates to null, an empty string is used as the schema
- **Null options:** When options evaluates to null, an empty map is used for options
- **Missing spark-avro dependency:** Throws `QueryCompilationErrors.avroNotLoadedSqlFunctionsUnusable` if the AvroDataToCatalyst class is not found
- **Non-constant arguments:** Schema and options must be constant/foldable expressions, otherwise type checking fails
- **Invalid schema format:** Runtime errors may occur if the JSON schema string is malformed

## Code Generation
This expression uses runtime replacement rather than direct code generation. The actual code generation behavior depends on the underlying `AvroDataToCatalyst` expression that is instantiated at runtime.

## Examples
```sql
-- Convert Avro binary data using a simple schema
SELECT FROM_AVRO(avro_data, '{"type": "string"}') as converted_value
FROM avro_table;

-- Convert with options map
SELECT FROM_AVRO(
  avro_data, 
  '{"type": "record", "name": "User", "fields": [{"name": "id", "type": "long"}]}',
  map('mode', 'PERMISSIVE')
) as user_record
FROM avro_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

val schema = """{"type": "string"}"""
val options = Map("mode" -> "PERMISSIVE")

df.select(
  expr(s"FROM_AVRO(avro_column, '$schema', map('mode', 'PERMISSIVE'))").alias("converted")
)
```

## See Also

- `ToAvro` - Converts Catalyst data types to Avro binary format
- `AvroDataToCatalyst` - The underlying expression that performs the actual conversion
- Spark Avro documentation for schema format and options