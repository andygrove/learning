# FromProtobuf

## Overview

The `FromProtobuf` expression converts binary data in Protobuf format into its corresponding Catalyst (Spark SQL) values. It uses a Protobuf descriptor file to understand the schema and deserialize the binary data into structured Spark SQL data types.

## Syntax

```sql
FROM_PROTOBUF(data, messageName, descFilePath, options)
FROM_PROTOBUF(data, messageName, descFilePathOrOptions)  
FROM_PROTOBUF(data, messageName)
```

```scala
// DataFrame API usage would be through expr() function
df.select(expr("FROM_PROTOBUF(protobuf_column, 'MessageType', '/path/to/desc.desc', map())"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `data` | BinaryType | The Catalyst binary input column containing Protobuf-encoded data |
| `messageName` | StringType (constant) | The protobuf message name to look for in descriptor file |
| `descFilePath` | StringType/BinaryType/NullType (constant) | The Protobuf descriptor file path or binary content. Created using `protoc` with `--descriptor_set_out` and `--include_imports` options |
| `options` | MapType[StringType, StringType] (constant) | Optional map of configuration options for the conversion |

## Return Type

Returns a StructType that matches the schema defined in the specified Protobuf message definition. The exact structure depends on the Protobuf schema being deserialized.

## Supported Data Types

- **Input**: BinaryType (Protobuf-encoded binary data)
- **Output**: StructType (corresponding to the Protobuf message schema)
- **Parameters**: StringType for message name, StringType/BinaryType for descriptor file, MapType for options

## Algorithm

- Validates that all parameters are constant/literal values and have correct data types
- Extracts the message name, descriptor file content, and options from the literal expressions
- Uses reflection to dynamically load the `ProtobufDataToCatalyst` class from the Protobuf connector
- Creates an instance of the actual implementation class with the validated parameters
- The replacement expression handles the runtime conversion from Protobuf binary to Catalyst values

## Partitioning Behavior

- **Preserves partitioning**: Yes, this is a row-level transformation that doesn't change partitioning
- **Requires shuffle**: No, operates on individual rows independently
- Each partition can process its rows without coordination with other partitions

## Edge Cases

- **Null handling**: If the input data is null, the result depends on the underlying implementation
- **Empty descriptor file**: Empty string or empty byte array for descriptor file is treated as null/None
- **Invalid message name**: Throws `IllegalArgumentException` if message name is null
- **Schema mismatch**: Behavior is undefined if the actual Protobuf data doesn't match the expected schema
- **Missing Protobuf connector**: Throws `QueryCompilationErrors.protobufNotLoadedSqlFunctionsUnusable` if the Protobuf classes are not available

## Code Generation

This expression uses `RuntimeReplaceable`, which means it doesn't directly support Tungsten code generation. Instead, it creates a replacement expression (`ProtobufDataToCatalyst`) at planning time, and code generation support depends on the replacement expression's implementation.

## Examples

```sql
-- Convert Protobuf binary data to structured format
SELECT FROM_PROTOBUF(protobuf_data, 'Person', '/path/to/descriptor.desc', map()) AS person_struct
FROM protobuf_table;

-- Check for null results
SELECT FROM_PROTOBUF(s, 'Person', '/path/to/descriptor.desc', map()) IS NULL AS result 
FROM (SELECT NAMED_STRUCT('name', name, 'id', id) AS s 
      FROM VALUES ('John Doe', 1), (NULL, 2) tab(name, id));

-- Using with options
SELECT FROM_PROTOBUF(data, 'MessageType', '/desc/file.desc', 
                     map('recursive.fields.max.depth', '10')) AS parsed_data
FROM binary_protobuf_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("FROM_PROTOBUF(protobuf_column, 'Person', '/path/to/desc.desc', map())").as("person"))
```

## See Also

- `ToProtobuf` - Converts Catalyst values to Protobuf binary format
- `from_json` - Similar functionality for JSON data
- `from_avro` - Similar functionality for Avro data

---

# ToProtobuf

## Overview

The `ToProtobuf` expression converts Catalyst (Spark SQL) structured data into binary Protobuf format. It serializes Spark SQL StructType data into Protobuf binary representation using a specified message schema from a descriptor file.

## Syntax

```sql
TO_PROTOBUF(data, messageName, descFilePath, options)
TO_PROTOBUF(data, messageName, descFilePathOrOptions)
TO_PROTOBUF(data, messageName)
```

```scala
// DataFrame API usage would be through expr() function
df.select(expr("TO_PROTOBUF(struct_column, 'MessageType', '/path/to/desc.desc', map())"))
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `data` | StructType | The Catalyst structured input data to be converted to Protobuf |
| `messageName` | StringType (constant) | The protobuf message name to use for serialization |
| `descFilePath` | StringType/BinaryType/NullType (constant) | The Protobuf descriptor file path or binary content |
| `options` | MapType[StringType, StringType] (constant) | Optional map of configuration options (e.g., 'emitDefaultValues') |

## Return Type

Returns BinaryType containing the Protobuf-encoded binary representation of the input structured data.

## Supported Data Types

- **Input**: StructType (structured Spark SQL data)
- **Output**: BinaryType (Protobuf-encoded binary data)
- **Parameters**: StringType for message name, StringType/BinaryType for descriptor file, MapType for options

## Algorithm

- Validates that the input data is of StructType and all parameters are constant values with correct types
- Extracts the message name, descriptor file content, and options from the literal expressions
- Uses reflection to dynamically load the `CatalystDataToProtobuf` class from the Protobuf connector
- Creates an instance of the actual implementation class with the validated parameters
- The replacement expression handles the runtime conversion from Catalyst values to Protobuf binary

## Partitioning Behavior

- **Preserves partitioning**: Yes, this is a row-level transformation that doesn't affect partitioning
- **Requires shuffle**: No, operates on individual rows independently
- Each partition processes its rows without needing data from other partitions

## Edge Cases

- **Null handling**: If input data is null, returns null (as shown in examples)
- **Non-struct input**: Throws `TypeCheckResult.DataTypeMismatch` with "NON_STRUCT_TYPE" error
- **Invalid message name**: Throws `IllegalArgumentException` if message name is null
- **Schema mismatch**: Behavior depends on the compatibility between Catalyst struct and Protobuf message schema
- **Missing Protobuf connector**: Throws `QueryCompilationErrors.protobufNotLoadedSqlFunctionsUnusable` if Protobuf classes are not available

## Code Generation

This expression uses `RuntimeReplaceable`, so it doesn't directly support Tungsten code generation. Code generation support depends on the replacement expression (`CatalystDataToProtobuf`) created at planning time.

## Examples

```sql
-- Convert structured data to Protobuf binary
SELECT TO_PROTOBUF(person_struct, 'Person', '/path/to/descriptor.desc', map()) AS protobuf_data
FROM structured_table;

-- Using with emit default values option
SELECT TO_PROTOBUF(s, 'Person', '/path/to/descriptor.desc', map('emitDefaultValues', 'true')) IS NULL 
FROM (SELECT NULL AS s);

-- Convert struct to binary for storage/transmission
SELECT TO_PROTOBUF(NAMED_STRUCT('id', 123, 'name', 'John'), 'Person', '/desc/person.desc', map()) 
AS serialized_person;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("TO_PROTOBUF(person_struct, 'Person', '/path/to/desc.desc', map('emitDefaultValues', 'true'))").as("protobuf_binary"))
```

## See Also

- `FromProtobuf` - Converts Protobuf binary format to Catalyst values
- `to_json` - Similar functionality for JSON serialization
- `to_avro` - Similar functionality for Avro serialization