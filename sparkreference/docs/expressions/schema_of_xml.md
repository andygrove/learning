# SchemaOfXml

## Overview
The `SchemaOfXml` expression infers and returns the schema of XML data as a DDL-formatted string. It analyzes the structure of XML input to determine the appropriate Spark SQL data types that would be needed to represent the XML data in a structured format.

## Syntax
```sql
schema_of_xml(xml_string [, options_map])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| xml_string | STRING | The XML string to analyze for schema inference |
| options_map | MAP<STRING, STRING> | Optional map of XML parsing options (e.g., 'excludeAttribute' -> 'true') |

## Return Type
Returns a `STRING` representing the inferred schema in DDL format (e.g., "STRUCT<field1: INT, field2: STRING>").

## Supported Data Types

- Input: STRING type only for the XML parameter
- Options: MAP<STRING, STRING> for configuration parameters

## Algorithm

- Validates that the input XML string is foldable (constant expression) and not null
- Creates an `XmlInferSchema` instance with the provided options and case sensitivity settings
- Parses the XML string to infer the structural schema using Spark's XML inference engine
- Converts the inferred schema to DDL string format
- Uses `StaticInvoke` to call `XmlExpressionEvalUtils.schemaOfXml` for actual evaluation

## Partitioning Behavior
This expression does not affect partitioning since:

- It operates on constant (foldable) expressions only
- No shuffle operations are required
- Partitioning is preserved as this is a metadata operation

## Edge Cases

- **Null Input**: Throws `DataTypeMismatch` error with "UNEXPECTED_NULL" subclass if XML input is null
- **Non-foldable Input**: Throws `DataTypeMismatch` error if the XML parameter is not a constant expression
- **Invalid Data Type**: Only accepts STRING type for XML input; other types cause "UNEXPECTED_INPUT_TYPE" error
- **Malformed Parse Mode**: Throws `QueryCompilationErrors.parseModeUnsupportedError` if `DropMalformedMode` is specified
- **Non-nullable**: The expression itself is marked as non-nullable (`nullable = false`)

## Code Generation
This expression uses runtime replacement via `StaticInvoke` rather than direct code generation. It delegates to `XmlExpressionEvalUtils.schemaOfXml` method for actual evaluation, which operates in interpreted mode.

## Examples
```sql
-- Basic schema inference
SELECT schema_of_xml('<person><name>John</name><age>30</age></person>');
-- Returns: STRUCT<person: STRUCT<name: STRING, age: BIGINT>>

-- With options to exclude attributes
SELECT schema_of_xml('<p><a attr="2">1</a><a>3</a></p>', map('excludeAttribute', 'true'));
-- Returns: STRUCT<a: ARRAY<BIGINT>>
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.expr

df.select(expr("schema_of_xml('<root><field>value</field></root>')"))

// With options map
df.select(expr("schema_of_xml(xml_column, map('excludeAttribute', 'true'))"))
```

## See Also

- `from_xml` - Parses XML strings into structured data
- `to_xml` - Converts structured data to XML strings
- `schema_of_json` - Similar schema inference functionality for JSON data