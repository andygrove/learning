# ToProtobuf

## Overview
The `ToProtobuf` expression converts Spark SQL struct data into Protocol Buffer (protobuf) binary format. It serves as a runtime-replaceable expression that validates input parameters and delegates actual conversion to the `CatalystDataToProtobuf` implementation. This expression enables serialization of structured data to protobuf format for interoperability with protobuf-based systems.

## Syntax
```sql
TO_PROTOBUF(data, messageName [, descFilePath] [, options])
```

```scala
// DataFrame API usage through SQL expression
df.selectExpr("TO_PROTOBUF(struct_column, 'MessageName', 'path/to/descriptor.desc') as protobuf_data")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `data` | StructType | The struct data to be converted to protobuf format |
| `messageName` | StringType (constant) | The name of the protobuf message type to use for conversion |
| `descFilePath` | StringType/BinaryType (constant, optional) | File path to protobuf descriptor file or binary descriptor content |
| `options` | MapType[String, String] (constant, optional) | Configuration options for the protobuf conversion process |

## Return Type
Returns `BinaryType` - the protobuf-encoded binary representation of the input struct data.

## Supported Data Types
- **Input data**: Must be `StructType` only
- **Message name**: `StringType` (must be foldable/constant)
- **Descriptor file**: `StringType`, `BinaryType`, or `NullType` (must be foldable/constant)
- **Options**: `MapType[StringType, StringType]` or `NullType` (must be foldable/constant)

## Algorithm
- Validates that the input data is a struct type and all parameters are constant expressions
- Extracts the message name string from the constant expression
- Reads descriptor file content (either from file path or direct binary data)
- Parses options map from the constant map expression
- Uses reflection to instantiate `CatalystDataToProtobuf` with the validated parameters
- Delegates actual protobuf conversion to the replacement expression

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-level transformation that doesn't require data movement
- **Requires shuffle**: No, operates independently on each row within partitions
- Can be applied per-partition without cross-partition dependencies

## Edge Cases
- **Null message name**: Throws `IllegalArgumentException` at runtime
- **Missing protobuf library**: Throws `QueryCompilationErrors.protobufNotLoadedSqlFunctionsUnusable`
- **Invalid descriptor file**: Handled by `ProtobufUtils.readDescriptorFileContent`
- **Empty options map**: Defaults to `Map.empty` when null or empty
- **Null descriptor file**: Treated as `None` (uses default descriptor resolution)
- **Non-struct input data**: Fails type checking with `NON_STRUCT_TYPE` error

## Code Generation
This expression uses **interpreted mode** as it's a `RuntimeReplaceable` expression. Code generation is handled by the replacement `CatalystDataToProtobuf` expression, not by `ToProtobuf` itself. The expression acts as a factory that creates the actual implementation during analysis phase.

## Examples
```sql
-- Basic usage with message name only
SELECT TO_PROTOBUF(struct_col, 'PersonMessage') as protobuf_data
FROM table_name;

-- With descriptor file path
SELECT TO_PROTOBUF(
  struct_col, 
  'PersonMessage', 
  '/path/to/person.desc'
) as protobuf_data
FROM table_name;

-- With options map
SELECT TO_PROTOBUF(
  struct_col,
  'PersonMessage',
  '/path/to/person.desc',
  map('option1', 'value1', 'option2', 'value2')
) as protobuf_data
FROM table_name;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(
  expr("TO_PROTOBUF(person_struct, 'PersonMessage', 'person.desc')").alias("protobuf_data")
)

// With multiple parameters
df.selectExpr(
  "TO_PROTOBUF(data_struct, 'MyMessage', descriptor_path, conversion_options) as proto_binary"
)
```

## See Also
- `FromProtobuf` - Converts protobuf binary data back to struct format
- `CatalystDataToProtobuf` - The actual implementation expression for protobuf conversion
- `to_json` - Similar serialization function for JSON format
- `ProtobufUtils` - Utility functions for protobuf descriptor handling