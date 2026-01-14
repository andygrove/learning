# StructsToXml

## Overview
The `StructsToXml` expression converts struct or variant data types into XML string format. It provides configurable XML serialization with timezone-aware processing and supports customizable formatting options through a parameter map.

## Syntax
```sql
to_xml(struct_column [, options_map])
```

```scala
// DataFrame API
df.select(to_xml($"struct_column"))
df.select(to_xml($"struct_column", $"options_map"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The struct or variant expression to convert to XML |
| options | Map[String, String] | Configuration options for XML formatting (optional, defaults to empty map) |
| timeZoneId | Option[String] | Timezone identifier for timestamp formatting (optional) |

## Return Type
Returns `StringType` (UTF8String) representing the XML serialization of the input struct.

## Supported Data Types

- `StructType`: Primary supported input type for structured data
- `VariantType`: Supported for semi-structured data conversion

## Algorithm

- Validates input data type is either StructType or VariantType
- Creates a lazy-initialized `StructsToXmlEvaluator` with provided options and timezone
- Delegates actual XML conversion to the evaluator's `evaluate` method
- Returns null for null inputs (null-intolerant behavior)
- Preserves timezone information through TimeZoneAwareExpression interface

## Partitioning Behavior
This expression preserves partitioning:

- Does not require shuffle operations
- Performs row-by-row transformation without changing data distribution
- Can be applied within existing partitions independently

## Edge Cases

- **Null handling**: Returns null for null inputs (nullable = true, nullIntolerant = true)
- **Type validation**: Throws DataTypeMismatch error for unsupported input types
- **Empty structs**: Handled by the underlying StructsToXmlEvaluator implementation
- **Timezone handling**: Uses provided timezone or falls back to system default for timestamp fields

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code that calls the `nullSafeEval` method for efficient execution.

## Examples
```sql
-- Convert a struct to XML
SELECT to_xml(struct(1 as id, 'John' as name)) as xml_output;

-- Convert struct with options
SELECT to_xml(struct_column, map('rootTag', 'record')) as xml_data
FROM my_table;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic conversion
df.select(to_xml($"struct_column"))

// With options
val options = Map("rootTag" -> "record", "arrayElementName" -> "item")
df.select(to_xml($"struct_column", lit(options)))

// With timezone handling (via withTimeZone method)
df.select(to_xml($"struct_with_timestamps").withTimeZone("UTC"))
```

## See Also

- `from_xml`: Inverse operation to parse XML strings into structs
- `to_json`: Similar serialization for JSON format
- `struct`: Function to create struct types for XML conversion
- XML parsing and generation functions in the `xml_funcs` group