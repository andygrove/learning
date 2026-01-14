# SchemaOfAvro

## Overview
`SchemaOfAvro` is a Spark Catalyst expression that generates a schema string representation from an Avro JSON schema definition. This is a runtime replaceable expression that dynamically loads the actual Avro implementation and evaluates the schema conversion based on the provided JSON schema and optional configuration parameters.

## Syntax
```sql
SCHEMA_OF_AVRO(jsonFormatSchema [, options])
```

```scala
// DataFrame API usage through SQL function
df.select(expr("schema_of_avro(json_schema_column, options_map)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| jsonFormatSchema | StringType | A constant string containing the JSON representation of the Avro schema |
| options | MapType[String, String] (optional) | A constant map of string key-value pairs containing conversion options |

## Return Type
Returns a `StringType` representing the derived schema structure from the Avro JSON schema.

## Supported Data Types

**First Parameter (jsonFormatSchema):**

- StringType (foldable/constant expressions only)
- NullType (foldable/constant expressions only)

**Second Parameter (options):**

- MapType(StringType, StringType, _) (foldable/constant expressions only)
- MapType(NullType, NullType, _) (foldable/constant expressions only)
- NullType (foldable/constant expressions only)

## Algorithm

- Validates that both input parameters are foldable (constant) expressions with correct data types
- Evaluates the JSON schema string parameter, converting UTF8String to String or handling null as empty string
- Evaluates the options parameter, converting ArrayBasedMapData to a Map[String, String] or using empty map as default
- Dynamically loads the `org.apache.spark.sql.avro.SchemaOfAvro` class using reflection
- Creates a new instance of the loaded class with the evaluated schema and options parameters
- Returns the constructed expression as the replacement for runtime evaluation

## Partitioning Behavior
This expression does not affect partitioning behavior as it operates on constant values:

- Preserves existing partitioning since it's a deterministic function of constant inputs
- Does not require shuffle operations
- Can be evaluated during query planning phase due to constant folding

## Edge Cases

**Null Handling:**

- If jsonFormatSchema evaluates to null, it's converted to an empty string
- If options parameter is null or empty, an empty Map is used as default

**Error Conditions:**

- Throws QueryCompilationErrors.avroNotLoadedSqlFunctionsUnusable if Avro classes are not available on classpath
- Type check failures occur if parameters are not foldable (constant) expressions
- Type check failures occur if parameter data types don't match expected types

**Empty Input:**

- Empty JSON schema string is passed through to the underlying Avro implementation
- Empty options map is handled gracefully with default behavior

## Code Generation
This expression uses runtime replacement pattern rather than direct code generation. The actual code generation is delegated to the dynamically loaded Avro expression implementation, which replaces this expression during query planning.

## Examples
```sql
-- Basic usage with JSON schema string
SELECT SCHEMA_OF_AVRO('{"type": "record", "name": "test", "fields": [{"name": "field1", "type": "string"}]}')

-- With options map
SELECT SCHEMA_OF_AVRO(
  '{"type": "record", "name": "test", "fields": [{"name": "field1", "type": "string"}]}',
  map('option1', 'value1', 'option2', 'value2')
)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  expr("schema_of_avro('{\"type\": \"string\"}')")
)

// With options
df.select(
  expr("schema_of_avro('{\"type\": \"string\"}', map('option1', 'value1'))")
)
```

## See Also

- `from_avro` - Convert Avro binary data to Spark SQL data types
- `to_avro` - Convert Spark SQL data types to Avro binary format
- Schema inference functions for other formats (JSON, CSV, etc.)