# XmlToStructs

## Overview
`XmlToStructs` is a Spark Catalyst expression that parses XML strings and converts them into Spark SQL struct data types. This function enables structured querying of XML data by transforming XML content into nested struct columns that can be accessed using standard SQL operations.

## Syntax
```sql
xml_to_struct(xml_string, schema)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(xml_to_struct($"xml_column", schema))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| xml_string | StringType | The XML string to be parsed into a struct |
| schema | StructType | The target schema defining the structure of the output |

## Return Type
Returns a `StructType` that matches the provided schema parameter, containing the parsed XML data as nested fields.

## Supported Data Types

- Input: `StringType` (XML string data)

- Output: `StructType` with nested fields of various types including:
  - Primitive types (StringType, IntegerType, etc.)
  - ArrayType for XML arrays
  - Nested StructType for complex XML elements

## Algorithm

- Parses the input XML string using XML parsing libraries

- Maps XML elements and attributes to corresponding struct fields based on the provided schema

- Handles nested XML structures by creating nested struct types

- Converts XML arrays (repeated elements) into Spark ArrayType columns

- Applies type coercion to match the target schema data types

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require data shuffle as it operates on individual rows

- Maintains existing partition boundaries since it's a row-level transformation

- Can be executed in parallel across partitions without cross-partition dependencies

## Edge Cases

- Null input: Returns null when the input XML string is null

- Empty XML: Returns a struct with null fields when XML is empty or whitespace-only

- Malformed XML: Throws parsing exception or returns null based on configuration

- Schema mismatch: Fields not present in XML are set to null in the resulting struct

- Extra XML fields: XML elements not defined in schema are ignored during parsing

## Code Generation
This expression likely falls back to interpreted mode due to the complexity of XML parsing operations, which are difficult to express in generated Java code. The XML parsing logic requires external libraries that are better suited for interpreted execution.

## Examples
```sql
-- Parse XML string into struct
SELECT xml_to_struct(
  '{"teacher":"Alice","student":[{"name":"Bob","rank":1},{"name":"Charlie","rank":2}]}',
  'teacher STRING, student ARRAY<STRUCT<name: STRING, rank: INT>>'
) AS parsed_data;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.types._

val schema = StructType(Seq(
  StructField("teacher", StringType),
  StructField("student", ArrayType(StructType(Seq(
    StructField("name", StringType),
    StructField("rank", IntegerType)
  ))))
))

df.select(xml_to_struct($"xml_column", lit(schema.json)))
```

## See Also

- `from_json` - Similar function for parsing JSON strings
- `get_json_object` - Extract specific fields from JSON
- `json_tuple` - Extract multiple fields from JSON as a tuple
- XML parsing functions in the `xml_funcs` group