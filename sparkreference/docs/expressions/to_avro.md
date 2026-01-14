# ToAvro

## Overview
The ToAvro expression converts input data into Apache Avro binary format. It serves as a runtime-replaceable wrapper that delegates to the actual Avro serialization implementation at query planning time, supporting both automatic schema inference and explicit schema specification via JSON format.

## Syntax
```sql
TO_AVRO(column)
TO_AVRO(column, schema_json)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("to_avro(column)"))
df.select(expr("to_avro(column, schema_json)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression/column to convert to Avro format |
| jsonFormatSchema | Expression | Optional JSON string representing the Avro schema to use for conversion. Must be a constant string or null |

## Return Type
Binary data type containing the Avro-encoded representation of the input data.

## Supported Data Types
The expression accepts any input data type for the child expression, as the underlying CatalystDataToAvro implementation handles the conversion. The jsonFormatSchema parameter must be:

- StringType (constant/foldable expressions only)
- NullType (when schema parameter is omitted)

## Algorithm

- Validates that the jsonFormatSchema parameter is either null or a constant string expression
- At runtime replacement phase, evaluates the schema parameter to extract the JSON schema string
- Uses reflection to instantiate the CatalystDataToAvro class from the spark-avro module
- Delegates actual Avro serialization to the CatalystDataToAvro expression with the provided schema
- Throws compilation error if spark-avro module is not available on the classpath

## Partitioning Behavior
This expression preserves partitioning as it operates row-by-row without requiring data redistribution:

- Preserves existing partitioning schemes
- Does not require shuffle operations
- Can be applied within partition boundaries

## Edge Cases

- Null jsonFormatSchema: Uses automatic schema inference from input data structure
- Missing spark-avro dependency: Throws QueryCompilationErrors.avroNotLoadedSqlFunctionsUnusable at query compilation time
- Non-constant schema parameter: Fails type checking with descriptive error message about requiring constant string
- Invalid JSON schema format: Error handling delegated to underlying CatalystDataToAvro implementation

## Code Generation
This expression uses runtime replacement pattern and does not directly support code generation. Code generation support depends on the underlying CatalystDataToAvro expression that replaces this wrapper at query planning time.

## Examples
```sql
-- Convert struct to Avro with automatic schema inference
SELECT TO_AVRO(struct(id, name, age)) as avro_data FROM users;

-- Convert with explicit schema
SELECT TO_AVRO(user_data, '{"type":"record","name":"User","fields":[{"name":"id","type":"int"}]}') 
FROM users;
```

```scala
// DataFrame API with automatic schema
import org.apache.spark.sql.functions._
df.select(expr("to_avro(struct(id, name))").alias("avro_data"))

// With explicit schema
val schema = """{"type":"record","name":"User","fields":[{"name":"id","type":"int"}]}"""
df.select(expr(s"to_avro(user_struct, '$schema')"))
```

## See Also

- FROM_AVRO: Expression for deserializing Avro binary data back to Spark data types
- CatalystDataToAvro: The underlying implementation class that performs actual Avro serialization
- RuntimeReplaceable: The trait that enables compile-time expression replacement pattern