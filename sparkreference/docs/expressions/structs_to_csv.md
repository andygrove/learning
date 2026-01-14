# StructsToCsv

## Overview
The `StructsToCsv` expression converts a Spark SQL struct (row) to a CSV string representation. It uses Apache Spark's CSV writer implementation to serialize structured data into comma-separated values format with configurable options for formatting, timezone handling, and field delimiters.

## Syntax
```sql
to_csv(struct_column)
to_csv(struct_column, options_map)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(to_csv($"struct_column"))
df.select(to_csv($"struct_column", Map("delimiter" -> "|")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression (StructType) | The struct expression to convert to CSV format |
| options | Map[String, String] | CSV formatting options (delimiter, quote character, etc.) |
| timeZoneId | Option[String] | Optional timezone ID for timestamp formatting |

## Return Type
Returns `UTF8String` - a CSV formatted string representation of the input struct.

## Supported Data Types
- **Supported**: All primitive types (numeric, string, boolean, timestamp, date), arrays, maps, nested structs, and user-defined types
- **Unsupported**: `VariantType` is explicitly excluded
- **Recursive Support**: For complex types (arrays, maps, structs), all nested element types must also be supported

## Algorithm
- Validates input is a `StructType` with all field types being supported data types
- Creates a `UnivocityGenerator` instance configured with CSV options and input schema
- Uses a `CharArrayWriter` as the underlying buffer for CSV output generation
- Converts input `InternalRow` to CSV string format using the pre-configured generator
- Returns the CSV string as a `UTF8String` object

## Partitioning Behavior
- **Preserves Partitioning**: Yes, this is a row-level transformation that doesn't affect data distribution
- **Requires Shuffle**: No, operates independently on each row within partitions
- **Partition-Local**: Each partition processes its rows independently without cross-partition dependencies

## Edge Cases
- **Null Handling**: `nullIntolerant = true` and `nullable = true` - null input structs return null output
- **Empty Struct**: Empty structs produce empty CSV strings
- **Nested Nulls**: Null values within struct fields are handled according to CSV formatting rules
- **Complex Types**: Arrays and maps are serialized using CSV's complex type representation
- **Timezone Dependency**: Timestamp fields are formatted according to the specified timezone

## Code Generation
Supports **Tungsten code generation** via the `doGenCode` method. Generated code:
- Creates a reference to the expression instance in the code generation context
- Uses `nullSafeCodeGen` for efficient null checking
- Directly calls the converter function on the input value
- Avoids interpreted evaluation overhead for better performance

## Examples
```sql
-- Convert a struct to CSV with default options
SELECT to_csv(struct(id, name, salary)) as csv_row
FROM employees;

-- Convert with custom delimiter
SELECT to_csv(named_struct('id', 1, 'name', 'John', 'active', true), 
              map('delimiter', '|')) as csv_row;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.select(to_csv($"employee_struct"))

// With custom options
val csvOptions = Map("delimiter" -> "|", "quote" -> "'")
df.select(to_csv($"employee_struct", lit(csvOptions)))

// With nested structs
df.select(to_csv(struct($"id", $"name", struct($"street", $"city").as("address"))))
```

## See Also
- `CsvToStructs` - Inverse operation for parsing CSV strings to structs
- `StructsToJson` - Similar serialization expression for JSON format
- `GetStructField` - Extract individual fields from structs
- CSV data source options for file-level CSV configuration