# FromProtobuf

## Overview
FromProtobuf is a Spark SQL expression that converts binary Protobuf data into Spark SQL data types based on a specified message schema. It serves as a runtime-replaceable quaternary expression that delegates actual deserialization to the ProtobufDataToCatalyst implementation when the protobuf module is available.

## Syntax
```sql
FROM_PROTOBUF(data, messageName)
FROM_PROTOBUF(data, messageName, descFilePathOrOptions)  
FROM_PROTOBUF(data, messageName, descFilePath, options)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.expr
df.select(expr("FROM_PROTOBUF(protobuf_data, 'MessageName')"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| data | Expression | Binary data containing the Protobuf message to deserialize |
| messageName | Expression (StringType) | Constant string specifying the Protobuf message type name |
| descFilePath | Expression (StringType/BinaryType) | Optional constant string path to descriptor file or binary descriptor content |
| options | Expression (MapType[String,String]) | Optional constant map of configuration options for deserialization |

## Return Type
Returns structured data types (StructType) corresponding to the Protobuf message schema. The exact schema depends on the message definition and is determined at runtime by the replacement expression.

## Supported Data Types
- **Input data**: Binary data (typically stored as BinaryType columns)
- **Message name**: StringType constants only
- **Descriptor path**: StringType (file paths) or BinaryType (descriptor content)
- **Options**: MapType with StringType keys and values

## Algorithm
- Validates that messageName is a foldable StringType expression at compile time
- Evaluates messageName to extract the Protobuf message type as a UTF8String
- Processes descFilePath to either read descriptor file content or use provided binary data
- Extracts options map from ArrayBasedMapData if provided
- Dynamically loads ProtobufDataToCatalyst class via reflection and instantiates it as the replacement expression
- Delegates actual Protobuf deserialization to the replacement expression at runtime

## Partitioning Behavior
- **Preserves partitioning**: Yes, this is a row-wise transformation that does not change data distribution
- **Requires shuffle**: No, operates independently on each row without cross-partition dependencies

## Edge Cases
- **Null message name**: Throws IllegalArgumentException during replacement creation
- **Missing descriptor file**: Empty strings or null values result in None for descriptor content
- **Empty options**: Missing or empty options default to empty Map
- **Missing protobuf module**: Throws QueryCompilationErrors.protobufNotLoadedSqlFunctionsUnusable
- **Invalid Protobuf data**: Handled by the underlying ProtobufDataToCatalyst implementation
- **Non-constant arguments**: Validation fails with TypeCheckFailure for non-foldable expressions

## Code Generation
This expression implements RuntimeReplaceable and does not directly support code generation. Code generation support depends on the replacement ProtobufDataToCatalyst expression that is instantiated at runtime.

## Examples
```sql
-- Basic usage with message name only
SELECT FROM_PROTOBUF(protobuf_column, 'UserMessage') as user_data
FROM protobuf_table;

-- With descriptor file path
SELECT FROM_PROTOBUF(data, 'Person', '/path/to/schema.desc') as person
FROM binary_data;

-- With options map
SELECT FROM_PROTOBUF(
  protobuf_data, 
  'Transaction',
  MAP('recursive.fields.max.depth', '10')
) as transaction
FROM events;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.expr

// Basic deserialization
df.select(expr("FROM_PROTOBUF(protobuf_col, 'MessageType')").as("parsed_data"))

// With descriptor and options
val result = df.select(
  expr("""FROM_PROTOBUF(data, 'MyMessage', '/schema.desc', 
          MAP('option1', 'value1'))""").as("structured_data")
)
```

## See Also
- ToProtobuf - Complementary expression for serializing Spark data to Protobuf format
- from_json/to_json - Similar functionality for JSON data format
- ProtobufDataToCatalyst - The underlying implementation class for actual deserialization